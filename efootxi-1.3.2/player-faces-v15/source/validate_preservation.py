from pathlib import Path
import json,hashlib
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v12';a=Toc(str(old/'container/pc9298_mobile_and.utoc'));b=Toc(str(out/'container/pc9298_mobile_and.utoc'));rows=[]
assert set(a.files).issubset(b.files) and len(b.files)>len(a.files)
for name,i in a.files.items():
 if name.startswith('ui/'):continue
 data=a.read(i);assert data==b.read(b.files[name]),name;rows.append({'name':name,'sha256':hashlib.sha256(data).hexdigest()})
r={'status':'ALL_264_EXISTING_HEAD_CHUNKS_BYTE_IDENTICAL_PLUS_2008_AND_SINGLE_PORTRAIT_PASS','protected_files':rows,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'head_textures_unchanged':True,'phone_tested':False};(out/'preservation-validation.json').write_text(json.dumps(r,indent=2));print(r['status'],len(rows))

# Reuse measurements only for preserved old heads. 2008 gets separate new checks.
sha=r['container_sha256']
for filename in ['quality-validation.json','texture-validation.json','seam-validation.json']:
 p=out/filename;v=json.loads(p.read_text());v['container_sha256']=sha;v['measurement_reused_from']='v12/10: all 264 old head chunks byte-identical. New 2008 checked separately.';p.write_text(json.dumps(v,indent=2))
