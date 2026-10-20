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
root,regions,leagues,teams,out,obuf=0x30090000,0x30091000,0x30092000,0x30093000,0x30094000,0x30095000
old=[213,182,413,114,4211,4213,1329,420,218,212,180,414,403,181,112,217,221,113]
new=[101,102,103,114,100,173,179,108,109,172,121,119,120,181,112,125,327,130]
def w(addr,fmt,*values):u.mem_write(addr,struct.pack('<'+fmt,*values))
def vec(addr,start,n,stride):w(addr,'QQQ',start,start+n*stride,start+n*stride)
u.mem_write(root,b'\0'*0x118)
vec(root+0x90,regions,1,32);vec(regions+8,leagues,2,40)
vec(leagues+16,teams,18,4);vec(leagues+40+16,teams+0x100,18,4)
# Low 14 bits are deliberately nonzero and different: preserve the complete native words.
words={t:(t<<14)|(i+37) for i,t in enumerate(sorted(set(old+new)))}
for base,ids in [(teams,old),(teams+0x100,new)]:w(base,'18I',*(words[t] for t in ids))
def get(home):
 vec(out,obuf,0,4);w(out+16,'Q',obuf+18*4)
 call(0x737e05c,root,home,out)
 begin,end,cap=struct.unpack('<QQQ',u.mem_read(out,24))
 assert begin==obuf and end==obuf+72
 return list(struct.unpack('<18I',u.mem_read(begin,end-begin)))
# isHome=true uses indices +74/+7c; false uses +78/+80.
w(root+0x74,'4I',0,0,0,1)
assert get(1)==old
assert get(0)==new
other_before=bytes(u.mem_read(teams+0x100,72))
from elftools.elf.elffile import ELFFile
libbase=0x35000000
with Path(__file__).with_name('libselect_team.so').open('rb') as f:
 elf=ELFFile(f)
 assert not any(s.name.startswith('.rela') and s.num_relocations() for s in elf.iter_sections())
 for seg in elf.iter_segments():
  if seg['p_type']!='PT_LOAD':continue
  start=(libbase+seg['p_vaddr'])&~4095
  end=(libbase+seg['p_vaddr']+seg['p_memsz']+4095)&~4095
  u.mem_map(start,end-start);u.mem_write(libbase+seg['p_vaddr'],seg.data())
 symbols={s.name:libbase+s['st_value'] for s in elf.get_section_by_name('.dynsym').iter_symbols()}
w(root,'Q',0x98c3ff0)
assert call(symbols['fix'],root,0)==1
assert call(symbols['fix'],root,0)==2
assert get(1)==new and get(0)==new
assert bytes(u.mem_read(teams+0x100,72))==other_before
w(teams,'18I',*(words[t] for t in old));assert get(1)==old
# Unrelated native menu class, special flat-list mode, and malformed vectors must not write.
before=bytes(u.mem_read(teams,72))
w(root,'Q',0x12345678);assert call(symbols['fix'],root,0)==6
w(root,'Q',0x98c3ff0);u.mem_write(root+0xf0,b'\x20');assert call(symbols['fix'],root,0)==7
u.mem_write(root+0xf0,b'\x00');w(root+0x90+8,'Q',regions-1);assert call(symbols['fix'],root,0)==8
vec(root+0x90,regions,1,32)
assert bytes(u.mem_read(teams,72))==before
# Missing target team and conflicting packed identity must fail before any write.
w(teams+0x100,'I',999<<14);assert call(symbols['fix'],root,0)==3
w(teams+0x100,'I',words[new[0]])
w(teams+3*4,'I',words[114]^1);assert call(symbols['fix'],root,0)==4
w(teams+3*4,'I',words[114]);assert bytes(u.mem_read(teams,72))==before
# Test the real entry detour -> compiled hook -> relocated original prologue -> native getter.
import importlib.util
spec=importlib.util.spec_from_file_location('runtime',Path(__file__).with_name('select_team_runtime.py'))
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
cave=0x0b000000;u.mem_map(cave,4096)
original4=bytes(u.mem_read(0x737e05c,4))
u.mem_write(cave,runtime.jump(symbols['menu_hook'])+b'\0'*16+original4+runtime.jump(0x737e060))
call(symbols['configure'],0,cave+32)
call(symbols['store_instruction'],0x737e05c,runtime.branch(0x737e05c,cave))
u.ctl_remove_cache(0x737e05c,0x737e06c)
actual=get(1)
assert actual==new,(actual,call(symbols['status'],0),call(symbols['status'],1))
assert call(symbols['status'],1)==1
assert get(1)==new and call(symbols['status'],1)==1
assert bytes(u.mem_read(teams+0x100,72))==other_before
u.mem_write(0x737e05c,original4)
report={'status':'NATIVE_COMPONENT_TEST_ONLY','device_tested':False,'libUE4_sha256':'3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98','getter_va':'0x737e05c','passed':['original France list','independent home/away indices','compiled C patch replaces all 18 packed words','other league bytes unchanged','restore original list','wrong class rejected','special list rejected','invalid vector rejected','missing team rejected without writes','ambiguous packed identity rejected without writes','atomic branch detour and trampoline execute full getter','repeated menu calls are idempotent'],'original_ids':old,'target_ids':new}
Path(__file__).with_name('native-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
