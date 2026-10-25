from pathlib import Path
import json,numpy as np
P=Path('/workspace/ronaldo-work/73-ui3');build=json.loads((P/'rolled-build.json').read_text());assert build['count']==356 and all(len(r['lods'])==2 for r in build['models'])
def load(root,name):
 j=json.loads((root/(name+'.gltf')).read_text());raw=(root/(name+'.bin')).read_bytes()
 def arr(i):
  a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];return np.frombuffer(raw,dtype=dt,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
 return j,arr
proof=[]
for source,dest in [('SK_015a07','SK_2015b07'),('SK_015d07','SK_2015e07')]:
 old,oa=load(Path('/workspace/ronaldo-work/73-ui2/cloth-export/Game/Assets/character/Body'),source);new,na=load(P/'rolled-export/Game/Assets/character/Body',dest);prior,pa=load(Path('/workspace/ronaldo-work/73-ui2/rolled-export/Game/Assets/character/Body'),dest)
 op=old['meshes'][0]['primitives'][0];np_=new['meshes'][0]['primitives'][0];pp=prior['meshes'][0]['primitives'][0];attrs=op['attributes'];nattrs=np_['attributes'];v=oa(attrs['POSITION']);nv=na(nattrs['POSITION']);pv=pa(pp['attributes']['POSITION']);c=oa(attrs['COLOR_0']);assert v.shape==nv.shape
 assert np.array_equal(oa(op['indices']),na(np_['indices']))and np.array_equal(c,na(nattrs['COLOR_0']))
 for name in ['TEXCOORD_0','TEXCOORD_1','TEXCOORD_2','TEXCOORD_3']:assert np.array_equal(oa(attrs[name]),na(nattrs[name]))
 changed=np.linalg.norm(v-nv,axis=1)>1e-5;cloth=np.all(c==0,axis=1);assert np.any(changed&cloth)
 # No change to torso, neck, legs or visible bare wrists/hands. Hidden arm skin
 # is tucked inside cloth rather than leaving an intersecting second surface.
 far=(abs(v[:,0])>.54)|(abs(v[:,0])<.20)|(v[:,1]<1.)
 assert np.array_equal(v[far],nv[far])
 assert [(n.get('name'),n.get('translation'),n.get('rotation'))for n in old['nodes']if n.get('name','').startswith(('sk_','d_','attach_'))]==[(n.get('name'),n.get('translation'),n.get('rotation'))for n in new['nodes']if n.get('name','').startswith(('sk_','d_','attach_'))]
 assert np.array_equal(oa(old['skins'][0]['inverseBindMatrices']),na(new['skins'][0]['inverseBindMatrices']))
 assert np.isfinite(nv).all()and np.array_equal(v.min(0),nv.min(0))and np.array_equal(v.max(0),nv.max(0))
 # Width in the depth axis catches UI2's oversized cuff independently of the fitter.
 region=cloth&(abs(nv[:,0])>.30)&(abs(nv[:,0])<.48)
 oldwidth=np.ptp(pv[region,2]);newwidth=np.ptp(nv[region,2]);assert newwidth<oldwidth*.90,(oldwidth,newwidth)
 row=next(r for r in build['models']if r['destination']==dest);side=row['lods'][0]['sides'][1];axis=np.array(side['axis']);center=np.array(side['center'])
 # glTF exports UE XYZ as X,Z,-Y in meters. Measure cuff progress along
 # the actual forearm, so the narrower radius does not hide the lower hem.
 def along(points):return (np.stack([points[:,0],-points[:,2],points[:,1]],axis=1)*100-center)@axis
 arm=cloth&(nv[:,0]>.2);oldend=along(pv)[arm].max();newend=along(nv)[arm].max();assert 1<newend-oldend<5,(oldend,newend)
 proof.append({'mesh':dest,'vertices':len(v),'UI2_sleeve_depth_cm':round(float(oldwidth*100),2),'UI3_sleeve_depth_cm':round(float(newwidth*100),2),'cuff_lowered_cm':round(float(newend-oldend),2),'changed_vertices':int(changed.sum()),'hidden_skin_tucked':int((changed&~cloth).sum()),'visible_wrist_and_torso_unchanged':True,'indices_uv_skeleton_bind_matrices_exact':True})
for name in ['SK_2015b07','SK_2015e07','SK_2015b02','SK_2123e07']:
 log=(P/(name+'.log')).read_text();assert 'Exporting SkeletalMesh4 '+name in log and 'ERROR:'not in log.replace('ERROR: glTF animation could be exported from mesh viewer only.','')
(P/'mesh-validation.json').write_text(json.dumps({'passed':True,'private_models':356,'two_lods_per_model':True,'stock_names_overridden':False,'native_reader_samples':4,'samples':proof,'android_gpu_tested':False},indent=2));print('MESH_PASS',proof)
