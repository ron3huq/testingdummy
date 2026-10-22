from pathlib import Path
import sys,json
import numpy as np,texture2ddecoder
from PIL import Image
r=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;checks=[]
for suffix in ['', 'lg00v0000','ep01v0291','ep00v0313']:
 name='T_ND01'+suffix+'_Face_D';bulk=(r/'v4a-extracted'/(name+'.ubulk')).read_bytes()[:524288]
 old=np.frombuffer(texture2ddecoder.decode_etc2(bulk,1024,1024),'u1').reshape(1024,1024,4)[:,:,[2,1,0,3]]
 new=np.array(Image.open(out/(name+'-decoded.png')).convert('RGBA'));assert np.array_equal(old,new[:1024,:1024]);checks.append(name)
base='Game/Assets/character/RealFace/T_ND01ep00v0313_Face_D.png'
# An independent decoder must also give exactly the SAME old/new face pixels.
# Different ETC libraries round colors differently; do not confuse that with payload corruption.
old=np.array(Image.open(r/'v4a-texture-export'/base).convert('RGBA'));new=np.array(Image.open(r/'v6-export'/base).convert('RGBA'))
assert old.shape==(1024,1024,4) and new.shape==(2048,2048,4) and np.array_equal(old,new[:1024,:1024])
result={'status':'V4A_FACE_DIFFUSE_TEXELS_EXACT_IN_TWO_DECODERS_PASS','v4a_mip0_exact_atlas_regions':checks,'independent_UEViewer_old_vs_new_exact':True,'phone_material_assignment_verified':False}
(out/'texture-validation.json').write_text(json.dumps(result,indent=2));print(result['status'])
