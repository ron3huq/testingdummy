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
outer=0x39cdb10;mesh=0x39cd71c;done=0x39d3e1c;tex=0x39d3604;printf=0x45b58b0;bake=0x39cb75c;entries=[(0x3a908a0,'player_name'),(bake,'bake'),(outer,'outer'),(mesh,'load'),(done,'done'),(tex,'texture_done'),(printf,'path')];events=[];pause=None;depth=0;inline_failure=False;format_value=0x85575c;test_foreign_tls=False
sizes={0x3a908a0:0x190,bake:0x1b0,outer:0x1d0,mesh:0x100,done:0x90,tex:0x40,printf:0x60}
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
 if addr==0x3a908a4:events.append(('original_player_name',uc.reg_read(UC_ARM64_REG_X1)));finish(0x3a908a0);return
 if addr==0x42ccbbc:
  uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return # QuantizeSize: exact requested byte size
 if addr==0x42cca20:
  uc.reg_write(UC_ARM64_REG_X0,0x30280000);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return # FMemory::Realloc boundary
 if addr==outer+4:pause='outer';uc.emu_stop();return
 if addr==mesh+4:
  p=uc.reg_read(UC_ARM64_REG_X1);name,sub,n,cap=struct.unpack('<QQii',uc.mem_read(p,24));assert name in names and sub==0 and n==0 and cap==0;events.append(('mesh',names[name]));finish(mesh)
 elif addr==done+4:events.append(('done',));finish(done)
 elif addr==tex+4:
  a=struct.unpack('<Q',uc.mem_read(uc.reg_read(UC_ARM64_REG_X0),8))[0];p=struct.unpack('<Q',uc.mem_read(uc.reg_read(UC_ARM64_REG_X1),8))[0];uc.mem_write(a+0x1a40,struct.pack('<Q',p));events.append(('texture_done',));finish(tex)
 elif addr==bake+4:
  events.append(('bake',uc.reg_read(UC_ARM64_REG_X0)));finish(bake)
 elif addr==0x63233e8:
  uc.reg_write(UC_ARM64_REG_X0,0x30180000);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 elif addr==0x4414bec:
  dst=uc.reg_read(UC_ARM64_REG_X0);src=uc.reg_read(UC_ARM64_REG_X1);word=bytes(uc.mem_read(src,50)).split(b'\0')[0].decode();key=next((k for k,v in names.items() if v==word),len(names)+1);names[key]=word;uc.mem_write(dst,struct.pack('<Q',key));uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 elif addr==0x59b8644:
  key=uc.reg_read(UC_ARM64_REG_X1);events.append(('set_texture',uc.reg_read(UC_ARM64_REG_X0),names[key],uc.reg_read(UC_ARM64_REG_X2)));uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 elif addr==printf+4:
  out=uc.reg_read(UC_ARM64_REG_X0);p=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_X2);value=text(p,n);key=len(names)+1;names[key]=value;uc.mem_write(out,struct.pack('<QQii',key,0,0,0));events.append(('path',value,n));finish(printf)
path_name_override=None
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
  path_name=path_name_override or name
  meshpath=prefix+'/Game/Assets/character/RealFace/SK_'+path_name+'_Face.SK_'+path_name+'_Face'+suffix
  pf=actor+0x5000+depth*0x1000;pc=pf+0x100;putstr(pc,meshpath)
  if foreign:
   u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33002000);call(printf,pf,pc,len(meshpath));u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
  call(printf,pf,pc,len(meshpath)+int(with_nul));call(mesh,a,pf)
  if with_texture:
   texture="Texture2D'/Game/Assets/character/RealFace/T_"+path_name+'_Face_D.T_'+path_name+"_Face_D'";putstr(pc,texture);call(printf,pf,pc,len(texture))
  if inline_failure:
   inline_failure=False;u.mem_write(closure,struct.pack('<Q',a));u.mem_write(result,b'\0'*8);call(done,closure,result,detail)
  u.context_restore(state);finish(outer);start=u.reg_read(UC_ARM64_REG_PC)
 depth-=1;return u.reg_read(UC_ARM64_REG_X0)
