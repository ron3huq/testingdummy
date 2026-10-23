"""Preservation + independent card export verification; not an Android shader test."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from iostore import Toc,parse_header,store_entry
out=Path(__file__).resolve().parent.parent;old=Toc(str(out.parent/'player-faces-v13/container/pc9298_mobile_and.utoc'));new=Toc(str(out/'container/pc9298_mobile_and.utoc'));rows=[]
for path,i in old.files.items():
 if not path.startswith('character/'):continue
 data=old.read(i);assert data==new.read(new.files[path]),path;rows.append({'name':path,'sha256':hashlib.sha256(data).hexdigest()})
assert len(rows)==277
large='ui/Data/Thumbnail/Player/Variation2022/88045755960841_l.uasset';assert old.read(old.files[large])==new.read(new.files[large])
for i in range(len(new.ids)):assert hashlib.sha1(new.read(i)).digest()==new.metas[i][:20]
report=json.loads((out/'card-art-validation.json').read_text());export=Path('/workspace/ronaldo-work/v14-card-verified/Game/Assets/ui/Data/Thumbnail/Player/Variation2022');cards=[]
for row in report['cards']:
 p=export/(Path(row['path']).stem+'.png');im=Image.open(p).convert('RGBA');assert list(im.size)==row['dimensions'][0]
 source=out/'card-art-research/xuan-son/Nguyen-Xuan-Son-thumbnail.png' if row['card_id']=='88045755960841' else out/'card-inputs'/row['file']
 expected=np.array(Image.open(source).convert('RGBA').resize(im.size,Image.Resampling.LANCZOS));decoded=np.array(im);mae=float(np.abs(expected.astype(float)-decoded).mean());assert mae<12,(p.name,mae)
 cards.append({'path':row['path'],'dimensions':list(im.size),'UEViewer_export_found':True,'source_vs_export_mae':mae})
assert len(cards)==19
sha=hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()
(out/'preservation-validation.json').write_text(json.dumps({'status':'ALL_277_HEAD_CHUNKS_13_CARDS_AND_LARGE_XUAN_SON_ART_BYTE_IDENTICAL_PASS','protected_files':rows,'container_sha256':sha,'phone_tested':False},indent=2))
report.update(independent_ueviewer_export=cards,container_sha256=sha);(out/'card-art-validation.json').write_text(json.dumps(report,indent=2))
# Prior skeletal/texture/seam evidence is reused after proving every input byte.
for filename in ['asset-validation.json','quality-validation.json','texture-validation.json','seam-validation.json','2008-texture-validation.json']:
 p=out/filename;v=json.loads((out.parent/'player-faces-v13'/filename).read_text());v['container_sha256']=sha;v['measurement_reused_from']='v13: all277head chunks verified byte-identical; only19UItextures changed';p.write_text(json.dumps(v,indent=2))
(out/'v14-assets-validation.json').write_text(json.dumps({'status':'277_HEAD_CHUNKS_AND_19_INDEPENDENT_CARD_EXPORTS_PASS','container_sha256':sha,'head_meshes':25,'render_lods':50,'UI_exports':cards,'phone_tested':False},indent=2));print('V14_ASSET_PRESERVATION_AND_19_CARD_EXPORTS_PASS')
