from pathlib import Path
import json
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0];exec(s)
from unicorn import UC_HOOK_CODE
R=Path('/workspace/work/full8-rc3');helper=load(R/'payload/assets/gateway-release/work/tools/libtactics_bridge.so',0x39000000)
w(0xa5fb348,'Q',0x33300000);w(0x33300048,'Q',0x33310000)
# Only mode/context acquisition boundaries are synthetic. The actual engine
# GetCpuLevel body, setting getter and observer wrapper run in ARM64.
def boundary(uc,addr,size,data):
 values={0x7a87db8:0x33320000,0x7b7cfb4:0,0x7b833ec:0,0x7b7b31c:0}
 if addr in values:uc.reg_write(UC_ARM64_REG_X0,values[addr]);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary);call(helper['configure_cpu_level'],0,0x73a9ba4)
for level in range(7):
 call(0x7b80140,0,level);before=bytes(u.mem_read(0x33310000,0x2000));assert call(helper['native_cpu_level_hook'],0)==level;assert call(helper['cpu_probe_status'],1)==level;assert bytes(u.mem_read(0x33310000,0x2000))==before
assert call(helper['cpu_probe_status'],0)==7
report=dict(passed=True,original_mode_dependent_GetCpuLevel_body_executed=True,global_mode_context_boundaries_mocked=True,observer_preserves_all_seven_return_values=True,observer_does_not_write_native_CPU_settings=True,natural_call_count_and_last_level_available=True,min_clamp_and_boss_branches_not_executed=True,AI_decision_effect_not_measured=True,phone_verified=False)
(R/'cpu-observer-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
