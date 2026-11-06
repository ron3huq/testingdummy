"""Reconstruct the complete payload from pinned RC7 plus the verified delta.
No API token, APK, engine, save, or source rebuild is needed on the Actions runner.
"""
from pathlib import Path
import hashlib,json,sys,zipfile

def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def extract(archive,root):
 root=root.resolve()
 with zipfile.ZipFile(archive)as z:
  assert len(z.namelist())==len(set(z.namelist()))
  for info in z.infolist():
   dest=(root/info.filename).resolve();assert dest.is_relative_to(root)
  assert z.testzip()is None
  z.extractall(root)
def main():
 info=json.loads(Path('_ci/reconstruction.json').read_text());base=Path('RC7-baseline.zip');delta=Path('_ci/RC22-RECONSTRUCTION-DELTA.zip');root=Path('payload')
 assert sha(base)==info['baseline_sha256'],'RC7 baseline checksum mismatch'
 assert sha(delta)==info['delta_sha256'],'RC22 update checksum mismatch'
 root.mkdir(exist_ok=False);extract(base,root);extract(delta,root)
 assert sha(root/'payload-inventory.json')==info['inventory_sha256']
 inv=json.loads((root/'payload-inventory.json').read_text());expected={r['path']for r in inv['files']}|{'payload-inventory.json'};actual={p.relative_to(root).as_posix()for p in root.rglob('*')if p.is_file()}
 assert actual==expected,dict(extra=sorted(actual-expected),missing=sorted(expected-actual))
 for row in inv['files']:
  p=root/row['path'];assert p.stat().st_size==row['bytes']and sha(p)==row['sha256'],row['path']
 assert not list((root/'assets/gateway-release/work/tools').glob('ucl_lp_*'))
 assert not(root/'assets/gateway-release/work/tools/libucl_rules.so').exists()
 assert not any(p.suffix.lower()in{'.apk','.db','.sqlite','.sqlite3'}for p in root.rglob('*')if p.is_file())
 for name in ['face-readback','mouth-readback','event-full-cycle','face-profile','dex','startup']:
  assert json.loads((root/'validation'/('full8-rc22-'+name+'.json')).read_text())['passed'],name
 print(json.dumps(dict(passed=True,payload_files_verified=len(expected),inventory_sha256=info['inventory_sha256'],version=inv['version'],phone_verified=False),indent=2))
if __name__=='__main__':main()
