from pathlib import Path
import sys,argparse,random,json,collections
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;sys.path[:0]=[str(r),str(a.gateway/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds
cfg=worlds.config();tiers=cfg['leagues']['122']['tiers'];tops=[int(t) for t,v in tiers.items() if v<=1];g3=[int(t) for t,v in tiers.items() if v==2];g4=[int(t) for t,v in tiers.items() if v>=3]
assert len(tops)==len(g3)==len(g4)==6
class Fixed:
 def __init__(self,v):self.value=v
 def random(self):return self.value
 def gauss(self,*args):return 0
s=dict(competition_id=122,team_id=999999,season=1)
checks=0
for group,cases in [(g3,[(.849999,'W'),(.85,'D'),(.949999,'D'),(.95,'L')]),(g4,[(.949999,'W'),(.95,'D'),(.989999,'D'),(.99,'L')])]:
 for top in tops:
  for other in group:
   for home,away in [(top,other),(other,top)]:
    for roll,expected in cases:
     hg,ag=model._hierarchy_score(s,home,away,Fixed(roll));tg,og=(hg,ag) if home==top else (ag,hg)
     actual='W' if tg>og else 'D' if tg==og else 'L';assert actual==expected,(home,away,roll,actual,expected);checks+=1
reports={}
for key,group,expected in [('group3',g3,.85),('group4',g4,.95)]:
 rng=random.Random(852195);counts=collections.Counter();scores=set()
 for i in range(20000):
  top=rng.choice(tops);other=rng.choice(group);home,away=(top,other) if i%2==0 else (other,top)
  season=dict(s,season=i+1)
  hg,ag=model._hierarchy_score(season,home,away,rng);tg,og=(hg,ag) if top==home else (ag,hg)
  counts['win' if tg>og else 'draw' if tg==og else 'loss']+=1;scores.add((tg,og))
 rates={k:counts[k]/20000 for k in ['win','draw','loss']};assert abs(rates['win']-expected)<.01,(key,rates)
 assert (1,0) in scores and (4,0) in scores and (5,0) in scores and any(t<o for t,o in scores)
 reports[key]=dict(matches=20000,measured=rates,configured=cfg['club_outcome_policy']['vs_'+key])
report=dict(status='CLUB_POLICY_PASS',device_tested=False,boundary_checks=checks,pairs_both_venues=144,monte_carlo=reports,dembele=dict(card_id='88039313485858',removed_flag=108,removed_learned_id=5,added_flag=135),limits='CPU simulated fixtures only; no guarantee for a short run or user-played matches.')
(r/'club-policy-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
