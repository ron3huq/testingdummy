from pathlib import Path
import struct,json
R=Path('/workspace/work/full8-rc2');T=R/'payload/assets/gateway-release/work/tools'
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0];exec(s)
from unicorn import UC_HOOK_CODE
base=0x39000000;symbols2=load(T/'libsingle_player.so',base)
assert call(symbols2['single_player_configure'],0x10000000,1,89138556572074)==1
sp=0x33ffe000;frame=sp+8
u.mem_write(frame,bytes(0x70))
for off in [0,0x10,0x18,0x40]:w(frame+off,'Q',0x30010000)
for off,value in [(0x48,0),(0x4c,0),(0x50,5)]:w(frame+off,'I',value)
u.mem_write(frame+0x62,b'\x01\x01')
# Execute the real decision block and Frame::usable; only stop at its action.
calls=[]
def stop(uc,addr,size,data):
 if addr in[base+0x120ac,base+0x11a10,base+0x117b4]:calls.append((addr-base,uc.reg_read(UC_ARM64_REG_X0)));uc.emu_stop()
u.hook_add(UC_HOOK_CODE,stop)
def route(ai):
 calls.clear();u.mem_write(base+0x32c7f,bytes([ai]));u.mem_write(base+0x32c7d,b'\0')
 u.reg_write(UC_ARM64_REG_X25,base+0x32ca0);u.reg_write(UC_ARM64_REG_SP,sp);u.emu_start(base+0x112a8,base+0x11364,count=10000)
 return calls[0][0]
assert route(0)==0x120ac;assert route(1)==0x120ac
assert call(symbols2['single_player_configure'],0x10000000,0,89138556572074)==1
assert route(0)==0x117b4
from elftools.elf.elffile import ELFFile
old=Path('/workspace/work/full8/candidate/assets/gateway-release/work/tools/libsingle_player.so').read_bytes();new=(T/'libsingle_player.so').read_bytes();diff=[i for i,(a,b)in enumerate(zip(old,new))if a!=b];assert len(old)==len(new)and max(diff)-min(diff)<4
report=dict(passed=True,actual_ARM64_decision_and_Frame_usable_executed=True,AI_off_enters_fixed_player_action=True,AI_on_enters_fixed_player_action=True,disabled_enters_restore_action=True,only_one_instruction_changed_from_verified_restore_module=True,frame_synthetic=True,control_action_boundary_not_executed=True,phone_verified=False)
(R/'single-native-gate-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
