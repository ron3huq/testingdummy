from pathlib import Path
import json,numpy as np
from scipy.spatial.transform import Rotation
P=Path('/workspace/ronaldo-work/73-ui5');old=Path('/workspace/ronaldo-work/73-ui4/test_mesh.py').read_text();exec(old[old.index('def load('):old.index("root=P/")]);exec(old[old.index('def pose('):old.index('proof=[]')]);rows=[]
for name in ['SK_4015a07','SK_4015d07','SK_4015a02','SK_4123d07']:
 j,a=load(P/'new-export/Game/Assets/character/Body',name);p=j['meshes'][0]['primitives'][0];v=a(p['attributes']['POSITION']);tri=a(p['indices']).reshape(-1,3);c=a(p['attributes']['COLOR_0']);cloth=np.all(c==0,axis=1);arm=cloth&(abs(v[:,0])>.2)&(v[:,1]>1.0);selection=tri[np.any(arm[tri],axis=1)];edges=np.concatenate([selection[:,[0,1]],selection[:,[1,2]],selection[:,[2,0]]]);samples=[]
 for deg in [0,30,60,90,120]:
  q=pose(j,a,np.deg2rad(deg));assert np.isfinite(q).all();lens=np.linalg.norm(q[edges[:,0]]-q[edges[:,1]],axis=1);longest=float(lens.max()*100);assert longest<35,(name,deg,longest);samples.append({'elbow_degrees':deg,'largest_arm_triangle_edge_cm':round(longest,3)})
 rows.append({'mesh':name,'samples':samples})
(P/'pose-validation.json').write_text(json.dumps({'passed':True,'native_export_skinning':True,'weight_values_normalized_before_skinning':True,'samples':rows,'android_gpu_tested':False,'absence_of_all_self_intersections_not_proven':True},indent=2));print('POSE_PASS',rows)
