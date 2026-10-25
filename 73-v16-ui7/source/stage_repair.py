from pathlib import Path
import zipfile,json
P=Path('/workspace/ronaldo-work/73-ui7');a=P/'repair-assets';a.mkdir(exist_ok=True)
for zf in Path('/workspace/testingdummy/73-v16-ui7').glob('*.zip'):
 with zipfile.ZipFile(zf)as z:
  for n in z.namelist():
   if n.startswith('assets/gateway-release/'):
    p=a/n.removeprefix('assets/');p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(z.read(n))
