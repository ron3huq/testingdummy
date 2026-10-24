from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
from iostore import Toc
from bundle_tools import decode_first_texture
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');t=Toc(str(O/'container/pc9298_mobile_and.utoc'));rows=[]
for code,source in [('NX01',R/'v24-input/rp/converted/face_normal.png'),('NX27',R/'v24-input/2027/converted/face_normal.png'),('NXJR',R/'v24-input/prince/converted/face_normal.png'),('NXNC',R/'v24-input/fifa/converted/face_nrm.png')]:
 a=np.array(Image.open(source).convert('RGBA').resize((1024,1024)),dtype=float)/255;x=a[:,:,3]*2-1;y=a[:,:,1]*2-1;length=np.maximum(1,np.sqrt(x*x+y*y));x/=length;y/=length;z=np.sqrt(np.maximum(0,1-x*x-y*y));expected=np.stack([x,y,z],axis=-1)
 p='character/RealFace/T_'+code+'ep00v0313_Face_N';decoded=np.array(decode_first_texture(t.read(t.files[p+'.uasset']),t.read(t.files[p+'.ubulk']))).astype(float)[:1024,:1024,:3]/127.5-1;mae=float(abs(decoded-expected).mean());assert mae<.04 and float(z.mean())>.90
 rows.append({'profile':code,'decoded_normal_mean_absolute_error':mae,'normal_source_X_channel':'A','normal_source_Y_channel':'G','source_R_std':float(a[:,:,0].std()),'source_A_std':float(a[:,:,3].std()),'mean_reconstructed_Z':float(z.mean())})
assert rows[3]['source_R_std']==0 and rows[3]['source_A_std']>.02
(O/'normal-validation.json').write_text(json.dumps({'status':'V24_DXT5NM_ALPHA_GREEN_NATIVE_READBACK_PASS','profiles':rows,'v23_FIFA_R_equals_255_was_proven_incorrect_X_source':True,'does_not_prove_sole_cause_of_black_faces':True,'phone_tested':False},indent=2));print('V24_DXT5NM_ALPHA_GREEN_NATIVE_READBACK_PASS')
