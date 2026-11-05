"""Host-only MILP. Android receives validated schedules, never SciPy."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
IDS=[109,127,173,103,108,114,119,101,100,102,126,128,172,120,121,327,234,179,226,269,125,191,192,193,112,113,116,118,117,197,181,265,267,196,130,231]
ASSOC={'ENG':[100,101,102,103,106,107,173,179],'ESP':[109,108,172,265,267,196],'GER':[127,126,128,231,226],'FRA':[114,112,113,181],'ITA':[119,120,121,327,234,125,122,124],'POR':[191,192,193],'NED':[116,118,117],'TUR':[130,197],'BEL':[269]}
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
 sol=milp(rng.random(len(edges)),integrality=np.ones(len(edges)),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':60})
 if sol.x is None:raise RuntimeError('opponent draw: '+str(sol.message))
 picked=[e for e,x in zip(edges,sol.x)if x>.5];assert len(picked)==144
 rows=[];lo=[];hi=[]
 for k in range(144):add([k*8+r for r in range(8)],1,1)
 for t in range(36):
  for r in range(8):add([k*8+r for k,e in enumerate(picked)if t in e],1,1)
 A=lil_matrix((len(rows),1152))
 for i,r in enumerate(rows):A[i,r]=1
 sol=milp(rng.random(1152),integrality=np.ones(1152),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':60})
 if sol.x is None:raise RuntimeError('draw cannot be scheduled into eight complete rounds')
 rounds=[[]for _ in range(8)]
 for k,(h,a)in enumerate(picked):
  r=int(np.argmax(sol.x[k*8:k*8+8]));rounds[r].append([IDS[h],IDS[a]])
 return rounds
if __name__=='__main__':
 out=Path(__file__).parent/'runtime/ucl_lp_draws.json';draws=[]
 for seed in range(8):
  try:draws.append(dict(seed=seed,rounds=solve(seed)));print('draw',seed,flush=True)
  except RuntimeError as e:print(seed,str(e),flush=True)
 if not draws:raise RuntimeError('No feasible draw; not shipping')
 out.write_text(json.dumps(dict(schema=1,pots='balanced game-strength tiers; not UEFA coefficient pots',teams=TEAMS,draws=draws),indent=2))
