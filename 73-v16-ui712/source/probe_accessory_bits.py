from pathlib import Path
P=Path('/workspace/73-ui712');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/apk/assets/gateway-release/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_INVALID
def bad(uc,access,addr,size,value,data):
 print('INVALID',hex(addr),'PC',hex(uc.reg_read(UC_ARM64_REG_PC)),flush=True);return False
u.hook_add(UC_HOOK_MEM_INVALID,bad)
out=0x30010000;packed=0x30020000;vector=0x30030000;color=0x30040000;w(color,'4I',0xffffffff,0xffffffff,0xffffffff,0xffffffff)
# The source converter only constructs local strings here; avoid allocator calls in this fixture.
def stub(uc,addr,size,data):
 if addr in [0x2f46d10,0x2f376d4]:uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 if addr==0x8c1bc00:raise AssertionError('stack canary failed')
u.hook_add(UC_HOOK_CODE,stub)
def convert(raw):
 u.mem_write(out,bytes(0x300));u.mem_write(packed,raw);w(out+0x210,'QQQ',vector,vector,vector+216);u.mem_write(vector,bytes(216));u.reg_write(UC_ARM64_REG_X5,color);u.reg_write(UC_ARM64_REG_X6,color);u.reg_write(UC_ARM64_REG_X7,0);call(0x68d1fbc,out,packed,0,0,color);return bytes(u.mem_read(vector,216))
baseline=convert(bytes(52));rows=[]
for bit in range(52*8):
 raw=bytearray(52);raw[bit//8]=1<<(bit%8);data=convert(bytes(raw));flags=[];colors=[]
 for kind in range(18):
  assert struct.unpack_from('<I',data,kind*12)[0]==kind
  if data[kind*12+8]!=baseline[kind*12+8]:flags.append([kind,data[kind*12+8]])
  if data[kind*12+4:kind*12+8]!=baseline[kind*12+4:kind*12+8]:colors.append(kind)
 if flags or colors:rows.append({'byte':bit//8,'bit':bit%8,'flags':flags,'colors':colors})
(P/'accessory-packed-bits.json').write_text(json.dumps({'baseline':[list(struct.unpack_from('<IIB',baseline,i*12))for i in range(18)],'changes':rows},indent=2));print('NATIVE_FULL_CONVERTER_ACCESSORIES_PROBED',len(rows))
