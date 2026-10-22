from pathlib import Path
import zipfile,sys,hashlib,json
r=Path(__file__).resolve().parent;out=r.parent;input_zip=Path(sys.argv[1]);name='Ronaldo-v5-source-and-2006-input.zip'
files=[p for p in r.iterdir() if p.suffix in ['.py','.c','.sh','.patch','.txt']]
files += [p for p in out.iterdir() if p.suffix in ['.json','.md']]
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(out))
 z.write(input_zip,'inputs/CRISTIANO-RONALDO-2006.zip')
 z.write(out/'geometry-texture-diagnostic.png','geometry-texture-diagnostic.png')
with zipfile.ZipFile(out/name) as z:assert z.testzip() is None
print(name,(out/name).stat().st_size,hashlib.sha256((out/name).read_bytes()).hexdigest())
