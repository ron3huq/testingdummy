"""On-demand per-card identity, body/motion donor and foot traits; immutable native profiles."""
from pathlib import Path
import json,copy,threading,functools,ctypes as C
import body_dimensions as body,player_model as model,myleague_editor_runtime as editor
KEY='ui711_profiles';profiles={};_conn=None;_lock=threading.RLock();revision=0
TARGETS=['105837926394281','88040387132864','106654775417922','105758469512061','105563585358239']
DEFAULTS={pid:{'name':'C.Ronaldo','shirt':'Ronaldo','club':100 if pid=='105758469512061'else 109,'nation':228,'model_source':'89138556572074'}for pid in TARGETS}
@functools.lru_cache(maxsize=1)
def options():return json.loads(Path(__file__).with_name('profile_options.json').read_text())
def merged():
 out=copy.deepcopy(DEFAULTS)
 for pid,row in profiles.items():out[pid]=dict(out.get(pid,{}),**row)
 return out

def validate(row):
 if not isinstance(row,dict)or set(row)-{'name','shirt','club','nation','age','traits','model_source'}:raise ValueError('Invalid profile fields')
 for key in ['name','shirt']:
  if key in row:
   text=row[key]
   if not isinstance(text,str)or not text.strip()or len(text.encode('utf8'))>60 or any(ord(c)<32 or ord(c)==127 for c in text):raise ValueError('Names must be non-empty and at most60 UTF-8 bytes; control characters are not allowed')
 for key,rows in [('club',options()['clubs']),('nation',options()['countries'])]:
  if key in row and(type(row[key])is not int or row[key]not in {x['id']for x in rows}):raise ValueError('Select a valid '+key)
 if 'age'in row and(type(row['age'])is not int or not 15<=row['age']<=63):raise ValueError('Age must be15–63')
 if 'model_source'in row and row['model_source']not in {x['id']for x in options()['models']}|{'89138556572074'}:raise ValueError('Unsupported body/motion donor')
 if 'traits'in row:
  if not isinstance(row['traits'],dict)or set(row['traits'])-{'33','42','43','45'}:raise ValueError('Invalid foot/fitness fields')
  for k,v in row['traits'].items():
   if type(v)is not int or not 0<=v<=(1 if k=='43'else 3):raise ValueError('Foot/fitness value outside native range')
 return row

def load(conn):
 global profiles,_conn
 if conn is _conn:return
 r=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();data=json.loads(r[0])if r else{}
 if not isinstance(data,dict)or len(data)>1024:raise ValueError('Invalid player profiles')
 for pid,row in data.items():body.identity(pid);validate(row)
 profiles=data;_conn=conn
 validate_copy_graph(merged())

def validate_copy_graph(data):
 for pid in data:
  seen=set();at=pid
  while data.get(at,{}).get('model_source'):
   if at in seen or len(seen)>=16:raise ValueError('Body-copy sources must not form a cycle')
   seen.add(at);at=data[at]['model_source']

def donor_info(donor,seen=None):
 seen=set()if seen is None else set(seen)
 if donor in seen or len(seen)>=16:raise ValueError('Cyclic body-copy source')
 seen.add(donor);info=copy.deepcopy(options()['sources'][donor]);row=merged_cached.get(donor,{})
 if row.get('model_source'):
  inherited=donor_info(row['model_source'],seen)
  for key in ['height','weight','foot','model']:info[key]=inherited[key]
 info.update({k:v for k,v in body.profiles.get(donor,{}).items()if k in ['height','weight']});info['model'].update(model.profiles.get(donor,{}));info['foot']=row.get('traits',{}).get('43',info['foot']);return info

def source_info(pid):
 donor=merged_cached.get(pid,{}).get('model_source')
 return donor_info(donor)if donor else None

def sync_names():
 global revision
 import editor_names
 for pid,row in merged().items():
  if row.get('name'):editor_names.NAMES[pid]=row['name']
 revision+=1

