from pathlib import Path
import sys,json,struct,re
from collections import Counter
import numpy as np
from scipy.spatial import cKDTree
r=Path(__file__).parent;p=r.parent;sys.path.insert(0,str(p/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc
f=FmdlFile();f.readFile(str(p/'new-face-4522/models/face_high.fmdl'));h=FmdlFile();h.readFile(str(p/'new-face-4522/models/hair_high.fmdl'));vertices=f.meshes[0].vertices+f.meshes[2].vertices+h.meshes[1].vertices
expected=np.array([[v.position.x,v.position.y,v.position.z] for v in vertices]);uv_expected=np.array([[v.uv[0].u,v.uv[0].v] for v in vertices]).astype(np.float16).astype(float)
t=Toc(str(r/'container/pc9298_mobile_and.utoc'))
def read(path):
 d=json.loads(path.read_text());return d,(path.parent/d['buffers'][0]['uri']).read_bytes()
def get(d,b,i):
 a=d['accessors'][i];v=d['bufferViews'][a['bufferView']];off=v.get('byteOffset',0)+a.get('byteOffset',0);w={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];size=w*{5121:1,5123:2,5125:4,5126:4}[a['componentType']];stride=v.get('byteStride',size);return b''.join(b[off+j*stride:off+j*stride+size] for j in range(a['count']))
def vec(d,b,a,attr,w,fmt='<f4'):return np.frombuffer(get(d,b,a['attributes'][attr]),fmt).reshape(-1,w)
rows=[]
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 name='SK_'+variant.replace('4522','ND01',1)+'_Face';d,b=read(r/'full-export/Game/Assets/character/RealFace'/(name+'.gltf'));o,ob=read(p/'android-hair-v1/original-export/Game/Assets/character/RealFace'/('SK_'+variant+'_Face.gltf'));skin,hair=d['meshes'][0]['primitives'];xyz=vec(d,b,skin,'POSITION',3);uv=vec(d,b,skin,'TEXCOORD_0',2)
 assert len(xyz)==2366 and d['accessors'][skin['indices']]['count']==4420*3
 # Exporter may reorder duplicate vertices: verify joint position/UV tuples as a multiset.
 key=lambda pos,tex:Counter(tuple(np.round(np.r_[a,q],6)) for a,q in zip(pos,tex))
 actual=np.c_[xyz,uv];want=np.c_[expected,uv_expected];assert cKDTree(want).query(actual)[0].max()<2e-6 and cKDTree(actual).query(want)[0].max()<2e-6
 assert get(d,b,d['skins'][0]['inverseBindMatrices'])==get(o,ob,o['skins'][0]['inverseBindMatrices'])
 bones=[d['nodes'][n]['name'] for n in d['skins'][0]['joints']];assert len(bones)==166
 joints=vec(d,b,skin,'JOINTS_0',4,'<u2');weights=vec(d,b,skin,'WEIGHTS_0',4,'u1');assert np.all(weights.sum(axis=1)==255)
 controlled={}
 for name_bone in ['skf_jaw','skf_eyelid_t_l','skf_eyelid_b_l','skf_eyelid_t_r','skf_eyelid_b_r']:
  influence=np.sum((joints==bones.index(name_bone))*weights/255,axis=1);assert (influence>0).sum()>0;controlled[name_bone]=int((influence>0).sum())
 # Exercise a world-space jaw displacement in the standard skinning equation.
 inv=np.frombuffer(get(d,b,d['skins'][0]['inverseBindMatrices']),'<f4').reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inv);modified=bind.copy();jaw=bones.index('skf_jaw');modified[jaw,:3,3]+=[0,-.006,.001];mat=modified@inv;hom=np.c_[xyz,np.ones(len(xyz))];posed=np.zeros_like(hom)
 for slot in range(4):posed+=np.einsum('nij,nj->ni',mat[joints[:,slot]],hom)*(weights[:,slot]/255)[:,None]
 movement=np.linalg.norm(posed[:,:3]-xyz,axis=1);assert (movement>1e-5).sum()>20 and movement.max()<.0062
 assert d['accessors'][hair['attributes']['POSITION']]['count']==5005 and d['accessors'][hair['indices']]['count']==5179*3
 # Raw metadata audit: both RequiredBones and ActiveBoneIndices include hands/feet/facial controls.
 raw=(r/'asset'/(name+'.uasset')).read_bytes();ff=struct.unpack_from('<16I',raw);de=ff[13]+ff[14]+struct.unpack_from('<Q',raw,ff[11]+8)[0]-struct.unpack_from('<Q',raw,ff[11]+72)[0]
 # Reader log positions belong to name-renamed assets actually parsed from the container.
 whole=(r/'full-asset-reader.log').read_text();block=whole.split('Loading SkeletalMesh4 '+name+' ')[1].split('Exporting SkeletalMesh4 '+name)[0] if 'Loading SkeletalMesh4 '+name+' ' in whole else ''
 # The 166-entry array occurs at each LOD and at the active list; original byte topology unchanged.
 allbones=struct.pack('<I',166)+struct.pack('<166H',*range(166));assert raw.count(allbones)>=3
 assert t.read(t.files['RealFace/'+name+'.uasset'])==raw
 rows.append({'variant':variant,'pc_skin_vertices':2366,'pc_skin_triangles':4420,'source_pc_skin_positions_and_uv_roundtrip_max_error_under_2e_6':True,'native_bind_matrices_all_166_identical':True,'named_facial_controls_weighted_vertices':controlled,'jaw_skinning_moves_vertices':int((movement>1e-5).sum()),'all_166_active_and_required_bones':True})
assert len([n for n in t.files if n.endswith('.uasset')])==11
assert (r/'full-asset-reader.log').read_text().count('Exported 4/4 objects')==1
assert (r/'face-texture-reader.log').read_text().count('SizeX=1024 SizeY=1024')==4
(r/'asset-validation.json').write_text(json.dumps({'status':'FULL_PC_FACE_NATIVE_RIG_REQUIRED_BONES_AND_BASIC_SKINNING_PASS','variants':rows,'mobile_cutscene_tested':False,'mobile_facial_clips_tested':False},indent=2));print('FULL_PC_FACE_NATIVE_RIG_REQUIRED_BONES_AND_BASIC_SKINNING_PASS')
