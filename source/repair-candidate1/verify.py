from pathlib import Path
import sys, types, json, copy, sqlite3, struct, hashlib
R=Path('/workspace/work/full8/candidate')
T=R/'assets/gateway-release/work/tools'
sys.path.insert(0,str(T))
import myleague_team_snapshot as snapshot
import myleague_editor_runtime as editor

# Cached indices deliberately differ from roster positions and card IDs.
ids=[str(10000000000000+i)for i in range(14)]
indices=[91,23,77,104,15,8,64,31,52,6,99,113,42,19]
raw=bytearray(0x5d4);struct.pack_into('<I',raw,0,12345<<14)
struct.pack_into('<I',raw,0x40c,14<<9)
for i,pid in enumerate(ids):
 struct.pack_into('<QQ',raw,0x110+16*i,indices[i],int(pid))
 struct.pack_into('<H',raw,0x3a2+2*i,i+1)
order=list(range(14));order[2],order[7]=order[7],order[2]
raw[0x538:0x538+14]=bytes(order)
for off in (0x478,0x49a,0x4d8,0x4fa):
 for i in range(11):raw[off+i]=0 if i==0 else 5
raw[0x569]=7;raw[0x560:0x566]=bytes([7,2,1,3,4,5])
blob=struct.pack('<4I',12345,518,2,1)+raw
row=snapshot.decode(blob)
assert [p['id']for p in row['roster']]==[ids[i]for i in order]
assert row['captain']==ids[7] and row['kickers'][0]==ids[7]
assert row['native_keys'][7]=={'word0':31,'player_id':ids[7]}
try:snapshot.decode(struct.pack('<4I',12345,518,1,1)+raw)
except ValueError:pass
else:raise AssertionError('stock keys interpreted as cached indices')
bad=bytearray(blob);struct.pack_into('<Q',bad,16+0x120,indices[0])
try:snapshot.decode(bad)
except ValueError:pass
else:raise AssertionError('duplicate cache index accepted')

# Drive the actual original ARM64 accessor on the same cache record.
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM
from unicorn.arm64_const import UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_SP,UC_ARM64_REG_LR
from elftools.elf.elffile import ELFFile
engine=Path('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so')
assert hashlib.sha256(engine.read_bytes()).hexdigest()==snapshot.ENGINE_SHA
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
with engine.open('rb')as f:
 for seg in ELFFile(f).iter_segments():
  if seg['p_type']!='PT_LOAD':continue
  start=seg['p_vaddr']&~4095;end=(seg['p_vaddr']+seg['p_memsz']+4095)&~4095
  u.mem_map(start,end-start);u.mem_write(seg['p_vaddr'],seg.data())
u.mem_map(0x30000000,0x10000);u.mem_write(0x30000000,bytes(raw))
native=[]
for pool in order[:11]:
 u.reg_write(UC_ARM64_REG_X0,0x30000000);u.reg_write(UC_ARM64_REG_X1,pool);u.reg_write(UC_ARM64_REG_X2,0)
 u.reg_write(UC_ARM64_REG_SP,0x3000f000);u.reg_write(UC_ARM64_REG_LR,0x3000f100)
 u.emu_start(0x68fc714,0x3000f100,count=10000)
 key=(u.reg_read(UC_ARM64_REG_X0),u.reg_read(UC_ARM64_REG_X1))
 assert key==(indices[pool],int(ids[pool])),(pool,key)
 native.append(key)

# Durable DB -> restored runtime file -> real installer arguments, after repair.
body=types.ModuleType('body_dimensions');body.identity=lambda x:x
sys.modules['body_dimensions']=body
import transfer_editor as transfer
transfer.validate_team=editor.validate # load validates below through a wrapper
transfer.validate_team=lambda r:editor.validate(dict(copy.deepcopy(editor.DEFAULT),teams=[r]))
work=Path('/workspace/work/full8/tests');work.mkdir(exist_ok=True)
editor.PATH=work/'myleague_editor.json'
editor.PATH.write_text(json.dumps(editor.DEFAULT));editor._config=None
c=sqlite3.connect(':memory:');c.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)')
c.execute('INSERT INTO meta VALUES(?,?)',(transfer.KEY,json.dumps({'518:12345':row})));c.commit()
transfer.load(c);transfer.restore_config()
assert editor.config()['teams'][0]['captain']==ids[7]
editor.requested_long_sleeves=lambda d:d
class Fn:
 def __init__(self,name):self.name=name;self.calls=[]
 def __call__(self,*args):self.calls.append(args);return 1
class Hook:
 def __init__(self):self.fns={}
 def __getattr__(self,name):return self.fns.setdefault(name,Fn(name))
hook=Hook();editor.install_native(hook)
assert hook.editor_add_team.calls==[(12345,518,14,2)]
assert hook.editor_team_slot.calls[2][2]==int(ids[7])
assert hook.editor_team_taker.calls[0]==(1,0,2)
editor.PATH.write_text(json.dumps(editor.DEFAULT));editor._config=None
transfer.restore_config();assert editor.config()['teams'][0]['captain']==ids[7]

report={'base_commit':'74a1cd8100c8ecd022af9f16ef1f9f98cffcfc96',
 'checks':['cached index/full-ID decoding','stock/cached key separation','duplicate index rejection','original ARM64 Team accessor on synthetic mode-2 record','DB restoration after resource replacement','native installer receives captain and taker by exact player ID'],
 'original_native_accessor_keys':native,'device_verified':False,
 'limitations':['Synthetic records do not establish real cache pool ownership.','The original native hook is unchanged.','No match, facial animation, body rig or real phone validation.']}
(work/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
