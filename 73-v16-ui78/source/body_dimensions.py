"""On-demand height/weight editing. No catalogue scans or per-player SQL hooks."""
from pathlib import Path
import copy,json,functools,threading
ROOT=None;KEY='ui7_body_dimensions_v1';profiles={};_loaded_conn=None;_lock=threading.RLock()
def load(conn):
 global profiles,_loaded_conn
 if conn is _loaded_conn:return
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();data=json.loads(row[0])if row else{}
 if not isinstance(data,dict):raise ValueError('Invalid saved body settings')
 for pid,v in data.items():validate_values(v);identity(pid)
 profiles=data;_loaded_conn=conn

def identity(pid):
 if not isinstance(pid,str)or not pid.isascii()or not pid.isdecimal()or str(int(pid))!=pid or not 0<int(pid)<2**63:raise ValueError('Select a valid card')
 return pid

def validate_values(req):
 h=req.get('height');w=req.get('weight')
 if type(h)is not int or not 140<=h<=220 or type(w)is not int or not 40<=w<=130:raise ValueError('Height must be140–220cm; weight40–130kg')
 return h,w

def owned(conn,req):
 pid=identity(str(req.get('id','')));serial=req.get('serial')
 if type(serial)is not int or serial<0:raise ValueError('Select an owned card instance')
 row=conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(pid,serial)).fetchone()
 if not row:raise ValueError('Player changed; reopen the player list')
 value=json.loads(row[0]);params=value.get('parameters')
 if not isinstance(params,list)or len(params)!=147:raise ValueError('Unsupported player data')
 return pid,value

def get(conn,req):
 with _lock:
  load(conn);pid,value=owned(conn,req);p=value['parameters'];v=profiles.get(pid,{})
  return dict(height=v.get('height',p[47]),weight=v.get('weight',p[48]))

def write_config(data):
 import myleague_editor_runtime as editor
 path=ROOT/'work/tools/myleague_editor.json';cfg=json.loads(path.read_text())
 for pid,v in data.items():
  row=next((r for r in cfg['players']if r['id']==pid and r['competition']==0),None)
  if row is None:row={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(row)
  row['ui7_body']=True;row['parameters']['47']=v['height'];row['parameters']['48']=v['weight']
 editor.validate(cfg);encoded=json.dumps(cfg,indent=2)
 if path.read_text()!=encoded:
  temp=path.with_suffix('.ui7-body.tmp');temp.write_text(encoded);temp.replace(path)
 editor._config=None

def engine_loaded():return 'libUE4.so'in Path('/proc/self/maps').read_text()

def apply(conn,req):
 global profiles
 with _lock:
  load(conn);pid,value=owned(conn,req);h,w=validate_values(req)
  if engine_loaded():raise ValueError('Close and reopen the app, then edit before entering the game')
  if conn.in_transaction:raise ValueError('Another save operation is active; try again')
  changed=copy.deepcopy(profiles);changed[pid]={'height':h,'weight':w}
  for key in['parameters','_careerplan_base_parameters']:
   p=value.get(key)
   if isinstance(p,list)and len(p)==147:p[47]=h;p[48]=w
  path=ROOT/'work/tools/myleague_editor.json';before=path.read_bytes()
  try:
   conn.execute('BEGIN IMMEDIATE');conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(value,separators=(',',':')),pid,req['serial']))
   conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(changed,separators=(',',':'))));write_config(changed);conn.commit()
  except Exception:
   conn.rollback();temp=path.with_suffix('.rollback.tmp');temp.write_bytes(before);temp.replace(path)
   import myleague_editor_runtime as editor
   editor._config=None
   raise
  profiles=changed;return dict(saved=True,card_id=pid,height=h,weight=w)

def project(value):
 pid=str((value.get('gameplayer_id')or{}).get('id',value.get('id','')));v=profiles.get(pid)
 if not v or len(value.get('parameters',[]))!=147:return value
 out=dict(value);p=list(value['parameters']);p[47]=v['height'];p[48]=v['weight'];out['parameters']=p;return out

def install(root,module):
 global ROOT
 ROOT=Path(root)
 if getattr(module.manage,'_ui7_body',False):return False
 conn=getattr(getattr(module,'_logic',None),'conn',None)
 if conn is not None:
  load(conn)
  if profiles:write_config(profiles)
 original=module.manage
 @functools.wraps(original)
 def manage(action,payload=''):
  if action in['ui7_body_get','ui7_body_apply']:
   req=json.loads(payload or'{}');conn=module._logic.conn
   return json.dumps(get(conn,req)if action.endswith('_get')else apply(conn,req))
  return original(action,payload)
 manage._ui7_body=True;module.manage=manage
 import club_store
 old=club_store.wire_player
 @functools.wraps(old)
 def wire(*args,**kwargs):return project(old(*args,**kwargs))
 club_store.wire_player=wire;return True
