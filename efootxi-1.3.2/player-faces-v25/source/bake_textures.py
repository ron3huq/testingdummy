from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw,ImageFilter
P=Path('/workspace/ronaldo-work/v25');a=np.load(P/'export.npz');W=H=2048
c=np.array(Image.open('/workspace/ronaldo-work/new-hair-sources/2017/converted/hair_parts_bsm_alp.png').convert('RGBA'),dtype=float)
al=np.array(Image.open('/workspace/ronaldo-work/new-hair-sources/2017/converted/hair_alpha8.png').convert('RGBA'),dtype=float)
out=np.zeros((H,W,4),np.float32);covered=np.zeros((H,W),bool);overlap=0

def sample(im,uv):
 h,w=im.shape[:2];x=np.clip(uv[:,0]*(w-1),0,w-1);y=np.clip(uv[:,1]*(h-1),0,h-1);ix=x.astype(int);iy=y.astype(int);jx=np.minimum(ix+1,w-1);jy=np.minimum(iy+1,h-1);dx=(x-ix)[:,None];dy=(y-iy)[:,None]
 return (im[iy,ix]*(1-dx)+im[iy,jx]*dx)*(1-dy)+(im[jy,ix]*(1-dx)+im[jy,jx]*dx)*dy
for ids in a['hairtri']:
 uv=a['hairuv'][ids];xy=uv*np.array([W-1,H-1]);lo=np.maximum(0,np.floor(xy.min(0)).astype(int));hi=np.minimum([W-1,H-1],np.ceil(xy.max(0)).astype(int))
 if np.any(hi<lo):continue
 xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));p,q,r=xy;den=(q[1]-r[1])*(p[0]-r[0])+(r[0]-q[0])*(p[1]-r[1])
 if abs(den)<1e-9:continue
 u=((q[1]-r[1])*(xx-r[0])+(r[0]-q[0])*(yy-r[1]))/den;v=((r[1]-p[1])*(xx-r[0])+(p[0]-r[0])*(yy-r[1]))/den;w=1-u-v;valid=(u>=0)&(v>=0)&(w>=0)
 xs=xx[valid];ys=yy[valid];weights=np.c_[u[valid],v[valid],w[valid]]
 if len(xs)==0:continue
 overlap+=int(covered[ys,xs].sum());rgba=sample(c,weights@a['hair_source_uv1'][ids]);rgba[:,3]=sample(al,weights@a['hair_source_uv0'][ids])[:,3];out[ys,xs]=rgba;covered[ys,xs]=True
# RGB-only padding, no alpha growth between strands or UV islands.
filled=covered.copy()
for it in range(6):
 sums=np.zeros((H,W,3),np.float32);n=np.zeros((H,W),np.float32)
 for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
  mask=np.roll(filled,(dy,dx),(0,1));sums+=np.roll(out[:,:,:3],(dy,dx),(0,1))*mask[:,:,None];n+=mask
 add=(~filled)&(n>0);out[add,:3]=sums[add]/n[add,None];filled|=add
Image.fromarray(np.uint8(np.clip(np.rint(out),0,255))).save(P/'hair-mobile-atlas.png')
for name,lo,hi in [('face',239,2028),('cap',2028,2369)]:
 im=Image.new('L',(1024,1024));d=ImageDraw.Draw(im)
 for tri in a['skin_tri']:
  if min(tri)>=lo and max(tri)<hi:d.polygon([tuple(p*1023)for p in a['skin_uv'][tri]],fill=255)
 im.filter(ImageFilter.MaxFilter(3)).save(P/(name+'-coverage.png'))
assert covered.sum()>100000 and np.count_nonzero(out[:,:,3]>128)>10000
assert overlap/max(1,covered.sum())<.01,overlap
(P/'atlas-bake.json').write_text(json.dumps({'status':'DUAL_UV_TO_UNIQUE_RGBA_ATLAS_PASS','covered_pixels':int(covered.sum()),'overlap_pixels':overlap,'opaque_hair_pixels':int(np.count_nonzero(out[:,:,3]>128)),'colour_from_uv1_alpha_from_uv0':True,'rgb_padding_alpha_unchanged':True},indent=2));print('V25_ATLAS_BAKE_PASS',covered.sum(),overlap)
