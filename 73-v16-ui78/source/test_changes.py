from pathlib import Path
import sys,tempfile,sqlite3,json,copy,shutil
P=Path('/workspace/ronaldo-work/73-ui78');sys.path.insert(0,str(P/'payload/work/tools'));import body_dimensions as b,appearance_choices as a,player_tuning as t,myleague_editor_runtime as e
root=Path(tempfile.mkdtemp(prefix='ui78-storage-'));tools=root/'work/tools';tools.mkdir(parents=True);e.PATH=tools/'myleague_editor.json';e.PATH.write_text(json.dumps(e.DEFAULT));b.ROOT=root
c=sqlite3.connect(root/'test.sqlite3');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);CREATE INDEX instances ON gameplayers(id,serial);')
pid='88044950524330';req={'id':pid,'serial':1};params=[0]*147;params[47]=185;params[48]=80;params[70]=1
v={'parameters':params,'_careerplan_base_parameters':list(params),'additional_skill_id':[4,8,74,74,74],'level_info':{'level':10},'other':'keep'};c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,1,json.dumps(v)));c.commit()
# Emulate upgrading a phone which actually saved the excessive UI7.7 dimensions.
c.execute('INSERT INTO meta VALUES(?,?)',(b.KEY,json.dumps({pid:{'height':255,'weight':250}})));cfg=copy.deepcopy(e.DEFAULT);cfg['players']=[{'id':pid,'competition':0,'sleeve':'none','ui7_body':True,'parameters':{'47':255,'48':250}}];e.PATH.write_text(json.dumps(cfg));c.commit();a.migrate(root,c);d=json.loads(c.execute('SELECT value FROM meta WHERE key=?',(b.KEY,)).fetchone()[0]);assert [d[pid]['height'],d[pid]['weight']]==a.baseline(pid)[:2];assert(root/'backups/ui78-measurements-before.sqlite3').exists();b.load(c);b.write_config(b.profiles)
for h,w in [(220,130),(140,40)]:b.apply(c,dict(req,height=h,weight=w))
for h,w in [(255,130),(220,250),(221,130),(220,131)]:
 try:b.apply(c,dict(req,height=h,weight=w));raise AssertionError('Invalid dimension accepted')
 except ValueError:pass
labels=json.loads((P/'payload/work/tools/innate_skill_labels.json').read_text());assert len(labels)==64;assert labels['3']=='Marseille Turn'and labels['8']=='Tap Trick'and labels['62']=='Long-Reach Tackle'and labels['66']=='Aerial Fort'
# Read current actual bits and save by stable native index, preserving Additional Skills.
current=t.get(c,'ui77_skills_get',req);assert current['selected']==[0];assert len(current['choices'])==64
t.apply(c,'ui77_skills_apply',dict(req,selected=[3,8,62,66]));new=json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0]);assert new['additional_skill_id']==v['additional_skill_id']and new['level_info']==v['level_info'];assert all(new['parameters'][flag]==int(i in [3,8,62,66])for i,flag in enumerate(e.FLAGS))
choices=a.choices();assert len(choices['59'])==286 and len(choices['60'])==32;goal=next(r['id']for r in choices['59']if r['id']>200);special=next(r['id']for r in choices['60']if r['id']>10)
a.manage(c,'ui78_appearance_apply',dict(req,values={'59':goal,'60':special,'skin':6}));assert a.manage(c,'ui78_appearance_get',req)['59']==goal;assert a.manage(c,'ui78_appearance_get',dict(req,section='skin'))['choices']=={}
new=json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0]);assert new['parameters'][59:61]==[goal,special];assert new['additional_skill_id']==v['additional_skill_id']
for values in [{'59':542},{'60':595},{'skin':7},{'skin':'#ff0000'},{'rgb':'#ff0000'}]:
 try:a.manage(c,'ui78_appearance_apply',dict(req,values=values));raise AssertionError('Invalid appearance accepted')
 except ValueError:pass
before=e.PATH.read_bytes();saved=c.execute('SELECT json FROM gameplayers').fetchone()[0];old=a.write_config
def fail(data):old(data);raise OSError('injected failure')
a.write_config=fail
try:a.manage(c,'ui78_appearance_apply',dict(req,values={'59':0,'skin':1}));raise AssertionError('Failure missing')
except OSError:pass
a.write_config=old;assert e.PATH.read_bytes()==before and c.execute('SELECT json FROM gameplayers').fetchone()[0]==saved and a.profiles[pid]['skin']==6
trace=[];c.set_trace_callback(trace.append);trace.clear();out=a.project(t.project(b.project({'id':pid,'parameters':[0]*147})));assert not trace;assert out['parameters'][59:61]==[goal,special];assert out['parameters'][125]==1
# Clearing skin restores the original palette path, while keeping the celebration fields.
a.manage(c,'ui78_appearance_apply',dict(req,values={'59':goal,'60':special}));assert a.manage(c,'ui78_appearance_get',req)['skin']==0
assert e.project({'gameplayer_id':{'id':int(pid)},'parameters':new['parameters'],'additional_skill_id':v['additional_skill_id']},122)['additional_skill_id']==v['additional_skill_id']
# Instance ownership is still enforced.
try:a.manage(c,'ui78_appearance_apply',dict(req,serial=999,values={'skin':2}));raise AssertionError('Unowned accepted')
except ValueError:pass
(P/'storage-validation.json').write_text(json.dumps({'passed':True,'old_dimension_bounds_restored':True,'UI77_extremes_migrated_to_original_card_values_with_backup':True,'64_corrected_English_skill_labels':True,'innate_flags_and_additional_slots_independent':True,'celebration_parameters59_60_saved_and_projected':True,'only_observed_celebration_values_accepted':True,'skin_profiles_saved_and_original_reset':True,'custom_RGB_rejected_not_faked':True,'SQL_config_cache_rollback':True,'wire_projection_zero_SQL':True,'ownership_enforced':True,'device_tested':False},indent=2));c.close();shutil.rmtree(root);print('STORAGE_PASS')
