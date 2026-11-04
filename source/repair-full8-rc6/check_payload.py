"""Check every allowlisted packaged byte and reject private/build inputs."""
from pathlib import Path
import hashlib,json,sys,zipfile

def check(root):
 root=Path(root);d=json.loads((root/'payload-inventory.json').read_text());assert d['resource_revision']==19014 and d['phone_verified']is False
 names=['payload-inventory.json'];seen=set()
 for r in d['files']:
  n=r['path'];p=root/n;assert n not in seen and p.resolve().is_relative_to(root.resolve());seen.add(n)
  assert '__pycache__'not in p.parts and not p.name.endswith('.private.json')and p.suffix.lower()not in {'.db','.sqlite','.sqlite3','.log','.zip','.rar','.apk','.mp4'},n
  assert p.stat().st_size==r['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],n
  assert not n.startswith('.ci-'),n
  names.append(n)
 return names
if __name__=='__main__':
 names=check(sys.argv[1]);print('Verified all',len(names),'payload files')
 if len(sys.argv)>2:
  root=Path(sys.argv[1]);out=Path(sys.argv[2])
  with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True)as z:
   for n in names:z.write(root/n,n)
  with zipfile.ZipFile(out)as z:assert z.namelist()==names and z.testzip()is None
  print('FULL ZIP verified',out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
