"""Native-only My League rosters; no experimental inline opponent or START injection."""
import copy,json,hashlib
from pathlib import Path
CONFIG_PATH=Path(__file__).with_name('myleague_custom.json')
STAT_INDEX={'offensive_awareness':14,'defensive_awareness':15,'defensive_engagement':26,'tackling':24,'dribbling':17,'ball_control':18,'tight_possession':19,'finishing':20,'low_pass':21,'lofted_pass':22,'heading':23,'curl':28,'speed':34,'acceleration':38,'physical_contact':35,'kicking_power':37,'jumping':39,'aggression':25,'stamina':40}
EXPECTED_NATIVE_CONFIG_SHA='b57d39d81ea69fde667371acf6ab0fccb680e69ec2fa548f5126b7bb2f8c9130'
_config=None
_installed=False
NATIVE_BRIDGE=None # Test dependency only; actual Android uses the verified native loader.

def config():
 global _config
 if _config is None:
  d=json.loads(CONFIG_PATH.read_text(encoding='utf8'))
  if d.get('schema')!=2 or d.get('version')!='native-hotfix-v9':raise ValueError('v9 configuration required')
  for cid,row in d['leagues'].items():
   if len(row['teams'])!=len(set(row['teams'])) or set(row['tiers'])!=set(map(str,row['teams'])):raise ValueError('invalid league membership')
  for tid,ids in d['native_rosters'].items():
   if not tid.isdecimal() or not 0<int(tid)<2**18 or not 11<=len(ids)<=40 or len(ids)!=len(set(ids)) or any(type(pid)!=int or not 0<pid<2**63 for pid in ids):raise ValueError('invalid native base roster IDs')
  for collection in ['base_overrides','card_overrides']:
   for pid,row in d[collection].items():
    if not pid.isdecimal() or not 0<int(pid)<2**63:raise ValueError('invalid exact player ID')
    for key,value in row.get('stats',{}).items():
     if key not in STAT_INDEX or type(value)!=int or not 40<=value<=99:raise ValueError('invalid stat override')
    for flag in row.get('skill_flags_add',[])+row.get('skill_flags_remove',[]):
     if type(flag)!=int or not 70<=flag<=143:raise ValueError('invalid skill flag')
  for pid,rows in d.get('base_adjustments',{}).items():
   if not pid.isdecimal() or not 0<int(pid)<=0xffffffff:raise ValueError('invalid adjustment ID')
   for row in rows:
    if row['stat'] not in STAT_INDEX or row['delta'] not in (4,6) or row['below'] not in (84,100):raise ValueError('invalid adjustment')
  native={k:d[k] for k in ('native_rosters', 'base_overrides', 'card_overrides', 'base_adjustments', 'team_names', 'league_logos', 'shirt_overrides', 'global_player_rules', 'classic_teams', 'classic_profiles', 'visual_aliases', 'ovr_policy', 'match_environment', 'messi_ids', 'defender_skill_policy', 'league_names')};native['leagues']=d['leagues']
  if hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=EXPECTED_NATIVE_CONFIG_SHA:raise ValueError('native config differs from compiled v9; rebuild required')
  _config=d
 return _config

