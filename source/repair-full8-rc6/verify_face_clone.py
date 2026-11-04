"""Compare entire authored export payloads after namespace-only cloning.
No source script or nested archive is executed or copied into the FULL.
"""
from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'repair-full8-rc4'))
if not(Path(__file__).resolve().parent.parent/'repair-full8-rc4').exists():sys.path.insert(0,'/workspace/work/full8-rc5-hf1/payload/source/repair-full8-rc4')
from iostore import Toc

def verify(root,source):
 src=Toc(str(Path(source)/'pc9298_mobile_and.utoc'));live=Path(root)/'assets/gateway-release/livedata';new={}
 for n in range(9352,9356):
  t=Toc(str(live/('pc%d_mobile_and.utoc'%n)))
  for p,i in t.files.items():assert p not in new;new[p]=t.read(i)
 report=[]
 for p,i in src.files.items():
  q='character/'+p.replace('ND0001','RG2701').replace('ND01','RG27');a=src.read(i);b=new.pop(q)
  if p.endswith('.ubulk'):assert a==b;kind='whole texture bulk byte exact'
  else:
   f=struct.unpack_from('<16I',a);g=struct.unpack_from('<16I',b);assert len(a)==len(b)
   sa=f[13]+f[14];sb=g[13]+g[14];assert a[sa:]==b[sb:],p
   kind='entire export payload byte exact, including authored LODs, skeleton, bind pose, geometry, weights, UV and material properties'
  report.append({'asset':q,'check':kind})
 assert not new
 return {'passed':True,'logical_assets':len(report),'phone_verified':False,'source_scripts_copied':False,'source_archive_copied':False,'geometry_modified':False,'texture_modified':False,'rig_modified':False,'checks':report}
if __name__=='__main__':
 d=verify(*sys.argv[1:3]);Path(sys.argv[3]).write_text(json.dumps(d,indent=2));print('PASS all',d['logical_assets'],'authored export payloads unchanged')
