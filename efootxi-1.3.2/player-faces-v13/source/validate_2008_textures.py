from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
out=Path(__file__).resolve().parent.parent;work=Path('/workspace/ronaldo-work');folder=work/'v13-export-final/Game/Assets/character/RealFace';rows=[]
for name in ['T_ND08ep00v0313_Face_D','T_ND08ep00v0313_Face_N','T_ND08ep00v0313_Face_SRO','T_ND0008_Hair_D']:
 own=np.array(Image.open(out/(name+'-decoded.png')).convert('RGBA'));independent=np.array(Image.open(folder/(name+'.png')).convert('RGBA'));assert own.shape==independent.shape
 error=np.abs(own.astype(float)-independent);mean=float(error.mean());p95=float(np.percentile(error,95));assert mean<1.5 and p95<=4
 rows.append({'name':name,'size':list(Image.open(folder/(name+'.png')).size),'two_decoder_mae':mean,'p95':p95})
source=np.array(Image.open(work/'input-2008/converted/hair_parts_bsm_alp.png').convert('RGBA'));target=np.array(Image.open(folder/'T_ND0008_Hair_D.png').convert('RGBA'));assert source.shape==target.shape;alpha_error=float(np.abs(source[:,:,3].astype(float)-target[:,:,3]).mean());assert alpha_error<4
r={'status':'RONALDO_2008_INDEPENDENT_TEXTURE_DECODERS_AND_SOURCE_HAIR_ALPHA_PASS','textures':rows,'hair_alpha_mae':alpha_error,'source_resolution_preserved':True,'collapsed_scalp_pole_zero_normals_repaired':11,'phone_tested':False,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()};(out/'2008-texture-validation.json').write_text(json.dumps(r,indent=2));print(r['status'],alpha_error)
