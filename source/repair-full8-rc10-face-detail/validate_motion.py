"""LBS and visibility checks on Android container readback; not a phone test."""
import bpy,numpy as np,json,math
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
r=Path('/workspace/apk73-face-detail/preview');z=np.load(r/'asset.npz');p=z['p'];f=z['f'];w=z['weights'];rest=z['rest'];parent=z['parents'];lab=z['labels'];area=np.linalg.norm(np.cross(p[f[:,1]]-p[f[:,0]],p[f[:,2]]-p[f[:,0]]),axis=1);f=f[area>1e-8];skin=np.isin(lab,list(range(28))+[34]);skinF=f[skin[f].all(1)];eyesF=f[np.isin(lab[f],(32,33)).all(1)];ids=np.flatnonzero(skin);_,inv=np.unique(np.round(p[ids],4),axis=0,return_inverse=True);first=np.full(inv.max()+1,len(ids));np.minimum.at(first,inv,np.arange(len(ids)));refs=ids[first[inv]]
def pose(changes):
 posed=[]
 for i in range(len(parent)):
  inherited=np.eye(4)if parent[i]<0 else posed[parent[i]]@np.linalg.inv(rest[parent[i]]);move=np.eye(4)
  if i in changes:
   axis,angle=changes[i];C=Matrix.Translation(Vector(rest[i,:3,3]));move=np.array(C@Matrix.Rotation(math.radians(angle),4,axis)@C.inverted())
  posed.append(inherited@move@rest[i])
 trans=np.array(posed)@np.linalg.inv(rest);return np.einsum('vij,vj->vi',np.einsum('vb,bij->vij',w,trans),np.c_[p,np.ones(len(p))])[:,:3]
def visible(pp):
 body=BVHTree.FromPolygons(pp.tolist(),skinF.tolist(),all_triangles=True);eye=BVHTree.FromPolygons(pp.tolist(),eyesF.tolist(),all_triangles=True);out={}
 for label in [32,33]:
  q=pp[lab==label];lo=q.min(0);hi=q.max(0);n=0
  for xx in np.linspace(lo[0],hi[0],45):
   for zz in np.linspace(lo[2],hi[2],35):
    o=Vector((xx,100,zz));d=Vector((0,-1,0));bh=body.ray_cast(o,d,200)[0];eh=eye.ray_cast(o,d,200)[0]
    if eh is not None and(bh is None or eh.y>bh.y+.0005):n+=1
  out['eye'+str(label)]=n
 for label in [28,29,30]:
  n=0
  for point in pp[lab==label]:
   bh=body.ray_cast(Vector((point[0],100,point[2])),Vector((0,-1,0)),200)[0]
   if bh is None or point[1]>bh.y-.002:n+=1
  out['oral'+str(label)]=n
 return out
states={'neutral':{},'blink':{10:('X',-35),12:('X',-35),11:('X',15),13:('X',15)},'jaw5':{8:('X',-5)},'jaw12':{8:('X',-12)},'jaw20':{8:('X',-20)},'jaw30':{8:('X',-30)},'head-turn':{5:('Z',5),6:('Z',10),7:('Z',15)},'combined-blink-jaw-turn':{5:('Z',4),6:('Z',6),7:('Z',10),8:('X',-20),10:('X',-35),12:('X',-35),11:('X',15),13:('X',15)}};reports={}
for name,changes in states.items():
 q=pose(changes);gap=np.linalg.norm(q[ids]-q[refs],axis=1).max();row=dict(finite=bool(np.isfinite(q).all()),duplicate_skin_seam_max_cm=float(gap));assert row['finite']and gap<1e-4
 if name!='head-turn':row.update(visible(q))
 reports[name]=row
assert reports['neutral']['oral28']==reports['neutral']['oral29']==reports['neutral']['oral30']==0
assert reports['blink']['eye32']==reports['blink']['eye33']==0
assert reports['jaw20']['oral28']>0 and reports['jaw20']['oral29']>0 and reports['jaw20']['oral30']>0
assert reports['combined-blink-jaw-turn']['eye32']==reports['combined-blink-jaw-turn']['eye33']==0
(r/'motion-validation.json').write_text(json.dumps(dict(states=reports,phone_verified=False),indent=2));print(json.dumps(reports,indent=2))
