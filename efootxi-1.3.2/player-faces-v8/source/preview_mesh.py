"""CPU texture/geometry diagnostic; NOT an Android renderer or phone screenshot."""
from pathlib import Path
import sys,numpy as np
from PIL import Image,ImageDraw
from gltf_read import Gltf
r=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent
panels=[]
for profile in ['ND01','ND06','ND13','ND27','NDJR','NDXS','NDDB']:
 g=Gltf(r/'v8-export/Game/Assets/character/RealFace'/('SK_'+profile+'ep00v0313_Face.gltf'));bones=[g.d['nodes'][i]['name'] for i in g.d['skins'][0]['joints']]
 inv=g.get(g.d['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1).astype(float);bind=np.linalg.inv(inv)
 for opened in [False,True]:
  canvas=np.full((680,520,3),28,dtype='u1');depth=np.full((680,520),-np.inf);pose=bind.copy()
  if opened:
   pose[bones.index('skf_jaw'),:3,3]+=[0,-.012,-.001]
   for side,angle in [('l',.10),('r',-.10)]:
    c=np.cos(angle);s=np.sin(angle);rot=np.eye(4);rot[:3,:3]=[[c,0,s],[0,1,0],[-s,0,c]];k=bones.index('skf_eye_'+side);pose[k]=bind[k]@rot
  for part,p in enumerate(g.d['meshes'][0]['primitives']):
   xyz=g.get(p['attributes']['POSITION']);normal=g.get(p['attributes']['NORMAL']);uv=g.get(p['attributes']['TEXCOORD_0']);tri=g.get(p['indices']).reshape(-1,3)
   if opened:
    js=g.get(p['attributes']['JOINTS_0']);weights=g.get(p['attributes']['WEIGHTS_0'])/255;hom=np.c_[xyz,np.ones(len(xyz))];new=np.zeros_like(hom);mat=pose@inv
    for slot in range(4):new+=np.einsum('nij,nj->ni',mat[js[:,slot]],hom)*weights[:,slot,None]
    xyz=new[:,:3]
   texpath=out/(('T_'+profile+'ep00v0313_Face_D-decoded.png') if part==0 else ('T_'+('ND0001' if profile=='ND01' else 'ND00'+profile[2:])+'_Hair_D-decoded.png'))
   if not texpath.exists():
    texpath=r/'v8-full-export/Game/Assets/character/RealFace/T_ND0001_Hair_D.png'
   tex=np.asarray(Image.open(texpath).convert('RGBA'));h,w=tex.shape[:2]
   screen=np.c_[260+xyz[:,0]*2100,590-(xyz[:,1]-1.57)*2100,xyz[:,2]]
   for face in tri:
    v=screen[face];lo=np.maximum(np.floor(v[:,:2].min(0)).astype(int),[0,35]);hi=np.minimum(np.ceil(v[:,:2].max(0)).astype(int),[519,679])
    if (lo>hi).any():continue
    x,y=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5);den=(v[1,1]-v[2,1])*(v[0,0]-v[2,0])+(v[2,0]-v[1,0])*(v[0,1]-v[2,1])
    if abs(den)<1e-8:continue
    a=((v[1,1]-v[2,1])*(x-v[2,0])+(v[2,0]-v[1,0])*(y-v[2,1]))/den;b=((v[2,1]-v[0,1])*(x-v[2,0])+(v[0,0]-v[2,0])*(y-v[2,1]))/den;c=1-a-b
    z=a*v[0,2]+b*v[1,2]+c*v[2,2];d=depth[lo[1]:hi[1]+1,lo[0]:hi[0]+1];inside=(a>=0)&(b>=0)&(c>=0)&(z>d)
    texuv=a[...,None]*uv[face[0]]+b[...,None]*uv[face[1]]+c[...,None]*uv[face[2]];tx=np.clip((texuv[...,0]*w).astype(int),0,w-1);ty=np.clip((texuv[...,1]*h).astype(int),0,h-1);sample=tex[ty,tx];inside &=sample[...,3]>127
    norm=a[...,None]*normal[face[0]]+b[...,None]*normal[face[1]]+c[...,None]*normal[face[2]];shade=.55+.45*np.maximum(0,np.sum(norm*np.array([.2,.35,.915]),axis=-1));color=np.clip(sample[...,:3]*shade[...,None],0,255).astype('u1');d[inside]=z[inside];sub=canvas[lo[1]:hi[1]+1,lo[0]:hi[0]+1];sub[inside]=color[inside]
  im=Image.fromarray(canvas);draw=ImageDraw.Draw(im);draw.text((10,8),profile+(' - synthetic jaw/eye pose' if opened else ' - bind pose'),fill='white');draw.text((10,660),'CPU DIAGNOSTIC - NOT ANDROID / NOT PHONE VERIFIED',fill='white');panels.append(im)
result=Image.new('RGB',(1040,4760));
for i,im in enumerate(panels):result.paste(im,((i%2)*520,(i//2)*680))
result.save(out/'geometry-texture-diagnostic.png');print(out/'geometry-texture-diagnostic.png')
