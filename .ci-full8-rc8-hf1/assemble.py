from pathlib import Path
import sys,json,hashlib,subprocess,shutil
root=Path.cwd();src=root/'source/repair-full8-rc8-hf1';spec=json.loads((root/'.ci-full8-rc8-hf1/expected.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root/'payload-inventory.json')=='6c2963941fc9a279c418dbcd1c2d9b4ebe018e5289f79e7166bef718b504355e'
for p in(src/'overlays').rglob('*'):
 if p.is_file():q=root/p.relative_to(src/'overlays');q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
subprocess.run([sys.executable,str(src/'finalize.py'),str(root)],check=True)
subprocess.run([sys.executable,str(src/'check_payload.py'),str(root)],check=True)
assert sha(root/'payload-inventory.json')==spec['inventory_sha256']
print('RC8 HF1 FULL source reconstruction matches complete local inventory; on-phone verification pending.')
