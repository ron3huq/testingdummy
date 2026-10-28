"""Native team snapshots and exact scoped roster edits; no fabricated current formations."""
from pathlib import Path
import json,gzip,functools,copy,hashlib,threading,ctypes as C
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui712_transfer';profiles={};_conn=None;_lock=threading.RLock();_capture_key=None;_captures={};_preloaded=False;_preload_index=0
@functools.lru_cache(maxsize=1)
def catalog():return json.loads(gzip.decompress(Path(__file__).with_name('transfer_catalog.json.gz').read_bytes()))
@functools.lru_cache(maxsize=1)
def team_names():return {r['id']:r['name']for r in catalog()['teams']}
def key(tid,cid):return str(cid)+':'+str(tid)
def integer(x,lo,hi):return editor.integer(x,lo,hi)
def identity(req):
 tid=integer(req.get('team_id'),1,262143);cid=integer(req.get('competition',0),0,1000)
 group=next((r for r in catalog()['leagues']if r['id']==cid),None)
 if group is None or tid not in group['teams']:raise ValueError('Team does not belong to the selected competition')
 return tid,cid

def captures():
 global _capture_key,_captures
 path=Path(__file__).with_name('myleague-live-teams.json')
 try:stamp=(path.stat().st_mtime_ns,path.stat().st_size)
 except OSError:return _captures
 if stamp==_capture_key:return _captures
 d=json.loads(path.read_text());from myleague_team_snapshot import ENGINE_SHA
 if d.get('schema')!=1 or d.get('engine_sha256')!=ENGINE_SHA or not isinstance(d.get('teams'),list)or len(d['teams'])>1024:raise ValueError('Native snapshot identity mismatch')
 rows={}
 for r in d['teams']:
  try:validate_team(r);rows[key(r['team_id'],r['competition'])]=r
  except (ValueError,KeyError,TypeError):continue
 _capture_key=stamp;_captures=rows;return rows

@functools.lru_cache(maxsize=1)
def valid_players():
 import motion_editor
 valid=set(motion_editor.donors())
 for ids in catalog()['base_rosters'].values():valid.update(map(str,ids))
 valid.update(str(p['player_id'])for row in __import__('myleague_worlds').config()['classic_teams'].values()for p in row['slots'])
 return valid

def validate_team(row):
 cfg=copy.deepcopy(editor.DEFAULT);cfg['teams']=[row];editor.validate(cfg)
 valid=valid_players()
 if any(p['id']not in valid for p in row['roster']):raise ValueError('Roster references a missing native card')
 return row

def classic(tid,cid):
 import myleague_worlds
 d=myleague_worlds.config()['classic_teams'].get(str(tid))
 if not d or d.get('competition',518)!=cid:return None
 roster=[]
 for i,p in enumerate(d['slots']):
  role,x,y=d['formation'][i]if i<11 else(p['source_primary_role']if p['source_primary_role']is not None else {r['name']:r['id']for r in catalog()['roles']}[p['role']],0,0);roster.append({'id':str(p['player_id']),'shirt':p['shirt'],'role':role,'x':x,'y':y})
 ids=[p['id']for p in roster];row={'team_id':tid,'competition':cid,'name':d['name'],'roster':roster,'captain':ids[d['responsibilities']['captain']],'kickers':[ids[i]if i!=255 else None for i in d['set_piece_taker']],'source':'VERIFIED_COMPILED_NATIVE_CLASSIC_PLAN','verified_formation':True};validate_team(row);return row

def source(tid,cid):
 exact=profiles.get(key(tid,cid));global_row=profiles.get(key(tid,0));native=captures();row=exact or global_row or native.get(key(tid,cid))or classic(tid,cid)or native.get(key(tid,0))
 if not row:return None
 row=copy.deepcopy(row);row['team_id']=tid;row['competition']=cid
 # Bench primary roles come from canonical native Player records, not guessed positions.
 if not row.get('ui712_transfer'):
  import motion_editor
  for p in row['roster'][11:]:p['role']=catalog()['positions'].get(p['id'],motion_editor.donors().get(p['id'],{}).get('role',p.get('role',0)))
 return row

def revision(row):return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def display(row):
 import motion_editor,editor_names
 out=copy.deepcopy(row);out['revision']=revision(row);out['name']=team_names().get(row['team_id'],row.get('name','Team'))
 classic_names={str(p['player_id']):p['name']for row in __import__('myleague_worlds').config()['classic_teams'].values()for p in row['slots']}
 for p in out['roster']:p['name']=editor_names.NAMES.get(p['id'],classic_names.get(p['id'],motion_editor.donors().get(p['id'],{}).get('name',p['id'])))
 return out

