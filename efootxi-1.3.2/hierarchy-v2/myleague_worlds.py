"""Runtime league/roster overlay. Never replaces user's registry, schedule files or DB."""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CONFIG_PATH=Path(__file__).with_name('myleague_custom.json')
STAT_INDEX={'offensive_awareness':14,'finishing':20,'low_pass':21,'lofted_pass':22,'curl':28,'speed':34,'acceleration':35,'stamina':40}
EXPECTED_TEAMS={'122': [101, 102, 103, 114, 100, 173, 179, 108, 109, 172, 121, 119, 120, 181, 127, 125, 327, 130], '566': [5763, 5750, 1031, 5759, 5752, 54, 52, 53, 1184, 57, 55, 1010, 1032, 1026, 56, 5748, 1011, 1012], '128': [7, 50, 8, 5, 45, 6, 10, 9, 14, 12, 24, 49, 44, 40, 32, 39, 16, 17, 38, 1174]}
_config=None
_installed=False

def config():
 global _config
 if _config is None:
  _config=json.loads(CONFIG_PATH.read_text(encoding='utf8'))
  if _config.get('schema')!=2:raise ValueError('unsupported custom league config')
  for cid,ids in EXPECTED_TEAMS.items():
   row=_config['leagues'][cid]
   if row['teams']!=ids or set(row['tiers'])!=set(map(str,ids)):raise ValueError('team IDs differ from compiled native patch')
   if any(type(t)!=int or not 0<=t<=10 for t in row['tiers'].values()):raise ValueError('invalid hierarchy tier')
  for tid,ids in _config['custom_rosters'].items():
   if int(tid) not in {t for row in _config['leagues'].values() for t in row['teams']} or not 11<=len(ids)<=40 or len(ids)!=len(set(ids)) or any(type(p)!=int or not 0<p<262144 for p in ids):raise ValueError('invalid custom roster')
  if any(type(b) not in (int,float) or not 0<b<=10 for b in _config['scorer_boosts'].values()):raise ValueError('invalid scorer boost')
  import player_skills
  for pid,override in _config.get('player_overrides',{}).items():
   if not pid.isdecimal() or not 0<int(pid)<262144 or set(override)-{'stats','skills_add'}:raise ValueError('invalid base-player override')
   for key,value in override.get('stats',{}).items():
    if key not in STAT_INDEX or type(value)!=int or not 40<=value<=99:raise ValueError('unsupported stat/value')
   skills=override.get('skills_add',[])
   if not isinstance(skills,list) or any(type(s)!=int or s not in player_skills.SELECTABLE_SKILL_IDS for s in skills):raise ValueError('unsupported native skill ID')
 return _config

