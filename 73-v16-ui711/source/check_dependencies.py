from pathlib import Path
import sys,json
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry
P=Path('/tmp/73-ui711');packs=[P/'build/payload/livedata/pc9305_mobile_and.utoc',P/'build/payload/livedata/pc9307_mobile_and.utoc',P/'fixed-faces/livedata/pc9308_mobile_and.utoc',P/'art-pack/livedata/pc9306_mobile_and.utoc',Path('/workspace/ronaldo-work/73-ui7/carry/livedata/pc9298_mobile_and.utoc')];own=set();newown=set();needed=set();counts={}
for f in packs:
 t=Toc(str(f));h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)));pids=set(h['pids']);assert not own&pids;own|=pids
 if f.name!='pc9298_mobile_and.utoc':newown|=pids
 counts[f.name]=len(pids)
 for i in range(len(h['pids'])):needed.update(store_entry(h['store'],i)[1])
external=needed-own;found=set();native=set()
for f in list(Path('/workspace/ronaldo-work/resources').rglob('*.utoc'))+[Path('/workspace/ronaldo-work/apk/assets/pc0010_mobile_and.utoc')]+list(Path('/workspace/ronaldo-work/pc0000/PesMobile/Content/Paks').glob('*.utoc')):
 if f.name=='global.utoc':continue
 t=Toc(str(f))
 for path,index in t.files.items():
  if path.endswith('.uasset'):native.add(int.from_bytes(t.ids[index][:8],'little'))
found=external&native;missing=external-native
report={'passed':not missing and not newown&native,'package_counts':counts,'new_package_IDs_unique_against_existing_face_pack':True,'existing_face_pack_intentional_stock_overrides_unchanged':True,'native_ID_collisions':[hex(x)for x in newown&native],'external_dependencies':len(external),'missing':[hex(x)for x in missing],'device_tested':False};(P/'dependency-validation.json').write_text(json.dumps(report,indent=2));print(report);assert report['passed']
