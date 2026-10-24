import bpy,sys,math,json,os
import numpy as np
from pathlib import Path
from collections import Counter
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from mathutils.geometry import barycentric_transform,intersect_point_line
R=Path('/workspace/ronaldo-work');OUT=R/'hair-repair-v3';sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
YEAR=sys.argv[sys.argv.index('--')+1];P=OUT/YEAR;P.mkdir(exist_ok=True)
source=(R/'new-hair-sources/2017/fpk/hair_high.fmdl') if YEAR=='2017' else next((R/'input-2013').rglob('hair_high.fmdl'))
texroot=R/'new-hair-sources/2017/converted' if YEAR=='2017' else R/'input-2013/converted'
f=FmdlFile();f.readFile(str(source));s=bpy.context.scene;rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID']
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def cv(p):return Vector((p.x,-p.z,p.y))
def shape_face(p):
 if YEAR!='2017':return p.copy()
 x,y,z=p;q=p.copy();front=smooth(.075,.13,-y)
 # Small continuous sculpt: lower cheek volume, jaw corner and submental contour.
 cheek=math.exp(-((z-1.635)/.028)**2)*smooth(.025,.065,abs(x))*front
 q.x-=math.copysign(.0022*cheek,x);q.y+=.0012*cheek
 under=math.exp(-((z-1.592)/.022)**2)*(1-smooth(.135,.16,-y))*front
 q.z+=.0030*under;q.y+=.0035*under
 corner=math.exp(-((z-1.608)/.014)**2)*math.exp(-((abs(x)-.065)/.014)**2)*front
 q.x+=math.copysign(.0012*corner,x)
 neck=math.exp(-((z-1.565)/.032)**2)*smooth(.085,.12,-y)*(1-smooth(.045,.075,abs(x)))
 q.y+=.0040*neck
 return q
# Sculpt on a copy of source scene; retain UV/topology, weights, original materials.
sculpt={}
for name in ['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat']:
 o=bpy.data.objects[name];old=[v.co.copy() for v in o.data.vertices];oldn=[v.vector.copy() for v in o.data.corner_normals];newnorm=[]
 if YEAR=='2017':
  for v,p in zip(o.data.vertices,old):v.co=shape_face(p)
  for loop,n in zip(o.data.loops,oldn):
   p=old[loop.vertex_index];eps=1e-5;cols=[]
   for k in range(3):
    a=p.copy();b=p.copy();a[k]+=eps;b[k]-=eps;cols.append((shape_face(a)-shape_face(b))/(2*eps))
   jac=Matrix(cols).transposed();newnorm.append((jac.inverted_safe().transposed()@n).normalized())
  o.data.normals_split_custom_set(newnorm)
 sculpt[name]={'changed':sum((v.co-p).length>1e-8 for v,p in zip(o.data.vertices,old)),'max_displacement_m':max((v.co-p).length for v,p in zip(o.data.vertices,old))}
# Keep the original 2006 cap geometry/UV/normals/weights. Sample donor colour
# per output texel instead of interpolating discontinuous donor UV at vertices.
oldcap=bpy.data.objects['hair_high_0_fox_skin_mat'];om=oldcap.data
oldtree=BVHTree.FromPolygons([v.co for v in om.vertices],[list(p.vertices) for p in om.polygons])
# Weld positions for boundary detection only: UV-island seams are not holes.
keys=[tuple(round(q,6) for q in v.co) for v in om.vertices];positions={key:Vector(key) for key in keys}
edges=Counter(tuple(sorted((keys[p.vertices[i]],keys[p.vertices[(i+1)%len(p.vertices)]]))) for p in om.polygons for i in range(len(p.vertices)) if keys[p.vertices[i]]!=keys[p.vertices[(i+1)%len(p.vertices)]])
bound=[(positions[a],positions[b]) for (a,b),n in edges.items() if n==1]
edgepoints=[]
for a,b in bound:
 steps=max(1,math.ceil((b-a).length/.0004))
 edgepoints.extend(a.lerp(b,i/steps) for i in range(steps+1))
