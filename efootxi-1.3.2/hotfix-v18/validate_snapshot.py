"""Passive Team -> JSON -> editor -> original runtime formation consumer.
Fixture deliberately uses a nonidentity order, four different plans, unset
roles and a bench captain. Expected identities are checked through native
accessors, independently of the JSON parser.
"""
from pathlib import Path
import sys,json,struct,ctypes as C,copy
r=Path(__file__).parent;sys.path[:0]=[str(r),str(r.parent/'android/user-gateway/work/tools')]
import myleague_team_snapshot as snapshot,myleague_editor_runtime as editor
s=(r/'validate_native.py').read_text();exec(compile(s[:s.index('import sys,sqlite3')],str(r/'validate_native.py'),'exec'),globals())
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(addr,0x33000010,count=20000000);assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
cat=json.loads((r.parent/'editor-v17/catalog.json').read_text());base=cat['teams']['518:1220'];ids=[int(p['id'])for p in base['roster']];tp=0x33300000;db=0x30000000;XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
for i,pid in enumerate(sorted(ids)):
 p=db+i*0x1d0;w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR)
 call(0x82a907c,p,47,185)
 for ix in range(14,41):
  if ix!=33:call(0x82a907c,p,ix,70)
w(db+0x2686098,'I',len(ids));u.mem_write(tp,b'\0'*0x700);w(tp,'I',1220<<14);u.mem_write(tp+4,b'Actual Madrid\0');w(tp+0x40c,'I',len(ids)<<9)
for i,pid in enumerate(ids):w(tp+0x110+16*i,'QQ',0,pid);w(tp+0x3a2+2*i,'H',i+1)
order=[0,2,1,4,3,5,7,6,10,8,9]+list(range(11,len(ids)));u.mem_write(tp+0x538,bytes(order)+bytes([255])*(40-len(ids)))
for variant,off in enumerate([0x478,0x49a,0x4d8,0x4fa]):
 for i,row in enumerate(base['roster'][:11]):
  call(0x82b5edc,tp+off,i,row['role']);call(0x8251cd8,tp+off+11+2*i,max(0,row['x']-variant),row['y'])
 u.mem_write(tp+off+33,bytes([variant%2]))
u.mem_write(tp+0x560,bytes([9,255,8,6,7,10]));u.mem_write(tp+0x569,bytes([12]));before=bytes(u.mem_read(tp,0x700))
def boundary(uc,a,size,data):
 if a in [0x33000060,0x33000040]:ret=tp
 elif a==0x82468d4:ret=0x33201000
 else:return
 uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary);w(0x33201040,'Q',db)
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4);call(symbols['configure_cached_team'],0,0x33000060)
call(symbols['activate_context'],0);call(symbols['cached_team_hook'],0,0)
assert bytes(u.mem_read(tp,0x700))==before
class Function:
 def __init__(self,name):self.name=name
 def __call__(self,*args):
  if self.name=='team_capture_copy':
   i,out,n=args;dest=0x33220000;size=call(symbols[self.name],i,dest,n)
   if size:C.memmove(out,bytes(u.mem_read(dest,size)),size)
   return size
  return call(symbols[self.name],*args)
class Handle:
 def __getattr__(self,name):f=Function(name);setattr(self,name,f);return f
