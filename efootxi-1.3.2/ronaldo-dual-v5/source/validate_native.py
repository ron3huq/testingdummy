"""Execute five ARM64 detours and scoped original-call chain in Unicorn.
Engine bodies are modeled; native hook code, scope, FString ABI and fallback execute.
"""
from pathlib import Path
import struct,json,hashlib
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
r=Path(__file__).parent;ep=Path('/workspace/ronaldo-work/apk/lib/arm64-v8a/libUE4.so');engine=ep.read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);syms={}
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
outer=0x39cdb10;mesh=0x39cd71c;done=0x39d3e1c;tex=0x39d3604;printf=0x45b58b0;entries=[(outer,'outer'),(mesh,'load'),(done,'done'),(tex,'texture_done'),(printf,'path')];events=[];pause=None;depth=0;inline_failure=False;format_value=0x85575c;test_foreign_tls=False
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
 u.reg_write(UC_ARM64_REG_SP,sp+sizes[addr]);u.reg_write(UC_ARM64_REG_PC,u.reg_read(UC_ARM64_REG_LR))
def boundary(uc,addr,size,data):
 global pause
 if addr==outer+4:pause='outer';uc.emu_stop();return
 if addr==mesh+4:
  p=uc.reg_read(UC_ARM64_REG_X1);name,sub,n,cap=struct.unpack('<QQii',uc.mem_read(p,24));assert name in names and sub==0 and n==0 and cap==0;events.append(('mesh',names[name]));finish(mesh)
 elif addr==done+4:events.append(('done',));finish(done)
 elif addr==tex+4:events.append(('texture_done',));finish(tex)
 elif addr==printf+4:
  out=uc.reg_read(UC_ARM64_REG_X0);p=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_X2);value=text(p,n);key=len(names)+1;names[key]=value;uc.mem_write(out,struct.pack('<QQii',key,0,0,0));events.append(('path',value,n));finish(printf)
names={};plain=True;with_texture=False;with_nul=False;foreign=False;u.hook_add(UC_HOOK_CODE,boundary)
def call(addr,*args,x8=None):
 global pause,depth,inline_failure,test_foreign_tls
 depth+=1;assert depth<10
 for reg,v in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,v)
 if x8 is not None:u.reg_write(UC_ARM64_REG_X8,x8)
 u.reg_write(UC_ARM64_REG_SP,0x32fff000-depth*0x10000);u.reg_write(UC_ARM64_REG_LR,stop);start=addr
 while True:
  pause=None
  try:u.emu_start(start,stop,count=200000)
  except UcError:
   print("PC",hex(u.reg_read(UC_ARM64_REG_PC)));raise
  if pause is None:assert u.reg_read(UC_ARM64_REG_PC)==stop;break
  # Model the original outer function's synchronous string/path construction.
  state=u.context_save();a=u.reg_read(UC_ARM64_REG_X0);f=u.reg_read(UC_ARM64_REG_X1);name=string(f);events.append(('outer',a,name));u.mem_write(a+0x448,bytes(u.mem_read(f,16)))
  prefix="" if plain else "SkeletalMesh'";suffix="" if plain else "'"
  meshpath=prefix+'/Game/Assets/character/RealFace/SK_'+name+'_Face.SK_'+name+'_Face'+suffix
  pf=actor+0x5000+depth*0x1000;pc=pf+0x100;putstr(pc,meshpath)
  if foreign:
   u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33002000);call(printf,pf,pc,len(meshpath));u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
  call(printf,pf,pc,len(meshpath)+int(with_nul));call(mesh,a,pf)
  if with_texture:
   texture="Texture2D'/Game/Assets/character/RealFace/T_"+name+'_Face_D.T_'+name+"_Face_D'";putstr(pc,texture);call(printf,pf,pc,len(texture))
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
 es=request(pid,'4522');assert all('ND01' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append('other_card_'+str(pid))
for plain in [True,False]:
 for with_nul in [True,False]:
  for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
   es=request(target,name);assert es[0]==('outer',actor,name) and es[1][1].count('SK_ND01')==2 and es[2][1]==es[1][1]
   u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
   assert ''.join(chr(call(syms['noodle_profile_char'],i)) for i in range(64)).split('\0',1)[0]==name
   checks.append(('plain_' if plain else 'classref_')+name+('_nul' if with_nul else ''))
with_texture=True;es=request(target,'4522');assert es[-1][1].count('T_ND01')==2;checks.append('mesh_and_texture_paths_same_scope_original_identity');with_texture=False
# Device-reported call shape: lower argument is FName + FString, not FString.
# No hook dereference of the FName bits, which are deliberately invalid as pointers.
fakepath=actor+0x9000;u.mem_write(fakepath,struct.pack('<QQii',0x123456789,0,0,0));names[0x123456789]='opaque_original';at=len(events);call(mesh,actor,fakepath);assert events[at:]==[('mesh','opaque_original')];checks.append('actual_24byte_FSoftObjectPath_is_opaque')
# Scope ended; arbitrary/foreign paths and other threads cannot inherit it.
for p in ['/Game/Assets/character/RealFace/SK_4522_Face.SK_4522_Face','/Game/Assets/character/Body/SK_Base_Face.SK_Base_Face']:
 putstr(chars,p);at=len(events);call(printf,holder,chars,len(p));assert events[-1][1]==p
checks.append('closed_scope_passthrough')
es=request(target,'9999');assert 'ND01' not in es[1][1];checks.append('unknown_variant_passthrough')
es=request(target,'4522',0);assert 'ND01' not in es[1][1];checks.append('disabled_passthrough')
foreign=True;es=request(target,'4522');assert 'ND01' not in es[1][1] and 'ND01' in es[2][1];foreign=False;checks.append('foreign_thread_passthrough')
request(target,'4522ep00v0313');u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);es=events[at:];assert es[0]==('done',) and 'ND01' not in es[-1][1];checks.append('async_failed_mesh_full_original_restore')
inline_failure=True;es=request(target,'4522');assert len([e for e in es if e[0]=='outer'])==2 and 'ND01' not in es[-1][1];checks.append('inline_failed_mesh_no_redirect_loop')
u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(tex,closure,result,detail);assert events[at:]==[('texture_done',)];checks.append('texture_callback_original_cleanup')
# Second exact Card ID has an independent namespace; no change to original identity.
second=89135066911146
for plain in [True,False]:
 for with_nul in [True,False]:
  for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
   with_texture=True;es=request(second,name);with_texture=False
   assert es[1][1].count('SK_ND06')==2 and es[-1][1].count('T_ND06')==2
   assert all('ND01' not in e[1] for e in es if e[0] in ('mesh','path'))
   u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
   checks.append('second_exact_card_'+name+str(plain)+str(with_nul))
