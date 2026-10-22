from pathlib import Path
import zipfile,hashlib,json
out=Path(__file__).resolve().parent.parent
names=[]
attachments=Path('/workspace/attachments')
archive_paths={name:(out/'original-inputs'/name) if (out/'original-inputs'/name).exists() else next(attachments.rglob(name)) for name in names}
name='Faces-v12-source-and-research.zip'
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in (out/'source').glob('*'):
  if p.suffix in ['.py','.c','.sh','.txt','.patch']:z.write(p,'source/'+p.name)
 for p in (out/'card-art-research').rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(out)))
 for p in (out/'body-skin-research').rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(out)))
 for p in (out/'references').rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(out)))
 for p in out.glob('*'):
  if p.suffix in ['.json','.md'] or p.name=='geometry-texture-diagnostic.png':z.write(p,p.name)
 for name,p in archive_paths.items():z.write(p,'original-inputs/'+name)
with zipfile.ZipFile(out/'Faces-v12-source-and-research.zip') as z:assert z.testzip() is None
files=[p for p in out.glob('*') if p.is_file() and p.name!='SHA256SUMS' and (p.suffix in ['.json','.md','.zip'] or p.name=='geometry-texture-diagnostic.png')]
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(files)))
print('SOURCE_ARCHIVE_CRC_PASS', (out/'Faces-v12-source-and-research.zip').stat().st_size)
