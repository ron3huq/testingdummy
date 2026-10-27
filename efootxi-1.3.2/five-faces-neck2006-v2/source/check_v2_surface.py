from pathlib import Path
import json,numpy as np,collections
R=Path(__file__).parent;out={'phone_tested':False,'heads':{}}
for k in ['orc','naruto']:
 d=json.loads((R/k/'native_geometry.json').read_text());p=np.array([v['p']for v in d['vertices']]);_,ids=np.unique(np.round(p,8),axis=0,return_inverse=True);counts=collections.Counter()
 for tri in d['triangles']:
  t=[int(ids[i])for i in tri]
  for a,b in zip(t,t[1:]+t[:1]):
   if a!=b:counts[tuple(sorted((a,b)))]+=1
 boundary=sum(v==1 for v in counts.values());nonmanifold=sum(v>2 for v in counts.values());out['heads'][k]={'vertices':len(p),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'position_min':p.min(axis=0).tolist(),'position_max':p.max(axis=0).tolist()};assert boundary==0,(k,boundary,nonmanifold)
 if nonmanifold:
  spans=[float(np.linalg.norm(pts[0]-pts[1])) for edge,count in counts.items() if count>2 for pts in [np.unique(np.round(p,8),axis=0)[list(edge)]]];assert max(spans)<.000001,(k,spans);out['heads'][k]['collapsed_edge_max_length_m']=max(spans)
(R/'surface-v2-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
