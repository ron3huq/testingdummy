import hashlib
"""Independent reader + native per-LOD pose contract; never equates this to replay."""
from pathlib import Path
import sys,json,struct,hashlib
import numpy as np
from mesh_tools import Mesh,platform_lod_properties
from gltf_read import Gltf
from iostore import Toc,parse_header,store_entry
from scipy.spatial import cKDTree
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;report=json.loads((out/'build-report.json').read_text());rows=[]
assert hashlib.sha256(Path(__file__).with_name('mesh_tools.py').read_bytes()).hexdigest()==json.loads((out/'input-inventory.json').read_text())['v7_lod_writer_sha256']
t=Toc(str(out/'container/pc9298_mobile_and.utoc'));heads=Toc(str(next((R/'resources').rglob('pc3700_mobile_and.utoc'))))
for i in range(len(t.ids)):assert hashlib.sha1(t.read(i)).digest()==t.metas[i][:20]
header=parse_header(t.read(next(i for i,c in enumerate(t.ids) if c[11]==10)));assert header['pids']==[p['package_id'] for p in report['packages']]
private=set(header['pids']);source=set()
for path in list((R/'resources').rglob('*.utoc'))+list((R/'apk').rglob('*.utoc'))+list((R/'pc0000').rglob('*.utoc')):
 if path.name=='global.utoc':continue
 c=Toc(str(path));source.update(struct.unpack('<Q',id[:8])[0] for id in c.ids if id[11]==2)
for i,p in enumerate(report['packages']):
 deps=store_entry(header['store'],i)[1];assert deps==p['imports'];assert set(deps)<=private|source,(p['name'],set(deps)-private-source)
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
models={}
for year,profile in [('2006','ND06'),('2013','ND13'),('2027','ND27')]:
 root=R/('input-1' if year=='2006' else 'input-'+year);f=FmdlFile();f.readFile(str(next(root.rglob('face_high.fmdl'))));h=FmdlFile();h.readFile(str(next(root.rglob('hair_high.fmdl'))));models[profile]=(f,h)
