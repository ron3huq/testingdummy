from pathlib import Path
import json,hashlib
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v10';a=Toc(str(old/'container/pc9298_mobile_and.utoc'));b=Toc(str(out/'container/pc9298_mobile_and.utoc'));rows=[]
assert set(a.files)==set(b.files)
for name,i in a.files.items():
 data=a.read(i);assert data==b.read(b.files[name]),name;rows.append({'name':name,'sha256':hashlib.sha256(data).hexdigest()})
for ext in ['pak','utoc','ucas']:assert (old/'container'/('pc9298_mobile_and.'+ext)).read_bytes()==(out/'container'/('pc9298_mobile_and.'+ext)).read_bytes()
r={'status':'ALL_V10_ASSETS_AND_COMPLETE_CONTAINER_BYTE_IDENTICAL_PASS','protected_files':rows,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'head_textures_unchanged':True,'phone_tested':False};(out/'preservation-validation.json').write_text(json.dumps(r,indent=2));print(r['status'],len(rows))
