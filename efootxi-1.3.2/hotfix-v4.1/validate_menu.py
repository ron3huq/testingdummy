"""Execute the original Android ARM64 getter on synthetic, bounded native vectors."""
import struct, json, argparse, hashlib
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM
from unicorn.arm64_const import *
parser=argparse.ArgumentParser()
parser.add_argument('--libue4',required=True)
args=parser.parse_args()
engine=Path(args.libue4)
assert hashlib.sha256(engine.read_bytes()).hexdigest()=='3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98'
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
with engine.open('rb') as f:
 elf=ELFFile(f)
 for seg in elf.iter_segments():
  if seg['p_type']!='PT_LOAD':continue
  start=seg['p_vaddr']&~4095;end=(seg['p_vaddr']+seg['p_memsz']+4095)&~4095
  u.mem_map(start,end-start);u.mem_write(seg['p_vaddr'],seg.data())
for addr,size in [(0x30000000,0x1000000),(0x32000000,0x100000),(0x33000000,0x1000),(0x34000000,0x1000)]:u.mem_map(addr,size)
u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x34000000)
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x320ff000);u.reg_write(UC_ARM64_REG_LR,0x33000010)
 u.emu_start(addr,0x33000010,count=5000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_W0)
import collections
from unicorn import UC_HOOK_CODE
root,regions,leagues=0x30090000,0x30091000,0x30092000
out,obuf=0x30094000,0x30095000
cfg=json.loads(Path(__file__).with_name('myleague_custom.json').read_text())
keys=['122','566','128','125'];sources=[cfg['leagues'][k]['original_teams'] for k in keys]
def w(addr,fmt,*values):u.mem_write(addr,struct.pack('<'+fmt,*values))
def vec(addr,start,n,stride):w(addr,'QQQ',start,start+n*stride,start+n*stride)
u.mem_write(root,b'\0'*0x118);w(root,'Q',0x98c3ff0)
vec(root+0x90,regions,1,32);vec(regions+8,leagues,4,40)
for i,ids in enumerate(sources):
 base=0x30096000+i*0x1000;vec(leagues+i*40+16,base,len(ids),4);w(base,str(len(ids))+'I',*(t<<14 for t in ids))
def get(index):
 w(root+0x74,'4I',0,0,index,index)
 vec(out,obuf,0,4);w(out+16,'Q',obuf+40*4)
 call(0x737e05c,root,1,out)
 begin,end,cap=struct.unpack('<QQQ',u.mem_read(out,24))
 return list(struct.unpack('<'+str((end-begin)//4)+'I',u.mem_read(begin,end-begin)))
for i in range(4):assert get(i)==sources[i]
libbase=0x35000000
with Path(__file__).with_name('libselect_team.so').open('rb') as f:
 elf=ELFFile(f)
 for seg in elf.iter_segments():
  if seg['p_type']!='PT_LOAD':continue
  start=(libbase+seg['p_vaddr'])&~4095;end=(libbase+seg['p_vaddr']+seg['p_memsz']+4095)&~4095
  u.mem_map(start,end-start);u.mem_write(libbase+seg['p_vaddr'],seg.data())
 symbols={s.name:libbase+s['st_value'] for s in elf.get_section_by_name('.dynsym').iter_symbols()}
 for section in elf.iter_sections():
  if section.name.startswith('.rela'):
   for rel in section.iter_relocations():
    assert rel['r_info_type']==1027 # R_AARCH64_RELATIVE, no outside symbol lookup.
    w(libbase+rel['r_offset'],'Q',libbase+rel['r_addend'])
heap=0x31000000;u.mem_map(heap,0x100000);allocated=[];freed=[]
def alloc_hook(uc,addr,size,unused):
 global heap
 if addr==0x2f37644:
  n=uc.reg_read(UC_ARM64_REG_X0);assert uc.reg_read(UC_ARM64_REG_X1)==0
  value=heap;heap+=(n+15)&~15;allocated.append((value,n));uc.mem_write(value,b'\0'*n);uc.reg_write(UC_ARM64_REG_X0,value)
 elif addr==0x2f376d4:freed.append(uc.reg_read(UC_ARM64_REG_X0))
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,alloc_hook)
import importlib.util
spec=importlib.util.spec_from_file_location('runtime',Path(__file__).with_name('select_team_runtime.py'));runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
cave=0x0b000000;u.mem_map(cave,4096);stolen=bytes(u.mem_read(0x737e05c,4))
u.mem_write(cave,runtime.jump(symbols['menu_hook'])+b'\0'*16+stolen+runtime.jump(0x737e060))
call(symbols['configure'],0,cave+32)
call(symbols['store_instruction'],0x737e05c,runtime.branch(0x737e05c,cave));u.ctl_remove_cache(0x737e05c,0x737e06c)
for i,key in enumerate(keys):assert get(i)==cfg['leagues'][key]['teams']
assert len(allocated)==1 and allocated[0][1]==80
assert freed==[0x30098000]
for i,key in enumerate(keys):assert get(i)==cfg['leagues'][key]['teams']
assert len(allocated)==1
assert all(call(symbols['status'],i+3)==2 for i in range(4))
# Reject unrelated class/special flat-list and malformed vector, without writes.
image=bytes(u.mem_read(leagues,4*40));w(root,'Q',123);assert call(symbols['fix'],root,0)==6
w(root,'Q',0x98c3ff0);u.mem_write(root+0xf0,b'\x20');assert call(symbols['fix'],root,0)==7
u.mem_write(root+0xf0,b'\0');w(root+0x98,'Q',regions-1);assert call(symbols['fix'],root,0)==8
vec(root+0x90,regions,1,32);assert bytes(u.mem_read(leagues,160))==image
# Execute the real native region/league/team-vector destructor. New Portugal memory
# must be freed by the same engine allocator family, once, with no old double-free.
call(0x7381094,root+0x90)
assert freed.count(allocated[0][0])==1 and freed.count(0x30098000)==1
report={'status':'ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED','device_tested':False,'checks':['all four original lists read by real getter','compiled hook via atomic branch and original trampoline','Ligue 1 replaces Monaco with Bayern ID127','Eredivisie contains exact 18 requested available clubs, including confirmed replacements','Belgium native list contains exact 18 national IDs','Portugal native list grows from 18 to 20 national IDs','native ID constructor format ID<<14 used for absent teams','engine allocator used for 80-byte replacement','old buffer freed once; native destructor frees new buffer once','repeated calls idempotent','wrong class/special list/invalid vector refused'],'league_team_counts':{k:len(cfg['leagues'][k]['teams']) for k in keys}}
Path(__file__).with_name('menu-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
