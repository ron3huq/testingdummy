"""Browser ZIP -> validated JSON -> C setter API -> actual native getters/roles.
Uses synthetic exact64 database and original Android ARM64 methods in Unicorn.
"""
from pathlib import Path
import json,zipfile,hashlib,sys,copy
r=Path(__file__).parent;app=r.parent/'editor-app';sys.path.insert(0,str(r))
import myleague_editor_runtime as editor
with zipfile.ZipFile(app/'browser-export.zip')as z:
 assert z.testzip()is None
 names=[n for n in z.namelist()if n.startswith('install/work/tools/')];assert len(names)==9
 for n in names:
  p=Path(n).name
  if p!='myleague_editor.json':assert z.read(n)==(r/p).read_bytes(),p
 data=editor.validate(json.loads(z.read('install/work/tools/myleague_editor.json')))
assert any(p['id']=='88044950524330'and p['competition']==122 and p['parameters']['107']==0 for p in data['players'])
# Reuse only the ELF loader and native call helpers, NOT the old test suite.
s=(r/'validate_native.py').read_text();exec(compile(s[:s.index('import sys,sqlite3')],str(r/'validate_native.py'),'exec'),globals())
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(addr,0x33000010,count=20000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR);ids=sorted({int(row['id'])for row in data['players']}|{int(p['id'])for team in data['teams']for p in team['roster']});db=0x30000000;players={}
for i,pid in enumerate(ids):
 p=db+i*0x1d0;players[pid]=p;w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR)
 for ix,v in [(0,12),(47,185),(48,80),(107,1)]+[(j,70)for j in range(14,41)if j!=33]:call(0x82a907c,p,ix,v)
w(db+0x2686098,'I',len(ids));team=data['teams'][0];tp=0x33300000;u.mem_write(tp,b'\x55'*0x700);w(tp,'I',team['team_id']<<14);w(tp+0x40c,'I',(11<<9)|0x80000001)
# Explicit editor replacement can replace mixed old keys, after FULL new-roster preflight.
for i in range(11):w(tp+0x110+i*16,'QQ',1,9999+i)
def boundary(uc,addr,size,data):
 if addr in [0x8c1bc60,0x8c1bc70]:
  dest,src,size=[uc.reg_read(reg)for reg in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]];uc.mem_write(dest,bytes(uc.mem_read(src,size)));ret=dest
 elif addr==0x33000060:ret=tp
 elif addr==0x33000040:ret=tp if uc.reg_read(UC_ARM64_REG_W1)>>14==team['team_id']else 0
 elif addr==0x82468d4:ret=0x33201000
 else:return
 uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary);w(0x33201040,'Q',db)
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4)
class Function:
 def __init__(self,name):self.name=name
 def __call__(self,*args):return call(symbols[self.name],*args)
class Handle:
 def __getattr__(self,name):f=Function(name);setattr(self,name,f);return f
editor._config=data;editor.install_native(Handle());assert call(symbols['editor_status'],0)==1
pid=88044950524330;p=players[pid]
for repeat in range(3):
 call(symbols['activate_context'],122);assert call(symbols['player_hook'],db,0,pid)==p
 assert {ix:get(p,ix)for ix in [17,20,47,48,107,116]}=={17:93,20:94,47:190,48:85,107:0,116:1}
 call(symbols['activate_context'],518);call(symbols['player_hook'],db,0,pid)
 assert get(p,47)==185 and get(p,48)==80 and get(p,107)==1
call(symbols['activate_context'],518);before=bytes(u.mem_read(tp,0x700))
# Missing single player must prevent ALL team field writes.
missing=int(team['roster'][-1]['id']);w(players[missing]+0x40,'Q',XOR)
assert call(symbols['ensure_team'],team['team_id'])==13 and bytes(u.mem_read(tp,0x700))==before
w(players[missing]+0x40,'Q',missing^XOR)
assert call(symbols['ensure_team'],team['team_id'])==1
for i,row in enumerate(team['roster']):
 assert struct.unpack('<QQ',u.mem_read(tp+0x110+i*16,16))==(0,int(row['id']))
 assert struct.unpack('<H',u.mem_read(tp+0x3a2+i*2,2))[0]==row['shirt']
for off in [0x478,0x49a,0x4d8,0x4fa]:
 for i,row in enumerate(team['roster'][:11]):
  assert call(0x82b5f10,tp+off,i)==row['role'];pos=call(0x82b5f30,tp+off,i);assert bytes(u.mem_read(pos,2))==bytes([row['x'],row['y']]),(hex(off),i,row,list(u.mem_read(pos,2)))
