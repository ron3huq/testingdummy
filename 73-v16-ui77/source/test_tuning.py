from pathlib import Path
import sys,sqlite3,json,tempfile,copy,shutil
P=Path('/workspace/ronaldo-work/73-ui77');sys.path.insert(0,str(P/'payload/work/tools'));import player_tuning as t,body_dimensions as b,myleague_editor_runtime as e
root=Path(tempfile.mkdtemp());tools=root/'work/tools';tools.mkdir(parents=True);e.PATH=tools/'myleague_editor.json';e.PATH.write_text(json.dumps(e.DEFAULT));b.ROOT=root
c=sqlite3.connect(root/'test.sqlite3');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);')
pid='88045755960841';req={'id':pid,'serial':1};params=[70]*147
for i in range(70,144):params[i]=0
params[70]=1;params[71]=1;params[47]=185;params[48]=83
v={'parameters':params,'_careerplan_base_parameters':list(params),'additional_skill_id':[4,8,74,74,74],'level_info':{'level':10},'other':'keep'};c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,1,json.dumps(v)));c.commit()
assert t.get(c,'ui77_skills_get',req)['selected']==[0,2]
t.apply(c,'ui77_skills_apply',dict(req,selected=[1,17,62]));new=json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0]);assert new['additional_skill_id']==v['additional_skill_id']and new['level_info']==v['level_info']
assert all(new['parameters'][flag]==int(i in [1,17,62])for i,flag in enumerate(e.FLAGS));assert new['parameters'][:70]==params[:70]
t.apply(c,'ui77_physics_apply',dict(req,height=255,weight=250,jump=99));new=json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0]);assert [new['parameters'][i]for i in [47,48,39]]==[255,250,99]
tr=[];c.set_trace_callback(tr.append);tr.clear();out=t.project({'id':pid,'parameters':[0]*147});assert not tr and out['parameters'][39]==99 and 'innate_skills'not in out
before=e.PATH.read_bytes();saved=c.execute('SELECT json FROM gameplayers').fetchone()[0]
for bad in [dict(req,height=350,weight=250,jump=99),dict(req,height=255,weight=251,jump=99),dict(req,height=255,weight=250,jump=100)]:
 try:t.apply(c,'ui77_physics_apply',bad);raise AssertionError('invalid accepted')
 except ValueError:pass
original=t.write_config
def fail(cfg):original(cfg);raise OSError('injected failure')
t.write_config=fail
try:t.apply(c,'ui77_skills_apply',dict(req,selected=[]));raise AssertionError('failure not raised')
except OSError:pass
t.write_config=original;assert e.PATH.read_bytes()==before and c.execute('SELECT json FROM gameplayers').fetchone()[0]==saved
t._conn=None;t.skills={};t.physics={};t.load(c);assert t.skills[pid]==[1,17,62]and t.physics[pid]['jump']==99
cfg=json.loads(e.PATH.read_text());row=next(r for r in cfg['players']if r['id']==pid);assert row['parameters']['47']==255 and row['parameters']['48']==250 and row['parameters']['107']==1
projection=e.project({'gameplayer_id':{'id':int(pid)},'parameters':new['parameters'],'additional_skill_id':list(v['additional_skill_id'])},122);assert projection['additional_skill_id']==v['additional_skill_id']
shutil.rmtree(root);(P/'tuning-storage-validation.json').write_text(json.dumps({'passed':True,'selected_skill_flags_match_native147_layout':True,'current_innate_list_shown':True,'additional_skills_progression_and_other_fields_preserved':True,'height255_weight250_jump99_saved':True,'height350_and_out_of_range_rejected':True,'config_SQL_and_cache_rollback':True,'settings_reload':True,'wire_projection_zero_SQL':True,'device_tested':False},indent=2));print('TUNING_STORAGE_PASS')