def load(c):
 global profiles,_conn
 if c is _conn:return
 r=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(r[0])if r else{}
 if not isinstance(profiles,dict)or len(profiles)>128:raise ValueError('Invalid team editor profiles')
 for k,row in profiles.items():validate_team(row)
 _conn=c

def kit_choices(tid):
 import team_kits,myleague_worlds
 alias=myleague_worlds.config().get('kit_aliases',{}).get(str(tid),tid);ids=team_kits._ui712_original(tid)if hasattr(team_kits,'_ui712_original')else team_kits.uniform_ids(tid)
 if alias!=tid:ids=[int(alias)*16384+i for i in range(2)]
 return [ids[i]if i<len(ids)else None for i in range(4)]
def validate_kits(row):
 values=row.get('kits')
 if values is None:return
 if not isinstance(values,list)or len(values)!=4:raise ValueError('Four kit slots required')
 import team_kits,myleague_worlds
 known=team_names();virtual=set(map(int,myleague_worlds.config()['kit_aliases'].values()))
 for uid in values:
  if uid is None:continue
  integer(uid,1,2**32-1);tid,slot=uid//16384,uid%16384
  if tid not in known and tid not in virtual:raise ValueError('Unknown uniform team')
  if slot>15:raise ValueError('Invalid native uniform slot')
  available=(team_kits._ui712_original(tid)if hasattr(team_kits,'_ui712_original')else team_kits.uniform_ids(tid))if tid not in virtual else[tid*16384,tid*16384+1]
  if uid not in available:raise ValueError('The selected team has no native kit in that slot')