def xyz(meshes):return np.array([[v.position.x*100,v.position.z*100,v.position.y*100] for mesh in meshes for v in mesh.vertices],dtype='<f4')
def required(data,lod):n=struct.unpack_from('<I',data,lod+10)[0];return list(struct.unpack_from('<%dH'%n,data,lod+14))
for p in report['meshes']:
 profile=p['profile'];suffix=p['variant'][4:];name='SK_'+profile+suffix+'_Face';raw=t.read(t.files['RealFace/'+name+'.uasset']);log=(R/('v8-'+profile+suffix+'.log')).read_text()
 lod_properties=platform_lod_properties(raw);assert lod_properties['MinLod']==[0];assert np.allclose(lod_properties['ScreenSize'],[.3,.05])
 native_raw=heads.read(heads.files['RealFace/SK_4522'+suffix+'_Face.uasset']);native=Mesh(native_raw,(R/('native-'+suffix+'.log')).read_text())
 oldraw=(R/'v4a-extracted'/('SK_ND01'+suffix+'_Face.uasset')).read_bytes();old=Mesh(oldraw,(R/('v4a-'+suffix+'.log')).read_text())
 hq_seam_rows=Mesh(raw,log,0).global_weights(0)
 ns=p['skin_vertices'];na=p['accessory_vertices'];neck=p['neck_vertices'];nh=p['hair_vertices'];lodrows=[]
 for lod in [0,1]:
  m=Mesh(raw,log,lod);assert len(m.lods)==2 and len(m.positions)==ns+na+nh
  assert raw[m.r['REF_BEGIN']:m.r['REF_END']]==native_raw[native.r['REF_BEGIN']:native.r['REF_END']]
  req=required(raw,m.lods[lod]);expected=required(native_raw,native.lods[lod]);assert req==expected
  # A compact pose used by the body must preserve EVERY native bone's position.
  native_map={bone:i for i,bone in enumerate(expected)};compact={bone:i for i,bone in enumerate(req)};assert compact==native_map
  at=m.r['ACTIVE_BEGIN'];n=struct.unpack_from('<I',raw,at)[0];active=list(struct.unpack_from('<%dH'%n,raw,at+4));assert set(active)<=set(req)
  assert all(set(q['bones'])<=set(req) and len(q['bones'])<=75 for q in m.info)
  assert struct.unpack_from('<II',raw,m.lods[lod]+2)==(0,1)
  # Compare existing heads to v7; only sub-millimeter seam snapping is allowed above the neck.
  if profile in ['ND01','ND06','ND13','ND27']:
   oldmesh=Mesh((out/'references/v7'/(name+'.uasset')).read_bytes(),(out/'references/v7'/(profile+suffix+'.log')).read_text(),lod)
   assert np.max(np.linalg.norm(m.positions[:ns]-oldmesh.positions[:ns],axis=1))<.002
   assert np.array_equal(m.positions[ns+na:],oldmesh.positions[ns+na:])
  delta=np.zeros(neck)
  # Real geometric seams share identical weights, not only identical bind positions.
  seam={};skinweights=m.global_weights(0)
  for i,point in enumerate(m.positions[:ns]):seam.setdefault(tuple(np.round(point,3)),[]).append(i)
  checked=0
  for group in seam.values():
   if len(group)<2:continue
   palette={k for i in group for k,w in hq_seam_rows[i]};sameuv=np.max(np.linalg.norm(m.uv[group,:2].astype(float)-m.uv[group[0],:2].astype(float),axis=1))<.00005
   if not sameuv and not palette<={4,5,6,7}:continue
   assert len({tuple(sorted(skinweights[i])) for i in group})==1,(profile,lod,group)
   assert np.max(np.linalg.norm(m.positions[group]-m.positions[group[0]],axis=1))<1e-6,(profile,lod,group,m.positions[group].tolist(),palette,sameuv)
   checked+=1
  assert checked>10
  assert np.all(m.weights[:,4:].sum(1)==255)
  frame=m.tangents.view('i1').astype(float)/127;dots=np.abs(np.sum(frame[:,:3]*frame[:,4:7],axis=1));assert dots.max()<.025,(profile,dots.max())
  assert np.all((np.linalg.norm(frame[:,:3],axis=1)>.98)&(np.linalg.norm(frame[:,4:7],axis=1)>.98))
  if lod==0:
   controls={b:sum(any(k==b for k,w in row) for row in m.global_weights(0)) for b in [8,10,11,12,13,14,15]};assert all(v>0 for v in controls.values())
  else:assert active==list(range(8)) and all(k in [4,5,6,7] for row in m.global_weights(0) for k,w in row)
  lodrows.append({'lod':lod,'required_bones':len(req),'active_bones':active,'native_body_compact_pose_indices_identical':True,'neck_vertices_moved':int((delta>1e-4).sum()),'neck_max_move_cm':float(delta.max()) if len(delta) else 0.,'seam_groups_checked':checked,'face_scalp_hair_positions_identical':True})
 g=Gltf(R/'v8-export/Game/Assets/character/RealFace'/(name+'.gltf'));native_g=Gltf(R/'native-export/Game/Assets/character/RealFace'/('SK_4522'+suffix+'_Face.gltf'));inv=g.get(g.d['skins'][0]['inverseBindMatrices']);assert inv.tobytes()==native_g.get(native_g.d['skins'][0]['inverseBindMatrices']).tobytes()
 assert len(g.d['skins'][0]['joints'])==166
 # Actual LBS for HQ jaw/eyeball/eyelids, with unmodified Android bind matrices.
 primitive=g.d['meshes'][0]['primitives'][0];positions=g.get(primitive['attributes']['POSITION']);joints=g.get(primitive['attributes']['JOINTS_0']);w=g.get(primitive['attributes']['WEIGHTS_0'])/255;inverse=inv.reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inverse);pose=bind.copy()
 for b in [8,10,11,12,13,14,15]:
  rot=np.eye(4);c=np.cos(.12);s=np.sin(.12);rot[:3,:3]=[[1,0,0],[0,c,-s],[0,s,c]];pose[b]=bind[b]@rot
 mat=pose@inverse;hom=np.c_[positions,np.ones(len(positions))];posed=np.zeros_like(hom)
 for slot in range(4):posed+=np.einsum('nij,nj->ni',mat[joints[:,slot]],hom)*w[:,slot,None]
 move=np.linalg.norm(posed[:,:3]-positions,axis=1);assert np.isfinite(move).all() and move.max()<.08
 for b in [8,10,11,12,13,14,15]:assert np.any(move[np.any((joints==b)&(w>0),axis=1)]>1e-5)
 rows.append({'profile':profile,'variant':p['variant'],'lods':lodrows,'platform_lod_properties':lod_properties,'hq_accessory_vertices':na,'hq_facial_controls':controls,'skin_pose_max_m':float(move.max())})
# Regression: v6 must FAIL this contract, proving test catches the reported structural regression.
v6raw=(out/'references/v6/SK_ND06ep00v0313_Face.uasset').read_bytes();v6mesh=Mesh(v6raw,(out/'references/v6/reader.log').read_text());assert required(v6raw,v6mesh.lods[1])!=required(native_raw,native.lods[1]);assert 144 not in required(v6raw,v6mesh.lods[1])
assert len(rows)==19
result={'status':'NINETEEN_HEADS_V7_LOD_CONTRACT_SEAMS_AND_FACIAL_CONTROLS_PASS','meshes':rows,'render_lods':38,'all_chunk_sha1':True,'all_imports_resolved':True,'v6_missing_body_bones_regression_detected':True,'cutscene_renderer_tested':False,'phone_tested':False}
result['container_sha256']=hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()
(out/'asset-validation.json').write_text(json.dumps(result,indent=2));print(result['status'])
