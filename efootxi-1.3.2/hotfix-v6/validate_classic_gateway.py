from pathlib import Path
import argparse,sys,json,sqlite3,tempfile,hashlib,collections,copy
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;g=a.gateway;sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,my_league as league,club_store as store,season_rankings as ranks,gate_logic,ziru_data
class Bridge:
 @staticmethod
 def ensure_native_team(t):return 1
worlds.NATIVE_BRIDGE=Bridge;model.ATTRS=g/'outputs/reference/external-attrs';model.install();c=worlds.config();src=g/'outputs/efootball/local-club.sqlite3';sha=hashlib.sha256(src.read_bytes()).hexdigest();substitutes=json.loads((r/'classic-replacements.json').read_text())['rows'];assert len(substitutes)==47
original=json.loads((g/'outputs/reference/ziru-data/schedules/ml_schedule_518.json').read_text())['schedule_list'];round_count=len(original)
assert set(c['classic_teams'])==set(map(str,c['leagues']['518']['teams']))
source_rosters=ranks._rosters();tested=[]
with tempfile.TemporaryDirectory() as tmp:
 con=sqlite3.connect(Path(tmp)/'copy.db');con.row_factory=sqlite3.Row;ro=sqlite3.connect(src.as_uri()+'?mode=ro',uri=True);ro.backup(con);ro.close();inventory=[tuple(x) for x in con.execute('select * from gameplayers order by rowid')]
 for tid,team in c['classic_teams'].items():
  ids=c['native_rosters'][tid];assert len(ids)>=11 and len(set(ids))==len(ids);assert len({s['shirt'] for s in team['slots']})==len(ids)
  assert source_rosters[tid]==ids
  s=store.get_meta(con,league.KEY,'')
  out=league.select(con,{},dict(rqid='classic-'+tid,select_team_id=int(tid),select_compe_unit_id=518),session_token='classic-tests');assert out['result']=='NOERR'
  state=league.state(con);rows=league.fixtures(state);assert len(rows)==round_count
  assert len(league.ranking(state))==12
  for fx in rows:
   teams=[m[side+'_team_id'] for m in fx['match_list'] for side in ['home','away']];assert len(teams)==len(set(teams))
  prepared=league.prepare(con,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='prep-'+tid,cpu_level='NORMAL',match_category='SEASON'),session_token='classic-tests');assert prepared['result']=='NOERR' and prepared.get('player_list') is None
  entries=gate_logic.GateLogic({},conn=con)._home_entries(league.start_refs(con,{}));req=dict(msgid='CMD_START_GAME',rqid='start-'+tid,game_id=prepared['game_id'],match_category='SEASON',user_id=1)
  out=league.start(con,{},req,entries);assert out['result']=='NOERR'
  side='away' if league.state(con)['active']['side']=='HOME' else 'home';assert out['squad_data_'+side] is None
  assert [tuple(x) for x in con.execute('select * from gameplayers order by rowid')]==inventory
  tested.append(team['name'])
 # Rankings use actual full64 native keys; no ghost legend or substituted identity.
 state=league.state(con);state['team_id']=999999;state['played']={};state['active']=None
 for fx in league.fixtures(state)[:5]:
  matches=league.fixture_matches(state,fx);con.execute('BEGIN IMMEDIATE');ranks.record_fixture(con,state,fx['fixture'],matches);con.commit();record=json.loads(store.get_meta(con,ranks._scope(state)+'fixture_'+str(fx['fixture'])))
  for m in matches:
   for side in ['home','away']:
    tid=m[side+'_team_id'];events=[x for x in record['rows'] if x['team_id']==tid];assert sum(x['goal'] for x in events)==m[side+'_goals'];assert all(x['player_id'] in source_rosters[str(tid)] for x in events)
 assert con.execute('pragma quick_check').fetchone()[0]=='ok'
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
report=dict(status='CLASSIC_GATEWAY_PASS',device_tested=False,native_readiness_stubbed=True,teams=tested,slots=sum(len(t['slots']) for t in c['classic_teams'].values()),source_round_count=round_count,temporary_substitutions=47,checks=['all12 club selections, ranking12 teams, prepare/START with original native-only CPU payload','source Scottish fixture format retained, one match per team/round','actual GateLogic home-entry path; no pre-edited test inputs','own inventory unchanged, original DB unchanged, SQLite integrity','full64 CPU ranking events belong to selected real rosters and conserve team goals'])
(r/'classic-gateway-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
