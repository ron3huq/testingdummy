from pathlib import Path
import sys,json,zlib,base64,hashlib,sqlite3,copy,types,time
P=Path('/tmp/73-ui79');T=P/'build/payload/work/tools';sys.path.insert(0,str(T));sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');import custom_skin as cs
from iostore import Toc
root=P/'rgb-test';profiles={'105647605587130':{'rgb':'123456'}};start=time.monotonic();doc=cs.prepare(root,profiles);first=time.monotonic()-start
for colour,slot in doc['slots'].items():
 toc=Toc(str(root/'livedata'/(doc['stem']+'.utoc')))
 for part in ['Skin','Body','Lowbody']:
  row=cs.templates()['slots'][str(slot)][part];data=toc.read(toc.files[row['path']]);source=cs.source(part);edited=cs.tint(source,colour,cs.templates()['source'][part]['reference']);actual=b''.join(data[pos:pos+n]for pos,n,w,h in row['spans']);assert actual==edited and actual[3::4]==source[3::4]
start=time.monotonic();again=cs.prepare(root,profiles);cache=time.monotonic()-start;assert again==doc
cs.activate(root,profiles,doc);v={'version_file':json.dumps({'version':1234,'dt880':[]}), 'livedata_list':[]};a=cs.advertise(v,8085);assert cs.advertise(a,8085)==a
for row in a['livedata_list']:
 p=root/'livedata'/row['url'].split('/')[-1];assert p.stat().st_size==row['size']
try:cs.colour('#4e5b3700');raise AssertionError('alpha accepted')
except ValueError:pass
assert cs.effective({'106754901843130':{'rgb':None}})=={}
try:cs.effective({str(i):{'rgb':f'{i:06x}'}for i in range(65)});raise AssertionError('65colours accepted')
except ValueError:pass
# Exercise real appearance persistence with an isolated SQLite and native config. No player/user data is used.
import appearance_choices as ac,body_dimensions as body,myleague_editor_runtime as editor
root2=P/'appearance-test';cfgpath=root2/'work/tools/myleague_editor.json';cfgpath.parent.mkdir(parents=True,exist_ok=True)
cfg=json.loads((T/'myleague_editor.json').read_text());cfgpath.write_text(json.dumps(cfg));editor.PATH=cfgpath;body.ROOT=root2
conn=sqlite3.connect(':memory:');conn.executescript('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);CREATE TABLE gameplayers(id TEXT,serial INT,json TEXT);')
pid='106754901843130';p={'gameplayer_id':{'id':int(pid),'serial':42},'parameters':[70]*147};p['parameters'][59]=0;p['parameters'][60]=0
conn.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,42,json.dumps(p)));conn.commit();body.engine_loaded=lambda:False;body.owned=lambda c,r:(pid,json.loads(c.execute('SELECT json FROM gameplayers WHERE serial=?',(r['serial'],)).fetchone()[0]));ac._conn=None
req={'id':pid,'serial':42,'values':{'59':0,'60':0,'rgb':'abcdef'}};assert ac.manage(conn,'ui78_appearance_apply',req)['saved'];saved=json.loads(conn.execute('SELECT value FROM meta WHERE key=?',(ac.KEY,)).fetchone()[0]);assert saved[pid]['rgb']=='abcdef';assert cs.effective(saved)[pid]=='abcdef';assert ac.manage(conn,'ui78_appearance_get',{'serial':42})['rgb']=='abcdef'
oldcfg=cfgpath.read_bytes();oldsql=conn.execute('SELECT value FROM meta WHERE key=?',(ac.KEY,)).fetchone()[0];selected=cs._selected
original=ac.write_config
ac.write_config=lambda data:(_ for _ in ()).throw(RuntimeError('Simulated disk/config failure'))
try:ac.manage(conn,'ui78_appearance_apply',{'id':pid,'serial':42,'values':{'59':0,'60':0,'rgb':'112233'}});raise AssertionError('failure ignored')
except RuntimeError as e:assert str(e)=='Simulated disk/config failure'
finally:ac.write_config=original
assert cfgpath.read_bytes()==oldcfg and conn.execute('SELECT value FROM meta WHERE key=?',(ac.KEY,)).fetchone()[0]==oldsql and cs._selected is selected
ac._conn=None;ac.load(conn);assert ac.profiles[pid]['rgb']=='abcdef';assert cs.effective(ac.profiles)[pid]=='abcdef'
report={'passed':True,'all3_texture_families_all_mips_readback':True,'all_alpha_bytes_unchanged':True,'Hulk_default':'#4e5b37','two_colours_one_private_container':True,'manifest_advertisement_idempotent':True,'RGB_saves_and_reloads_from_SQL':True,'SQL_and_config_rollback_on_failed_save':True,'custom_RGB_alpha_input_rejected':True,'distinct_colour_limit':64,'first_build_host_ms':round(first*1000,1),'cached_verify_host_ms':round(cache*1000,1),'phone_tested':False}
(P/'rgb-validation.json').write_text(json.dumps(report,indent=2));print('RGB_PASS',report)
