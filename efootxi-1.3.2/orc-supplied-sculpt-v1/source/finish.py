import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from scipy.ndimage import distance_transform_edt
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'ORC_BAKED_STAGE.blend'));low=bpy.data.objects['ORC_GAME_LOD'];s=bpy.context.scene
# The bake images store linear floats. Compose cavity gently in linear light.
color=bpy.data.images.get('Orc source material diffuse');ao=bpy.data.images.get('Orc high sculpt cavity');a=np.empty(len(color.pixels),np.float32);color.pixels.foreach_get(a);a=a.reshape(-1,4);z=np.empty(len(ao.pixels),np.float32);ao.pixels.foreach_get(z);z=z.reshape(-1,4)
# Fill missed bake rays and atlas margins from the nearest valid source pixel.
valid=a[:,3]>.5
if not valid.all():
 idx=distance_transform_edt(~valid.reshape(2048,2048),return_distances=False,return_indices=True);near=(idx[0]*2048+idx[1]).reshape(-1);a[~valid,:3]=a[near[~valid],:3];z[~valid,:3]=z[near[~valid],:3]
# AO PNG was saved with sRGB metadata, Blender's buffer reopens to linear.
a[:,:3]*=(.63+.37*np.clip(z[:,:1],0,1));a[:,3]=1
im=bpy.data.images.new('Orc game diffuse atlas - source sculpt cavities',2048,2048,alpha=True);im.pixels.foreach_set(a.reshape(-1));im.filepath_raw=str(R/'atlas.png');im.file_format='PNG';im.save();im.pack()
mat=bpy.data.materials.new('ORC_GAME_ATLAS');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=im;l.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.68;bs.inputs['Specular IOR Level'].default_value=.18
# Normal bake is provided for Blender. Native export uses the existing diffuse shader.
normal=bpy.data.images.get('Orc high sculpt tangent normals');normal.colorspace_settings.name='Non-Color';tn=n.new('ShaderNodeTexImage');tn.image=normal;nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;l.new(tn.outputs['Color'],nm.inputs['Color'])
l.new(nm.outputs['Normal'],bs.inputs['Normal'])
# Blender preview uses the baked tangent normal; native game uses geometric normals.
low.data.materials.clear();low.data.materials.append(mat)
for p in low.data.polygons:p.material_index=0
# Continuous native head/neck/chest weights; face and tusks remain rigid together.
for g in list(low.vertex_groups):low.vertex_groups.remove(g)
for name in ['sk_head','sk_cervicalspine_02','sk_spine_03']:low.vertex_groups.new(name=name)
def smooth(v):v=max(0,min(1,v));return v*v*(3-2*v)
for v in low.data.vertices:
 x,y,z=v.co;h=smooth((z-1.53)/.075);c=smooth((z-1.45)/.08);chest=(1-h)*(1-c)
 shoulder=smooth((abs(x+.0047)-.08)/.11)*smooth((1.61-z)/.12)
 chest=chest+(1-chest)*shoulder;h*=1-shoulder;neck=1-h-chest
 for name,w in [('sk_head',h),('sk_cervicalspine_02',neck),('sk_spine_03',chest)]:
  if w>1e-8:low.vertex_groups[name].add([v.index],w,'REPLACE')
# Export UV seam vertices, retaining the original source shape in rest pose.
mesh=low.data;mesh.calc_loop_triangles();uv=mesh.uv_layers.active;vv=[];tt=[];lookup={};names={g.index:g.name for g in low.vertex_groups}
for tri in mesh.loop_triangles:
 out=[]
 for li in tri.loops:
  loop=mesh.loops[li];v=mesh.vertices[loop.vertex_index];u=uv.data[li].uv;normal=mesh.corner_normals[li].vector;key=(v.index,round(u.x,7),round(u.y,7))
  if key not in lookup:
   weights={names[g.group]:g.weight for g in v.groups if g.weight>1e-8};total=sum(weights.values());weights={k:w/total for k,w in weights.items()};assert abs(sum(weights.values())-1)<1e-6
   lookup[key]=len(vv);vv.append({'p':list(v.co),'n':list(normal),'uv':list(u),'weights':weights})
  out.append(lookup[key])
 tt.append(out)
assert len(vv)<65532,len(vv)
(R/'native_geometry.json').write_text(json.dumps({'vertices':vv,'triangles':tt}));(R/'export-validation.json').write_text(json.dumps({'visible_vertices':len(vv),'triangles':len(tt),'weights_normalized':True,'fixed_source_expression':True,'new_eyeball_geometry_added':False,'phone_tested':False},indent=2));print('GEOMETRY',len(vv),len(tt),flush=True)
# Append the original Android 166-bone rest rig, solely for Blender posing.
source=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-hair-v1/original-export/Game/Assets/character/RealFace/SK_4522_Face.gltf')
old=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(source));new=set(bpy.data.objects)-old;arm=next(o for o in new if o.type=='ARMATURE')
for obj in new:
 if obj!=arm and obj.type=='MESH':bpy.data.objects.remove(obj,do_unlink=True)
arm.name='ORC_NATIVE_166_BONE_RIG';print('HEAD_REST',list(arm.matrix_world@arm.data.bones['sk_head'].head_local),flush=True);mod=low.modifiers.new('Native head neck chest skinning','ARMATURE');mod.object=arm;low.parent=arm;low.matrix_parent_inverse=arm.matrix_world.inverted();arm.show_in_front=False;arm.hide_render=True
# Safe example poses, while the saved scene opens at the original rest shape.
s.frame_start=1;s.frame_end=80
for frame,angle in [(1,0),(20,-30),(40,30),(60,0),(80,0)]:
 pb=arm.pose.bones['sk_head'];pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,math.radians(angle));pb.keyframe_insert(data_path='rotation_euler',frame=frame)
s.frame_set(1)
# Studio preview, clearly distinct from a screenshot of the game.
s.render.engine='CYCLES';s.cycles.use_denoising=False;s.cycles.samples=32;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('Orc studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.04,.04,.04,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3
s.view_settings.view_transform='AgX';s.view_settings.exposure=0
for obj in list(bpy.data.objects):
 if obj.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(obj,do_unlink=True)
def light(name,loc,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,-.02,1.68))-ob.location).to_track_quat('-Z','Y').to_euler()
light('Key',(-.45,-.65,2.1),10,.6);light('Fill',(.5,-.35,1.8),4,.5);light('Rim',(.2,.4,2),12,.5)
d=bpy.data.cameras.new('Orc preview camera');c=bpy.data.objects.new('Orc preview camera',d);s.collection.objects.link(c);s.camera=c;d.type='ORTHO';d.ortho_scale=.49
for name,angle in [('orc_front',0),('orc_quarter',35),('orc_profile',90)]:
 a=math.radians(angle);c.location=(math.sin(a),-.015-math.cos(a),1.69);c.rotation_euler=(Vector((-.0047,-.015,1.661))-c.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
# Pack source atlases and name the original geometry unambiguously.
for image in bpy.data.images:
 if image.source=='FILE' and image.pixels:image.pack()
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_extras=False;area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.object.select_all(action='DESELECT');low.select_set(True);bpy.context.view_layer.objects.active=low
bpy.ops.wm.save_as_mainfile(filepath=str(R/'ORC_GAME_RIGGED.blend'),compress=True)
print('FINISHED',flush=True)
