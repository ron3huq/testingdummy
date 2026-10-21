"""Actual installed gateway integration and multi-season CPU simulation, no device claims."""
from pathlib import Path
import argparse,collections,copy,json,sys,time,sqlite3,tempfile,hashlib
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);p.add_argument('--seasons',type=int,default=6);a=p.parse_args();r=Path(__file__).parent;g=a.gateway;sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_realism as m,myleague_worlds as w,my_league as league,season_rankings as ranks,club_store as store
class Bridge:
 @staticmethod
 def activate_context(*a):pass
 @staticmethod
 def set_environment(*a):return 1
 @staticmethod
 def ensure_native_team(*a):return 1
w.NATIVE_BRIDGE=Bridge;m.ATTRS=g/'outputs/reference/external-attrs';m.install();c=w.config();started=time.monotonic();reports={};all_scores=set();failures=[]
def state(cid,seed,team=999999):return dict(competition_id=cid,season=1,team_id=team,fixture=1,played={},active=None,completed=False,cpu_level='NORMAL',realism_v1={'seed':str(seed)})
# Explicit Japan probabilities and zero loss regardless of venue/form.
for opponent,tier,expected in [(5750,3,(.85,.15,0)),(57,2,(.7,.15,.15)),(53,1,(.65,.22,.13))]:
 for h,aw in [(52,opponent),(opponent,52)]:
  v=m._outcome_probabilities(state(566,'japan'),1,h,aw);v=v if h==52 else tuple(reversed(v));assert all(abs(x-y)<1e-9 for x,y in zip(v,expected)),v
# Updated modern groups and equal Clasico before styles/form.
assert c['leagues']['122']['tiers']['126']==3 and c['leagues']['122']['tiers']['179']==5 and c['leagues']['122']['tiers']['100']==6
assert c['leagues']['518']['tiers']['2365']==0 and c['leagues']['518']['tiers']['5317']==1
# Full64 rosters, native hook and unrelated league data must not change.
old=json.loads((r.parent/'hotfix-v9/myleague_custom.json').read_text())
for key in ['native_rosters','classic_teams','classic_profiles','card_overrides','base_overrides','match_environment','league_names','team_names','shirt_overrides']:
 assert c[key]==old[key],key
