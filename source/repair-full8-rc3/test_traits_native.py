"""Original engine mode-2 lookup + FULL-7 detours + new bridge on synthetic DB.
This deliberately does not stub the player lookup or the two-word key decoder.
"""
from pathlib import Path
import json,struct
R=Path('/workspace/work/full8');T=R/'candidate/assets/gateway-release/work/tools'
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(T/'libselect_team.so'));exec(s)
bridge=load(R/'libcached_lookup.so',0x38000000)
from unicorn import UC_HOOK_CODE
db=0x30000000;team=0x33300000;ctx=0x33310000;side=0x33311000;tid=12345
XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
ids=[10000000000000+i for i in range(15)]
for i,pid in enumerate(ids):
 p=db+i*0x1d0;w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR)
 for ix,value in [(0,0 if i==0 else 5),(47,185),(14,70)]:call(0x82a907c,p,ix,value)
w(db+0x2686098,'I',len(ids));w(db+0x3194a10,'I',2)
# This is the real bug: in mode 2, word zero selects record zero, whatever ID.
wrong=call(0x823c8d4,db,0,ids[7]);assert wrong==db
assert call(0x68fe720,wrong)==0 and u.reg_read(UC_ARM64_REG_X1)==ids[0]
assert call(0x823c8d4,db,7,ids[7])==db+7*0x1d0
def boundary(uc,addr,size,data):
 if addr==0x82468d4:uc.reg_write(UC_ARM64_REG_X0,ctx)
 elif addr==0x33000140:uc.reg_write(UC_ARM64_REG_X0,team)
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary);w(ctx+0x40,'Q',db)
call(symbols['configure_player'],0,0x823c8d4)
call(symbols['configure_cached_team'],0,0x33000140)
call(symbols['configure_team'],0,0x33000140)
assert call(bridge['cached_lookup_configure'],0,0x823c8d4,symbols['player_hook'])==1
call(symbols['configure_player'],0,bridge['cached_lookup_original'])
player=call(symbols['editor_add_player'],ids[7],518,0);assert player
assert call(symbols['editor_parameter'],player,14,94)==1
for ix,v in[(43,1),(42,3),(45,3)]:assert call(symbols['editor_parameter'],player,ix,v)==1
assert call(symbols['editor_accessory'],player,4,2)==1
# Team pool order differs from both DB indices and requested starting order.
pool=[1,8,3,4,5,6,7,2,9,10,11,12,13,14];desired=pool.copy();desired[2],desired[6]=desired[6],desired[2]
u.mem_write(team,bytes(0x5d8));w(team,'I',tid<<14);w(team+0x40c,'I',14<<9)
for j,i in enumerate(pool):w(team+0x110+j*16,'QQ',i,ids[i]);w(team+0x3a2+j*2,'H',i)
u.mem_write(team+0x538,bytes(range(14))+b'\xff'*26);u.mem_write(team+0x560,bytes([6,2,1,3,4,5]));u.mem_write(team+0x569,b'\x06')
row=call(symbols['editor_add_team'],tid,518,14,desired.index(7));assert row
# Existing call helper exposes five arguments; slot needs seven.
def call7(addr,*args):
 regs=[UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6]
 for reg,v in zip(regs,args):u.reg_write(reg,v)
 u.reg_write(UC_ARM64_REG_SP,0x33fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(addr,0x33000010,count=20000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
for slot,index in enumerate(desired):assert call7(symbols['editor_team_slot'],row,slot,ids[index],index,0 if slot==0 else 5,slot%53,slot*7%105)==1
for k,index in enumerate([7,3,8,4,5,6]):assert call(symbols['editor_team_taker'],row,k,desired.index(index))==1
assert call(symbols['editor_commit'])==1;call(symbols['activate_context'],518)

traits=load(Path('/workspace/work/full8-rc3/payload/assets/gateway-release/work/tools/libtactics_bridge.so'),0x39000000)
call(traits['tactics_player_bind'],0,bridge['cached_lookup_player'],symbols['environment_status'])
for i,value in enumerate([1,2,3]):call(0x82a907c,db+7*0x1d0,144+i,value)
assert call(traits['transfer_booster_add'],ids[7],518,31,511,418)==1
assert call(traits['transfer_position_add'],ids[7],518,0,12)==1
for ix in range(1,14):assert call(traits['transfer_position_add'],ids[7],518,ix,2)==1
call(traits['transfer_booster_commit'])
assert call(traits['tactics_player_hook'],db,7,ids[7])==db+7*0x1d0
assert [get(db+7*0x1d0,144+i)for i in range(3)]==[31,511,418]
assert [get(db,144+i)for i in range(3)]==[0,0,0]
assert get(db+7*0x1d0,0)==12 and all(get(db+7*0x1d0,i)==2 for i in range(1,14))
assert get(db,0)==0
assert [get(db+7*0x1d0,i)for i in[43,42,45]]==[1,3,3]
assert [get(db,i)for i in[43,42,45]]==[0,0,0]
call(symbols['activate_context'],122)
call(traits['tactics_player_hook'],db,7,ids[7])
assert [get(db+7*0x1d0,144+i)for i in range(3)]==[1,2,3]
assert get(db+7*0x1d0,0)==5 and all(get(db+7*0x1d0,i)==0 for i in range(1,14))
call(symbols['activate_context'],518)
call(traits['tactics_player_hook'],db,7,ids[7])
assert [get(db+7*0x1d0,144+i)for i in range(3)]==[31,511,418]
report=dict(passed=True,dominant_and_weak_foot_reach_exact_native_player_record=True,all_14_native_position_fields_applied_and_scope_restored=True,actual_native_booster_fields_144_145_146=True,full_ID_scoped=True,other_record_unchanged=True,competition_exit_restores_original=True,reentry_applies_saved_values=True,conditional_booster_gameplay_effect_not_measured=True,phone_verified=False)
Path('/workspace/work/full8-rc3/traits-native-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
