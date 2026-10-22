from pathlib import Path
import sys,json,struct,hashlib
import numpy as np
from mesh_tools import Mesh
from gltf_read import Gltf
from iostore import Toc,parse_header,store_entry
from scipy.spatial import cKDTree
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;report=json.loads((out/'build-report.json').read_text());rows=[]
t=Toc(str(out/'container/pc9298_mobile_and.utoc'))
# Verify all chunk digests, exact directory contents and actual container store imports.
for i in range(len(t.ids)):assert hashlib.sha1(t.read(i)).digest()==t.metas[i][:20]
header=parse_header(t.read(next(i for i,c in enumerate(t.ids) if c[11]==10)))
assert header['pids']==[p['package_id'] for p in report['packages']]
for i,p in enumerate(report['packages']):assert store_entry(header['store'],i)[1]==p['imports']
private={p['package_id'] for p in report['packages']};source_pids=set()
for path in list((R/'resources').rglob('*.utoc'))+list((R/'apk').rglob('*.utoc')):
 try:
  c=Toc(str(path));source_pids.update(struct.unpack('<Q',i[:8])[0] for i in c.ids if i[11]==2)
 except Exception:raise
for p in (R/'pc0000').rglob('*.utoc'):
 if p.name=='global.utoc':continue
 c=Toc(str(p));source_pids.update(struct.unpack('<Q',i[:8])[0] for i in c.ids if i[11]==2)
missing=[]
for p in report['packages']:
 for dep in p['imports']:
  if dep not in private|source_pids:missing.append([p['name'],dep])
assert not missing,missing
for p in report['meshes']:
 profile=p['profile'];suffix=p['variant'][4:];name='SK_'+profile+suffix+'_Face';raw=t.read(t.files['RealFace/'+name+'.uasset']);log=(R/('v6-'+profile+suffix+'.log')).read_text();m=Mesh(raw,log)
 g=Gltf(R/'v6-export/Game/Assets/character/RealFace'/(name+'.gltf'));native=Gltf(R/'native-export/Game/Assets/character/RealFace'/('SK_4522'+suffix+'_Face.gltf'));oldraw=(R/'v4a-extracted'/('SK_ND01'+suffix+'_Face.uasset')).read_bytes();old=Mesh(oldraw,(R/('v4a-'+suffix+'.log')).read_text())
 bones=[g.d['nodes'][i]['name'] for i in g.d['skins'][0]['joints']];assert len(bones)==166
 inv=g.get(g.d['skins'][0]['inverseBindMatrices']);assert inv.tobytes()==native.get(native.d['skins'][0]['inverseBindMatrices']).tobytes()
 assert raw[m.r['REF_BEGIN']:m.r['REF_END']]==oldraw[old.r['REF_BEGIN']:old.r['REF_END']]
 allbones=struct.pack('<I',166)+struct.pack('<166H',*range(166));assert len(m.info[0]['bones'])<25
 active=p['active_bones'];packed=struct.pack('<I',len(active))+struct.pack('<%dH'%len(active),*active);assert raw.count(packed)>=3
 assert set(m.info[0]['bones'])<=set(active) and not any(any(word in bones[i] for word in ['hand','foot','shoulder','leg','arm']) for i in active)
 ns=p['skin_vertices'];na=p['accessory_vertices'];nh=p['hair_vertices'];assert len(m.positions)==ns+na+nh;assert m.info[0]['verts']==ns+na and m.info[1]['verts']==nh
 if profile=='ND01':
  assert np.array_equal(m.positions[:ns],old.positions[:ns]);assert np.array_equal(m.positions[ns+na:],old.positions[ns:]);protected=(m.positions[:ns,2]>=164)|(m.positions[:ns,1]>=14.5);assert np.array_equal(m.tangents[:ns][protected],old.tangents[:ns][protected]);assert np.array_equal(m.tangents[ns+na:],old.tangents[ns:]);assert np.array_equal(m.uv[ns+na:],old.uv[ns:]);assert np.array_equal(m.indices[:old.info[0]['tris']],old.indices[:old.info[0]['tris']])
  # Half precision UV rescaling is exact for ordinary source values except very small subnormals.
  assert np.max(abs(m.uv[:ns,:2].astype(float)*2-old.uv[:ns,:2]))<1e-6
  assert all(not any('shoulder' in bones[k] or 'arm' in bones[k] or 'leg' in bones[k] or 'hand' in bones[k] or 'foot' in bones[k] for k,w in row) for row in m.global_weights(0))
 assert len(m.info[0]['bones'])<=75 and len(m.info[1]['bones'])<=75
 skin,hair=g.d['meshes'][0]['primitives'];xyz=g.get(skin['attributes']['POSITION']);joints=g.get(skin['attributes']['JOINTS_0']);w=g.get(skin['attributes']['WEIGHTS_0']);assert np.all(w.sum(1)==255)
 rawpos=m.positions[:ns+na][:,[0,2,1]]/100;assert cKDTree(rawpos).query(xyz)[0].max()<2e-6
 controls={}
 for b in ['skf_jaw','skf_eye_l','skf_eye_r','skf_eyelid_t_l','skf_eyelid_b_l','skf_eyelid_t_r','skf_eyelid_b_r']:
  controls[b]=int(np.any((joints==bones.index(b))&(w>0),axis=1).sum());assert controls[b]>0
 assert controls['skf_eye_l']==controls['skf_eye_r']==44
 # Actual linear blend skinning: independently rotate jaw/eyes using retained inverse bind matrices.
 inv=inv.reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inv);posed=bind.copy()
 for b,axis,angle in [('skf_jaw',0,.20),('skf_eye_l',1,.10),('skf_eye_r',1,-.10)]:
  k=bones.index(b);c=np.cos(angle);s=np.sin(angle);rot=np.eye(4)
  if axis==0:rot[:3,:3]=[[1,0,0],[0,c,-s],[0,s,c]]
  else:rot[:3,:3]=[[c,0,s],[0,1,0],[-s,0,c]]
  posed[k]=bind[k]@rot
 mat=posed@inv;hom=np.c_[xyz,np.ones(len(xyz))];deformed=np.zeros_like(hom)
 for slot in range(4):deformed+=np.einsum('nij,nj->ni',mat[joints[:,slot]],hom)*(w[:,slot]/255)[:,None]
 move=np.linalg.norm(deformed[:,:3]-xyz,axis=1);assert np.isfinite(deformed).all() and move.max()<.07
 for b in ['skf_eye_l','skf_eye_r','skf_jaw']:
  affected=np.any((joints==bones.index(b))&(w>0),axis=1);assert (move[affected]>1e-5).any()
 rows.append(dict(profile=profile,variant=p['variant'],vertices=len(m.positions),skin_vertices=ns,eye_mouth_vertices=na,hair_vertices=nh,native_skeleton_and_bind_bytes_identical=True,active_required_bones=len(active),controls=controls,pose_max_displacement_m=float(move.max()),face_hair_geometry_preserved=profile=='ND01',reader_exported=True))
assert len(rows)==8
result=dict(status='EIGHT_HEAD_ONLY_POSE_SCOPED_MESHES_AND_NATIVE_BIND_PASS',meshes=rows,packages=len(report['packages']),all_chunk_sha1=True,all_imports_resolved_in_private_or_public_containers=True,renderer_tested=False,replay_tested=False,phone_tested=False)
(out/'asset-validation.json').write_text(json.dumps(result,indent=2));print(result['status'])