boundary_tree=KDTree(len(edgepoints))
for i,p in enumerate(edgepoints):boundary_tree.insert(p,i)
boundary_tree.balance()
# Skin reference assembled from original face+neck+cap, preserving per-corner UV.
skinverts=[];skinfaces=[];skinuv=[]
for ob in [bpy.data.objects['face_high_0_fox_skin_mat'],bpy.data.objects['face_high_2_fox_skin_mat'],oldcap]:
 offset=len(skinverts);skinverts.extend(v.co.copy() for v in ob.data.vertices)
 for poly in ob.data.polygons:
  skinfaces.append([offset+i for i in poly.vertices]);skinuv.append([Vector((*ob.data.uv_layers[0].data[i].uv,0)) for i in poly.loop_indices])
skintree=BVHTree.FromPolygons(skinverts,skinfaces)
oldimage=bpy.data.images['face_bsm_alp.png'];oldpixels=np.array(oldimage.pixels[:],np.float32).reshape(oldimage.size[1],oldimage.size[0],4)
original_cap_material=oldcap.data.materials[0]
cap=oldcap.copy();cap.data=oldcap.data.copy();cap.name='SCALP_NATIVE_2006_BAKED_DONOR_COLOR';s.collection.objects.link(cap);cap.data.materials.clear()
for name in ['hair_high_0_fox_skin_mat','hair_high_1_fox_hair_mat','hair_high_2_fox_head_shell_mat']:
 ob=bpy.data.objects.get(name)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
def loadimage(name):
 im=bpy.data.images.load(str(texroot/name),check_existing=False);im.alpha_mode='CHANNEL_PACKED';return im
