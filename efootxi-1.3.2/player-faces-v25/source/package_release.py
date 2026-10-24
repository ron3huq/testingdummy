from pathlib import Path
import json,hashlib,zipfile,importlib.util
r=Path(__file__).resolve().parent;O=r.parent;root=r/'deploy'
assert json.loads((O/'asset-validation.json').read_text())['status']=='V25_ONE_CARD_ALL_OLD_CHUNKS_EXACT_NATIVE_READER_PASS'
assert len(json.loads((O/'native-validation.json').read_text())['checks'])==578
assert json.loads((r/'hook-install-validation.json').read_text())['worker_reaches_hook_active']
assert json.loads((O/'runtime-validation.json').read_text())['status']=='V25_BUNDLE_HASH_17_IDS_MANIFEST_PLUS43_IDEMPOTENCE_FAILURE_FALLBACK_PASS'
assert json.loads((O/'cpu-review.json').read_text())['status']=='V25_R2017_THREE_VIEWS_CPU_BACKFACE_CULLING_PASS'
assert json.loads((O/'stability-validation.json').read_text())['other_native_behavior_exact_v24']
spec=importlib.util.spec_from_file_location('release_v25',root/'work/tools/noodle_hair.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);meta=m.bundle();assert meta['new_2017_profile']=='NV17'
sha=lambda b:hashlib.sha256(b).hexdigest()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
with zipfile.ZipFile(O.parent/'player-faces-v24/Faces-v24-three-2017-and-new-2027.zip')as z:
 for n in files:
  if n.startswith('work/')and Path(n).name not in ['noodle_hair.py','libnoodle_hair.so','noodle_bundle.json']:assert z.read(n)==(root/n).read_bytes()
name='Faces-v25-Ronaldo2017-BlenderV3-test.zip';path=O/name
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 z.write(O/'HUONG_DAN.md','HUONG_DAN.md')
 for n in files:z.write(root/n,n)
with zipfile.ZipFile(path)as z:
 assert z.testzip()is None and set(z.namelist())==set(files+['HUONG_DAN.md'])
 for n in files:assert z.read(n)==(root/n).read_bytes()
report={'status':'V25_COMPLETE_ZIP_HASH_CRC_PASS','file':name,'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),'changed_card_ids':['88044950524330'],'device_verified':False,'native_checks':578,'files':{n:{'bytes':(root/n).stat().st_size,'sha256':sha((root/n).read_bytes())}for n in files}}
(O/'package-validation.json').write_text(json.dumps(report,indent=2));(O/'SHA256SUMS').write_text(report['sha256']+'  '+name+'\n');print(json.dumps({k:report[k]for k in ['file','bytes','sha256']}))
