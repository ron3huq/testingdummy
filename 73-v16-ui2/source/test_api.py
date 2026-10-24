from pathlib import Path
import sys,types,sqlite3,json,time,shutil,hashlib
exec(open('/workspace/ronaldo-work/73-ui/inspect_live.py').read().split("print('APPEARANCE'")[0])
sys.path.insert(0,'/workspace/testingdummy/73-v16-ui2/source')
import editor_names,editor_fast,card_rules,club_store
p=Path('/workspace/ronaldo-work/73-ui2');original=p.parent/'73-ui/save-audit/club.sqlite3';before=hashlib.sha256(original.read_bytes()).hexdigest();shutil.copy2(original,p/'test.sqlite3');c=sqlite3.connect(p/'test.sqlite3')
editor_names.install();assert player_editor.name_index()is player_editor.name_index();card_rules.install()
players_before=c.execute('SELECT id,serial,json FROM gameplayers ORDER BY id,serial').fetchall()
rows=player_editor.players(c);names={r['id']:r['name_en']for r in rows};assert names['88045755960841']=='Nguyen Xuan Son'
for cid in ['89136418985303','89136418985302']:
 row=next(r for r in rows if r['id']==cid);assert 5 not in row['innate_skills']and 62 in row['innate_skills']
 raw=json.loads(c.execute('SELECT json FROM gameplayers WHERE id=?',(cid,)).fetchone()[0]);old=list(raw['parameters']);wire=club_store.wire_player(raw)
 assert wire['parameters'][108]==0 and wire['parameters'][125]==1 and raw['parameters']==old
 for i in range(147):
  if i not in [108,125]:assert wire['parameters'][i]==club_store.wire_player.__wrapped__(raw)['parameters'][i]
raw['gameplayer_id']['id']+=1<<32;assert card_rules.project(raw)is raw
calls=[]
def original_manage(action,path=''):
 calls.append(action)
 return json.dumps(player_editor.dispatch(c,action,path,r))if action.startswith('editor_')else action
m=types.SimpleNamespace(_logic=types.SimpleNamespace(conn=c),manage=original_manage);assert editor_fast.install(m);assert not editor_fast.install(m)
first=m.manage('editor_list','{"summary":true}');start=time.perf_counter();second=m.manage('editor_list','{"summary":true}');cached=time.perf_counter()-start;assert first==second and calls.count('editor_list')==1
c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',('ui2_cache_test','1'));c.commit();m.manage('editor_list','{"summary":true}');assert calls.count('editor_list')==2
other=sqlite3.connect(p/'test.sqlite3');other.execute('UPDATE meta SET value=? WHERE key=?',('2','ui2_cache_test'));other.commit();other.close();m.manage('editor_list','{"summary":true}');assert calls.count('editor_list')==3
m.manage('unrelated');m.manage('editor_list','{"summary":true}');assert calls.count('editor_list')==4
# A restored/closed context must be reopened by the original gateway first.
count=[0];reopening=types.SimpleNamespace(_logic=None)
def reopen(action,path=''):
 count[0]+=1;reopening._logic=types.SimpleNamespace(conn=c);return 'reopened'
reopening.manage=reopen;editor_fast.install(reopening)
assert reopening.manage('editor_list')=='reopened'and reopening.manage('editor_list')=='reopened'and count[0]==1
# Remove persisted Body & motion JSON fields once, preserving the rest of the editor.
root=p/'config-test';tools=root/'work/tools';tools.mkdir(parents=True,exist_ok=True)
shutil.copy2(p/'payload/work/tools/myleague_editor.json',tools/'myleague_editor.json');shutil.copy2(p/'payload/work/tools/ui2_skill_rules.json',tools/'ui2_skill_rules.json')
data=json.loads((tools/'myleague_editor.json').read_text());data['players'].append({'id':'88044950524330','competition':0,'sleeve':'short','parameters':{'43':1,'47':195,'14':93},'accessories':{'7':2}});(tools/'myleague_editor.json').write_text(json.dumps(data))
card_rules.install_native_config(root);changed=json.loads((tools/'myleague_editor.json').read_text());row=next(x for x in changed['players']if x['id']=='88044950524330');assert row['parameters']=={'14':93}and'accessories'not in row
for row in changed['players']:
 if row['id']in card_rules.CARDS:assert row['parameters']['108']==0 and row['parameters']['125']==1
assert changed['teams']==data['teams']and changed['weather']==data['weather']
assert c.execute('SELECT id,serial,json FROM gameplayers ORDER BY id,serial').fetchall()==players_before
assert hashlib.sha256(original.read_bytes()).hexdigest()==before
(p/'api-validation.json').write_text(json.dumps({'passed':True,'cached_owned_read_seconds':cached,'checks':['shared alias index reused, full renamed owned list correct','two full64 card skill replacement in native-style parameters and innate editor display','wire commands preserve other parameters and do not mutate source','cache invalidated by own/external DB writes and other commands','input save and owned-player rows unchanged','no body/motion projection or metadata lookup']},indent=2));print('UI2_API_PASS',cached)
