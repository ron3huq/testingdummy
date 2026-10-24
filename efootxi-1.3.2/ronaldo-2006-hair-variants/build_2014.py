import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/workspace/ronaldo-work');P=R/'new-hair-sources/2014-blender';P.mkdir(exist_ok=True);random.seed(2014)
s=bpy.context.scene
# Start from original 2006 face. No old/spiky/mullet hair cards are used for 2014.
for name in ['hair_high_1_fox_hair_mat','hair_high_2_fox_head_shell_mat']:
 o=bpy.data.objects.get(name)
 if o:bpy.data.objects.remove(o,do_unlink=True)
original_cap=bpy.data.objects['hair_high_0_fox_skin_mat'];rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID']
cap=original_cap.copy();cap.data=original_cap.data.copy();cap.name='2014_CROPPED_HAIR_CAP';s.collection.objects.link(cap)
# Original nape skin shader is mixed only inside the cropped hair area.
mat=cap.data.materials[0].copy();mat.name='2014_Cropped_Sides_Original_Nape';cap.data.materials[0]=mat
# Subdivide only cap, never original face meshes; smooth masks without triangles.
mod=cap.modifiers.new('Scalp mask subdivision','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=2;bpy.context.view_layer.objects.active=cap;bpy.ops.object.modifier_apply(modifier=mod.name)
attr=cap.data.color_attributes.new(name='2014_Hair_Mask',type='FLOAT_COLOR',domain='POINT')
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
for v in cap.data.vertices:
 x,y,z=v.co;front=smooth(.08,.147,-y);threshold=1.662+.117*front
 # Higher border above the ears; front retains natural original face skin.
 threshold+=.008*smooth(.05,.075,abs(x))*(1-front)
 mask=smooth(threshold-.005,threshold+.008,z)
 attr.data[v.index].color=(mask,mask,mask,1)
 if mask>.01:
  out=Vector((x,y+.060,max(0,z-1.705)));out.normalize();v.co+=out*.0015*mask
cap.data.normals_split_custom_set([(0,0,0)]*len(cap.data.loops))
for ff in cap.data.polygons:ff.use_smooth=True
n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');tex=next(x for x in n if x.type=='TEX_IMAGE')
col=n.new('ShaderNodeVertexColor');col.layer_name=attr.name
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1500;noise.inputs['Detail'].default_value=2
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.014,.010,.007,1);ramp.color_ramp.elements[1].color=(.065,.045,.030,1);l.new(noise.outputs['Fac'],ramp.inputs[0])
mix=n.new('ShaderNodeMixRGB');l.new(col.outputs['Color'],mix.inputs[0]);l.new(tex.outputs['Color'],mix.inputs[1]);l.new(ramp.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],bs.inputs['Base Color']);l.new(col.outputs['Color'],bs.inputs['Alpha']);mat.surface_render_method='DITHERED';bs.inputs['Roughness'].default_value=.7;bs.inputs['Specular IOR Level'].default_value=.15
# Continuous physical hair base prevents exposed scalp between swept locks.
# Only the cap copy is shaped, never the original face or neck.
import bmesh
base_mesh=cap.data.copy();base_mesh.name='2014_coherent_hair_base';bm=bmesh.new();bm.from_mesh(base_mesh)
bad=[]
for face in bm.faces:
 c=face.calc_center_median();front=smooth(.08,.147,-c.y);threshold=1.662+.117*front+.008*smooth(.05,.075,abs(c.x))*(1-front)
 if c.z<max(1.765,threshold+.002):bad.append(face)
bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(base_mesh);bm.free()
for v in base_mesh.vertices:
 top=smooth(1.755,1.805,v.co.z);out=Vector((v.co.x,v.co.y+.060,max(0,v.co.z-1.705)));out.normalize();v.co+=out*.0018;v.co.z+=.007*top;v.co.x+=.003*top
