from pathlib import Path
import zipfile,hashlib
out=Path(__file__).resolve().parent.parent;baseline=out.parent/'player-faces-v15/Faces-v15-13-cards.zip'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='263f4f9cc85d561f21c07c040fdaa757993755ba29c7cac28727815fb5575243'
dest=out.parent/'player-faces-v15/container';dest.mkdir(exist_ok=True)
with zipfile.ZipFile(baseline) as z:
 for ext in ['pak','utoc','ucas']:
  name='pc9298_mobile_and.'+ext;data=z.read('livedata/'+name);p=dest/name
  if p.exists():assert p.read_bytes()==data
  else:p.write_bytes(data)
print('V15_BASELINE_SHA256_PASS')