h=Handle();path=r.parent/'editor-v18/synthetic-live-teams.json';snapshot._last=None;assert snapshot.export(h,path);doc=json.loads(path.read_text());assert len(doc['teams'])==1 and not doc['errors'];t=doc['teams'][0]
assert [p['id']for p in t['roster']]==[str(ids[i])for i in order];assert [p['shirt']for p in t['roster']]==[i+1 for i in order];assert t['captain']==str(ids[12]);assert t['kickers']==[str(ids[9]),None,str(ids[8]),str(ids[6]),str(ids[7]),str(ids[10])]
# Update one cached shirt, observe change; identical reread must not rewrite file.
assert not snapshot.export(h,path);u.mem_write(tp+0x3a2+2*9,bytes([77,0]));call(symbols['cached_team_hook'],0,0);assert snapshot.export(h,path);doc=json.loads(path.read_text());t=doc['teams'][0];assert next(p for p in t['roster']if p['id']==str(ids[9]))['shirt']==77
# For browser rendering fixture keep the nonidentity order, four variants,
# bench captain and unset FK; the device-produced kind/version match exactly.
project=copy.deepcopy(editor.DEFAULT);project['teams']=[t];editor._config=editor.validate(project);editor.install_native(h)
ptr=call(0x823c8d4,db,0,ids[0]);assert ptr==db+sorted(ids).index(ids[0])*0x1d0,('resolve-before',hex(db),hex(ptr))
assert call(0x68fe720,ptr)==0 and u.reg_read(UC_ARM64_REG_X1)==ids[0],('key',hex(ptr),call(0x68fe720,ptr),u.reg_read(UC_ARM64_REG_X1))
call(symbols['activate_context'],518);result=call(symbols['ensure_team'],1220);assert result==1,(result,call(symbols['editor_status'],4),ids)
out=0x33230000
for block in range(2):
 for variant in range(2):
  call(0x82bfb2c,out,11,tp+0x478+block*0x60,variant,tp+0x538)
  for i,old in enumerate(order[:11]):
   member,xy,role=struct.unpack('<IH2xI',u.mem_read(out+16*i,12));call(0x68fc714,tp,member,0x33200000)
   assert u.reg_read(UC_ARM64_REG_X1)==ids[old]
   assert role==base['roster'][i]['role'];assert xy==struct.unpack('<H',bytes([max(0,base['roster'][i]['x']-(block*2+variant)),base['roster'][i]['y']]))[0]
  assert u.mem_read(tp+0x478+block*0x60+variant*0x22+33,1)[0]==variant%2
capt=u.mem_read(tp+0x569,1)[0];assert struct.unpack('<Q',u.mem_read(tp+0x118+capt*16,8))[0]==ids[12]
assert u.mem_read(tp+0x561,1)[0]==255
# Import/edit/export view must not claim arbitrary rows not present in a capture.
assert len(doc['teams'])==1 and t['source']=='NATIVE_MATCH_CACHE'
# Reject malformed source records instead of silently fabricating starters.
raw_capture=bytearray(struct.pack('<4I',1220,518,2,99)+before[:0x5d4]);rejected=[]
for case in ['count','order','keykind','captain','role']:
 bad=bytearray(raw_capture)
 if case=='count':struct.pack_into('<I',bad,16+0x40c,41<<9)
 if case=='order':bad[16+0x539]=bad[16+0x538]
 if case=='keykind':struct.pack_into('<Q',bad,16+0x110,1)
 if case=='captain':bad[16+0x569]=254
 if case=='role':bad[16+0x478]=13
 try:snapshot.decode(bad)
 except ValueError:rejected.append(case)
 else:raise AssertionError(case)
# The bootstrap update accepts v17 project in memory without rewriting it.
import tempfile
with tempfile.TemporaryDirectory()as tmp:
 old=Path(tmp)/'myleague_editor.json';legacy=copy.deepcopy(project);legacy['base_version']='native-hotfix-v17';old.write_text(json.dumps(legacy));saved=old.read_bytes();oldpath=editor.PATH;editor.PATH=old;editor._config=None
 assert editor.config()['base_version']=='native-hotfix-v18' and old.read_bytes()==saved
 editor.PATH=oldpath
report=dict(status='PASSIVE_CAPTURE_NONIDENTITY_ORDER_FOUR_PLAN_ROUNDTRIP_PASS',device_tested=False,source_team_bytes_unchanged_on_capture=True,exact64_and_shirts_follow_identity=True,four_distinct_native_plans_preserved=True,unset_taker_and_bench_captain_preserved=True,engine_runtime_consumer_82bfb2c_verified=True,unchanged_snapshot_not_rewritten=True,invalid_records_rejected=rejected,fixture='synthetic; not a phone dump')
(r/'snapshot-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