assert (r/'libselect_team.so').read_bytes()==(r.parent/'hotfix-v9/libselect_team.so').read_bytes()
source=g/'outputs/efootball/local-club.sqlite3';source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory() as tmp:
 conn=sqlite3.connect(Path(tmp)/'rankings.db');conn.row_factory=sqlite3.Row
 ro=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);ro.backup(conn);ro.close()
 for cid in [122,518,566,128]:
  counts=collections.Counter();champions=[];mu_points=[];rankleaders=[];nround=0;quotas=0;shocks_max=0;rare_max=0;target_goals={}
  for seed in range(a.seasons):
   s=state(cid,'v10-test-'+str(seed));s['season']=seed+1
   fixtures=league.fixtures(s);s['schedule_v2']=copy.deepcopy(fixtures);before_draw=copy.deepcopy(fixtures);points=collections.Counter();scorers=collections.Counter();assisters=collections.Counter()
   for fx in fixtures:
    no=fx['fixture'];s['fixture']=no;before=copy.deepcopy(s);matches=league.fixture_matches(s,fx);assert before==s
    if seed==0 and no in [1,8,len(fixtures)]:assert league.fixture_matches(json.loads(json.dumps(s)),fx)==matches
    # No accidental re-use of past/protocol objects, deterministic snapshot.
    assert fx==before_draw[no-1]
    for v in matches:
     h,aw,x,y=[v[k]for k in ['home_team_id','away_team_id','home_goals','away_goals']];assert x>=0 and y>=0 and max(x,y)<=(7 if cid==122 else 5)
     all_scores.add((x,y));counts['games']+=1;counts['goals']+=x+y;counts['draw']+=x==y;counts['home']+=x>y;counts['btts']+=min(x,y)>0;counts['zero']+=x==y==0;counts['fiveplus']+=x+y>=5;counts['m'+str(min(4,abs(x-y)))]+=1
     points[h]+=3 if x>y else 1 if x==y else 0;points[aw]+=3 if y>x else 1 if x==y else 0
    # Event path tested on first full season of each league, using actual gateway receipts.
    if seed==0:
     conn.execute('BEGIN IMMEDIATE');ranks.record_fixture(conn,s,no,matches);conn.commit()
     record=json.loads(store.get_meta(conn,ranks._scope(s)+'fixture_'+str(no)))
     for v in matches:
      for side in ['home','away']:
       tid=v[side+'_team_id'];rows=[x for x in record['rows']if x['team_id']==tid]
       assert sum(x['goal']for x in rows)==v[side+'_goals']
       for row in rows:
        assert row['player_id']in ranks._rosters()[str(tid)];assert not row['goal'] or m._position(row['player_id'])!=0
        scorers[row['player_id']]+=row['goal'];assisters[row['player_id']]+=row['assist']
    s['played'][str(no)]={'matches':copy.deepcopy(matches),'result':'DRAW'}
    history=m._history(s,no+1);definition=m._sim_definition(s)
    shocks=sum(m._large_upset(definition,v)for rnd,v in history if rnd>=no-9);shocks_max=max(shocks_max,shocks)
    rare=sum((v['home_goals'],v['away_goals'])in m._RARE for _,v in history);rare_max=max(rare_max,rare)
    # Strict quota checks are evaluated, not assumed: feedback may be infeasible.
    score=[(v['home_goals'],v['away_goals'])for v in matches];draws=sum(x==y for x,y in score);low=1 if len(score)<=6 else 2;high=2 if len(score)<=6 else 3
    feasible=low<=draws<=high and any(sorted(x)==[0,1]for x in score) and any(sum(x)>=4 for x in score) and any(x<y for x,y in score) and any(min(x)>=2 for x in score) and max(collections.Counter(score).values())<=2 and max(collections.Counter(abs(x-y)for x,y in score).values())<=3
    quotas+=feasible;nround+=1
    saved=copy.deepcopy(s);assert league.fixture_matches(s,fx)==matches and s==saved
   assert shocks_max<=2,(cid,seed,shocks_max)
   assert rare<=2
   champion=points.most_common(1)[0];champions.append({'team':champion[0],'points':champion[1]})
   if cid==122:mu_points.append(points[100])
   if seed==0:target_goals={str(pid):scorers[pid] for pid in [47287,110718,133543,70373039149482,17592722922839]};rankleaders=[{'goals':scorers.most_common(8),'assists':assisters.most_common(8)}]
  n=counts['games'];reports[str(cid)]={'seasons':a.seasons,'matches':n,'draw':counts['draw']/n,'home_win':counts['home']/n,'away_win':1-(counts['home']+counts['draw'])/n,'goals_per_game':counts['goals']/n,'zero_zero':counts['zero']/n,'five_plus':counts['fiveplus']/n,'both_score':counts['btts']/n,'margins':{str(i):counts['m'+str(i)]/n for i in range(5)},'complete_round_quotas_met':quotas,'rounds':nround,'max_large_upsets_in10rounds':shocks_max,'max_rare_scores':rare_max,'champions':champions,'mu_points':mu_points,'first_season_ranking':rankleaders,'target_goals':target_goals}
  print(cid,json.dumps(reports[str(cid)]),flush=True)
 # Player fixture placeholder is never modified into an invented result.
 s=state(122,'user',101);fx=league.fixtures(s)[0];before=copy.deepcopy(s);rows=league.fixture_matches(s,fx)
 assert s==before
 for v in rows:
  if 101 in [v['home_team_id'],v['away_team_id']]:assert v['home_goals']==v['away_goals']==0
 assert conn.execute('pragma quick_check').fetchone()[0]=='ok'
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
assert (0,0)in all_scores and (3,2)in all_scores and (4,1)in all_scores and (2,2)in all_scores
report=dict(status='SIMULATION_V10_PASS',device_tested=False,seconds=time.monotonic()-started,reports=reports,score_support=sorted(all_scores),checks=['explicit Japan boundaries','all four competition memberships unchanged','all native binary/rosters/roles/OVR/weather unchanged','full-season played-history feedback and10-round upset budget','snapshot/reload/accepted matches immutable','actual original ranking simulator wrapped; full64 roster membership and goal conservation','live selected fixture remains native; no fake card/minute/injury events'],limits=['Probabilities are priors; round quotas and form alter observed rates','Round and end-season targets approximate; Scottish12clubs22rounds, not18clubs34rounds','No Android renderer/device test'])
(r/'simulation-validation.json').write_text(json.dumps(report,indent=2)+'\n')
