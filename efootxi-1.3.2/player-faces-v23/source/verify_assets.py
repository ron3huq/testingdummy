from pathlib import Path
import json,struct,subprocess,sys,hashlib
import numpy as np
from PIL import Image,ImageChops
from iostore import Toc,parse_header
from mesh_tools import Mesh
from zen_clone import pid,objid
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');old=Toc(str(O.parent/'player-faces-v22/container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'));logs=O/'reader-logs';logs.mkdir(exist_ok=True)
report={'phone_tested':False,'black_face_root_cause_proven':False,'crash_fixed_on_device_verified':False,'meshes':[]}
def reader(name,mesh=False):
 cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v23-reader'),'-out='+str(R/'v23-export')]
 if mesh:cmd.append('-gltf')
 p=subprocess.run(cmd+[name],capture_output=True);raw=p.stdout+p.stderr;(logs/(name+'.log')).write_bytes(raw);assert p.returncode==0 and b'ERROR:'not in raw.replace(b'ERROR: glTF animation could be exported from mesh viewer only.',b'')
 return raw.decode('utf8','replace')
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
profiles=[('2017','NW01',['','lg00v0000','ep01v0291','ep00v0313']),('2027','NW27',['','lg00v0000','ep01v0291','ep00v0313']),('junior','NWJR',['ep00v0313']),('hoang-duc','NWHD',['ep00v0313']),('ozil','NWOZ',['ep00v0313'])]
allowed=set()
for label,code,suffixes in profiles:
 root=R/'v23-input/ozil'if label=='ozil'else R/'v20-input'/label if label in ['2017','2027']else R/('input-junior'if label=='junior'else'input-hoang-duc')
 models=[]
 for name in ['face_high.fmdl','hair_high.fmdl']:
  f=FmdlFile();f.readFile(str(next(root.rglob(name))));models.append(f)
 skin=[m for m in models[0].meshes if m.materialInstance.name.startswith('fox_skin_mat')]+[m for m in models[1].meshes if m.materialInstance.name.startswith('fox_skin_mat')];pos=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for m in skin for v in m.vertices],dtype='<f4');ns=len(pos)+135
 source_tri=[];offset=0
 for mm in skin:
  ix={id(v):offset+i for i,v in enumerate(mm.vertices)};source_tri.extend([[ix[id(v)]for v in reversed(t.vertices)]for t in mm.faces]);offset+=len(mm.vertices)
 for suf in suffixes:
  name='SK_'+code+suf+'_Face';path='character/RealFace/'+name+'.uasset';allowed.add(path);log=reader(name,True);raw=new.read(new.files[path]);dpath='character/RealFace/SK_ND06'+suf+'_Face.uasset';donor=old.read(old.files[dpath]);dlog=(O.parent/'player-faces-v20/references/ND06'/('v10-ND06'+suf+'.log')).read_text()
  for lod in [0,1]:
   m=Mesh(raw,log,lod);d=Mesh(donor,dlog,lod);assert np.array_equal(m.positions[:len(pos)],pos);assert np.array_equal(m.indices[:len(source_tri)],source_tri)
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
for ext in ['uasset','ubulk']:allowed.add('character/RealFace/T_NW00OZ_Hair_D.'+ext)
for q in ['HQ','MQ']:allowed.add('character/RealFace/MI_NW00OZ_Head_Hair_'+q+'.uasset')
for row in json.loads((O/'mini-framing.json').read_text()):
 card=row['card'];path=next(p for p in old.files if Path(p).name==card+'_.uasset');allowed.add(path);reader(card+'_');a=Image.open(next((R/'v23-export').rglob(card+'_.png'))).convert('RGBA');b=Image.open(O/'art'/(card+'_-decoded.png')).convert('RGBA');assert a.size==b.size==(128,128)and ImageChops.difference(a,b).getbbox()is None;assert row['head_center_x_after']==64 and row['head_top_after']==8
changed=[p for p in new.files if p in old.files and new.read(new.files[p])!=old.read(old.files[p])];removed=set(old.files)-set(new.files)
assert set(changed)<=allowed and not(set(new.files)-set(old.files));assert len(removed)==9 and any('NT01'in p for p in removed)
assert all(old.read(old.files[p])==new.read(new.files[p])for p in old.files if p.endswith('_l.uasset'))
h=parse_header(new.read(next(i for i,c in enumerate(new.ids)if c[11]==10)));ids=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')];assert len(set(ids))==len(ids)and set(ids)==set(h['pids'])
report.update(status='V23_SOURCE_TOPOLOGY_NATIVE_RIG_AND_MINI_READBACK_PASS',changed_chunks=changed,removed_v22_diagnostic_and_Ex_assets=sorted(removed),all_large_portraits_and_v21_backgrounds_byte_identical=True,other_working_faces_and_kits_byte_identical=True)
(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
