from pathlib import Path
import hashlib,json,re,shutil
r=Path(__file__).resolve().parent;out=r.parent;baseline=out.parent/'ronaldo-pc-mesh-v4a/Ronaldo-PC-mesh-v4a-88044950524330.zip'
if not baseline.exists():baseline=Path('/workspace/ronaldo-work/v4a.zip')
code=(r/'noodle_hair.py').read_text();native=(r/'libnoodle_hair.so').read_bytes();sha=hashlib.sha256(native).hexdigest();code=re.sub(r"HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(sha),code);(r/'noodle_hair.py').write_text(code)
tools=r/'deploy/work/tools';live=r/'deploy/livedata';tools.mkdir(parents=True,exist_ok=True);live.mkdir(parents=True,exist_ok=True)
shutil.copyfile(r/'myleague_editor_runtime.py',tools/'myleague_editor_runtime.py')
(tools/'noodle_hair.py').write_text(code);(tools/'libnoodle_hair.so').write_bytes(native)
import zipfile
with zipfile.ZipFile(baseline) as z:
 gateway=z.read('work/tools/gateway_runtime.py');assert len(gateway)==2441;(tools/'gateway_runtime.py').write_bytes(gateway)
files={}
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(out/'container'/name).read_bytes();(live/name).write_bytes(data);files[name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
meta={'version':'ronaldo-dual-v6-neck-head-scope','target_card_ids':['88044950524330','89135066911146'],'container':'pc9298_mobile_and','files':files,'native_sha256':sha,'asset_revision':'v6-head-only-active15-pc-normal-neck-native-weights-hq2006','active_head_bones':15,'reference_skeleton_bones':166,'appearance_overlay_sha256':hashlib.sha256((tools/'myleague_editor_runtime.py').read_bytes()).hexdigest(),'phone_tested':False,'replay_verified':False,'retarget':'named Android eye/jaw/eyelid controls, reduced PC facial rig; not all PC expressions','accessory_source':'135 vertices from original Android face section; PC oral.fmdl inspected but not used with missing FOX common oral textures'}
(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));(tools/'noodle_hair.json').write_text('{"enabled":true}\n')
print('Staged complete dual-card bundle; gateway byte-identical to v4a:',len(gateway))
