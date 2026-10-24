"""Card-wide body/motion fields using verified canonical147 native accessors.
Keeps owned progression/skills/positions intact. Settings are backed up in save meta.
"""
import copy,json,os,sqlite3,functools
from pathlib import Path
FIELDS={'height':(47,140,220),'weight':(48,40,130),'foot':(43,0,1),'celebration':(60,0,127)}
KEY='v25_native_body_profiles_v1'
ROOT=None

def _profiles(conn):
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone()
 data=json.loads(row[0]) if row else {}
 if not isinstance(data,dict):raise ValueError('Invalid stored body settings')
 return data

def _owned(conn,request):
 cid=str(request.get('id',''));serial=request.get('serial')
 if not cid.isdecimal() or type(serial)is not int:raise ValueError('Select an owned player instance first')
 row=conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(cid,serial)).fetchone()
 if not row:raise ValueError('Player instance changed; reopen the list')
 player=json.loads(row[0]);params=player.get('parameters',[])
 if len(params)!=147:raise ValueError('Unsupported parameter layout; original player left untouched')
 return cid,player

def _write_config(profiles):
 import myleague_editor_runtime as editor
 p=ROOT/'work/tools/myleague_editor.json';data=json.loads(p.read_text())
 for cid,profile in profiles.items():
  rows=[r for r in data['players'] if r['id']==cid and r['competition']==0]
  if not rows:
   row={'id':cid,'competition':0,'sleeve':'none','parameters':{}};data['players'].append(row)
  else:row=rows[0]
  for key,(index,low,high) in FIELDS.items():
   if key in profile:row['parameters'][str(index)]=profile[key]
  if 'sleeve' in profile:row['sleeve']=profile['sleeve']
  if 'accessories' in profile:row['accessories']=profile['accessories']
 editor.validate(data)
 temp=p.with_suffix('.json.tmp');temp.write_text(json.dumps(data,indent=2));temp.replace(p);editor._config=None

def get(conn,request):
 import player_editor
 cid,player=_owned(conn,request);params=player['parameters'];profile=_profiles(conn).get(cid,{})
 out={k:profile.get(k,params[i]) for k,(i,lo,hi) in FIELDS.items()}
 rows=player_editor.celebration_choices(conn);choices=[]
 for r in rows:
  if not 0<=r['id']<=127:continue
  n=r['label'].split('的',1)[0];choices.append({'id':r['id'],'label':n+' · preset '+str(r['id'])})
 if out['celebration'] not in [r['id'] for r in choices]:choices.insert(0,{'id':out['celebration'],'label':'Current native preset '+str(out['celebration'])})
 out['celebrations']=choices
 out['accessories']=profile.get('accessories',{})
 import myleague_editor_runtime as editor
 matching=[r for r in editor.config()['players'] if r['id']==cid and r['competition']==0]
 sleeve=profile.get('sleeve',(matching[0].get('sleeve','none') if matching else 'none'))
 out['sleeve_index']={'none':0,'original':0,'short':1,'long':2}[sleeve]
 return out

def apply(conn,request):
 cid,player=_owned(conn,request)
 if 'libUE4.so' in Path('/proc/self/maps').read_text():raise ValueError('Close and reopen the app before changing body settings; the game engine is already running')
 values={}
 for key,(_,low,high) in FIELDS.items():
  value=request.get(key)
  if type(value)is not int or not low<=value<=high:raise ValueError(key+' must be between '+str(low)+' and '+str(high))
  values[key]=value
 allowed={r['id'] for r in get(conn,request)['celebrations']}
 if values['celebration'] not in allowed:raise ValueError('Choose a verified native preset from the list')
 if request.get('sleeve') not in ['none','short','long']:raise ValueError('Invalid sleeve choice')
 gear=request.get('accessories',{})
 if not isinstance(gear,dict)or set(gear)-{'4','5','6','7'}or any(type(v)is not int or not 0<=v<=2 for v in gear.values()):raise ValueError('Invalid accessory choice')
 values['accessories']=gear
 values['sleeve']=request['sleeve'];profiles=_profiles(conn);profiles[cid]=values
 # Keep the save metadata and runtime overlay consistent if either write fails.
 if conn.in_transaction:raise ValueError('Another save operation is active; retry after it finishes')
 path=ROOT/'work/tools/myleague_editor.json';before=path.read_bytes()
 try:
  conn.execute('BEGIN IMMEDIATE')
  conn.execute('INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)',(KEY,json.dumps(profiles,separators=(',',':'))))
  _write_config(profiles)
  conn.commit()
 except Exception:
  conn.rollback()
  temp=path.with_suffix('.rollback.tmp');temp.write_bytes(before);temp.replace(path)
  import myleague_editor_runtime as editor
  editor._config=None
  raise
 return dict(saved=True,card_id=cid,settings=values,scope='card-wide',engine_restart_required=False)

def _project(player,profiles):
 cid=str((player.get('gameplayer_id')or{}).get('id',player.get('id','')));profile=profiles.get(cid)
 if not profile or len(player.get('parameters',[]))!=147:return player
 out=copy.deepcopy(player)
 for key,(index,lo,hi) in FIELDS.items():
  if key in profile:out['parameters'][index]=profile[key]
 return out

def install(root,module):
 global ROOT
 ROOT=Path(root)
 if getattr(module.manage,'_v25_body',False):return False
 conn=module._logic.conn
 profiles=_profiles(conn)
 if profiles:_write_config(profiles)
 original=module.manage
 @functools.wraps(original)
 def manage(action,payload=''):
  if action in ['v25_body_get','v25_body_apply']:
   request=json.loads(payload or '{}')
   result=get(module._logic.conn,request) if action=='v25_body_get' else apply(module._logic.conn,request)
   return json.dumps(result,ensure_ascii=False)
  return original(action,payload)
 manage._v25_body=True;module.manage=manage
 import player_editor,club_store
 old_players=player_editor.players
 @functools.wraps(old_players)
 def players(conn,*args,**kwargs):
  profiles=_profiles(conn)
  return [_project(p,profiles) for p in old_players(conn,*args,**kwargs)]
 player_editor.players=players
 old_wire=club_store.wire_player
 @functools.wraps(old_wire)
 def wire(player,*args,**kwargs):return _project(old_wire(player,*args,**kwargs),_profiles(module._logic.conn))
 club_store.wire_player=wire
 return True
