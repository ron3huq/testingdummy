from pathlib import Path
import json
r=Path(__file__).resolve().parent
exec((r/'validate_native.py').read_text())
assert not any(name.startswith('noodle_draw_')for name in syms)
for card in [88044950524330,105807861630781,88045755960841]:
 request(card,'4522ep00v0313')
 actual=call(syms['noodle_stat_word'],10,0)|(call(syms['noodle_stat_word'],10,1)<<32)
 assert actual==card
# V23 native source is V21 with only one pure reporting function added.
a=(r.parent.parent/'player-faces-v21/source/noodle_hair.c').read_text();b=(r/'noodle_hair.c').read_text();addition='__attribute__((visibility("default"))) u32 noodle_stat_word(u32 i,u32 high){uptr v=noodle_stat(i);return (u32)(v>>(high?32:0));}\n';assert b.replace(addition,'')==a
report={'status':'V23_V21_NATIVE_BASELINE_NO_DRAW_PROBE_FULL64_PASS','base_native_source_exact_except_pure_reporting_function':True,'no_draw_probe_exports_or_new_engine_queries':True,'phone_tested':False,'crash_root_cause_proven':False}
(r.parent/'stability-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
