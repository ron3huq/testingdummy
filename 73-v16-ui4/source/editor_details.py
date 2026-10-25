"""On-demand dimensions/native-skill edits. No catalogue hooks or per-row SQL."""
from pathlib import Path
import json,copy,functools
ROOT=None;profiles={}
KEY='ui4_dimensions_skills_v1'
_loaded_conn=None
def load_profiles(conn):
 global profiles,_loaded_conn
 if conn is _loaded_conn:return
 row=conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();profiles=json.loads(row[0])if row else{};_loaded_conn=conn


def owned(conn,req):
 cid=str(req.get('id',''));serial=req.get('serial')
 if not cid.isdecimal()or type(serial)is not int:raise ValueError('Select an owned card first')
 row=conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(cid,serial)).fetchone()
 if not row:raise ValueError('Player instance changed; reopen the list')
 value=json.loads(row[0])
 if len(value.get('parameters',[]))!=147:raise ValueError('Unsupported card parameter layout')
 return cid,value

@functools.lru_cache(maxsize=1)
def skill_labels():return json.loads((Path(__file__).parent/'editor_skill_labels.json').read_text())

def get(conn,req):
 import player_skills
 load_profiles(conn)
 cid,value=owned(conn,req);p=value['parameters'];extra=profiles.get(cid,{})
 skills=[{'id':i,'label':skill_labels().get(str(i),name.replace('_',' ').title()),'parameter':player_skills.PARAMETER_BY_SKILL[i]}for i,name in enumerate(player_skills.SKILL_NAMES)if i in player_skills.PARAMETER_BY_SKILL]
 return dict(height=extra.get('height',p[47]),weight=extra.get('weight',p[48]),selected=extra.get('skills',player_skills.innate_skill_ids(p)),skills=skills)

def write_config(data):
 import myleague_editor_runtime as editor,player_skills
 path=ROOT/'work/tools/myleague_editor.json';cfg=json.loads(path.read_text())
 for cid,v in data.items():
  row=next((r for r in cfg['players']if r['id']==cid and r['competition']==0),None)
  if row is None:row={'id':cid,'competition':0,'sleeve':'none','parameters':{}};cfg['players'].append(row)
  row['ui4_details']=True;params=row['parameters'];params['47']=v['height'];params['48']=v['weight'];selected=set(v['skills'])
  params.update({str(index):int(i in selected)for i,index in player_skills.PARAMETER_BY_SKILL.items()})
 editor.validate(cfg);temp=path.with_suffix('.ui4.tmp');temp.write_text(json.dumps(cfg,indent=2));temp.replace(path);editor._config=None

def apply(conn,req):
 global profiles
 import player_skills
 load_profiles(conn)
 cid,value=owned(conn,req);h=req.get('height');w=req.get('weight');skills=req.get('skills')
 if type(h)is not int or not 140<=h<=220 or type(w)is not int or not 40<=w<=130:raise ValueError('Height140–220cm; weight40–130kg')
 if not isinstance(skills,list)or any(type(i)is not int or i not in player_skills.PARAMETER_BY_SKILL for i in skills)or len(skills)!=len(set(skills)):raise ValueError('Invalid skill choice')
 # Native settings are installed before entering the engine. Never pretend that
 # an already loaded hook has adopted a changed immutable profile table.
 if 'libUE4.so'in Path('/proc/self/maps').read_text():raise ValueError('Reopen the app and edit before entering the game')
 if conn.in_transaction:raise ValueError('Another save operation is active')
 changed=copy.deepcopy(profiles);changed[cid]=dict(height=h,weight=w,skills=sorted(skills))
 selected=set(skills)
 for key in ['parameters','_careerplan_base_parameters']:
  p=value.get(key)
  if isinstance(p,list)and len(p)==147:
   p[47]=h;p[48]=w
   for i,index in player_skills.PARAMETER_BY_SKILL.items():p[index]=int(i in selected)
 value['_skills']=sorted(selected)
 path=ROOT/'work/tools/myleague_editor.json';before=path.read_bytes()
 try:
  conn.execute('BEGIN IMMEDIATE')
  conn.execute('UPDATE gameplayers SET json=? WHERE id=? AND serial=?',(json.dumps(value,separators=(',',':')),cid,req['serial']))
  conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(changed,separators=(',',':'))))
  write_config(changed);conn.commit()
 except Exception:
  conn.rollback();temp=path.with_suffix('.rollback.tmp');temp.write_bytes(before);temp.replace(path)
  import myleague_editor_runtime as editor
  editor._config=None
  raise
 profiles=changed;return dict(saved=True,card_id=cid,height=h,weight=w,skills=sorted(skills))

def project(value):
 cid=str((value.get('gameplayer_id')or{}).get('id',value.get('id','')));v=profiles.get(cid)
 if not v or len(value.get('parameters',[]))!=147:return value
 import player_skills
 out=dict(value);p=list(value['parameters']);p[47]=v['height'];p[48]=v['weight']
 for i,index in player_skills.PARAMETER_BY_SKILL.items():p[index]=int(i in v['skills'])
 out['parameters']=p
 if 'innate_skills'in out:out['innate_skills']=list(v['skills'])
 return out

def install(root,module):
 global ROOT,profiles
 ROOT=Path(root)
 if getattr(module.manage,'_ui4_details',False):return False
 conn=getattr(getattr(module,'_logic',None),'conn',None)
 if conn is not None:
  load_profiles(conn)
  if profiles:write_config(profiles)
 original=module.manage
 @functools.wraps(original)
 def manage(action,payload=''):
  if action in ['ui4_details_get','ui4_details_apply']:
   req=json.loads(payload or '{}');conn=module._logic.conn
   return json.dumps(get(conn,req)if action.endswith('_get')else apply(conn,req))
  return original(action,payload)
 manage._ui4_details=True;module.manage=manage
 import club_store
 old=club_store.wire_player
 @functools.wraps(old)
 def wire(*args,**kwargs):return project(old(*args,**kwargs))
 club_store.wire_player=wire
 return True
