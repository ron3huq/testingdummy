from pathlib import Path
import struct,json
P=Path('/workspace/ronaldo-work/73-ui6');s=(P/'test_native.py').read_text();exec(s[:s.index('import sys,sqlite3')]);seen=[];heap=0x31000000
u.mem_write(0xa5a4f40,b'\1')
def stubs(uc,addr,size,data):
 global heap
 if addr==0x2f3877c:
  dst=uc.reg_read(UC_ARM64_REG_X0);src=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_X2);raw=bytes(uc.mem_read(src,n));seen.append(raw.decode('ascii','replace'))
  if n<23:uc.mem_write(dst,bytes([n*2])+raw+b'\0'*(23-n))
  else:
   uc.mem_write(heap,raw+b'\0');uc.mem_write(dst,struct.pack('<QQQ',(n+16)|1,n,heap));heap+=n+32
  uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stubs)
try:call(0x75eac8c)
except Exception as exc:print('STOP',hex(u.reg_read(UC_ARM64_REG_PC)),str(exc)[:180])
rows=[]
for i in range(147):
 at=0xa5a19f8+24*i;b=bytes(u.mem_read(at,24));n=struct.unpack_from('<Q',b,8)[0]if b[0]&1 else b[0]>>1
 if 0<n<100:
  value=bytes(u.mem_read(struct.unpack_from('<Q',b,16)[0],n))if b[0]&1 else b[1:1+n]
  if all(32<=c<127 for c in value):rows.append({'index':i,'name':value.decode(),'value':struct.unpack('<I',u.mem_read(0xa5ac888+i*4,4))[0]})
(P/'parameter-enum.json').write_text(json.dumps(rows,indent=2));print('ENUM',len(rows));print([r for r in rows if 43<=r['index']<=70])
