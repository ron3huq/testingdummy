"""Original ARM64 region selector/FString allocator with bounded synthetic heap.
Asset renderer is not executed; this is not Android UI verification.
"""
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
import json,struct,hashlib,sys
r=Path(__file__).parent;sys.path.insert(0,str(r));import select_team_runtime as runtime
engine=Path('/workspace/analysis/my-league/android/official-apk/lib/arm64-v8a/libUE4.so');assert hashlib.sha256(engine.read_bytes()).hexdigest()==runtime.ENGINE_SHA
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
def load(path,base=0):
 with path.open('rb') as f:
  e=ELFFile(f)
  for s in e.iter_segments():
   if s['p_type']=='PT_LOAD':
    a=(base+s['p_vaddr'])&~4095;end=(base+s['p_vaddr']+s['p_memsz']+4095)&~4095;u.mem_map(a,end-a);u.mem_write(base+s['p_vaddr'],s.data())
  if base:
   for s in e.iter_sections():
    if s.name.startswith('.rela'):
     for rel in s.iter_relocations():
      assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
   return {s.name:base+s['st_value'] for s in e.get_section_by_name('.dynsym').iter_symbols()}
load(engine);symbols=load(r/'libselect_team.so',0x35000000)
u.mem_map(0x30000000,0x1000000);u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x30004000)
heap=0x30100000;allocs={};captured=[];fallbacks=[];OUT=0x30005000;INFO=0x30006000
names={'122':'UEFA Champions League','566':'AFC Nation League','128':'World Super League','549':'Asia-Pacific League'}
regions={'122':'nationalEurope','128':'nationalLatinAmerica','566':'nationalAsia','549':'nationalNorthAmerica'}
def read_string(p):
 ptr,n,cap=struct.unpack('<QII',u.mem_read(p,16));assert 0<=n<=cap<1024
 return bytes(u.mem_read(ptr,n*2)).decode('utf-16-le').rstrip('\0') if n else ''
def stub(uc,a,size,d):
 global heap
 x0,x1,x2=[uc.reg_read(v) for v in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]]
 if a==0x42ccbbc:val=x0
 elif a==0x42cca20:
  val=heap;heap+=(x1+15)&~15
  if x0:uc.mem_write(val,bytes(uc.mem_read(x0,min(allocs[x0],x1))))
  allocs[val]=x1
 elif a==0x42cc968:val=0
 elif a==0x8c1bc70:uc.mem_write(x0,bytes(uc.mem_read(x1,x2)));val=x0
 elif a==0x3a5aecc:
  captured.append((read_string(x0),x1,uc.reg_read(UC_ARM64_REG_X8)));uc.mem_write(uc.reg_read(UC_ARM64_REG_X8),b'\0'*16);val=0
 elif a in (0x3a55840,0x3a59928,0x3a55870,0x3a56dec):
  fallbacks.append((a,x0,x1,x2,uc.reg_read(UC_ARM64_REG_X8)));uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+(32 if a==0x3a55840 else 64 if a==0x3a55870 else 0x180 if a==0x3a56dec else 0x150));val=0
 else:return
 uc.reg_write(UC_ARM64_REG_X0,val);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub)
def call(a,*args):
 for reg,v in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,v)
 u.reg_write(UC_ARM64_REG_X8,OUT);u.reg_write(UC_ARM64_REG_SP,0x300ff000);u.reg_write(UC_ARM64_REG_LR,0x30009000);u.emu_start(a,0x30009000,count=200000);assert u.reg_read(UC_ARM64_REG_PC)==0x30009000
for number,(entry,hook,configure) in enumerate([(0x3a5583c,'competition_name_hook','configure_competition_name'),(0x3a59924,'competition_logo_hook','configure_competition_logo'),(0x3a5586c,'kit_hook','configure_kit'),(0x3a56de8,'emblem_hook','configure_emblem'),(0x82b4a7c,'short_hook','configure_short')]):
 cave=0x0b000000+number*4096;u.mem_map(cave,4096);stolen=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(symbols[hook])+b'\0'*16+stolen+runtime.jump(entry+4));call(symbols[configure],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
for cid,name in names.items():
 call(0x3a5583c,int(cid));assert read_string(OUT)==name
 u.mem_write(INFO,struct.pack('<II',int(cid),17));call(0x3a59924,INFO,3,2);assert captured[-1]==(regions[cid],3,OUT)
for cid in [125,121,549<<14]:
 call(0x3a5583c,cid);assert fallbacks[-1][0:2]==(0x3a55840,cid) and fallbacks[-1][-1]==OUT
 u.mem_write(INFO,struct.pack('<II',cid,17));call(0x3a59924,INFO,2,3);assert fallbacks[-1]==(0x3a59928,INFO,2,3,OUT)
assert len(captured)==4
for target,donor in [(1986,114),(131,173),(1987,103),(116,181),(108,108)]:
 call(0x3a56de8,target,2,3);assert fallbacks[-1]==(0x3a56dec,donor,2,3,OUT)
 call(0x3a5586c,target,2,3);assert fallbacks[-1]==(0x3a55870,(target if target==116 else donor),2,3,OUT)
u.mem_write(INFO,struct.pack('<I',5741<<14));ptr=None
call(0x82b4a7c,INFO);ptr=u.reg_read(UC_ARM64_REG_X0);assert bytes(u.mem_read(ptr,5))==b'LAFC\0'
report=dict(status='PRESENTATION_ARM64_COMPONENT_PASS',device_tested=False,names=names,logo_region_symbols=regions,checks=['actual detours and original trampoline fallback','X8 FString indirect result preserved','custom name strings allocated by original engine FString reserve on synthetic heap','original ARM64 special-region selector and symbol construction reached for all4 league logos','original Eredivisie125 name/logo paths preserved','PSG/City/Liverpool kit and emblem aliases preserve X8/style; Ajax emblem retained','LAFC getter returns4 letters while native short field stays within4 bytes','unrelated IDs/styles/output pointer preserved'],limits='Actual assets, renderer, cached textures and every UI caller remain untested on phone.')
(r/'presentation-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
