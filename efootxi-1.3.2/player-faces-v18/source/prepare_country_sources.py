"""Rebuild the two research tables from a pinned CPK already in this repository.
WESYS v2 unpacker; no network, no phone files, no dependency on cached bytecode.
"""
from pathlib import Path
import hashlib,json,struct,zlib
root=Path(__file__).resolve().parent.parent
meta=json.loads((root/'references/country-source-offsets.json').read_text())
cpk=(root.parent/'crcfix/test/dt200_mobile_all.cpk').read_bytes()
assert hashlib.sha256(cpk).hexdigest()==meta['cpk_sha256']
def unpack(data):
 assert data[3:8]==b'WESYS'
 compressed,size=struct.unpack_from('<II',data,8);payload=bytearray(data[16:16+compressed]);assert len(payload)==compressed
 if data[2]&2:
  assert data[1]&15==2
  x,y,z=3982174560,1246903118,4087552941;w=(compressed|(size<<16))&0xffffffff
  for p in range(0,compressed//4*4,4):
   t=(x^(x<<11))&0xffffffff;x,y,z=y,z,w;w=(w^(w>>19)^t^(t>>8))&0xffffffff
   struct.pack_into('<I',payload,p,struct.unpack_from('<I',payload,p)[0]^w)
 raw=zlib.decompress(payload) if data[2]&1 else bytes(payload);assert len(raw)==size
 return raw
out=Path('/workspace/ronaldo-work/v17-research/tables');out.mkdir(parents=True,exist_ok=True);rows=[]
for r in meta['rows']:
 encoded=cpk[r['offset']:r['offset']+r['size']];assert hashlib.sha256(encoded).hexdigest()==r['sha256'];decoded=unpack(encoded);p=out/(Path(r['file']).stem+'-decoded.bin');p.write_bytes(decoded);rows.append({'file':r['file'],'decoded_bytes':len(decoded),'decoded_sha256':hashlib.sha256(decoded).hexdigest()})
country=(out/'Country-decoded.bin').read_bytes();countries={}
for i in range(0,len(country),1488):
 row=country[i:i+1488];name=row[148:218].split(b'\0',1)[0].decode('utf8')
 if name in ['Vietnam','Portugal']:
  packed=int.from_bytes(row[:8],'little');countries[name]={'internal_country_code':(packed>>10)&511,'flag_resource_id':packed&1023,'source_row':i//1488}
assert countries['Vietnam']['internal_country_code']==38 and countries['Portugal']['internal_country_code']==228
report={'status':'PINNED_CPK_COUNTRY_AND_PLAYER_WESYS_DECODE_PASS','country_row_bytes':1488,'player_row_bytes':400,'countries':countries,'source_cpk_sha256':meta['cpk_sha256'],'decoded_tables':rows,'native_importer':'0x824c5d0 -> wire country getter 0x8257850 -> Country lookup 0x8257878 -> native record setter 0x8257598 (uint16 record+0x198)','phone_verified':False}
(root/'nationality-source-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],countries)
