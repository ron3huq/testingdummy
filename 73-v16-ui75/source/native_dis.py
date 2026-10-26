from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
f=open('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so','rb');e=ELFFile(f);cs=Cs(CS_ARCH_ARM64,CS_MODE_ARM)
def read(a,n):
 for s in e.iter_segments():
  if s['p_type']=='PT_LOAD'and s['p_vaddr']<=a<s['p_vaddr']+s['p_filesz']:f.seek(s['p_offset']+a-s['p_vaddr']);return f.read(n)
def dis(a,n):return '\n'.join(f'{i.address:x} {i.mnemonic} {i.op_str}' for i in cs.disasm(read(a,n),a))
if __name__=='__main__':
 import sys
 print(dis(int(sys.argv[1],16),int(sys.argv[2],16)))
