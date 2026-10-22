from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).parent;tools=r/'deploy/work/tools';live=r/'deploy/livedata';tools.mkdir(parents=True,exist_ok=True);live.mkdir(parents=True,exist_ok=True)
s=(r.parent/'hook-fix-v1b/noodle_hair.py').read_text();assert 'import hashlib,json,os,platform,struct,threading,time' in s
s=s.replace("'version':'ronaldo-noodle-trial-v1b'","'version':'ronaldo-noodle-v2-color-face'").replace("version['version']+=19","version['version']+=20")
(r/'noodle_hair.py').write_text(s);(tools/'noodle_hair.py').write_text(s)
gateway=(r.parent/'startup-fix/gateway_runtime_fixed.py').read_bytes();assert len(gateway)==2441;(tools/'gateway_runtime.py').write_bytes(gateway)
shutil.copyfile(r.parent/'android-hair-v1/libnoodle_hair.so',tools/'libnoodle_hair.so')
files={}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(r/'container'/name).read_bytes();(live/name).write_bytes(data);files[name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
meta={'version':'ronaldo-noodle-v2-color-face','target_card_id':'88044950524330','container':'pc9298_mobile_and','files':files,'native_sha256':hashlib.sha256((tools/'libnoodle_hair.so').read_bytes()).hexdigest(),'asset_revision':'two-uv-color-alpha-atlas-2048-and-conservative-cheek-jaw','phone_tested':False}
(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));(tools/'noodle_hair.json').write_text('{"enabled":true}\n');print('v2 staged; gateway and native binary unchanged from v1b')
source=(r.parent/'android-hair-v1/validate_runtime.py').read_text().replace('+19','+20');(r/'validate_runtime.py').write_text(source)
