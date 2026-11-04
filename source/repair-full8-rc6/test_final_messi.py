"""Original engine mode-2 lookup + FULL-7 detours + new bridge on synthetic DB.
This deliberately does not stub the player lookup or the two-word key decoder.
"""
from pathlib import Path
import json,struct
R=Path('/workspace/work/full8');T=Path('/workspace/work/full8-rc6/payload/assets/gateway-release/work/tools')
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(T/'libselect_team.so'));exec(s)
bridge=load(R/'libcached_lookup.so',0x38000000)
from unicorn import UC_HOOK_CODE
db=0x30000000;team=0x33300000;ctx=0x33310000;side=0x33311000;tid=12345
XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
ids=[10000000000000+i for i in range(15)];ids[7]=17592722922839;ids[8]=105557948213709
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
assert call(symbols['editor_parameter'],player,14,40)==1
assert call(symbols['editor_parameter'],player,116,0)==1
for ix,v in[(43,1),(42,3),(45,3)]:assert call(symbols['editor_parameter'],player,ix,v)==1
assert call(symbols['editor_accessory'],player,4,2)==1

assert call(symbols['editor_commit'])==1;call(symbols['activate_context'],518)
p=db+7*0x1d0
call(bridge['cached_lookup_player'],db,7,ids[7])
peer=db+8*0x1d0
call(bridge['cached_lookup_player'],db,8,ids[8])
peer_before=[get(peer,i)for i in range(147)]
baseline_stats={i:get(p,i)for i in range(14,41)if i!=33}
print('Old last values Messi Y17 offensive',get(p,14),'skill116',get(p,116))
final=load(Path('/workspace/work/full8-rc6/libtransfer_final.so'),0x3b000000)
assert call(final['final_bind'],0,bridge['cached_lookup_player'],symbols['environment_status'])==1
r=call(final['final_add'],ids[7],518);assert r
values={**baseline_stats,14:40,116:0,43:0,42:3,45:3,0:12,1:0,144:56,145:511,146:418}
for k,v in values.items():assert call(final['final_parameter'],r,k,v)==1
call(final['final_commit'])
spec=json.loads(Path('/workspace/work/full8-rc6/editor-callback-spec.json').read_text())
call(0x35000000+spec['configure_rva'],final['final_before_record'],final['final_after_record'],final['final_skip_balance'])
for repeat in range(3):
 assert call(final['final_player'],db,7,ids[7])==p
 for k,v in values.items():assert get(p,k)==v,(repeat,k,v,get(p,k))
assert call(final['final_skip_balance'],p,ids[7])==1
assert call(final['final_skip_balance'],peer,ids[8])==0
call(final['final_player'],db,8,ids[8])
assert [get(peer,i)for i in range(147)]==peer_before,'Unedited Y17 player was changed'
call(symbols['activate_context'],122);assert call(final['final_skip_balance'],p,ids[7])==0;call(final['final_player'],db,7,ids[7]);assert get(p,43)==0
assert call(final['final_status'],10)>=3
print('PASS final exact-ID Y17 overrides survive native classic/world/rating; repeated lookup; other competition restores')

print('PASS edited Y17 full ID alone bypasses balance; all 26 edited-profile stats preserved; unedited Y17 peer stays byte-value identical; exemption does not cross leagues')
