from pathlib import Path
import json,numpy as np,hashlib,sys
p=Path('/workspace/ronaldo-work/73-ui2');build=json.loads((p/'rolled-build.json').read_text());assert build['count']==356 and all(len(r['lods'])==2 for r in build['models'])
def load(root,name):
 j=json.loads((root/(name+'.gltf')).read_text());raw=(root/(name+'.bin')).read_bytes()
 def arr(i):
  a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];return np.frombuffer(raw,dtype=dt,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
 return j,arr
proof=[]
for source,dest in [('SK_015a07','SK_2015b07'),('SK_015d07','SK_2015e07')]:
 old,oa=load(p/'cloth-export/Game/Assets/character/Body',source);new,na=load(p/'rolled-export/Game/Assets/character/Body',dest);op=old['meshes'][0]['primitives'][0];np_=new['meshes'][0]['primitives'][0]
 attrs=op['attributes'];nattrs=np_['attributes'];v=oa(attrs['POSITION']);nv=na(nattrs['POSITION']);c=oa(attrs['COLOR_0']);assert v.shape==nv.shape
 assert np.array_equal(oa(op['indices']),na(np_['indices']))and np.array_equal(c,na(nattrs['COLOR_0']))
 for name in ['TEXCOORD_0','TEXCOORD_1','TEXCOORD_2','TEXCOORD_3']:assert np.array_equal(oa(attrs[name]),na(nattrs[name]))
 changed=np.linalg.norm(v-nv,axis=1)>.00001;assert changed.sum()>40 and np.all(np.all(c[changed]==0,axis=1));assert np.array_equal(v[~changed],nv[~changed])
 # Original reference joints, bind matrices and all skin vertices remain exact.
 assert [(n.get('name'),n.get('translation'),n.get('rotation'))for n in old['nodes']if n.get('name','').startswith(('sk_','d_','attach_'))]==[(n.get('name'),n.get('translation'),n.get('rotation'))for n in new['nodes']if n.get('name','').startswith(('sk_','d_','attach_'))]
 assert np.array_equal(oa(old['skins'][0]['inverseBindMatrices']),na(new['skins'][0]['inverseBindMatrices']))
 assert np.isfinite(nv).all();assert np.array_equal(v.min(0),nv.min(0))and np.array_equal(v.max(0),nv.max(0))
 proof.append({'source':source,'private_mesh':dest,'vertices':len(v),'changed_cuff_vertices':int(changed.sum()),'skin_vertices_exact':True,'indices_uv_skeleton_bind_matrices_exact':True})
for name in ['SK_2015b07','SK_2015e07','SK_2015b02','SK_2123e07']:
 log=(p/(name+'.log')).read_text();assert 'Exporting SkeletalMesh4 '+name in log and 'ERROR:'not in log.replace('ERROR: glTF animation could be exported from mesh viewer only.','')
(p/'mesh-validation.json').write_text(json.dumps({'passed':True,'private_models':356,'two_lods_per_model':True,'source_assets_written':False,'stock_names_overridden':False,'native_reader_samples':4,'unsupported_source_variants_kept_native':build['failed'],'samples':proof,'android_gpu_tested':False},indent=2));print('MESH_PASS',proof)
