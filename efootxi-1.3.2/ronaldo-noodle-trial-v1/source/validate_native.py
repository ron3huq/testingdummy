"""Execute exact ARM64 hook and detours; rendering/async loader are modeled."""
from pathlib import Path
import sys,json,struct,hashlib
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
r=Path(__file__).parent;ep=Path('/workspace/analysis/my-league/android/official-apk/lib/arm64-v8a/libUE4.so');engine=ep.read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);syms={}
for path,base in [(ep,0),(r/'libnoodle_hair.so',0x35000000)]:
 with path.open('rb') as f:
  e=ELFFile(f)
  for seg in e.iter_segments():
   if seg['p_type']=='PT_LOAD':
    lo=(base+seg['p_vaddr'])&~4095;hi=(base+seg['p_vaddr']+seg['p_memsz']+4095)&~4095;u.mem_map(lo,hi-lo);u.mem_write(base+seg['p_vaddr'],seg.data())
  if base:
   syms={s.name:base+s['st_value'] for s in e.get_section_by_name('.dynsym').iter_symbols()}
   for sec in e.iter_sections():
    if sec.name.startswith('.rela'):
     for rel in sec.iter_relocations():assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
u.mem_map(0x30000000,0x4000000);u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000);stop=0x33000010
actor=0x30000000;face=actor+0x3000;chars=actor+0x3100;closure=actor+0x4000;result=actor+0x4100;detail=actor+0x4200
load=0x39cdb10;done=0x39d3e1c;events=[];target=88044950524330
for a,name,cave in [(load,'load',0xb000000),(done,'done',0xb001000)]:
 u.mem_map(cave,4096);pro=engine[a-0x4000:a-0x4000+4];hook=syms['noodle_'+name+'_hook']
 jump=lambda dest:struct.pack('<IIQ',0x58000050,0xd61f0200,dest)
 u.mem_write(cave,jump(hook)+b'\0'*16+pro+jump(a+4));u.mem_write(a,struct.pack('<I',0x14000000|(((cave-a)//4)&0x3ffffff)))
 def call(addr,*args):
  for reg,v in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,v)
  u.reg_write(UC_ARM64_REG_SP,0x32fff000);u.reg_write(UC_ARM64_REG_LR,stop);u.emu_start(addr,stop,count=100000);assert u.reg_read(UC_ARM64_REG_PC)==stop;return u.reg_read(UC_ARM64_REG_X0)
 call(syms['configure_'+name],0,cave+32)
def string(ptr):
 data,n,cap=struct.unpack('<Qii',u.mem_read(ptr,16));return bytes(u.mem_read(data,n*2)).decode('utf-16-le').rstrip('\0')
def boundary(uc,addr,size,data):
 if addr==load+4:
  a=uc.reg_read(UC_ARM64_REG_X0);f=uc.reg_read(UC_ARM64_REG_X1);events.append(('load',a,string(f)));uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x1d0)
 elif addr==done+4:
  events.append(('done',uc.reg_read(UC_ARM64_REG_X0),uc.reg_read(UC_ARM64_REG_X1),uc.reg_read(UC_ARM64_REG_X2)));uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x90)
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary)
def request(pid,name,enable=1):
 u.mem_write(actor+0x10b0,struct.pack('<Q',pid));raw=(name+'\0').encode('utf-16-le');u.mem_write(chars,raw);u.mem_write(face,struct.pack('<Qii',chars,len(name)+1,len(name)+1));call(syms['noodle_enable'],enable);before=bytes(u.mem_read(actor,0x2000));beforeface=bytes(u.mem_read(face,0x200));at=len(events);call(load,actor,face);assert bytes(u.mem_read(actor,0x2000))==before and bytes(u.mem_read(face,0x200))==beforeface;return events[at:]
checks=[]
for pid in [4522,target+(1<<32),89138556572074,70373039149482,88038776539586]:
 assert request(pid,'4522')==[('load',actor,'4522')];checks.append('other_card_'+str(pid))
for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 assert request(target,name)==[('load',actor,name.replace('4522','ND01',1))]
 u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(done,closure,result,detail);assert events[at:]==[('done',closure,result,detail)];checks.append('target_'+name)
assert request(target,'4522ep00v0313')==[('load',actor,'ND01ep00v0313')];u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);assert events[at:]==[('done',closure,result,detail),('load',actor,'4522ep00v0313')];checks.append('missing_asset_cleanup_then_original_restore')
# The fallback completion must not create a redirect/restore loop.
at=len(events);call(done,closure,result,detail);assert events[at:]==[('done',closure,result,detail)]
assert request(target,'4522',enable=0)==[('load',actor,'4522')]
assert request(target,'35496')==[('load',actor,'35496')]
assert request(target,'4522'+'x'*70)==[('load',actor,'4522'+'x'*70)]
assert request(target,'4522')==[('load',actor,'ND01')];call(syms['noodle_enable'],0);u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(done,closure,result,detail);assert events[at:]==[('done',closure,result,detail),('load',actor,'4522')];checks.append('disabled_during_async_load_restores_original')
report={'status':'ARM64_SCOPE_DETOUR_AND_FALLBACK_PASS','engine_sha256':hashlib.sha256(engine).hexdigest(),'hook_sha256':hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest(),'checks':checks,'modeled_boundaries':['original LoadRealFace body after first instruction','original completion callback body after first instruction'],'renderer_tested':False,'phone_tested':False,'stats':[call(syms['noodle_stat'],i) for i in range(11)]};(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
