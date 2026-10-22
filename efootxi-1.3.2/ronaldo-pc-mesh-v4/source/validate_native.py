"""Execute five ARM64 detours and scoped original-call chain in Unicorn.
Engine bodies are modeled; native hook code, scope, FString ABI and fallback execute.
"""
from pathlib import Path
import struct,json,hashlib
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
u.mem_map(0x30000000,0x4000000);u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000);stop=0x33000010;actor=0x30000000;face=actor+0x3000;chars=actor+0x3100;closure=actor+0x4000;result=actor+0x4100;detail=actor+0x4200;holder=actor+0x4500
outer=0x39cdb10;mesh=0x39cd71c;done=0x39d3e1c;tex=0x39d3604;printf=0x428ed20;entries=[(outer,'outer'),(mesh,'load'),(done,'done'),(tex,'texture_done'),(printf,'printf')];events=[];pause=None;depth=0;inline_failure=False;format_value=0x85575c;test_foreign_tls=False
sizes={outer:0x1d0,mesh:0x100,done:0x90,tex:0x40,printf:0x60}
def putstr(addr,text):u.mem_write(addr,(text+'\0').encode('utf-16-le'))
def fstring(addr,text,dataaddr):putstr(dataaddr,text);u.mem_write(addr,struct.pack('<Qii',dataaddr,len(text)+1,len(text)+1))
def string(addr):
 p,n,cap=struct.unpack('<Qii',u.mem_read(addr,16));return text(p,n)
def text(p,n=None):
 out=[]
 for i in range(n or 200):
  q=struct.unpack('<H',u.mem_read(p+i*2,2))[0]
  if not q:break
  out.append(chr(q))
 return ''.join(out)
def finish(addr):
 sp=u.reg_read(UC_ARM64_REG_SP)
 if addr==printf:
  fp,lr=struct.unpack('<QQ',u.mem_read(sp,16));u.reg_write(UC_ARM64_REG_X29,fp);u.reg_write(UC_ARM64_REG_LR,lr)
 u.reg_write(UC_ARM64_REG_SP,sp+sizes[addr]);u.reg_write(UC_ARM64_REG_PC,u.reg_read(UC_ARM64_REG_LR))
def boundary(uc,addr,size,data):
 global pause
 if addr==outer+4:pause='outer';uc.emu_stop();return
 if addr==mesh+4:
  events.append(('mesh',string(uc.reg_read(UC_ARM64_REG_X1))));finish(mesh)
 elif addr==done+4:events.append(('done',));finish(done)
 elif addr==tex+4:events.append(('texture_done',));finish(tex)
 elif addr==printf+4:
  events.append(('printf',uc.reg_read(UC_ARM64_REG_X0),text(uc.reg_read(UC_ARM64_REG_X1)),text(uc.reg_read(UC_ARM64_REG_X2)),uc.reg_read(UC_ARM64_REG_X8),uc.reg_read(UC_ARM64_REG_X3)));finish(printf)
u.hook_add(UC_HOOK_CODE,boundary)
def call(addr,*args,x8=None):
 global pause,depth,inline_failure,test_foreign_tls
 depth+=1;assert depth<10
 for reg,v in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,v)
 if x8 is not None:u.reg_write(UC_ARM64_REG_X8,x8)
 u.reg_write(UC_ARM64_REG_SP,0x32fff000-depth*0x10000);u.reg_write(UC_ARM64_REG_LR,stop);start=addr
 while True:
  pause=None;u.emu_start(start,stop,count=200000)
  if pause is None:assert u.reg_read(UC_ARM64_REG_PC)==stop;break
  # Model the original outer function's synchronous string/path construction.
  state=u.context_save();a=u.reg_read(UC_ARM64_REG_X0);f=u.reg_read(UC_ARM64_REG_X1);name=string(f);events.append(('outer',a,name));u.mem_write(a+0x448,bytes(u.mem_read(f,16)))
  if test_foreign_tls:
   test_foreign_tls=False;u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33002000);call(printf,format_value,chars,chars,x8=holder);u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
  original_chars=struct.unpack('<Q',u.mem_read(f,8))[0]
  call(printf,format_value,original_chars,original_chars,x8=holder)
  path="SkeletalMesh'/Game/Assets/character/RealFace/SK_"+name+'_Face.SK_'+name+"_Face'";pf=actor+0x5000+depth*0x1000;fstring(pf,path,pf+0x100)
  call(mesh,a,pf)
  if inline_failure:
   inline_failure=False;u.mem_write(closure,struct.pack('<Q',a));u.mem_write(result,b'\0'*8);call(done,closure,result,detail)
  u.context_restore(state);finish(outer);start=u.reg_read(UC_ARM64_REG_PC)
 depth-=1;return u.reg_read(UC_ARM64_REG_X0)
