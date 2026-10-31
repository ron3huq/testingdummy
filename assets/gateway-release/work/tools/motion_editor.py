"""Name-indexed native motion donors. No fullID spoofing or unverified unique-pass claims."""
from pathlib import Path
import json,functools,unicodedata,ctypes as C,threading
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui712_motion';FIELD_KEY='ui718_motion_fields';overrides={};profiles={};_conn=None;_lock=threading.RLock()
def fold(x):return ''.join(c for c in unicodedata.normalize('NFKD',x.casefold())if not unicodedata.combining(c)).replace('đ','d')
@functools.lru_cache(maxsize=1)
def donors():
 rows=json.loads(Path(__file__).with_name('motion_donors.json').read_text());return {r['id']:dict(r,fold=fold(r['name']))for r in rows}
def load(c):
 global profiles,overrides,_conn
 if c is _conn:return
 r=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(r[0])if r else{}
 if not isinstance(profiles,dict)or len(profiles)>1024:raise ValueError('Invalid motion profiles')
 for pid,source in profiles.items():body.identity(pid);validate_source(pid,source)
 r=c.execute('SELECT value FROM meta WHERE key=?',(FIELD_KEY,)).fetchone();overrides=json.loads(r[0])if r else{}
 if not isinstance(overrides,dict)or len(overrides)>1024:raise ValueError('Invalid individual motion profiles')
 for pid,values in overrides.items():body.identity(pid);validate_fields(values)
 check_graph(profiles);_conn=c

def check_graph(rows):
 for pid in rows:
  at=pid;seen=set()
  while at in rows:
   if at in seen or len(seen)>=16:raise ValueError('Motion donor cycle or chain too long')
   seen.add(at);at=rows[at]
def validate_source(pid,source):
 if source not in donors()or source==pid:raise ValueError('Choose a different existing native player')
FIELD_LABELS=['Dribble Type','Dribbling Posture','Dribbling Arm','Running Posture','Running Arm','Free Kick Type','Penalty Kick Type','Corner Kick Pattern']
FIELD_MAX=[3,7,15,7,15,31,7,15]
@functools.lru_cache(maxsize=1)
def native_values():
 import zlib
 return json.loads(zlib.decompress(Path(__file__).with_name('motion_defaults.zlib').read_bytes()))
def validate_fields(values):
 if not isinstance(values,dict)or any(k not in {str(i)for i in range(51,59)}for k in values):raise ValueError('Invalid motion field')
 for k,v in values.items():
  if type(v)is not int or not 0<=v<=FIELD_MAX[int(k)-51]:raise ValueError('Motion value outside native storage range')
 return values
def current_values(pid,player):
 import profile_editor
 seen=set();chain=[];source=pid;motion_chain=pid in profiles
 while source not in seen:
  seen.add(source);chain.append(source)
  next_source=profiles.get(source)if motion_chain else profile_editor.merged_cached.get(source,{}).get('model_source')
  if not next_source:break
  source=next_source
 base=native_values().get(source)or native_values().get(str(int(source)&262143))or player['parameters'][51:59]
 out={str(i+51):v for i,v in enumerate(base)}
 for target in reversed(chain):
  out.update(overrides.get(target,{}))
 out.update(overrides.get(pid,{}));return out

