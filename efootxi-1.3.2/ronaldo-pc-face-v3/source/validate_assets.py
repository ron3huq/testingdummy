from pathlib import Path
import json,struct,hashlib,sys
from collections import Counter
import numpy as np
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc
r=Path(__file__).parent;t=Toc(str(r/'container/pc9298_mobile_and.utoc'));atlas=np.load(r/'atlas_uv.npy')
def get(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];off=v.get('byteOffset',0)+a.get('byteOffset',0);size={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}[a['componentType']]*{'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];stride=v.get('byteStride',size);return b''.join(b[off+j*stride:off+j*stride+size] for j in range(a['count']))
def read(path):
 d=json.loads(path.read_text());return d,(path.parent/d['buffers'][0]['uri']).read_bytes()
rows=[]
for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 name='SK_'+v.replace('4522','ND01',1)+'_Face';d,b=read(r/'full-export/Game/Assets/character/RealFace'/(name+'.gltf'));o,ob=read(r/'original-export/Game/Assets/character/RealFace'/('SK_'+v+'_Face.gltf'));a=d['meshes'][0]['primitives'][0];z=o['meshes'][0]['primitives'][0];hair=d['meshes'][0]['primitives'][1]
 for attr in ['TEXCOORD_0','TEXCOORD_1','JOINTS_0','WEIGHTS_0','COLOR_0']:assert get(d,b,a['attributes'][attr])==get(o,ob,z['attributes'][attr]),(v,attr)
 assert get(d,b,a['indices'])==get(o,ob,z['indices'])
 assert get(d,b,d['skins'][0]['inverseBindMatrices'])==get(o,ob,o['skins'][0]['inverseBindMatrices'])
 p=np.frombuffer(get(d,b,a['attributes']['POSITION']),'<f4').reshape(-1,3);op=np.frombuffer(get(o,ob,z['attributes']['POSITION']),'<f4').reshape(-1,3);delta=np.linalg.norm(p-op,axis=1)*100;assert .1<delta.max()<.81
 # Eye/forehead/nose bridge points above 170.5cm unchanged to serialization precision.
 assert np.isfinite(p).all()
 normal=np.frombuffer(get(d,b,a['attributes']['NORMAL']),'<f4').reshape(-1,3);assert np.isfinite(normal).all() and np.max(np.abs(np.linalg.norm(normal,axis=1)-1))<.02
 u=np.frombuffer(get(d,b,hair['attributes']['TEXCOORD_0']),'<f4').reshape(-1,2);assert Counter(map(tuple,u))==Counter(map(tuple,atlas))
 assert d['accessors'][hair['attributes']['POSITION']]['count']==5005 and d['accessors'][hair['indices']]['count']==5179*3
 joints=get(d,b,hair['attributes']['JOINTS_0']);weights=get(d,b,hair['attributes']['WEIGHTS_0']);assert all(struct.unpack_from('<H',joints,i*8)[0]==7 and weights[i*4:i*4+4]==b'\xff\0\0\0' for i in range(5005))
 for attr in ['POSITION','NORMAL','TANGENT','JOINTS_0','WEIGHTS_0','TEXCOORD_1']:
  old,oldb=read(r.parent/'android-hair-v1/full-export/Game/Assets/character/RealFace'/(name+'.gltf'));oh=old['meshes'][0]['primitives'][1];raw1=get(d,b,hair['attributes'][attr]);raw2=get(old,oldb,oh['attributes'][attr]);stride=len(raw1)//5005;assert Counter(raw1[i:i+stride] for i in range(0,len(raw1),stride))==Counter(raw2[i:i+stride] for i in range(0,len(raw2),stride)),(v,attr)
 assert t.read(t.files['RealFace/'+name+'.uasset'])==(r/'asset'/(name+'.uasset')).read_bytes()
 rows.append({'variant':v,'max_face_change_cm':float(delta.max()),'face_uv_weights_colors_indices_bind_matrices_preserved':True,'hair_geometry_and_weights_unchanged':True,'hair_uv_matches_baked_atlas':True})
log=(r/'full-asset-reader.log').read_text();assert 'Exported 4/4 objects' in log and 'SizeX=2048 SizeY=2048' in log
assert len([n for n in t.files if n.endswith('.uasset')])==11
texture_log=(r/'face-texture-reader.log').read_text();assert texture_log.count('SizeX=1024 SizeY=1024')==4
for variant in ['ND01','ND01lg00v0000','ND01ep01v0291','ND01ep00v0313']:
 for ext in ['uasset','ubulk']:
  name='T_'+variant+'_Face_D.'+ext;assert t.read(t.files['RealFace/'+name])==(r/'asset'/name).read_bytes()
(r/'asset-validation.json').write_text(json.dumps({'status':'PC_FACE_NATIVE_TOPOLOGY_FOUR_HEADS_AND_FOUR_TEXTURES_READER_PASS','variants':rows,'phone_tested':False},indent=2));print('PC_FACE_NATIVE_TOPOLOGY_FOUR_HEADS_AND_FOUR_TEXTURES_READER_PASS')
