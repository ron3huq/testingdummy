"""Decode mip0 directly from cooked assets with texture2ddecoder (not UEViewer)."""
from pathlib import Path
import struct,texture2ddecoder
from PIL import Image
out=Path(__file__).resolve().parent.parent
for p in (out/'asset').glob('T_*.uasset'):
 raw=p.read_bytes();rgba=b'PF_ETC2_RGBA\0' in raw;fmt=b'PF_ETC2_RGBA\0' if rgba else b'PF_ETC2_RGB\0';at=raw.rfind(fmt)
 if at<0:continue
 w,h,z=struct.unpack_from('<III',raw,at-16);first,count=struct.unpack_from('<II',raw,at+len(fmt));assert first==0
 at+=len(fmt)+8;cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);assert cooked==1 and n==size
 payload=p.with_suffix('.ubulk').read_bytes()[offset:offset+n] if flags==66817 else raw[at+24:at+24+n];assert len(payload)==n
 decoded=(texture2ddecoder.decode_etc2a8 if rgba else texture2ddecoder.decode_etc2)(payload,w,h);Image.frombytes('RGBA',(w,h),decoded,'raw','BGRA').save(out/(p.stem+'-decoded.png'))
print('Decoded all first mips independently')