source_cap=next(m for m in f.meshes if m.materialInstance.name=='fox_skin_mat')
def make_object(src,name):
 idx={id(v):i for i,v in enumerate(src.vertices)};faces=[[idx[id(v)] for v in reversed(ff.vertices)] for ff in src.faces];co=[cv(v.position) for v in src.vertices]
 if YEAR=='2014':
  # Mirror the authored side part to match the supplied 2014 right-temple photos.
  for p in co:p.x=-p.x
  faces=[list(reversed(face)) for face in faces]
  # Retain coherent cards; shorten and sweep the quiff into 2014.
  for i,p in enumerate(co):
   w=smooth(1.785,1.825,p.z);p.z-=max(0,p.z-1.805)*.24;p.x+=.007*w;p.y+=.004*w
   front=smooth(.075,.135,-p.y)*smooth(1.79,1.83,p.z);p.y+=.012*front;p.z-=.006*front
   back=smooth(-.025,.020,p.y)
   if back>0:
    q,n,fi,d=oldtree.find_nearest(p);out=Vector((q.x,q.y+.060,max(0,q.z-1.705))).normalized();p=p.lerp(q+out*.003,back*.92);co[i]=p
  # Close cut at temples, let the existing cap texture carry the shaved sides.
  faces=[face for face in faces if not (sum(abs(co[i].x) for i in face)/3>.061 and sum(co[i].z for i in face)/3<1.776)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(co,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob)
 for ui in range(src.vertexFields.uvCount):
  uv=mesh.uv_layers.new(name=f'UV{ui}')
  for loop in mesh.loops:
   q=src.vertices[loop.vertex_index].uv[ui];uv.data[loop.index].uv=(q.u,1-q.v)
 # Preserve authored normals; reflect their x component with the 2014 hair.
 normals=[cv(src.vertices[loop.vertex_index].normal) for loop in mesh.loops]
 if YEAR=='2014':
  for n in normals:n.x=-n.x
 mesh.normals_split_custom_set(normals)
 for v,sv in zip(mesh.vertices,src.vertices):
  for b,w in (sv.boneMapping or {}).items():
   if w>0:
    if b.name not in ob.vertex_groups:ob.vertex_groups.new(name=b.name)
    ob.vertex_groups[b.name].add([v.index],w,'REPLACE')
 ob.parent=rig;am=ob.modifiers.new('PES reference skinning','ARMATURE');am.object=rig
 for p in mesh.polygons:p.use_smooth=True
 return ob
# Full cap-bake UV is the native source UV, never a nearest-vertex UV transfer.
capim=loadimage('face_bsm_alp.png');caparr=np.array(capim.pixels[:],np.float32).reshape(capim.size[1],capim.size[0],4).copy();donorpixels=caparr.copy();H,W=caparr.shape[:2];covered=np.zeros((H,W),bool);cap_hairmask=np.zeros((H,W),np.float32)
def sample(arr,u,v):
 h,w=arr.shape[:2];x=max(0,min(w-1,u*(w-1)));y=max(0,min(h-1,v*(h-1)));x0=int(x);y0=int(y);x1=min(x0+1,w-1);y1=min(y0+1,h-1);a=x-x0;b=y-y0
 return (arr[y0,x0]*(1-a)+arr[y0,x1]*a)*(1-b)+(arr[y1,x0]*(1-a)+arr[y1,x1]*a)*b
facepath=(source.parent/'face_high.fmdl');ff=FmdlFile();ff.readFile(str(facepath));face_src=ff.meshes[2]
fverts=[];ffaces=[];fuv=[]
for sm in [face_src,source_cap]:
 ix={id(v):i for i,v in enumerate(sm.vertices)};offset=len(fverts);fverts.extend(cv(v.position) for v in sm.vertices)
 for face in sm.faces:
  ids=[ix[id(v)] for v in reversed(face.vertices)];ffaces.append([offset+i for i in ids]);fuv.append([Vector((sm.vertices[i].uv[0].u,1-sm.vertices[i].uv[0].v,0)) for i in ids])
ftree=BVHTree.FromPolygons(fverts,ffaces)
def temple_mask(p):
 x,y,z=p;side=smooth(.049,.075,abs(x));high=smooth(1.698,1.732,z);back=1-smooth(.100,.156,-y)
 upper_side=smooth(.020,.045,abs(x))*smooth(1.736,1.770,z)
 upper_front=smooth(1.762,1.783,z)
 seam=(1-smooth(.0005,.009,boundary_tree.find(p)[2]))*smooth(1.716,1.740,z)
 return max(side*high*back,side*smooth(1.750,1.777,z),upper_side,upper_front,seam)
def donor_sample(p):
 hit,n,fi,d=ftree.find_nearest(p);ids=ffaces[fi];q=barycentric_transform(hit,*[fverts[i] for i in ids],*fuv[fi]);return sample(donorpixels,q.x,q.y).copy()
def nearest_skin(p):
 hit,n,fi,d=skintree.find_nearest(p);ids=skinfaces[fi];q=barycentric_transform(hit,*[skinverts[i] for i in ids],*skinuv[fi]);return sample(oldpixels,q.x,q.y)
# World-space stroke locations on the right temple. Bake into cap diffuse, not
# floating geometry. A real part already exists in the authored 2013 source.
lines=[ [Vector((-.078,-.120,1.724)),Vector((-.079,-.096,1.743)),Vector((-.078,-.069,1.746)),Vector((-.077,-.048,1.743)),Vector((-.073,-.065,1.761)),Vector((-.063,-.083,1.779))], [Vector((-.078,-.114,1.704)),Vector((-.080,-.091,1.720)),Vector((-.080,-.064,1.727)),Vector((-.078,-.041,1.727))] ]
if YEAR=='2014':lines.append([Vector((-.038,-.144,1.790)),Vector((-.048,-.115,1.805)),Vector((-.058,-.080,1.797)),Vector((-.064,-.045,1.780)),Vector((-.064,-.018,1.760))])
ctree=BVHTree.FromPolygons([v.co for v in cap.data.vertices],[list(p.vertices) for p in cap.data.polygons])
projected=[];stroke_tree=None
if YEAR=='2014':
 for line in lines:
  dense=[]
  for a,b in zip(line,line[1:]):
   steps=max(1,math.ceil((b-a).length/.00035))
   dense.extend(ctree.find_nearest(a.lerp(b,i/steps))[0] for i in range(steps+1))
  projected.append(dense)
 points=[p for line in projected for p in line];stroke_tree=KDTree(len(points))
 for i,p in enumerate(points):stroke_tree.insert(p,i)
 stroke_tree.balance()
def stroke_distance(p):return stroke_tree.find(p)[2] if stroke_tree else 1.
boundary_dist=[min((v.co-(a+(b-a)*max(0,min(1,intersect_point_line(v.co,a,b)[1])))).length for a,b in bound) for v in cap.data.vertices]
scalp_skin=np.mean([nearest_skin(Vector(p)) for p in [(-.035,-.165,1.744),(-.045,-.161,1.742),(-.025,-.166,1.747)]],axis=0);scalp_skin[:3]*=.92
def hair_zone(p):
 x,y,z=p;front=smooth(.080,.145,-y);border=1.668+.108*front
 return smooth(border-.003,border+.010,z)
# Reuse actual short-crop scalp detail from the supplied 2017 source instead of
# a flat procedural cap. Only the 2014 top hair cards come from edited 2013.
crop_tree=None
if YEAR=='2014':
 cf=FmdlFile();cf.readFile(str(R/'new-hair-sources/2017/fpk/face_high.fmdl'));ch=FmdlFile();ch.readFile(str(R/'new-hair-sources/2017/fpk/hair_high.fmdl'));cropverts=[];cropfaces=[];cropuv=[]
 for sm in [cf.meshes[2],ch.meshes[1]]:
  ix={id(v):i for i,v in enumerate(sm.vertices)};offset=len(cropverts);cropverts.extend(cv(v.position) for v in sm.vertices)
  for face in sm.faces:
   ids=[ix[id(v)] for v in reversed(face.vertices)];cropfaces.append([offset+i for i in ids]);cropuv.append([Vector((sm.vertices[i].uv[0].u,1-sm.vertices[i].uv[0].v,0)) for i in ids])
 crop_tree=BVHTree.FromPolygons(cropverts,cropfaces);ci=bpy.data.images.load(str(R/'new-hair-sources/2017/converted/face_bsm_alp.png'),check_existing=False);ci.alpha_mode='CHANNEL_PACKED';crop_pixels=np.array(ci.pixels[:],np.float32).reshape(ci.size[1],ci.size[0],4)
def cropped_2014_colour(p):
 hit,n,fi,d=crop_tree.find_nearest(p);ids=cropfaces[fi];q=barycentric_transform(hit,*[cropverts[i] for i in ids],*cropuv[fi]);colour=sample(crop_pixels,q.x,q.y).copy()
 x,y,z=p;top=smooth(1.772,1.812,z)*(1-smooth(.042,.070,abs(x)))*hair_zone(p)
 colour[:3]=colour[:3]*(1-top)+np.array([.09,.06,.035])*top;colour[3]=1
 return colour
count=0;linepixels=0
for poly in cap.data.polygons:
 ids=list(poly.vertices);pts=np.array([tuple(cap.data.vertices[i].co) for i in ids]);uv=np.array([tuple(cap.data.uv_layers[0].data[i].uv) for i in poly.loop_indices]);xy=uv*np.array([W-1,H-1]);lo=np.maximum(0,np.floor(xy.min(axis=0)).astype(int));hi=np.minimum([W-1,H-1],np.ceil(xy.max(axis=0)).astype(int));
 if np.any(hi<lo):continue
 xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));a,b,c=xy;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
 if abs(den)<1e-8:continue
 w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1;valid=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
 for iy,ix in zip(*np.nonzero(valid)):
  x=int(xx[iy,ix]);y=int(yy[iy,ix]);p=Vector(w0[iy,ix]*pts[0]+w1[iy,ix]*pts[1]+w2[iy,ix]*pts[2]);colour=donor_sample(p)
  # Seam matching follows actual boundary distance, plus full original neck colour.
  neck=1-smooth(1.675,1.72,p.z)
  bd=sum(w*boundary_dist[i] for w,i in zip([w0[iy,ix],w1[iy,ix],w2[iy,ix]],ids))
  seam=(1-smooth(.001,.006,bd))*(1-temple_mask(p));weight=max(neck,seam)
  if weight>.001:colour=colour*(1-weight)+nearest_skin(p)*weight
  if YEAR=='2014':
   crop_weight=smooth(1.685,1.728,p.z);colour=colour*(1-crop_weight)+cropped_2014_colour(p)*crop_weight
   dist=stroke_distance(p);mask=1-smooth(.00055,.00105,dist)
   if mask>0:
    # Actual exposed-scalp colour, no white tube floating over hair.
    skin=scalp_skin;colour[:3]=colour[:3]*(1-mask)+skin[:3]*mask;linepixels+=1
  colour[3]=1;caparr[y,x]=colour;covered[y,x]=True;cap_hairmask[y,x]=hair_zone(p);count+=1
