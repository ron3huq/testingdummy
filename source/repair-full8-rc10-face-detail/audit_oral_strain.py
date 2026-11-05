import numpy as np
import sys
# Diagnostic only: no universal safe strain threshold is asserted.
from scipy.spatial.transform import Rotation
z=np.load(sys.argv[1]);p=z['p'];f=z['f'];w=z['weights'];rest=z['rest'];par=z['parents'];lab=z['labels'];qrest=p[f];e=np.stack([qrest[:,1]-qrest[:,0],qrest[:,2]-qrest[:,0],qrest[:,2]-qrest[:,1]],1);lens=np.linalg.norm(e,axis=2);isoral=np.isin(lab[f[:,0]],list(range(2,8))+list(range(9,12))+list(range(13,32)));mid=qrest.mean(1)
for angle in [-5,-12,-20,-30]:
 move=np.eye(4);move[:3,:3]=Rotation.from_euler('x',angle,degrees=True).as_matrix();C=np.eye(4);C[:3,3]=rest[8,:3,3];move=C@move@np.linalg.inv(C);posed=[]
 for i in range(len(par)):
  parent=np.eye(4) if par[i]<0 else posed[par[i]]@np.linalg.inv(rest[par[i]])
  posed.append(parent@(move if i==8 else np.eye(4))@rest[i])
 T=np.array(posed)@np.linalg.inv(rest);q=np.einsum('vij,vj->vi',np.einsum('vb,bij->vij',w,T),np.c_[p,np.ones(len(p))])[:,:3];qf=q[f];el=np.linalg.norm(np.stack([qf[:,1]-qf[:,0],qf[:,2]-qf[:,0],qf[:,2]-qf[:,1]],1),axis=2);ratio=np.max(el/np.maximum(lens,.0001),axis=1);bad=np.flatnonzero(isoral&(ratio>3)&(lens.min(1)>.015));print(angle,len(bad),'max',ratio[bad].max() if len(bad) else 0,[(int(lab[f[j,0]]),round(float(ratio[j]),2),f[j].tolist())for j in sorted(bad,key=lambda j:-ratio[j])[:10]])