def schedule(teams):
 # Circle-method double round robin, including proper byes for odd leagues.
 ring=list(teams);ring += [None] if len(ring)%2 else []
 first=[];n=len(ring)
 for r in range(n-1):
  matches=[]
  for i in range(n//2):
   h,a=ring[i],ring[-i-1]
   if (r+i)%2:h,a=a,h
   if h is not None and a is not None:matches.append(dict(home_team_id=h,away_team_id=a,home_goals=0,away_goals=0))
  first.append(dict(fixture=r+1,match_list=matches,is_boss_match='NO'))
  ring=[ring[0],ring[-1]]+ring[1:-1]
 second=[dict(fixture=len(first)+i+1,match_list=[dict(home_team_id=m['away_team_id'],away_team_id=m['home_team_id'],home_goals=0,away_goals=0) for m in fx['match_list']],is_boss_match='NO') for i,fx in enumerate(first)]
 return first+second

def _custom_squad(conn,team):
 import opponent_squad as squad
 import ziru_data,club_store as store
 cfg=config();ids=cfg['custom_rosters'][str(team)];players=[]
 for i,pid in enumerate(ids):
  card=squad._library_card(conn,pid)
  if not card or int(card.get('gameplayer_id',{}).get('id',0))!=pid:raise ValueError('Custom team base card missing: '+str(pid))
  card=copy.deepcopy(card)
  override=cfg.get('player_overrides',{}).get(str(pid),{})
  for name,value in override.get('stats',{}).items():card['parameters'][STAT_INDEX[name]]=value
  import player_skills
  for sid in override.get('skills_add',[]):card['parameters'][player_skills.PARAMETER_BY_SKILL[sid]]=1
  player=store.wire_player(card,'list');params=list(player.get('parameters') or [])
  if not 145<=len(params)<=149:raise ValueError('Custom team parameter layout unsupported')
  if 0<=params[0]<13:params[1+params[0]]=2
  player['parameters']=params+[0]*(149-len(params));player['gameplayer_id']={'id':pid,'serial':903000000+team*1000+i};player['uniform_number']=i+1
  players.append(player)
 template=ziru_data.vscom_opponent();roles,_=squad._system_formation(template)
 positions=[squad.CARD_POSITION_NAMES[p['parameters'][0]] for p in players]
 starting,_=squad.slot_order(roles,positions,11)
 if len(starting)!=11 or len(set(starting))!=11:raise ValueError('Custom team starting XI unavailable')
 order=starting+[i for i in range(len(players)) if i not in starting];players=[players[i] for i in order]
 for i,p in enumerate(players[:11]):p['parameters'][1+squad.FORMATION_ROLE_CODES[roles[i]]]=2
 data=copy.deepcopy(template['squad_data']);data['team_id']=team
 data['player_list']=[dict(gameplayer_id=p['gameplayer_id'],uniform_number=p['uniform_number']) for p in players]
 plan=data['squad_gameplan'];native=next(v for v in plan['formation'] if v.get('use_multi_formation')=='NO')
 plan['formation']=[copy.deepcopy(native) for _ in plan['formation']]
 settings=plan['match_plan_settings'];settings['order']=list(range(len(players)))
 if settings.get('captain',255)>=len(players):settings['captain']=0
 for key in ['set_piece_taker','df_overlap_setplay']:
  if isinstance(settings.get(key),list):settings[key]=[v if type(v)==int and 0<=v<len(players) else 255 for v in settings[key]]
 return dict(player_list=players,squad_data=data,coach_data=copy.deepcopy(template.get('coach_data')))

def _install_bayern(league):
 import club_store as store,match_protocol as protocol
 prepare=league.prepare;start=league.start
 def prepare_custom(conn,req,**kwargs):
  out=prepare(conn,req,**kwargs)
  if out.get('result')!='NOERR' or str((out.get('team_data')or{}).get('base_team_id')) not in config()['custom_rosters']:return out
  season=league.state(conn);active=season['active']
  if active.get('started') or active['opponent'].get('player_list'):return out
  payload=_custom_squad(conn,out['team_data']['base_team_id']) # Must resolve the exact Bayern players; never substitute Monaco/other players.
  league.begin(conn)
  try:
   season=league.state(conn);active=season['active']
   if active['game_id']!=out['game_id'] or active.get('started'):raise protocol.MatchError('Custom team active match changed')
   active['opponent'].update(copy.deepcopy(payload));league.save(conn,season);conn.commit();out.update(payload);return out
  except Exception:conn.rollback();raise
 def start_custom(conn,resp,req,home_entries):
  season=league.state(conn);active=(season or{}).get('active')or{};op=active.get('opponent')or{}
  if str((op.get('team_data')or{}).get('base_team_id')) in config()['custom_rosters'] and not op.get('player_list') and not active.get('started'):raise protocol.MatchError('Custom squad was not prepared')
  out=start(conn,resp,req,home_entries)
  if out.get('result')=='NOERR' and str((op.get('team_data')or{}).get('base_team_id')) in config()['custom_rosters'] and op.get('player_list'):
   physical='away' if active['side']=='HOME' else 'home'
   data=copy.deepcopy(op['squad_data']);data['player_list']=copy.deepcopy(op['player_list']);out['squad_data_'+physical]=data
  return out
 league.prepare=prepare_custom;league.start=start_custom

def install():
 global _installed
 if _installed:return False
 import my_league as league,season_rankings as rankings,ziru_data
 cfg=config();names=ziru_data.team_names();registry=copy.deepcopy(ziru_data.competition_registry())
 for cid,definition in cfg['leagues'].items():
  comp=registry['competitions'][cid];original=comp['team_ids']
  for tid in original:
   if registry['team_to_competition'].get(str(tid))==int(cid):registry['team_to_competition'].pop(str(tid))
  ids=definition['teams'];comp.update(team_ids=ids,teams=[dict(team_id=t,name=names.get(str(t),{}).get('name',str(t)),short=names.get(str(t),{}).get('short','')) for t in ids])
  for tid in ids:registry['team_to_competition'][str(tid)]=int(cid)
  ziru_data._cache['schedules/ml_schedule_'+cid+'.json']={'schedule_list':schedule(ids)}
 ziru_data._cache['ml_competition_registry.json']=registry
 canonical=rankings._canonical_data()
 if not canonical:raise ValueError('canonical native rosters required')
 # Use native rosters except explicit Bayern127 and Brazil45 squads in config.
 for tid,players in cfg['custom_rosters'].items():canonical['rosters'][tid]=list(players)
 _install_bayern(league)
 _installed=True
 return True
