from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v24/source');from cpk_extract import utf,decompress
P=Path('/workspace/ronaldo-work/73-ui74');P.mkdir(exist_ok=True);old=Path('/workspace/ronaldo-work/73-ui6/original-dt870.cpk').read_bytes();overlay=Path('/workspace/ronaldo-work/73-ui71/payload/livedata/dt870_mobile_and.cpk').read_bytes()
F={0:'B',1:'b',2:'H',3:'h',4:'I',5:'i',6:'Q',7:'q',8:'f',9:'d',10:'I',11:'II'}
def xor(data):
 out=bytearray();key=0x655f
 for b in data:out.append(b^(key&255));key=(key*0x4115)&0xffffffff
 return bytes(out)
def schema(raw):
 raw=raw if raw[:4]==b'@UTF'else xor(raw);b=raw[8:];ro,so,do,no,nc,rl,nr=struct.unpack_from('>IIIIHHI',b);at=24;out=[]
 for i in range(nc):
  start=at;flag=b[at];at+=1
  if flag==0:flag=b[at+2];at+=3
  prefix=b[start:at];ix=struct.unpack_from('>I',b,at)[0];at+=4;name=b[so+ix:b.find(b'\0',so+ix)].decode();typ=flag&15
  out.append((name,flag,prefix))
  if flag&0xf0 in(0x20,0x30):at+=struct.calcsize('>'+F[typ])
 return out

def table(title,columns,rows,encrypted):
 strings=bytearray();indexes={}
 def string(s):
  if s is None:s=''
  if s not in indexes:indexes[s]=len(strings);strings.extend(s.encode()+b'\0')
  return indexes[s]
 def value(v,typ):
  if typ==10:v=string(v)
  return struct.pack('>'+F[typ],*(v if typ==11 else(v,)))
 titleid=string(title);cols=bytearray();body=bytearray();rowlen=0
 for name,flag,prefix in columns:
  cols+=prefix+struct.pack('>I',string(name));store=flag&0xf0;typ=flag&15
  if store in(0x20,0x30):
   vals=[r[name]for r in rows];assert all(v==vals[0]for v in vals),name;cols+=value(vals[0],typ)
  elif store==0x50:rowlen+=struct.calcsize('>'+F[typ])
  else:assert all(r.get(name)is None for r in rows),name
 for row in rows:
  for name,flag,prefix in columns:
   if flag&0xf0==0x50:body+=value(row[name],flag&15)
 ro=24+len(cols);so=ro+len(body);do=so+len(strings);data=struct.pack('>IIIIHHI',ro,so,do,titleid,len(columns),rowlen,len(rows))+cols+body+strings;raw=b'@UTF'+struct.pack('>I',len(data))+data
 return xor(raw)if encrypted else raw

def read(data):
 h=utf(data[16:2048])[0];off=h['TocOffset'];size=struct.unpack_from('<Q',data,off+8)[0];rows=utf(data[off+16:off+16+size]);base=min(off,h['ContentOffset']);content={}
 for row in rows:
  name=((row.get('DirName')or'')+'/'+row['FileName']).lstrip('/');start=base+row['FileOffset'];content[name]=(decompress(data[start:start+row['FileSize']]),row)
 return h,off,size,rows,content
h,off,size,oldrows,oldfiles=read(old);nh,nof,nsz,orows,wanted=read(overlay);hc=schema(old[16:2048]);tc=schema(old[off+16:off+16+size]);encH=old[16:20]!=b'@UTF';encT=old[off+16:off+20]!=b'@UTF';align=h['Align'];roundup=lambda n:(n+align-1)//align*align
ordered=[((r.get('DirName')or'')+'/'+r['FileName']).lstrip('/')for r in oldrows]+[name for name,(_,r)in sorted(wanted.items(),key=lambda item:item[1][1]['ID'])if name not in oldfiles]
rows=[dict(wanted[name][1])for name in ordered]
# Calculate table size using original storage flags and constant columns.
toc=table('CpkTocInfo',tc,rows,encT);content_at=roundup(off+16+len(toc));shift=content_at-h['ContentOffset'];assert shift>=0
out=bytearray(content_at)+bytearray(old[h['ContentOffset']:]);at=roundup(len(out));out.extend(b'\0'*(at-len(out)));changed=[]
for row in rows:
 name=((row.get('DirName')or'')+'/'+row['FileName']).lstrip('/');data=wanted[name][0]
 if name in oldfiles and oldfiles[name][0]==data:
  original=oldfiles[name][1];row['FileOffset']=original['FileOffset']+shift;row['FileSize']=original['FileSize'];row['ExtractSize']=original['ExtractSize'];assert row['ID']==original['ID']
 else:
  row['FileOffset']=at-off;row['FileSize']=row['ExtractSize']=len(data);out.extend(data);end=roundup(len(out));out.extend(b'\0'*(end-len(out)));at=end;changed.append({'file':name,'new':name not in oldfiles,'bytes':len(data)})
toc=table('CpkTocInfo',tc,rows,encT);h2=dict(h);h2.update(Sorted=0,ContentOffset=content_at,ContentSize=len(out)-content_at,TocSize=16+len(toc),Files=len(rows),EnabledPackedSize=sum(r['FileSize']for r in rows),EnabledDataSize=sum(r['ExtractSize']for r in rows))
header=table('CpkHeader',hc,[h2],encH);assert 16+len(header)<off
out[:off]=old[:off];out[:16+len(header)]=old[:8]+struct.pack('<Q',len(header))+header;out[off:off+16+len(toc)]=old[off:off+8]+struct.pack('<Q',len(toc))+toc
outpath=P/'dt870_ui74_mobile_and.cpk';outpath.write_bytes(out);newh,newoff,newsz,newrows,files=read(out)
assert set(files)==set(wanted)
assert [r['ID']for r in newrows[:len(oldrows)]]==[r['ID']for r in oldrows]
for name,(data,row)in files.items():assert data==wanted[name][0]and row['ID']==wanted[name][1]['ID'],name
assert schema(out[16:off])==hc and schema(out[newoff+16:newoff+16+newsz])==tc
assert {k for k,v in newh.items()if v is None}=={k for k,v in h.items()if v is None}
assert out[16:20]!=b'@UTF'and out[off+16:off+20]!=b'@UTF'
report={'passed':True,'file_bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'all142_asset_payloads_match_UI73':True,'all142_file_IDs_match_UI73':True,'header_and_TOC_storage_flags_match_stock':True,'stock_NULL_fields_preserved':True,'stock_UTF_encryption_preserved':True,'changed_or_added_assets':changed,'retained_original_content_region':True,'original101_TOC_row_positions_preserved':True,'unsorted_filename_TOC_declared_Sorted0':True,'device_tested':False};(P/'cpk-format-validation.json').write_text(json.dumps(report,indent=2));print('CPK_FORMAT_PASS',len(out),report['sha256'],'changed_or_added',len(changed))
