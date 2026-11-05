"""Bounded atlas edits; preserve pores, skin, iris identity, and unrelated blocks.
Teeth and tongue remain visible in shadow. Only the throat/cavity is near black.
"""
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from bundle_tools import decode_first_texture
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent/'repair-full8-rc9-ucl'))
from face_texture_base import patch_blocks
PALETTES=np.array([[174,137,117],[162,120,93],[162,116,85],[138,102,77],[101,74,60],[85,62,52]],float)
_EXTRA={}
def world_map(mesh,lab,size):
 w,h=size;xyz=np.zeros((h,w,3),np.float32);valid=np.zeros((h,w),bool);uv=mesh.uv[:,:2].astype(float)*[w,h]
 tri=mesh.indices[:mesh.info[0]['tris']]
 for f in tri:
  if not(lab[f[0]]<28 or lab[f[0]]==34):continue
  q=uv[f];p=mesh.positions[f];lo=np.maximum(np.floor(q.min(0)).astype(int),0);hi=np.minimum(np.ceil(q.max(0)).astype(int),[w-1,h-1]);a,b,c=q;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-8 or (hi<lo).any():continue
  yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5;u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;bc=np.stack([u,v,1-u-v],-1);inside=(bc>=-1e-5).all(-1);region=xyz[lo[1]:hi[1]+1,lo[0]:hi[0]+1];region[inside]=(bc@p)[inside];valid[lo[1]:hi[1]+1,lo[0]:hi[0]+1]|=inside
 return xyz,valid

def crease_field(xyz,valid):
 x,y,z=np.moveaxis(xyz,-1,0);a=np.abs(x);field=np.zeros_like(x)
 def segment(ax,az,bx,bz,width):
  dx=bx-ax;dz=bz-az;t=np.clip(((a-ax)*dx+(z-az)*dz)/(dx*dx+dz*dz),0,1);dist=((a-(ax+t*dx))**2+(z-(az+t*dz))**2)**.5;return np.exp(-.5*(dist/width)**2)
 # Short, separated canthal lines, not a deep scar drawn across the temple.
 for end in [(5.85,171.15),(6.05,170.65),(5.8,169.9)]:field=np.maximum(field,segment(4.45,170.45,*end,.035)*.75)
 # Two soft lower-lid folds follow the socket, strongest towards the outer eye.
 for shift,weight in [(0,1),(-.24,.45)]:
  zline=169.63+shift+.10*((a-3.25)/1.15)**2;line=np.exp(-.5*((z-zline)/.035)**2)*np.exp(-((a-3.3)/1.4)**6)*weight;field=np.maximum(field,line)
 return field*valid*(y>11)*(a>1.65)*(a<6.5)*(z>168.5)*(z<172.0)

def masks(mesh,lab,size):
 tri=mesh.indices[:mesh.info[0]['tris']];uv=mesh.uv[:,:2].astype(float);out={}
 for name in ['skin','neck','cavity','teeth','tongue','eyes']:
  mask=Image.new('L',size);draw=ImageDraw.Draw(mask)
  for f in tri:
   k=int(lab[f[0]]);yes=(k<28 or k==34)if name=='skin'else k==34 if name=='neck'else k==31 if name=='cavity'else k in(28,30)if name=='teeth'else k==29 if name=='tongue'else k in(32,33)
   if yes:draw.polygon([(float(uv[i,0]*size[0]),float(uv[i,1]*size[1]))for i in f],fill=255)
  out[name]=mask.filter(ImageFilter.MaxFilter(5))
 xyz,valid=world_map(mesh,lab,size);out['xyz']=xyz;out['valid']=valid;out['crease']=crease_field(xyz,valid);_EXTRA['current']=out
 return out['skin'],out['neck'],out['cavity']

def build_texture(raw,bulk,channel,palette,skin,neck,oral):
 im=decode_first_texture(raw,bulk);a=np.array(im).astype(float);e=_EXTRA['current'];s=np.array(skin)>0;n=np.array(neck)>0;c=np.array(oral)>0;t=np.array(e['teeth'])>0;g=np.array(e['tongue'])>0;crease=e['crease'];x,y,z=np.moveaxis(e['xyz'],-1,0);valid=e['valid'];lip=valid&(abs(x)<3.3)&(y>15.8)&(z>162.8)&(z<164.9)&(a[:,:,2]>a[:,:,1]*.9)&(a[:,:,:3].mean(2)>60)
 if channel=='D':
  gain=PALETTES[palette-1]/np.array([158.,115.,92.]);a[s,:3]*=gain;a[n,:3]*=np.array([158/163,115/117,1.]);a[:,:,:3]*=(1-.085*crease[:,:,None]);a[lip,:3]*=np.array([1.01,1.045,.95]);a[t,:3]*=.55;a[g,:3]*=.30;a[c,:3]=2;mask=Image.fromarray(np.uint8(s|t|g|c)*255)
 elif channel=='SRO':
  a[c,0]=0;a[c,1]=255;a[c,2]=0;a[t,0]=45;a[t,1]=125;a[t,2]=255;a[g,0]=30;a[g,1]=175;a[g,2]=255;a[:,:,1]=np.clip(a[:,:,1]+crease*8,0,255);mask=Image.fromarray(np.uint8((crease>.001)|t|g|c)*255)
 else:
  assert channel=='N';height=-.003*crease;dy,dx=np.gradient(height);normal=a[:,:,:3]/127.5-1;normal[:,:,0]-=dx/.035;normal[:,:,1]+=dy/.035;normal/=np.maximum(np.linalg.norm(normal,axis=2)[:,:,None],1e-8);changed=crease>.0001;changed|=np.abs(dx)+np.abs(dy)>1e-7;a[changed,:3]=(normal[changed]+1)*127.5;mask=Image.fromarray(np.uint8(changed)*255)
 new=Image.fromarray(np.rint(np.clip(a,0,255)).astype('u1'),'RGBA');return patch_blocks(raw,bulk,new,mask)
