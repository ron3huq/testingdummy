"""Explicit raw native ability overrides. Loaded once; no SQL in projection or engine hooks."""
import json,copy,threading,functools
from pathlib import Path
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui712_stats';profiles={};_conn=None;_lock=threading.RLock()
LABELS={14:'Offensive Awareness',15:'Defensive Awareness',16:'GK Awareness',17:'Dribbling',18:'Ball Control',19:'Tight Possession',20:'Finishing',21:'Low Pass',22:'Lofted Pass',23:'Heading',24:'Tackling',25:'Aggression',26:'Defensive Engagement',27:'Set Piece Taking',28:'Curl',29:'GK Catching',30:'GK Parrying',31:'GK Reflexes',32:'GK Reach',34:'Speed',35:'Physical Contact',36:'Balance',37:'Kicking Power',38:'Acceleration',39:'Jumping',40:'Stamina'}
def validate(v):
 if not isinstance(v,dict)or set(v)-{str(k)for k in LABELS}:raise ValueError('Invalid ability field')
 if any(type(x)is not int or not 0<=x<=127 for x in v.values()):raise ValueError('Native ability storage range is0–127;128 wraps to0 and is rejected')
 return v

def load(c):
 global _conn,profiles
 if c is _conn:return
 row=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(row[0])if row else{}
 if not isinstance(profiles,dict)or len(profiles)>1024:raise ValueError('Too many ability profiles')
 for pid,v in profiles.items():body.identity(pid);validate(v)
 _conn=c

def inject(cfg):
 for pid,v in profiles.items():
  rows=[r for r in cfg['players']if r['id']==pid]
  if not any(r['competition']==0 for r in rows):
   r={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(r);rows.append(r)
  for r in rows:r['parameters'].update(v);r['ui712_stats']=True
 return cfg

def project(p):
 pid=str((p.get('gameplayer_id')or{}).get('id',p.get('id','')));v=profiles.get(pid)
 if not v or len(p.get('parameters',[]))!=147:return p
 out=dict(p);a=list(p['parameters'])
 for k,x in v.items():a[int(k)]=x
 out['parameters']=a;return out

def manage(c,action,req):
 global profiles
 with _lock,body._lock:
  load(c);pid,p=body.owned(c,req)
  if action.endswith('_get'):
   import card_rules,profile_editor
   p=project(profile_editor.project(card_rules.project(p)))
   return {'values':{str(k):p['parameters'][k]for k in LABELS},'fields':[{'index':k,'name':v,'min':0,'max':127}for k,v in LABELS.items()],'note':'Native storage0–127. Gameplay may impose its own effective limits; no claim that127 performs above every game cap.'}
  if body.engine_loaded():raise ValueError('Close and reopen the app; edit before Enter Game')
  if c.in_transaction:raise ValueError('Another save operation is active')
  values=validate(req.get('values'));updated=copy.deepcopy(profiles);updated[pid]=dict(updated.get(pid,{}),**values)
  if len(updated)>1024:raise ValueError('Maximum1024 ability profiles')
  before=editor.PATH.read_bytes();old=profiles
  try:
   c.execute('BEGIN IMMEDIATE')
   for serial,raw in c.execute('SELECT serial,json FROM gameplayers WHERE id=?',(pid,)).fetchall():
    v=json.loads(raw)
    for field in ['parameters','_careerplan_base_parameters','original_parameters']:
     a=v.get(field)
     if isinstance(a,list)and len(a)==147:
      for k,x in values.items():a[int(k)]=x
    c.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(v,separators=(',',':')),pid,serial))
   c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));profiles=updated;cfg=inject(json.loads(before));editor.validate(cfg);temp=editor.PATH.with_suffix('.stats.tmp');temp.write_text(json.dumps(cfg,indent=2));temp.replace(editor.PATH);c.commit()
  except Exception:
   c.rollback();profiles=old;temp=editor.PATH.with_suffix('.stats.rollback');temp.write_bytes(before);temp.replace(editor.PATH);editor._config=None;raise
  editor._config=None;return {'saved':True,'card_id':pid}

def install(module):
 if getattr(module.manage,'_ui712_stats',False):return
 load(module._logic.conn);original=module.manage
 if profiles:
  cfg=inject(json.loads(editor.PATH.read_text()));editor.validate(cfg);tmp=editor.PATH.with_suffix('.stats-install.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);editor._config=None
 @functools.wraps(original)
 def wrapper(action,payload=''):
  if action in ['ui712_stats_get','ui712_stats_apply']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')))
  return original(action,payload)
 wrapper._ui712_stats=True;module.manage=wrapper
 import club_store
 prev=club_store.wire_player
 @functools.wraps(prev)
 def wire(*a,**k):return project(prev(*a,**k))
 club_store.wire_player=wire
