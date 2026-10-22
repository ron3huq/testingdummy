from pathlib import Path
import sys,json,hashlib,numpy as np
from mesh_tools import Mesh
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v8';R=Path(sys.argv[1]);t=Toc(str(out/'container/pc9298_mobile_and.utoc'));checks=[]
for name in json.loads((out/'preserved-v8-assets.json').read_text()):
 original=(old/'asset'/name).read_bytes();actual=t.read(t.files['RealFace/'+name]);assert original==actual,name
 checks.append({'name':name,'sha256':hashlib.sha256(actual).hexdigest()})
changed=[]
for prev,code in [('ND01','NF01'),('ND27','NF27'),('NDJR','NFJR')]:
 for row in json.loads((old/'build-report.json').read_text())['meshes']:
  if row['profile']!=prev:continue
  suffix=row['variant'][4:];name='SK_'+code+suffix+'_Face';raw=t.read(t.files['RealFace/'+name+'.uasset']);before=(old/'asset'/('SK_'+prev+suffix+'_Face.uasset')).read_bytes()
  for lod in [0,1]:
   a=Mesh(before,(R/('v8-'+prev+suffix+'.log')).read_text(),lod);b=Mesh(raw,(R/('v9-'+code+suffix+'.log')).read_text(),lod)
   for field in ['positions','uv','indices','weights','colors']:assert np.array_equal(getattr(a,field),getattr(b,field)),(code,lod,field)
  changed.append(name)
from PIL import Image
folder='Game/Assets/character/RealFace';a=np.asarray(Image.open(R/'v8-full-export'/folder/'T_NDXSep00v0313_Face_D.png')).astype(float);b=np.asarray(Image.open(R/'v9-full-export'/folder/'T_NDXSep00v0313_Face_D.png')).astype(float)
assert b[:1024,:1024,:3].mean()<a[:1024,:1024,:3].mean()*.9
assert np.array_equal(a[1024:],b[1024:]),'native XS eyes/mouth diffuse must remain unchanged'
report={'status':'V8_APPROVED_ASSETS_BYTE_IDENTICAL_BAD_HEAD_GEOMETRY_UNCHANGED_PASS','protected_files':checks,'revised_tangent_head_meshes':changed,'xuan_son_diffuse_only_darker':True,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'phone_tested':False,'black_face_root_cause_confirmed':False}
(out/'preservation-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'files')
