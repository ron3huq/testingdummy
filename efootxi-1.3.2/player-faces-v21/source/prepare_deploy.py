from pathlib import Path
import json,hashlib,zipfile,shutil,re

r=Path(__file__).resolve().parent;O=r.parent
baseline=O.parent/'player-faces-v20/Faces-v20-14-cards-4-teams.zip'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(baseline)=='5d754379d28f2c625e8dab42effbdee90907ba2d2d7a9c115dca5029b874b974'
root=r/'deploy';tools=root/'work/tools';live=root/'livedata';tools.mkdir(parents=True,exist_ok=True);live.mkdir(exist_ok=True)
with zipfile.ZipFile(baseline)as z:
    for name in z.namelist():
        if name.startswith('work/tools/')and not name.endswith('/'):
            dest=root/name;dest.write_bytes(z.read(name))
meta=json.loads((tools/'noodle_bundle.json').read_text())
native_sha=sha(r/'libnoodle_hair.so');p=r/'noodle_hair.py';p.write_text(re.sub(r"HOOK_SHA='[0-9a-f]{64}'",'HOOK_SHA='+repr(native_sha),p.read_text()))
for name in ['noodle_hair.py','libnoodle_hair.so']:shutil.copyfile(r/name,tools/name)
for ext in ['pak','utoc','ucas']:
    name='pc9298_mobile_and.'+ext;shutil.copyfile(O/'container'/name,live/name)
meta.update(version='player-faces-v21-native-head-path',native_sha256=native_sha,target_card_ids=meta['target_card_ids']+['105807861630781','176104','84062184'],asset_revision='v21-native-head-lifecycle-Diomande-source-UV-jaw-seams-six-mini-historical-jersey-colors',phone_tested=False,replay_verified=False,four_black_faces_renderer_verified_fixed=False,jersey_names_device_verified_fixed=False)
meta['files']={p.name:{'size':p.stat().st_size,'sha256':sha(p)}for p in sorted(live.iterdir())}
assert (tools/'gateway_runtime.py').stat().st_size==2441
assert sha(tools/'myleague_editor_runtime.py')==meta['appearance_overlay_sha256']
for name,digest in meta['appearance_files'].items():assert sha(tools/name)==digest
(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
print('V21_COMPLETE_DEPLOY_17_EXACT_IDS_GATEWAY_2441_PASS')