def sync_model_inheritance():
 inherited={}
 for pid,row in merged().items():
  donor=row.get('model_source')
  if donor:inherited[pid]=dict(donor_info(donor)['model'])
 model.inherited=inherited

def config_bytes(data):
 cfg=json.loads(editor.PATH.read_text())
 for pid,v in data.items():
  fields={str(k):x for k,x in v.get('traits',{}).items()}
  if 'age'in v:fields['46']=v['age']
  if fields or v.get('model_source'):
   row=next((r for r in cfg['players']if r['id']==pid and r['competition']==0),None)
   if row is None:row={'id':pid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(row)
   row['parameters'].update(fields)
   if v.get('model_source'):row['ui711_copy']=v['model_source']
 editor.validate(cfg);return json.dumps(cfg,indent=2).encode()

def manage(conn,action,req):
 global profiles
 with _lock,body._lock,model._lock:
  load(conn);pid,player=body.owned(conn,req);current=merged().get(pid,{});p=player['parameters']
  if action.endswith('_get'):
   effective_traits={k:p[int(k)]for k in ['33','42','43','45']}
   donor=source_info(pid)
   if donor:effective_traits['43']=donor['foot']
   return {'values':dict(current),'current_name':current.get('name',req.get('name','')),'current_shirt':current.get('shirt',''),'age':current.get('age',p[46]),'traits':dict(effective_traits,**current.get('traits',{})),'models':options()['models'],'model_source_name':options()['sources'].get(current.get('model_source'),{}).get('name','Original'),'clubs':options()['clubs']if req.get('section')=='affiliation'else[],'countries':options()['countries']if req.get('section')=='affiliation'else[]}
  if body.engine_loaded():raise ValueError('Close and reopen the app; edit before Enter Game')
  if conn.in_transaction:raise ValueError('Another save operation is active')
  changes=validate(req.get('values'));updated=copy.deepcopy(profiles);v=dict(current,**changes);updated[pid]=v
  validate_copy_graph(dict(merged(),**updated))
  if len(updated)>1024:raise ValueError('Maximum1024 customized card profiles')
  before=editor.PATH.read_bytes();nextcfg=config_bytes(updated);body.load(conn);model.load(conn);newbody=copy.deepcopy(body.profiles);newmodel=copy.deepcopy(model.profiles)
  import appearance_choices as appearances
  appearances.load(conn);newappearance=copy.deepcopy(appearances.profiles)
  copying='model_source'in changes
  if copying:
   if changes['model_source']==pid:raise ValueError('Choose a different source card')
   donor=donor_info(changes['model_source']);v.get('traits',{}).pop('43',None);newbody.pop(pid,None);newmodel.pop(pid,None)
   if pid in newappearance:
    for field in ['59','60']:newappearance[pid].pop(field,None)
   # Explicit copy replaces prior body edits for this card; all other cards and skills remain intact.
   cfg=json.loads(nextcfg)
   for r in cfg['players']:
    if r['id']==pid:
     for field in ['43','47','48']+[str(i)for i in range(50,61)]+[str(i)for i in range(63,70)]:r.get('parameters',{}).pop(field,None)
   nextcfg=json.dumps(cfg,indent=2).encode()
  tmp=editor.PATH.with_suffix('.ui711.tmp')
  try:
   conn.execute('BEGIN IMMEDIATE')
   if copying:
    for serial,raw in conn.execute('SELECT serial,json FROM gameplayers WHERE id=?',(pid,)).fetchall():
     obj=json.loads(raw)
     for key in ['parameters','_careerplan_base_parameters','original_parameters']:
      arr=obj.get(key)
      if isinstance(arr,list)and len(arr)==147:arr[47]=donor['height'];arr[48]=donor['weight']
     conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(obj,separators=(',',':')),pid,serial))
    for key,val in [(body.KEY,newbody),(model.KEY,newmodel),(appearances.KEY,newappearance)]:conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(key,json.dumps(val,separators=(',',':'))))
   conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));tmp.write_bytes(nextcfg);tmp.replace(editor.PATH);conn.commit()
  except Exception:
   conn.rollback();tmp.write_bytes(before);tmp.replace(editor.PATH);editor._config=None;raise
  profiles=updated;body.profiles=newbody;model.profiles=newmodel;appearances.profiles=newappearance;editor._config=None;refresh();return {'saved':True,'card_id':pid,'values':v}

