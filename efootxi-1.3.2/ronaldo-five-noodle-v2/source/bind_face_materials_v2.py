from pathlib import Path
import sys,json,struct,subprocess,hashlib,shutil
R=Path(__file__).parent;V=R/'v2';P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/sys.argv[1];sys.path.insert(0,str(N));from zen_clone import rename,pid
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc
source=Toc('/workspace/analysis/my-league/android/official-apk/assets/gateway-release/livedata/pc9257_mobile_and.utoc');targets=json.loads((V/'targets.json').read_text());meta=json.loads((N/'deploy/work/tools/noodle_bundle.json').read_text());targets={k:v for k,v in targets.items()if k in meta['target_card_ids']};base='/Game/Assets/character/RealFace/';report={}
for card,row in targets.items():
 imports={base+'T_133157_Face_'+kind:base+'T_'+row['prefix']+'_Face_'+kind for kind in ['D','N','SRO']}
 for quality in ['HQ','MQ']:
  old='MI_133157_Head_FaceUpcon_'+quality;new='MI_'+row['material_prefix']+'_Head_FaceLegacy_'+quality;rep={base+old:base+new,old:new}
  mapping=imports.copy()
  if quality=='HQ':
   root='/Game/Assets/MaterialLibrary/Character/Head/MasterMaterials/';mapping[root+'MI_Head_FaceUpcon_HQ']=root+'MI_Head_FaceLegacy_HQ'
  for a,b in mapping.items():rep[a]=b;rep[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
  data=source.read(source.files['character/RealFace/'+old+'.uasset']);data=rename(data,rep,base+old,base+new,imports=mapping);(N/'asset'/(new+'.uasset')).write_bytes(data)
 for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
  f=N/'asset'/('SK_'+variant.replace('4522',row['prefix'],1)+'_Face.uasset');rep={};im={}
  for quality in ['HQ','MQ']:
   for part in ['FaceLegacy','FaceUpcon','Hair']:
    old=base+'MI_'+variant+'_Head_'+part+'_'+quality;new=base+'MI_'+row['material_prefix']+'_Head_'+('Hair'if part=='Hair'else'FaceLegacy')+'_'+quality;rep[old]=new;rep[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1];im[old]=new
  f.write_bytes(rename(f.read_bytes(),rep,imports=im))
 report[card]={'private_face_mi_hq_mq':True,'normal_sro_bound_in_private_material':True,'legacy_hq_parent_retained':True,'mq_native_face_parent':True}
s=(N/'build_full_container.py').read_text();s=s.replace("parts=['Hair']if True else['Hair','FaceLegacy','FaceUpcon']", "parts=['Hair','FaceLegacy','FaceUpcon']")
s=s.replace("pid(base+'MI_'+mi+'_Head_Hair_'+q)for part in parts", "pid(base+'MI_'+mi+'_Head_'+('Hair'if part=='Hair'else'FaceLegacy')+'_'+q)for part in parts")
if 'private face materials bind' not in s:
 at=s.index('chunks=[];');s=s[:at]+'''# private face materials bind the matching albedo/normal/SRO atlas set
for kind,row in targets.items():
 mi=row['material_prefix'];prefix=row['prefix'];teximports={pid(base+'T_133157_Face_'+x):pid(base+'T_'+prefix+'_Face_'+x)for x in ['D','N','SRO']}
 for q in ['HQ','MQ']:
  mapping=teximports.copy()
  if q=='HQ':
   root='/Game/Assets/MaterialLibrary/Character/Head/MasterMaterials/';mapping[pid(root+'MI_Head_FaceUpcon_HQ')]=pid(root+'MI_Head_FaceLegacy_HQ')
  recipes.append(('MI_'+mi+'_Head_FaceLegacy_'+q,mats,'character/RealFace/MI_133157_Head_FaceUpcon_'+q+'.uasset',mapping))
'''+s[at:]
 (N/'build_full_container.py').write_text(s)
subprocess.run([sys.executable,str(N/'build_full_container.py')],check=True);t=N/'deploy/work/tools';l=N/'deploy/livedata'
for ext in ['pak','utoc','ucas']:
 name='pc9298_mobile_and.'+ext;data=(N/'container'/name).read_bytes();(l/name).write_bytes(data);meta['files'][name]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));(N/'face-material-validation.json').write_text(json.dumps({'phone_tested':False,'cards':report},indent=2))
for name in ['validate_runtime.py','read_assets.py']:subprocess.run([sys.executable,str(N/name)],check=True)
# A missing face material must no longer be silently represented by dummy_material_0.
folder=N/'export-final/Game/Assets/character/RealFace'
for card,row in targets.items():
 g=json.loads((folder/('SK_'+row['prefix']+'_Face.gltf')).read_text());name=g['materials'][g['meshes'][0]['primitives'][0]['material']]['name'];assert name=='MI_'+row['material_prefix']+'_Head_FaceLegacy_MQ',(card,name)
print('PRIVATE_FACE_MATERIALS_RESOLVE_FOR_ALL_CARDS',flush=True)
