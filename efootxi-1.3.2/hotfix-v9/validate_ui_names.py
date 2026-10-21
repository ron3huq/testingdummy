"""Ordinary, three AllCaps UI paths and native competition-name fields.
Original UE wrapper bodies are inspected for ABI/call edges; actual replacement
entry detours and FString allocator run. DB lookup itself is explicitly stubbed.
"""
from pathlib import Path
r=Path(__file__).parent
source=(r/'validate_presentation.py').read_text();exec(compile(source.split('for number,(entry,hook,configure)')[0],str(r/'validate_presentation.py'),'exec'))
names=json.loads((r/'myleague_custom.json').read_text())['league_names'];records={int(cid):0x30007000+i*0x400 for i,cid in enumerate(list(names)+['125'])};unknown=0x3000a000
for cid,p in records.items():u.mem_write(p,b'\x55'*0x300);u.mem_write(p,struct.pack('<H',cid));u.mem_write(p+2,b'OLD COMPETITION\0')
fall=[]
# AllCaps fallback entry+4: original first instruction subtracted0x190.
def extra_stub(uc,a,size,d):
 x0=uc.reg_read(UC_ARM64_REG_X0);cid=uc.reg_read(UC_ARM64_REG_W1)
 if a in [0x389b7c8,0x389bbd8,0x389bde0]:
  fall.append((a,x0,cid));uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x190);value=7
 elif a in [0x823cfd4,0x823d0d0]:
  value=records.get(cid,unknown);uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x20)
 else:return
 uc.reg_write(UC_ARM64_REG_X0,value);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,extra_stub)
entries=[(0x389b7c4,'name_caps_hook','configure_name_caps'),(0x389bbd4,'name_knockout_hook','configure_name_knockout'),(0x389bddc,'name_all_hook','configure_name_all'),(0x823cfd0,'compe_record_hook','configure_compe_record'),(0x823d0cc,'compe_unit_hook','configure_compe_unit')]
for number,(entry,hook,configure) in enumerate(entries):
 cave=0x0b020000+number*4096;u.mem_map(cave,4096);first=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(symbols[hook])+b'\0'*16+first+runtime.jump(entry+4));call(symbols[configure],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
checks=0
for entry,hook,configure in entries[:3]:
 u.mem_write(OUT,b'\0'*16)
 for repeat in range(3):
  for cid,name in names.items():
   call(entry,OUT,int(cid));assert u.reg_read(UC_ARM64_REG_W0)==1 and read_string(OUT)==name;checks+=1
 call(entry,OUT,125);assert u.reg_read(UC_ARM64_REG_W0)==7 and fall[-1][1:]==(OUT,125)
for entry,hook,configure in entries[3:]:
 for cid,name in names.items():
  ptr=records[int(cid)];before=bytes(u.mem_read(ptr,0x300));call(entry,INFO,int(cid));assert u.reg_read(UC_ARM64_REG_X0)==ptr
  assert bytes(u.mem_read(ptr,2))==before[:2] and bytes(u.mem_read(ptr+2+len(name)+1,0x300-3-len(name)))==before[3+len(name):]
  ptr2=call(0x8244254,ptr);assert u.reg_read(UC_ARM64_REG_X0)==ptr+2
  assert bytes(u.mem_read(ptr+2,len(name)+1))==name.encode()+b'\0';checks+=1
 ptr=records[125];before=bytes(u.mem_read(ptr,0x300));call(entry,INFO,125);assert bytes(u.mem_read(ptr,0x300))==before
# ABI/call graph from actual instructions, rather than a guessed function name.
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
cs=Cs(CS_ARCH_ARM64,CS_MODE_ARM);raw=engine.read_bytes();edges={}
for wrapper,target in [(0x40d670c,0x389b7c4),(0x40d64f4,0x389bbd4),(0x40d63e8,0x389bddc)]:
 instr=list(cs.disasm(raw[wrapper-0x4000:wrapper-0x4000+0x130],wrapper));assert any(i.mnemonic=='bl' and i.op_str=='#'+hex(target)for i in instr);edges[hex(wrapper)]=hex(target)
report=dict(status='MY_LEAGUE_NAME_PATHS_PASS',phone_verified=False,db_lookup_stubbed=True,ui_name_checks=checks,exact_names=names,original_blueprint_call_edges=edges,checks=['three actual AllCaps detours use FString*outX0 and cidW1, not ordinary-name X8 ABI','all five names survive repeated writes into reused FString storage','unknown league returns original result','native competition lookup patches only matchingID name bytes, original8244254 reads name+2','competition IDs and every byte after name terminator retained'],limits='Full Android UI/render not executed')
(r/'ui-names-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
