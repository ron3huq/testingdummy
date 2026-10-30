"""Exact-card celebration and native body-palette settings; cached after startup."""
import json,functools,threading,ctypes as C,zlib,sqlite3
from pathlib import Path
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui78_appearance_choices';profiles={};_conn=None;_lock=threading.RLock();_keep=[];_chain=None
@functools.lru_cache(maxsize=1)
def choices():return json.loads(Path(__file__).with_name('celebration_choices.json').read_text())
@functools.lru_cache(maxsize=1)
def skin_previews():return json.loads(Path(__file__).with_name('native_skin_previews.json').read_text())
@functools.lru_cache(maxsize=1)
def defaults():return json.loads(zlib.decompress(Path(__file__).with_name('body_defaults.zlib').read_bytes()))
def baseline(pid):return defaults().get(pid)or defaults().get(str(int(pid)&262143))
def validate(v):
 if not isinstance(v,dict)or set(v)-{'59','60','skin'}:raise ValueError('Invalid appearance settings')
 for k,value in v.items():
  if k=='skin':
   if type(value)is not int or not 1<=value<=6:raise ValueError('Native palette must be1–6')
  elif type(value)is not int or value not in {r['id']for r in choices()[k]}:raise ValueError('Celebration ID is not present in this73 database')
 return v

def migrate(root,conn):
 """Repair UI7.7 extreme saved measurements before strict config validation."""
 path=Path(root)/'work/tools/myleague_editor.json';cfg=json.loads(path.read_text());raw=conn.execute('SELECT value FROM meta WHERE key=?',(body.KEY,)).fetchone();data=json.loads(raw[0])if raw else{};updates={}
 for pid,v in data.items():
  body.identity(pid);h,w=v['height'],v['weight']
  if 140<=h<=220 and 40<=w<=130:continue
  base=baseline(pid)
  if not base:raise ValueError('Cannot restore original measurements for '+pid)
  new={'height':h if 140<=h<=220 else base[0],'weight':w if 40<=w<=130 else base[1]}
  body.validate_values(new)
  if new!=v:data[pid]=new;updates[pid]=new
 changed=False
 for row in cfg['players']:
  p=row.get('parameters',{});base=None
  for key,low,high,at in [('47',140,220,0),('48',40,130,1)]:
   if key in p and not low<=p[key]<=high:
    base=base or baseline(row['id'])
    if not base:raise ValueError('Cannot restore original measurements for '+row['id'])
    p[key]=base[at];changed=True
 if not updates and not changed:return
 backup=Path(root)/'backups/ui78-measurements-before.sqlite3';backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():
  dest=sqlite3.connect(backup)
  try:conn.backup(dest)
  finally:dest.close()
 before=path.read_bytes()
 try:
  conn.execute('BEGIN IMMEDIATE')
  for pid,v in updates.items():
   for serial,encoded in conn.execute('SELECT serial,json FROM gameplayers WHERE id=?',(pid,)).fetchall():
    player=json.loads(encoded)
    for key in ['parameters','_careerplan_base_parameters']:
     p=player.get(key)
     if isinstance(p,list)and len(p)==147:p[47]=v['height'];p[48]=v['weight']
    conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(player,separators=(',',':')),pid,serial))
  conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(body.KEY,json.dumps(data)))
  tmp=path.with_suffix('.ui78-migrate.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(path);conn.commit()
 except Exception:
  conn.rollback();path.write_bytes(before);raise
 body._loaded_conn=None;editor._config=None

def load(conn):
 global _conn,profiles
 if conn is _conn:return
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(row[0])if row else{}
 if not isinstance(profiles,dict)or len(profiles)>1024:raise ValueError('Invalid appearance profiles')
 for pid,v in profiles.items():body.identity(pid);validate(v)
 _conn=conn

def write_config(data):
 cfg=json.loads(editor.PATH.read_text())
 for pid,v in data.items():
  row=next((r for r in cfg['players']if r['id']==pid and r['competition']==0),None)
  if row is None:row={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(row)
  for key in ['59','60']:row['parameters'].pop(key,None)
  row['parameters'].update({k:val for k,val in v.items()if k not in ['skin','rgb']})
 editor.validate(cfg);tmp=editor.PATH.with_suffix('.ui78.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);editor._config=None

def manage(conn,action,req):
 global profiles
 with _lock,body._lock:
  load(conn);pid,player=body.owned(conn,req);p=player['parameters']
  if action.endswith('_get'):
   current=profiles.get(pid,{})
   return {'skin':current.get('skin',0),'59':current.get('59',p[59]),'60':current.get('60',p[60]),'choices':choices()if req.get('section')!='skin'else{},'skin_palettes':[1,2,3,4,5,6],'skin_previews':skin_previews(),'skin_scope':'native_body_palettes_only','custom_rgb_supported':False}
  values=validate(req.get('values'))
  if body.engine_loaded():raise ValueError('Close and reopen the app, then edit before entering the game')
  if conn.in_transaction:raise ValueError('Another save operation is active')
  updated=dict(profiles);updated[pid]=values
  if len(updated)>1024:raise ValueError('Maximum1024 appearance profiles')
  for key in ['parameters','_careerplan_base_parameters']:
   if isinstance(player.get(key),list)and len(player[key])==147:
    for k,v in values.items():
     if k not in ['skin','rgb']:player[key][int(k)]=v
  before=editor.PATH.read_bytes()
  try:
   conn.execute('BEGIN IMMEDIATE');conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(player,separators=(',',':')),pid,req['serial']));conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));write_config(updated);conn.commit()
  except Exception:
   conn.rollback();tmp=editor.PATH.with_suffix('.rollback.tmp');tmp.write_bytes(before);tmp.replace(editor.PATH);editor._config=None;raise
  profiles=updated;return {'saved':True,'card_id':pid,'values':values}

