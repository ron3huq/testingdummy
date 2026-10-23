from pathlib import Path
import json,zipfile,hashlib
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';name='Faces-v13-13-cards.zip'
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
for filename in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:(out/filename).write_bytes((r/filename).read_bytes())
native=json.loads((out/'native-validation.json').read_text());assert len(native['checks'])==479
sleeves=json.loads((out/'sleeve-validation.json').read_text());assert sleeves['cases']==1296
assert sleeves['hook_sha256']==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
assets=json.loads((out/'asset-validation.json').read_text());assert len(assets['meshes'])==25 and assets['render_lods']==50
assert json.loads((out/'quality-validation.json').read_text())['status'].endswith('_PASS');assert json.loads((out/'texture-validation.json').read_text())['status'].endswith('_PASS')
for report_name in ['asset-validation.json','quality-validation.json','texture-validation.json','seam-validation.json','preservation-validation.json']:
 assert json.loads((out/report_name).read_text())['container_sha256']==hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),('stale report',report_name)
for ext in ['pak','utoc','ucas']:
 assert (deploy/'livedata'/('pc9298_mobile_and.'+ext)).read_bytes()==(out/'container'/('pc9298_mobile_and.'+ext)).read_bytes(),('stale deploy',ext)
for filename in ['libnoodle_hair.so','libselect_team.so','noodle_hair.py','select_team_runtime.py']:
 assert (deploy/'work/tools'/filename).read_bytes()==(r/filename).read_bytes(),('stale runtime',filename)
for path in r.glob('*.py'):compile(path.read_bytes(),str(path),'exec')
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:z.write(deploy/f,f)
 z.write(out/'HUONG_DAN.md','HUONG_DAN.md')
with zipfile.ZipFile(out/name) as z:
 assert z.testzip() is None and set(z.namelist())==set(files+['HUONG_DAN.md']);assert len(z.read('work/tools/gateway_runtime.py'))==2441
 meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['target_card_ids']==['88044950524330','89135066911146','106781745353130','106734785925546','105765448873424','88045755960841','88038776539586','105643042189511','106728863696709','105848932271764','105874433662542','88033139360669','106726716084650']
 for f,row in meta['files'].items():
  data=z.read('livedata/'+f);assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
 for f,sha in meta['appearance_files'].items():assert hashlib.sha256(z.read('work/tools/'+f)).hexdigest()==sha
 assert hashlib.sha256(z.read('work/tools/myleague_editor_runtime.py')).hexdigest()==meta['appearance_overlay_sha256']
 native_sha=hashlib.sha256(z.read('work/tools/libnoodle_hair.so')).hexdigest();assert native_sha==native['hook_sha256'] and native_sha==meta['native_sha256'] and native_sha in z.read('work/tools/noodle_hair.py').decode()
 assert hashlib.sha256(z.read('work/tools/libselect_team.so')).hexdigest() in z.read('work/tools/select_team_runtime.py').decode()
with zipfile.ZipFile(out/'Tat-thay-dau-v13.zip','w',zipfile.ZIP_DEFLATED) as z:z.writestr('work/tools/noodle_hair.json','{"enabled":false}\n')
result={'status':'V13_ELEVEN_FILES_CRC_HASHES_NATIVE_LODS_AND_SLEEVES_PASS','installed_files':len(files),'native_head_cases':479,'native_shirt_selector_cases':1296,'head_meshes':25,'render_lods':50,'phone_tested':False,'replay_verified':False,'prior_v7_cutscene_confirmed_by_user':True,'missing_source_card_ids':[],'artifacts':{n:{'bytes':(out/n).stat().st_size,'sha256':hashlib.sha256((out/n).read_bytes()).hexdigest()} for n in [name,'Tat-thay-dau-v13.zip']}}
(out/'package-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
