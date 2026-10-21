"""Actual Android ARM64 serialization, sleeve converter and hooked detour.
Engine allocation, std::string assignment and libc copying are modeled; renderer
and texture loading are not emulated. Source tables are read-only.
"""
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
import json,struct,hashlib,sys,random
r=Path(__file__).parent;a=r.parent/'android';engine_path=a/'official-apk/lib/arm64-v8a/libUE4.so';engine=engine_path.read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);sys.path.insert(0,str(r));import select_team_runtime as runtime
assert hashlib.sha256(engine).hexdigest()==runtime.ENGINE_SHA
symbols={}
for path,base in [(engine_path,0),(r/'libselect_team.so',0x35000000)]:
 with path.open('rb')as f:
  elf=ELFFile(f)
  for seg in elf.iter_segments():
   if seg['p_type']=='PT_LOAD':
    lo=(base+seg['p_vaddr'])&~4095;hi=(base+seg['p_vaddr']+seg['p_memsz']+4095)&~4095;u.mem_map(lo,hi-lo);u.mem_write(base+seg['p_vaddr'],seg.data())
  if base:
   symbols={s.name:base+s['st_value']for s in elf.get_section_by_name('.dynsym').iter_symbols()}
   for section in elf.iter_sections():
    if section.name.startswith('.rela'):
     for rel in section.iter_relocations():assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
u.mem_map(0x30000000,0x4000000);u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
heap=0x31000000
stubs=set()
def stub(uc,addr,size,data):
 global heap
 x0,x1,x2=[uc.reg_read(reg)for reg in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]]
 if addr in [0x8c1bc60,0x8c1bc70]:
  if x2:u.mem_write(x0,bytes(u.mem_read(x1,x2)))
  result=x0
 elif addr==0x2f46d10:
  raw=bytes(u.mem_read(x1,x2))if x2 else b'';u.mem_write(x0,b'\0'*24)
  if len(raw)<=22:u.mem_write(x0,bytes([len(raw)*2])+raw+b'\0')
  else:
   dest=heap;heap+=(len(raw)+16+15)&~15;u.mem_write(dest,raw+b'\0');u.mem_write(x0,struct.pack('<QQQ',((len(raw)+16)&~15)|1,len(raw),dest))
  result=x0
 elif addr==0x2f37644:
  result=heap;heap+=(x0+31)&~15
 elif addr==0x2f376d4:result=0
 elif addr==0x8c1bc00:raise AssertionError('original native stack canary failed')
 else:return
 stubs.add(hex(addr));uc.reg_write(UC_ARM64_REG_X0,result);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub)
