import hashlib
"""Compare separate ETC decoders, not a phone/material assignment test."""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;folder=R/'v8-full-export/Game/Assets/character/RealFace';rows=[]
for profile in ['ND01','ND06','ND13','ND27','NDJR','NDXS','NDDB']:
 names=['T_'+profile+'ep00v0313_Face_'+channel for channel in ['D','N','SRO']]
 if profile!='ND01':names+=['T_ND00'+profile[2:]+'_Hair_D']
 for name in names:
  independent=np.array(Image.open(folder/(name+'.png')).convert('RGBA'));ours=np.array(Image.open(out/(name+'-decoded.png')).convert('RGBA'));assert ours.shape==independent.shape
  error=np.abs(ours.astype(float)-independent);mean=float(error.mean());p95=float(np.percentile(error,95));assert mean<1.5 and p95<4,(name,mean,p95)
  rows.append({'name':name,'shape':ours.shape,'two_decoder_mae':mean,'p95':p95})
(out/'texture-validation.json').write_text(json.dumps({'status':'INDEPENDENT_TEXTURE_DECODERS_PASS','container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'textures':rows,'renderer_tested':False},indent=2));print('INDEPENDENT_TEXTURE_DECODERS_PASS',len(rows))