def apply_fields(c,req):
 global overrides
 pid,player=body.owned(c,req);values=validate_fields(req.get('values'));updated=dict(overrides);updated[pid]=dict(updated.get(pid,{}),**values)
 if len(updated)>1024:raise ValueError('Maximum1024 motion profiles')
 if body.engine_loaded():raise ValueError('Reopen and edit before Enter Game')
 if c.in_transaction:raise ValueError('Another save operation is active')
 before=editor.PATH.read_bytes();cfg=json.loads(before);rows=[r for r in cfg['players']if r['id']==pid]
 if not any(r['competition']==0 for r in rows):
  r={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(r);rows.append(r)
 for r in rows:r['parameters'].update(values);r['ui718_motion_fields']=True
 editor.validate(cfg)
 try:
  c.execute('BEGIN IMMEDIATE')
  for serial,raw in c.execute('SELECT serial,json FROM gameplayers WHERE id=?',(pid,)).fetchall():
   row=json.loads(raw)
   for field in ['parameters','original_parameters','_careerplan_base_parameters']:
    a=row.get(field)
    if isinstance(a,list)and len(a)==147:
     for k,v in values.items():a[int(k)]=v
   c.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(row,separators=(',',':')),pid,serial))
  c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(FIELD_KEY,json.dumps(updated,separators=(',',':'))));tmp=editor.PATH.with_suffix('.motion.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);c.commit()
 except Exception:
  c.rollback();tmp=editor.PATH.with_suffix('.motion.rollback');tmp.write_bytes(before);tmp.replace(editor.PATH);raise
 overrides=updated;editor._config=None;return {'saved':True,'card_id':pid,'values':current_values(pid,player)}

def manage(c,action,req):
 global profiles,overrides
 with _lock,body._lock:
  load(c)
  if action=='ui712_motion_search':
   q=fold(str(req.get('query','')).strip())[:80];page=req.get('page',0)
   if type(page)is not int or not 0<=page<=2000:raise ValueError('Invalid page')
   words=q.split();found=[{'id':r['id'],'name':r['name'],'role':r['role']}for r in donors().values()if r['id']==q or all(w in r['fold']for w in words)];return {'items':found[page*40:(page+1)*40],'total':len(found),'page':page}
  pid,p=body.owned(c,req)
  if action=='ui718_motion_fields_get':return {'values':current_values(pid,p),'fields':[{'index':i+51,'name':name,'min':0,'max':FIELD_MAX[i],'choices':json.loads(Path(__file__).with_name('motion_choices.json').read_text())[str(i+51)]}for i,name in enumerate(FIELD_LABELS)]}
  if action=='ui718_motion_fields_apply':return apply_fields(c,req)
  if action.endswith('_get'):
   source=profiles.get(pid);return {'source':source,'name':donors().get(source,{}).get('name','Original'),'fields':['Dribble Type','Dribbling Posture','Dribbling Arm','Running Posture','Running Arm','Free Kick Type','Penalty Kick Type','Corner Kick Pattern'],'scope':'Eight verified native motion fields. Keeps face/body/skills/celebrations. Identity-keyed unique passing or shooting animations are not proven transferable.'}
  if body.engine_loaded():raise ValueError('Close and reopen the app; edit before Enter Game')
  if c.in_transaction:raise ValueError('Another save operation is active')
  source=req.get('source');validate_source(pid,source);updated=dict(profiles);updated[pid]=source;check_graph(updated)
  if len(updated)>1024:raise ValueError('Maximum1024 motion profiles')
  before=editor.PATH.read_bytes();cfg=json.loads(before);r=next((r for r in cfg['players']if r['id']==pid and r['competition']==0),None)
  if r is None:r={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(r)
  r['ui712_motion']=source
  # Copy replaces explicit values for these eight fields; unrelated parameter edits remain intact.
  for row in cfg['players']:
   if row['id']==pid:
    for ix in range(51,59):row.get('parameters',{}).pop(str(ix),None)
  editor.validate(cfg)
  try:
   c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));fields=dict(overrides);fields.pop(pid,None);c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(FIELD_KEY,json.dumps(fields,separators=(',',':'))));tmp=editor.PATH.with_suffix('.motion.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);c.commit()
  except Exception:
   c.rollback();tmp=editor.PATH.with_suffix('.motion.rollback');tmp.write_bytes(before);tmp.replace(editor.PATH);raise
  profiles=updated;overrides=fields;editor._config=None;return {'saved':True,'card_id':pid,'source':source}

def project(player):
 import profile_editor
 pid=str((player.get('gameplayer_id')or{}).get('id',player.get('id','')))
 if len(player.get('parameters',[]))!=147 or not(pid in profiles or pid in overrides or profile_editor.merged_cached.get(pid,{}).get('model_source')):return player
 out=dict(player);p=list(player['parameters'])
 for k,v in current_values(pid,player).items():p[int(k)]=v
 out['parameters']=p;return out

def configure(hook):
 hook.editor_motion_add.argtypes=[C.c_uint64,C.c_uint64];hook.editor_motion_add.restype=C.c_uint
 for pid,source in profiles.items():
  if hook.editor_motion_add(int(pid),int(source))!=1:raise ValueError('Native motion donor rejected')
 hook.editor_motion_commit.argtypes=[];hook.editor_motion_commit.restype=None;hook.editor_motion_commit()

def install(module):
 if getattr(module.manage,'_ui712_motion',False):return
 load(module._logic.conn);old=module.manage
 @functools.wraps(old)
 def wrapper(action,payload=''):
  if action in ['ui712_motion_get','ui712_motion_apply','ui712_motion_search','ui718_motion_fields_get','ui718_motion_fields_apply']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')),ensure_ascii=False)
  return old(action,payload)
 wrapper._ui712_motion=True;module.manage=wrapper
 import club_store
 prior=club_store.wire_player
 @functools.wraps(prior)
 def wire(*a,**k):return project(prior(*a,**k))
 club_store.wire_player=wire
