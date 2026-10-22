"""Regression: pose the exact v7 cracked seams and the corresponding v9 vertices.
Synthetic neck/head poses with native bind matrices; not an Android render test.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from mesh_tools import Mesh
from gltf_read import Gltf
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;rows=[]
for profile in ['ND06','ND13']:
 name='SK_'+profile+'ep00v0313_Face';base=out/'references/v7';old=Mesh((base/(name+'.uasset')).read_bytes(),(out/'references/v7'/(profile+'ep00v0313.log')).read_text(),0);new=Mesh((out/'asset'/(name+'.uasset')).read_bytes(),(R/('v9-'+profile+'ep00v0313.log')).read_text(),0)
 g=Gltf(R/'v9-export/Game/Assets/character/RealFace'/(name+'.gltf'));inv=g.get(g.d['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inv)
 groups={};oldrows=old.global_weights(0)
 n=next(p['skin_vertices'] for p in json.loads((out/'build-report.json').read_text())['meshes'] if p['profile']==profile)
 for i,p in enumerate(old.positions[:n]):groups.setdefault(tuple(np.round(p,3)),[]).append(i)
 cracked=[]
 for group in groups.values():
  if len(group)<2:continue
  palette={k for i in group for k,w in oldrows[i]}
  if palette<={4,5,6,7} and len({tuple(sorted(oldrows[i])) for i in group})>1:cracked.append(group)
 assert len(cracked)>20
 def deform(mesh,sign):
  pose=bind.copy()
  for bone,angle in [(4,.02),(5,.15),(6,-.12),(7,.3),(8,.2)]:
   c=np.cos(angle*sign);s=np.sin(angle*sign);rot=np.eye(4);rot[:3,:3]=[[c,0,s],[0,1,0],[-s,0,c]];pose[bone]=bind[bone]@rot
  mat=pose@inv;positions=np.c_[mesh.positions[:n][:,[0,2,1]]/100,np.ones(n)];result=np.zeros((n,4));weights=mesh.global_weights(0)
  for i in range(n):
   for bone,w in weights[i]:result[i]+=mat[bone]@positions[i]*w/255
  return result[:,:3]
 cases=[]
 for sign in [-1,1]:
  a=deform(old,sign);b=deform(new,sign);before=max(np.linalg.norm(a[group]-a[group[0]],axis=1).max() for group in cracked);after=max(np.linalg.norm(b[group]-b[group[0]],axis=1).max() for group in cracked)
  assert before>1e-5 and after<1e-7,(profile,before,after);cases.append({'turn_sign':sign,'v7_max_gap_mm':float(before*1000),'v9_max_gap_mm':float(after*1000)})
 rows.append({'profile':profile,'v7_weight_mismatch_groups':len(cracked),'cases':cases})
result={'status':'V7_NECK_SEAM_POSE_REGRESSION_AND_V9_CLOSED_SEAMS_PASS','checks':rows,'pose_is_synthetic':True,'phone_tested':False,'container_sha256':hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()}
(out/'seam-validation.json').write_text(json.dumps(result,indent=2));print(result['status'])
