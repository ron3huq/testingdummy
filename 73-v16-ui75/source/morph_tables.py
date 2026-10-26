from native_dis import read
from pathlib import Path
import json,struct
r=json.loads(Path('/workspace/ronaldo-work/73-ui/relocs.json').read_text())
for off in range(0x988f230,0x988f380,24):
 getter=int(r.get(str(off+8),'0'));table=int(r.get(str(off),'0'));names=[]
 for a in range(table,table+1024,32):
  addr=int(r.get(str(a),'0'))
  if not addr:break
  n=read(addr,100).split(b'\0')[0].decode('ascii','replace');names.append((n,struct.unpack('<6f',read(a+8,24))))
 print(hex(getter),names)
