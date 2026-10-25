from pathlib import Path
import json,hashlib
P=Path('/workspace/ronaldo-work/73-ui6');root=P/'payload';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();rows=[]
for f in(root/'work/tools').iterdir():
 if f.suffix in['.py','.so']or f.name in['myleague_custom.json','ui2_skill_rules.json','myleague_base_rosters.json.gz','noodle_bundle.json','extras_bundle.json','manager_bundle.json','kits_bundle.json']:
  rows.append({'path':f.relative_to(root).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
for f in list((root/'livedata').iterdir())+list(Path('/workspace/ronaldo-work/73-v25-port/package/payload/livedata').glob('pc9298_mobile_and.*')):
 rows.append({'path':'livedata/'+f.name,'bytes':f.stat().st_size,'sha256':sha(f)})
out=P/'apk-assets/assets/gateway-release/ui6-runtime-manifest.json';out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps({'version':'73-ui6-persistent-native-20261025','files':rows},indent=2));print('REPAIR_MANIFEST',len(rows))
