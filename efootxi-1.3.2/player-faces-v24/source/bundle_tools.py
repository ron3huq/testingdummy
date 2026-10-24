"""Lossless IoStore merge and native Texture2D payload replacement utilities."""
from pathlib import Path
import struct,hashlib,zlib,shutil
from PIL import Image
import etcpak,texture2ddecoder
from iostore import Toc,parse_header,store_entry,build_store,dir_index
class Bundle:
 def __init__(self,t):
  self.base=t;self.files={p:(t.ids[i],t.read(i)) for p,i in t.files.items()};h=parse_header(t.read(next(i for i,x in enumerate(t.ids) if x[11]==10)));self.entries={p:store_entry(h['store'],i) for i,p in enumerate(h['pids'])}
 def put(self,path,idb,data,entry=None):
  self.files[path]=(idb,bytes(data))
  if entry is not None:self.entries[int.from_bytes(idb[:8],'little')]=entry
 def native(self,t,path,data):
  i=t.files[path];h=parse_header(t.read(next(i for i,x in enumerate(t.ids) if x[11]==10)));pk=int.from_bytes(t.ids[i][:8],'little');dest=t.mount+path;dest=dest.split('/Content/Assets/',1)[1];self.put(dest,t.ids[i],data,store_entry(h['store'],h['pids'].index(pk)))
 def write(self,out):
  out=Path(out);out.mkdir(parents=True,exist_ok=True);name='pc9298_mobile_and';cid=int.from_bytes(hashlib.sha256(name.encode()).digest()[:8],'little');chunks=[];paths={};pids=[]
  for p,(idb,b) in self.files.items():
   paths[p]=len(chunks);chunks.append((idb,b,hashlib.sha1(b).digest()+b'\0'*12+b'\1'))
   if p.endswith('.uasset'):pids.append(int.from_bytes(idb[:8],'little'))
  assert len(set(pids))==len(pids);st=build_store([self.entries[p] for p in pids]);hb=struct.pack('<QIiiiQ',cid,len(pids),0,8,0,0) if False else struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)
  hb+=struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13));ids=[];ols=[];blocks=[];voff=0;block=65536
  with (out/(name+'.ucas')).open('wb') as f:
   for idb,body,meta in chunks:
    ids.append(idb);ols.append((voff,len(body)))
    for a in range(0,len(body),block):
     raw=body[a:a+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));p=comp if method else raw;blocks.append((f.tell(),len(p),len(raw),method));f.write(p)
    voff+=(len(body)+block-1)//block*block
  di=dir_index('../../../PesMobile/Content/Assets/',paths);h=bytearray(self.base.raw[:self.base.hs]);struct.pack_into('<9I',h,20,self.base.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
  data=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(x[2] for x in chunks);(out/(name+'.utoc')).write_bytes(data);shutil.copyfile(self.base.path[:-5]+'.pak',out/(name+'.pak'))
  t=Toc(str(out/(name+'.utoc')))
  for p,(_,b) in self.files.items():assert t.read(t.files[p])==b
  return t

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