base_ob=bpy.data.objects.new('2014_HAIR_BASE_NOT_FACE',base_mesh);s.collection.objects.link(base_ob);base_ob.parent=rig
base_mat=bpy.data.materials.new('2014_Coherent_dark_hair');base_mat.use_nodes=True;bb=base_mat.node_tree.nodes.get('Principled BSDF');bb.inputs['Base Color'].default_value=(.012,.008,.004,1);bb.inputs['Roughness'].default_value=.8;bb.inputs['Specular IOR Level'].default_value=.08;base_mesh.materials.clear();base_mesh.materials.append(base_mat)
base_mesh.normals_split_custom_set([(0,0,0)]*len(base_mesh.loops))
for face in base_mesh.polygons:face.use_smooth=True
bm=bmesh.new();bm.from_mesh(base_mesh);deform=bm.verts.layers.deform.active
if deform:
 for v in bm.verts:v[deform].clear()
bm.to_mesh(base_mesh);bm.free()
base_ob.vertex_groups.clear();g=base_ob.vertex_groups.new(name='sk_head');g.add(list(range(len(base_mesh.vertices))),1,'REPLACE');am=base_ob.modifiers.new('PES reference skinning','ARMATURE');am.object=rig

bm=bmesh.new();bm.from_mesh(cap.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_center_median().z<1.685],context='FACES');bm.to_mesh(cap.data);bm.free()
bpy.context.view_layer.update();bvh=BVHTree.FromObject(cap,bpy.context.evaluated_depsgraph_get());base_bvh=BVHTree.FromObject(base_ob,bpy.context.evaluated_depsgraph_get())
def surface(x,y):
 hit,*_=bvh.ray_cast(Vector((x,y,2)),Vector((0,0,-1)))
 return hit
mats=[]
for i,color in enumerate([(.010,.007,.004),(.017,.011,.006),(.028,.019,.010)]):
 m=bpy.data.materials.new('2014_swept_locks_%d'%i);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=.62;b.inputs['Specular IOR Level'].default_value=.06;mats.append(m)
cu=bpy.data.curves.new('2014_Swept_Side_Part','CURVE');cu.dimensions='3D';cu.bevel_depth=.00019;cu.bevel_resolution=1
for m in mats:cu.materials.append(m)
locks=0
# Sweeping waves lie on the scalp with lifted middle; both ends settle onto head,
# unlike the rejected upright spike bundles.
for row,y in enumerate([-.145+i*.005 for i in range(33)]):
 for x in [-.034+i*.007 for i in range(12)]:
  sx=x+random.uniform(-.003,.003);sy=y+random.uniform(-.003,.003);ex=min(.071,sx+.035+random.uniform(-.006,.008));ey=sy+.020+random.uniform(-.008,.009)
  start=surface(sx,sy);end=surface(ex,ey)
  if start is None or end is None or start.z<1.755:continue
  front=smooth(.06,.14,-sy);lift=.008+.010*front+random.uniform(-.002,.003)
  for j in range(22):
   dx=random.uniform(-.0025,.0025);dy=random.uniform(-.0025,.0025)
   sp=cu.splines.new('POLY');sp.points.add(17);sp.material_index=random.choices([0,1,2],[.65,.30,.05])[0]
   for k,p in enumerate(sp.points):
    t=k/17;px=sx+(ex-sx)*t+dx*(1-.4*t);py=sy+(ey-sy)*t+dy
    hit=surface(px,py)
    if hit is None:hit=start.lerp(end,t)
    hit.z+=.002+.007*smooth(1.755,1.805,hit.z)+.004*math.sin(math.pi*t)**.85
    hit.x+=.001*math.sin(t*math.pi*2+row*.15)*math.sin(t*math.pi)
    p.co=(*hit,1);p.radius=max(.025,math.sin(math.pi*(.10+.90*t))**.5)*random.uniform(.8,1.1)
  locks+=1
