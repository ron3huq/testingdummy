"""Native-only My League rosters; no experimental inline opponent or START injection."""
import copy,json,hashlib
from pathlib import Path
CONFIG_PATH=Path(__file__).with_name('myleague_custom.json')
STAT_INDEX={'offensive_awareness':14,'dribbling':17,'ball_control':18,'tight_possession':19,'finishing':20,'low_pass':21,'lofted_pass':22,'heading':23,'curl':28,'speed':34,'acceleration':35,'physical_contact':36,'stamina':40}
EXPECTED_NATIVE_CONFIG_SHA='c4e382bd463667dd433164a3aefefcf1bb98a201cb488611f36dc1eb0b98f4da'
_config=None
_installed=False
NATIVE_BRIDGE=None # Test dependency only; actual Android uses the verified native loader.

def config():
 global _config
 if _config is None:
  d=json.loads(CONFIG_PATH.read_text(encoding='utf8'))
  if d.get('schema')!=2 or d.get('version')!='native-hotfix-v3':raise ValueError('v3 configuration required')
  for cid,row in d['leagues'].items():
   if len(row['teams'])!=len(set(row['teams'])) or set(row['tiers'])!=set(map(str,row['teams'])):raise ValueError('invalid league membership')
  for collection in ['base_overrides','card_overrides']:
   for pid,row in d[collection].items():
    if not pid.isdecimal() or not 0<int(pid)<2**63:raise ValueError('invalid exact player ID')
    for key,value in row.get('stats',{}).items():
     if key not in STAT_INDEX or type(value)!=int or not 40<=value<=99:raise ValueError('invalid stat override')
    for flag in row.get('skill_flags_add',[])+row.get('skill_flags_remove',[]):
     if type(flag)!=int or not 70<=flag<=143:raise ValueError('invalid skill flag')
  native=dict(native_rosters=d['native_rosters'],base_overrides=d['base_overrides'],league_teams={k:v['teams'] for k,v in d['leagues'].items()})
  if hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=EXPECTED_NATIVE_CONFIG_SHA:raise ValueError('native config differs from compiled v3; rebuild required')
  _config=d
 return _config

