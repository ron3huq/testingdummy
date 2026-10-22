from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).parent;root=r/'deploy';tools=root/'work/tools';live=root/'livedata';tools.mkdir(parents=True,exist_ok=True);live.mkdir(parents=True,exist_ok=True)
for name in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so']:shutil.copyfile(r/name,tools/name)
files={}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(r/'container'/name).read_bytes();(live/name).write_bytes(data);files[name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
meta={'version':'ronaldo-noodle-trial-v1','target_card_id':'88044950524330','container':'pc9298_mobile_and','files':files,'native_sha256':hashlib.sha256((tools/'libnoodle_hair.so').read_bytes()).hexdigest()}
(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));(tools/'noodle_hair.json').write_text(json.dumps({'enabled':True},indent=2));print('Deployment staged:',len(list(root.rglob('*'))),'entries')