for i,(addr,name) in enumerate(entries):
 cave=0xb000000+i*0x1000;u.mem_map(cave,4096);jump=lambda dest:struct.pack('<IIQ',0x58000050,0xd61f0200,dest);u.mem_write(cave,jump(syms['noodle_'+name+'_hook'])+b'\0'*16+engine[addr-0x4000:addr-0x4000+4]+jump(addr+4));u.mem_write(addr,struct.pack('<I',0x14000000|(((cave-addr)//4)&0x3ffffff)));call(syms['configure_'+name],0,cave+32)
target=88044950524330;checks=[]
def request(pid,name,enable=1):
 u.mem_write(actor+0x10b0,struct.pack('<Q',pid));fstring(face,name,chars);call(syms['noodle_enable'],enable);at=len(events);call(outer,actor,face);assert string(actor+0x448)==name and string(face)==name;return events[at:]
for pid in [4522,target+(1<<32),89138556572074,70373039149482,88038776539586]:
 es=request(pid,'4522');assert es[0]==('outer',actor,'4522') and es[1][2:4]==('4522','4522') and 'ND01' not in es[2][1];checks.append('other_card_'+str(pid))
for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 es=request(target,name);assert es[0]==('outer',actor,name) and es[1][2:4]==(name.replace('4522','ND01'),)*2 and es[1][4]==holder
 assert es[2][1].count('SK_ND01')==2 and 'SK_4522' not in es[2][1]
 u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(done,closure,result,detail);assert events[at:]==[('done',)]
 assert ''.join(chr(call(syms['noodle_profile_char'],i)) for i in range(64)).split('\0',1)[0]==name;checks.append('target_'+name+'_original_identity_private_assets')
# No scope survives the synchronous outer call; no unrelated async/thread request is rewritten.
putstr(chars,'4522');at=len(events);u.reg_write(UC_ARM64_REG_X3,0x12345678);call(printf,format_value,chars,chars,x8=holder);assert events[-1][2:4]==('4522','4522') and events[-1][4:]==(holder,0x12345678);checks.append('scope_closed_and_sret_varargs_preserved')
# Different format is a direct pass-through even while a target face scope is active.
format_value=0x8556d4;es=request(target,'4522');assert es[1][1]==format_value and es[1][2:4]==('4522','4522');format_value=0x85575c;checks.append('non_texture_format_passthrough')
# A failed asynchronous private load re-enters the original complete face load, with
# a suppressed scope: both mesh and texture return to original paths, without looping.
request(target,'4522ep00v0313');u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);es=events[at:];assert es[0]==('done',) and es[1]==('outer',actor,'4522ep00v0313') and es[2][2:4]==('4522ep00v0313',)*2 and 'SK_ND01' not in es[3][1];checks.append('full_original_mesh_texture_restore')
# Also exercise inline completion before the outer target scope unwinds.
inline_failure=True;es=request(target,'4522');assert len([e for e in es if e[0]=='outer'])==2 and 'SK_ND01' not in es[-1][1];checks.append('inline_failure_suppresses_nested_redirect')
es=request(target,'4522',0);assert es[1][2:4]==('4522','4522') and 'ND01' not in es[2][1];checks.append('disabled_passthrough')
u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(tex,closure,result,detail);assert events[at:]==[('texture_done',)];checks.append('texture_callback_original_cleanup')
test_foreign_tls=True;es=request(target,'4522');assert es[1][2:4]==('4522','4522') and es[2][2:4]==('ND01','ND01');checks.append('foreign_thread_cannot_inherit_target_asset_scope')
report={'status':'FIVE_ARM64_DETOURS_SCOPE_SRET_IDENTITY_FALLBACK_PASS','checks':checks,'engine_sha256':hashlib.sha256(engine).hexdigest(),'hook_sha256':hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest(),'engine_bodies_modeled':True,'renderer_cutscene_verified':False,'phone_tested':False};(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
