"""On-demand exact-card body proportions; no catalogue processing or SQL in match hooks."""
import json,threading,functools,ctypes as C,zlib
from pathlib import Path
@functools.lru_cache(maxsize=1)
def baseline_rows():return json.loads(zlib.decompress(Path(__file__).with_name("player_model_baselines.json.gz").read_bytes()))
inherited={}
def baseline(pid):
 if pid in inherited:return dict(inherited[pid])
 rows=baseline_rows();raw=rows.get(pid)or rows.get(str(int(pid)&262143))
 if raw is None:return {}
 b=bytes.fromhex(raw);nibbles=[7,3,0,4,1,2,10,8,5,6,9]
 return {key:((b[n//2]>>((n%2)*4))&15)for key,n in zip(FIELDS,nibbles)}
FIELDS=('arm_length','shoulder_width','neck_length','chest','neck_size','shoulder_height','leg_length','thigh_size','waist_size','arm_size','calf_size')
KEY='ui75_player_model_v1';profiles={};_lock=threading.RLock();_conn=None;_module=None

def validate(values):
 if not isinstance(values,dict)or set(values)-set(FIELDS):raise ValueError('Invalid player model fields')
 if any(type(v)is not int or not 0<=v<=14 for v in values.values()):raise ValueError('Body proportions must be integers from0 to14')
 return values

def load(conn):
 global profiles,_conn
 if conn is _conn:return
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();data=json.loads(row[0])if row else{}
 if not isinstance(data,dict)or len(data)>1024:raise ValueError('Invalid saved player model profiles')
 import body_dimensions as body
 for pid,value in data.items():body.identity(pid);validate(value)
 profiles=data;_conn=conn

def manage(conn,action,req):
 global profiles
 import body_dimensions as body
 with _lock:
  load(conn);pid,_=body.owned(conn,req)
  if action=='ui75_model_get':
   current=dict(baseline(pid));current.update(inherited.get(pid,{}))
   return {'values':profiles.get(pid,{}),'baseline':current,'fields':list(FIELDS),'minimum':0,'maximum':14,'copied_model':pid in inherited}
  values=validate(req.get('values'))
  if body.engine_loaded():raise ValueError('Close and reopen the app, then edit before entering the game')
  if conn.in_transaction:raise ValueError('Another save operation is active; try again')
  updated=dict(profiles)
  if values:updated[pid]=dict(values)
  else:updated.pop(pid,None)
  if len(updated)>1024:raise ValueError('Maximum1024 custom model profiles')
  try:
   conn.execute('BEGIN IMMEDIATE');conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));conn.commit()
  except Exception:conn.rollback();raise
  profiles=updated;return {'saved':True,'card_id':pid,'values':values}

def configure_native(hook):
 with _lock:
  if _module is not None:load(_module._logic.conn)
  hook.model_add.argtypes=[C.c_uint64,C.c_uint64];hook.model_add.restype=C.c_uint
  hook.model_commit.argtypes=[];hook.model_commit.restype=None
  hook.model_status.argtypes=[C.c_uint];hook.model_status.restype=C.c_uint64
  effective={pid:dict(values)for pid,values in inherited.items()}
  for pid,values in profiles.items():effective[pid]=dict(effective.get(pid,{}),**values)
  for pid,values in effective.items():
   packed=sum(values.get(key,15)<<(i*4)for i,key in enumerate(FIELDS))
   if hook.model_add(int(pid),packed)!=1:raise ValueError('Native model profile rejected')
  hook.model_commit()

def install(module):
 global _module
 if getattr(module.manage,'_ui75_model',False):return False
 load(module._logic.conn);_module=module;original=module.manage
 @functools.wraps(original)
 def wrapped(action,payload=''):
  if action in('ui75_model_get','ui75_model_apply'):return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')))
  return original(action,payload)
 wrapped._ui75_model=True;module.manage=wrapped;return True
