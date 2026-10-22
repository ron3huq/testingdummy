from pathlib import Path
import sys,json,hashlib,numpy as np
from PIL import Image
from iostore import Toc
from mesh_tools import Mesh
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v9';R=Path(sys.argv[1]);t=Toc(str(out/'container/pc9298_mobile_and.utoc'));prev=Toc(str(old/'container/pc9298_mobile_and.utoc'));checks=[];changed=[]
for name,i in prev.files.items():
 a=prev.read(i);b=t.read(t.files[name]);stem=Path(name).stem
 if stem in ['T_NDXSep00v0313_Face_D','T_NDPQep00v0313_Face_D']:
  assert a!=b;changed.append(name);continue
 assert a==b,name;checks.append({'name':name,'sha256':hashlib.sha256(b).hexdigest()})
folder='Game/Assets/character/RealFace'
for code in ['NDXS','NDPQ']:
 name='T_'+code+'ep00v0313_Face_D.png';a=np.array(Image.open(out/'references/v9'/name));b=np.array(Image.open(R/'v10-full-export'/folder/name));assert np.array_equal(a[1024:],b[1024:]);assert b[:1024,:,:3].mean()<a[:1024,:,:3].mean()*.9
# Sample the same cheek/nose band in all three independent reader exports.
r=json.loads((out/'build-report.json').read_text());tones=[]
for code in ['NDXS','NDPQ','NDSP']:
 name='SK_'+code+'ep00v0313_Face';m=Mesh((out/'asset'/(name+'.uasset')).read_bytes(),(R/('v10-'+code+'ep00v0313.log')).read_text(),0);n=next(x['skin_vertices'] for x in r['meshes'] if x['profile']==code);p=m.positions[:n];mask=(abs(p[:,0])<5)&(p[:,1]>13)&(p[:,2]>168)&(p[:,2]<171);pixel=np.clip((m.uv[:n,:2][mask].astype(float)*2048).astype(int),0,2047);im=np.array(Image.open(R/'v10-full-export'/folder/('T_'+code+'ep00v0313_Face_D.png')));median=np.median(im[pixel[:,1],pixel[:,0],:3],axis=0);assert np.max(abs(median-[82,52,37]))<8,(code,median);tones.append({'profile':code,'cheek_median_srgb':median.tolist()})
report={'status':'V9_ALL_EXISTING_GEOMETRY_AND_APPROVED_ASSETS_IDENTICAL_THREE_TONES_MATCH_PASS','protected_files':checks,'only_existing_assets_changed':changed,'skin_samples':tones,'phone_tested':False,'black_face_root_cause_confirmed':False,'runtime_bake_overwrite_found_in_engine':True,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()};(out/'preservation-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'protected files')
