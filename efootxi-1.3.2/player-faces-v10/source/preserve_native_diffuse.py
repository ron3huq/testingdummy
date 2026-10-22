from pathlib import Path
import struct
out=Path(__file__).resolve().parent.parent;old=out.parent/'player-faces-v9/asset'
def levels(raw):
 fmt=b'PF_ETC2_RGB\0';at=raw.rfind(fmt)+len(fmt);first,count=struct.unpack_from('<II',raw,at);at+=8;assert first==0
 for _ in range(count):
  cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;inline=at
  if flags==72:at+=n
  w,h,z=struct.unpack_from('<III',raw,at);at+=12;yield flags,n,offset if flags==66817 else inline,w,h
for code in ['NDXS','NDPQ','NDSP']:
 name='T_'+code+'ep00v0313_Face_D';src='T_'+('NDXS' if code=='NDSP' else code)+'ep00v0313_Face_D';p=out/'asset'/(name+'.uasset');raw=bytearray(p.read_bytes());bulk=bytearray(p.with_suffix('.ubulk').read_bytes());sr=(old/(src+'.uasset')).read_bytes();sb=(old/(src+'.ubulk')).read_bytes()
 for (flag,n,off,w,h),(sf,sn,soff,sw,sh) in zip(levels(raw),levels(sr)):
  assert (flag,n,w,h)==(sf,sn,sw,sh)
  if h<8:continue
  mid=(h//8)*(w//4)*8;a=bulk if flag==66817 else raw;b=sb if sf==66817 else sr;a[off+mid:off+n]=b[soff+mid:soff+n]
 p.write_bytes(raw);p.with_suffix('.ubulk').write_bytes(bulk)
print('Native eye/mouth lower-half ETC blocks preserved for all mips >=8')
