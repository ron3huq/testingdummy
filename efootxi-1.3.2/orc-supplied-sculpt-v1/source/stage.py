from pathlib import Path
import json,shutil,hashlib,re,subprocess,sys
P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');R=P/'android-orc-v1';t=R/'deploy/work/tools';l=R/'deploy/livedata';t.mkdir(parents=True,exist_ok=True);l.mkdir(parents=True,exist_ok=True)
s=(R/'noodle_hair.py').read_text();s=re.sub("HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(hashlib.sha256((R/'libnoodle_hair.so').read_bytes()).hexdigest()),s);(R/'noodle_hair.py').write_text(s);(t/'noodle_hair.py').write_text(s);shutil.copyfile(R/'libnoodle_hair.so',t/'libnoodle_hair.so');shutil.copyfile(P/'startup-fix/gateway_runtime_fixed.py',t/'gateway_runtime.py');(t/'noodle_hair.json').write_text('{"enabled":true}\n')
meta={'version':'orc-supplied-sculpt-v1','container':'pc9298_mobile_and','target_card_ids':{'orc':'53878485695166'},'native_sha256':hashlib.sha256((t/'libnoodle_hair.so').read_bytes()).hexdigest(),'files':{},'phone_tested':False,'fixed_facial_expression':True,'animation_policy':'supplied Orc shape, native head/neck/chest skinning; original native 166-bone binds retained; no independent jaw/blink'}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;b=(R/'container'/name).read_bytes();(l/name).write_bytes(b);meta['files'][name]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
assert len((t/'gateway_runtime.py').read_bytes())==2441
for name in ['validate_native.py','validate_install.py','validate_runtime.py']:subprocess.run([sys.executable,str(R/name)],check=True)
print('ORC_STAGED_HOST_VALIDATED')
