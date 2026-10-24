from pathlib import Path
import json,struct,subprocess,sys,hashlib
import numpy as np
from PIL import Image,ImageChops
from iostore import Toc,parse_header
from mesh_tools import Mesh
from zen_clone import pid,objid
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');old=Toc(str(O.parent/'player-faces-v23/container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'));logs=O/'reader-logs';logs.mkdir(exist_ok=True)
report={'phone_tested':False,'black_face_root_cause_proven':False,'crash_fixed_on_device_verified':False,'meshes':[]}
def reader(name,mesh=False):
 cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v24-reader'),'-out='+str(R/'v24-export')]
 if mesh:cmd.append('-gltf')
 p=subprocess.run(cmd+[name],capture_output=True);raw=p.stdout+p.stderr;(logs/(name+'.log')).write_bytes(raw);assert p.returncode==0 and b'ERROR:'not in raw.replace(b'ERROR: glTF animation could be exported from mesh viewer only.',b'')
 return raw.decode('utf8','replace')
from source_models import load
profiles=[('rp','NX01',['','lg00v0000','ep01v0291','ep00v0313']),('2027','NX27',['','lg00v0000','ep01v0291','ep00v0313']),('prince','NXJR',['ep00v0313']),('fifa','NXNC',['ep00v0313'])]
allowed=set()
for label,code,suffixes in profiles:
 root,face,hair=load(label);models=[face,hair]
 skin=[m for f in models for m in f.meshes if m.materialInstance.name=='fox_skin_mat'and not getattr(m,'skip_native',False)];pos=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for m in skin for v in m.vertices],dtype='<f4');ns=len(pos)+135
 hairmeshes=[m for m in hair.meshes if not getattr(m,'skip_native',False)and m.materialInstance.name not in ['fox_skin_mat','fox_head_shell_mat']and'eye'not in m.materialInstance.name and any(role=='Base_Tex_SRGB'for role,t in m.materialInstance.textures)];hairpos=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for m in hairmeshes for v in m.vertices],dtype='<f4')
 source_tri=[];offset=0
 for mm in skin:
  ix={id(v):offset+i for i,v in enumerate(mm.vertices)};source_tri.extend([[ix[id(v)]for v in (reversed(t.vertices)if label=='fifa'else t.vertices)]for t in mm.faces]);offset+=len(mm.vertices)
 for suf in suffixes:
  name='SK_'+code+suf+'_Face';path='character/RealFace/'+name+'.uasset';allowed.add(path);log=reader(name,True);raw=new.read(new.files[path]);dpath='character/RealFace/SK_ND06'+suf+'_Face.uasset';donor=old.read(old.files[dpath]);dlog=(O.parent/'player-faces-v20/references/ND06'/('v10-ND06'+suf+'.log')).read_text()
  for lod in [0,1]:
   m=Mesh(raw,log,lod);d=Mesh(donor,dlog,lod);assert np.array_equal(m.positions[:len(pos)],pos)and np.array_equal(m.positions[ns:],hairpos);assert np.array_equal(m.indices[:len(source_tri)],source_tri)
   assert raw[m.r['REF_BEGIN']:m.r['REF_END']]==donor[d.r['REF_BEGIN']:d.r['REF_END']]
   required_at=m.lods[lod]+10;n=struct.unpack_from('<I',raw,required_at)[0];assert n==[166,153][lod]
   assert m.info[0]['verts']==ns and np.isfinite(m.positions).all()and np.isfinite(m.uv).all()
   assert m.indices.max()<len(m.positions)and (m.weights[:,4:].sum(1)==255).all()
   for section in m.info:assert len(section['bones'])<=75
   # Source topology and static neck controls, no PC hand/foot indices.
   assert all(b<=15 for sec in m.info for b in sec['bones'])
   normals=m.tangents.view('i1')[:,4:7].astype(float)/127;assert (np.linalg.norm(normals,axis=1)>.90).all()
  report['meshes'].append({'profile':code+suf,'source_skin_vertices':len(pos),'skin_and_scalp_positions_exact':True,'source_triangles_exact':True,'native_accessory_vertices':135,'native_skeleton_and_LOD_required_bones_exact':True})
  for ch in ['D','N','SRO']:
   for ext in ['uasset','ubulk']:allowed.add('character/RealFace/T_'+code+suf+'_Face_'+ch+'.'+ext)
  kind='FaceUpcon'if suf=='lg00v0000'else'FaceLegacy'
  for q in ['HQ','MQ']:allowed.add('character/RealFace/MI_'+code+suf+'_Head_'+kind+'_'+q+'.uasset')
for haircode in ['NXH1','NXHJ','NXHN','NXH7']:
 for ext in ['uasset','ubulk']:allowed.add('character/RealFace/T_'+haircode+'_Hair_D.'+ext)
 for q in ['HQ','MQ']:allowed.add('character/RealFace/MI_'+haircode+'_Head_Hair_'+q+'.uasset')
changed=[p for p in new.files if p in old.files and new.read(new.files[p])!=old.read(old.files[p])];removed=set(old.files)-set(new.files)
added=set(new.files)-set(old.files);assert not changed and added<=allowed
assert removed and all(any(Path(p).name.startswith(pre+code)for pre in ['SK_','MI_','T_']for code in ['NW01','NW27','NWJR'])for p in removed)
assert len(report['meshes'])==10
assert all(old.read(old.files[p])==new.read(new.files[p])for p in old.files if p.startswith('ui/')or'/Uniform/'in p)
assert all(old.read(old.files[p])==new.read(new.files[p])for p in old.files if p.endswith('_l.uasset'))
h=parse_header(new.read(next(i for i,c in enumerate(new.ids)if c[11]==10)));ids=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')];assert len(set(ids))==len(ids)and set(ids)==set(h['pids'])
report.update(status='V24_SOURCE_TOPOLOGY_NATIVE_RIG_AND_MINI_READBACK_PASS',changed_chunks=changed,removed_superseded_skin_assets=sorted(removed),new_profile_assets=sorted(added),all_large_portraits_and_v21_backgrounds_byte_identical=True,all_retained_faces_UI_and_kits_byte_identical=True)
(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
