"""Validate against the supplied Android gateway; never open a user's live save for writing."""
import argparse,collections,copy,hashlib,json,sqlite3,statistics,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--gateway',required=True,type=Path);p.add_argument('--seasons',type=int,default=300);a=p.parse_args()
gateway=a.gateway.resolve();sys.path[:0]=[str(Path(__file__).parent),str(gateway/'work/tools')]
import my_league as league
import season_rankings as ranks
import club_store as store
import myleague_realism as mod
mod.ATTRS=gateway/'outputs/reference/external-attrs'
old_fixtures=league.fixtures;old_scores=league.fixture_matches
checks=[]
assert mod.install() and not mod.install()
def season(seed=None,team=101):
 s=dict(team_id=team,competition_id=122,fixture=1,played={},completed=False,active=None,cpu_level='NORMAL',season=1)
 if seed is not None:s[mod.META]=dict(seed=str(seed),version=mod.VERSION)
 return s
def pairs(rows):return collections.Counter((m['home_team_id'],m['away_team_id']) for fx in rows for m in fx['match_list'])
registry=json.loads((gateway/'outputs/reference/ziru-data/ml_competition_registry.json').read_text())
for key,comp in registry['competitions'].items():
 s=season('all-leagues');s['competition_id']=int(key)
 original=old_fixtures(s);actual=league.fixtures(s)
 assert pairs(original)==pairs(actual)
 assert [fx['fixture'] for fx in original]==[fx['fixture'] for fx in actual]
 for fx in actual:
  ids=[m[side+'_team_id'] for m in fx['match_list'] for side in ('home','away')]
  assert len(ids)==len(set(ids))
checks.append('all registered competitions preserve directed pairs, round IDs, byes and one match per team per round')
s=season();rows=league.fixtures(s);assert s[mod.META]['seed']
assert league.fixtures(s)==rows
s['schedule_v2']=rows;assert league.fixtures(json.loads(json.dumps(s)))==rows
assert len({json.dumps(league.fixtures(season(i)),sort_keys=True) for i in range(100)})==100
checks.append('draw persists across reads/JSON reload and 100 seed draws differ')
legacy=season();legacy['schedule_v2']=old_fixtures(legacy)
for fx in legacy['schedule_v2'][:10]:legacy['played'][str(fx['fixture'])]={'matches':old_scores(legacy,fx),'result':'DRAW'}
legacy['fixture']=11;legacy['active']={'fixture':11,'side':'HOME','started':True,'game_id':123}
before=copy.deepcopy(legacy)
assert league.fixtures(legacy)==before['schedule_v2']
for fx in legacy['schedule_v2'][:10]:assert league.fixture_matches(legacy,fx)==before['played'][str(fx['fixture'])]['matches']
assert legacy==before
current=legacy['schedule_v2'][10]
assert league.fixture_matches(legacy,current)==league.fixture_matches(json.loads(json.dumps(legacy)),current)
assert legacy==before
checks.append('10 played rounds, active match and existing schedule unchanged; future preview/reload stable')
for team in [108,109,114,173]:
 roster=ranks._rosters()[str(team)];pool=mod.weighted_roster(None,roster)
 assert set(pool)<=set(roster)
 assert all(mod._position(pid)!=0 for pid in pool)
checks.append('simulated player IDs belong to native team roster; no GK scorers')
# Real gateway transactions on a NEW database copy. No changes to owned/inventory tables.
source=gateway/'outputs/efootball/local-club.sqlite3';source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
def inventory(conn):
 result={}
 for (name,) in conn.execute("select name from sqlite_master where type='table' and name not in ('meta','events','sqlite_sequence')"):
  data=conn.execute('select * from "'+name.replace('"','""')+'"').fetchall()
  result[name]=hashlib.sha256(repr([tuple(x) for x in data]).encode()).hexdigest()
 return result
with tempfile.TemporaryDirectory() as tmp:
 db=Path(tmp)/'copy.sqlite3';src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);conn=sqlite3.connect(db);src.backup(conn);src.close();conn.row_factory=sqlite3.Row
 before_inv=inventory(conn)
 reply=league.select(conn,{},dict(rqid='realism-select',select_team_id=101,select_compe_unit_id=122),session_token='realism-tests')
 assert reply['result']=='NOERR'
 saved=league.state(conn);assert mod.META in saved and 'schedule_v2' in saved
 signature=json.dumps(saved,sort_keys=True)
 reply=league.select(conn,{},dict(rqid='realism-resume',select_team_id=101,select_compe_unit_id=122),session_token='realism-tests')
 assert reply['result']=='NOERR' and json.dumps(league.state(conn),sort_keys=True)==signature
 fx=league.fixtures(saved)[0];matches=league.fixture_matches(saved,fx)
 conn.execute('BEGIN IMMEDIATE');ranks.record_fixture(conn,saved,1,matches);conn.commit()
 key=ranks._scope(saved)+'fixture_1';raw=store.get_meta(conn,key,'');record=json.loads(raw)
 for match in matches:
  if saved['team_id'] in (match['home_team_id'],match['away_team_id']):continue
  for side in ['home','away']:
   tid=match[side+'_team_id'];goals=sum(row['goal'] for row in record['rows'] if row['team_id']==tid)
   assert goals==match[side+'_goals']
   assert sum(row['assist'] for row in record['rows'] if row['team_id']==tid)<=goals
 conn.execute('BEGIN IMMEDIATE');ranks.record_fixture(conn,saved,1,matches);conn.commit();assert store.get_meta(conn,key,'')==raw
 # Old observed match record: not touched by CPU ranking hook.
 observed_key=ranks._scope(saved)+'match_987';observed={'source':'observed_native_match','own':[dict(player_id=110718,team_id=101,is_com='NO',goal=2,assist=1)],'opponent':[]}
 store.set_meta(conn,observed_key,json.dumps(observed));conn.commit();preserved=store.get_meta(conn,observed_key,'')
 output=ranks.populate(conn,saved,{})
 assert any(row['player_id']==110718 and row['is_com']=='NO' and row['value']==2 for row in output['goal_ranking'])
 assert store.get_meta(conn,observed_key,'')==preserved
 prepared=league.prepare(conn,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='realism-prepare',cpu_level='NORMAL',match_category='SEASON'),session_token='realism-tests')
 assert prepared['result']=='NOERR'
 assert inventory(conn)==before_inv
 conn.close();conn=sqlite3.connect(db);conn.row_factory=sqlite3.Row
 assert league.state(conn)['schedule_v2']==saved['schedule_v2'] and league.state(conn)[mod.META]==saved[mod.META]
 assert conn.execute('pragma quick_check').fetchone()[0]=='ok';conn.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
