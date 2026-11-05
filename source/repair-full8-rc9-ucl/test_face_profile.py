"""Run the actual source-built ARM64 selector, with RC7 as independent control."""
from pathlib import Path
import json,os
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM
from unicorn.arm64_const import UC_ARM64_REG_X0,UC_ARM64_REG_LR,UC_ARM64_REG_SP
B=0x40000000;END=0x50000000
class Runner:
 def __init__(self,path):
  self.u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
  with Path(path).open('rb')as f:
   e=ELFFile(f);seg=[s for s in e.iter_segments()if s['p_type']=='PT_LOAD'];end=max(s['p_vaddr']+s['p_memsz']for s in seg);self.u.mem_map(B,(end+4095)&~4095)
   for s in seg:self.u.mem_write(B+s['p_vaddr'],s.data())
  self.u.mem_map(END,4096);self.u.mem_map(0x60000000,65536)
 def call(self,rva,arg):
  self.u.reg_write(UC_ARM64_REG_X0,arg);self.u.reg_write(UC_ARM64_REG_SP,0x6000ff00);self.u.reg_write(UC_ARM64_REG_LR,END);self.u.emu_start(B+rva,END,count=10000);return self.u.reg_read(UC_ARM64_REG_X0)
 def profile(self,pid):
  p=self.call(0x1a5e8,pid);return bytes(self.u.mem_read(p,16)).split(b'\0')[0].decode()if p else None
if __name__=='__main__':
 stage=Path(os.environ.get('FACE_TEST_BUILD','/workspace/apk73-build'));old=Runner(stage/'rc7-noodle.so');new=Runner(stage/'face-noodle.so');ids=[106654775417922,106782819217056,88035555413452,105756321970183,123,89138556572073,89138556572075]
 for palette in range(1,7):
  assert new.call(0x101028,palette)==1;assert new.profile(89138556572074)=='R8A'+str(palette)
  for pid in ids:assert old.profile(pid)==new.profile(pid),(pid,old.profile(pid),new.profile(pid))
 for v in [0,7,255]:assert new.call(0x101028,v)==0
 print(json.dumps(dict(passed=True,actual_arm64_executed=True,palettes=6,unrelated_card_controls=len(ids),phone_verified=False)))