def call(addr,*args):
 regs=[UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]
 for reg,value in zip(regs,args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x32fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(addr,0x33000010,count=500000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
source=(a/'tables/dt870-PlayerAppearance.bin').read_bytes();source_hash=hashlib.sha256(source).hexdigest();records={struct.unpack_from('<Q',source,i)[0]:source[i:i+64]for i in range(0,len(source),64)}
target=89138556572074;reference=88041729329832;hair_source=88038776539586;hair_target=88044950524330
targets={target,hair_target}
assert all(pid in records for pid in [target,reference,hair_source,hair_target])
assert records[target][15]>>6==0 and records[reference][15]>>6==2
record=0x30000000;packed=record+0x100;out=record+0x1000;color=record+0x2000
# Source80 includes derived header16 bytes before the52-byte packed data.
def make_record(pid,raw=None):
 raw=records.get(pid,records[target])if raw is None else raw
 return struct.pack('<QQQ',pid,0,0)+raw[8:60]+b'\0'*4
u.mem_write(record,make_record(target));assert call(0x68d0868,record,packed)==1;assert bytes(u.mem_read(packed,52))==records[target][8:60]
# Full native character converter and accessory-vector writer execute unchanged.
def convert(raw,winter):
 u.mem_write(packed,bytes(raw));u.mem_write(out,b'\0'*0x240);u.mem_write(color,struct.pack('<III',0xffffffff,0xffffffff,0xffffffff))
 call(0x68d1fbc,out,packed,winter,0,color,color+4,color+8,0)
 return bytes(u.mem_read(out,0x210)),struct.unpack('<I',u.mem_read(out+0x50,4))[0]
conversions=[]
for mode in [0,1,2]:
 raw=bytearray(records[target][8:60]);raw[7]=(raw[7]&63)|(mode<<6)
 for winter in [0,1]:
  body,value=convert(raw,winter);assert value==([winter,0,1][mode]),(mode,winter,value)
  conversions.append({'mode':mode,'winter':winter,'native_sleeveType2':value})
# Install the exact loader trampoline, including the original first instruction.
entry=0x68d0868;cave=0xc000000;u.mem_map(cave,4096);body=engine[entry-0x4000:entry-0x4000+16]
assert body.hex()=='fd7bbfa9fd03009102600091e00301aa'
u.mem_write(cave,runtime.jump(symbols['appearance_serialize_hook'])+b'\0'*16+body[:4]+runtime.jump(entry+4));call(symbols['configure_appearance_serialize'],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
checks=0;changed_fields=[]
for pid in [target,reference,hair_source,hair_target,4522,target+(1<<32),target+(1<<24)]:
 original=make_record(pid);u.mem_write(record,original);u.mem_write(packed-8,b'\x5a'*68);assert call(entry,record,packed)==1
 result=bytes(u.mem_read(packed,52));expected=bytearray(original[24:76])
 if pid in targets:expected[7]=(expected[7]&63)|128
 assert result==expected and bytes(u.mem_read(record,80))==original
 assert bytes(u.mem_read(packed-8,8))==b'\x5a'*8 and bytes(u.mem_read(packed+52,8))==b'\x5a'*8
 checks+=1
 if pid in targets:
  for winter in [0,1]:
   original_cfg,_=convert(original[24:76],winter);new_cfg,sleeve=convert(result,winter);assert sleeve==1
   differences=[i for i in range(len(new_cfg))if original_cfg[i]!=new_cfg[i]]
   # Header/face/hair/morph values and accessories must remain identical.
   assert all(0x50<=i<0x54 for i in differences),differences
   changed_fields.append({'winter':winter,'changed_config_offsets':differences})
assert call(symbols['appearance_status'])==2
# Additional random payloads stress masks, exact full64 scope and bounds.
rng=random.Random(42013)
for i in range(100):
 pid=target if i%2 else target+(1<<32);raw=bytearray(rng.randbytes(64));original=make_record(pid,raw);u.mem_write(record,original);call(entry,record,packed);result=bytes(u.mem_read(packed,52));expected=bytearray(original[24:76])
 if pid in targets:expected[7]=(expected[7]&63)|128
 assert result==expected and bytes(u.mem_read(record,80))==original
 checks+=1
assert call(symbols['appearance_status'])==52
# The actual shirt consumer loads actor+10f0 intoW24 and forwardsW24 inW3.
# It selects kit mesh IDs independently; only the sleeveType2 argument changes.
start=0x3a0b524;stop=0x3a0b5f8;actor=0x30200000;owner=0x30300000;stack=0x32ffe000;vtable=0x30400000;capture=0x30500000
u.mem_write(actor,b'\0'*0x1400);u.mem_write(owner+0x4d8,struct.pack('<Q',actor));u.mem_write(actor,struct.pack('<Q',vtable));u.mem_write(vtable+0x6b0,struct.pack('<Q',capture));u.mem_write(vtable+0x6a8,struct.pack('<Q',capture));u.mem_write(capture,struct.pack('<I',0xd65f03c0));u.mem_write(actor+0x10f0,struct.pack('<I',1))
u.reg_write(UC_ARM64_REG_SP,stack);u.reg_write(UC_ARM64_REG_X19,owner);u.reg_write(UC_ARM64_REG_W27,0);u.emu_start(start,stop,count=1000);assert u.reg_read(UC_ARM64_REG_PC)==stop and u.reg_read(UC_ARM64_REG_W3)==1
assert hashlib.sha256((a/'tables/dt870-PlayerAppearance.bin').read_bytes()).hexdigest()==source_hash

# Execute the WHOLE original builder, with DB/resource boundaries modeled.
# Deliberately normalize returned record ID to4522: v11 must miss, v12 must work.
ctx=0x30380000;db=0x30080000;resource=0x30381000;vt=0x30382000;name_stub=0x30383000
spec=0x30600000;cfg=0x30601000;cache=db+0x32e5988;ready=db+0x32e7288
u.mem_write(ctx+0x40,struct.pack('<Q',db));u.mem_write(ctx+0x50,struct.pack('<Q',db));u.mem_write(resource,struct.pack('<Q',vt));u.mem_write(vt+0xf8,struct.pack('<Q',name_stub));u.mem_write(name_stub,struct.pack('<I',0xd65f03c0))
scenario={'id':target,'record_id':4522,'cached':False}
modeled=set()
def boundaries(uc,addr,size,data):
 x0,x1,x2,x3=[uc.reg_read(reg)for reg in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3]]
 if addr==0x82468d4:ret=ctx
 elif addr==0x8246a60:ret=1
 elif addr==0x823c338:ret=0
 elif addr==0x82449f4:
  assert x3==scenario['id'];u.mem_write(x1,make_record(scenario['record_id']));ret=1
 elif addr==0x2866634:ret=resource
 elif addr==name_stub:u.mem_write(x3,b'\0'*24);ret=0
 elif addr in [0x68f1094,0x68f4778,0x68e6d70,0x39bd940]:ret=0
 elif addr==0x8c1bca0:
  ret=0
  while u.mem_read(x0+ret,1)!=b'\0':ret+=1
 else:return
 modeled.add(hex(addr));uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundaries)
def builder_input(pid,cached,winter):
 scenario.update(id=pid,record_id=4522,cached=cached)
 raw=bytearray(0xc0);struct.pack_into('<Q',raw,8,pid);raw[0x50]=11;raw[0x51]=0;raw[0x53]=winter
 u.mem_write(spec,bytes(raw));u.mem_write(cfg-8,b'\x5a'*8+b'\0'*0x220+b'\x5a'*8)
 u.mem_write(ready,bytes([int(cached)]));u.mem_write(cache,make_record(pid))
def detour(entry,name,cave):
 body=engine[entry-0x4000:entry-0x4000+16];u.mem_map(cave,4096)
 u.mem_write(cave,runtime.jump(symbols['appearance_'+name+'_hook'])+b'\0'*16+body[:4]+runtime.jump(entry+4))
 call(symbols['configure_appearance_'+name],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
# Both baselines run before builder detour; serializer fromv11 remains installed.
builder_baselines={}
for pid in [target,target+(1<<32),hair_target,4522]:
 for cached in [False,True]:
  for winter in [0,1]:
   builder_input(pid,cached,winter);call(0x68ceb44,cfg,spec)
   builder_baselines[pid,cached,winter]=(bytes(u.mem_read(cfg,0x220)),bytes(u.mem_read(spec,0xc0)))
assert struct.unpack_from('<I',builder_baselines[target,False,0][0],0x50)[0]==0
# Exactly reproduce the base-ID mismatch, not just a synthetic serializer hit.
assert call(symbols['appearance_status'])>51 # cached full64 case still works inv11
before_total=call(symbols['appearance_status'])
detour(0x68ceb44,'build',0xc001000)
builder_checks=0
for (pid,cached,winter),(before,spec_before) in builder_baselines.items():
 builder_input(pid,cached,winter);call(0x68ceb44,cfg,spec);after=bytes(u.mem_read(cfg,0x220));expected=bytearray(before)
 if pid in targets:struct.pack_into('<I',expected,0x50,1)
 assert after==expected,(pid,cached,winter,[(hex(i),before[i],after[i])for i in range(len(after))if before[i]!=after[i]])
 assert bytes(u.mem_read(spec,0xc0))==spec_before
 assert bytes(u.mem_read(cfg-8,8))==b'\x5a'*8 and bytes(u.mem_read(cfg+0x220,8))==b'\x5a'*8
 builder_checks+=1
assert call(symbols['appearance_diagnostic'],1)==16 and call(symbols['appearance_diagnostic'],2)==8
# Test original five-instruction entity dispatcher and exact new replacement.
# Verify real function ABI, null entity behavior, mode and config forwarding;
# no relocated CBZ trampoline is called, and only sleeve u32 is changed.
entity=0x30700000;entity_vt=0x30701000;dispatch=0x30702000
u.mem_write(entity,struct.pack('<Q',entity_vt));u.mem_write(entity_vt+0x58,struct.pack('<Q',dispatch));u.mem_write(dispatch,struct.pack('<I',0xd65f03c0))
received=[]
def capture_entity(uc,addr,size,data):
 if addr==dispatch:
  received.append((uc.reg_read(UC_ARM64_REG_X0),uc.reg_read(UC_ARM64_REG_W1),uc.reg_read(UC_ARM64_REG_X2),bytes(uc.mem_read(cfg,0x220))))
u.hook_add(UC_HOOK_CODE,capture_entity)
u.mem_write(cfg,b'\x33'*0x220);call(0x68db150,entity,7,cfg);assert received[-1]==(entity,7,cfg,b'\x33'*0x220)
call(0x68db150,0,8,0);assert len(received)==1
detour(0x68db150,'entity',0xc002000)
entity_checks=0
for pid in [target,target+(1<<32),hair_target,4522]:
 for mode in [0,7,0xffffffff]:
  raw=rng.randbytes(0x220);u.mem_write(entity+0x28,struct.pack('<Q',pid));u.mem_write(cfg-8,b'\x5a'*8+raw+b'\x5a'*8)
  call(0x68db150,entity,mode,cfg);expected=bytearray(raw)
  if pid in targets:struct.pack_into('<I',expected,0x50,1)
  assert received[-1]==(entity,mode,cfg,bytes(expected))
  assert bytes(u.mem_read(cfg-8,8))==b'\x5a'*8 and bytes(u.mem_read(cfg+0x220,8))==b'\x5a'*8
  entity_checks+=1
call(0x68db150,0,9,0);assert len(received)==13
assert call(symbols['appearance_diagnostic'],3)==13 and call(symbols['appearance_diagnostic'],4)==6
report=dict(status='APPEARANCE_REQUEST_AND_ENTITY_DETOURS_PASS',device_tested=False,engine_sha256=runtime.ENGINE_SHA,appearance_table_sha256=source_hash,exact_target=str(target),reference_card=str(reference),native_modes=conversions,serialization_cases=checks,full_builder_cases=builder_checks,entity_dispatch_cases=entity_checks+1,v11_base_id_mismatch_reproduced=True,full64_lowbits_collisions_rejected=True,source_and_adjacent_buffers_preserved=True,character_config_differences=changed_fields,actual_LoadUniShirt_argument3=1,new_native_entries=['0x68ceb44','0x68db150'],entity_pc_relative_trampoline_deliberately_unused=True,hair_applied=False,stubs=sorted(stubs),modeled_builder_boundaries=sorted(modeled),limits=['Whole native builder, converter, serializer and entity dispatcher tested in Unicorn','DB/context/resource callbacks and unrelated footwear setup modeled; normalized record key4522 is a test scenario, not device-confirmed cause','Actual mesh/texture renderer and Android device untested'])
(r/'appearance-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

# v13: actual UE shirt load function executes from entry through long/short
# resource selection, immediately up to the real LoadUniShirt virtual call.
# Kit resource retrieval/availability and first virtual update are modeled.
owner=0x30800000;actor=0x30810000;shirt_vt=0x30820000;shirt_noop=0x30821000;kit_control=0x30822000
u.mem_write(owner+0x4d8,struct.pack('<Q',actor));u.mem_write(shirt_vt+0x6b0,struct.pack('<Q',shirt_noop));u.mem_write(shirt_noop,struct.pack('<I',0xd65f03c0))
shirt_boundaries=set()
def shirt_external(uc,addr,size,data):
 x0,x1,x2=[uc.reg_read(reg)for reg in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]]
 if addr==0x3a8486c:ret=kit_control
 elif addr==0x3a84aec:
  assert x0==kit_control
  # Two distinct actual selector branches: short and long resource IDs.
  u.mem_write(x2+0x190,struct.pack('<IIII',100,101,200,201));ret=0
 elif addr==0x3a0d3fc:assert x0==actor+0xe18;ret=1
 elif addr==shirt_noop:ret=0
 else:return
 shirt_boundaries.add(hex(addr));uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,shirt_external)
def shirt_input(pid,before):
 u.mem_write(actor,b'\0'*0x2000);u.mem_write(actor,struct.pack('<Q',shirt_vt));u.mem_write(actor+0x10b0,struct.pack('<Q',pid));u.mem_write(actor+0x10f0,struct.pack('<I',before))
def run_shirt(kit):
 u.reg_write(UC_ARM64_REG_X0,owner);u.reg_write(UC_ARM64_REG_X1,kit);u.reg_write(UC_ARM64_REG_SP,0x32fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010)
 u.emu_start(0x3a0b28c,0x3a0b5f8,count=500000);assert u.reg_read(UC_ARM64_REG_PC)==0x3a0b5f8
 return bytes(u.mem_read(actor,0x2000)),tuple(u.reg_read(reg)for reg in [UC_ARM64_REG_W1,UC_ARM64_REG_W2,UC_ARM64_REG_W3])
pids=[target,4522,16781738,hair_target,reference,hair_source,114758,7511,target+(1<<32),target&0xffffffff,4522+(1<<32)]
shirt_baselines={}
for pid in pids:
 for before in [0,1]:
  for kit in [0,1,5]:
   shirt_input(pid,before);shirt_baselines[pid,before,kit]=run_shirt(kit)
# Actor can be absent during teardown: native function must return unchanged.
u.mem_write(owner+0x4d8,struct.pack('<Q',0));call(0x3a0b28c,owner,1)
u.mem_write(owner+0x4d8,struct.pack('<Q',actor));detour(0x3a0b28c,'shirt',0xb000000)
shirt_checks=0
for (pid,before,kit),(old_actor,old_args) in shirt_baselines.items():
 shirt_input(pid,before);new_actor,args=run_shirt(kit);expected=bytearray(old_actor);expected_args=old_args
 if pid in targets:struct.pack_into('<I',expected,0x10f0,1);expected_args=(200,201,1)
 assert new_actor==expected,(pid,before,kit,[hex(i)for i in range(len(new_actor))if new_actor[i]!=expected[i]])
 assert args==expected_args,(pid,before,kit,args,expected_args)
 shirt_checks+=1
u.mem_write(owner+0x4d8,struct.pack('<Q',0));call(0x3a0b28c,owner,1)
assert call(symbols['appearance_shirt_status'],0)==67
assert call(symbols['appearance_shirt_status'],1)==12
assert call(symbols['appearance_shirt_status'],2)==0
assert call(symbols['appearance_shirt_status'],3)==12
assert call(symbols['appearance_seen'],2,0)==0 and call(symbols['appearance_seen'],0,64)==0
seen={call(symbols['appearance_seen'],1,i)for i in range(64)}
assert target in seen and 4522 in seen and 16781738 in seen and 114758 in seen
# Aliases verified from exact source names, not arbitrary ID bit truncation.
player_table=(a/'tables/Player.bin').read_bytes();player_names={struct.unpack_from('<Q',player_table,i+8)[0]:player_table[i+332:i+400].split(b'\0')[0].decode('utf8',errors='replace')for i in range(0,len(player_table),400)}
assert all(player_names[p]=='Cristiano Ronaldo'for p in [target,4522,16781738]);assert player_names[114758]=='Marc Cardona'
report.update(status='DIRECT_SHIRT_LOAD_RESOURCE_SELECTION_PASS',shirt_load_cases=shirt_checks+1,actual_shirt_function='0x3a0b28c',actual_LoadUniShirt_call='0x3a0b5f8',short_resource_selector_args=[100,101,0],long_resource_selector_args=[200,201,1],verified_alias_names={str(p):player_names[p]for p in [target,4522,16781738]},player_table_sha256=hashlib.sha256(player_table).hexdigest(),shader_and_mesh_render_verified=False,shirt_boundaries_modeled=sorted(shirt_boundaries),shared_alias_can_affect_other_ronaldo_cards=False,non_target_full64_cards_remain_unchanged=True,ring_buffer_wrap_and_bounds_validated=True)
report['limits'].append('Actual UE shirt function runs to the LoadUniShirt call; resource IDs100/101/200/201 are synthetic sentinels; actual meshes and device rendering unverified')
(r/'appearance-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

assert call(symbols['appearance_card_status'],0)==4 and call(symbols['appearance_card_status'],1)==4
assert call(symbols['appearance_card_status'],2)==hair_target and call(symbols['appearance_card_status'],3)==1
observed=[35207,52781658444018,70369281084452,88033407832198,88044950524330,88045487423105,88045487427597,88045755960789,89136409091415,105556874407263,105577812371605,105578617736150,105587476043161,105634720683687,105638478844821,105727599373137,105802224470740,105810009038128,106722421241113,106773960836927,106782282337313,106787919475376]
# Replay every ID from the DEVICE log through the actual full builder detour.
# Modeled appearance DB returns normalized record4522 so builder ID is decisive.
for pid in observed:
 builder_input(pid,False,0);call(0x68ceb44,cfg,spec)
 assert struct.unpack('<I',u.mem_read(cfg+0x50,4))[0]==int(pid==hair_target),pid
assert call(symbols['appearance_card_status'],0)==4 and call(symbols['appearance_card_status'],1)==5
report.update(status='OBSERVED_DEVICE_ID_REPLAY_AND_EXACT_SLEEVES_PASS',explicit_target_ids=[str(p)for p in sorted(targets)],device_log_ids_replayed=len(observed),observed_target_id=str(hair_target),old_requested_id_in_device_log=target in observed,render_id_alias_relationship_proven=False,base_aliases_disabled=True,per_card_counters_verified=True)
(r/'appearance-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

assert player_names[hair_target]=='Cristiano Ronaldo'
report['explicit_target_names']={str(p):player_names[p]for p in targets}
report['named_bases_no_longer_targeted']=report.pop('verified_alias_names')
(r/'appearance-validation.json').write_text(json.dumps(report,indent=2)+'\n')
