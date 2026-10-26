import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath='/workspace/analysis/hulk-avengers-v2/HULK_AVENGERS_V2.blend')
# Carry every head component through the same enlargement, fixing the original body rim.
for o in list(bpy.data.objects):
 if o.type!='MESH':continue
 ma=o.matrix_world.copy();iv=ma.inverted()
 for v in o.data.vertices:
  p=ma@v.co;t=max(0,min(1,(p.z-1.43)/.10));t=t*t*(3-2*t)
  jaw=math.exp(-((p.z-1.575)/.047)**2)
  p.x*=1+t*(.20+.12*jaw);p.y=-.075+(p.y+.075)*(1+.13*t);p.z=1.53+(p.z-1.53)*(1+.04*t);v.co=iv@p
# Eyelid hoods close the excessive sclera aperture without enlarging the eyeballs.
face=bpy.data.objects['HULK_FACE_SCULPT'];face.data.calc_loop_triangles();bv=BVHTree.FromObject(face,bpy.context.evaluated_depsgraph_get());skin=face.data.materials[0]
from mathutils.geometry import barycentric_transform
for side in [-1,1]:
 eye=bpy.data.objects['HULK_EYE_'+str(side)];center=sum([eye.matrix_world@v.co for v in eye.data.vertices],Vector())/len(eye.data.vertices)
 verts=[];polys=[];uvs=[]
 for j in range(7):
  t=j/6
  for i in range(96):
   a=i*math.tau/96;dx=.0140*math.cos(a);dz=.0030*math.sin(a)+side*.045*dx
   inner=Vector((center.x+dx,center.y-.0135*math.sqrt(max(.1,1-(dx/.022)**2-(dz/.011)**2))-.0006,center.z+dz))
   query=Vector((center.x+.025*math.cos(a),center.y-.010,center.z+.0115*math.sin(a)))
   hit,n,idx,dist=bv.find_nearest(query)
   if hit is None:hit=query;idx=0
   p=inner.lerp(hit,t);p.y-=.0011*math.sin(t*math.pi);verts.append(p)
   poly=face.data.polygons[idx];lis=list(poly.loop_indices)[:3];ps=[face.data.vertices[face.data.loops[k].vertex_index].co for k in lis];uv=[Vector((*face.data.uv_layers[0].data[k].uv,0))for k in lis];uvs.append(barycentric_transform(hit,*ps,*uv))
   if j:polys.append(((j-1)*96+i,(j-1)*96+(i+1)%96,j*96+(i+1)%96,j*96+i))
 me=bpy.data.meshes.new('Narrow anatomical eye hood');me.from_pydata(verts,[],polys);me.materials.append(skin);o=bpy.data.objects.new('HULK_EYELID_HOOD_'+str(side),me);bpy.context.collection.objects.link(o);layer=me.uv_layers.new(name='UVMap')
 for l in me.loops:layer.data[l.index].uv=uvs[l.vertex_index].xy
 for p in me.polygons:p.use_smooth=True
# Original source packed diffuse is also supplied separately for later body colour work.
im=bpy.data.images['Hulk_skin_PACKED'];im.filepath_raw=str(R/'Hulk_skin_diffuse.png');im.file_format='PNG';im.save()
s=bpy.context.scene;s['revision']='Hulk v3 broader head jaw and neck, narrow eye hoods';s['game_verified']=False
s.camera.data.ortho_scale=.47;s.cycles.samples=32
for name,ang in [('front',0),('three_quarter',35),('profile',90),('back',180)]:
 a=math.radians(ang);s.camera.location=(.7*math.sin(a),-.07-.7*math.cos(a),1.72);s.camera.rotation_euler=(Vector((0,-.07,1.65))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'))
 if name=='three_quarter':bpy.ops.wm.save_as_mainfile(filepath=str(R/'HULK_GAME_V3.blend'))
 bpy.ops.render.render(write_still=True)
