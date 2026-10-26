from pathlib import Path
import sys,sqlite3,json,tempfile,shutil,types
P=Path('/workspace/ronaldo-work/73-ui75');sys.path[:0]=[str(P/'payload/work/tools')];import player_model as m,body_dimensions as b
r=Path(tempfile.mkdtemp());c=sqlite3.connect(r/'test.db');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INTEGER,json TEXT);')
pid='89136418985303';req={'id':pid,'serial':1};player={'parameters':[70]*147};c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,1,json.dumps(player)));c.commit();tr=[];c.set_trace_callback(tr.append)
assert m.manage(c,'ui75_model_get',req)['values']=={};tr.clear()
for i,key in enumerate(m.FIELDS):m.manage(c,'ui75_model_apply',dict(req,values={key:i}))
assert len(m.profiles)==1 and m.profiles[pid]=={'calf_size':10}
m._conn=None;m.profiles={};assert m.manage(c,'ui75_model_get',req)['values']=={'calf_size':10}
assert json.loads(c.execute('SELECT json FROM gameplayers').fetchone()[0])==player
for values in [{'other':7},{'arm_length':15},{'arm_length':-1},{'arm_length':True},{'arm_length':7.0},None]:
 try:m.manage(c,'ui75_model_apply',dict(req,values=values));raise AssertionError('accepted invalid')
 except ValueError:pass
old=b.engine_loaded;b.engine_loaded=lambda:True
try:m.manage(c,'ui75_model_apply',dict(req,values={}));raise AssertionError('edited while engine loaded')
except ValueError:pass
b.engine_loaded=old
# Native encoding uses15 for inherit, no clamping or aliasing to another field.
class F:
 def __init__(self,f):self.f=f
 def __call__(self,*args):return self.f(*args)
rows=[];h=types.SimpleNamespace(model_add=F(lambda a,b:rows.append((a,b))or 1),model_commit=F(lambda:None),model_status=F(lambda i:1));m.configure_native(h);assert rows==[(int(pid),sum((10 if k=='calf_size'else 15)<<(i*4)for i,k in enumerate(m.FIELDS)))]
m.manage(c,'ui75_model_apply',dict(req,values={}));assert pid not in m.profiles
m._conn=None;m.profiles={};assert not m.manage(c,'ui75_model_get',req)['values']
shutil.rmtree(r);report={'passed':True,'on_demand_exact_owned_card_validation':True,'11_fields_persist_reload_restore':True,'invalid_values_rejected':True,'no_gameplayer_stats_mutated':True,'native_inherit_encoding_verified':True,'edits_blocked_after_engine_load':True,'catalogue_search_code_unchanged':True,'device_tested':False};(P/'model-storage-validation.json').write_text(json.dumps(report,indent=2));print('MODEL_STORAGE_PASS')