checks.append('actual select/resume/save reopen/opponent prepare work on copied DB; inventory and source unchanged')
checks.append('ranking receipts idempotent; CPU player goals sum to team scores; observed player events preserved')
# Population benchmark: ALL clubs CPU, to avoid attributing invented goals to the human team.
points=collections.defaultdict(list);goals=collections.defaultdict(list);top4=collections.Counter();star_ids=[110718,133543,110626,117047,110644,162114]
star_goals=collections.defaultdict(list);star10=collections.Counter();star20=collections.Counter();total_scores=[];home_wins=away_wins=draws=0
for index in range(a.seasons):
 s=season('population-'+str(index),team=999999);schedule=league.fixtures(s);table={t:[0,0,0] for t in registry['competitions']['122']['team_ids']};events=collections.Counter()
 for fx in schedule:
  matches=league.fixture_matches(s,fx)
  for match in matches:
   h,aw=match['home_team_id'],match['away_team_id'];hg,ag=match['home_goals'],match['away_goals'];total_scores.extend([hg,ag])
   home_wins+=hg>ag;away_wins+=ag>hg;draws+=hg==ag
   for tid,gf,ga in [(h,hg,ag),(aw,ag,hg)]:table[tid][0]+=3 if gf>ga else 1 if gf==ga else 0;table[tid][1]+=gf-ga;table[tid][2]+=gf
  simulated,missing=ranks._simulate_matches(None,s,fx['fixture'],matches);assert not missing
  for row in simulated:events[row['player_id']]+=row['goal']
  if fx['fixture']==10:
   top={pid for pid,_ in events.most_common(20)}
   for pid in star_ids:star10[pid]+=events[pid]>0;star20[pid]+=pid in top
 ordered=sorted(table,key=lambda tid:(-table[tid][0],-table[tid][1],-table[tid][2],tid));top4.update(ordered[:4])
 for tid in table:points[tid].append(table[tid][0]);goals[tid].append(table[tid][2])
 for pid in star_ids:star_goals[pid].append(events[pid])
benchmark={'seasons':a.seasons,'scope':'all-CPU Super League benchmark, NOT actual player club matches; illustrative game-based model, not calibrated real-world forecast',
 'goals_per_match':round(statistics.mean(total_scores)*2,3),'home_win_rate':round(home_wins/(a.seasons*306),3),'draw_rate':round(draws/(a.seasons*306),3),'away_win_rate':round(away_wins/(a.seasons*306),3),
 'max_goals_single_team':max(total_scores),'clubs':{str(t):{'mean_points':round(statistics.mean(points[t]),2),'points_sd':round(statistics.pstdev(points[t]),2),'top4_rate':round(top4[t]/a.seasons,3),'mean_goals':round(statistics.mean(goals[t]),2)} for t in sorted(points)},
 'stars':{str(pid):{'name':mod._profile(pid)['name'],'mean_season_goals':round(statistics.mean(star_goals[pid]),2),'scored_by_round10_rate':round(star10[pid]/a.seasons,3),'top20_after_round10_rate':round(star20[pid]/a.seasons,3)} for pid in star_ids}}
assert 2.<benchmark['goals_per_match']<3.8 and .15<benchmark['draw_rate']<.35
assert benchmark['home_win_rate']>benchmark['away_win_rate']
assert max(total_scores)>3 and min(total_scores)==0
assert min(statistics.mean(points[t]) for t in [101,108,114,173])>statistics.mean(points[181])+12
assert all(statistics.pstdev(points[t])>5 for t in points)
assert all(star10[pid]/a.seasons>.85 for pid in star_ids)
checks.append('multi-season benchmark: home edge, draws, upsets/variation, score tails and star goal involvement')
report={'status':'SERVER_LOGIC_VALIDATED_ANDROID_INTEGRATION_PENDING','device_tested':False,'checks':checks,'benchmark':benchmark}
Path(__file__).with_name('validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