# Extend modified texels outside island edges for filtering/mip borders.
for iteration in range(8):
 prev=covered.copy();sums=np.zeros_like(caparr);msums=np.zeros((H,W),np.float32);n=np.zeros((H,W),np.float32)
 for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
  shifted=np.roll(prev,(dy,dx),(0,1));sums+=np.roll(caparr,(dy,dx),(0,1))*shifted[:,:,None];msums+=np.roll(cap_hairmask,(dy,dx),(0,1))*shifted;n+=shifted
 new=(~covered)&(n>0);caparr[new]=sums[new]/n[new,None];cap_hairmask[new]=msums[new]/n[new];covered|=new
capim.name=f'{YEAR}_Scalp_SeamMatched_BAKED';capim.pixels.foreach_set(caparr.ravel());capim.filepath_raw=str(P/f'{YEAR}_Scalp_SeamMatched_BAKED.png');capim.file_format='PNG';capim.save();capim.pack()
mat=original_cap_material.copy();mat.name=f'{YEAR}_Scalp_Baked_OneTexture';t=next(t for t in mat.node_tree.nodes if t.type=='TEX_IMAGE');t.image=capim;capim.alpha_mode='NONE';cap.data.materials.append(mat)
def apply_hair_mask(material,mask,name):
 h,w=mask.shape;im=bpy.data.images.new(name,width=w,height=h,alpha=True);im.colorspace_settings.name='Non-Color';rgba=np.ones((h,w,4),np.float32);rgba[:,:,:3]=mask[:,:,None];im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(P/(name+'.png'));im.file_format='PNG';im.save();im.pack()
 n=material.node_tree.nodes;l=material.node_tree.links;b=n.get('Principled BSDF');t=n.new('ShaderNodeTexImage');t.image=im
 for socket,a,z in [('Roughness',.58,.86),('Specular IOR Level',.5,.055)]:
  r=n.new('ShaderNodeMapRange');r.clamp=True;r.inputs['From Min'].default_value=0;r.inputs['From Max'].default_value=1;r.inputs['To Min'].default_value=a;r.inputs['To Max'].default_value=z;l.new(t.outputs['Color'],r.inputs['Value']);l.new(r.outputs[0],b.inputs[socket])
 return im
