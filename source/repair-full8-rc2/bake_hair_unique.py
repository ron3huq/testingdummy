"""Bake the two authored UV channels into unique native per-triangle UV cells.
Duplicate corner vertices only; preserve every source triangle's positions.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from PIL import Image
sys.path.insert(0,'/workspace/ronaldo-work/pes-fmdl-blender/pes-fmdl')
from FmdlFile import FmdlFile
R=Path('/workspace/work/full8/face-v8');OUT=Path('/workspace/work/full8-rc2/face')
f=FmdlFile();f.readFile(str(R/'models/hair_high.fmdl'))
alpha=np.array(Image.open(R/'textures/hair_parts_bsm_alp.png').convert('RGBA'));color=np.array(Image.open(R/'textures/hair_parts_bsm.png').convert('RGBA'))
size=2048;cell=20;columns=(size//2)//cell;canvas=np.array(Image.open(OUT/'hair-surface-bake.png').resize((size,size),Image.Resampling.LANCZOS));positions=[];uvs=[];frames=[];triangles=[];strand_charts=0
def sample(image,uv):
 h,w=image.shape[:2];x=np.clip(uv[:,0]*w-.5,0,w-1);y=np.clip(uv[:,1]*h-.5,0,h-1);x0=x.astype(int);y0=y.astype(int);x1=np.minimum(x0+1,w-1);y1=np.minimum(y0+1,h-1);fx=(x-x0)[:,None];fy=(y-y0)[:,None]
 return (image[y0,x0]*(1-fx)+image[y0,x1]*fx)*(1-fy)+(image[y1,x0]*(1-fx)+image[y1,x1]*fx)*fy
for mesh in f.meshes:
 if not any(t.filename=='hair_parts_bsm_alp.dds'for role,t in mesh.materialInstance.textures):continue
 assert mesh.vertexFields.uvCount>=2
 if max(v.uv[0].u for v in mesh.vertices)<.5:
  # Retain the high-detail, uniquely mapped cap surface on the left half.
  base=len(positions);indices={id(v):base+i for i,v in enumerate(mesh.vertices)}
  for vertex in mesh.vertices:
   positions.append([vertex.position.x*100,vertex.position.z*100,vertex.position.y*100]);uvs.append([vertex.uv[0].u,vertex.uv[0].v,3.0517578125e-5,3.0517578125e-5]);frames.append([vertex.tangent.x,vertex.tangent.z,vertex.tangent.y,vertex.tangent.w,vertex.normal.x,vertex.normal.z,vertex.normal.y,-vertex.tangent.w])
  for face in mesh.faces:triangles.append([indices[id(v)]for v in reversed(face.vertices)])
  continue
 for face in mesh.faces:
  index=strand_charts;strand_charts+=1;x=size//2+(index%columns)*cell;y=(index//columns)*cell;assert y+cell<=size
  vertices=list(reversed(face.vertices));a=np.array([[v.uv[0].u,v.uv[0].v]for v in vertices]);c=np.array([[v.uv[1].u,v.uv[1].v]for v in vertices])
  xx,yy=np.meshgrid(np.arange(cell)+.5,np.arange(cell)+.5);u=(xx.ravel()-3)/14;v=(yy.ravel()-3)/14
  # Extend edge texels into padding, preventing seams between adjacent triangles.
  u=np.maximum(u,0);v=np.maximum(v,0);scale=np.maximum(1,u+v);u/=scale;v/=scale;bary=np.c_[1-u-v,u,v]
  rgba=sample(color,bary@c);rgba[:,3]=sample(alpha,bary@a)[:,3]
  canvas[y:y+cell,x:x+cell]=np.rint(rgba.reshape(cell,cell,4)).astype('u1')
  texcoords=np.array([[x+3,y+3],[x+17,y+3],[x+3,y+17]])/size
  base=len(positions)
  for vertex,uv in zip(vertices,texcoords):
   positions.append([vertex.position.x*100,vertex.position.z*100,vertex.position.y*100]);uvs.append([*uv,3.0517578125e-5,3.0517578125e-5]);frames.append([vertex.tangent.x,vertex.tangent.z,vertex.tangent.y,vertex.tangent.w,vertex.normal.x,vertex.normal.z,vertex.normal.y,-vertex.tangent.w])
  triangles.append([base,base+1,base+2])
Image.fromarray(canvas).save(OUT/'hair-native-uv0.png')
np.savez_compressed(OUT/'hair-native.npz',positions=np.array(positions,dtype='<f4'),uv=np.array(uvs,dtype='<f2'),triangles=np.array(triangles,dtype='<u2'),tangents=np.clip(np.rint(np.array(frames)*127),-127,127).astype('i1').view('u1'))
(OUT/'hair-bake.json').write_text(json.dumps(dict(source_color='hair_parts_bsm UV1',source_alpha='hair_parts_bsm_alp UV0',native_uv='high-resolution cap retained; unique padded strand cells',source_triangles=len(triangles),native_corner_vertices=len(positions),positions_and_normals_from_source=True,source_shape_not_scaled=True,phone_verified=False),indent=2));print('Baked',len(triangles),'triangles with independent colour/alpha UVs.')
