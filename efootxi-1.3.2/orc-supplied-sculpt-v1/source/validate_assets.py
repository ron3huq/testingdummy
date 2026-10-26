from pathlib import Path
import json,numpy as np,struct,hashlib
r=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-orc-v1');d=r/'export-final/Game/Assets/character/RealFace';orig=r.parent/'android-hair-v1/original-export/Game/Assets/character/RealFace';report={'phone_tested':False,'reader':'independent UEViewer','variants':{}}
def load(path):return json.loads(path.read_text()),path.parent
def arr(g,root,index):
 a=g['accessors'][index];v=g['bufferViews'][a['bufferView']];data=(root/g['buffers'][v['buffer']]['uri']).read_bytes();dtype={5126:'<f4',5123:'<u2',5121:'u1'}[a['componentType']];n={'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16,'SCALAR':1}[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);out=np.frombuffer(data,dtype=dtype,count=a['count']*n,offset=offset).reshape(-1,n);return out.astype(float)/255 if a.get('normalized')and a['componentType']==5121 else out
for kind,prefix,root in [('orc','ND01','orc-source')]:
 geo=json.loads((Path('/workspace/analysis')/root/'native_geometry.json').read_text());expect=np.array([[v['p'][0],v['p'][2],-v['p'][1]]for v in geo['vertices']]);uv=np.array([v['uv']for v in geo['vertices']]);norm=np.array([[v['n'][0],v['n'][2],-v['n'][1]]for v in geo['vertices']]);stats=[]
 for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
  name='SK_'+prefix+suffix+'_Face';g,folder=load(d/(name+'.gltf'));b,bfolder=load(orig/('SK_4522'+suffix+'_Face.gltf'));skin=g['skins'][0];joints=[g['nodes'][n]['name']for n in skin['joints']];bjoints=[b['nodes'][n]['name']for n in b['skins'][0]['joints']];assert joints==bjoints and len(joints)==166
  assert arr(g,folder,skin['inverseBindMatrices']).tobytes()==arr(b,bfolder,b['skins'][0]['inverseBindMatrices']).tobytes()
  prim=g['meshes'][0]['primitives'][1];a=prim['attributes'];positions=arr(g,folder,a['POSITION']);assert positions.shape==expect.shape
  error=float(np.max(np.abs(positions-expect)));assert error<.000001
  tc=arr(g,folder,a['TEXCOORD_0']);# glTF uses UV origin at the top.
  uv_error=float(np.max(np.abs(tc-np.column_stack([uv[:,0],1-uv[:,1]]))));assert uv_error<.00051,uv_error
  n=arr(g,folder,a['NORMAL']);normal_error=float(np.max(np.abs(n-norm)));assert normal_error<.016,normal_error
  ji=arr(g,folder,a['JOINTS_0']);ww=arr(g,folder,a['WEIGHTS_0']);assert np.max(np.abs(ww.sum(axis=1)-1))<.00001;assert np.max(ji)<166
  for i,row in enumerate(geo['vertices']):
   expected={k:w for k,w in row['weights'].items()if w>0};actual={joints[int(j)]:float(w)for j,w in zip(ji[i],ww[i])if w>0}
   # Preserved Spider-Man source aliases were already reduced by its original builder.
   if kind!='spiderman':
    assert set(actual)<=set(expected);assert all(abs(actual.get(k,0)-w)<.008 for k,w in expected.items())
  indices=arr(g,folder,prim['indices']).reshape(-1,3);assert len(indices)==len(geo['triangles']) and indices.max()<len(positions)
  t=np.array(geo['triangles']);assert np.array_equal(np.sort(t,axis=1),np.sort(indices,axis=1))
  stats.append({'variant':name,'vertices':len(positions),'triangles':len(indices),'position_error_m':error,'uv_error':uv_error,'normal_error':normal_error,'native_166_bone_bind_matrices_byte_identical':True,'weights_normalized':True})
 report['variants'][kind]=stats
# No template-specific face material is needed on any of the new private meshes.
for f in (r/'asset').glob('SK_*.uasset'):
 data=f.read_bytes();assert b'MI_4522'not in data
(r/'asset-validation.json').write_text(json.dumps(report,indent=2));print('FOUR_ORC_MESHES_166_BINDS_UV_NORMAL_WEIGHTS_PASS')
