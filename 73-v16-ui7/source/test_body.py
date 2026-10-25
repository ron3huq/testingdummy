from pathlib import Path
import sys,sqlite3,json,copy,tempfile,types
P=Path('/workspace/ronaldo-work/73-ui7');sys.path.insert(0,str(P/'payload/work/tools'))
import body_dimensions as b,myleague_editor_runtime as e
root=Path(tempfile.mkdtemp(prefix='ui7-body-'));b.ROOT=root;t=root/'work/tools';t.mkdir(parents=True);e.PATH=t/'myleague_editor.json';e.PATH.write_text(json.dumps(e.DEFAULT));c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INTEGER,json TEXT,PRIMARY KEY(id,serial));')
pid='89136418985303';p={'parameters':[70]*147,'_careerplan_base_parameters':[60]*147,'progression':[1,2,3],'boosters':[49],'skills':[1,4],'name':'Kaká'};p['parameters'][47:49]=[187,83];old=copy.deepcopy(p)
for serial in[1,2]:c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,serial,json.dumps(p)))
c.commit();tr=[];c.set_trace_callback(tr.append);req={'id':pid,'serial':1};assert b.get(c,req)=={'height':187,'weight':83};assert len(tr)==2;tr.clear();b.get(c,req);assert len(tr)==1
b.apply(c,dict(req,height=190,weight=88));after=json.loads(c.execute('SELECT json FROM gameplayers WHERE serial=1').fetchone()[0]);expected=copy.deepcopy(old)
for k in['parameters','_careerplan_base_parameters']:expected[k][47:49]=[190,88]
assert after==expected;assert json.loads(c.execute('SELECT json FROM gameplayers WHERE serial=2').fetchone()[0])==old
cfg=json.loads(e.PATH.read_text());e.validate(cfg);assert cfg['players'][0]['parameters']=={'47':190,'48':88}and cfg['players'][0]['ui7_body']
v={'gameplayer_id':{'id':pid},'parameters':[1]*147};tr.clear();out=b.project(v);assert out['parameters'][47:49]==[190,88]and v['parameters']==[1]*147 and not tr;assert b.project({'id':'123','parameters':[1]*147})['parameters']==[1]*147
for h,w in[(139,88),(221,88),(190,39),(190,131),(True,80),(190,80.0)]:
 try:b.apply(c,dict(req,height=h,weight=w));raise AssertionError('invalid accepted')
 except ValueError:pass
for bad in[dict(req,serial=3),dict(req,serial=True),dict(req,id='x')]:
 try:b.get(c,bad);raise AssertionError('invalid owner accepted')
 except ValueError:pass
saved=c.execute('SELECT json FROM gameplayers WHERE serial=1').fetchone()[0];before=e.PATH.read_bytes();original=b.write_config
def fail(data):original(data);raise OSError('simulated write failure')
b.write_config=fail
try:b.apply(c,dict(req,height=200,weight=95));raise AssertionError('failure not raised')
except OSError:pass
b.write_config=original;assert e.PATH.read_bytes()==before and c.execute('SELECT json FROM gameplayers WHERE serial=1').fetchone()[0]==saved and b.get(c,req)=={'height':190,'weight':88}
loaded=b.engine_loaded;b.engine_loaded=lambda:True
try:b.apply(c,dict(req,height=200,weight=95));raise AssertionError('in game edit accepted')
except ValueError:pass
b.engine_loaded=loaded
# persisted dimensions restore after process restart; wire hooks have zero SQL.
b._loaded_conn=None;b.profiles={};b.load(c);assert b.get(c,req)=={'height':190,'weight':88};b.write_config(b.profiles)
# Existing startup skill migration must preserve dimensions + sleeves + accessories.
(t/'ui2_skill_rules.json').write_bytes((P/'payload/work/tools/ui2_skill_rules.json').read_bytes());import card_rules
card_rules.install_native_config(root);rows=json.loads(e.PATH.read_text())['players'];r=next(r for r in rows if r['id']==pid);assert r['parameters']['47']==190 and r['parameters']['48']==88 and r['sleeve']=='long'
# Verify routing and editor cache invalidation through production wrappers.
import editor_fast
calls=[];module=types.SimpleNamespace(_logic=types.SimpleNamespace(conn=c),manage=lambda action,payload='':(calls.append(action)or'{"players":[]}'))
club=types.ModuleType('club_store');club.wire_player=lambda value:value;sys.modules['club_store']=club
assert b.install(root,module);assert not b.install(root,module);assert editor_fast.install(module)
module.manage('editor_list');module.manage('editor_list');assert calls.count('editor_list')==1
assert json.loads(module.manage('ui7_body_get',json.dumps(req)))['height']==190
module.manage('ui7_body_apply',json.dumps(dict(req,height=191,weight=89)))
module.manage('editor_list');assert calls.count('editor_list')==2
tr.clear();assert club.wire_player(v)['parameters'][47:49]==[191,89]and not tr
report={'passed':True,'checks':['only parameters47/48 and matching career base changed; progression/skills/boosters intact','selected SQL card instance only; exact64 ID lookup','indexed read: first2 SQL, repeated1 SQL; wire projection zero SQL','strict bounds and owned-card validation','SQL/config rollback on injected write failure','edit blocked while engine loaded','dimensions persist and survive startup skill migration'],'device_tested':False};(P/'body-validation.json').write_text(json.dumps(report,indent=2));print('BODY_PASS',report)
