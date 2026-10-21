from pathlib import Path
import argparse,sys,json,collections,random
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;sys.path[:0]=[str(r),str(a.gateway/'work/tools')]
import myleague_worlds as w,myleague_realism as m
c=w.config();s=dict(competition_id=122,team_id=999999,season=1)
class Fixed:
 def __init__(self,v):self.v=v
 def random(self):return self.v
 def gauss(self,*args):return 0
boundaries=0
for h,aw,fav,win,draw in [(101,173,101,.7,.2),(173,101,101,.7,.2),(101,100,101,.9,.07),(100,101,101,.9,.07),(173,100,173,.95,.04),(101,103,101,.85,.1)]:
 for roll,outcome in [(win-1e-6,'W'),(win,'D'),(win+draw-1e-6,'D'),(win+draw,'L')]:
  hg,ag=m._hierarchy_score(s,h,aw,Fixed(roll));fg,og=(hg,ag) if fav==h else (ag,hg);actual='W' if fg>og else 'D' if fg==og else 'L';assert actual==outcome,(h,aw,roll,actual);boundaries+=1
rates={};scores=set()
for label,pairs,expected in [('top1_top2',[(101,109),(101,173),(101,127),(114,109),(114,173),(114,127),(108,173),(108,127)],.7),('top1_bottom',[(t,b) for t in [101,114,108] for b in [179,130,327,126,125,100]],.9),('top2_bottom',[(t,b) for t in [109,173,127] for b in [179,130,327,126,125,100]],.95),('clasico',[(108,109)],None)]:
 rng=random.Random(60322);counts=collections.Counter();n=20000
 for i in range(n):
  top,other=pairs[i%len(pairs)];h,aw=(top,other) if (i//len(pairs))%2 else (other,top);season=dict(s,season=i+1);hg,ag=m._hierarchy_score(season,h,aw,rng);fg,og=(hg,ag) if h==top else (ag,hg);counts['win' if fg>og else 'draw' if fg==og else 'loss']+=1;scores.add((hg,ag))
  assert max(hg,ag)<=4 and (hg,ag) not in [(7,4),(4,7),(4,2),(2,4)]
  if label in ('clasico','top1_top2'):assert max(hg,ag)<=3 and min(hg,ag)<=1
 distribution={k:counts[k]/n for k in ['win','draw','loss']};rates[label]=distribution
 if expected is not None:assert abs(distribution['win']-expected)<.014,(label,distribution)
 else:assert abs(distribution['win']-distribution['loss'])<.025 and distribution['draw']>.18
assert (0,0) in scores and (1,1) in scores and (4,0) in scores and (1,2) in scores
# Every remaining club pair respects the score envelope, including MU mid-table games.
for h in c['leagues']['122']['teams']:
 for aw in c['leagues']['122']['teams']:
  if h==aw:continue
  hg,ag=m.cpu_score(s,1,h,aw);assert max(hg,ag)<=4
report=dict(status='CLUB_POLICY_V6_PASS',device_tested=False,boundary_checks=boundaries,monte_carlo_matches=80000,distributions=rates,limits='CPU results only. No minute events exist, so late goals/pressing are not fabricated. Played results remain unchanged.')
(r/'club-policy-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
