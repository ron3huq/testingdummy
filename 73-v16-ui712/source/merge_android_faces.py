from pathlib import Path
import sys,re,struct,json,inspect
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry;from bundle_tools import Bundle;from zen_clone import rename,pid
P=Path('/workspace/73-ui712');b=None;rows=[]
for label,target,tag,hair in [('ronaldo2018','88042803047215','NR18','HR18'),('RONALDOmulletv8','89138288266704','NMV8','HMV8')]:
 t=Toc(str(P/'input'/label/'livedata/pc9298_mobile_and.utoc'))
 if b is None:b=Bundle(t);b.files={};b.entries={}
 h=parse_header(t.read(next(i for i,v in enumerate(t.ids)if v[11]==10)));base='/Game/Assets/character/RealFace/';mapping={};names={}
 for path in t.files:
  if path.endswith('.uasset'):
   old=Path(path).stem;new=re.sub(r'ND000\d',hair,old);new=re.sub(r'ND0\d',tag,new);assert old!=new,(old,new);names[old]=new;mapping[base+old]=base+new
 remap={pid(a):pid(z)for a,z in mapping.items()}
 for path,i in t.files.items():
  old=Path(path).stem;new=names[old];ext=Path(path).suffix;raw=t.read(i);entry=None
  if ext=='.uasset':
   fixed,deps=store_entry(h['store'],h['pids'].index(int.from_bytes(t.ids[i][:8],'little')));entry=(fixed,[remap.get(x,x)for x in deps]);raw=rename(raw,{**mapping,**names},base+old,base+new,imports=mapping)
  b.put('character/RealFace/'+new+ext,struct.pack('<Q',pid(base+new))+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),raw,entry)
 rows.append({'source':label,'card_id':target,'namespace':tag,'trial_code_imported':False})
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9313_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'android-faces/livedata');(P/'android-face-provenance.json').write_text(json.dumps(rows,indent=2));print('ANDROID_2_IMPORTED')
