"""Repack the shipped dt870 losslessly, adding exact Y08 kit recipes."""
from pathlib import Path
import sys,struct,zlib,json,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v24/source');from cpk_extract import utf,decompress,extract
P=Path('/workspace/ronaldo-work/73-ui6');old=(P/'original-dt870.cpk').read_bytes();header=utf(old[16:2048])[0]
oldtoc=header['TocOffset'];oldtocsize=struct.unpack_from('<Q',old,oldtoc+8)[0];oldrows=utf(old[oldtoc+16:oldtoc+16+oldtocsize]);oldids={(r.get('DirName','')+'/'+r['FileName']).lstrip('/'):r['ID']for r in oldrows};nextid=max(oldids.values())+1
def plain(b):
 if b[:4]==b'@UTF':return b
 key=0x655f;out=bytearray()
 for x in b:out.append(x^(key&255));key=(key*0x4115)&0xffffffff
 return bytes(out)
def schema(raw):
 raw=plain(raw);data=raw[8:];ro,so,do,no,nc,rl,nr=struct.unpack_from('>IIIIHHI',data);p=24;cols=[]
 for i in range(nc):
  f=data[p];p+=1
  if not f:f=data[p+2];p+=3
  ni=struct.unpack_from('>I',data,p)[0];p+=4;name=data[so+ni:data.find(b'\0',so+ni)].decode();typ=f&15;cols.append((name,typ))
  if f&0xf0 in[0x20,0x30]:p+={0:1,1:1,2:2,3:2,4:4,5:4,6:8,7:8,8:4,9:8,10:4,11:8}[typ]
 return cols
formats={0:'B',1:'b',2:'H',3:'h',4:'I',5:'i',6:'Q',7:'q',8:'f',9:'d',10:'I',11:'II'}
def make_utf(title,columns,rows):
 strings=bytearray();indexes={}
 def string(s):
  if s is None:s=''
  if s not in indexes:indexes[s]=len(strings);strings.extend(s.encode()+b'\0')
  return indexes[s]
 no=string(title);coldata=bytearray()
 for name,typ in columns:coldata+=struct.pack('>BI',0x50|typ,string(name))
 body=bytearray()
 for row in rows:
  for name,typ in columns:
   v=row.get(name);v=string(v)if typ==10 else (0 if v is None else v)
   body+=struct.pack('>'+formats[typ],*(v if typ==11 else(v,)))
 rowlen=sum(struct.calcsize('>'+formats[t])for _,t in columns);ro=24+len(coldata);so=ro+len(body);do=so+len(strings);table=struct.pack('>IIIIHHI',ro,so,do,no,len(columns),rowlen,len(rows))+coldata+body+strings
 return b'@UTF'+struct.pack('>I',len(table))+table
content={f.relative_to(P/'original-cpk').as_posix():f.read_bytes()for f in(P/'original-cpk').rglob('*')if f.is_file()}
additions={f.relative_to(P/'cpk-kit-additions').as_posix():f.read_bytes()for f in(P/'cpk-kit-additions').rglob('*')if f.is_file()};assert not(set(content)&set(additions));content.update(additions)
rows=[]
for i,(path,data)in enumerate(sorted(content.items())):
 fileid=oldids.get(path)
 if fileid is None:fileid=nextid;nextid+=1
 parent,name=(path.rsplit('/',1)if '/'in path else ('',path));rows.append({'DirName':parent,'FileName':name,'FileSize':len(data),'ExtractSize':len(data),'FileOffset':0,'ID':fileid,'UserString':'<NULL>'})
cols=schema(old[oldtoc+16:oldtoc+16+oldtocsize])
roundup=lambda n:(n+2047)&~2047
toc=make_utf('CpkTocInfo',cols,rows);content_at=roundup(2048+16+len(toc));at=content_at
for row in rows:row['FileOffset']=at-2048;at=roundup(at+row['FileSize'])
toc=make_utf('CpkTocInfo',cols,rows)
h=dict(header);h.update(TocOffset=2048,TocSize=16+len(toc),ContentOffset=content_at,ContentSize=at-content_at,Files=len(rows),FileSize=at,Align=2048,EnabledPackedSize=sum(map(len,content.values())),EnabledDataSize=sum(map(len,content.values())))
for k in ['EtocOffset','EtocSize','ItocOffset','ItocSize','GtocOffset','GtocSize','HtocOffset','HtocSize','HgtocOffset','HgtocSize']:h[k]=0
hd=make_utf('CpkHeader',schema(old[16:2048]),[h]);assert len(hd)+16<2048
packet=lambda magic,data:magic+(old[4:8]if magic==b'CPK 'else old[oldtoc+4:oldtoc+8])+struct.pack('<Q',len(data))+data
out=bytearray(at);out[:16+len(hd)]=packet(b'CPK ',hd);out[2048:2048+16+len(toc)]=packet(b'TOC ',toc);out[2042:2048]=b'(c)CRI'
for row in rows:
 name=(row['DirName']+'/'+row['FileName']).lstrip('/');start=2048+row['FileOffset'];out[start:start+row['FileSize']]=content[name]
path=P/'payload/livedata/dt870_mobile_and.cpk';path.write_bytes(out)
# Verify through a separate existing reader, including every original byte.
newheader=utf(out[16:2048])[0];newrows=utf(out[2064:2064+len(toc)]);assert len(newrows)==len(content)
for row in newrows:
 name=(row['DirName']+'/'+row['FileName']).lstrip('/');start=min(newheader['TocOffset'],newheader['ContentOffset'])+row['FileOffset'];assert bytes(out[start:start+row['FileSize']])==content[name]
 if name in oldids:assert row['ID']==oldids[name]
(P/'cpk-validation.json').write_text(json.dumps({'passed':True,'original_files_preserved':len(content)-len(additions),'added_exact_kit_recipes':len(additions),'original_file_IDs_preserved':True,'original_TOC_schema_preserved':True,'readback_files':len(newrows),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'phone_tested':False},indent=2));print('CPK_PASS',len(newrows),len(out))
