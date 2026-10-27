from pathlib import Path
import struct,json,numpy as np
from PIL import Image
import texture2ddecoder
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');targets=json.loads((R/'targets.json').read_text());report={}
for kind in targets:
 N=P/('android-five-'+kind);data=(N/'noodle-color-atlas-2048.ktx').read_bytes();h=struct.unpack_from('<13I',data,12);assert h[4]==0x9278 and h[6:8]==(2048,2048)and h[11]==12;at=64+h[12];stats=[]
 for i in range(12):
  count=struct.unpack_from('<I',data,at)[0];at+=4;mip=data[at:at+count];at=(at+count+3)&~3;dim=max(4,2048>>i);assert len(mip)==dim*dim;a=np.frombuffer(texture2ddecoder.decode_etc2a8(mip,dim,dim),np.uint8).reshape(dim,dim,4);logical=max(1,2048>>i);valid=a[:logical,:logical];stats.append({'mip':i,'dimension':dim,'logical_dimension':logical,'alpha_min':int(valid[:,:,3].min()),'alpha_max':int(valid[:,:,3].max()),'rgb_mean':valid[:,:,:3].mean(axis=(0,1)).tolist()})
  if kind!='ronaldo':assert valid[:,:,3].min()==255,(kind,i)
 report[kind]={'mips':stats,'opaque_neck_at_all_mips':kind!='ronaldo','decode_success':True}
(R/'texture-mips-validation.json').write_text(json.dumps(report,indent=2));print('ALL_FIVE_TEXTURES_TWELVE_MIPS_DECODE_PASS')
