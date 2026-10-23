"""Repair SNORM8 tangent frames without touching positions, UVs or skin weights."""
import numpy as np

def repair_frame(pos,tan,uv,tri,derive=False):
 a=tan.view('i1').astype(float)/127;n=a[:,4:7].copy()
 # Source 2008 scalp has collapsed pole vertices with zero normals.
 # Reuse the nearest defined source normal; no position/weight edits.
 missing=np.linalg.norm(n,axis=1)<1e-8
 if missing.any():
  from scipy.spatial import cKDTree
  valid=np.where(~missing)[0];assert len(valid)
  _,nearest=cKDTree(pos[valid]).query(pos[missing]);n[missing]=n[valid[nearest]]
 n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12);t=a[:,:3].copy();out=tan.copy()
 if derive:
  dp1=pos[tri[:,1]]-pos[tri[:,0]];dp2=pos[tri[:,2]]-pos[tri[:,0]];du1=uv[tri[:,1],:2].astype(float)-uv[tri[:,0],:2].astype(float);du2=uv[tri[:,2],:2].astype(float)-uv[tri[:,0],:2].astype(float);det=du1[:,0]*du2[:,1]-du1[:,1]*du2[:,0];valid=np.abs(det)>1e-10;weight=np.linalg.norm(np.cross(dp1,dp2),axis=1);tangent=np.zeros_like(dp1);bitangent=np.zeros_like(dp1)
  tangent[valid]=(dp1[valid]*du2[valid,1,None]-dp2[valid]*du1[valid,1,None])/det[valid,None]*weight[valid,None];bitangent[valid]=(dp2[valid]*du1[valid,0,None]-dp1[valid]*du2[valid,0,None])/det[valid,None]*weight[valid,None]
  t=np.zeros_like(n);b=np.zeros_like(n)
  for j in range(3):np.add.at(t,tri[:,j],tangent);np.add.at(b,tri[:,j],bitangent)
  sign=np.sign(np.sum(np.cross(n,t)*b,axis=1));sign[sign==0]=1;out[:,7]=np.rint(sign*127).astype('i1').view('u1')
 t-=n*np.sum(t*n,axis=1,keepdims=True);length=np.linalg.norm(t,axis=1);bad=length<1e-8
 for i in np.where(bad)[0]:axis=np.eye(3)[np.argmin(abs(n[i]))];t[i]=np.cross(n[i],axis)
 t/=np.maximum(np.linalg.norm(t,axis=1,keepdims=True),1e-12)
 out[:,:3]=np.rint(np.clip(t,-1,1)*127).astype('i1').view('u1');out[:,4:7]=np.rint(np.clip(n,-1,1)*127).astype('i1').view('u1');return out
