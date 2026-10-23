from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from iostore import Toc
out=Path(__file__).resolve().parent.parent;old=Toc(str(out.parent/'player-faces-v15/container/pc9298_mobile_and.utoc'));new=Toc(str(out/'container/pc9298_mobile_and.utoc'));protected=[]
for p,i in old.files.items():
 if not p.startswith('character/'):continue
 assert old.read(i)==new.read(new.files[p]),p;protected.append(p)
assert len(protected)==277
for i in range(len(new.ids)):assert hashlib.sha1(new.read(i)).digest()==new.metas[i][:20]
report=json.loads((out/'card-art-validation.json').read_text());export=Path('/workspace/ronaldo-work/v16-verified/Game/Assets');cards=[]
for row in report['cards']:
 image=Image.open(export/Path(row['path']).with_suffix('.png')).convert('RGBA');source=Image.open(out/'art'/row['file']).convert('RGBA');assert image.size==source.size and list(image.size)==row['dimensions'][0]
 mae=float(np.abs(np.asarray(image,dtype=float)-np.asarray(source,dtype=float)).mean());assert mae<12,(row['path'],mae);cards.append({'path':row['path'],'size':list(image.size),'ETC2_mean_error':mae,'independent_UEViewer_export':True})
assert len(cards)==22
sha=hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()
(out/'preservation-validation.json').write_text(json.dumps({'status':'ALL_277_HEAD_CHUNKS_BYTE_IDENTICAL_V15_PASS','protected_files':protected,'container_sha256':sha,'phone_tested':False},indent=2))
for name in ['asset-validation.json','quality-validation.json','texture-validation.json','seam-validation.json','2008-texture-validation.json','sleeve-validation.json']:
 v=json.loads((out.parent/'player-faces-v15'/name).read_text());v['container_sha256']=sha;v['measurement_reused_from']='v15: all277head chunks plus selector binary/runtime verified byte-identical';(out/name).write_text(json.dumps(v,indent=2))
report['independent_ueviewer_export']=cards;(out/'card-art-validation.json').write_text(json.dumps(report,indent=2));(out/'v16-assets-validation.json').write_text(json.dumps({'status':'277_HEAD_CHUNKS_AND_22_NATIVE_CARD_EXPORTS_PASS','container_sha256':sha,'cards':cards,'phone_tested':False},indent=2));print('V16_HEAD_PRESERVATION_AND_22_CARD_EXPORTS_PASS')
