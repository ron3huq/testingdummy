"""Actual loader branch/trampoline mechanics for the new game-called selectors.
The fallback delegate is the real this+28 accessor, not the full engine resource
list builder; renderer/asset loading are explicitly outside this component test.
"""
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
import json,struct,sys
r=Path(__file__).parent;sys.path.insert(0,str(r));import select_team_runtime as runtime
engine=(r.parent/'android/official-apk/lib/arm64-v8a/libUE4.so').read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);base=0x35000000
with (r/'libselect_team.so').open('rb') as f:
 e=ELFFile(f)
 for s in e.iter_segments():
  if s['p_type']=='PT_LOAD':
   lo=(base+s['p_vaddr'])&~4095;hi=(base+s['p_vaddr']+s['p_memsz']+4095)&~4095;u.mem_map(lo,hi-lo);u.mem_write(base+s['p_vaddr'],s.data())
 for s in e.iter_sections():
  if s.name.startswith('.rela'):
   for rel in s.iter_relocations():assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
 syms={s.name:base+s['st_value']for s in e.get_section_by_name('.dynsym').iter_symbols()}
u.mem_map(0x3421000,0x2000);u.mem_map(0x3033000,0x1000);u.mem_map(0x30000000,0x10000)
u.mem_write(0x3033e64,engine[0x3033e64-0x4000:0x3033e64-0x4000+8]);u.mem_write(0x30000128,struct.pack('<Q',0x30000200))
def call(a,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x3000f000);u.reg_write(UC_ARM64_REG_LR,0x3000ff00);u.emu_start(a,0x3000ff00,count=100000);assert u.reg_read(UC_ARM64_REG_PC)==0x3000ff00;return u.reg_read(UC_ARM64_REG_X0)
entries=[(0x3422074,'stage_default_hook','configure_stage_default'),(0x3421e38,'stage_home_hook','configure_stage_home')]
for i,(entry,hook,configure) in enumerate(entries):
 cave=0x0b000000+i*4096;u.mem_map(cave,4096);body=engine[entry-0x4000:entry-0x4000+16];u.mem_write(entry,body)
 u.mem_write(cave,runtime.jump(syms[hook])+b'\0'*16+body[:4]+runtime.jump(entry+4))
 # Test actual target branch installation. The original fallback delegate is
 # independently modeled by the actual engine member accessor with validself.
 call(syms[configure],0,0x3033e64);call(syms['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
 for cid in [518,122,566,128,549]:
  for stadium in [1,7,30,51,52,85]:
   assert call(syms['set_environment'],cid,stadium,0)==1
   assert call(entry,0x30000100)==stadium
 call(syms['activate_context'],0);assert call(entry,0x30000100)==0x30000200
report=dict(status='STAGE_MEMBER_DETOUR_PASS',device_tested=False,active_selector_cases=60,allowed_ids=[1,7,30,51,52,85],default100_returned=False,gateway_engine_calls=False,original_this_preserved_on_fallback=True,fallback_delegate='real3033e64 member accessor; full selector and renderer not executed',checks=['actual atomic B detours reach compiled wrappers','five competitions and six stadiums use assigned ID','context0 forwards original X0this to real accessor','no no-argument engine stage query'])
(r/'stage-detours-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
