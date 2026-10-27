from pathlib import Path
import sys,json,sqlite3,tempfile,copy,types
from unittest.mock import patch
P=Path('/tmp/73-ui711');T=P/'build/payload/work/tools';sys.path.insert(0,str(T));import profile_editor as p,body_dimensions as b,player_model as m,myleague_editor_runtime as e
root=Path(tempfile.mkdtemp(prefix='ui711-profile-',dir='/tmp'));(root/'work/tools').mkdir(parents=True);e.PATH=root/'work/tools/myleague_editor.json';e.PATH.write_bytes((T/'myleague_editor.json').read_bytes());b.ROOT=root;b.engine_loaded=lambda:False
c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);')
pid=p.TARGETS[0];base={'parameters':[0]*147,'_careerplan_base_parameters':[0]*147,'level_info':{'level':100},'additional_skill_id':[1,4,74,74,74]};base['parameters'][46]=27;base['parameters'][47]=185;base['parameters'][48]=78;base['_careerplan_base_parameters']=list(base['parameters'])
for id,serial in [(pid,1),(pid,2),('88044950524330',1)]:c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(id,serial,json.dumps(base)))
c.commit();req={'id':pid,'serial':1,'name':'C.Ronaldo'};p.load(c);p.refresh();assert len(p.merged_cached)==5 and p.merged_cached[pid]['club']==109;assert p.merged_cached['105758469512061']['club']==100
assert p.manage(c,'ui711_profile_apply',dict(req,values={'model_source':'89138556575063'}))['saved']
for serial in [1,2]:
 r=json.loads(c.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(pid,serial)).fetchone()[0]);assert r['parameters'][47:49]==[170,67];assert r['level_info']==base['level_info']and r['additional_skill_id']==base['additional_skill_id']
assert json.loads(c.execute('SELECT json FROM gameplayers WHERE id=?',('88044950524330',)).fetchone()[0])==base
p.manage(c,'ui711_profile_apply',dict(req,values={'name':'Nguyễn Ronaldo','shirt':'Ronaldo','age':22,'traits':{'33':3,'42':2,'43':1,'45':2}}));row=p.manage(c,'ui711_profile_get',req);assert row['current_name']=='Nguyễn Ronaldo'and row['age']==22 and row['traits']['43']==1;cfg=e.requested_long_sleeves(e.config());r=next(r for r in cfg['players']if r['id']==pid and r['competition']==0);assert r['parameters']['46']==22 and r['parameters']['43']==1
trace=[];c.set_trace_callback(trace.append);trace.clear();pr=p.project(dict(base,id=pid));assert not trace and pr['parameters'][46:49]==[22,170,67]and pr['initial_base_team_id']==109 and pr['_nation_id']==228 and pr['initial_base_national_team_id']==6
beforecfg=e.PATH.read_bytes();beforeSQL=c.execute('SELECT value FROM meta WHERE key=?',(p.KEY,)).fetchone()[0];oldreplace=Path.replace;once=[False]
def fail(obj,dst):
 out=oldreplace(obj,dst)
 if obj.name.endswith('.ui711.tmp')and not once[0]:once[0]=True;raise OSError('injected after replace')
 return out
try:
 with patch.object(Path,'replace',fail):p.manage(c,'ui711_profile_apply',dict(req,values={'age':40}))
 raise AssertionError('Failure not raised')
except OSError:pass
assert e.PATH.read_bytes()==beforecfg and c.execute('SELECT value FROM meta WHERE key=?',(p.KEY,)).fetchone()[0]==beforeSQL
for v in [{'age':64},{'name':'a'*61},{'name':'abc\0'},{'traits':{'43':2}},{'club':999999},{'nation':999999},{'model_source':pid}]:
 try:p.manage(c,'ui711_profile_apply',dict(req,values=v));raise AssertionError('Bad input accepted')
 except ValueError:pass
(P/'profile-storage-validation.json').write_text(json.dumps({'passed':True,'five_default_identities_correct':True,'source_dimensions_copied_to_all_owned_instances':True,'body11_inheritance_configured':True,'name_UTF8_age_and_foot_traits_save_reload':True,'native_parameter_override_config_created':True,'Portugal_national_team6_and_Real_MU_clubs':True,'unrelated_cards_skills_level_preserved':True,'SQL_and_config_rollback_after_partial_replace':True,'wire_projection_zero_SQL':True,'Android_tested':False},indent=2));print('PROFILE_STORAGE_PASS')
