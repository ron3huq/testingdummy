import struct
from PIL import Image
import etcpak,texture2ddecoder

def replace_texture(raw,image,bulk=b'',preserve_alpha=False):
 b=bytearray(raw);rgb=b.rfind(b'PF_ETC2_RGB\0');rgba=b.rfind(b'PF_ETC2_RGBA\0');alpha=rgba>rgb;fmt=b'PF_ETC2_RGBA\0' if alpha else b'PF_ETC2_RGB\0';p=b.rfind(fmt);assert p>0
 at=p+len(fmt);first,count=struct.unpack_from('<II',b,at);assert first==0;at+=8;bulk=bytearray(bulk);dims=[];decoded=None
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',b,at);assert cooked==1 and n==size;at+=24;external=bool(flags&0x100);dw,dh,d=struct.unpack_from('<III',b,at if external else at+n);assert d==1
  im=image.convert('RGBA').resize((max(4,dw),max(4,dh)),Image.Resampling.LANCZOS);payload=(etcpak.compress_etc2_rgba if alpha else etcpak.compress_etc2_rgb)(im.tobytes(),im.width,im.height);assert len(payload)==n
  if preserve_alpha:
   assert alpha
   original=bytes(bulk[off:off+n])if external else bytes(b[at:at+n]);edited=bytearray(payload)
   for block in range(0,n,16):edited[block:block+8]=original[block:block+8]
   payload=bytes(edited)
  if external:assert off>=0 and off+n<=len(bulk);bulk[off:off+n]=payload
  else:b[at:at+n]=payload;at+=n
  at+=12;dims.append([dw,dh])
  if level==0:decoded=Image.frombytes('RGBA',im.size,(texture2ddecoder.decode_etc2a8 if alpha else texture2ddecoder.decode_etc2)(payload,im.width,im.height),'raw','BGRA')
 assert len(b)==len(raw);return bytes(b),bytes(bulk),dims,decoded

def decode_first_texture(raw,bulk=b''):
 """Read native ETC2 top mip for atlas composition without decoded-file caches."""
 rgb=raw.rfind(b'PF_ETC2_RGB\0');rgba=raw.rfind(b'PF_ETC2_RGBA\0');alpha=rgba>rgb;fmt=b'PF_ETC2_RGBA\0'if alpha else b'PF_ETC2_RGB\0';at=max(rgb,rgba)+len(fmt);first,count=struct.unpack_from('<II',raw,at);assert first==0 and count;at+=8;cooked,flags,n,size,off=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and n==size
 if flags&0x100:data=bulk[off:off+n];w,h,d=struct.unpack_from('<III',raw,at)
 else:data=raw[at:at+n];w,h,d=struct.unpack_from('<III',raw,at+n)
 assert len(data)==n and d==1
 return Image.frombytes('RGBA',(max(4,w),max(4,h)),(texture2ddecoder.decode_etc2a8 if alpha else texture2ddecoder.decode_etc2)(data,max(4,w),max(4,h)),'raw','BGRA')
