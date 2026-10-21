from pathlib import Path
import struct,json
from unicorn import *
from unicorn.arm64_const import *
r=Path(__file__).parent;b=(r.parent/'android/official-apk/lib/arm64-v8a/libUE4.so').read_bytes();raw=(r.parent/'kit-research/Stadium.bin').read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
u.mem_map(0x82b0000,0x2000);u.mem_write(0x82b0a14,b[0x82b0a14-0x4000:0x82b0ac8-0x4000]);u.mem_map(0xcd6000,0x1000);u.mem_write(0xcd6e04,b[0xcd6e04:0xcd6e04+13]);u.mem_map(0x30000000,0x10000)
out=[]
for i in range(0,len(raw),1096):
 record=raw[i:i+1096];u.mem_write(0x30000000,record);values=[]
 for j in range(13):
  u.reg_write(UC_ARM64_REG_X0,0x30000000);u.reg_write(UC_ARM64_REG_X1,j);u.reg_write(UC_ARM64_REG_X2,0x30001000);u.reg_write(UC_ARM64_REG_LR,0x3000f000);u.emu_start(0x82b0a14,0x3000f000,count=500);values.append(struct.unpack('<I',u.mem_read(0x30001000,4))[0])
 row=dict(id=values[0],name=record[732:].split(b'\0')[0].decode(),parameters=values,snow_capability=bool(values[11]));out.append(row);print(row)
(r/'stadium-capabilities.json').write_text(json.dumps(dict(status='ORIGINAL_STADIUM_ACCESSOR_PASS',native_getter='0x82b0a14',snow_parameter=11,evidence='IsSnowPossible 0x3424294 calls73f46a4 -> DB lookup823e524 -> parameter11 via82b0a14',rows=out),indent=2,ensure_ascii=False)+'\n')
