"""Validated editor overlays; no writes to card database/save and no inline NPC payloads."""
import copy,json,re,ctypes as C
from pathlib import Path
PATH=Path(__file__).with_name('myleague_editor.json')
SCOPES={0,125,518,473,122,566,128,549};FIELDS=set(range(14,41))-{33}
SKILLS={70,107,71,72,73,108,74,75,135,136,102,116,124,130,140,76,121,77,120,101,78,103,104,109,127,143,134,79,80,81,114,128,82,110,83,84,119,85,86,98,117,118,122,141,87,88,105,89,90,99,100,138,139,126,129,91,92,93,106,111,112,113,125,137,115,94,123,132,142,95,131,96,97,133}
FLAGS=[70,107,71,72,73,108,74,75,135,136,102,116,124,130,140,76,121,77,120,101,78,103,104,109,127,143,134,79,80,81,114,128,82,110,83,84,119,85,86,98,117,118,122,141,87,88,105,89,90,99,100,138,139,126,129,91,92,93,106,111,112,113,125,137,115,94,123,132,142,95,131,96,97,133]
DEFAULT={'schema':1,'base_version':'native-hotfix-v18','players':[],'teams':[],'weather':{'summer_end':7,'winter_start':8,'winter_end':14,'rain_chance':.35,'night_chance':.5,'late_winter_chance':.45}}
_config=None

def integer(x,lo,hi):
 if type(x)is not int or not lo<=x<=hi:raise ValueError('integer out of range')
 return x

def identity(x):
 if not isinstance(x,str) or not x.isascii() or not x.isdecimal() or str(int(x))!=x or not 0<int(x)<2**63:raise ValueError('invalid exact64 player ID')
 return int(x)

def validate(data):
 if not isinstance(data,dict) or data.get('schema')!=1 or data.get('base_version')!='native-hotfix-v18':raise ValueError('unsupported editor project/version')
 rows=data.get('players',[]);teams=data.get('teams',[])
 if not isinstance(rows,list)or len(rows)>1024 or not isinstance(teams,list)or len(teams)>128:raise ValueError('editor capacity exceeded')
 seen=set()
 for row in rows:
  pid=identity(row['id']);cid=integer(row['competition'],0,1000)
  if cid not in SCOPES or (pid,cid)in seen:raise ValueError('duplicate or invalid player scope')
  seen.add((pid,cid))
  if row.get('sleeve','none')not in ['none','original','short','long','inner','highneck','cutlong']:raise ValueError('invalid sleeve')
  params=row.get('parameters',{})
  if not isinstance(params,dict):raise ValueError('invalid parameters')
  for key,value in params.items():
   if not isinstance(key,str)or not key.isdecimal():raise ValueError('invalid parameter key')
   ix=int(key)
   if ix in FIELDS:integer(value,0,127)
   elif ix in SKILLS:integer(value,0,1)
   elif ix==51:integer(value,0,3)
   elif ix in (52,54):integer(value,0,7)
   elif ix in (53,55):integer(value,0,15)
   elif ix in (33,42,45,50):integer(value,0,3)
   elif ix==46:integer(value,15,63)
   elif ix in range(63,70):integer(value,0,1)
   elif ix==56:integer(value,0,31)
   elif ix==57:integer(value,0,7)
   elif ix==58:integer(value,0,15)
   elif ix==43:integer(value,0,1)
   elif ix==59:integer(value,0,511)
   elif ix==60:integer(value,0,127)
   elif ix==47:integer(value,140,220)
   elif ix==48:integer(value,40,130)
   else:raise ValueError('unverified parameter is not editable')
  gear=row.get('accessories',{})
  if not isinstance(gear,dict):raise ValueError('invalid accessories')
  for key,mode in gear.items():
   if key not in ['0','1','2','3','4','5','6','7','8','9']:raise ValueError('unsupported accessory; GK gloves are excluded')
   integer(mode,0,2)
  colors=row.get('accessory_colors',{})
  if not isinstance(colors,dict)or set(colors)-{'0','1','2','3','4','5','6','7','8','9'}or any(not isinstance(x,str)or not re.fullmatch(r'#[0-9a-fA-F]{6}',x)for x in colors.values()):raise ValueError('Invalid accessory colors')
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
  if (row['captain']is not None and row['captain']not in ids)or len(row['kickers'])!=6 or any(p is not None and p not in ids for p in row['kickers']):raise ValueError('roles must reference roster players or native unset')
  if 'plans'in row:
   if not isinstance(row['plans'],list)or len(row['plans'])!=4:raise ValueError('four native plans required')
   for plan in row['plans']:
    integer(plan['flags'],0,255)
    if len(plan['slots'])!=11:raise ValueError('eleven formation slots required')
    if plan['slots'][0]['role']!=0 or any(p['role']==0 for p in plan['slots'][1:]):raise ValueError('exactly one GK in each plan')
    for p in plan['slots']:integer(p['role'],0,12);integer(p['x'],0,52);integer(p['y'],0,104)
 weather=data.get('weather',DEFAULT['weather'])
 a=integer(weather['summer_end'],1,100);b=integer(weather['winter_start'],1,100);e=integer(weather['winter_end'],b,100)
 if a>b:raise ValueError('summer/winter ranges conflict')
 for key in ['rain_chance','night_chance','late_winter_chance']:
  x=weather[key]
  if type(x)not in [float,int]or not 0<=x<=1:raise ValueError('weather probability outside0..1')
 return data

