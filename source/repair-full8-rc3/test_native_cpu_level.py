from pathlib import Path
import json,struct
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0];exec(s)
c=0x33300000;setting=0x33310000;w(0xa5fb348,'Q',c);w(c+0x48,'Q',setting)
rows=[]
for level,name in enumerate(['VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND']):
 assert call(0x389a154,level)==level
 call(0x7b80140,0,level)
 assert u.mem_read(setting+0x1cfd,1)==bytes([level]);assert call(0x7b7cc70,0)==level
 assert call(0x389a16c,level)==level
 call(0x7b7f780,level);assert call(0x7b7cc90)==level
 rows.append(dict(native_event_setting_also_roundtrips=True,level=level,name=name,actual_native_getter=level))
assert call(0x389a154,99)==2 and call(0x389a16c,99)==2
report=dict(passed=True,actual_original_engine_enum_normalizer_and_CPU_setter_getter_executed=True,levels=rows,invalid_native_enum_falls_back_to_NORMAL2=True,native_context_synthetic=True,does_not_prove_AI_decision_or_gameplay_difference=True,phone_verified=False)
Path('/workspace/work/full8-rc3/native-cpu-level-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