def save(c,changes):
 global profiles
 if body.engine_loaded():raise ValueError('Close and reopen the app; edit before Enter Game. Changes take effect on the next game launch')
 if c.in_transaction:raise ValueError('Another save operation is active')
 updated=copy.deepcopy(profiles);cfg=json.loads(editor.PATH.read_text());before=editor.PATH.read_bytes()
 for req in changes:
  tid,cid=identity(req);current=source(tid,cid)
  if current is None:raise ValueError('No native formation snapshot. Enter the game once, then reopen the app and return to Transfer')
  if req.get('revision')!=revision(current):raise ValueError('Team changed; reload the team before saving')
  row=copy.deepcopy(req['team']);row['team_id']=tid;row['competition']=cid;row.pop('revision',None)
  for p in row['roster']:p.pop('name',None)
  row['ui712_transfer']=True;row['source']='USER_EDIT_OF_NATIVE_TEAM';validate_team(row);validate_kits(row);updated[key(tid,cid)]=row
  cfg['teams']=[r for r in cfg['teams']if(r['team_id'],r['competition'])!=(tid,cid)]+[row]
 if len(updated)>128:raise ValueError('Maximum128 simultaneously edited teams')
 editor.validate(cfg)
 try:
  c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));backup=editor.PATH.parents[1]/'backups';backup.mkdir(exist_ok=True);(backup/'ui712-before-transfer.json').write_bytes(before);tmp=editor.PATH.with_suffix('.transfer.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);c.commit()
 except Exception:
  c.rollback();tmp=editor.PATH.with_suffix('.transfer.rollback');tmp.write_bytes(before);tmp.replace(editor.PATH);editor._config=None;raise
 profiles=updated;editor._config=None;return {'saved':True,'teams':len(changes)}

def manage(c,action,req):
 with _lock,body._lock:
  load(c)
  if action=='ui712_transfer_list':
   cid=req.get('competition',0);group=next((r for r in catalog()['leagues']if r['id']==cid),None)
   if group is None:raise ValueError('Unknown competition')
   native_rows=captures();classic_rows=__import__('myleague_worlds').config()['classic_teams']
   q=__import__('motion_editor').fold(str(req.get('query','')))[:80];rows=[{'id':tid,'name':team_names().get(tid,'Team '+str(tid)),'edited':key(tid,cid)in profiles,'ready':bool(profiles.get(key(tid,cid))or profiles.get(key(tid,0))or native_rows.get(key(tid,cid))or native_rows.get(key(tid,0))or (str(tid)in classic_rows and classic_rows[str(tid)].get('competition',518)==cid))}for tid in group['teams']if not q or q in __import__('motion_editor').fold(team_names().get(tid,''))or q==str(tid)];return {'teams':rows,'leagues':catalog()['leagues'],'roles':catalog()['roles']}
  tid,cid=identity(req)
  if action=='ui712_transfer_get':
   row=source(tid,cid)
   if row is None:return {'ready':False,'team_id':tid,'name':team_names().get(tid),'reason':'Enter Game once to collect native rosters/formations automatically, then fully close and reopen the app. No lineup is guessed.'}
   out=display(row);out['kits']=row.get('kits',kit_choices(tid));return {'ready':True,'team':out,'roles':catalog()['roles'],'kit_teams':[{'id':t,'name':n}for t,n in team_names().items()]}
  if action=='ui712_transfer_kits':
   donor=integer(req.get('donor'),1,262143);ids=kit_choices(donor);return {'kits':[{'id':uid,'label':team_names().get(donor,'Team')+' · '+('Home'if i==0 else'Away'if i==1 else'Slot'+str(i+1))}for i,uid in enumerate(ids)if uid is not None]}
  if action=='ui712_transfer_save':return save(c,[req])
  if action=='ui712_transfer_move':
   src=source(tid,cid);other={'team_id':req.get('target_team'),'competition':cid};dest_id,_=identity(other);dest=source(dest_id,cid)
   if src is None or dest is None or tid==dest_id:raise ValueError('Choose two teams with native snapshots')
   pid=str(req.get('player_id'));index=next((i for i,p in enumerate(src['roster'])if p['id']==pid),-1)
   if index<11:raise ValueError('Move the player to the bench first, so the starting formation stays intact')
   if len(src['roster'])<=11 or len(dest['roster'])>=40 or any(p['id']==pid for p in dest['roster']):raise ValueError('Transfer violates roster size or duplicates a card')
   from_rev=req.get('revision');to_rev=req.get('target_revision')
   p=src['roster'].pop(index);used={r['shirt']for r in dest['roster']}
   if p['shirt']in used:p['shirt']=next(i for i in range(1,100)if i not in used)
   p['x']=p['y']=0;dest['roster'].append(p)
   if src['captain']==pid:src['captain']=None
   src['kickers']=[None if x==pid else x for x in src['kickers']]
   return save(c,[dict(req,revision=from_rev,team=src),dict(other,revision=to_rev,team=dest)])
  raise ValueError('Unknown transfer action')

def preload(hook):
 # Bounded background batches. Do not scan835 teams in one CPU burst during play.
 global _preloaded,_preload_index
 if _preloaded:return
 import time
 hook.editor_capture_stock_team.argtypes=[C.c_uint];hook.editor_capture_stock_team.restype=C.c_uint
 preferred=list(dict.fromkeys(tid for league in catalog()['leagues']if league['id']for tid in league['teams']));ids=preferred+[r['id']for r in catalog()['teams']if r['id']not in preferred]
 if not ids or hook.environment_status(0)!=0:return
 start=time.perf_counter();n=0
 while _preload_index<len(ids)and n<32:
  ok=hook.editor_capture_stock_team(ids[_preload_index])
  if not ok and _preload_index==0:return
  _preload_index+=1;n+=1
  if time.perf_counter()-start>.008:break
 _preloaded=_preload_index>=len(ids)

def configure(hook):
 hook.editor_kit_add.argtypes=[C.c_uint]*4;hook.editor_kit_add.restype=C.c_uint
 for row in profiles.values():
  for slot,uid in enumerate(row.get('kits',[])):
   if uid is not None and hook.editor_kit_add(row['team_id'],row['competition'],slot,uid)!=1:raise ValueError('Native kit slot rejected')
 hook.editor_kit_commit.argtypes=[];hook.editor_kit_commit.restype=None;hook.editor_kit_commit()

def install(module):
 if getattr(module.manage,'_ui712_transfer',False):return
 load(module._logic.conn);old=module.manage
 @functools.wraps(old)
 def wrapper(action,payload=''):
  if action.startswith('ui712_transfer_'):return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')),ensure_ascii=False)
  return old(action,payload)
 wrapper._ui712_transfer=True;module.manage=wrapper
 import team_kits
 team_kits._ui712_original=team_kits.uniform_ids
 def kits(tid):
  import select_team_runtime
  cid=select_team_runtime.editor_context();row=profiles.get(key(tid,cid))or profiles.get(key(tid,0))
  if row and row.get('kits'):
   values=[uid for uid in row['kits']if uid is not None]
   if values:return list(dict.fromkeys(values))
  return team_kits._ui712_original(tid)
 team_kits.uniform_ids=kits

def post_install():
 import select_team_runtime as native,ziru_data,myleague_worlds
 if getattr(native.activate_context,'_ui712_transfer',False):return
 old=native.activate_context;base=copy.deepcopy(catalog()['base_rosters']);base.update({str(k):list(v)for k,v in myleague_worlds.config()['native_rosters'].items()})
 def activate(cid):
  result=old(cid);rows={k:list(v)for k,v in base.items()}
  for scope in (0,int(cid)):
   for row in profiles.values():
    if row['competition']==scope:rows[str(row['team_id'])]=[int(p['id'])for p in row['roster']]
  target=ziru_data.rosters();target.clear();target.update(rows);return result
 activate._ui712_transfer=True;native.activate_context=activate