for i,(addr,name) in enumerate(entries):
 cave=0xb000000+i*0x1000;u.mem_map(cave,4096);jump=lambda dest:struct.pack('<IIQ',0x58000050,0xd61f0200,dest);u.mem_write(cave,jump(syms['noodle_'+name+'_hook'])+b'\0'*16+engine[addr-0x4000:addr-0x4000+4]+jump(addr+4));u.mem_write(addr,struct.pack('<I',0x14000000|(((cave-addr)//4)&0x3ffffff)));call(syms['configure_'+name],0,cave+32)

target=88044950524330;checks=[]
def request(pid,name,enable=1):
 u.mem_write(actor+0x10b0,struct.pack('<Q',pid));fstring(face,name,chars);call(syms['noodle_enable'],enable);at=len(events);call(outer,actor,face);assert string(actor+0x448)==name and string(face)==name;return events[at:]
for pid in [4522,target+(1<<32),89138556572074,70373039149482]:
 es=request(pid,'4522');assert all('NF01' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append('other_card_'+str(pid))
for plain in [True,False]:
 for with_nul in [True,False]:
  for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
   es=request(target,name);assert es[0]==('outer',actor,name) and es[1][1].count('SK_NF01')==2 and es[2][1]==es[1][1]
   u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
   assert ''.join(chr(call(syms['noodle_profile_char'],i)) for i in range(64)).split('\0',1)[0]==name
   checks.append(('plain_' if plain else 'classref_')+name+('_nul' if with_nul else ''))
with_texture=True;es=request(target,'4522');assert es[-1][1].count('T_NF01')==2;checks.append('mesh_and_texture_paths_same_scope_original_identity');with_texture=False
# Device-reported call shape: lower argument is FName + FString, not FString.
# No hook dereference of the FName bits, which are deliberately invalid as pointers.
fakepath=actor+0x9000;u.mem_write(fakepath,struct.pack('<QQii',0x123456789,0,0,0));names[0x123456789]='opaque_original';at=len(events);call(mesh,actor,fakepath);assert events[at:]==[('mesh','opaque_original')];checks.append('actual_24byte_FSoftObjectPath_is_opaque')
# Scope ended; arbitrary/foreign paths and other threads cannot inherit it.
for p in ['/Game/Assets/character/RealFace/SK_4522_Face.SK_4522_Face','/Game/Assets/character/Body/SK_Base_Face.SK_Base_Face']:
 putstr(chars,p);at=len(events);call(printf,holder,chars,len(p));assert events[-1][1]==p
checks.append('closed_scope_passthrough')
es=request(target,'9999');assert 'NF01' not in es[1][1];checks.append('unknown_variant_passthrough')
es=request(target,'4522',0);assert 'NF01' not in es[1][1];checks.append('disabled_passthrough')
foreign=True;es=request(target,'4522');assert 'NF01' not in es[1][1] and 'NF01' in es[2][1];foreign=False;checks.append('foreign_thread_passthrough')
request(target,'4522ep00v0313');u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);es=events[at:];assert es[0]==('done',) and 'NF01' not in es[-1][1];checks.append('async_failed_mesh_full_original_restore')
inline_failure=True;es=request(target,'4522');assert len([e for e in es if e[0]=='outer'])==2 and 'NF01' not in es[-1][1];checks.append('inline_failed_mesh_no_redirect_loop')
u.mem_write(result,struct.pack('<Q',0x30080000));at=len(events);call(tex,closure,result,detail);assert events[at:]==[('texture_done',)];checks.append('texture_callback_original_cleanup')
# Second exact Card ID has an independent namespace; no change to original identity.
second=89135066911146
for plain in [True,False]:
 for with_nul in [True,False]:
  for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
   with_texture=True;es=request(second,name);with_texture=False
   assert es[1][1].count('SK_ND06')==2 and es[-1][1].count('T_ND06')==2
   assert all('NF01' not in e[1] for e in es if e[0] in ('mesh','path'))
   u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
   checks.append('second_exact_card_'+name+str(plain)+str(with_nul))
for pid in [second+(1<<32),second-1,second+1,second&0xffffffff]:
 es=request(pid,'4522');assert all('ND06' not in e[1] and 'NF01' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append('second_negative_full_id_'+str(pid))
for card,private in [(target,'NF01'),(second,'ND06'),(target,'NF01'),(second,'ND06')]:
 es=request(card,'4522ep00v0313');assert es[1][1].count('SK_'+private)==2;checks.append('alternate_card_namespace_'+str(card))
request(second,'4522ep00v0313');u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);assert 'ND06' not in events[-1][1];checks.append('second_async_null_callback_fallback')
es=request(second,'4522',0);assert 'ND06' not in es[1][1];checks.append('second_disabled_passthrough')
foreign=True;es=request(second,'4522');assert 'ND06' not in es[1][1] and 'ND06' in es[2][1];foreign=False;checks.append('second_foreign_thread_passthrough')
# Interleaved asynchronous callbacks for two distinct actor objects.
first_actor=actor;second_actor=actor+0x12000
es=request(target,'4522');assert es[1][1].count('SK_NF01')==2
actor=second_actor;es=request(second,'4522');assert es[1][1].count('SK_ND06')==2
before_callbacks=call(syms['noodle_stat'],3)
u.mem_write(result,struct.pack('<Q',0x30080000));u.mem_write(closure,struct.pack('<Q',second_actor));call(done,closure,result,detail)
u.mem_write(closure,struct.pack('<Q',first_actor));call(done,closure,result,detail)
assert call(syms['noodle_stat'],3)==before_callbacks+2;actor=first_actor
checks.append('two_actors_interleaved_reverse_order_callbacks')
# New supplied heads: same exact64, thread, path and fallback constraints.
for newcard,profile in [(106781745353130,'ND13'),(106734785925546,'NF27')]:
 for plain in [True,False]:
  for with_nul in [True,False]:
   for name in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
    with_texture=True;es=request(newcard,name);with_texture=False
    assert es[1][1].count('SK_'+profile)==2 and es[-1][1].count('T_'+profile)==2
    assert struct.unpack('<Q',u.mem_read(actor+0x10b0,8))[0]==newcard
    u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
    checks.append(profile+'_mesh_texture_'+name+str(plain)+str(with_nul))
 for pid in [newcard-1,newcard+1,newcard+(1<<32),newcard&0xffffffff]:
  es=request(pid,'4522');assert all('ND' not in e[1] and 'NF' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append(profile+'_negative_exact64_'+str(pid))
 es=request(newcard,'4522',0);assert profile not in es[1][1];checks.append(profile+'_disabled_passthrough')
 foreign=True;es=request(newcard,'4522');assert profile not in es[1][1] and profile in es[2][1];foreign=False;checks.append(profile+'_foreign_thread')
 request(newcard,'4522ep00v0313');u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);assert profile not in events[-1][1];checks.append(profile+'_async_fallback')
for newcard,profile in [(105765448873424,'NFJR'),(88045755960841,'NDXS'),(88038776539586,'NDDB'),(105643042189511,'NDHD'),(106728863696709,'NDHH'),(105848932271764,'NDPQ'),(105874433662542,'NDTL'),(88033139360669,'NDSP'),(106726716084650,'ND08')]:
 for plain in [True,False]:
  for with_nul in [True,False]:
   for name in ['200ep00v0999','4522','100001lg00v1100']:
    with_texture=True;es=request(newcard,name);with_texture=False
    assert es[1][1].count('SK_'+profile+'ep00v0313')==2 and es[-1][1].count('T_'+profile+'ep00v0313')==2
    assert string(actor+0x448)==name and struct.unpack('<Q',u.mem_read(actor+0x10b0,8))[0]==newcard
    u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(done,closure,result,detail)
    checks.append(profile+'_foreign_original_identity_'+name+str(plain)+str(with_nul))
 for pid in [newcard-1,newcard+1,newcard+(1<<32),newcard&0xffffffff]:
  es=request(pid,'4522');assert all('ND' not in e[1] and 'NF' not in e[1] for e in es if e[0] in ('mesh','path'));checks.append(profile+'_negative_exact64_'+str(pid))
 es=request(newcard,'200ep00v0999',0);assert profile not in es[1][1];checks.append(profile+'_disabled')
 foreign=True;es=request(newcard,'200ep00v0999');assert profile not in es[1][1] and profile in es[2][1];foreign=False;checks.append(profile+'_thread')
 request(newcard,'200ep00v0999');u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,b'\0'*8);at=len(events);call(done,closure,result,detail);assert events[-1][1].count('200ep00v0999')==2;checks.append(profile+'_fallback_restores_exact_foreign_face')
 for bad in ['../200','123_'+('a'*20),'9'*63]:
  es=request(newcard,bad);assert all(profile not in e[1] for e in es if e[0] in ('mesh','path'));checks.append(profile+'_malformed_original_'+str(len(bad)))
for card,private in [(target,'NF01'),(second,'ND06'),(106781745353130,'ND13'),(106734785925546,'NF27')]:
 for path_name_override in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
  with_texture=True;es=request(card,'4522');with_texture=False
  assert es[1][1].count('SK_'+private+path_name_override[4:])==2 and es[-1][1].count('T_'+private+path_name_override[4:])==2
  assert string(actor+0x448)=='4522';checks.append('v7_outer_base_and_formatted_profile_'+private+path_name_override)
for card,private in [(105765448873424,'NFJR'),(88045755960841,'NDXS'),(88038776539586,'NDDB'),(105643042189511,'NDHD'),(106728863696709,'NDHH'),(105848932271764,'NDPQ'),(105874433662542,'NDTL'),(88033139360669,'NDSP'),(106726716084650,'ND08')]:
 path_name_override='200ep00v0999';with_texture=True;es=request(card,'200');with_texture=False
 assert es[1][1].count('SK_'+private+'ep00v0313')==2 and es[-1][1].count('T_'+private+'ep00v0313')==2
 assert string(actor+0x448)=='200';checks.append('foreign_base_and_formatted_profile_'+private)
path_name_override=None
# Execute the REAL engine face-texture setter, modeling FName interning and UMaterial update only.
protected=[target,106734785925546,105765448873424,105643042189511,106726716084650]
plain=True;with_nul=False
for card in protected:
 for special in [0,1]:
  with_texture=True;request(card,'4522ep00v0313');with_texture=False
  u.mem_write(actor+0x1a5d,bytes([special]));u.mem_write(actor+0x1aa0,struct.pack('<Q',0x30090000));u.mem_write(actor+0x1ab8,struct.pack('<Q',0x30091000))
  u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(tex,closure,result,detail)
  start=len(events);call(bake,actor);es=events[start:];assert es[0]==('bake',actor);assert es[1:]==[('set_texture',0x30091000 if special else 0x30090000,'BaseColorMap' if special else 'faceBaseColor',0x30080000)],es
  checks.append('real_engine_setter_after_bake_'+str(card)+'_'+str(special))
  mid=actor+(0x1ab8 if special else 0x1aa0);saved=bytes(u.mem_read(mid,8));u.mem_write(mid,b'\0'*8);start=len(events);before=call(syms['noodle_stat'],26);call(bake,actor);assert events[start:]==[('bake',actor)] and call(syms['noodle_stat'],26)==before;u.mem_write(mid,saved);checks.append('null_material_no_write_'+str(card)+str(special))
  # A stale/replaced texture must never be restored.
  u.mem_write(actor+0x1a40,struct.pack('<Q',0x30080008));start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('bake_stale_texture_passthrough_'+str(card)+str(special))
for card in [89135066911146,106781745353130,88038776539586,106728863696709,105874433662542,88033139360669,88045755960841,105848932271764,target+(1<<32)]:
 with_texture=True;request(card,'4522ep00v0313');with_texture=False;u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000));call(tex,closure,result,detail);start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('approved_or_foreign_no_material_write_'+str(card))
with_texture=False;request(target,'4522');u.mem_write(closure,struct.pack('<Q',actor));call(tex,closure,result,detail);start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('no_private_texture_request_no_material_write')
with_texture=True;request(target,'4522');with_texture=False;call(tex,closure,result,detail);call(syms['noodle_enable'],0);start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('disabled_no_material_write')
# Device log regression: NO texture request/callback, but a valid private MIC exists on the mesh.
meshobj=0x30100000;mic=0x30110000;texobj=0x30120000;matarray=0x30130000;texarray=0x30140000
mapping={target:'NF01',106734785925546:'NF27',105765448873424:'NFJR',105643042189511:'NDHD',88045755960841:'NDXS',105848932271764:'NDPQ',88033139360669:'NDSP',106726716084650:'ND08'}
def intern_key(word):
 key=next((k for k,v in names.items() if v==word),len(names)+1);names[key]=word;return key
def fake_material(card,wrong_name=False,missing=False,invalid=False):
 u.mem_write(meshobj+0x10,struct.pack('<Q',0x30190000));u.mem_write(0x30180038,struct.pack('<I',0));u.mem_write(0x30190030,struct.pack('<Qii',0x301a0000,1,1));u.mem_write(0x301a0000,struct.pack('<Q',0x30180030))
 u.mem_write(meshobj+0xd8,struct.pack('<Qii',matarray,33 if invalid else 2,2));u.mem_write(matarray,struct.pack('<Q',mic)+b'\0'*72)
 key=intern_key('BaseColorMap');u.mem_write(mic+0x100,struct.pack('<Qii',texarray,0 if missing else 1,1));u.mem_write(mic+0xd0,b'\0'*8)
 u.mem_write(texarray,struct.pack('<QB3xiQ16s',key,2,-1,texobj,b'\0'*16));name='T_'+mapping[card]+'ep00v0313_Face_D';u.mem_write(texobj+0x18,struct.pack('<Q',intern_key('T_Original_Face_D' if wrong_name else name)))
for card in protected:
 with_texture=False;request(card,'4522ep00v0313');fake_material(card);u.mem_write(actor+0x1a40,b'\0'*8);u.mem_write(actor+0x1a5d,b'\0');u.mem_write(actor+0x1aa0,struct.pack('<Q',0x30090000));u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',meshobj));before=call(syms['noodle_stat'],32);call(done,closure,result,detail);assert call(syms['noodle_stat'],32)==before+1,(card,[call(syms['noodle_stat'],i) for i in range(28,33)])
 start=len(events);call(bake,actor);assert events[start:]==[('bake',actor),('set_texture',0x30090000,'faceBaseColor',texobj)],events[start:];assert struct.unpack('<Q',u.mem_read(actor+0x1a40,8))[0]==0
 checks.append('mesh_default_without_texture_callback_'+str(card))
for kind in ['wrong_name','missing','invalid','wrong_class']:
 request(target,'4522ep00v0313');fake_material(target,wrong_name=kind=='wrong_name',missing=kind=='missing',invalid=kind=='invalid');u.mem_write(result,struct.pack('<Q',meshobj));
 if kind=='wrong_class':u.mem_write(meshobj+0x10,b'\0'*8)
 before=call(syms['noodle_stat'],32);call(done,closure,result,detail);assert call(syms['noodle_stat'],32)==before;start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('mesh_default_fail_closed_'+kind)
# Whole-actor diff: native body skin selector and its dirty flag are the ONLY writes.
for card in [88045755960841,105848932271764,88033139360669,target,88045755960841+(1<<32)]:
 for skin in [1,4,6]:
  request(card,'4522ep00v0313');u.mem_write(actor+0x42c,struct.pack('<I',skin));u.mem_write(actor+0x1a6b,b'\xa4');before=bytes(u.mem_read(actor,0x2000));start=len(events);call(bake,actor);after=bytes(u.mem_read(actor,0x2000));wanted=bytearray(before)
  if card in [88045755960841,105848932271764,88033139360669] and skin!=6:wanted[0x42c:0x430]=struct.pack('<I',6);wanted[0x1a6b]=1
  assert after==bytes(wanted),(card,skin);checks.append('whole_actor_body_skin_only_'+str(card)+'_'+str(skin))
# Execute the real native selector, including range validation and Body/Lowbody family.
config=0x30160000
u.mem_write(actor+0x42c,struct.pack('<I',6))
for low in [0,1]:
 u.mem_write(config+0x95e,bytes([low]));u.reg_write(UC_ARM64_REG_X19,actor);u.reg_write(UC_ARM64_REG_X27,config);u.reg_write(UC_ARM64_REG_SP,0x32fff000);u.emu_start(0x39cac7c,0x39cacb8,count=100);assert u.reg_read(UC_ARM64_REG_W1)==6;family=text(u.reg_read(UC_ARM64_REG_X2));assert family in ['Body','Lowbody'],family;checks.append('real_native_skin6_texture_family_'+family)
# Regression v11 on device: private texture exists, BOTH actor MID caches NULL.
# Model only the component virtual Get/SetMaterial boundary, preserving hair slot1.
comp=0x30200000;othercomp=0x30210000;vt=0x30220000;ref=0x30230000
getstub=0x33008000;setstub=0x33008010;slots_live={};set_fail=False
def material_boundary(uc,addr,size,data):
 if addr not in [getstub,setstub]:return
 c=uc.reg_read(UC_ARM64_REG_X0);idx=uc.reg_read(UC_ARM64_REG_W1);assert idx==0
 if addr==getstub:uc.reg_write(UC_ARM64_REG_X0,slots_live[c][idx])
 else:
  m=uc.reg_read(UC_ARM64_REG_X2);events.append(('set_material',c,idx,m))
  if not set_fail:slots_live[c][idx]=m
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,material_boundary)
u.mem_write(vt+0x588,struct.pack('<QQ',getstub,setstub))
for card in protected:
 for route in ['indirect','alternate','both','duplicate']:
  request(card,'4522ep00v0313');fake_material(card);u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',meshobj));call(done,closure,result,detail)
  u.mem_write(actor+0x1aa0,b'\0'*8);u.mem_write(actor+0x1ab8,b'\0'*8)
  for c in [comp,othercomp]:u.mem_write(c,struct.pack('<Q',vt));u.mem_write(c+0x468,struct.pack('<Q',meshobj));slots_live[c]=[0x30099900,0x30099910]
  u.mem_write(ref,struct.pack('<Q',comp));u.mem_write(actor+0x1a70,struct.pack('<Q',ref if route!='alternate' else 0));u.mem_write(actor+0x228,struct.pack('<Q',comp if route=='duplicate' else othercomp if route in ['alternate','both'] else 0))
  cs=[othercomp] if route=='alternate' else [comp,othercomp] if route=='both' else [comp]
  start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)]+[('set_material',c,0,mic) for c in cs],events[start:]
  assert all(slots_live[c]==[mic,0x30099910] for c in cs)
  checks.append('null_actor_MIDs_bind_actual_head_'+str(card)+'_'+route)
  start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('head_material_idempotent_'+str(card)+'_'+route)
  # Engine replaces slot0 again; next bake restores it without touching hair.
  for c in cs:slots_live[c][0]=0x30099900
  start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)]+[('set_material',c,0,mic) for c in cs];checks.append('head_override_replaced_after_bake_'+str(card)+'_'+route)
