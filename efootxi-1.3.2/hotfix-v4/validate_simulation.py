from pathlib import Path
import argparse,sys,json,collections,random
p=argparse.ArgumentParser();p.add_argument('--gateway',required=True,type=Path);p.add_argument('--seasons',default=40,type=int);a=p.parse_args();r=Path(__file__).parent;sys.path[:0]=[str(r),str(a.gateway/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,my_league as league,season_rankings as ranks
model.ATTRS=a.gateway/'outputs/reference/external-attrs';model.install();cfg=worlds.config()
def state(cid,index):return dict(competition_id=cid,team_id=999999,season=index+1,fixture=1,played={},active=None,completed=False,cpu_level='NORMAL',realism_v1=dict(seed='benchmark-'+str(index),version=model.VERSION))
reports={}
for cid in [122,128,125]:
 totals=collections.defaultdict(collections.Counter);goals=collections.Counter();assists=collections.Counter();hist=collections.Counter()
 for index in range(a.seasons):
  s=state(cid,index)
  for fx in league.fixtures(s):
   matches=league.fixture_matches(s,fx)
   events,missing=ranks._simulate_matches(None,s,fx['fixture'],matches);assert not missing,missing
   counts=collections.Counter()
   for e in events:
    tid,pid=e['team_id'],e['player_id'];assert pid in ranks._rosters()[str(tid)]
    assert model._position(pid)!=0
    counts[tid]+=e['goal'];goals[pid]+=e['goal'];assists[pid]+=e['assist']
   for m in matches:
    h,aw=m['home_team_id'],m['away_team_id'];hg,ag=m['home_goals'],m['away_goals'];hist[f'{hg}-{ag}']+=1
    for t,gf,ga in [(h,hg,ag),(aw,ag,hg)]:
     assert counts[t]==gf
     totals[t]['wins']+=gf>ga;totals[t]['draws']+=gf==ga;totals[t]['losses']+=gf<ga;totals[t]['goals']+=gf
 team_report={str(t):dict(win_rate=round(v['wins']/(v['wins']+v['draws']+v['losses']),4),goals_per_season=round(v['goals']/a.seasons,2)) for t,v in totals.items()}
 if cid==122:assert team_report['100']['win_rate']<.12 and all(team_report[str(t)]['win_rate']>.60 for t in [101,108,114])
 if cid==128:assert min(team_report[str(t)]['win_rate'] for t in [7,50,8,5])>max(team_report[str(t)]['win_rate'] for t in [17,38,1174])
 if cid==125:assert all(team_report[str(t)]['win_rate']>.50 for t in [18961,17873,17733,17734,157,4155,158])
 # Missing requested players are deliberately NOT assigned events in this league.
 if cid==125:assert all(goals[p]==0 for p in [40002,16786160,16837770])
 for score in ['0-0','1-0','2-1','4-0','5-0','3-3']:assert hist[score]>0,(cid,score)
 reports[str(cid)]=dict(teams=team_report,top_scorers=goals.most_common(12),top_assisters=assists.most_common(12),score_histogram=dict(hist),requested_star_goals_per_season={str(p):round(goals[p]/a.seasons,2) for p in [7511,110718,133543,117047,47287,4522,16781738,43063,40002,162114,110644]},requested_assists_per_season={str(p):round(assists[p]/a.seasons,2) for p in [162114,129369]})
 print('finished league',cid,flush=True)
# A single matchup must also vary; it cannot just repeat a canned score.
for cid,h,aw in [(122,108,109),(122,101,100),(122,173,127),(125,18961,22428),(128,7,1174)]:
 results=collections.Counter(model.cpu_score(state(cid,i),1,h,aw) for i in range(10000))
 assert len(results)>25
 assert results[(0,0)] and results[(1,0)] and results[(4,0)] and results[(5,0)]
 assert any(hg<ag for hg,ag in results)
result=dict(status='CPU_BENCHMARK_PASS',device_tested=False,seasons_each_league=a.seasons,checks=['all recorded player goals sum to CPU team scores; assisters/scorers belong to actual roster; no GK scorer','hierarchy and MU weakness hold statistically','multiple score regimes include tight wins, routs, goalless and open draws','10,000 seeds per representative pair vary; lower teams can cause upsets','absent Lewandowski/Benzema/Mitrovic have no fabricated goals'],leagues=reports)
(r/'simulation-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('BENCHMARK PASS')
