from pathlib import Path
import subprocess,concurrent.futures,json,struct,hashlib
import numpy as np
from PIL import Image
from iostore import Toc
from mesh_tools import Mesh
from gltf_read import Gltf
from head_mq_and_seams import name_list
out=Path(__file__).resolve().parent.parent;work=Path('/workspace/ronaldo-work');old=Toc(str(out.parent/'player-faces-v16/container/pc9298_mobile_and.utoc'));new=Toc(str(out/'container/pc9298_mobile_and.utoc'));report=json.loads((out/'asset-rebase-build.json').read_text());records=report['changed_meshes'];logs=out/'reader-logs';logs.mkdir(exist_ok=True)
def export(row):
 name=row['mesh'];path=work/'v18-verified'/name;cmd=['/workspace/ronaldo-work/UEViewer/umodel','-export','-gltf','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(work/'v18-reader'),'-out='+str(path),name]
 # Use the audited original container key; keep SHA hashes separate from AES.
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(logs/(name+'.log')).write_text(p.stdout);assert p.returncode==0 and 'Exporting SkeletalMesh4 '+name in p.stdout,(name,p.stdout[-1500:]);return row,path,p.stdout
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(export,records));validation=[]
for row,exported,log in results:
 oldname='SK_'+row['old_profile']+'_Face';newname=row['mesh'];oldpath='character/RealFace/'+oldname+'.uasset';newpath='character/RealFace/'+newname+'.uasset';a=old.read(old.files[oldpath]);b=new.read(new.files[newpath]);oldlog=(out/'references/original'/('v10-'+row['old_profile']+'.log')).read_text();lodrows=[]
 for lod in [0,1]:
  left=Mesh(a,oldlog,lod);right=Mesh(b,log,lod)
  for attr in ['positions','indices','tangents','uv','colors','weights']:assert np.array_equal(getattr(left,attr),getattr(right,attr)),(newname,lod,attr)
  assert [q['bones'] for q in left.info]==[q['bones'] for q in right.info]
  assert all(len(q['bones'])<=75 for q in right.info)
  assert a[left.r['REF_BEGIN']:left.r['REF_END']]==b[right.r['REF_BEGIN']:right.r['REF_END']]
  assert a[left.lods[0]:]==b[right.lods[0]:]
  for field,last in [('ACTIVE_BEGIN','ACTIVE_END')]:assert a[left.r[field]:left.r[last]]==b[right.r[field]:right.r[last]]
  lo=left.lods[lod];ro=right.lods[lod];count=struct.unpack_from('<I',a,lo+10)[0];assert a[lo+10:lo+14+count*2]==b[ro+10:ro+14+count*2];assert count==[166,153][lod]
  lodrows.append({'lod':lod,'required_bones':count,'all_vertex_arrays_and_bonemaps_identical':True,'active_bones_identical':True})
 for channel in ['D','N','SRO']:
  oldtex='T_'+row['old_profile']+'_Face_'+channel;newtex='T_'+row['new_profile']+'_Face_'+channel
  assert old.read(old.files['character/RealFace/'+oldtex+'.ubulk'])==new.read(new.files['character/RealFace/'+newtex+'.ubulk'])
  key='character/RealFace/'+newtex+'.uasset';nb=new.read(new.files[key]);ob=old.read(old.files['character/RealFace/'+oldtex+'.uasset']);x=nb.rfind(b'PF_ETC2_RGB\0');y=ob.rfind(b'PF_ETC2_RGB\0');assert nb[x:]==ob[y:]
 # Diffuse read-back must equal the original exported decoded pixels exactly.
 got=Image.open(next(exported.rglob('T_'+row['new_profile']+'_Face_D.png'))).convert('RGBA');prior=Image.open(out/'references/original-diffuse'/('T_'+row['old_profile']+'_Face_D.png')).convert('RGBA');assert got.size==prior.size==(2048,2048);assert np.array_equal(np.asarray(got),np.asarray(prior))
 validation.append({'profile':row['new_profile'],'lods':lodrows,'diffuse_UEViewer_readback_pixel_identical_to_original':True,'all_texture_mip_and_bulk_payloads_identical':True})
# Approved heads, all hair assets, all card art remain byte-for-byte identical.
unchanged=[]
for path,i in old.files.items():
 if path not in new.files:continue
 assert old.read(i)==new.read(new.files[path]);unchanged.append(path)
assert len(unchanged)==209
final={'status':'TEN_REBASED_MESHES_TWENTY_LODS_ORIGINAL_GEOMETRY_AND_PIXELS_PRESERVED_PASS','meshes':validation,'unchanged_chunks':len(unchanged),'unchanged_card_art_chunks':sum(p.startswith('ui/') for p in unchanged),'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'phone_tested':False,'renderer_black_face_fix_verified':False};(out/'asset-validation.json').write_text(json.dumps(final,indent=2));print(final['status'])
