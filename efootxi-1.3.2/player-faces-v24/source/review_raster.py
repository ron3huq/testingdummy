"""Static CPU triangle/texture review with skin backface culling; not UE/GPU test."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from mesh_tools import Mesh
from iostore import Toc
from bundle_tools import decode_first_texture
O=Path(__file__).resolve().parent.parent;t=Toc(str(O/'container/pc9298_mobile_and.utoc'));canvas=Image.new('RGB',(4*200,3*240),'#293342');draw=ImageDraw.Draw(canvas);rows=[]
for col,(code,haircode)in enumerate([('NX01','NXH1'),('NXJR','NXHJ'),('NXNC','NXHN'),('NX27','NXH7')]):
 name='SK_'+code+'ep00v0313_Face';m=Mesh(t.read(t.files['character/RealFace/'+name+'.uasset']),(O/'reader-logs'/(name+'.log')).read_text(),0);textures=[]
 for tex in ['T_'+code+'ep00v0313_Face_D','T_'+haircode+'_Hair_D']:
  p='character/RealFace/'+tex;textures.append(np.array(decode_first_texture(t.read(t.files[p+'.uasset']),t.read(t.files[p+'.ubulk']))))
 for ri,yaw in enumerate([-55,0,55]):
  angle=np.deg2rad(yaw);c,s=np.cos(angle),np.sin(angle);pos=m.positions.copy();pos[:,0]=c*m.positions[:,0]-s*(m.positions[:,1]-7);pos[:,1]=s*m.positions[:,0]+c*(m.positions[:,1]-7);screen=np.c_[pos[:,0]*6+100,(188-pos[:,2])*6+8];zbuffer=np.full((224,200),-np.inf);output=np.full((224,200,3),[41,51,66],dtype='u1');skinpixels=np.zeros((224,200),bool)
  for section,texture in zip(m.info,textures):
   start=section['baseidx']//3
   for tri in m.indices[start:start+section['tris']]:
    p=screen[tri];area=(p[1,0]-p[0,0])*(p[2,1]-p[0,1])-(p[1,1]-p[0,1])*(p[2,0]-p[0,0]);ishair=section is m.info[1]
    if abs(area)<1e-8 or(not ishair and area>0):continue
    lo=np.maximum(np.floor(p.min(0)).astype(int),[0,0]);hi=np.minimum(np.ceil(p.max(0)).astype(int),[199,223])
    if(hi<lo).any():continue
    yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];q=np.stack([xx+.5,yy+.5],-1);a=((p[1,0]-q[:,:,0])*(p[2,1]-q[:,:,1])-(p[1,1]-q[:,:,1])*(p[2,0]-q[:,:,0]))/area;b=((p[2,0]-q[:,:,0])*(p[0,1]-q[:,:,1])-(p[2,1]-q[:,:,1])*(p[0,0]-q[:,:,0]))/area;w=np.stack([a,b,1-a-b],-1);depth=w@pos[tri,1];old=zbuffer[lo[1]:hi[1]+1,lo[0]:hi[0]+1];good=(w.min(-1)>=-1e-6)&(depth>old)
    if not good.any():continue
    uv=np.einsum('...i,ij->...j',w,m.uv[tri,:2].astype(float));tx=np.clip((uv[:,:,0]*texture.shape[1]).astype(int),0,texture.shape[1]-1);ty=np.clip((uv[:,:,1]*texture.shape[0]).astype(int),0,texture.shape[0]-1);rgba=texture[ty,tx]
    if ishair:good &=rgba[:,:,3]>51
    old[good]=depth[good];output[lo[1]:hi[1]+1,lo[0]:hi[0]+1][good]=rgba[:,:,:3][good];skinpixels[lo[1]:hi[1]+1,lo[0]:hi[0]+1][good]=not ishair
  count=int(skinpixels.sum());assert count>2000
  if yaw==0:assert float(np.median(zbuffer[85:120,90:110]))>3.,'Front face points inward or misses central facial surface'
  rows.append({'profile':code,'yaw':yaw,'visible_skin_pixels_with_backface_culling':count});canvas.paste(Image.fromarray(output),(col*200,ri*240+16));draw.text((col*200+5,ri*240+2),code+' '+str(yaw),fill='white')
canvas.save(O/'CPU-static-review.png');(O/'cpu-review.json').write_text(json.dumps({'status':'V24_FOUR_HEADS_THREE_VIEWS_CPU_BACKFACE_CULLING_PASS','views':rows,'scope':'static diffuse triangle review, not Unreal materials, animation or Android GPU','phone_tested':False},indent=2));print('V24_FOUR_HEADS_THREE_VIEWS_CPU_BACKFACE_CULLING_PASS')
