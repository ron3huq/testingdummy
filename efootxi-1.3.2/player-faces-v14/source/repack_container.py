from pathlib import Path
import sys,struct,hashlib,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from iostore import Toc,parse_header,store_entry,build_store,dir_index
out=Path(__file__).resolve().parent.parent/'container';a=out.parent/'asset';t=Toc(str(out/'pc9298_mobile_and.utoc'));header=parse_header(t.read(next(i for i,c in enumerate(t.ids) if c[11]==10)));entries=[store_entry(header['store'],i) for i in range(len(header['pids']))];pids=header['pids'];chunks=[];paths={}
for path,i in sorted(t.files.items(),key=lambda x:x[1]):
 data=(a/Path(path).name).read_bytes();paths[path]=len(chunks);chunks.append((t.ids[i],data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];st=build_store(entries);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
block=65536;ids=[];ols=[];blocks=[];voff=0
import zlib
with (out/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for at in range(0,len(body),block):
   raw=body[at:at+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
di=dir_index(t.mount,paths);h=bytearray(t.raw[:t.hs]);struct.pack_into('<9I',h,20,t.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
blob=bytes(h)+b''.join(ids)+b''.join(x.to_bytes(5,'big')+y.to_bytes(5,'big') for x,y in ols)+b''.join(x.to_bytes(5,'little')+y.to_bytes(3,'little')+z.to_bytes(3,'little')+bytes([m]) for x,y,z,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(out/(name+'.utoc')).write_bytes(blob)
print('repacked',len(chunks))
