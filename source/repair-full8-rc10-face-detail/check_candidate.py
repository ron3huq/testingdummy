from pathlib import Path
import json,hashlib,zipfile,sys
r=Path(sys.argv[1]);doc=json.loads((r/'payload-inventory.json').read_text());assert doc['resource_revision']==19019 and doc['ucl_integrated']is False;names=['payload-inventory.json'];seen=set()
for row in doc['files']:
 n=row['path'];p=r/n;assert n not in seen and p.resolve().is_relative_to(r.resolve())and '__pycache__'not in p.parts;seen.add(n);assert p.stat().st_size==row['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],n;names.append(n)
assert hashlib.sha256((r/'classes5.dex').read_bytes()).hexdigest()=='687f574b70c37888c274bd8d9b1cf193dc3eff33d4556eb8db34d8b124a53c51'
assert hashlib.sha256((r/'assets/gateway-release/work/tools/libsingle_player_live.so').read_bytes()).hexdigest()=='92cf68fe309a515f8be4ab6a1fc829eb164565d062f5f920b9d4d7dc57465b19'
print('Verified',len(names),'files; RC7 DEX and control binary exact; UCL NOT integrated.',flush=True)
if len(sys.argv)>2:
 with zipfile.ZipFile(sys.argv[2],'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for n in names:z.write(r/n,n)
 with zipfile.ZipFile(sys.argv[2])as z:assert z.namelist()==names and z.testzip()is None
 print('Archive verified',Path(sys.argv[2]).stat().st_size,hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest(),flush=True)
