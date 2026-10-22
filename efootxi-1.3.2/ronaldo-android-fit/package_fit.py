from pathlib import Path
import zipfile,json,hashlib
r=Path(__file__).parent;files={}
for n in ['README.md','unpack-validation.json','head-assets.json','validation.json','dependency-search.json','procedural-research.json','ueviewer-local.patch','fit_android_head.py','validate_head.py','extract_ronaldo.py','unpack.py','umodel-lod-audit.log']:
 files[n]=r/n
for folder in ['fit','extracted','export']:
 for p in (r/folder).rglob('*'):
  if p.is_file() and p.suffix in ['.blend','.fbx','.glb','.png','.json','.uasset','.gltf','.bin']:files[str(p.relative_to(r))]=p
files['UEViewer-LICENSE.txt']=r.parent/'UEViewer/LICENSE.txt'
sums={n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in files.items()}
z=r/'Ronaldo-ANDROID-head-noodle-REFERENCE-NOT-INSTALLABLE.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as f:
 for n,p in files.items():f.write(p,n)
 f.writestr('SHA256SUMS',''.join(sums[n]+'  '+n+'\n' for n in sorted(sums)))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for n,v in sums.items():assert hashlib.sha256(f.read(n)).hexdigest()==v
info={'zip':z.name,'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'files':len(files)+1,'installable':False};(r/'package-validation.json').write_text(json.dumps(info,indent=2));print(json.dumps(info,indent=2))
