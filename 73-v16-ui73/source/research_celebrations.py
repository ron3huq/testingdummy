from pathlib import Path
import sys,zipfile,struct,re,json,zlib,mmap,collections,csv
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v24/source');from cpk_extract import utf,decompress
P=Path('/workspace/ronaldo-work/73-ui73');out=P/'celebration-research';out.mkdir(exist_ok=True);found=[];tableinfo=[];allids=set()
engine=Path('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so')
def scan(data,source,kind):
 ids=set(int(m.group(1))for m in re.finditer(rb'dml_goal_celebrate_(\d{4})',data))
 # UTF16 labels are distinct evidence too.
 for m in re.finditer(rb'd\x00m\x00l\x00_\x00g\x00o\x00a\x00l\x00_\x00c\x00e\x00l\x00e\x00b\x00r\x00a\x00t\x00e\x00_\x00((?:[0-9]\x00){4})',data):ids.add(int(m.group(1).decode('utf-16le')))
 if ids:found.append({'source':source,'kind':kind,'ids':sorted(ids)});allids.update(ids)
 return ids
with engine.open('rb')as f:
 with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)as b:scan(b,str(engine),'native-engine')
with zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as apk:
 for archive in ['assets/dt230_mobile_all.cpk','assets/dt250_mobile_all.cpk','assets/dt251_mobile_all.cpk']:
  b=apk.read(archive);h=utf(b[16:2048])[0];off=h['TocOffset'];size=struct.unpack_from('<Q',b,off+8)[0];rows=utf(b[off+16:off+16+size]);base=min(off,h['ContentOffset'])
  for row in rows:
   name=((row.get('DirName')or'')+'/'+row['FileName']).lstrip('/');start=base+row['FileOffset'];raw=decompress(b[start:start+row['FileSize']]);data=raw;method='CPK'
   # PES bin payloads use a16-byte ESYS header followed by zlib.
   if len(raw)>18:
    try:
     decoded=zlib.decompress(raw[16:]);data=decoded;method='CPK+PES-zlib'
    except zlib.error:pass
   ids=scan(data,archive+':'+name,method)
   if name.endswith('.bin')and archive.startswith('assets/dt230'):
    safe=name.replace('/','__');(out/safe).write_bytes(data);tableinfo.append({'name':name,'raw_bytes':len(raw),'decoded_bytes':len(data),'header_hex':raw[:24].hex(),'method':method,'labels':sorted(ids)})
  print('SCANNED',archive,len(rows),flush=True)
(out/'labels-by-source.json').write_text(json.dumps(found,indent=2));(out/'anime-tables.json').write_text(json.dumps(tableinfo,indent=2));(out/'animation-labels.json').write_text(json.dumps(sorted(allids),indent=2));print('ALL_LABELS',len(allids),min(allids),max(allids),'REQUESTED',{x:x in allids for x in[542,571,595]},flush=True)
