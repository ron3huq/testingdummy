"""Name-indexed native motion donors. No fullID spoofing or unverified unique-pass claims."""
from pathlib import Path
import json,functools,unicodedata,ctypes as C,threading
import body_dimensions as body,myleague_editor_runtime as editor
KEY='ui712_motion';profiles={};_conn=None;_lock=threading.RLock()
def fold(x):return ''.join(c for c in unicodedata.normalize('NFKD',x.casefold())if not unicodedata.combining(c)).replace('đ','d')
@functools.lru_cache(maxsize=1)
def donors():
 rows=json.loads(Path(__file__).with_name('motion_donors.json').read_text());return {r['id']:dict(r,fold=fold(r['name']))for r in rows}
def load(c):
 global profiles,_conn
 if c is _conn:return
 r=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(r[0])if r else{}
 if not isinstance(profiles,dict)or len(profiles)>1024:raise ValueError('Invalid motion profiles')
 for pid,source in profiles.items():body.identity(pid);validate_source(pid,source)
 check_graph(profiles);_conn=c

def check_graph(rows):
 for pid in rows:
  at=pid;seen=set()
  while at in rows:
   if at in seen or len(seen)>=16:raise ValueError('Motion donor cycle or chain too long')
   seen.add(at);at=rows[at]
def validate_source(pid,source):
 if source not in donors()or source==pid:raise ValueError('Choose a different existing native player')
def manage(c,action,req):
 global profiles
 with _lock,body._lock:
  load(c)
  if action=='ui712_motion_search':
   q=fold(str(req.get('query','')).strip())[:80];page=req.get('page',0)
   if type(page)is not int or not 0<=page<=2000:raise ValueError('Invalid page')
   words=q.split();found=[{'id':r['id'],'name':r['name'],'role':r['role']}for r in donors().values()if r['id']==q or all(w in r['fold']for w in words)];return {'items':found[page*40:(page+1)*40],'total':len(found),'page':page}
  pid,p=body.owned(c,req)
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
   c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));tmp=editor.PATH.with_suffix('.motion.tmp');tmp.write_text(json.dumps(cfg,indent=2));tmp.replace(editor.PATH);c.commit()
  except Exception:
   c.rollback();tmp=editor.PATH.with_suffix('.motion.rollback');tmp.write_bytes(before);tmp.replace(editor.PATH);raise
  profiles=updated;editor._config=None;return {'saved':True,'card_id':pid,'source':source}

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
  if action in ['ui712_motion_get','ui712_motion_apply','ui712_motion_search']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')),ensure_ascii=False)
  return old(action,payload)
 wrapper._ui712_motion=True;module.manage=wrapper