# Bind immediately after successful async mesh callback, not only later bake.
for card in protected:
 request(card,'4522ep00v0313');fake_material(card)
 u.mem_write(comp+0x468,struct.pack('<Q',meshobj));u.mem_write(ref,struct.pack('<Q',comp));u.mem_write(actor+0x1a70,struct.pack('<Q',ref));u.mem_write(actor+0x228,b'\0'*8);u.mem_write(actor+0x1aa0,b'\0'*8);u.mem_write(actor+0x1ab8,b'\0'*8);slots_live[comp]=[0x30099900,0x30099910]
 u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',meshobj));start=len(events);before=call(syms['noodle_stat'],46);call(done,closure,result,detail)
 assert events[start:]==[('done',),('set_material',comp,0,mic)] and slots_live[comp]==[mic,0x30099910];assert call(syms['noodle_stat'],46)==before+1
 assert call(syms['noodle_stat'],47)&3==3 and call(syms['noodle_stat'],48)==card
 checks.append('async_mesh_callback_binds_before_first_bake_'+str(card))
# Wrong mesh: NEVER write a material to another component/body/old LOD mesh.
request(target,'4522ep00v0313');fake_material(target);call(done,closure,result,detail)
for c in [comp,othercomp]:u.mem_write(c+0x468,struct.pack('<Q',meshobj+8));slots_live[c]=[0x30099900,0x30099910]
u.mem_write(actor+0x1aa0,b'\0'*8);u.mem_write(actor+0x1ab8,b'\0'*8);start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('wrong_mesh_component_no_material_write')
# Disable and approved cards do not use this override, even with same pointers.
u.mem_write(comp+0x468,struct.pack('<Q',meshobj));u.mem_write(othercomp+0x468,struct.pack('<Q',meshobj))
for card in [target,89135066911146,106781745353130,88045755960841,88038776539586,106728863696709,105848932271764,105874433662542,88033139360669,target+(1<<32)]:
 request(card,'4522ep00v0313',0 if card==target else 1);start=len(events);call(bake,actor);assert events[start:]==[('bake',actor)];checks.append('head_binding_exact_card_or_disabled_'+str(card))
