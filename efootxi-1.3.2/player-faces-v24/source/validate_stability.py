from pathlib import Path
import json
r=Path(__file__).resolve().parent
exec((r/'validate_native.py').read_text())
assert not any(name.startswith('noodle_draw_')for name in syms)
for card in [88044950524330,105807861630781,88045755960841]:
 request(card,'4522ep00v0313');actual=call(syms['noodle_stat_word'],10,0)|(call(syms['noodle_stat_word'],10,1)<<32);assert actual==card
base=(r.parent.parent/'player-faces-v23/source/noodle_hair.c').read_text();new=(r/'noodle_hair.c').read_text();reverted=new.replace('"NXNC"','"NW01"').replace('"NX01"','"NW01"').replace('"NX27"','"NW27"').replace('"NXJR"','"NWJR"');assert reverted==base
(r.parent/'stability-validation.json').write_text(json.dumps({'status':'V24_ONLY_FOUR_PROFILE_MAPPINGS_CHANGED_NO_PROBE_FULL64_PASS','native_behavior_exact_v23_except_four_profile_mappings':True,'no_new_engine_queries_or_render_writes':True,'phone_tested':False},indent=2));print('V24_ONLY_FOUR_PROFILE_MAPPINGS_CHANGED_NO_PROBE_FULL64_PASS')
