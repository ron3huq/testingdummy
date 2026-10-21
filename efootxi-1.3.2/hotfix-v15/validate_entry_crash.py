"""Reproduce v7 using actual member-accessor instructions, not the old stub."""
from pathlib import Path
import json,struct
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
r=Path(__file__).parent;engine=(r.parent/'android/official-apk/lib/arm64-v8a/libUE4.so').read_bytes();expected=bytes.fromhex('001440f9c0035fd6');body=engine[0x3033e64-0x4000:0x3033e64-0x4000+8];assert body==expected

def setup(path):
 u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);u.mem_map(0x30000000,0x10000);u.mem_map(0x3033000,0x1000);u.mem_write(0x3033e64,body)
 base=0x35000000
 with path.open('rb') as f:
  e=ELFFile(f)
  for s in e.iter_segments():
   if s['p_type']=='PT_LOAD':
    lo=(base+s['p_vaddr'])&~4095;hi=(base+s['p_vaddr']+s['p_memsz']+4095)&~4095;u.mem_map(lo,hi-lo);u.mem_write(base+s['p_vaddr'],s.data())
  syms={s.name:base+s['st_value'] for s in e.get_section_by_name('.dynsym').iter_symbols()}
  for s in e.iter_sections():
   if s.name.startswith('.rela'):
    for rel in s.iter_relocations():assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
 def call(address,*args):
  for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,value)
  u.reg_write(UC_ARM64_REG_SP,0x3000f000);u.reg_write(UC_ARM64_REG_LR,0x3000ff00);u.emu_start(address,0x3000ff00,count=100000);assert u.reg_read(UC_ARM64_REG_PC)==0x3000ff00;return u.reg_read(UC_ARM64_REG_X0)
 return u,syms,call
old,syms,call=setup(r.parent/'hotfix-v7/libselect_team.so');old.mem_write(0x30000128,struct.pack('<Q',0x30000200));assert call(0x3033e64,0x30000100)==0x30000200
call(syms['configure_team'],0,0);faults=[]
def invalid(uc,access,address,size,value,data):faults.append(dict(pc=hex(uc.reg_read(UC_ARM64_REG_PC)),address=hex(address),x0=hex(uc.reg_read(UC_ARM64_REG_X0))));return False
old.hook_add(UC_HOOK_MEM_INVALID,invalid)
try:call(syms['stadium_mask'],0)
except UcError as error:assert error.errno==UC_ERR_READ_UNMAPPED
else:raise AssertionError('old crash was not reproduced')
assert faults==[dict(pc='0x3033e64',address='0x28',x0='0x0')],faults
new,syms,call=setup(r/'libselect_team.so');call(syms['configure_team'],0,0)
def forbidden(uc,address,size,data):raise AssertionError('member accessor must never be called')
forbidden_handle=new.hook_add(UC_HOOK_CODE,forbidden,begin=0x3033e64,end=0x3033e6b)
for cid in [0,122,518,566]:
 for snow in [0,1]:
  assert call(syms['stadium_mask'],snow)==0
  assert call(syms['set_environment'],cid,85,snow)==1
  if cid:
   assert call(syms['stage_default_hook'],0)==85
   assert call(syms['stage_home_hook'],0)==85
assert call(syms['set_environment'],518,100,0)==21
assert call(syms['set_environment'],999,85,0)==20
# Fallback executes actual3033e64 with original self, never a no-argument call.
new.hook_del(new.hook_add(UC_HOOK_CODE,lambda *x:None,begin=1,end=1))
# Remove the forbidden accessor hook only for the explicit game-called fallback.
new.hook_del(forbidden_handle)
new.mem_write(0x30000128,struct.pack('<Q',0x30000200))
call(syms['configure_stage_default'],0,0x3033e64);call(syms['configure_stage_home'],0,0x3033e64)
call(syms['activate_context'],0)
assert call(syms['stage_default_hook'],0x30000100)==0x30000200
assert call(syms['stage_home_hook'],0x30000100)==0x30000200
loader=(r/'select_team_runtime.py').read_text();assert '0x3422074' in loader and '0x3421e38' in loader
report=dict(status='V7_ENTRY_CRASH_REPRODUCED_AND_REMOVED_PASS',old_version='native-hotfix-v7',fixed_version='native-hotfix-v15',actual_engine_instruction='ldr x0,[x0,#0x28]; ret',old_faults=faults,old_stadium_accessor_stubbed=False,old_correct_this_argument_succeeds=True,new_gateway_no_engine_stage_calls=True,member_hooks_forward_this_on_fallback=True,forced_stage_never_100=True,phone_verified=False)
(r/'entry-crash-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
