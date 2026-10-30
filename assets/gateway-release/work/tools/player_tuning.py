"""On-demand innate skills. Physics controls removed. Never scan the catalogue."""
from pathlib import Path
import json,copy,threading,functools
import body_dimensions as body,player_model as model,myleague_editor_runtime as editor
SK='ui77_innate_skills';skills={};_conn=None;_lock=threading.RLock()
def load(conn):
 global _conn,skills
 if conn is _conn:return
 def read(key):
  r=conn.execute('SELECT value FROM meta WHERE key=?',(key,)).fetchone();return json.loads(r[0])if r else{}
 skills=read(SK)
 for pid,ids in skills.items():body.identity(pid);validate_skills(ids)
 _conn=conn

def validate_skills(ids):
 if not isinstance(ids,list)or len(ids)>74 or len(set(ids))!=len(ids)or any(type(v)is not int or not 0<=v<74 for v in ids):raise ValueError('Invalid innate skill selection')
 return sorted(ids)
def write_config(cfg):
 for pid,ids in skills.items():
  r=next((r for r in cfg['players']if r['id']==pid and r['competition']==0),None)
  if r is None:r={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(r)
  r['ui77_innate']=True;r['parameters'].update({str(flag):int(i in ids)for i,flag in enumerate(editor.FLAGS)})
 editor.validate(cfg);tmp=editor.PATH.with_suffix('.ui77.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);editor._config=None

def get(conn,action,req):
 with _lock:
  load(conn);pid,v=body.owned(conn,req);p=v['parameters']
  if action=='ui77_skills_get':
   import card_rules
   v=card_rules.project(v);p=v['parameters'];ids=skills.get(pid,[i for i,k in enumerate(editor.FLAGS)if p[k]])
   labels=json.loads(Path(__file__).with_name('innate_skill_labels.json').read_text())
   return {'selected':ids,'choices':[{'id':i,'label':labels.get(str(i),'Unmapped native skill '+str(i))}for i in range(74)if str(i)in labels or i in ids],'additional_skills_unchanged':True}
  raise ValueError('Unknown tuning action')

def apply(conn,action,req):
 global skills
 with _lock,body._lock:
  load(conn);body.load(conn);pid,v=body.owned(conn,req)
  if body.engine_loaded():raise ValueError('Close and reopen the app, then edit before entering the game')
  if conn.in_transaction:raise ValueError('Another save operation is active')
  oldskills=copy.deepcopy(skills);oldbody=copy.deepcopy(body.profiles);before=editor.PATH.read_bytes()
  if action=='ui77_skills_apply':
   ids=validate_skills(req.get('selected'));skills=dict(skills);skills[pid]=ids;changes={k:int(i in ids)for i,k in enumerate(editor.FLAGS)};v['innate_skills']=ids
  else:raise ValueError('Physics controls have been removed')
  try:
   for key in ['parameters','_careerplan_base_parameters']:
    if isinstance(v.get(key),list)and len(v[key])==147:
     v[key]=list(v[key])
     for k,val in changes.items():v[key][k]=val
   conn.execute('BEGIN IMMEDIATE');conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(v,separators=(',',':')),pid,req['serial']))
   for key,value in [(SK,skills),(body.KEY,body.profiles)]:conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(key,json.dumps(value,separators=(',',':'))))
   body.write_config(body.profiles);write_config(json.loads(editor.PATH.read_text()));conn.commit()
  except Exception:
   conn.rollback();skills=oldskills;body.profiles=oldbody;tmp=editor.PATH.with_suffix('.rollback.tmp');tmp.write_bytes(before);tmp.replace(editor.PATH);editor._config=None;raise
  return {'saved':True,'card_id':pid}

def project(v):
 pid=str((v.get('gameplayer_id')or{}).get('id',v.get('id','')))
 if len(v.get('parameters',[]))!=147 or pid not in skills:return v
 out=dict(v);p=list(v['parameters'])
 if pid in skills:
  if 'innate_skills'in out:out['innate_skills']=list(skills[pid])
  for i,k in enumerate(editor.FLAGS):p[k]=int(i in skills[pid])

 out['parameters']=p;return out

def install(module):
 if getattr(module.manage,'_ui77_tuning',False):return False
 load(module._logic.conn)
 import player_editor
 labels=json.loads(Path(__file__).with_name('innate_skill_labels.json').read_text())
 player_editor.SKILL_LABELS.update({int(k):v for k,v in labels.items()})
 if skills:write_config(json.loads(editor.PATH.read_text()))
 original=module.manage
 @functools.wraps(original)
 def manage(action,payload=''):
  if action in ['ui77_skills_get','ui77_skills_apply']:
   req=json.loads(payload or'{}');return json.dumps(get(module._logic.conn,action,req)if action.endswith('_get')else apply(module._logic.conn,action,req))
  return original(action,payload)
 manage._ui77_tuning=True;module.manage=manage
 import club_store
 old=club_store.wire_player
 @functools.wraps(old)
 def wire(*a,**k):return project(old(*a,**k))
 club_store.wire_player=wire;return True
