from pathlib import Path
import zipfile,hashlib,json
r=Path(__file__).resolve().parent
files={}
for name in ['README.md','source-inventory.json','model-analysis.json','bone-name-comparison.json','conversion-notes.json','validation.json','inspect_models.py','build_blender.py','validate_conversion.py']:
 files[name]=r/name
files['Ronaldo_source_preview.png']=r/'converted/Ronaldo_source_preview.png'
for folder in ['source-extracted','converted']:
 for p in sorted((r/folder).iterdir()):
  if not p.is_file() or p.suffix not in ['.fmdl','.bin','.ftex','.blend','.fbx','.glb','.png','.dds']:continue
  if p.name.startswith('preview_') or p.name.endswith('_RGB.png') or p.name=='Ronaldo_source_preview.png':continue
  files[str(p.relative_to(r))]=p
manifest={n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in files.items()}
z=r/'Ronaldo-noodle-88044950524330-SOURCE-NOT-INSTALLABLE.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as f:
 for n,p in files.items():f.write(p,n)
 f.writestr('SHA256SUMS',''.join(manifest[n]+'  '+n+'\n' for n in sorted(manifest)))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for n,s in manifest.items():assert hashlib.sha256(f.read(n)).hexdigest()==s
info={'zip':z.name,'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'files':len(files)+1,'installable':False}
(r/'package-validation.json').write_text(json.dumps(info,indent=2));print(json.dumps(info,indent=2))
