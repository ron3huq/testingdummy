from pathlib import Path
import shutil,json,hashlib,re
r=Path(__file__).parent;tools=r/'deploy/work/tools';live=r/'deploy/livedata';tools.mkdir(parents=True,exist_ok=True);live.mkdir(parents=True,exist_ok=True)
code=(r/'noodle_hair.py').read_text();code=re.sub(r"HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest()),code);(r/'noodle_hair.py').write_text(code)
for name in ['noodle_hair.py','libnoodle_hair.so']:shutil.copyfile(r/name,tools/name)
g=(r.parent/'startup-fix/gateway_runtime_fixed.py').read_bytes();assert len(g)==2441;(tools/'gateway_runtime.py').write_bytes(g)
files={}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(r/'container'/name).read_bytes();(live/name).write_bytes(data);files[name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
meta={'version':'spiderman-head-v6-original2006-neck20','target_card_id':'88044950524330','container':'pc9298_mobile_and','files':files,'native_sha256':hashlib.sha256((tools/'libnoodle_hair.so').read_bytes()).hexdigest(),'face_source':'Spider-Man closed mask/lenses/web, rigid head; Original 2006 source neck throat scalp collar; source boundary repair; no loft; 20mm shortening','asset_revision':'spiderman-v4-profile-neck20mm-native166','phone_tested':False}
(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));(tools/'noodle_hair.json').write_text('{"enabled":true}\n')
s=(r.parent/'android-hair-v1/validate_runtime.py').read_text().replace('+19','+26');(r/'validate_runtime.py').write_text(s)
print('v3 staged; protected gateway remains 2441 bytes')
