from pathlib import Path
import sys,struct,json,inspect
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry;from bundle_tools import Bundle;from zen_clone import rename,pid
P=Path('/tmp/73-ui710');t=Toc(str(P/'input/livedata/pc9298_mobile_and.utoc'));b=Bundle(t);b.files={};b.entries={};h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)));base='/Game/Assets/character/RealFace/';mapping={};names={}
for path in t.files:
 if not path.endswith('.uasset'):continue
 old=Path(path).stem;new=old.replace('ND0005','NN0005').replace('ND0002','NO0002').replace('ND05','NNAR').replace('ND02','NORC');names[old]=new;mapping[base+old]=base+new
for path,i in t.files.items():
 old=Path(path).stem;new=names[old];ext=Path(path).suffix;raw=t.read(i);pk=pid(base+new);entry=None
 if ext=='.uasset':
  oldpid=int.from_bytes(t.ids[i][:8],'little');fixed,deps=store_entry(h['store'],h['pids'].index(oldpid));remap={pid(a):pid(z)for a,z in mapping.items()};entry=(fixed,[remap.get(x,x)for x in deps]);raw=rename(raw,{**mapping,**names},base+old,base+new,imports=mapping)
 b.put('character/RealFace/'+new+ext,struct.pack('<Q',pk)+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),raw,entry)
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9307_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'new-heads/livedata');print('NEW_HERO_PRIVATE_PACK',len(b.files))
