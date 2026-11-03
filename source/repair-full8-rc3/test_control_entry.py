from pathlib import Path
import struct,json
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0];exec(s)
from unicorn import UC_HOOK_CODE
R=Path('/workspace/work/full8-rc3');base=0x39000000;fn=load(R/'payload/assets/gateway-release/work/tools/libsingle_player.so',base)
assert call(fn['single_player_configure'],0x10000000,1,89138556572074)==1
# Synthetic valid Frame; original engine accessors/setters execute at their
# real ELF virtual addresses. Pointer relocation differs only in the fixture.
w(base+0x32c88,'Q',0);w(base+0x32c90,'Q',0x6a9d2e0)
frame=0x33300000;match=0x33320000;pad=match+2*0xd0
u.mem_write(frame,bytes(0x70));u.mem_write(pad,bytes(0x100));u.mem_write(match,bytes(0x3000))
for off,ptr in [(0,0x33330000),(0x10,0x33340000),(0x18,match),(0x40,pad)]:w(frame+off,'Q',ptr)
for off,v in [(0x48,0),(0x4c,2),(0x50,7)]:w(frame+off,'I',v)
u.mem_write(frame+0x62,b'\x01\x01');u.mem_write(base+0x32c7f,b'\0');u.mem_write(base+0x32c7d,b'\0');u.mem_write(base+0x32c80,b'\0')
w(frame+0x58,'Q',1);w(base+0x32c60,'Q',0x33330000);w(base+0x32c48,'Q',1);u.mem_write(base+0x32c7c,b'\1');w(0xa58de28,'Q',0x33340000);w(0x33340000+0x340,'Q',match);w(0xa5909e8,'Q',0x33330000)
w(pad+0x5c,'B',1);w(pad+0x14,'I',3);w(pad+0x10,'I',3);w(match+0x1998+2*4,'I',1)
# Before this patch, the genuine enter function exits at120e8 with AI off.
new=bytes(u.mem_read(base+0x120e8,4));u.mem_write(base+0x120e8,struct.pack('<I',0x34fffe09));call(base+0x120ac,frame)
assert u.mem_read(pad+0x5c,1)==b'\1'and struct.unpack('<I',u.mem_read(pad+0x10,4))[0]==3
u.mem_write(base+0x120e8,new);u.ctl_remove_cache(base+0x120ac,base+0x12100);call(base+0x120ac,frame)
assert u.mem_read(pad+0x5c,1)==b'\3'
assert struct.unpack('<I',u.mem_read(pad+0x14,4))[0]==7
assert struct.unpack('<I',u.mem_read(pad+0x10,4))[0]==7
assert struct.unpack('<I',u.mem_read(match+0x1998+2*4,4))[0]==3
assert u.mem_read(base+0x32c7d,1)==b'\1'
for native_cursor in range(11):
 w(pad+0x10,'I',native_cursor);w(pad+0x14,'I',native_cursor);call(base+0x12a70,base+0x32c88,frame)
 assert struct.unpack('<I',u.mem_read(pad+0x10,4))[0]==7 and struct.unpack('<I',u.mem_read(pad+0x14,4))[0]==7
call(base+0x117b4,1)
assert u.mem_read(pad+0x5c,1)==b'\1'
assert struct.unpack('<I',u.mem_read(pad+0x14,4))[0]==3
assert struct.unpack('<I',u.mem_read(pad+0x10,4))[0]==3
assert struct.unpack('<I',u.mem_read(match+0x1998+2*4,4))[0]==1
assert u.mem_read(base+0x32c7d,1)==b'\0'
report=dict(passed=True,full_fixed_action_reasserts_selection_after_all_11_native_cursor_changes=True,full_restore_executed_with_original_engine_global_context_validation=True,previous_entry_reproduces_no_change_with_AI_off=True,full_control_entry_executed_not_stopped_at_boundary=True,actual_engine_controller_mode_set_to_fixed=True,actual_engine_current_and_selected_player_set_to7=True,actual_engine_match_controller_slot_set_to3=True,AI_original_flag_off=True,frame_synthetic=True,actual_phone_not_executed=True)
(R/'control-entry-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
