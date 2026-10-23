from pathlib import Path
import zipfile,hashlib
root=Path(__file__).resolve().parent.parent
p=root.parent/'player-faces-v18/Faces-v18-13-cards.zip'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='2cc4930aa0659616fdb7138c5d12cff81bddfd6779344e26c0a798baf66abe2d'
out=p.parent/'container';out.mkdir(exist_ok=True)
with zipfile.ZipFile(p) as z:
 for ext in ['pak','utoc','ucas']:
  name='pc9298_mobile_and.'+ext;(out/name).write_bytes(z.read('livedata/'+name))
print('PINNED_V18_CONTAINER_RESTORED')
