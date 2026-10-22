from pathlib import Path
import zipfile,hashlib,json
r=Path(__file__).resolve().parent;out=r.parent
uploads={'CRISTIANO RONALDO 2006.zip':Path('/workspace/attachments/ec9a3e5b-26bf-40ab-8087-41d8c9874e9a/CRISTIANO RONALDO 2006.zip'),'2013.rar':Path('/workspace/attachments/26f1f4c2-6746-4984-bc6d-64fe80c81414/2013.rar'),'2027.rar':Path('/workspace/attachments/ff956d64-99f9-4437-be89-adf2df71ae6a/2027.rar')}
name='Ronaldo-v7-source-and-original-inputs.zip';files=[p for p in r.iterdir() if p.is_file() and p.suffix in ['.py','.c','.sh','.txt','.patch']]+[p for p in out.iterdir() if p.is_file() and (p.suffix in ['.json','.md','.patch'] or p.name=='geometry-texture-diagnostic.png')]+list((out/'references').rglob('*'))
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:
  if p.is_file():z.write(p,str(p.relative_to(out)))
 for label,p in uploads.items():assert p.exists(),p;z.write(p,'original-inputs/'+label)
with zipfile.ZipFile(out/name) as z:assert z.testzip() is None
artifacts=[p for p in out.iterdir() if p.is_file() and (p.suffix in ['.json','.md','.zip','.patch'] or p.name=='geometry-texture-diagnostic.png')]
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(artifacts)))
print(name,(out/name).stat().st_size,'CRC_PASS')
