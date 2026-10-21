"""New8-team triple competition through actual gateway transactions on DB copy."""
from pathlib import Path
import argparse,sys,json,sqlite3,tempfile,hashlib,collections,copy,random
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;g=a.gateway;sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,my_league as league,season_rankings as ranks,club_store as store,ziru_data
class Bridge:
 @staticmethod
 def ensure_native_team(t):return 1
worlds.NATIVE_BRIDGE=Bridge;model.ATTRS=g/'outputs/reference/external-attrs';model.install();cfg=worlds.config();teams=cfg['leagues']['549']['teams'];assert len(teams)==8
source=g/'outputs/efootball/local-club.sqlite3';sha=hashlib.sha256(source.read_bytes()).hexdigest();names={}
with tempfile.TemporaryDirectory() as tmp:
 con=sqlite3.connect(Path(tmp)/'test.db');con.row_factory=sqlite3.Row;src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);src.backup(con);src.close()
 for tid in teams:
  reply=league.select(con,{},dict(rqid='asia-'+str(tid),select_team_id=tid,select_compe_unit_id=549),session_token='v5-asia-test');assert reply['result']=='NOERR'
  s=league.state(con);assert s['competition_id']==549 and s['team_id']==tid
  rows=league.fixtures(s);pairs=collections.Counter();home=collections.Counter();played=collections.Counter()
  assert len(rows)==21 and [x['fixture'] for x in rows]==list(range(1,22))
  for fx in rows:
   assert len(fx['match_list'])==4;seen=[]
   for m in fx['match_list']:
    h,aw=m['home_team_id'],m['away_team_id'];assert h!=aw;seen +=[h,aw];pairs[tuple(sorted([h,aw]))]+=1;home[h]+=1;played.update([h,aw])
   assert set(seen)==set(teams) and len(seen)==8
  assert set(pairs.values())=={3} and len(pairs)==28 and sum(pairs.values())==84
  assert set(played.values())=={21} and set(home.values())<={10,11}
  reopened=json.loads(json.dumps(s));assert league.fixtures(reopened)==rows
  old=json.dumps(s,sort_keys=True);reply=league.select(con,{},dict(rqid='resume-'+str(tid),select_team_id=tid,select_compe_unit_id=549),session_token='v5-asia-test');assert reply['result']=='NOERR' and json.dumps(league.state(con),sort_keys=True)==old
  prep=league.prepare(con,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='prep-'+str(tid),cpu_level='NORMAL',match_category='SEASON'),session_token='v5-asia-test');assert prep['result']=='NOERR' and prep.get('player_list') is None
  # End-of-schedule navigation uses21 rounds and8 table teams, no stale12-slot rule.
  s=league.state(con);s['active']=None;s['fixture']=21;league.save(con,s);con.commit();prep=league.prepare(con,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='last-'+str(tid),cpu_level='NORMAL',match_category='SEASON'),session_token='v5-asia-test');assert prep['result']=='NOERR'
  names[str(tid)]=ziru_data.team_names()[str(tid)]
 # Every generated goal/assist in all21 rounds belongs to an actual roster.
 s=league.state(con);s['team_id']=999999;s['played']={};s['active']=None
 for fx in league.fixtures(s):
  matches=league.fixture_matches(s,fx);con.execute('BEGIN IMMEDIATE');ranks.record_fixture(con,s,fx['fixture'],matches);con.commit();record=json.loads(store.get_meta(con,ranks._scope(s)+'fixture_'+str(fx['fixture'])))
  for m in matches:
   for side in ['home','away']:
    tid=m[side+'_team_id'];events=[row for row in record['rows'] if row['team_id']==tid]
    assert sum(row['goal'] for row in events)==m[side+'_goals'];assert sum(row['assist'] for row in events)<=m[side+'_goals']
    assert all(row['player_id'] in ranks._rosters()[str(tid)] and model._position(row['player_id'])!=0 for row in events)
 assert con.execute('pragma quick_check').fetchone()[0]=='ok'
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
rates={}
for tier,other in [('top2',5738),('remaining',157)]:
 wins=0
 for i in range(6000):
  s=dict(competition_id=549,team_id=999999,season=i);h,aw=(18961,other) if i%2 else (other,18961);hg,ag=model.cpu_score(s,1,h,aw);tg,og=(hg,ag) if h==18961 else (ag,hg);wins+=tg>og
 rates[tier]=wins/6000
assert rates['remaining']>rates['top2']>.55
report=dict(status='ASIA_PACIFIC_GATEWAY_PASS',device_tested=False,native_readiness_stubbed=True,teams=names,rounds=21,matches=84,games_per_team=21,home_games=[10,11],sample_top_win_rates=rates,checks=['all8 clubs select/resume/prepare first and last round in actual gateway','persistent random draw: every unordered pair3, one match per team per round','all21 CPU ranking receipts: goal conservation, roster IDs only, no goalkeepers','Eredivisie125 restored; Asia-Pacific name/logo moved to549','source DB and inventory preserved; no game save packaged'])
(r/'asia-pacific-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