def config():
 global _config
 if _config is None:
  loaded=json.loads(PATH.read_text())if PATH.exists()else copy.deepcopy(DEFAULT)
  if loaded.get('base_version')=='native-hotfix-v17':loaded['base_version']='native-hotfix-v18'
  _config=validate(loaded)
 return _config

def requested_long_sleeves(data):
 out=copy.deepcopy(data)
 for pid in ['88044950524330','89135066911146','106781745353130','106726716084650','17592722922839']:
  found=False
  for row in out.setdefault('players',[]):
   if row['id']==pid:
    row['sleeve']='long'
    if row['competition']==0:found=True
  if not found:out['players'].append({'id':pid,'competition':0,'sleeve':'long','parameters':{}})
 # Only the four requested Ronaldo cards. Defensive/GK fields, demographics,
 # weak-foot/form flags, skills and all other cards remain untouched.
 fields=[14,17,18,19,20,21,22,23,27,28,34,35,36,37,38,39,40]
 for card in ['88044950524330','89135066911146','106726716084650','106734785925546']:
  rows=[x for x in out.setdefault('players',[])if x['id']==card]
  if not any(x['competition']==0 for x in rows):
   row={'id':card,'competition':0,'sleeve':'none','parameters':{}};out['players'].append(row);rows.append(row)
  for row in rows:
   for ix in fields:row.setdefault('parameters',{})[str(ix)]=92+((ix+int(card)%5)%5)
 # User equipment selections override bundled sleeve defaults after they are expanded.
 import sys
 gear=sys.modules.get('appearance_gear')
 for row in out.get('players',[]):
  choice=getattr(gear,'profiles',{}).get(row['id'],{}).get('sleeve')
  if choice in ['original','short','long','inner','highneck','cutlong']:row['sleeve']=choice
 stats=sys.modules.get('stat_editor')
 if stats:out=stats.inject(out)
 return validate(out)

