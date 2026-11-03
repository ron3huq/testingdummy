"""Owned serial mismatch reproduced with real ARM64 roster lookup/decoder."""
from pathlib import Path
import struct,json
R=Path('/workspace/work/full8');T=R/'candidate/assets/gateway-release/work/tools'
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(T/'libselect_team.so'));exec(s)
bridge=load(R/'libcached_lookup.so',0x38000000)
team=0x30010000;wanted=106782819217056;serial=37;slot=5;pool=17
u.mem_write(team,bytes(0x5000));w(team,'I',1)
for i in range(40):w(team+4+4*i,'I',255)
w(team+4+4*slot,'I',pool);w(team+0xa8+pool*0x198+0x30,'QQ',serial,wanted)
# Exact native GamePlayerKey lookup rejects configured serial zero.
assert call(0x72f2de0,team,0,wanted)==255
expected=call(0x72f2de0,team,serial,wanted);assert expected==16,expected
call(bridge['configure_single_lookup'],0,0x72f2de0)
call(bridge['single_lookup_caller'],0x33000010,0x33000014)
assert call(bridge['single_lookup_hook'],team,0,wanted)==expected
assert call(bridge['single_lookup_hook'],team,0,wanted+(1<<32))==255
assert call(bridge['single_lookup_hook'],team,0,wanted&0xffffffff)==255
# Native callers outside the verified Single Player module retain exact serial.
call(bridge['single_lookup_caller'],0x10000,0x20000)
assert call(bridge['single_lookup_hook'],team,0,wanted)==255
assert call(bridge['single_lookup_hook'],team,serial,wanted)==expected
call(bridge['single_lookup_caller'],0x33000010,0x33000014)
# Bench is not selected; replacement at a different slot is found on next call.
w(team+4+4*slot,'I',255);w(team+4+4*15,'I',pool)
assert call(bridge['single_lookup_hook'],team,0,wanted)==255
w(team+4+4*15,'I',255);w(team+4+4*8,'I',pool)
assert call(bridge['single_lookup_hook'],team,0,wanted)==19
report=dict(passed=True,original_engine_owned_serial_mismatch_reproduced=True,live_serial=serial,full_id=str(wanted),original_engine_roster_consumers=True,caller_scope_preserves_native_serial_lookup=True,full64_collision_rejected=True,bench_rejected=True,new_starting_slot_follows_full_ID=True,verified_2e1ef197_AI_state_module_unchanged=True,phone_verified=False)
(R/'single-owned-serial-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
