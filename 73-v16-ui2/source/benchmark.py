exec(open('/workspace/ronaldo-work/73-ui/inspect_live.py').read().split("print('APPEARANCE'")[0])
import sqlite3,time,importlib.util,json,gc
c=sqlite3.connect('file:/workspace/ronaldo-work/73-ui/save-audit/club.sqlite3?mode=ro',uri=True);player_editor.name_index()
original=player_editor.name_index
# Reproduce UI1's cost without loading any body/motion logic.
def old_index():
 x=dict(original());x['88045755960841']=['Nguyen Xuan Son']*2;return x
player_editor.name_index=old_index
start=time.perf_counter();old=player_editor.catalog(c);slow=time.perf_counter()-start
player_editor.name_index=original
spec=importlib.util.spec_from_file_location('editor_names','/workspace/testingdummy/73-v16-ui2/source/editor_names.py');names=importlib.util.module_from_spec(spec);spec.loader.exec_module(names);names.install()
start=time.perf_counter();new=player_editor.catalog(c);fast=time.perf_counter()-start
# Real records and order preserved, only the requested aliases change.
assert len(old)==len(new)
for a,b in zip(sorted(old,key=lambda x:x['id']),sorted(new,key=lambda x:x['id'])):
 for key in set(a)|set(b):
  if key not in ['name','name_en']:assert a.get(key)==b.get(key),(a['id'],key)
print(json.dumps({'catalogue_rows':len(new),'ui1_seconds':slow,'ui2_seconds':fast,'speedup':slow/fast,'device_timing':False}),flush=True)
