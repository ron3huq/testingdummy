"""Recover the exact v10 baseline for the runtime-only v11 update."""
from pathlib import Path
import sys,hashlib,zipfile
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v10';archive=Path(sys.argv[1]) if len(sys.argv)>1 else old/'Faces-v10-12-cards.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='8f0e38a49cf14f66d6123224f03be1225158709d2a704612033d2f8753a34286'
for root in [out,old]:
 (root/'container').mkdir(parents=True,exist_ok=True);(root/'asset').mkdir(exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for ext in ['pak','utoc','ucas']:
   name='pc9298_mobile_and.'+ext;(root/'container'/name).write_bytes(z.read('livedata/'+name))
t=Toc(str(old/'container/pc9298_mobile_and.utoc'))
for name,i in t.files.items():
 data=t.read(i)
 for root in [out,old]:(root/'asset'/Path(name).name).write_bytes(data)
print('Published v10 baseline recovered without rebuilding any asset')