# Short side of the part, also laid down.
for row in range(21):
 sy=-.137+row*.007
 for j in range(30):
  sx=-.045+random.uniform(-.003,.003);start=surface(sx,sy)
  if start is None:continue
  sp=cu.splines.new('POLY');sp.points.add(13)
  for k,p in enumerate(sp.points):
   t=k/13;px=sx-.025*t;py=sy+.008*t;hit=surface(px,py)
   if hit is None:hit=start+Vector((-.02*t,.008*t,-.01*t))
   hit.z+=.001+.004*math.sin(math.pi*t);p.co=(*hit,1);p.radius=max(.025,(1-t)**.5)
ob=bpy.data.objects.new('EDIT_2014_Swept_Hair',cu);s.collection.objects.link(ob);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob=bpy.context.object
ob.parent=rig;g=ob.vertex_groups.new(name='sk_head');g.add(list(range(len(ob.data.vertices))),1,'REPLACE');mod=ob.modifiers.new('PES reference skinning','ARMATURE');mod.object=rig
for f in ob.data.polygons:f.use_smooth=True
# Sculpted part and shaved lightning lines on anatomical right side.
line_mat=bpy.data.materials.new('2014_Shaved_Part_Skin');line_mat.use_nodes=True;b=line_mat.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(.38,.25,.17,1);b.inputs['Roughness'].default_value=.8;b.inputs['Specular IOR Level'].default_value=.1
# Trace in world XYZ on actual scalp with closest-point projection.
def line(name,coords,radius):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(coords)-1)
 for p,v in zip(sp.points,coords):
  tree=base_bvh if v[2]>1.775 else bvh
  hit,normal,idx,dist=tree.find_nearest(Vector(v));hit+=normal*.0009;p.co=(*hit,1)
 o=bpy.data.objects.new(name,c);s.collection.objects.link(o);c.materials.append(line_mat);o.parent=rig
line('2014_Side_Part',[(-.038,-.146+i*.006,1.80) for i in range(30)],.00075)
# Two curved shaved lines photographed on right temple, not the back of the neck.
line('2014_Temple_Zigzag_A',[(-.077,-.105,1.733),(-.078,-.088,1.747),(-.078,-.066,1.751),(-.078,-.044,1.747),(-.078,-.062,1.768),(-.066,-.083,1.789)],.0008)
line('2014_Temple_Zigzag_B',[(-.078,-.101,1.712),(-.080,-.084,1.724),(-.080,-.061,1.731),(-.080,-.039,1.732)],.00075)
for o in list(bpy.data.objects):
 if o.name.startswith('2014_Side_Part') or o.name.startswith('2014_Temple_Zigzag'):
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');o=bpy.context.object
  g=o.vertex_groups.new(name='sk_head');g.add(list(range(len(o.data.vertices))),1,'REPLACE');am=o.modifiers.new('PES reference skinning','ARMATURE');am.object=rig
for o in bpy.data.objects:
 if o.type in ['ARMATURE','LIGHT','CAMERA']:o.hide_set(True)
for scr in bpy.data.screens:
 for a in scr.areas:
  if a.type=='VIEW_3D':a.spaces.active.overlay.show_overlays=False;a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_location=(0,-.06,1.72);a.spaces.active.region_3d.view_distance=.44
bpy.data.objects['Rim'].data.energy=2.0
s['variant']='2014 photo-guided hair; unchanged original 2006 face. No Android cook.'
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Ronaldo_2014_PHOTO_HAIR_2006_FACE.blend'))
(P/'report.json').write_text(json.dumps({'original_2006_face_unchanged':True,'hair_source':'built from supplied 2014 photos, not supplied model','swept_locks':locks,'spiky_variant_used':False,'android_verified':False},indent=2))
cam=s.camera
for label,loc in [('front',(0,-.70,1.77)),('three-quarter',(-.27,-.65,1.80)),('side',(-.65,-.04,1.74)),('back',(0,.65,1.73))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37;s.render.filepath=str(P/(label+'.png'));bpy.ops.render.render(write_still=True)
print('2014_DONE',locks)
