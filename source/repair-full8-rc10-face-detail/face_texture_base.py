"""Patch selected ETC2 blocks while preserving unrelated bytes and alpha."""
import struct,numpy as np,etcpak
from PIL import Image

def patch_blocks(raw,bulk,image,mask):
 b=bytearray(raw);bb=bytearray(bulk);p=max(b.rfind(b'PF_ETC2_RGB\0'),b.rfind(b'PF_ETC2_RGBA\0'));assert p>0;alpha=b[p:p+13]==b'PF_ETC2_RGBA\0';fmt=b'PF_ETC2_RGBA\0'if alpha else b'PF_ETC2_RGB\0';at=p+len(fmt);first,count=struct.unpack_from('<II',b,at);assert first==0;at+=8;changed=0;outside=0;checks=[]
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',b,at);at+=24;assert cooked==1 and n==size;external=bool(flags&0x100);dw,dh,d=struct.unpack_from('<III',b,at if external else at+n);assert d==1;w,h=max(dw,4),max(dh,4)
  im=image.resize((w,h),Image.Resampling.LANCZOS).convert('RGBA');ma=np.array(mask.resize((w,h),Image.Resampling.BOX))>0;ma=ma.reshape(h//4,4,w//4,4).any((1,3)).reshape(-1);encoded=(etcpak.compress_etc2_rgba if alpha else etcpak.compress_etc2_rgb)(im.tobytes(),w,h);assert len(encoded)==n
  old=bytes(bb[off:off+n])if external else bytes(b[at:at+n]);new=bytearray(old);step=16 if alpha else 8
  for k,yes in enumerate(ma):
   if yes:new[k*step+(8 if alpha else 0):(k+1)*step]=encoded[k*step+(8 if alpha else 0):(k+1)*step];changed+=1
   else:outside+=1
  if alpha:
   for k in range(0,n,16):assert new[k:k+8]==old[k:k+8]
  if external:bb[off:off+n]=new
  else:b[at:at+n]=new;at+=n
  checks.append([dw,dh]);at+=12
 assert len(b)==len(raw)and len(bb)==len(bulk)
 return bytes(b),bytes(bb),{'changed_blocks':changed,'untouched_blocks_exact':outside,'all_alpha_blocks_exact':True,'mips':checks}
