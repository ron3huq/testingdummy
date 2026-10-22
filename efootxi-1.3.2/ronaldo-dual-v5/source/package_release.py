from pathlib import Path
import json,zipfile,hashlib,re
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';guide=(out/'HUONG_DAN.md').read_bytes();name='Ronaldo-v5-hai-the-mat-mieng-2006.zip';files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for path in files:z.write(deploy/path,path)
 z.writestr('HUONG_DAN.md',guide)
with zipfile.ZipFile(out/name) as z:
 assert z.testzip() is None and set(z.namelist())==set(files+['HUONG_DAN.md']);assert len(z.read('work/tools/gateway_runtime.py'))==2441
 meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['target_card_ids']==['88044950524330','89135066911146'];assert json.loads(z.read('work/tools/noodle_hair.json'))['enabled'] is True
 for f,row in meta['files'].items():
  data=z.read('livedata/'+f);assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
 native=hashlib.sha256(z.read('work/tools/libnoodle_hair.so')).hexdigest();assert native==meta['native_sha256'] and native in z.read('work/tools/noodle_hair.py').decode()
 for f in ['gateway_runtime.py','noodle_hair.py']:compile(z.read('work/tools/'+f),f,'exec')
with zipfile.ZipFile(out/'Tat-ban-thu-v5.zip','w',zipfile.ZIP_DEFLATED) as z:z.writestr('work/tools/noodle_hair.json','{"enabled":false}\n')
reports={}
for filename in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:
 data=(r/filename).read_bytes();(out/filename).write_bytes(data);reports[filename]=json.loads(data)
assert len(reports['native-validation.json']['checks'])>=58
assets=json.loads((out/'asset-validation.json').read_text());assert len(assets['meshes'])==8 and assets['all_chunk_sha1']
summary={'status':'DUAL_CARD_EIGHT_FILES_ZIP_CRC_AND_CHECKSUMS_PASS','native_checks':len(reports['native-validation.json']['checks']),'meshes':8,'gateway_bytes':2441,'phone_tested':False,'replay_verified':False,'artifacts':{n:{'bytes':(out/n).stat().st_size,'sha256':hashlib.sha256((out/n).read_bytes()).hexdigest()} for n in [name,'Tat-ban-thu-v5.zip']}}
(out/'package-validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
