from pathlib import Path
import sys,struct,json,inspect,re
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry;from bundle_tools import Bundle;from zen_clone import rename,pid
P=Path('/tmp/73-ui711');b=None;report=[]
ids=['105837926394281','88040387132864','106654775417922','105758469512061','105563585358239']
for number,card in enumerate(ids,1):
 f=next((P/'input'/card).rglob('*.utoc'));t=Toc(str(f))
 if b is None:b=Bundle(t);b.files={};b.entries={}
 h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)));base='/Game/Assets/character/RealFace/';mapping={};names={};tag='NCA'+str(number);hair='NC000'+str(number)
 for path in t.files:
  if not path.endswith('.uasset'):continue
  old=Path(path).stem;new=re.sub(r'ND000\d',hair,old);new=re.sub(r'ND0\d',tag,new);assert new!=old,(card,old);names[old]=new;mapping[base+old]=base+new
 remap={pid(a):pid(z)for a,z in mapping.items()}
 for path,i in t.files.items():
  old=Path(path).stem;new=names[old];ext=Path(path).suffix;raw=t.read(i);pk=pid(base+new);entry=None
  if ext=='.uasset':
   oldpid=int.from_bytes(t.ids[i][:8],'little');fixed,deps=store_entry(h['store'],h['pids'].index(oldpid));entry=(fixed,[remap.get(x,x)for x in deps]);raw=rename(raw,{**mapping,**names},base+old,base+new,imports=mapping)
  key='character/RealFace/'+new+ext;assert key not in b.files;b.put(key,struct.pack('<Q',pk)+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),raw,entry)
 report.append({'card_id':card,'namespace':tag,'source':str(f),'assets':len(t.files),'trial_native_library_imported':False})
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9308_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'new-faces/livedata');(P/'face-import-provenance.json').write_text(json.dumps(report,indent=2));print('5FACES_MERGED',len(b.files))