apply_hair_mask(mat,cap_hairmask,f'{YEAR}_Scalp_HairMask_BAKED')
# Remove the embedded 2006 hair shadow at temples without changing central face.
faceob=bpy.data.objects['face_high_2_fox_skin_mat'];farr=oldpixels.copy();FH,FW=farr.shape[:2];face_hairmask=np.zeros((FH,FW),np.float32);templepixels=0;facelinepixels=0
for poly in faceob.data.polygons:
 ids=list(poly.vertices);pts=np.array([tuple(faceob.data.vertices[i].co) for i in ids])
 if max(temple_mask(Vector(p)) for p in pts)<.0001:continue
 uv=np.array([tuple(faceob.data.uv_layers[0].data[i].uv) for i in poly.loop_indices]);xy=uv*np.array([FW-1,FH-1]);lo=np.maximum(0,np.floor(xy.min(axis=0)).astype(int));hi=np.minimum([FW-1,FH-1],np.ceil(xy.max(axis=0)).astype(int))
 if np.any(hi<lo):continue
 xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));a,b,c=xy;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
 if abs(den)<1e-8:continue
 w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1;valid=(w0>=0)&(w1>=0)&(w2>=0)
 for iy,ix in zip(*np.nonzero(valid)):
  x=int(xx[iy,ix]);y=int(yy[iy,ix]);p=Vector(w0[iy,ix]*pts[0]+w1[iy,ix]*pts[1]+w2[iy,ix]*pts[2]);weight=temple_mask(p)
  if weight<.0001:continue
  hit,n,fi,d=ftree.find_nearest(p);idsf=ffaces[fi];q=barycentric_transform(hit,*[fverts[i] for i in idsf],*fuv[fi]);col=sample(donorpixels,q.x,q.y)
  if YEAR=='2014':col=cropped_2014_colour(p)
  farr[y,x]=oldpixels[y,x]*(1-weight)+col*weight;templepixels+=1
  if YEAR=='2014':
   weight=1-smooth(.00055,.00105,stroke_distance(p))
   if weight>0:farr[y,x,:3]=farr[y,x,:3]*(1-weight)+scalp_skin[:3]*weight;facelinepixels+=1
  farr[y,x,3]=oldpixels[y,x,3];face_hairmask[y,x]=hair_zone(p)*temple_mask(p)
