from pathlib import Path
import sys,json,inspect,struct,re
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle
from zen_clone import rename,pid
P=Path('/workspace/ronaldo-work/73-ui6');R=P.parent
old=Toc(str(R/'73-ui5/payload/livedata/pc9302_mobile_and.utoc'));b=Bundle(old)
base=Toc(str(R/'pc0000/PesMobile/Content/Paks/pakchunk0-Android_ETC2.utoc'));restored=[]
for path in old.files:
 if 'character/DemoFace/Manager/'in path:
  original='PesMobile/Content/Assets/'+path
  assert original in base.files,original
  b.native(base,original,base.read(base.files[original]));restored.append(path)
def write(bundle,stem):
 s=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='"+stem+"_mobile_and'");ns={};exec('class Writer:\n'+s,Bundle.write.__globals__,ns);ns['Writer'].write(bundle,P/'payload/livedata')
write(b,'pc9302')
old=Toc(str(R/'73-ui5/payload/livedata/pc9300_mobile_and.utoc'));b=Bundle(old);coach=Toc(str(next((R/'resources').rglob('pc1000_mobile_and.utoc'))))
for cid in ['17606144688129','17604802510874']:
 path='ui/Data/Symbol/Coach/Variation/coach_'+cid+'_.uasset';assert path in coach.files;b.native(coach,path,coach.read(coach.files[path]))
write(b,'pc9300')
# Mirror real donor resources to the league clubs' own native paths. This also
# covers the pre-match screen and the original uniform-selection IDs.
alias={1706:352,4937:242,1957:108,1956:121,4962:120,4964:102,4938:103,1950:119,1228:101,1955:127}
paths=sorted((R/'resources').rglob('*.utoc'),key=lambda f:f.name)+[R/'73-v25-port/package/payload/livedata/pc9298_mobile_and.utoc',R/'73-ui5/payload/livedata/pc9300_mobile_and.utoc']
baseface=Toc(str(R/'73-v25-port/package/payload/livedata/pc9298_mobile_and.utoc'));b=object.__new__(Bundle);b.base=baseface;b.files={};b.entries={};latest={}
for file in paths:
 t=Toc(str(file))
 for path,index in t.files.items():
  full=(t.mount+path).replace('\\','/')
  if '/Content/Assets/'not in full:continue
  relative=full.split('/Content/Assets/')[1]
  if 'uniform'not in relative.lower():continue
  for target,donor in alias.items():
   # Real3D textures/materials/font and kit thumbnail variants use u####.
   if re.search(r'u'+f'{donor:04d}'+r'[pg]',relative)or any('uni'+str((donor<<14)+slot)+'_'in relative for slot in range(3)):latest[(target,relative)]=(t,path,index,donor)
headers={};proof=[]
for (target,relative),(t,path,index,donor)in latest.items():
 oldtoken='u'+f'{donor:04d}';newtoken='u'+f'{target:04d}';dest=relative.replace(oldtoken,newtoken)
 for slot in range(3):dest=dest.replace('uni'+str((donor<<14)+slot)+'_','uni'+str((target<<14)+slot)+'_')
 raw=t.read(index)
 h=headers.setdefault(t.path,parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10))))
 if relative.endswith('.uasset'):
  op='/Game/Assets/'+relative[:-7];np_='/Game/Assets/'+dest[:-7];edited=rename(raw,{Path(path).stem:Path(dest).stem,op:np_},op,np_);idb=struct.pack('<Q',pid(np_))+t.ids[index][8:];pk=int.from_bytes(t.ids[index][:8],'little');entry=store_entry(h['store'],h['pids'].index(pk));b.put(dest,idb,edited,entry)
 else:
  oldasset='/Game/Assets/'+relative.rsplit('.',1)[0];newasset=oldasset.replace(oldtoken,newtoken);idb=struct.pack('<Q',pid(newasset))+t.ids[index][8:];b.put(dest,idb,raw)
 proof.append({'team':target,'donor':donor,'source':relative,'destination':dest,'source_container':Path(t.path).name})
assert all(any(r['team']==tid and 'Uni_D.uasset'in r['source']for r in proof)for tid in [1706,4937,1957,1956,1950,1228]),{tid:sum(r['team']==tid for r in proof)for tid in alias}
write(b,'pc9303');(P/'resources-build.json').write_text(json.dumps({'restored_original_manager_assets':restored,'restored_native_portraits':2,'mirrored_kits':proof},indent=2));print('RESOURCES',len(restored),'manager originals;',len(proof),'kit assets', {tid:sum(r['team']==tid for r in proof)for tid in alias})
