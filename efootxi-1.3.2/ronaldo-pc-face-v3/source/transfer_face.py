"""Adapt supplied PC face surface/color onto native Android facial topology."""
from pathlib import Path
import sys,re,struct,json
import numpy as np
from PIL import Image
import trimesh
r=Path(__file__).parent;p=r.parent;sys.path.insert(0,str(p/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
f=FmdlFile();f.readFile(str(p/'new-face-4522/models/face_high.fmdl'))
pc=[];puv=[];tri=[]
for mesh in [f.meshes[0],f.meshes[2]]:
 start=len(pc);index={id(v):start+i for i,v in enumerate(mesh.vertices)}
 pc.extend([[v.position.x*100,v.position.z*100,v.position.y*100] for v in mesh.vertices]);puv.extend([[v.uv[0].u,v.uv[0].v] for v in mesh.vertices]);tri.extend([[index[id(v)] for v in face.vertices] for face in mesh.faces])
pc=np.array(pc);puv=np.array(puv);tri=np.array(tri);surface=trimesh.Trimesh(pc,tri,process=False);prox=trimesh.proximity.ProximityQuery(surface)
b=(p/'pc3700-new/extracted/SK_4522ep00v0313_Face.uasset').read_bytes();h=struct.unpack_from('<16I',b);delta=h[13]+h[14]+struct.unpack_from('<Q',b,h[11]+8)[0]-struct.unpack_from('<Q',b,h[11]+72)[0];ranges={k:int(v)+delta for k,v in re.findall(r'RANGE (\w+) (\d+)',(p/'android-hair-v1/layout-4522ep00v0313.log').read_text())}
pos=np.array([struct.unpack_from('<fff',b,ranges['POSITION_BEGIN']+16+i*12) for i in range(743)]);idx=np.frombuffer(b[ranges['INDICES_BEGIN']+9:ranges['INDICES_BEGIN']+9+3666*2],'<u2').reshape(-1,3)
at=ranges['TANGENT_UV_BEGIN'];nv=1344;uat=at+26+nv*8+8;uv=np.array([struct.unpack_from('<ee',b,uat+i*8) for i in range(743)])
nearest,dist,which=prox.on_surface(pos)
# Constrain transfer to facial surface; preserve back of skull / neck seam / eyes rig alignment.
front=np.clip((pos[:,1]-1)/5,0,1);zmask=np.clip((pos[:,2]-156)/3,0,1)*np.clip((179-pos[:,2])/2,0,1)
strength=front*zmask*np.clip((2.0-dist)/.8,0,1)
eye_centers=np.array([[2.5595858,13.423942,171.34473],[-3.500015,13.572004,171.35321]])
eye_distance=np.linalg.norm(pos[:,None,:]-eye_centers[None,:,:],axis=2).min(axis=1)
strength*=np.clip((eye_distance-1.3)/1.5,0,1)
new=pos+(nearest-pos)*strength[:,None]
# Cap large geometric deviations to 8mm; no skeleton/bind changes.
v=new-pos;length=np.linalg.norm(v,axis=1);v*=np.minimum(1,.8/np.maximum(length,1e-12))[:,None];new=pos+v
# Texture: sample the PC face surface UV per point on native UV-space triangles.
N=1024;out=np.zeros((N,N,3),np.uint8);covered=np.zeros((N,N),bool);image=np.array(Image.open(p/'converted/face_bsm_alp.png').convert('RGB'),float)
def sample(coords):
 hh,ww=image.shape[:2];q=np.clip(coords,0,1)*[ww-1,hh-1];x=np.floor(q[:,0]).astype(int);y=np.floor(q[:,1]).astype(int);fx=(q[:,0]-x)[:,None];fy=(q[:,1]-y)[:,None];xx=np.minimum(x+1,ww-1);yy=np.minimum(y+1,hh-1)
 return (image[y,x]*(1-fx)+image[y,xx]*fx)*(1-fy)+(image[yy,x]*(1-fx)+image[yy,xx]*fx)*fy
# Direct layout fallback protects unrepresented scalp/back pixels; RGB uses supplied PC skin.
out[:]=np.array(Image.open(p/'converted/face_bsm_alp.png').convert('RGB').resize((N,N),Image.Resampling.LANCZOS))
close,dd,ti=prox.on_surface(new)
bary=trimesh.triangles.points_to_barycentric(pc[tri[ti]],close)
projected_uv=np.einsum('ij,ijk->ik',bary,puv[tri[ti]])
u_delta=projected_uv-uv
# Keep the existing PES-compatible chart at seams/back/neck; small front corrections only.
uv_weight=strength*np.clip((.075-np.linalg.norm(u_delta,axis=1))/.025,0,1)
mapped_uv=uv+u_delta*uv_weight[:,None]
for n,ids in enumerate(idx):
 q=uv[ids]*N-.5;a,c,d=q;den=(c[1]-d[1])*(a[0]-d[0])+(d[0]-c[0])*(a[1]-d[1])
 if abs(den)<1e-9:continue
 lo=np.maximum(0,np.floor(q.min(axis=0)).astype(int));hi=np.minimum(N-1,np.ceil(q.max(axis=0)).astype(int));xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));w0=((c[1]-d[1])*(xx-d[0])+(d[0]-c[0])*(yy-d[1]))/den;w1=((d[1]-a[1])*(xx-d[0])+(a[0]-d[0])*(yy-d[1]))/den;w2=1-w0-w1;ok=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
 if not ok.any():continue
 bc=np.stack([w0[ok],w1[ok],w2[ok]],axis=1);points=bc@new[ids];uv_fallback=bc@uv[ids]
 # Bake a continuous per-triangle UV transfer; avoid nearest-surface chart jumps.
 values=sample(bc@mapped_uv[ids])
 out[yy[ok],xx[ok]]=np.clip(values,0,255).astype(np.uint8);covered[yy[ok],xx[ok]]=True
 if n%200==0:print('bake triangles',n,flush=True)
Image.fromarray(out,'RGB').save(r/'pc-face-baked-1024.png');np.save(r/'face_positions_cm.npy',new);np.save(r/'face_original_positions_cm.npy',pos)
# Native UV topology, vertex IDs, skin weights and bind matrices are retained by builder.
report={'source':'4522.cpk face_high.fmdl meshes 0 and 2, face_bsm_alp.ftex','native_vertices':743,'native_triangles':1222,'pc_skin_vertices':len(pc),'pc_skin_triangles':len(tri),'changed_vertices':int((np.linalg.norm(new-pos,axis=1)>1e-4).sum()),'max_surface_transfer_cm':float(np.linalg.norm(new-pos,axis=1).max()),'baked_size':[N,N],'texture_covered_pixels':int(covered.sum()),'scope':'PC facial surface/color adapted to native topology; not a direct PC mesh transplant','mouth_eyes_animation_verified_on_phone':False}
(r/'face-transfer-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
