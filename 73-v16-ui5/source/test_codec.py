from pathlib import Path
import json,struct,zlib
P=Path('/workspace/ronaldo-work/73-ui5');s=(P/'test_native.py').read_text();exec(s[:s.index('import sys,sqlite3')])
checks=[];dest=0x30001000;stream=0x30060000;source=0x30100000;pool=0x30200000
u.mem_write(0x33000200,b'1.2.11\0');allocated=[]
def helpers(uc,addr,size,data):
 global pool
 if addr==0x33000100:
  n=uc.reg_read(UC_ARM64_REG_X1)*uc.reg_read(UC_ARM64_REG_X2);out=pool;pool=(pool+n+31)&~31;assert pool<0x31000000
  uc.mem_write(out,b'\0'*n);allocated.append((out,n));uc.reg_write(UC_ARM64_REG_X0,out);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 elif addr==0x33000120:uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,helpers)
call(symbols['configure_raw_inflate'],0,0x6917eb0)
def inflate(raw,patched=True):
 comp=zlib.compress(raw);u.mem_write(source,comp);u.mem_write(dest,b'\xcd'*len(raw));u.mem_write(stream,b'\0'*112)
 w(stream,'Q',source);w(stream+8,'I',len(comp));w(stream+24,'Q',dest);w(stream+32,'I',len(raw));w(stream+64,'QQ',0x33000100,0x33000120)
 result=call(0x6917c84,stream,15,0x33000200,112);assert result==0,('init',hex(result))
 result=call(symbols['raw_inflate_hook']if patched else 0x6917eb0,stream,4);assert result==1,('inflate',hex(result))
 assert struct.unpack('<Q',u.mem_read(stream+40,8))[0]==len(raw)
 assert call(0x6919fcc,stream)==0
 return bytes(u.mem_read(dest,len(raw)))
ordinary=b'unchanged real zlib output'*250;assert inflate(ordinary)==ordinary
checks.append('Actual original73 inflateInit2/inflate/inflateEnd execute with compiled raw_inflate_hook; unrelated bytes exact')
ns={};code=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v18/source/prepare_country_sources.py').read_text();exec('import struct,zlib\n'+code[code.index('def unpack'):code.index('out=Path')],ns)
for tid in [100,242,245,351,352]:
 for slot,part in [(1,'1st'),(2,'2nd')]:
  raw=ns['unpack']((Path('/workspace/ronaldo-work/73-ui2/tables870/common/etc/uniform/team'if tid==100 else'/workspace/ronaldo-work/73-ui/tables/common/etc/uniform/team')/str(tid)/(str(tid)+'_DEF_'+part+'_realUni.bin')).read_bytes());out=inflate(raw);donor=ns['unpack']((Path('/workspace/ronaldo-work/73-ui2/tables870/common/etc/uniform/team/100')/('100_DEF_'+part+'_realUni.bin')).read_bytes())
  expected=bytearray(raw)
  if tid!=100:expected[19:76]=donor[19:76]
  assert out==bytes(expected),(tid,slot)
checks.append('All eight native custom home/away layouts receive exact licensed glyph layout; team100 remains byte exact')
raw=Path('/workspace/ronaldo-work/73-ui4/Coach-decoded.bin').read_bytes();out=inflate(raw);expected=bytearray(raw)
for rule in json.loads(Path('/workspace/ronaldo-work/73-ui4/coach-rules.json').read_text()):
 pos=rule['offset'];expected[pos:pos+176]=bytes.fromhex(rule['new']);bits=int.from_bytes(out[pos+16:pos+32],'little');assert(bits>>42)&511==rule['country_internal'];assert((bits>>103)&63)+15==rule['age'];assert out[pos+78:pos+124].rstrip(b'\0').decode()==rule['name']
assert out==bytes(expected)
checks.append('Actual292336-byte Coach table decompresses and changes exactly two pinned176-byte rows; names/country/age decoded back')
(P/'codec-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'real_engine_zlib':True,'phone_tested':False},indent=2));print('CODEC_PASS',checks)