roster_ids=[p['id']for p in team['roster']];assert list(u.mem_read(tp+0x560,6))==[roster_ids.index(pid)for pid in team['kickers']];assert u.mem_read(tp+0x569,1)[0]==roster_ids.index(team['captain'])
# Custom fields outside known write ranges must be preserved.
changed=[i for i,(a,b)in enumerate(zip(before,u.mem_read(tp,0x700)))if a!=b];allowed=set(range(0x110,0x390))|set(range(0x3a2,0x3f2))|set(range(0x40c,0x410))|set(range(0x478,0x56a))|set(range(4,0x4e))|set(range(0x56f,0x5bf))|set(range(0x3f4,0x3f8))
assert all(i in allowed for i in changed)
# Repeated queries retain final custom formation; explicit leaving scope restores base data.
for i in range(3):assert call(symbols['ensure_team'],team['team_id'])==1
call(symbols['configure_cached_team'],0,0x33000060)
call(symbols['activate_context'],0);call(symbols['cached_team_hook'],0,0)
assert bytes(u.mem_read(tp,0x700))==before
call(symbols['team_hook'],db,team['team_id']<<14)
# The default compiled mod may change the team again; it must not remain the editor transfer.
assert struct.unpack('<Q',u.mem_read(tp+0x118+10*16,8))[0]!=110718
# Gateway projection strips explicitly removed learned skill too, without mutating source.
source={'gameplayer_id':{'id':pid},'parameters':[70]*147,'additional_skill_id':[1,11,74],'is_skill_added':'YES'};original=copy.deepcopy(source);out=editor.project(source,122);assert out['parameters'][17]==93 and out['parameters'][107]==0 and out['additional_skill_id']==[74,11,74] and source==original
assert editor.project(source,566)==source
# Invalid entire projects fail BEFORE native configuration.
invalid=[]
for change in ['duplicate_shirt','unknown_parameter','duplicate_player','bad_taker','float_id']:
 bad=copy.deepcopy(data)
 if change=='duplicate_shirt':bad['teams'][0]['roster'][1]['shirt']=bad['teams'][0]['roster'][0]['shirt']
 if change=='unknown_parameter':bad['players'][0]['parameters']['146']=1
 if change=='duplicate_player':bad['teams'][0]['roster'][1]['id']=bad['teams'][0]['roster'][0]['id']
 if change=='bad_taker':bad['teams'][0]['kickers'][0]='1'
 if change=='float_id':bad['players'][0]['id']=float(bad['players'][0]['id'])
 try:editor.validate(bad)
 except ValueError:invalid.append(change)
 else:raise AssertionError(change)
# Original native accessors must represent all body bounds offered by the UI.
for ix,values in [(47,[140,185,220]),(48,[40,80,130])]:
 for value in values:assert call(0x82a907c,p,ix,value)==1 and get(p,ix)==value,(ix,value,get(p,ix))
# Dynamic short/long choice exercised in the existing real serializer and
# native entity configuration hook, not just the JSON policy reader.
call(symbols['configure_appearance_serialize'],0,0x68d0868)
record=0x33210000;packed=record+0x100;entity=record+0x200;cfgp=record+0x400;vt=record+0x800;retstub=0x33000050
u.mem_write(retstub,struct.pack('<I',0xd65f03c0));w(entity,'Q',vt);w(entity+0x28,'Q',pid);w(vt+0x58,'Q',retstub)
u.mem_write(record,struct.pack('<QQQ',pid,0,0)+b'\0'*56)
for cid,packed_mode,field in [(122,1,0),(518,2,1)]:
 call(symbols['activate_context'],cid);assert call(symbols['appearance_serialize_hook'],record,packed)==1
 assert u.mem_read(packed+7,1)[0]>>6==packed_mode
 w(cfgp+0x50,'I',9);call(symbols['appearance_entity_hook'],entity,7,cfgp);assert struct.unpack('<I',u.mem_read(cfgp+0x50,4))[0]==field
call(symbols['set_appearance_trial'],1);assert call(symbols['appearance_card_status'],7)==0
report={'status':'BROWSER_ZIP_TO_NATIVE_EDITOR_PASS','device_tested':False,'exported_files':9,'exact64_ids_preserved':True,'stats_skills_height_weight_read_with_original_getters':True,'scope_exit_restores_height_weight_skills':True,'body_bounds_verified':True,'short_and_long_native_fields_verified':True,'repeat_queries_idempotent':True,'all_four_formation_variants_verified':True,'cached_team_restored_on_context0':True,'captain_six_takers_shirts_verified':True,'missing_player_prevents_all_team_writes':True,'explicit_roster_replaces_old_mixed_keys':True,'gateway_removes_learned_skill_without_source_mutation':True,'invalid_projects_rejected':invalid,'limits':['Synthetic exact64 DB and source records in Unicorn','Android appearance/formation visuals not tested']}
(r/'editor-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