def schedule(teams,legs=2):
 if legs not in (2,3):raise ValueError("unsupported leg count")
 ring=list(teams);ring += [None] if len(ring)%2 else [];first=[];n=len(ring)
 for r in range(n-1):
  matches=[]
  for i in range(n//2):
   h,a=ring[i],ring[-i-1]
   if (r+i)%2:h,a=a,h
   if h is not None and a is not None:matches.append(dict(home_team_id=h,away_team_id=a,home_goals=0,away_goals=0))
  first.append(dict(fixture=r+1,match_list=matches,is_boss_match='NO'));ring=[ring[0],ring[-1]]+ring[1:-1]
 second=[dict(fixture=len(first)+i+1,match_list=[dict(home_team_id=m['away_team_id'],away_team_id=m['home_team_id'],home_goals=0,away_goals=0) for m in fx['match_list']],is_boss_match='NO') for i,fx in enumerate(first)]
 third=[dict(fixture=2*len(first)+i+1,match_list=copy.deepcopy(fx['match_list']),is_boss_match='NO') for i,fx in enumerate(first)]
 if legs==3:
  order={team:i for i,team in enumerate(teams)}
  for fx in third:
   for match in fx['match_list']:
    h,a=match['home_team_id'],match['away_team_id'];hi,ai=order[h],order[a];distance=(ai-hi)%len(teams)
    if distance>len(teams)/2 or (distance==len(teams)/2 and hi>ai):match['home_team_id'],match['away_team_id']=a,h
 return first+second+(third if legs==3 else [])

_adjustment_targets={}
def apply_global(params,pid,learned=()):
 power=config()['global_player_rules']['kicking_power'];original=params[37]
 if original>power['above']:params[37]=min(power['cap'],original+power['add'])
 if 4<=params[0]<=12 and not(params[127] or params[120] or set(learned)&{18,24}):params[103]=1
 return params

def edit_projection(player):
 out=copy.deepcopy(player);pid=str((out.get('gameplayer_id')or{}).get('id',0));rule=config()['card_overrides'].get(pid) or config()['base_overrides'].get(pid)
 for move in config().get('transfers',[]):
  if pid==str(move['player_id']):out['initial_base_team_id']=move['to_team']
 adjustments=config().get('base_adjustments',{}).get(pid,[])
 rule=rule or{}
 params=list(out.get('parameters')or[])
 if len(params)!=147:
  if rule or adjustments:raise ValueError('expected canonical147 for exact override')
  return out
 for row in adjustments:
  index=STAT_INDEX[row['stat']];key=(pid,index)
  if key not in _adjustment_targets:
   original=params[index];_adjustment_targets[key]=min(99,original+row['delta']) if original<row['below'] else original
  params[index]=_adjustment_targets[key]
 for key,value in rule.get('stats',{}).items():params[STAT_INDEX[key]]=value
 for flag in rule.get('skill_flags_add',[]):params[flag]=1
 for flag in rule.get('skill_flags_remove',[]):params[flag]=0
 learned=set(out.get('additional_skill_id')or[])|set(out.get('additional_skill')or[])
 apply_global(params,pid,learned)
 out['parameters']=params
 for name in ['additional_skill_id','additional_skill']:
  if name in out:out[name]=[74 if sid in rule.get('skill_ids_remove',[]) else sid for sid in out[name]]
 if 'is_skill_added' in out:out['is_skill_added']='YES' if any(x!=74 for x in out.get('additional_skill_id',out.get('additional_skill',[]))) else 'NO'
 return out

def _install_card_projection():
 import club_store as store,gate_logic,player_skills,player_parameters
 project=store._wire_project;detail=gate_logic.GateLogic._player_data
 def edited_project(player,shape='login'):return edit_projection(project(player,shape))
 def edited_detail(self,resp,req):
  out=detail(self,resp,req);found=out.get('gameplayer_list')or[]
  if found and out.get('original_parameters'):
   identity=found[0].get('gameplayer_id');source=store.player_by_key(self.conn,identity['id'],identity.get('serial'))
   baseline=list((source or{}).get('_careerplan_base_parameters') or player_parameters.owned_parameters(source)) if source else list(out['original_parameters'])
   temporary=edit_projection(dict(gameplayer_id=identity,parameters=baseline,additional_skill_id=(source or{}).get('additional_skill_id',[])))
   out['original_parameters']=temporary['parameters'];out['skillcard_id_list']=player_skills.selectable_skill_ids(found[0])
  return out
 store._wire_project=edited_project;gate_logic.GateLogic._player_data=edited_detail

def _bridge():
 if NATIVE_BRIDGE is not None:return NATIVE_BRIDGE
 import select_team_runtime
 return select_team_runtime

def _ensure_native(team):return _bridge().ensure_native_team(team)

def environment_for(s,available=None):
 from myleague_realism import _rng,_seed
 cfg=config()['match_environment'];fixture=int(s['fixture']);snow=8<=fixture<=14
 rng=_rng('match-environment-v7',_seed(s),s['competition_id'],s['team_id'],s['season'],fixture)
 season=cfg['winter'] if snow or rng.random()<.5 else cfg['summer']
 weather=cfg['snow_weather'] if snow else cfg['rain_weather'] if rng.random()<.35 else cfg['fine_weather']
 daytime=cfg['day'] if rng.random()<.5 else cfg['night']
 choices=cfg['stadium_ids'] if available is None else available
 if not choices:raise ValueError('no installed permitted stadium supports requested conditions')
 return dict(weather=weather,season_type=season,time_zone=daytime,stadium_id=rng.choice(choices),fixture=fixture,snow_required=snow,version='native-hotfix-v9')

def _environment_diagnostic(**row):
 try:Path(__file__).with_name('myleague-environment-status.json').write_text(json.dumps(dict(version='native-hotfix-v9',device_verified=False,**row),indent=2))
 except OSError:pass

def _prepare_environment(s):
 _bridge().activate_context(int(s['competition_id']))
 from myleague_realism import _rng,_seed
 cid=int(s['competition_id']);cfg=config()['match_environment'];fixture=int(s['fixture'])
 if str(cid) not in cfg['home_assignment_scope']:
  return dict(weather=cfg['fine_weather'],season_type=cfg['summer'],time_zone=cfg['day'],stadium_id=0,fixture=fixture)
 import my_league as league
 _,_,match=league._info_fixture(s,league.fixtures(s))
 # fixtures() may initialize a missing legacy seed: resolve it before drawing.
 rng=_rng('weather-v9',_seed(s),cid,s['team_id'],s['season'],fixture)
 winter=8<=fixture<=14 or rng.random()<.5
 host=match['home_team_id'] if match else s['team_id'];stadium=cfg['home_stadiums'].get(str(host),0)
 if stadium not in cfg['stadium_ids']:raise ValueError('home club lacks permitted stadium assignment')
 if _bridge().set_environment(cid,stadium,False)!=1:raise ValueError('native home stadium selector not ready')
 phase=_rng('weather-cycle-v9',_seed(s),cid,s['season']).randrange(4)
 condition=cfg['weather_cycle'][(fixture-1+phase)%4]
 env=dict(weather=condition['weather'],season_type=cfg['winter'] if winter else cfg['summer'],time_zone=condition['time_zone'],stadium_id=stadium,home_team_id=host,stadium_applied='NATIVE_TEAM_FIELD',snow_applied=False,snow_required=8<=fixture<=14,fixture=fixture,version='native-hotfix-v9')
 _environment_diagnostic(state='HOME_STADIUM_ASSIGNED_WEATHER_ENUMS',environment=env,reason='four weather/time protocol states; native parameters9/10 enabled only for six allowed stadiums; snow stays disabled; renderer verification pending')
 return env


def _messi(pid):
 # Exact known identities; the native profile also knows all English source IDs.
 return str(pid) in config().get('messi_ids',[]) or str(pid) in [p for p,t in config()['classic_profiles'].items() if t['name']=='Lionel Messi'] or str(pid)=='7511'


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
 prepare=league.prepare;start=league.start;info=league.info
 def native_prepare(conn,req,**kwargs):
  _retire_unsafe_active(conn,league)
  s=league.state(conn)
  if s and not s['completed']:
   _bridge().activate_context(int(s['competition_id']))
   try:env=_prepare_environment(s)
   except ValueError as exc:
    _environment_diagnostic(state='BLOCKED_MISSING_STADIUM_OR_NATIVE_HOOK',error=str(exc),fixture=s['fixture'])
    return league.fail('CMD_GET_VSCOM_OPPONENT',req)
   _,match,_=league.current(s);team=match['away_team_id'] if match['home_team_id']==s['team_id'] else match['home_team_id']
   if str(team) in config()['native_rosters']:
    status=_ensure_native(team)
    if status!=1:
     diagnostic=dict(team=team,status=status,command='CMD_GET_VSCOM_OPPONENT',version='native-hotfix-v9')
     store.log_event(conn,'v4_native_roster_not_ready',diagnostic);conn.commit()
     try:Path(__file__).with_name('myleague-native-error.json').write_text(json.dumps(diagnostic,indent=2))
     except OSError:pass
     return league.fail('CMD_GET_VSCOM_OPPONENT',req)
  out=prepare(conn,req,**kwargs)
  # Original My League schema. No separate VS-COM player/coach/squad payload.
  if out.get('result')=='NOERR' and any(out.get(k) is not None for k in ['player_list','squad_data','coach_data']):raise ValueError('unsafe inline opponent rejected')
  if out.get('result')=='NOERR' and s and not s['completed']:
   league.begin(conn)
   try:
    fresh=league.state(conn)
    if fresh.get('active'):
     fresh['active']['environment']=env;league.save(conn,fresh)
    conn.commit()
   except Exception:conn.rollback();raise
  return out
 def native_info(conn,resp,req):
  out=info(conn,resp,req);s=league.state(conn)
  if s:
   _bridge().activate_context(int(s['competition_id']))
   view=dict(s,fixture=out.get('fixture',s['fixture']))
   env=_prepare_environment(view)
   for key in ['weather','season_type','time_zone']:out[key]=env[key]
  return out
 def native_start(conn,resp,req,home_entries):
  if _retire_unsafe_active(conn,league):return league.fail('CMD_START_GAME',req)
  s=league.state(conn);a=(s or{}).get('active')or{};team=(a.get('opponent')or{}).get('team_data',{}).get('base_team_id')
  if str(team) in config()['native_rosters'] and _ensure_native(team)!=1:return league.fail('CMD_START_GAME',req)
  # GateLogic._home_entries bypasses wire_player. Apply exact-card edits here too,
  # after learned-skill overlay, so Marseille Turn cannot be added back at START.
  if s:
   try:_prepare_environment(s)
   except ValueError as exc:
    _environment_diagnostic(state='BLOCKED_MISSING_STADIUM_OR_NATIVE_HOOK',error=str(exc),fixture=s['fixture'])
    return league.fail('CMD_START_GAME',req)
  from myleague_balance import project
  edited=[project(edit_projection(p),s['competition_id'],_messi((p.get('gameplayer_id')or{}).get('id'))) for p in home_entries]
  out=start(conn,resp,req,edited)
  # Uniform IDs and the team ID must point to the same original donor. The
  # native kit-path hook alone cannot fix inherited Scottish wire uniform IDs.
  if out.get('result')=='NOERR':
   for side in ['home','away']:
    key='uniform_list_'+side;row=out.get(key)
    if isinstance(row,dict):
     tid=row.get('base_team_id');donor=config()['visual_aliases'].get(str(tid))
     if donor:
      import team_kits
      row.update(base_team_id=donor,uniform_list=team_kits.uniform_ids(donor))
  return out
 league.prepare=native_prepare;league.start=native_start;league.info=native_info

def install():
 global _installed
 if _installed:return False
 import my_league as league,season_rankings as rankings,ziru_data
 cfg=config();canonical=rankings._canonical_data()
 if not canonical:raise ValueError('native roster data required')
 names=copy.deepcopy(ziru_data.team_names());names.update(cfg.get('team_names',{}));ziru_data._cache['team_names.json']=names
 registry=copy.deepcopy(ziru_data.competition_registry())
 for cid,definition in cfg['leagues'].items():
  comp=registry['competitions'][cid]
  for tid in comp['team_ids']:
   if registry['team_to_competition'].get(str(tid))==int(cid):registry['team_to_competition'].pop(str(tid))
  ids=definition['teams'];comp.update(name=definition['name'],team_count=len(ids),team_ids=ids,teams=[dict(team_id=t,name=names.get(str(t),{}).get('name',str(t)),short=names.get(str(t),{}).get('short','')) for t in ids])
  for tid in ids:registry['team_to_competition'][str(tid)]=int(cid)
  if not definition.get('preserve_original_schedule'):ziru_data._cache['schedules/ml_schedule_'+cid+'.json']={'schedule_list':schedule(ids,definition.get('legs',2))}
 ziru_data._cache['ml_competition_registry.json']=registry
 for tid,players in {**cfg.get('simulation_rosters',{}),**cfg['native_rosters']}.items():canonical['rosters'][tid]=list(players)
 for pid,row in cfg.get('classic_profiles',{}).items():canonical['positions'][pid]=row['roles'][0]
 _install_card_projection();_install_native_match_path(league)
 import gate_logic
 original_start=gate_logic.GateLogic._start_game;original_opponent=gate_logic.GateLogic._vscom_opponent
 def scoped_start(self,resp,req):
  import match_protocol
  try:is_myleague=match_protocol.resolve_mode(self.conn,req,include_receipts=False)==match_protocol.SEASON
  except (ValueError,match_protocol.MatchError):is_myleague=False
  if not is_myleague:_bridge().activate_context(0)
  return original_start(self,resp,req)
 def scoped_opponent(self,mid,resp,req):
  if not league.is_season(req):_bridge().activate_context(0)
  return original_opponent(self,mid,resp,req)
 gate_logic.GateLogic._start_game=scoped_start;gate_logic.GateLogic._vscom_opponent=scoped_opponent
 _installed=True;return True
