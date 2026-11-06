"""Host-only MILP. Android receives validated schedules, never SciPy."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
IDS=[109,127,173,103,108,114,119,101,100,102,213,182,172,120,121,327,234,179,1195,269,125,191,192,193,112,113,4219,118,117,197,181,265,267,196,130,5220]
ASSOC={'ENG':[100,101,102,103,106,107,173,179],'ESP':[109,108,172,265,267,196],'GER':[127],'FRA':[114,112,113,181,213,182],'ITA':[119,120,121,327,234,125,4219,122,124],'POR':[191,192,193],'NED':[118,117],'TUR':[130,197],'BEL':[269,1195,5220]}
TEAMS=[dict(team_id=t,association=next(a for a,ts in ASSOC.items()if t in ts),pot=i//9+1,strength=90-i*.35,coefficient=None)for i,t in enumerate(IDS)]
# Build four balanced native-strength tiers. Coefficients are unavailable in APK73.
pr=[];pl=[];pu=[]
for i in range(36):pr.append([i*4+p for p in range(4)]);pl.append(1);pu.append(1)
for p in range(4):
 pr.append([i*4+p for i in range(36)]);pl.append(9);pu.append(9)
 for country in ASSOC:
  pr.append([i*4+p for i,t in enumerate(TEAMS)if t['association']==country]);pl.append(0);pu.append(2)
A=lil_matrix((len(pr),144))
for i,row in enumerate(pr):A[i,row]=1
res=milp(np.array([-i*p for i in range(36)for p in range(4)],float),integrality=np.ones(144),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),pl,pu));assert res.x is not None
for i,t in enumerate(TEAMS):t['pot']=int(np.argmax(res.x[i*4:i*4+4]))+1
TEAMS=sorted(TEAMS,key=lambda t:(t['pot'],-t['strength']));IDS=[t['team_id']for t in TEAMS]
POOL={r['team_id']:r for r in json.loads(Path(__file__).with_name('native_pool.json').read_text())['teams']}
for team in TEAMS:
 team.update({k:POOL[team['team_id']][k]for k in ['name','short','roster_count']})
def solve(seed):
 rng=np.random.default_rng(seed);edges=[(i,j)for i in range(36)for j in range(36)if i!=j and TEAMS[i]['association']!=TEAMS[j]['association']];rows=[];lo=[];hi=[]
 def add(ix,l,h):rows.append(ix);lo.append(l);hi.append(h)
 for t in range(36):
  for pot in range(1,5):
   add([k for k,(i,j)in enumerate(edges)if i==t and TEAMS[j]['pot']==pot],1,1)
   add([k for k,(i,j)in enumerate(edges)if j==t and TEAMS[i]['pot']==pot],1,1)
  for a in ASSOC:add([k for k,(i,j)in enumerate(edges)if (i==t and TEAMS[j]['association']==a)or(j==t and TEAMS[i]['association']==a)],0,2)
 for i in range(36):
  for j in range(i+1,36):
   ix=[k for k,e in enumerate(edges)if set(e)=={i,j}]
   if ix:add(ix,0,1)
 A=lil_matrix((len(rows),len(edges)))
 for i,r in enumerate(rows):A[i,r]=1
 sol=milp(rng.random(len(edges)),integrality=np.ones(len(edges)),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':30,'mip_rel_gap':1.0})
 if sol.x is None:raise RuntimeError('opponent draw: '+str(sol.message))
 picked=[e for e,x in zip(edges,sol.x)if x>.5];assert len(picked)==144
 # Factor the8-regular opponent graph into5 perfect matchings and a final
 # three-colouring. This is much smaller than a single1152-variable colour MILP.
 print('opponent graph ready',seed,flush=True)
 for attempt in range(24):
  remaining=list(range(len(picked)));rounds=[];failed=False
  for _ in range(5):
   A=lil_matrix((36,len(remaining)))
   for j,k in enumerate(remaining):
    h,a=picked[k];A[h,j]=1;A[a,j]=1
   match=milp(rng.random(len(remaining)),integrality=np.ones(len(remaining)),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),np.ones(36),np.ones(36)),options={'time_limit':3,'mip_rel_gap':1.0})
   if match.x is None:failed=True;break
   chosen={remaining[j]for j,v in enumerate(match.x)if v>.5};assert len(chosen)==18
   rounds.append([[IDS[picked[k][0]],IDS[picked[k][1]]]for k in sorted(chosen)]);remaining=[k for k in remaining if k not in chosen]
  if failed:continue
  n=len(remaining);assert n==54
  A=lil_matrix((n+36*3,n*3))
  for j,k in enumerate(remaining):
   h,a=picked[k]
   for colour in range(3):A[j,j*3+colour]=1;A[n+h*3+colour,j*3+colour]=1;A[n+a*3+colour,j*3+colour]=1
  final=milp(np.zeros(n*3),integrality=np.ones(n*3),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),np.ones(n+108),np.ones(n+108)),options={'time_limit':3})
  if final.x is None:continue
  for colour in range(3):rounds.append([[IDS[picked[k][0]],IDS[picked[k][1]]]for j,k in enumerate(remaining)if final.x[j*3+colour]>.5])
  sys.path.insert(0,str(Path(__file__).parent/'runtime'))
  from ucl_lp_mode import validate_draw
  validate_draw(TEAMS,rounds)
  return rounds
 raise RuntimeError('opponent graph could not be factored into eight valid matchdays')
if __name__=='__main__':
 out=Path(__file__).parent/'runtime/ucl_lp_draws.json';draws=[]
 count=int(sys.argv[1])if len(sys.argv)>1 else 8
 if not 1<=count<=8:raise ValueError('draw count must be1..8')
 for seed in range(count):
  try:draws.append(dict(seed=seed,rounds=solve(seed)));print('draw',seed,flush=True)
  except RuntimeError as e:print(seed,str(e),flush=True)
 if not draws:raise RuntimeError('No feasible draw; not shipping')
 out.write_text(json.dumps(dict(schema=1,pots='balanced game-strength tiers; not UEFA coefficient pots',teams=TEAMS,draws=draws),indent=2))
