"""On-demand per-card sleeve/accessory choices, using the audited native editor registry."""
import functools,json,threading,ctypes as C
from pathlib import Path
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui710_equipment';profiles={};_conn=None;_lock=threading.RLock()
BACKGROUNDS=[88039313485858,88045755960770,89138019805599,89138288266704,89133456301399,89133724764840,88037702764935]
CHOICES={'0':'Short tights','1':'Long tights','4':'Left wrist tape','5':'Right wrist tape','6':'Ankle tape','7':'Outfield gloves'}
def validate(v):
 if not isinstance(v,dict)or set(v)-{'sleeve','accessories','background'}:raise ValueError('Invalid equipment settings')
 if v.get('sleeve','none')not in ['none','original','short','long']:raise ValueError('Choose original, short or long sleeves')
 if 'background'in v and (type(v['background'])is not int or v['background']not in [0]+BACKGROUNDS):raise ValueError('Unsupported background donor')
 gear=v.get('accessories',{})
 if not isinstance(gear,dict)or set(gear)-set(CHOICES)or any(type(x)is not int or x not in [0,1,2]for x in gear.values()):raise ValueError('Unsupported accessory; goalkeeper gloves are excluded')
 if gear.get('0')==2 and gear.get('1')==2:raise ValueError('Choose short tights or long tights, not both')
 return v

def load(conn):
 global _conn,profiles
 if conn is _conn:return
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(row[0])if row else{}
 if not isinstance(profiles,dict)or len(profiles)>1024:raise ValueError('Invalid equipment profiles')
 for pid,v in profiles.items():body.identity(pid);validate(v)
 _conn=conn

def write_config(data):
 cfg=json.loads(editor.PATH.read_text())
 for pid,v in data.items():
  rows=[r for r in cfg['players']if r['id']==pid]
  if not any(r['competition']==0 for r in rows):
   row={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(row);rows.append(row)
  # A user-selected sleeve takes precedence over bundled competition-specific defaults.
  for row in rows:
   if 'sleeve'in v:row['sleeve']=v['sleeve']
   if 'accessories'in v:row['accessories']=dict(v['accessories'])
 editor.validate(cfg);tmp=editor.PATH.with_suffix('.equipment.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);editor._config=None

def manage(conn,action,req):
 global profiles
 with _lock,body._lock:
  load(conn);pid,player=body.owned(conn,req)
  if action.endswith('_get'):return {'values':profiles.get(pid,{'sleeve':'none','accessories':{}}),'accessory_choices':CHOICES,'modes':['Original','Off','On'],'backgrounds':BACKGROUNDS}
  values=validate(req.get('values'));values=dict(values)
  if 'accessories'in values:
   values['accessories']=dict(values['accessories'])
   if values['accessories'].get('0')==2:values['accessories']['1']=1
   elif values['accessories'].get('1')==2:values['accessories']['0']=1
  if body.engine_loaded():raise ValueError('Reopen the app, then edit before Enter Game')
  if conn.in_transaction:raise ValueError('Another save operation is active')
  updated=dict(profiles);updated[pid]=values
  if len(updated)>1024:raise ValueError('Maximum1024 equipment profiles')
  before=editor.PATH.read_bytes()
  try:
   conn.execute('BEGIN IMMEDIATE');write_config(updated);conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));conn.commit()
  except Exception:
   conn.rollback();tmp=editor.PATH.with_suffix('.equipment.rollback');tmp.write_bytes(before);tmp.replace(editor.PATH);editor._config=None;raise
  profiles=updated;return {'saved':True,'card_id':pid,'values':values}

def install(module):
 if getattr(module.manage,'_ui710_equipment',False):return
 load(module._logic.conn)
 if profiles:write_config(profiles)
 original=module.manage
 @functools.wraps(original)
 def wrapped(action,payload=''):
  if action in ['ui710_equipment_get','ui710_equipment_apply']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')))
  return original(action,payload)
 wrapped._ui710_equipment=True;module.manage=wrapped


def configure_native(hook):
 hook.noodle_background_add.argtypes=[C.c_uint64,C.c_uint64];hook.noodle_background_add.restype=C.c_uint
 for pid,row in profiles.items():
  if row.get('background',0) and hook.noodle_background_add(int(pid),row['background'])!=1:raise ValueError('Native background profile rejected')
 hook.noodle_background_commit.argtypes=[];hook.noodle_background_commit.restype=None;hook.noodle_background_commit()
