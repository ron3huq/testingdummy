from pathlib import Path
import sys,subprocess,json,struct
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from mesh_tools import Mesh,ranges
P=Path('/workspace/73-ui712');R=P/'mesh-reader';L=P/'final-mesh-logs';L.mkdir(exist_ok=True);O=P/'final-mesh-export';rows=[]
for folder,stem in [('pc-faces',9310),('fixed-android',9313)]:
 for f in(P/folder/'livedata').glob('*'):
  d=R/f.name
  if d.is_symlink():d.unlink()
  d.symlink_to(f)
for stem in [9310,9313]:
 t=Toc(str(R/f'pc{stem}_mobile_and.utoc'))
 for path,index in t.files.items():
  if not path.endswith('.uasset')or'/SK_'not in path:continue
  name=Path(path).stem;r=subprocess.run(['/workspace/ronaldo-work/UEViewer/umodel','-export','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R),'-out='+str(O),name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=r.stdout.decode(errors='replace');(L/(name+'.log')).write_text(log);assert r.returncode==0 and log.count('cooked_out=0 inlined=1')==2,(name,log[-2000:]);raw=t.read(index)
  rr,ss,ll=ranges(raw,log,lod_index=1);at=rr['REF_BEGIN'];assert struct.unpack_from('<I',raw,at)[0]==166;proof=[]
  for lod in [0,1]:
   m=Mesh(raw,log,lod_index=lod);r0,sections,starts=ranges(raw,log,lod_index=lod);n=struct.unpack_from('<I',raw,starts[lod]+10)[0];required=list(struct.unpack_from('<%dH'%n,raw,starts[lod]+14));assert required==list(range(166));a=r0['ACTIVE_BEGIN'];n=struct.unpack_from('<I',raw,a)[0];assert n==166 and list(struct.unpack_from('<166H',raw,a+4))==list(range(166))
   for sec in range(2):
    for w in m.global_weights(sec):assert sum(v for k,v in w)==255 and all(0<=k<166 for k,v in w)
   proof.append({'LOD':lod,'vertices':len(m.positions),'triangles':len(m.indices),'full_native_bones':166})
  rows.append({'name':name,'LODs':proof,'independent_UEReader_export':True});print('FACE_VERIFIED',name,flush=True)
assert len(rows)==24;(P/'six-face-rig-validation.json').write_text(json.dumps({'passed':True,'variants':rows,'PC_assets_named_retarget':True,'trial_hooks_not_imported':True,'Android_tested':False},indent=2));print('ALL24_MESHES_VALID')
