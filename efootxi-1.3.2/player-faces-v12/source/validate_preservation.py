from pathlib import Path
import json,hashlib
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v10';a=Toc(str(old/'container/pc9298_mobile_and.utoc'));b=Toc(str(out/'container/pc9298_mobile_and.utoc'));rows=[]
assert {'character/'+n for n in a.files}.issubset(b.files) and len(b.files)==len(a.files)+2
for name,i in a.files.items():
 data=a.read(i);assert data==b.read(b.files['character/'+name]),name;rows.append({'name':name,'sha256':hashlib.sha256(data).hexdigest()})
r={'status':'ALL_264_V10_HEAD_CHUNKS_BYTE_IDENTICAL_PLUS_TWO_CARD_PORTRAITS_PASS','protected_files':rows,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'head_textures_unchanged':True,'phone_tested':False};(out/'preservation-validation.json').write_text(json.dumps(r,indent=2));print(r['status'],len(rows))

# Reuse asset/quality/texture/seam measurements ONLY after byte identity above.
sha=r['container_sha256']
for filename in ['asset-validation.json','quality-validation.json','texture-validation.json','seam-validation.json']:
 p=out/filename;v=json.loads(p.read_text());v['container_sha256']=sha;v['measurement_reused_from']='v10, all 264 head chunks verified byte-identical; two UI portraits added';p.write_text(json.dumps(v,indent=2))
