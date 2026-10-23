"""Restore the exact reviewed v14 container from its published full bundle."""
from pathlib import Path
import zipfile,hashlib
out=Path(__file__).resolve().parent.parent;baseline=out.parent/'player-faces-v14/Faces-v14-13-cards.zip'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='fa696be193d38803371ae5a6a1846c967270f59695567e125e41ea64f33e0d5e'
dest=out.parent/'player-faces-v14/container';dest.mkdir(exist_ok=True)
with zipfile.ZipFile(baseline) as z:
 for ext in ['pak','utoc','ucas']:
  name='pc9298_mobile_and.'+ext;data=z.read('livedata/'+name);p=dest/name
  if p.exists():assert p.read_bytes()==data
  else:p.write_bytes(data)
print('V14_BASELINE_SHA256_AND_CONTAINER_VERIFIED')
