from elftools.elf.elffile import ELFFile
import capstone,io,sys,struct
p=sys.argv[1];b=open(p,'rb').read();e=ELFFile(io.BytesIO(b))
segs=[(s['p_vaddr'],s['p_offset'],s['p_filesz']) for s in e.iter_segments() if s['p_type']=='PT_LOAD']
def off(va):
    for v,o,n in segs:
        if v<=va<v+n:return o+va-v
def rd(va,n):o=off(va);return b[o:o+n]
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_ARM)
def dis(va,n=400,stop=True):
    for i in md.disasm(rd(va,n),va):
        print(hex(i.address),i.mnemonic,i.op_str)
        if stop and i.mnemonic=='ret':break
sym={s.name:s['st_value'] for s in e.get_section_by_name('.symtab').iter_symbols()}
print('profile_for');dis(sym['profile_for'],64,False)

from unicorn import *
from unicorn.arm64_const import *
def run(card):
    mu=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
    mu.mem_map(0,0x200000)
    for v,o,n in segs:
        if n:mu.mem_write(v,b[o:o+n])
    mu.mem_map(0x7000000,0x100000);mu.reg_write(UC_ARM64_REG_SP,0x70f0000)
    mu.reg_write(UC_ARM64_REG_X0,card);mu.reg_write(UC_ARM64_REG_LR,0x7000000)
    mu.emu_start(sym['profile_for'],0x7000000,count=100000)
    r=mu.reg_read(UC_ARM64_REG_X0)
    try:
        s=mu.mem_read(r,16).split(b'\0')[0]
    except Exception:s=None
    return hex(r),s
for c in sys.argv[2:]:print(c,run(int(c)))
