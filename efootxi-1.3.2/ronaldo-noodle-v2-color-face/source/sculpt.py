"""Conservative local cheek / under-jaw adjustment, in Unreal centimeters."""
import math
import numpy as np

def smooth(a,b,v):
 t=max(0.,min(1.,(v-a)/(b-a)));return t*t*(3-2*t)

def point(v):
 x,y,z=v
 # Cheek soft tissue only: central mouth, nose, eyes, ears and neck seam stay put.
 cheek=math.exp(-((z-167.1)/2.0)**2)*smooth(2.,4.8,abs(x))*(1-smooth(6.7,8.2,abs(x)))*smooth(5.,9.,y)*(1-smooth(169.3,170.5,z))
 jaw=math.exp(-((z-162.0)/1.5)**2)*smooth(2.,4.5,abs(x))*(1-smooth(6.3,7.8,abs(x)))*smooth(4.,8.,y)
 under=math.exp(-((z-160.3)/1.4)**2)*(1-smooth(2.,5.6,abs(x)))*smooth(3.,7.,y)*(1-smooth(11.5,13.,y))
 return np.array([x-math.copysign(.24*cheek+.10*jaw,x),y-.13*cheek-.23*under,z+.24*under])

def normals(v,n):
 eps=.001;v=np.array(v);j=np.column_stack([(point(v+np.eye(3)[i]*eps)-point(v-np.eye(3)[i]*eps))/(2*eps) for i in range(3)])
 n=np.linalg.solve(j.T,np.array(n));return n/max(1e-12,np.linalg.norm(n)),j