def project(v):
 pid=str((v.get('gameplayer_id')or{}).get('id',v.get('id','')));row=profiles.get(pid)
 if not row or len(v.get('parameters',[]))!=147:return v
 out=dict(v);p=list(v['parameters'])
 for k,val in row.items():
  if k not in ['skin','rgb']:p[int(k)]=val
 out['parameters']=p;return out

def install(module):
 if getattr(module.manage,'_ui78_appearance',False):return False
 retire_custom_rgb(module._logic.conn)
 load(module._logic.conn)
 if profiles:write_config(profiles)
 original=module.manage
 @functools.wraps(original)
 def wrapped(action,payload=''):
  if action in ['ui78_appearance_get','ui78_appearance_apply']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')))
  return original(action,payload)
 wrapped._ui78_appearance=True;module.manage=wrapped
 import club_store
 old=club_store.wire_player
 @functools.wraps(old)
 def wire(*a,**k):return project(old(*a,**k))
 club_store.wire_player=wire

def configure_skin_chain(noodle,base,trampoline):
 """Reuse the already installed native bake entry: no extra trampoline or Python frame callbacks."""
 global _chain
 if _chain==(base,trampoline):return
 from mod_integrity import digest
 import select_team_runtime as rt
 path=Path(__file__).with_name('libselect_team.so')
 if digest(path)!=rt.HOOK_SHA:raise ValueError('Skin library hash mismatch')
 hook=C.CDLL(str(path));hook.skin_add.argtypes=[C.c_uint64,C.c_uint];hook.skin_add.restype=C.c_uint
 for pid,v in profiles.items():
  if v.get('skin')and hook.skin_add(int(pid),v['skin'])!=1:raise ValueError('Native skin profile rejected')
 hook.skin_commit.argtypes=[];hook.skin_commit.restype=None;hook.skin_commit();hook.configure_skin_bake.argtypes=[C.c_size_t,C.c_size_t];hook.configure_skin_bake.restype=None;hook.configure_skin_bake(base,trampoline)
 noodle.configure_bake.argtypes=[C.c_size_t,C.c_size_t];noodle.configure_bake(base,C.cast(hook.skin_bake_hook,C.c_void_p).value);_keep.append(hook);_chain=(base,trampoline)


def retire_custom_rgb(conn):
 """Retain an exact backup before dropping retired RGB settings; native palettes and motions survive."""
 global _conn
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone()
 if not row:return False
 data=json.loads(row[0])
 if not any('rgb'in v for v in data.values()):return False
 if conn.in_transaction:raise ValueError('Save operation active during RGB migration')
 backup=Path(body.ROOT)/'backups/ui710-before-remove-rgb.sqlite3';backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():
  dest=sqlite3.connect(backup)
  try:conn.backup(dest)
  finally:dest.close()
 clean={pid:{k:v for k,v in profile.items()if k!='rgb'}for pid,profile in data.items()}
 try:
  conn.execute('BEGIN IMMEDIATE');conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(clean,separators=(',',':'))));conn.commit()
 except Exception:conn.rollback();raise
 _conn=None;return True