def schedule(teams):
 ring=list(teams);ring += [None] if len(ring)%2 else [];first=[];n=len(ring)
 for r in range(n-1):
  matches=[]
  for i in range(n//2):
   h,a=ring[i],ring[-i-1]
   if (r+i)%2:h,a=a,h
   if h is not None and a is not None:matches.append(dict(home_team_id=h,away_team_id=a,home_goals=0,away_goals=0))
  first.append(dict(fixture=r+1,match_list=matches,is_boss_match='NO'));ring=[ring[0],ring[-1]]+ring[1:-1]
 return first+[dict(fixture=len(first)+i+1,match_list=[dict(home_team_id=m['away_team_id'],away_team_id=m['home_team_id'],home_goals=0,away_goals=0) for m in fx['match_list']],is_boss_match='NO') for i,fx in enumerate(first)]

def edit_projection(player):
 out=copy.deepcopy(player);pid=str((out.get('gameplayer_id')or{}).get('id',0));rule=config()['card_overrides'].get(pid) or config()['base_overrides'].get(pid)
 if not rule:return out
 params=list(out.get('parameters')or[])
 if len(params)!=147:raise ValueError('expected canonical 147 parameters for exact player override')
 for key,value in rule.get('stats',{}).items():params[STAT_INDEX[key]]=value
 for flag in rule.get('skill_flags_add',[]):params[flag]=1
 for flag in rule.get('skill_flags_remove',[]):params[flag]=0
 out['parameters']=params
 for name in ['additional_skill_id','additional_skill']:
  if name in out:out[name]=[sid for sid in out[name] if sid not in rule.get('skill_ids_remove',[])]
 if 'is_skill_added' in out:out['is_skill_added']='YES' if any(x!=74 for x in out.get('additional_skill_id',out.get('additional_skill',[]))) else 'NO'
 return out

def _install_card_projection():
 import club_store as store,gate_logic,player_skills
 project=store._wire_project;detail=gate_logic.GateLogic._player_data
 def edited_project(player,shape='login'):return edit_projection(project(player,shape))
 def edited_detail(self,resp,req):
  out=detail(self,resp,req);found=out.get('gameplayer_list')or[]
  if found and out.get('original_parameters'):
   identity=found[0].get('gameplayer_id');temporary=edit_projection(dict(gameplayer_id=identity,parameters=out['original_parameters']))
   out['original_parameters']=temporary['parameters'];out['skillcard_id_list']=player_skills.selectable_skill_ids(found[0])
  return out
 store._wire_project=edited_project;gate_logic.GateLogic._player_data=edited_detail

def _ensure_native(team):
 bridge=NATIVE_BRIDGE
 if bridge is None:
  import select_team_runtime as bridge
 return bridge.ensure_native_team(team)

def _retire_unsafe_active(conn,league):
 import club_store as store,match_protocol as protocol
 s=league.state(conn);a=(s or{}).get('active')or{};op=a.get('opponent')or{}
 if not (op.get('player_list') or op.get('squad_data')):return False
 # V2 custom opponent was persisted before a crash. Quarantine its receipt/plan,
 # retain fixture/scores and force a fresh native-only preparation.
 league.begin(conn)
 try:
  s=league.state(conn);a=s.get('active')or{};gid=a.get('game_id')
  if gid:
   store.set_meta(conn,'v3_quarantined_inline_'+str(gid),json.dumps(a))
   store.set_meta(conn,'efootxi_match_abandoned_'+protocol.SEASON+'_'+str(gid),json.dumps(dict(game_id=gid,mode=protocol.SEASON,started=bool(a.get('started')),reason='v2_inline_crash_recovery',season=s['season'])))
  s['active']=None;league.save(conn,s);conn.commit();return True
 except Exception:conn.rollback();raise

def _install_native_match_path(league):
 import club_store as store
 prepare=league.prepare;start=league.start
 def native_prepare(conn,req,**kwargs):
  _retire_unsafe_active(conn,league)
  s=league.state(conn)
  if s and not s['completed']:
   _,match,_=league.current(s);team=match['away_team_id'] if match['home_team_id']==s['team_id'] else match['home_team_id']
   if str(team) in config()['native_rosters']:
    status=_ensure_native(team)
    if status!=1:
     store.log_event(conn,'v3_native_roster_not_ready',dict(team=team,status=status));conn.commit();return league.fail('CMD_GET_VSCOM_OPPONENT',req)
  out=prepare(conn,req,**kwargs)
  # Original My League schema. No separate VS-COM player/coach/squad payload.
  if out.get('result')=='NOERR' and any(out.get(k) is not None for k in ['player_list','squad_data','coach_data']):raise ValueError('unsafe inline opponent rejected')
  return out
 def native_start(conn,resp,req,home_entries):
  if _retire_unsafe_active(conn,league):return league.fail('CMD_START_GAME',req)
  s=league.state(conn);a=(s or{}).get('active')or{};team=(a.get('opponent')or{}).get('team_data',{}).get('base_team_id')
  if str(team) in config()['native_rosters'] and _ensure_native(team)!=1:return league.fail('CMD_START_GAME',req)
  # GateLogic._home_entries bypasses wire_player. Apply exact-card edits here too,
  # after learned-skill overlay, so Marseille Turn cannot be added back at START.
  edited=[edit_projection(p) for p in home_entries]
  return start(conn,resp,req,edited)
 league.prepare=native_prepare;league.start=native_start

def install():
 global _installed
 if _installed:return False
 import my_league as league,season_rankings as rankings,ziru_data
 cfg=config();canonical=rankings._canonical_data()
 if not canonical:raise ValueError('native roster data required')
 names=ziru_data.team_names();registry=copy.deepcopy(ziru_data.competition_registry())
 for cid,definition in cfg['leagues'].items():
  comp=registry['competitions'][cid]
  for tid in comp['team_ids']:
   if registry['team_to_competition'].get(str(tid))==int(cid):registry['team_to_competition'].pop(str(tid))
  ids=definition['teams'];comp.update(team_ids=ids,teams=[dict(team_id=t,name=names.get(str(t),{}).get('name',str(t)),short=names.get(str(t),{}).get('short','')) for t in ids])
  for tid in ids:registry['team_to_competition'][str(tid)]=int(cid)
  ziru_data._cache['schedules/ml_schedule_'+cid+'.json']={'schedule_list':schedule(ids)}
 ziru_data._cache['ml_competition_registry.json']=registry
 for tid,players in cfg['native_rosters'].items():canonical['rosters'][tid]=list(players)
 _install_card_projection();_install_native_match_path(league)
 _installed=True;return True
