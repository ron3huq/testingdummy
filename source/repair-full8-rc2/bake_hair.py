from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
sys.path.insert(0,'/workspace/ronaldo-work/pes-fmdl-blender/pes-fmdl')
from FmdlFile import FmdlFile
R=Path('/workspace/work/full8/face-v8');OUT=Path('/workspace/work/full8-rc2/face');OUT.mkdir(exist_ok=True)
f=FmdlFile();f.readFile(str(R/'models/hair_high.fmdl'))
alpha=np.array(Image.open(R/'textures/hair_parts_bsm_alp.png').convert('RGBA'));color=np.array(Image.open(R/'textures/hair_parts_bsm.png').convert('RGB'));h,w=alpha.shape[:2];result=alpha.copy();covered=np.zeros((h,w),bool);tri_count=0
for mesh in f.meshes:
 if not any(t.filename=='hair_parts_bsm_alp.dds'for role,t in mesh.materialInstance.textures):continue
 assert mesh.vertexFields.uvCount>=2
 for face in mesh.faces:
  uv0=np.array([[v.uv[0].u,v.uv[0].v]for v in face.vertices]);uv1=np.array([[v.uv[1].u,v.uv[1].v]for v in face.vertices]);p=uv0*np.array([w,h]);lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int),[w-1,h-1])
  if (hi<lo).any():continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5);points=np.c_[xx.ravel(),yy.ravel()];a,b,c=p;v0=b-a;v1=c-a;d=points-a;den=v0[0]*v1[1]-v0[1]*v1[0]
  if abs(den)<1e-9:continue
  u=(d[:,0]*v1[1]-d[:,1]*v1[0])/den;v=(v0[0]*d[:,1]-v0[1]*d[:,0])/den;inside=(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)
  if not inside.any():continue
  dst=points[inside].astype(int);bary=np.c_[1-u[inside]-v[inside],u[inside],v[inside]];src=bary@uv1
  sx=np.clip(src[:,0]*color.shape[1]-.5,0,color.shape[1]-1);sy=np.clip(src[:,1]*color.shape[0]-.5,0,color.shape[0]-1);x0=sx.astype(int);y0=sy.astype(int);x1=np.minimum(x0+1,color.shape[1]-1);y1=np.minimum(y0+1,color.shape[0]-1);fx=(sx-x0)[:,None];fy=(sy-y0)[:,None]
  rgb=(color[y0,x0]*(1-fx)+color[y0,x1]*fx)*(1-fy)+(color[y1,x0]*(1-fx)+color[y1,x1]*fx)*fy
  result[dst[:,1],dst[:,0],:3]=np.rint(rgb).astype('u1');covered[dst[:,1],dst[:,0]]=True;tri_count+=1
assert np.array_equal(result[:,:,3],alpha[:,:,3]);assert covered.sum()>10000
Image.fromarray(result).save(OUT/'hair-native-uv0.png')
(OUT/'hair-bake.json').write_text(json.dumps(dict(source_color='hair_parts_bsm UV1',source_alpha='hair_parts_bsm_alp UV0',triangles_baked=tri_count,covered_texels=int(covered.sum()),alpha_exactly_preserved=True,phone_verified=False),indent=2));print('Hair UV1 colour baked to native UV0; source alpha preserved.')
