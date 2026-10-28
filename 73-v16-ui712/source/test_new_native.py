from pathlib import Path
P=Path('/workspace/73-ui712');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/apk/assets/gateway-release/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE
pid=123456789876;donor=88044950524330;p=0x30020000;d=0x30021000;ctx=0x30022000;db=0x30023000;XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
for at,id in [(p,pid),(d,donor)]:u.mem_write(at,bytes(0x500));w(at+0x40,'Q',id^XOR)
w(ctx+0x40,'Q',db)
for at in [p,d]:call(0x82a907c,at,47,185)
def stub(uc,addr,size,data):
 if addr==0x82468d4:uc.reg_write(UC_ARM64_REG_X0,ctx)
 elif addr==0x33000120:uc.reg_write(UC_ARM64_REG_X0,d if uc.reg_read(UC_ARM64_REG_X2)==donor else p)
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);call(symbols['configure_team'],0,0x33000130);call(symbols['configure_player'],0,0x33000120)
row=call(symbols['editor_add_player'],pid,0,0);assert call(symbols['editor_global_stats'],row)==1
for ix in [14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40]:
 assert call(symbols['editor_parameter'],row,ix,127)==1;assert call(symbols['editor_parameter'],row,ix,128)==0
assert call(symbols['editor_commit'])==1
call(symbols['activate_context'],0);call(symbols['editor_apply_player'],p,pid)
assert all(get(p,i)==127 for i in list(range(14,33))+list(range(34,41)))
# Dedicated motion donor leaves identity, stats, body and celebrations untouched.
motion={51:2,52:5,53:11,54:6,55:12,56:17,57:6,58:10}
for ix,value in motion.items():assert call(0x82a907c,d,ix,value)==1
assert call(symbols['editor_motion_add'],pid,donor)==1;call(symbols['editor_motion_commit']);before=[get(p,i)for i in range(147)];call(symbols['editor_apply_player'],p,pid);after=[get(p,i)for i in range(147)]
print('MOTION_STATUS',[call(symbols['editor_motion_status'],i)for i in range(6)],'SRC',[get(d,i)for i in range(51,59)])
for ix in range(147):assert after[ix]==motion.get(ix,before[ix]),(ix,after[ix])
# Whole original player_hook executes additive native World Nation policy and restores on exit.
sys=__import__('sys');sys.path.insert(0,str(P/'build/apk/assets/gateway-release/work/tools'));import world_skills
proof=[]
for role in range(13):
 call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid)
 for flag in range(70,144):call(0x82a907c,p,flag,int(flag in [70,143,141]))
 call(0x82a907c,p,0,role);call(symbols['player_hook'],db,0,pid);saved=[get(p,i)for i in range(70,144)];call(symbols['activate_context'],128);call(symbols['player_hook'],db,0,pid)
 assert all(get(p,f)==1 for f in world_skills.flags(role));assert all(get(p,f)==1 for f in [70,143,141]);one=[get(p,i)for i in range(70,144)];call(symbols['player_hook'],db,0,pid);assert [get(p,i)for i in range(70,144)]==one
 call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid);assert [get(p,i)for i in range(70,144)]==saved
 proof.append({'role':role,'added_flags':len(set(world_skills.flags(role))),'preserved_existing':True,'restored_outside_league':True})
# Exact competition + slot remap, preserves other team and other slot.
assert call(symbols['editor_kit_add'],4937,473,2,242*16384)==1;assert call(symbols['editor_kit_add'],109,0,1,351*16384+1)==1;call(symbols['editor_kit_commit']);call(symbols['activate_context'],473)
assert call(symbols['editor_kit_resolve'],4937*16384+2)==242*16384
assert call(symbols['editor_kit_resolve'],4937*16384+1)==4937*16384+1
call(symbols['activate_context'],518);assert call(symbols['editor_kit_resolve'],4937*16384+2)==4937*16384+2
assert call(symbols['editor_kit_resolve'],109*16384+1)==351*16384+1
(P/'new-native-validation.json').write_text(json.dumps({'passed':True,'Android_tested':False,'original_native_147_getter_setter':True,'stat_bounds':[0,127],'motion_parameters_copied':motion,'all_unrelated_fields_preserved':True,'world_nation_roles':proof,'kit_scope_and_four_slot_remap':True},indent=2));print('NEW_NATIVE_PASS')
