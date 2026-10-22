"""Bake both supplied FOX UV streams into a unique Android diffuse/alpha atlas."""
from pathlib import Path
import sys,json,collections,math
import numpy as np
from PIL import Image
from rectpack import newPacker,MaxRectsBssf,SORT_AREA
from scipy.ndimage import distance_transform_edt
r=Path(__file__).parent;p=r.parent;sys.path.insert(0,str(p/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
f=FmdlFile();f.readFile(str(p/'source-extracted/hair_high.fmdl'));m=f.meshes[0];ix={id(v):i for i,v in enumerate(m.vertices)};faces=np.array([[ix[id(v)] for v in t.vertices] for t in m.faces]);uv=np.array([[[q.u,q.v] for q in v.uv] for v in m.vertices]);parent=list(range(len(m.vertices)))
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for a,b,c in faces:parent[root(int(b))]=root(int(a));parent[root(int(c))]=root(int(a))
g=collections.defaultdict(list)
for i in range(len(parent)):g[root(i)].append(i)
N=2048;pad=5;bounds={k:(uv[v,0].min(axis=0),uv[v,0].max(axis=0)) for k,v in g.items()}
for scale in range(500,350,-5):
 pk=newPacker(rotation=False,pack_algo=MaxRectsBssf,sort_algo=SORT_AREA)
 for k,(lo,hi) in bounds.items():pk.add_rect(max(2,math.ceil((hi[0]-lo[0])*scale))+2*pad,max(2,math.ceil((hi[1]-lo[1])*scale))+2*pad,rid=k)
 pk.add_bin(N,N);pk.pack();rects=pk.rect_list()
 if len(rects)==len(g):break
else:raise ValueError('atlas packing failed')
newuv=np.zeros((len(parent),2),dtype=np.float64);rectangles={}
for _,x,y,w,h,k in rects:
 lo,hi=bounds[k];newuv[g[k]]=(uv[g[k],0]-lo)*scale+np.array([x+pad+.5,y+pad+.5]);rectangles[k]=(x,y,w,h)
# Quantize to the exact half UV precision shipped to Android before raster baking.
newuv=(newuv/N).astype(np.float16).astype(np.float64)
color=np.array(Image.open(p/'converted/hair_parts_bsm_alp.png').convert('RGB'),dtype=float)
alpha=np.array(Image.open(p/'converted/hair_alpha8.png').convert('RGBA'),dtype=float)[:,:,3]
out=np.zeros((N,N,4),dtype=np.float32);out[:,:,:3]=[23,17,13];coverage=np.zeros((N,N),dtype=np.uint16);conflicts=0;triangles=0
# The asset UVs use image top-left convention; no Blender vertical flip here.
def sample(tex,coords,wrap=False):
 h,w=tex.shape[:2];c=coords%1.0 if wrap else np.clip(coords,0,1);q=c*np.array([w,h])-.5
 x0=np.floor(q[:,0]).astype(int);y0=np.floor(q[:,1]).astype(int);fx=q[:,0]-x0;fy=q[:,1]-y0
 if wrap:x1=(x0+1)%w;y1=(y0+1)%h;x0%=w;y0%=h
 else:x1=np.clip(x0+1,0,w-1);y1=np.clip(y0+1,0,h-1);x0=np.clip(x0,0,w-1);y0=np.clip(y0,0,h-1)
 if tex.ndim==3:fx=fx[:,None];fy=fy[:,None]
 return (tex[y0,x0]*(1-fx)+tex[y0,x1]*fx)*(1-fy)+(tex[y1,x0]*(1-fx)+tex[y1,x1]*fx)*fy
for ids in faces:
 pos=newuv[ids]*N-.5;a,b,c=pos;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
 if abs(den)<1e-8:continue
 lo=np.maximum(0,np.floor(pos.min(axis=0)).astype(int));hi=np.minimum(N-1,np.ceil(pos.max(axis=0)).astype(int));xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1))
 w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1;mask=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
 if not mask.any():continue
 xs=xx[mask];ys=yy[mask];bc=np.stack([w0[mask],w1[mask],w2[mask]],axis=1)
 uv0=bc@uv[ids,0];uv1=bc@uv[ids,1];rgb=sample(color,uv1);aa=sample(alpha,uv0,True)
 # Retain authored color; a modest exposure lift makes gold strands readable on mobile.
 rgb=np.clip(rgb*1.12,0,255)
 occupied=coverage[ys,xs]>0;conflicts+=int(np.sum(occupied & (np.max(np.abs(out[ys,xs,:3]-rgb),axis=1)>32)))
 replace=(~occupied)|(aa>out[ys,xs,3]);out[ys[replace],xs[replace],:3]=rgb[replace];out[ys,xs,3]=np.maximum(out[ys,xs,3],aa);coverage[ys,xs]+=1;triangles+=1
# Dilate edge RGB/alpha only within each card's private gutter to prevent mip fringes.
for k,(x,y,w,h) in rectangles.items():
 reg=out[y:y+h,x:x+w];cov=coverage[y:y+h,x:x+w]>0
 if cov.any():
  dist,ind=distance_transform_edt(~cov,return_indices=True);gutter=(~cov)&(dist<=pad);reg[gutter]=reg[ind[0][gutter],ind[1][gutter]]
result=Image.fromarray(np.round(out).astype(np.uint8),'RGBA');result.save(r/'noodle-color-atlas-2048.png');np.save(r/'atlas_uv.npy',newuv)
mask=out[:,:,3]>128;gold=(out[:,:,0]>out[:,:,2]*1.35)&(out[:,:,0]>65)&mask
report={'atlas_size':[N,N],'source_primary_size':[512,512],'source_color_size':[1024,1024],'connected_cards':len(g),'atlas_texels_per_uv_unit':scale,'triangles_rasterized':triangles,'uv_overlap_conflict_pixels':conflicts,'visible_pixels':int(mask.sum()),'visible_gold_pixels':int(gold.sum()),'two_uv_sources_baked':True,'new_vertices':len(newuv),'exposure_multiplier':1.12,'not_a_new_hair_shader':True};assert report['visible_gold_pixels']>1000
(r/'bake-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
