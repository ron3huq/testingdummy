"""Clone only user-supplied Android face assets, with no mesh/rig/texture edits.
Ignore all scripts, DLLs, instructions and nested archives from the source ZIP.
"""
from pathlib import Path
import sys,struct,hashlib,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'repair-full8-rc4'))
from iostore import Toc
from ci_bundle import Bundle
from zen_clone import rename,pid
BASE='/Game/Assets/character/RealFace/'
def build(root,src):
 root=Path(root);src=Path(src);t=Toc(str(src/'pc9298_mobile_and.utoc'));original=Bundle(t)
 change=lambda s:s.replace('ND0001','RG2701').replace('ND01','RG27')
 mappings={BASE+Path(p).stem:BASE+change(Path(p).stem)for p in t.files if p.endswith('.uasset')};remap={pid(a):pid(b)for a,b in mappings.items()}
 out=Bundle(t);out.files={};out.entries={};report=[]
 for path,index in t.files.items():
  assert path.startswith('RealFace/')and Path(path).suffix in['.uasset','.ubulk'],path
  name=Path(path).stem;newname=change(name);ext=Path(path).suffix;raw=t.read(index);entry=None;before=raw
  if ext=='.uasset':
   key=int.from_bytes(t.ids[index][:8],'little');fixed,deps=original.entries[key];entry=(fixed,[remap.get(x,x)for x in deps]);replacements={BASE+name:BASE+newname,name:newname}
   for a,b in mappings.items():replacements[a]=b;replacements[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
   raw=rename(raw,replacements,BASE+name,BASE+newname,imports=mappings)
  else:assert raw==before
  out.put('character/RealFace/'+newname+ext,struct.pack('<Q',pid(BASE+newname))+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),raw,entry)
  report.append(dict(source=path,output=newname+ext,source_sha256=hashlib.sha256(before).hexdigest(),output_sha256=hashlib.sha256(raw).hexdigest(),edit='package identifiers only'if ext=='.uasset'else'byte exact'))
 live=root/'assets/gateway-release/livedata'
 for i,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
  part=Bundle(t);part.files={p:v for p,v in out.files.items()if (suffix in p if suffix else not any(q in p for q in ['ep00v0313','ep01v0291','lg00v0000']))};part.entries=out.entries;part.output_name='pc'+str(9352+i)+'_mobile_and';part.write(live)
 return report
if __name__=='__main__':
 report=build(sys.argv[1],sys.argv[2]);Path(sys.argv[3]).write_text(json.dumps(report,indent=2));print('Cloned',len(report),'logical source assets; no geometry,rig,texture edits')