for pid in [second+(1<<32),second-1,second+1,second&0xffffffff]:
 es=request(pid,'4522');assert all('ND06' not in e[1] and 'ND01' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append('second_negative_full_id_'+str(pid))
for card,private in [(target,'ND01'),(second,'ND06'),(target,'ND01'),(second,'ND06')]:
 es=request(card,'4522ep00v0313');assert es[1][1].count('SK_'+private)==2;checks.append('alternate_card_namespace_'+str(card))
request(second,'4522ep00v0313');u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);assert 'ND06' not in events[-1][1];checks.append('second_async_null_callback_fallback')
es=request(second,'4522',0);assert 'ND06' not in es[1][1];checks.append('second_disabled_passthrough')
foreign=True;es=request(second,'4522');assert 'ND06' not in es[1][1] and 'ND06' in es[2][1];foreign=False;checks.append('second_foreign_thread_passthrough')
# Interleaved asynchronous callbacks for two distinct actor objects.
first_actor=actor;second_actor=actor+0x12000
es=request(target,'4522');assert es[1][1].count('SK_ND01')==2
actor=second_actor;es=request(second,'4522');assert es[1][1].count('SK_ND06')==2
before_callbacks=call(syms['noodle_stat'],3)
u.mem_write(result,struct.pack('<Q',0x30080000));u.mem_write(closure,struct.pack('<Q',second_actor));call(done,closure,result,detail)
u.mem_write(closure,struct.pack('<Q',first_actor));call(done,closure,result,detail)
assert call(syms['noodle_stat'],3)==before_callbacks+2;actor=first_actor
checks.append('two_actors_interleaved_reverse_order_callbacks')
report={'status':'SOFTPATH_ABI_AND_FIVE_ARM64_DETOURS_PASS','checks':checks,'engine_sha256':hashlib.sha256(engine).hexdigest(),'hook_sha256':hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest(),'engine_bodies_modeled':True,'renderer_cutscene_verified':False,'phone_tested':False};(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
