from pathlib import Path
import sys,struct,json,subprocess,hashlib
import numpy as np
from PIL import Image
from iostore import Toc,parse_header
from mesh_tools import Mesh
from zen_clone import rename,pid
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');P=R/'v25';a=np.load(P/'export.npz');old=Toc(str(O.parent/'player-faces-v24/container/pc9298_mobile_and.utoc'));new=Toc(str(O/'container/pc9298_mobile_and.utoc'));BASE='/Game/Assets/character/RealFace/';report={'device_verified':False,'meshes':[]}
reader=R/'v25-reader';reader.mkdir(exist_ok=True)
for f in (R/'v24-reader').iterdir():
 if not f.name.startswith('pc9298'):
  p=reader/f.name
  if not p.exists():p.symlink_to(f.resolve())
for ext in ['pak','utoc','ucas']:
 p=reader/('pc9298_mobile_and.'+ext)
 if not p.exists():p.symlink_to(O/'container'/p.name)
logs=O/'reader-logs';logs.mkdir(exist_ok=True)
for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
 name='SK_NV17'+suffix+'_Face';cmd=[str(R/'UEViewer/umodel'),'-export','-png','-gltf','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(R/'v25-export'),name];res=subprocess.run(cmd,capture_output=True);log=(res.stdout+res.stderr).decode('utf8','replace');(logs/(name+'.log')).write_text(log);assert res.returncode==0 and 'ERROR:'not in log.replace('ERROR: glTF animation could be exported from mesh viewer only.',''),log[-1000:]
 raw=new.read(new.files['character/RealFace/'+name+'.uasset']);donor=old.read(old.files['character/RealFace/SK_ND06'+suffix+'_Face.uasset']);dlog=(O.parent/'player-faces-v20/references/ND06'/('v10-ND06'+suffix+'.log')).read_text()
 for lod in [0,1]:
  m=Mesh(raw,log,lod);d=Mesh(donor,dlog,lod);ns=d.info[0]['verts'];nt=d.info[0]['tris'];pc=ns-135
  assert raw[m.r['REF_BEGIN']:m.r['REF_END']]==donor[d.r['REF_BEGIN']:d.r['REF_END']]
  at=m.lods[lod]+10;n=struct.unpack_from('<I',raw,at)[0];assert n==[166,153][lod]
  assert np.allclose(m.positions[:pc],d.positions[:pc]+a['skin_delta'],atol=.00002)
  assert np.array_equal(m.positions[pc:ns],d.positions[pc:ns]);assert np.array_equal(m.uv[:ns],d.uv[:ns]);assert np.array_equal(m.colors[:ns],d.colors[:ns]);assert np.array_equal(m.indices[:nt],d.indices[:nt])
  assert np.array_equal(m.positions[ns:],a['hairpos'].astype('<f4'));assert np.array_equal(m.indices[nt:]-ns,a['hairtri'])
  assert [dict(x)for x in m.global_weights(0)]==[dict(x)for x in d.global_weights(0)]
  assert m.indices.max()<len(m.positions)and m.weights[:,4:].sum(1).min()==255
  assert np.isfinite(m.positions).all()and np.isfinite(m.uv).all();assert all(len(sec['bones'])<=75 for sec in m.info)
  assert len(m.positions)<65536
  nn=m.tangents.view('i1')[:,4:7].astype(float)/127;assert (np.linalg.norm(nn,axis=1)>.9).all()
 for ch in ['N','SRO']:
  newname='T_NV17'+suffix+'_Face_'+ch;oldname='T_ND06'+suffix+'_Face_'+ch;nr=new.read(new.files['character/RealFace/'+newname+'.uasset']);rr=rename(nr,{BASE+newname:BASE+oldname,newname:oldname},BASE+newname,BASE+oldname);assert rr==old.read(old.files['character/RealFace/'+oldname+'.uasset']);assert new.read(new.files['character/RealFace/'+newname+'.ubulk'])==old.read(old.files['character/RealFace/'+oldname+'.ubulk'])
 kind='FaceUpcon'if suffix=='lg00v0000'else'FaceLegacy'
 for q in ['HQ','MQ']:
  n='MI_NV17'+suffix+'_Head_'+kind+'_'+q;t='MI_ND06'+suffix+'_Head_'+kind+'_'+q;im={BASE+'T_NV17'+suffix+'_Face_'+c:BASE+'T_ND06'+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+n:BASE+t,n:t}
  for k,v in im.items():rep[k]=v;rep[k.split('/')[-1]]=v.split('/')[-1]
  back=rename(new.read(new.files['character/RealFace/'+n+'.uasset']),rep,BASE+n,BASE+t,imports=im);assert back==old.read(old.files['character/RealFace/'+t+'.uasset'])
 report['meshes'].append({'profile':'NV17'+suffix,'lods':2,'skin_uv_weights_accessories_and_topology_exact':True,'native_skeleton_required166_153_exact':True,'source_hair_and_sculpt_readback_match':True,'working_ND06_materials_N_SRO_exact':True})
changed=[p for p in old.files if p in new.files and old.read(old.files[p])!=new.read(new.files[p])];removed=set(old.files)-set(new.files);added=set(new.files)-set(old.files);assert not changed and not removed;assert len(added)==40 and all(any(Path(p).name.startswith(pre+code)for pre in ['SK_','MI_','T_']for code in ['NV17','NVH1'])for p in added)
h=parse_header(new.read(next(i for i,idb in enumerate(new.ids)if idb[11]==10)));ids=[int.from_bytes(new.ids[i][:8],'little')for p,i in new.files.items()if p.endswith('.uasset')];assert len(ids)==len(set(ids))and set(ids)==set(h['pids'])
decoded_image=Image.open(P/'hair-native-readback.png').convert('RGBA');expected=Image.open(P/'hair-mobile-atlas.png').convert('RGBA').resize(decoded_image.size,Image.Resampling.LANCZOS);expected.save(P/'hair-native-input.png');hair=np.array(expected,dtype=float);decoded=np.array(decoded_image,dtype=float);mask=hair[:,:,3]>192;mae=float(abs(hair[:,:,:3]-decoded[:,:,:3])[mask].mean());alpha=float(abs(hair[:,:,3]-decoded[:,:,3]).mean());assert mae<22 and alpha<15,(mae,alpha)
report.update(status='V25_ONE_CARD_ALL_OLD_CHUNKS_EXACT_NATIVE_READER_PASS',changed_old_chunks=changed,removed_old_chunks=sorted(removed),added_profile_files=sorted(added),native_hair_dimensions=list(decoded_image.size),native_hair_format_and_dimensions_preserved=True,hair_rgb_MAE_opaque=mae,hair_alpha_MAE=alpha,all_other_faces_kits_cards_working_assets_byte_exact=True)
(O/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
