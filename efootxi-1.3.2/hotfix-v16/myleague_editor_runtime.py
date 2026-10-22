"""Validated editor overlays; no writes to card database/save and no inline NPC payloads."""
import copy,json,ctypes as C
from pathlib import Path
PATH=Path(__file__).with_name('myleague_editor.json')
SCOPES={0,518,122,566,128,549};FIELDS=set(range(14,41))-{33}
SKILLS={70,107,71,72,73,108,74,75,135,136,102,116,124,130,140,76,121,77,120,101,78,103,104,109,127,143,134,79,80,81,114,128,82,110,83,84,119,85,86,98,117,118,122,141,87,88,105,89,90,99,100,138,139,126,129,91,92,93,106,111,112,113,125,137,115,94,123,132,142,95,131,96,97,133}
FLAGS=[70,107,71,72,73,108,74,75,135,136,102,116,124,130,140,76,121,77,120,101,78,103,104,109,127,143,134,79,80,81,114,128,82,110,83,84,119,85,86,98,117,118,122,141,87,88,105,89,90,99,100,138,139,126,129,91,92,93,106,111,112,113,125,137,115,94,123,132,142,95,131,96,97,133]
DEFAULT={'schema':1,'base_version':'native-hotfix-v16','players':[],'teams':[],'weather':{'summer_end':7,'winter_start':8,'winter_end':14,'rain_chance':.35,'night_chance':.5,'late_winter_chance':.45}}
_config=None

def integer(x,lo,hi):
 if type(x)is not int or not lo<=x<=hi:raise ValueError('integer out of range')
 return x

def identity(x):
 if not isinstance(x,str) or not x.isascii() or not x.isdecimal() or str(int(x))!=x or not 0<int(x)<2**63:raise ValueError('invalid exact64 player ID')
 return int(x)

def validate(data):
 if not isinstance(data,dict) or data.get('schema')!=1 or data.get('base_version')!='native-hotfix-v16':raise ValueError('unsupported editor project/version')
 rows=data.get('players',[]);teams=data.get('teams',[])
 if not isinstance(rows,list)or len(rows)>1024 or not isinstance(teams,list)or len(teams)>128:raise ValueError('editor capacity exceeded')
 seen=set()
 for row in rows:
  pid=identity(row['id']);cid=integer(row['competition'],0,1000)
  if cid not in SCOPES or (pid,cid)in seen:raise ValueError('duplicate or invalid player scope')
  seen.add((pid,cid))
  if row.get('sleeve','none')not in ['none','original','short','long']:raise ValueError('invalid sleeve')
  params=row.get('parameters',{})
  if not isinstance(params,dict):raise ValueError('invalid parameters')
  for key,value in params.items():
   if not isinstance(key,str)or not key.isdecimal():raise ValueError('invalid parameter key')
   ix=int(key)
   if ix in FIELDS:integer(value,40,99)
   elif ix in SKILLS:integer(value,0,1)
   elif ix==47:integer(value,140,220)
   elif ix==48:integer(value,40,130)
   else:raise ValueError('unverified parameter is not editable')
 seen=set()
 for row in teams:
  tid=integer(row['team_id'],1,262143);cid=integer(row['competition'],0,1000)
  if cid not in SCOPES or(tid,cid)in seen:raise ValueError('duplicate or invalid team scope')
  seen.add((tid,cid));roster=row['roster']
  if not isinstance(roster,list)or not 11<=len(roster)<=40:raise ValueError('roster must have11..40 players')
  ids=[];numbers=set()
  for i,p in enumerate(roster):
   identity(p['id'])
   if p['id']in ids:raise ValueError('duplicate roster player')
   ids.append(p['id']);n=integer(p['shirt'],1,99)
   if n in numbers:raise ValueError('duplicate shirt number')
   numbers.add(n);integer(p['role'],0,12);integer(p['x'],0,52);integer(p['y'],0,104)
   if (i==0 and p['role']!=0)or(0<i<11 and p['role']==0):raise ValueError('one starting GK must occupy slot1')
  if row['captain']not in ids[:11]or len(row['kickers'])!=6 or any(p not in ids[:11]for p in row['kickers']):raise ValueError('roles must reference starting players')
 weather=data.get('weather',DEFAULT['weather'])
 a=integer(weather['summer_end'],1,100);b=integer(weather['winter_start'],1,100);e=integer(weather['winter_end'],b,100)
 if a>b:raise ValueError('summer/winter ranges conflict')
 for key in ['rain_chance','night_chance','late_winter_chance']:
  x=weather[key]
  if type(x)not in [float,int]or not 0<=x<=1:raise ValueError('weather probability outside0..1')
 return data

