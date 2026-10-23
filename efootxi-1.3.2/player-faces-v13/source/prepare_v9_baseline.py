"""Recover byte-identical v9 assets from the published ZIP; does not rebuild them."""
from pathlib import Path
import zipfile,hashlib,json,sys,shutil
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v9';old.mkdir(exist_ok=True);archive=Path(sys.argv[1]) if len(sys.argv)>1 else old/'Faces-v9-11-cards.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='af9915e6d22316351abd3ba2a05f92666fabdb19b86406f43cd407b4d786b47f'
(old/'container').mkdir(exist_ok=True);(old/'asset').mkdir(exist_ok=True);(out/'asset').mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for ext in ['pak','utoc','ucas']:
  name='pc9298_mobile_and.'+ext;(old/'container'/name).write_bytes(z.read('livedata/'+name))
(old/'build-report.json').write_bytes((out/'references/v9/build-report.json').read_bytes())
t=Toc(str(old/'container/pc9298_mobile_and.utoc'))
for name,i in t.files.items():
 data=t.read(i);(old/'asset'/Path(name).name).write_bytes(data);(out/'asset'/Path(name).name).write_bytes(data)
print('Byte-identical published v9 baseline extracted')
