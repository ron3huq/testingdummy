from pathlib import Path
import sys,sqlite3,json,types,tempfile
R=Path('/workspace/work/full8-rc2');T=R/'payload/assets/gateway-release/work/tools';sys.path[:0]=[str(T),'/workspace/73-v191-migration/decoded']
import single_player_runtime as single,body_dimensions
c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT); CREATE TABLE squads(squad_id INTEGER PRIMARY KEY,json TEXT); CREATE TABLE gameplayers(id INTEGER,serial INTEGER,json TEXT);CREATE TABLE player_pool(id INTEGER,serial INTEGER,json TEXT)')
pids=['89138556572074','88035555413452','106782819217056']
for i,pid in enumerate(pids):c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(int(pid),i+10,json.dumps({'parameters':[0]*147})))
c.execute('INSERT INTO squads VALUES(?,?)',(1,json.dumps({'squad_data':{'player_list':[{'gameplayer_id':{'id':int(pids[0]),'serial':10}},{'gameplayer_id':{'id':int(pids[1]),'serial':11}},{'gameplayer_id':{'id':int(pids[2]),'serial':0}}]}})));c.commit()
single._module=types.SimpleNamespace(_logic=types.SimpleNamespace(conn=c));single.start=lambda:None
assert [r['id']for r in single.player_index()]==pids[:2]
assert single.manage('ui7_single_player_search',{'query':pids[2]})['players']==[]
body_dimensions.engine_loaded=lambda:False
assert single.manage('ui7_single_player_apply',{'enabled':True,'player_id':pids[0]})['saved'];assert single.config()['player_id']==pids[0]
try:single.manage('ui7_single_player_apply',{'enabled':True,'player_id':pids[2]});raise AssertionError('non squad accepted')
except ValueError:pass
class Native:
 def __init__(self):self.calls=[];self.reject=False
 def single_player_configure(self,*args):self.calls.append(args);return int(not self.reject)
native=Native();single._native=native;single._ready.set();single._engine_base=123
body_dimensions.engine_loaded=lambda:True
assert single.manage('ui7_single_player_live',{'enabled':False,'player_id':pids[0]})['applies']=='live';assert not single.config()['enabled']
native.reject=True
try:single.manage('ui7_single_player_live',{'enabled':True,'player_id':pids[0]});raise AssertionError('rejection ignored')
except ValueError:pass
assert not single.config()['enabled'];assert native.calls[-1]==(123,0,int(pids[0]))
body_dimensions.engine_loaded=lambda:False
import transfer_player_editor as players,myleague_editor_runtime as editor,transfer_editor as transfer,transfer_traits
transfer.identity=lambda req:(12345,518);transfer.source=lambda tid,cid:{'roster':[{'id':pids[0]}]}
original_path=editor.PATH;directory=tempfile.TemporaryDirectory(dir=R);editor.PATH=Path(directory.name)/'config.json';editor.PATH.write_text(json.dumps({'schema':1,'players':[],'teams':[]}));editor._config=None
# Preserve actual validator configuration schema from baseline.
baseline=json.loads(original_path.read_text())if original_path.exists()else None
if baseline is None:
 baseline={'schema':1,'players':[],'teams':[]}
editor.PATH.write_text(json.dumps(baseline));editor._config=None
req={'player_id':pids[0],'values':{'skills':[0,5,73],'boosters':[31,511,418]}}
result=players.manage(c,'ui712_transfer_player_apply',req);assert result['saved']
editor._config=None
loaded=json.loads(editor.PATH.read_text());rows=[r for r in loaded['players']if r['id']==pids[0]and r['competition']==518];assert len(rows)==1
row=rows[0];assert row['boosters']==[31,511,418]
assert all(row['parameters'][str(flag)]==int(i in[0,5,73])for i,flag in enumerate(editor.FLAGS))
got=transfer_traits.manage(c,'ui712_transfer_traits_get',{'player_id':pids[0]});assert got['skills']==[0,5,73]and got['boosters']==[31,511,418]
players.manage(c,'ui712_transfer_player_apply',{'player_id':pids[0],'values':{'skills':[],'boosters':[0,0,0]}})
got=transfer_traits.manage(c,'ui712_transfer_traits_get',{'player_id':pids[0]});assert got['skills']==[]and got['boosters']==[0,0,0]
assert players.read(c)['518:'+pids[0]]['boosters']==[0,0,0]
report={'passed':True,'current_squad_exact_ID_and_serial_only':True,'unknown_and_unassigned_excluded':True,'single_save_reopen':True,'live_toggle_and_rejection_rollback':True,'transfer_traits_save_reopen_remove':True,'all_74_skill_flags_in_runtime_config':True,'three_booster_slots_in_runtime_config':True,'native_live_calls_mocked':True,'database_synthetic':True,'phone_verified':False}
(R/'runtime-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