def install_native(hook):
 data=requested_long_sleeves(config())
 signatures={'editor_accessory_color':([C.c_uint]*3,C.c_uint),'editor_team_global':([C.c_uint],C.c_uint),'editor_global_stats':([C.c_uint],C.c_uint),'editor_accessory':([C.c_uint]*3,C.c_uint),'editor_add_player':([C.c_uint64,C.c_uint,C.c_uint],C.c_uint),'editor_parameter':([C.c_uint,C.c_uint,C.c_uint],C.c_uint),'editor_add_team':([C.c_uint]*4,C.c_uint),'editor_team_slot':([C.c_uint,C.c_uint,C.c_uint64,C.c_uint,C.c_uint,C.c_uint,C.c_uint],C.c_uint),'editor_team_plan':([C.c_uint]*7,C.c_uint),'editor_team_taker':([C.c_uint]*3,C.c_uint),'editor_commit':([],C.c_uint)}
 for name,(args,result)in signatures.items():fn=getattr(hook,name);fn.argtypes=args;fn.restype=result
 for row in data.get('players',[]):
  n=hook.editor_add_player(int(row['id']),row['competition'],['none','original','short','long'].index('long'if row.get('sleeve')=='cutlong'else'short'if row.get('sleeve')in ['inner','highneck']else row.get('sleeve','none')))
  if not n:raise ValueError('native rejected player row')
  if row.get('ui712_stats')and hook.editor_global_stats(n)!=1:raise ValueError('Native stats scope rejected')
  for key,mode in row.get('accessories',{}).items():
   if hook.editor_accessory(n,int(key),mode)!=1:raise ValueError('native rejected accessory')
  for key,color in row.get('accessory_colors',{}).items():
   if hook.editor_accessory_color(n,int(key),0xff000000|int(color[1:],16))!=1:raise ValueError('Native accessory color rejected')
  for key,value in row.get('parameters',{}).items():
   if hook.editor_parameter(n,int(key),value)!=1:raise ValueError('native rejected player parameter')
 for row in data.get('teams',[]):
  ids=[p['id']for p in row['roster']];n=hook.editor_add_team(row['team_id'],row['competition'],len(ids),ids.index(row['captain'])if row['captain']is not None else 255)
  if not n:raise ValueError('native rejected team')
  if row.get('ui712_transfer')and row['competition']==0 and hook.editor_team_global(n)!=1:raise ValueError('Native team scope rejected')
  for slot,p in enumerate(row['roster']):
   if hook.editor_team_slot(n,slot,int(p['id']),p['shirt'],p['role'],p['x'],p['y'])!=1:raise ValueError('native rejected roster slot')
  for variant,plan in enumerate(row.get('plans',[])):
   for slot,p in enumerate(plan['slots']):
    if hook.editor_team_plan(n,variant,slot,p['role'],p['x'],p['y'],plan['flags'])!=1:raise ValueError('native rejected formation variant')
  for i,pid in enumerate(row['kickers']):
   if hook.editor_team_taker(n,i,(ids.index(pid)if pid is not None else 255))!=1:raise ValueError('native rejected role')
 if hook.editor_commit()!=1:raise ValueError('native rejected editor transaction')

_projection_sources=None;_projection_rows={}
def projection_rows():
 global _projection_sources,_projection_rows
 import sys
 data=config();gear=getattr(sys.modules.get('appearance_gear'),'profiles',None);stats=getattr(sys.modules.get('stat_editor'),'profiles',None)
 sources=(data,gear,stats)
 if _projection_sources is None or any(a is not b for a,b in zip(sources,_projection_sources)):
  rows={}
  for row in requested_long_sleeves(data).get('players',[]):rows.setdefault(row['id'],[]).append(row)
  _projection_rows=rows;_projection_sources=sources
 return _projection_rows

def project(player,cid):
 if int(cid)not in SCOPES-{0}:return player
 from world_skills import project as add_world_skills
 player=add_world_skills(player,cid)
 pid=str((player.get('gameplayer_id')or{}).get('id',0));rows=[r for r in projection_rows().get(pid,[])if r['competition']in [0,int(cid)]]
 if not rows:return player
 out=copy.deepcopy(player);params=list(out.get('parameters')or[])
 if len(params)!=147:return out
 for row in sorted(rows,key=lambda r:r['competition']!=0):
  for k,v in row.get('parameters',{}).items():params[int(k)]=v
  removed={i for i,flag in enumerate(FLAGS)if not row.get('ui77_innate')and row.get('parameters',{}).get(str(flag))==0}
  for field in ['additional_skill_id','additional_skill']:
   if field in out:out[field]=[74 if sid in removed else sid for sid in out[field]]
 if int(cid)not in(518,473)and pid in ['88044950524330','89135066911146','106726716084650']:
  params[0]=9 if pid=='88044950524330'else 10
  for ix in range(1,14):params[ix]=2 if(ix==3 if pid=='88044950524330'else ix in [9,4])else 0
 if int(cid)in(518,473):
  from myleague_worlds import config as league_config
  profile=league_config()['classic_profiles'].get(pid)
  if profile and profile.get('competition',518)==int(cid):
   for ix in range(1,14):params[ix]=2
 out['parameters']=params
 if 'is_skill_added'in out:out['is_skill_added']='YES'if any(s!=74 for s in out.get('additional_skill_id',out.get('additional_skill',[])))else'NO'
 return out

def environment(fixture,rng,cfg):
 w=config()['weather'];winter=w['winter_start']<=fixture<=w['winter_end']
 if not winter and fixture>w['summer_end']:winter=rng.random()<w['late_winter_chance']
 return (cfg['winter']if winter else cfg['summer']),dict(weather=cfg['rain_weather']if rng.random()<w['rain_chance']else cfg['fine_weather'],time_zone=cfg['night']if rng.random()<w['night_chance']else cfg['day'])

def has_team(tid,cid):
 return any(r['team_id']==int(tid or 0)and r['competition']in [0,int(cid)]for r in config().get('teams',[]))