u.mem_write(actor+0x1a70,b'\0'*8);u.mem_write(actor+0x228,b'\0'*8)
# Exact64 UI name override; native FString allocator boundary is modeled.
for card in [88045755960841,88045755960840,88045755960842,88045755960841+(1<<32),88045755960841&0xffffffff]:
 for enabled in [0,1]:
  call(syms['noodle_enable'],enabled);out=0x30270000;u.mem_write(out,b'\0'*16);start=len(events);call(0x3a908a0,0,card,out)
  if enabled and card==88045755960841:assert string(out)=='Nguyen Xuan Son' and events[start:]==[]
  else:assert events[start:]==[('original_player_name',card)]
  checks.append('native_UI_name_exact64_'+str(card)+'_'+str(enabled))
report={'status':'SEVEN_ARM64_DETOURS_COMPONENT_BINDING_AND_EXACT64_UI_NAME_PASS','checks':checks,'engine_sha256':hashlib.sha256(engine).hexdigest(),'hook_sha256':hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest(),'engine_bodies_modeled':True,'native_FString_ResizeTo_body_executed':True,'name_allocator_boundary_modeled':True,'native_UI_name_phone_verified':False,'component_material_virtual_boundary_modeled':True,'null_actor_mid_regression':True,'face_set_helper_body_executed':True,'bake_guard_material_cases':True,'renderer_cutscene_verified':False,'phone_tested':False};(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