def config():
 global _config
 if _config is None:_config=validate(json.loads(PATH.read_text())if PATH.exists()else copy.deepcopy(DEFAULT))
 return _config

def install_native(hook):
 data=config()
 signatures={'editor_add_player':([C.c_uint64,C.c_uint,C.c_uint],C.c_uint),'editor_parameter':([C.c_uint,C.c_uint,C.c_uint],C.c_uint),'editor_add_team':([C.c_uint]*4,C.c_uint),'editor_team_slot':([C.c_uint,C.c_uint,C.c_uint64,C.c_uint,C.c_uint,C.c_uint,C.c_uint],C.c_uint),'editor_team_taker':([C.c_uint]*3,C.c_uint),'editor_commit':([],C.c_uint)}
 for name,(args,result)in signatures.items():fn=getattr(hook,name);fn.argtypes=args;fn.restype=result
 for row in data.get('players',[]):
  n=hook.editor_add_player(int(row['id']),row['competition'],['none','original','short','long'].index(row.get('sleeve','none')))
  if not n:raise ValueError('native rejected player row')
  for key,value in row.get('parameters',{}).items():
   if hook.editor_parameter(n,int(key),value)!=1:raise ValueError('native rejected player parameter')
 for row in data.get('teams',[]):
  ids=[p['id']for p in row['roster']];n=hook.editor_add_team(row['team_id'],row['competition'],len(ids),ids.index(row['captain']))
  if not n:raise ValueError('native rejected team')
  for slot,p in enumerate(row['roster']):
   if hook.editor_team_slot(n,slot,int(p['id']),p['shirt'],p['role'],p['x'],p['y'])!=1:raise ValueError('native rejected roster slot')
  for i,pid in enumerate(row['kickers']):
   if hook.editor_team_taker(n,i,ids.index(pid))!=1:raise ValueError('native rejected role')
 if hook.editor_commit()!=1:raise ValueError('native rejected editor transaction')

def project(player,cid):
 if int(cid)not in SCOPES-{0}:return player
 pid=str((player.get('gameplayer_id')or{}).get('id',0));rows=[r for r in config().get('players',[])if r['id']==pid and r['competition']in [0,int(cid)]]
 if not rows:return player
 out=copy.deepcopy(player);params=list(out.get('parameters')or[])
 if len(params)!=147:return out
 for row in sorted(rows,key=lambda r:r['competition']!=0):
  for k,v in row.get('parameters',{}).items():params[int(k)]=v
  removed={i for i,flag in enumerate(FLAGS)if row.get('parameters',{}).get(str(flag))==0}
  for field in ['additional_skill_id','additional_skill']:
   if field in out:out[field]=[74 if sid in removed else sid for sid in out[field]]
 out['parameters']=params
 if 'is_skill_added'in out:out['is_skill_added']='YES'if any(s!=74 for s in out.get('additional_skill_id',out.get('additional_skill',[])))else'NO'
 return out

def environment(fixture,rng,cfg):
 w=config()['weather'];winter=w['winter_start']<=fixture<=w['winter_end']
 if not winter and fixture>w['summer_end']:winter=rng.random()<w['late_winter_chance']
 return (cfg['winter']if winter else cfg['summer']),dict(weather=cfg['rain_weather']if rng.random()<w['rain_chance']else cfg['fine_weather'],time_zone=cfg['night']if rng.random()<w['night_chance']else cfg['day'])

def has_team(tid,cid):
 return any(r['team_id']==int(tid or 0)and r['competition']in [0,int(cid)]for r in config().get('teams',[]))
