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
 if pid==target:expected[7]=(expected[7]&63)|128
 assert result==expected and bytes(u.mem_read(record,80))==original
 assert bytes(u.mem_read(packed-8,8))==b'\x5a'*8 and bytes(u.mem_read(packed+52,8))==b'\x5a'*8
 checks+=1
 if pid==target:
  for winter in [0,1]:
   original_cfg,_=convert(original[24:76],winter);new_cfg,sleeve=convert(result,winter);assert sleeve==1
   differences=[i for i in range(len(new_cfg))if original_cfg[i]!=new_cfg[i]]
   # Header/face/hair/morph values and accessories must remain identical.
   assert all(0x50<=i<0x54 for i in differences),differences
   changed_fields.append({'winter':winter,'changed_config_offsets':differences})
assert call(symbols['appearance_status'])==1
# Additional random payloads stress masks, exact full64 scope and bounds.
rng=random.Random(42013)
for i in range(100):
 pid=target if i%2 else target+(1<<32);raw=bytearray(rng.randbytes(64));original=make_record(pid,raw);u.mem_write(record,original);call(entry,record,packed);result=bytes(u.mem_read(packed,52));expected=bytearray(original[24:76])
 if pid==target:expected[7]=(expected[7]&63)|128
 assert result==expected and bytes(u.mem_read(record,80))==original
 checks+=1
assert call(symbols['appearance_status'])==51
# The actual shirt consumer loads actor+10f0 intoW24 and forwardsW24 inW3.
# It selects kit mesh IDs independently; only the sleeveType2 argument changes.
start=0x3a0b524;stop=0x3a0b5f8;actor=0x30200000;owner=0x30300000;stack=0x32ffe000;vtable=0x30400000;capture=0x30500000
u.mem_write(actor,b'\0'*0x1400);u.mem_write(owner+0x4d8,struct.pack('<Q',actor));u.mem_write(actor,struct.pack('<Q',vtable));u.mem_write(vtable+0x6b0,struct.pack('<Q',capture));u.mem_write(vtable+0x6a8,struct.pack('<Q',capture));u.mem_write(capture,struct.pack('<I',0xd65f03c0));u.mem_write(actor+0x10f0,struct.pack('<I',1))
u.reg_write(UC_ARM64_REG_SP,stack);u.reg_write(UC_ARM64_REG_X19,owner);u.reg_write(UC_ARM64_REG_W27,0);u.emu_start(start,stop,count=1000);assert u.reg_read(UC_ARM64_REG_PC)==stop and u.reg_read(UC_ARM64_REG_W3)==1
assert hashlib.sha256((a/'tables/dt870-PlayerAppearance.bin').read_bytes()).hexdigest()==source_hash
report=dict(status='APPEARANCE_SERIALIZE_DETOUR_PASS',device_tested=False,engine_sha256=runtime.ENGINE_SHA,appearance_table_sha256=source_hash,exact_target=str(target),reference_card=str(reference),native_modes=conversions,serialization_cases=checks,full64_lowbits_collisions_rejected=True,source_and_adjacent_buffers_preserved=True,character_config_differences=changed_fields,actual_LoadUniShirt_argument3=1,source_fields_changed='only bits62..63 of packed appearance firstu64, in an output copy',hair_applied=False,hair_target=str(hair_target),hair_source=str(hair_source),stubs=sorted(stubs),limits=['Actual52-byte engine serializer, full native sleeve converter and actual virtual shirt-call setup executed in Unicorn','libc copying, allocation and std::string assignment modeled; source derived header synthetic except exact full64 ID','Native mesh/texture renderer and Android device untested','Hair/face fields unchanged; exact hair transplant not implemented'])
(r/'appearance-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
