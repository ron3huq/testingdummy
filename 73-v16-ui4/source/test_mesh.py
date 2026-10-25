from pathlib import Path
import json,numpy as np
from scipy.spatial.transform import Rotation
P=Path('/workspace/ronaldo-work/73-ui4');build=json.loads((P/'cuff-build.json').read_text());assert len(build['models'])==356
assert all(len(r['lods'])==2 and all(x['native_bone_indices_weights_section_palettes_untouched']for x in r['lods'])for r in build['models'])
def load(root,name):
 j=json.loads((root/(name+'.gltf')).read_text());raw=(root/(name+'.bin')).read_bytes()
 def arr(i):
  a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];return np.frombuffer(raw,dtype=dt,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
 return j,arr
root=P/'rolled-export/Game/Assets/character/Body';stock=P/'stock-long-export/Game/Assets/character/Body'
base,ba=load(stock,'SK_015b07');bp=base['meshes'][0]['primitives'][0];battrs=bp['attributes'];v0=ba(battrs['POSITION'])
def pose(j,arr,angle):
 nodes=j['nodes'];world={};parents={c:i for i,n in enumerate(nodes)for c in n.get('children',[])}
 def globalmat(i):
  if i in world:return world[i]
  n=nodes[i];m=np.eye(4);m[:3,:3]=Rotation.from_quat(n.get('rotation',[0,0,0,1])).as_matrix()@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);name=n.get('name','')
  if name in ['sk_forearm_l','sk_forearm_r']:m[:3,:3]=m[:3,:3]@Rotation.from_rotvec([angle*(1 if name.endswith('_l')else -1),0,0]).as_matrix()
  world[i]=(globalmat(parents[i])if i in parents else np.eye(4))@m;return world[i]
 skin=j['skins'][0];bind=arr(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);mats=np.stack([globalmat(i)for i in skin['joints']])@bind
 attrs=j['meshes'][0]['primitives'][0]['attributes'];v=arr(attrs['POSITION']);w=arr(attrs['WEIGHTS_0']).astype(float);w/=w.sum(axis=1,keepdims=True);joints=arr(attrs['JOINTS_0']);h=np.c_[v,np.ones(len(v))];return np.sum(np.einsum('nvij,nj->nvi',mats[joints],h)*w[:,:,None],axis=1)[:,:3]
proof=[]
for name in ['SK_2015b07','SK_2015e07']:
 j,a=load(root,name);prim=j['meshes'][0]['primitives'][0];attrs=prim['attributes'];v=a(attrs['POSITION']);assert len(v)==len(v0)
 for field in ['JOINTS_0','WEIGHTS_0']:assert np.array_equal(a(attrs[field]),ba(battrs[field])),field
 assert np.array_equal(a(prim['indices']),ba(bp['indices']))
 assert j['nodes']==base['nodes'] or [(n.get('name'),n.get('translation'),n.get('rotation'),n.get('children'))for n in j['nodes'][1:]]==[(n.get('name'),n.get('translation'),n.get('rotation'),n.get('children'))for n in base['nodes'][1:]]
 assert np.array_equal(a(j['skins'][0]['inverseBindMatrices']),ba(base['skins'][0]['inverseBindMatrices']))
 far=(abs(v0[:,0])<.2)|(v0[:,1]<1.)|(abs(v0[:,0])>.65);assert np.array_equal(v[far],v0[far])
 triangles=a(prim['indices']).reshape(-1,3);changed=np.linalg.norm(v-v0,axis=1)>1e-6;checks=[]
 for deg in [0,30,60,90,120]:
  p=pose(j,a,np.deg2rad(deg));q=pose(base,ba,np.deg2rad(deg));assert np.isfinite(p).all()
  # No triangles can acquire unmapped section-local bone indices. Skinning uses
  # exactly stock joints/weights; both arm branches move with their stock rig.
  displacement=np.linalg.norm(p-q,axis=1);assert displacement.max()<.08,(name,deg,float(displacement.max()))
  edges=np.concatenate([triangles[:,[0,1]],triangles[:,[1,2]],triangles[:,[2,0]]]);lens=np.linalg.norm(p[edges[:,0]]-p[edges[:,1]],axis=1);checks.append({'elbow_degrees':deg,'max_delta_from_native_long_cm':round(float(displacement.max()*100),3),'max_triangle_edge_cm':round(float(lens.max()*100),3)})
 proof.append({'mesh':name,'vertices':len(v),'changed':int(changed.sum()),'native_joint_weight_index_bind_exact':True,'posed_samples':checks})
for name in ['SK_2015b07','SK_2015e07','SK_2015b02','SK_2123e07']:
 s=(P/(name+'.log')).read_text();assert 'Exporting SkeletalMesh4 '+name in s and 'ERROR:'not in s.replace('ERROR: glTF animation could be exported from mesh viewer only.','')
(P/'mesh-validation.json').write_text(json.dumps({'passed':True,'meshes':356,'LODs':2,'native_reader_samples':4,'stock_long_skinning_preserved':True,'samples':proof,'android_gpu_tested':False,'self_intersection_not_proven_absent':True},indent=2));print('MESH_PASS')
