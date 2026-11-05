from pathlib import Path
import sys,json,struct
sys.path.insert(0,'/workspace/work/full8-rc8-hf1/payload/assets/gateway-release/work/tools')
import hook_arena as h
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM
from unicorn.arm64_const import *
n=len(h.PLANS);assert n==63 and n*h.SLOT<=4096
page=4096;targets=[0x10000000+e for e in sorted(h.PLANS)];hole=(targets[0]+8191)&~4095;entries=[(targets[0]-(1<<27),hole),(hole+4096,targets[-1]+(1<<27))]
assert not h.candidates(entries,targets,page,0,8192)
assert h.candidates(entries,targets,page,0,4096)
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
for a in [0x100000,0x200000,0x300000,0x400000]:u.mem_map(a,4096)
stop=0x400000
u.mem_write(0x300000,struct.pack('<Q',0x200100));u.mem_write(0x200100,struct.pack('<II',0x528000e0,0xd65f03c0))
pro=struct.pack('<IIII',0xb4000080,0x52800160,0xd65f03c0,0xd503201f);u.mem_write(0x200000,pro+struct.pack('<II',0x528002c0,0xd65f03c0))
h.__dict__['__import__']=lambda name:type('Chain',(),{'target':staticmethod(lambda t:None)})if name=='v19_chain'else __import__(name)
prefix=struct.pack('<IIIIQ',0x58000090,0xf9400210,0xd61f0200,0xd503201f,0x300000)
code=prefix+h.relocated(pro,0x200000);assert len(prefix)==h.RETURN==24 and len(code)<=h.SLOT
u.mem_write(0x100000,code)
def call(a,v):
 u.reg_write(UC_ARM64_REG_X0,v);u.reg_write(UC_ARM64_REG_LR,stop);u.emu_start(a,stop,count=100);assert u.reg_read(UC_ARM64_REG_PC)==stop;return u.reg_read(UC_ARM64_REG_X0)
assert call(0x100000,0)==7
assert call(0x100000+h.RETURN,0)==22
assert call(0x100000+h.RETURN,1)==11
report={'passed':True,'planned_slots':n,'old_span_bytes':8192,'new_span_bytes':4096,'single_page_gap_old_fails_new_fits':True,'ARM64_indirect_dispatch':True,'conditional_trampoline_both_paths':True,'cached_lookup_uses_shared_RETURN':True,'phone_verified':False}
Path('/workspace/work/full8-rc8-hf1/compact-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
