from pathlib import Path
import struct,json,hashlib
r=Path(__file__).parent;p=next((r/'extracted').rglob('face.fpk'));raw=p.read_bytes()
if raw[:8]==b'CRILAYLA':
 n,c=struct.unpack_from('<II',raw,8);assert n<64*1024*1024 and c+16+256<=len(raw);out=bytearray(n+256);out[:256]=raw[16+c:16+c+256];pos=16+c-1;buf=0;have=0
 def bits(k):
  global pos,buf,have
  v=0
  while k:
   if not have:buf=raw[pos];pos-=1;have=8
   take=min(k,have);v=(v<<take)|((buf>>(have-take))&((1<<take)-1));have-=take;k-=take
  return v
 at=len(out)-1
 while at>=256:
  if bits(1)==0:out[at]=bits(8);at-=1
  else:
   back=bits(13)+3;count=3
   for k in [2,3,5,8]:
    v=bits(k);count+=v
    if v!=(1<<k)-1:break
   else:
    while True:
     v=bits(8);count+=v
     if v!=255:break
   assert at-count+1>=256 and at+back<len(out)
   for _ in range(count):out[at]=out[at+back];at-=1
 data=bytes(out)
else:data=raw
assert data[:7]==b'foxfpk\0';(r/'face-uncompressed.fpk').write_bytes(data);out=r/'models';out.mkdir(exist_ok=True);rows=[]
for i in range(struct.unpack_from('<I',data,36)[0]):
 offset,size,noff,nlen=struct.unpack_from('<4Q',data,48+48*i);assert offset+size<=len(data) and noff+nlen<=len(data);name=data[noff:noff+nlen].decode();p=out/name;assert p.resolve().is_relative_to(out.resolve());p.parent.mkdir(parents=True,exist_ok=True);body=data[offset:offset+size];p.write_bytes(body);old=r.parent/'source-extracted'/name;rows.append({'name':name,'size':size,'sha256':hashlib.sha256(body).hexdigest(),'identical_to_previous_source':old.exists() and old.read_bytes()==body})
(r/'fpk-comparison.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
