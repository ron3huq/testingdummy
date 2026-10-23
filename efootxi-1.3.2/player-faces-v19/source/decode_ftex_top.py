"""Recover BC7 FTEX 2.03 full-resolution level without relying on malformed
small source mip headers. Re-encoding uses native Android mip layout separately.
"""
from pathlib import Path
import struct,zlib,json,hashlib
from PIL import Image
root=Path(__file__).resolve().parent.parent;rows=[]
for p in sorted((root/'kit-inputs').glob('*.ftex')):
 b=p.read_bytes();magic,version,fmt,w,h,d=struct.unpack_from('<4sfHHHH',b);assert magic==b'FTEX' and abs(version-2.03)<.0001 and fmt==11 and d==1
 offset,size,compressed,index,extension,chunks=struct.unpack_from('<IIIBBH',b,64);assert index==extension==0 and size==((w+3)//4)*((h+3)//4)*16
 payload=[]
 for i in range(chunks):
  cs,us,off=struct.unpack_from('<HHI',b,offset+i*8);piece=b[offset+(off&0x7fffffff):offset+(off&0x7fffffff)+cs];decoded=piece if off>>31 else zlib.decompress(piece);assert len(decoded)==us;payload.append(decoded)
 data=b''.join(payload);assert len(data)==size
 hdr=struct.pack('<I6I11I',124,0x81007,h,w,len(data),0,0,*([0]*11))+struct.pack('<II4s5I',32,4,b'DX10',0,0,0,0,0)+struct.pack('<5I',0x1000,0,0,0,0);assert len(hdr)==124
 temporary=p.with_suffix('.dds');temporary.write_bytes(b'DDS '+hdr+struct.pack('<5I',98,3,0,1,0)+data)
 im=Image.open(temporary);im.save(p.with_suffix('.png'));temporary.unlink()
 rows.append({'file':p.name,'size':[w,h],'sha256':hashlib.sha256(b).hexdigest(),'recovered_top_level_bytes':len(data),'ignored_small_mips':True})
assert len(rows)==2;(root/'ftex-source-validation.json').write_text(json.dumps({'status':'TWO_FTEX_TOP_LEVEL_BC7_RECOVERY_PASS','files':rows},indent=2));print('TWO_FTEX_TOP_LEVEL_BC7_RECOVERY_PASS')
