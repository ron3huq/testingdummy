from pathlib import Path
import sys,sqlite3,json,copy,tempfile
P=Path('/tmp/73-ui711');T=P/'build/payload/work/tools';sys.path.insert(0,str(T));import appearance_gear as a,body_dimensions as b,myleague_editor_runtime as e
root=Path(tempfile.mkdtemp(prefix='ui710-gear-',dir='/tmp'));e.PATH=root/'config.json';b.ROOT=root;cfg=json.loads((T/'myleague_editor.json').read_text());e.PATH.write_text(json.dumps(cfg));pid='88044950524330';orig=copy.deepcopy(cfg);c=sqlite3.connect(':memory:');c.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);');c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,1,json.dumps({'parameters':[0]*147})));c.commit();b.engine_loaded=lambda:False;req={'id':pid,'serial':1};a.manage(c,'ui710_equipment_apply',dict(req,values={'background':a.BACKGROUNDS[0]}));after=json.loads(e.PATH.read_text())
for old in orig['players']:
 new=next(r for r in after['players']if(r['id'],r['competition'])==(old['id'],old['competition']));assert new['sleeve']==old['sleeve'];assert new.get('accessories')==old.get('accessories')
assert a.manage(c,'ui710_equipment_apply',dict(req,values={'sleeve':'short','accessories':{'0':2,'1':1,'4':2,'5':1,'6':0,'7':2},'background':0}))['saved'];after=json.loads(e.PATH.read_text());assert all(r['sleeve']=='short'and r['accessories']['4']==2 for r in after['players']if r['id']==pid)
for val in [{'accessories':{'0':2,'1':2}},{'accessories':{'2':2}},{'accessories':{'8':2,'9':2}},{'sleeve':'rolled'},{'background':123},{'accessories':{'4':True}}]:
 try:a.validate(val);raise AssertionError('Invalid choice accepted')
 except ValueError:pass
assert all(r['sleeve']=='short'for r in e.requested_long_sleeves(after)['players']if r['id']==pid)
for style,expected in [('inner',{'8':2,'9':1}),('highneck',{'8':1,'9':2}),('long',{'8':1,'9':1}),('original',{'8':0,'9':0})]:
 a.manage(c,'ui710_equipment_apply',dict(req,section='sleeve',values={'sleeve':style,'socks':'short','accessories':{}}));v=a.manage(c,'ui710_equipment_get',req)['values'];assert v['accessories']==expected and v['socks']=='short'
 cfg=e.requested_long_sleeves(json.loads(e.PATH.read_text()));assert all(r['sleeve']==style for r in cfg['players']if r['id']==pid)
a.manage(c,'ui710_equipment_apply',dict(req,section='accessories',values={'sleeve':'short','accessories':{'8':2,'9':1}}));assert a.profiles[pid]['sleeve']=='inner'
before=e.PATH.read_bytes();sql=c.execute('SELECT value FROM meta WHERE key=?',(a.KEY,)).fetchone()[0];old=a.write_config
def fail(v):old(v);raise OSError('injected write failure')
a.write_config=fail
try:a.manage(c,'ui710_equipment_apply',dict(req,values={'sleeve':'long'}));raise AssertionError('failure not raised')
except OSError:pass
a.write_config=old;assert e.PATH.read_bytes()==before and c.execute('SELECT value FROM meta WHERE key=?',(a.KEY,)).fetchone()[0]==sql
(P/'equipment-validation.json').write_text(json.dumps({'passed':True,'background_does_not_change_sleeve_or_gear':True,'user_sleeve_overrides_all_competition_defaults':True,'eight_audited_accessory_types':[0,1,4,5,6,7,8,9],'native_long_shirt_and_two_undershirt_modes_persist':True,'normal_long_short_socks':True,'GK_gloves_rejected':True,'SQL_config_rollback_verified':True,'device_tested':False},indent=2));print('EQUIPMENT_PERSISTENCE_PASS')
