from pathlib import Path
import zipfile,json,hashlib
r=Path(__file__).parent;root=r/'deploy'
files=['work/tools/gateway_runtime.py','work/tools/noodle_hair.py','work/tools/libnoodle_hair.so','work/tools/noodle_hair.json','work/tools/noodle_bundle.json']+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
assert len(files)==8
z=r/'Ronaldo-noodle-trial-v1-88044950524330.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for n in files:f.write(root/n,n)
 f.write(r/'HUONG_DAN.md','HUONG_DAN.md')
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and not any('myleague_editor.json' in n or 'libselect_team.so' in n or 'dt200' in n for n in f.namelist())
 for n in files:assert f.read(n)==(root/n).read_bytes()
rollback=r/'Tat-noodle-hair.zip'
with zipfile.ZipFile(rollback,'w',zipfile.ZIP_DEFLATED) as f:f.writestr('work/tools/noodle_hair.json','{"enabled":false}\n')
report={'status':'EXPERIMENTAL_ANDROID_TRIAL_NOT_DEVICE_VERIFIED','target_card_id':'88044950524330','files':files,'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [z,rollback]},'phone_tested':False}
(r/'package-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['artifacts'],indent=2))
