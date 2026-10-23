from pathlib import Path
import sys,zipfile,hashlib
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v13';arc=Path(sys.argv[1]) if len(sys.argv)>1 else old/'Faces-v13-13-cards.zip'
assert hashlib.sha256(arc.read_bytes()).hexdigest()=='7c57ca4ee8814cca8d59ca677efd81e5f42f73db278d09dc6e8e723a9194b748'
(old/'container').mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(arc) as z:
 assert z.testzip() is None
 for ext in ['pak','utoc','ucas']:
  n='pc9298_mobile_and.'+ext;(old/'container'/n).write_bytes(z.read('livedata/'+n))
print('Exact published v13 container recovered without rebuilding heads')