faceim=oldimage.copy();faceim.name=f'{YEAR}_Face_Temples_Clean_BAKED';faceim.pixels.foreach_set(farr.ravel());faceim.filepath_raw=str(P/f'{YEAR}_Face_Temples_Clean_BAKED.png');faceim.file_format='PNG';faceim.save();faceim.pack()
fm=faceob.data.materials[0].copy();fm.name=f'{YEAR}_Face_2006_TemplesClean';next(n for n in fm.node_tree.nodes if n.type=='TEX_IMAGE').image=faceim;faceob.data.materials[0]=fm;apply_hair_mask(fm,face_hairmask,f'{YEAR}_Face_HairMask_BAKED')
# Import actual authored hair, excluding stencil/hidden head shells.
hairobjs=[]
for mi,m in enumerate(f.meshes):
 if m==source_cap or 'head_shell' in m.materialInstance.name:continue
 if YEAR=='2014' and 'hair_transfer' in m.materialInstance.name:continue
 ob=make_object(m,f'{YEAR}_AUTHORED_HAIR_{mi}');mat=bpy.data.materials.new(f'{YEAR}_Hair_Material_{mi}');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.55;bs.inputs['Specular IOR Level'].default_value=.12
 dual=m.materialInstance.name=='Material.002';file='hair_parts_bsm_alp.png';im=loadimage(file)
 if YEAR=='2014':
  arr=np.array(im.pixels[:],np.float32).reshape(im.size[1],im.size[0],4);lum=arr[:,:,:3].mean(axis=2);arr[:,:,:3]=np.array([.007,.004,.002])+lum[:,:,None]*np.array([.024,.014,.007]);im.pixels.foreach_set(arr.ravel());im.name='2014_Hair_Dark_BAKED';im.filepath_raw=str(P/'2014_Hair_Dark_BAKED.png');im.file_format='PNG';im.save()
 im.pack();t=n.new('ShaderNodeTexImage');t.image=im;uv=n.new('ShaderNodeUVMap');uv.uv_map='UV1' if dual else 'UV0';l.new(uv.outputs[0],t.inputs['Vector']);l.new(t.outputs['Color'],bs.inputs['Base Color'])
 if dual:
  al=loadimage('hair_alpha8.png');al.pack();a=n.new('ShaderNodeTexImage');a.image=al;u=n.new('ShaderNodeUVMap');u.uv_map='UV0';l.new(u.outputs[0],a.inputs['Vector']);l.new(a.outputs['Alpha'],bs.inputs['Alpha'])
 else:l.new(t.outputs['Alpha'],bs.inputs['Alpha'])
 if YEAR=='2014':
  mult=n.new('ShaderNodeMixRGB');mult.blend_type='MULTIPLY';mult.inputs[0].default_value=1;mult.inputs[2].default_value=(.55,.55,.55,1);l.new(t.outputs['Color'],mult.inputs[1]);l.new(mult.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.72;bs.inputs['Specular IOR Level'].default_value=.04
 mat.surface_render_method='DITHERED';ob.data.materials.append(mat);hairobjs.append(ob)
# Save five-sided evidence. Engine common eye textures remain absent in the PC source.
bpy.data.objects['Rim'].data.energy=2
for o in bpy.data.objects:
 if o.type in ['LIGHT','CAMERA','ARMATURE']:o.hide_set(True)
for scr in bpy.data.screens:
 for a in scr.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=False;a.spaces.active.region_3d.view_location=(0,-.06,1.72);a.spaces.active.region_3d.view_distance=.43
bpy.ops.object.select_all(action='DESELECT');cap.select_set(True);bpy.context.view_layer.objects.active=cap
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100
name=f'Ronaldo_{YEAR}_REPAIR_V3.blend';bpy.ops.wm.save_as_mainfile(filepath=str(P/name))
report={'year':YEAR,'scalp_topology':'native 2006 geometry, UV, normals and weights unchanged; donor sampled per texel','scalp_uv_transfer_removed':True,'physical_open_boundary_edges':len(bound),'uv_seams_excluded_from_boundary_feather':True,'cap_texture_baked':True,'baked_texels':count,'shaved_line_texture_pixels':linepixels+facelinepixels,'temple_texture_pixels_cleaned':templepixels,'sculpt':sculpt,'source_hair':str(source),'source_2013_hair_restyled':YEAR=='2014','android_verified':False};(P/'build-report.json').write_text(json.dumps(report,indent=2))
for label,loc in [('front',(0,-.70,1.77)),('right',(-.65,-.04,1.74)),('left',(.65,-.04,1.74)),('back',(0,.65,1.73)),('three-quarter',(-.27,-.65,1.80))]:
 cam=s.camera;cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37;s.render.filepath=str(P/(label+'.png'));bpy.ops.render.render(write_still=True)
print('REPAIR_V3_COMPLETE',YEAR,report,flush=True)
