"""Bounded CRI UTF/CPK reader; no execution of archive contents."""
import struct,zlib
from pathlib import Path

def utf(data):
 if data[:4]!=b'@UTF':
  key=0x655f;out=bytearray()
  for x in data:out.append(x^(key&255));key=(key*0x4115)&0xffffffff
  data=bytes(out)
 assert data[:4]==b'@UTF';size=struct.unpack_from('>I',data,4)[0];t=data[8:8+size];ro,so,do,no,nc,rl,nr=struct.unpack_from('>IIIIHHI',t);assert nr<100000 and nc<256
 def string(o):
  s=so+o;end=t.find(b'\0',s);assert 0<=s<=end<len(t);return t[s:end].decode('utf8','replace')
 def value(p,typ):
  fmts={0:'B',1:'b',2:'H',3:'h',4:'I',5:'i',6:'Q',7:'q',8:'f',9:'d',10:'I',11:'II'};fmt='>'+fmts[typ];v=struct.unpack_from(fmt,t,p);p+=struct.calcsize(fmt)
  return (string(v[0])if typ==10 else v if typ==11 else v[0]),p
 p=24;cols=[]
 for _ in range(nc):
  flag=t[p];p+=1
  if flag==0:flag=t[p+2];p+=3
  try:nm=string(struct.unpack_from('>I',t,p)[0])
  except AssertionError:
   assert nc==8 and rl==32;nm=['DirName','FileName','FileSize','ExtractSize','FileOffset','ID','UserString','CRC'][len(cols)]
  p+=4;v=None
  if flag&0xf0 in [0x20,0x30]:v,p=value(p,flag&15)
  cols.append((nm,flag,v))
 rows=[]
 for i in range(nr):
  p=ro+i*rl;row={}
  for nm,flag,v in cols:
   if flag&0xf0==0x50:v,p=value(p,flag&15)
   row[nm]=v
  rows.append(row)
 return rows

def decompress(b):
 if b[:8]!=b'CRILAYLA':return b
 size,offset=struct.unpack_from('<II',b,8);assert size<100000000;out=bytearray(size+256);out[:256]=b[16+offset:16+offset+256];at=16+offset-1;pool=0;bits=0
 def read(n):
  nonlocal at,pool,bits
  while bits<n:
   assert at>=16;pool=(pool<<8)|b[at];at-=1;bits+=8
  bits-=n;result=(pool>>bits)&((1<<n)-1);pool&=(1<<bits)-1;return result
 p=len(out)-1
 while p>=256:
  if not read(1):out[p]=read(8);p-=1;continue
  distance=read(13)+3;count=3
  for n in [2,3,5,8]:
   v=read(n);count+=v
   if v!=(1<<n)-1:break
  else:
   while True:
    v=read(8);count+=v
    if v!=255:break
  assert p-count+1>=256 and p+distance<len(out)
  for _ in range(count):out[p]=out[p+distance];p-=1
 return bytes(out)

def extract(path,dest):
 data=Path(path).read_bytes();assert data[:4]==b'CPK ';h=utf(data[16:2048])[0];off=h['TocOffset'];sz=struct.unpack_from('<Q',data,off+8)[0];rows=utf(data[off+16:off+16+sz]);base=min(h['ContentOffset'],off);dest=Path(dest).resolve();report=[]
 for row in rows:
  p=(dest/(row.get('DirName')or'')/row['FileName']).resolve();assert p.is_relative_to(dest);at=base+row['FileOffset'];raw=data[at:at+row['FileSize']];body=decompress(raw);assert len(body)==row['ExtractSize'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body);report.append({'file':str(p.relative_to(dest)),'bytes':len(body)})
 return report