def project(player):
 pid=str((player.get('gameplayer_id')or{}).get('id',player.get('id','')));v=merged_cached.get(pid)
 if not v:return player
 out=dict(player);params=list(player.get('parameters',[]))
 if len(params)==147:
  if v.get('model_source')and pid not in body.profiles:
   donor=source_info(pid);params[47]=donor['height'];params[48]=donor['weight'];params[43]=donor['foot']
  if 'age'in v:params[46]=v['age']
  for k,x in v.get('traits',{}).items():params[int(k)]=x
  out['parameters']=params
 if 'club'in v:
  out['initial_base_team_id']=v['club'];out['_league_id']=next(r['competition']for r in options()['clubs']if r['id']==v['club'])
 if 'nation'in v:
  out['_nation_id']=v['nation'];out['initial_base_national_team_id']=next(r['national_team_id']for r in options()['countries']if r['id']==v['nation'])
 return out
merged_cached={}
def refresh():
 global merged_cached
 merged_cached=merged();sync_names();sync_model_inheritance()

def configure_select(hook):
 hook.editor_copy_add.argtypes=[C.c_uint64,C.c_uint64];hook.editor_copy_add.restype=C.c_uint
 for pid,row in merged_cached.items():
  if row.get('model_source')and hook.editor_copy_add(int(pid),int(row['model_source']))!=1:raise ValueError('Native body/motion donor rejected')
 hook.editor_copy_commit.argtypes=[];hook.editor_copy_commit.restype=None;hook.editor_copy_commit()

def configure_noodle(hook):
 hook.noodle_identity_add.argtypes=[C.c_uint64,C.c_char_p,C.c_char_p,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint];hook.noodle_identity_add.restype=C.c_uint;clubs={r['id']:r['competition']for r in options()['clubs']}
 for pid,v in merged_cached.items():
  mask=(1 if 'club'in v else 0)|(2 if 'nation'in v else 0)|(4 if 'name'in v else 0)|(8 if 'shirt'in v else 0)
  if not mask:continue
  if hook.noodle_identity_add(int(pid),v.get('name','').encode(),v.get('shirt','').encode(),v.get('club',0),v.get('nation',0),clubs.get(v.get('club'),0),mask,next((r['national_team_id']for r in options()['countries']if r['id']==v.get('nation')),0))!=1:raise ValueError('Native identity profile rejected')
 hook.noodle_identity_commit.argtypes=[];hook.noodle_identity_commit.restype=None;hook.noodle_identity_commit()

def install(module):
 if getattr(module.manage,'_ui711_profile',False):return
 load(module._logic.conn);refresh()
 encoded=config_bytes(merged_cached)
 if encoded!=editor.PATH.read_bytes():
  temp=editor.PATH.with_suffix('.ui711-install.tmp');temp.write_bytes(encoded);temp.replace(editor.PATH);editor._config=None
 original=module.manage
 @functools.wraps(original)
 def wrapped(action,payload=''):
  if action in ['ui711_profile_get','ui711_profile_apply']:
   result=manage(module._logic.conn,action,json.loads(payload or'{}'));return json.dumps(result,ensure_ascii=False)
  return original(action,payload)
 wrapped._ui711_profile=True;module.manage=wrapped
 import club_store
 old=club_store.wire_player
 @functools.wraps(old)
 def wire(*a,**k):return project(old(*a,**k))
 club_store.wire_player=wire
