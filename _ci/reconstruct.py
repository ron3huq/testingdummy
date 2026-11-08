"""Pinned RC7 -> RC23 -> RC25. Verify the exact full payload before upload."""
from pathlib import Path
import hashlib,json,zipfile

def sha(p):
 with Path(p).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def extract(archive,root):
 root=root.resolve()
 with zipfile.ZipFile(archive)as z:
  assert len(z.namelist())==len(set(z.namelist()))
  for info in z.infolist():assert (root/info.filename).resolve().is_relative_to(root)
  assert z.testzip()is None;z.extractall(root)
def check(root,expected_sha):
 assert sha(root/'payload-inventory.json')==expected_sha
 inv=json.loads((root/'payload-inventory.json').read_text());expected={r['path']for r in inv['files']}|{'payload-inventory.json'};actual={p.relative_to(root).as_posix()for p in root.rglob('*')if p.is_file()};assert actual==expected,dict(extra=sorted(actual-expected),missing=sorted(expected-actual))
 for row in inv['files']:
  p=root/row['path'];assert p.stat().st_size==row['bytes']and sha(p)==row['sha256'],row['path']
 return inv

def main():
 info=json.loads(Path('_ci/reconstruction.json').read_text());root=Path('payload');base=Path('RC7-baseline.zip');prior=Path('RC23-delta.zip');update24=Path('RC24-delta.zip');delta=Path('_ci/RC25-RECONSTRUCTION-DELTA.zip')
 assert sha(update24)==info['rc24_delta_sha256'];assert sha(base)==info['baseline_sha256'];assert sha(prior)==info['rc23_delta_sha256'];assert sha(delta)==info['delta_sha256'];root.mkdir(exist_ok=False);extract(base,root);extract(prior,root);check(root,info['rc23_inventory_sha256']);extract(update24,root);check(root,info['rc24_inventory_sha256']);extract(delta,root);inv=check(root,info['inventory_sha256'])
 tools=root/'assets/gateway-release/work/tools';assert not list(tools.glob('ucl_lp_*'));assert not(tools/'libucl_rules.so').exists()
 assert not any(p.suffix.lower()in{'.apk','.db','.sqlite','.sqlite3'}for p in root.rglob('*')if p.is_file())
 for name in ['startup','event-cycle','native-opponent-stats','transfer','dex','native','face-gate','probability','settings','launcher']:
  assert json.loads((root/'validation'/('full8-rc25-'+name+'.json')).read_text())['passed'],name
 faces=json.loads((tools/'noodle_bundle.json').read_text())['new_three_faces'];assert all(faces[k]==v for k,v in {'89138556572074':'R9D2','106783356083208':'R7A2','88043608522885':'R0A2'}.items())
 print(json.dumps(dict(passed=True,payload_files_verified=len(inv['files'])+1,inventory_sha256=info['inventory_sha256'],version=inv['version'],phone_verified=False),indent=2))
if __name__=='__main__':main()
