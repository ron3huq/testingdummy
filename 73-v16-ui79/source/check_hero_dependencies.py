from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
P=Path('/tmp/73-ui79');t=Toc(str(P/'hero-pack/livedata/pc9305_mobile_and.utoc'));h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)));own=set(h['pids']);needed=set()
for i in range(len(h['pids'])):needed.update(store_entry(h['store'],i)[1])
external=needed-own;found={};all_native=set();errors=[]
for f in list(Path('/workspace/ronaldo-work/resources').rglob('*.utoc'))+[Path('/workspace/ronaldo-work/apk/assets/pc0010_mobile_and.utoc')]+list(Path('/workspace/ronaldo-work/pc0000/PesMobile/Content/Paks').glob('*.utoc')):
 if f.name=='global.utoc':continue
 try:
  source=Toc(str(f))
  for path,index in source.files.items():
   if not path.endswith('.uasset'):continue
   pid=int.from_bytes(source.ids[index][:8],'little');all_native.add(pid)
   if pid in external:found[pid]={'path':path,'toc':str(f)}
 except Exception as e:errors.append({'path':str(f),'error':str(e)})
missing=external-set(found);report={'private_packages':len(own),'external_dependencies':len(external),'resolved':found,'missing':[hex(x)for x in missing],'native_package_ID_collisions':[hex(x)for x in own&all_native],'toc_read_errors':errors,'phone_tested':False};(P/'hero-dependencies.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert not missing and not own&all_native
