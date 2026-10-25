from pathlib import Path
import hashlib,json,re
P=Path('/workspace/ronaldo-work/73-ui5');t=P/'payload/work/tools';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for f in(P/'payload/livedata').glob('pc9299_mobile_and.*'):f.unlink()
for stem,meta in [('pc9301','rolled_bundle.json'),('pc9300','extras_bundle.json'),('pc9302','manager_bundle.json')]:
 files={f.name:{'size':f.stat().st_size,'sha256':sha(f)}for f in(P/'payload/livedata').glob(stem+'_mobile_and.*')};assert len(files)==3;(t/meta).write_text(json.dumps({'files':files},indent=2))
f=t/'select_team_runtime.py';f.write_text(re.sub("HOOK_SHA = '[a-f0-9]+'","HOOK_SHA = '"+sha(t/'libselect_team.so')+"'",f.read_text()))
f=t/'noodle_hair.py';f.write_text(re.sub("HOOK_SHA='[a-f0-9]+'","HOOK_SHA='"+sha(t/'libnoodle_hair.so')+"'",f.read_text()))
f=t/'noodle_bundle.json';v=json.loads(f.read_text());v['native_sha256']=sha(t/'libnoodle_hair.so');v['appearance_files']={k:sha(t/k)for k in v['appearance_files']};v['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');v['editor_ui']='73-ui5-corrected-model-paths-owned-exemption-responsive';v['rolled_cuffs']='pc9301-unaltered-body-model-metadata-native-common-LOD';f.write_text(json.dumps(v,indent=2))
# Rebuild the on-device designer asset inventory after the responsive CSS change.
a=P/'apk-assets/assets/card-designer';items={}
for f in a.rglob('*'):
 if f.is_file()and f.name!='MANIFEST.json':items[f.relative_to(a).as_posix()]={'bytes':f.stat().st_size,'sha256':sha(f)}
(a/'MANIFEST.json').write_text(json.dumps(items,indent=2))
for f in t.glob('*.py'):compile(f.read_text(),str(f),'exec')
print('UI5 resource/native pins refreshed; old cuff container no longer advertised')
