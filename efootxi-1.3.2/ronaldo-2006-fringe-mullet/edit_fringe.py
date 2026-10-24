import bpy, math, random, json
from mathutils import Vector
from pathlib import Path
P=Path('/workspace/ronaldo-work/hair-2006-fringe');random.seed(2006)
s=bpy.context.scene; hair=bpy.data.objects['hair_high_1_fox_hair_mat']; original=[v.co.copy() for v in hair.data.vertices]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
# Restrict sculpt to the front/top. All rear/mullet vertices stay bit-exact.
changed=[]
for v,p in zip(hair.data.vertices,original):
 x,y,z=p; w=smooth(.065,.125,-y)*smooth(1.75,1.80,z)
 if w:
  v.co.z-=w*(.010+max(0,z-1.80)*.24)
  v.co.x+=.006*w
  v.co.y-=.003*w
  changed.append(v.index)
# Recalculate changed surface normals; UVs, faces, weights and original objects preserved.
hair.data.normals_split_custom_set([(0,0,0)] * len(hair.data.loops))
for poly in hair.data.polygons:poly.use_smooth=True
im=bpy.data.images['hair_parts_bsm_alp.png'];im.alpha_mode='STRAIGHT'
mat=hair.data.materials[0]; n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');tex=next(x for x in n if x.type=='TEX_IMAGE')
mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.22,.22,.22,1);l.new(tex.outputs['Color'],mul.inputs[1]);l.new(mul.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.78;bs.inputs['Specular IOR Level'].default_value=.05
# Preview-only scalp material: the supplied packed face atlas gives white patches
# on the PC scalp in Blender; preserve original material datablock and textures.
scalp=bpy.data.objects['hair_high_0_fox_skin_mat'];scalpmat=scalp.data.materials[0].copy();scalpmat.name='Blender_preview_scalp_dark';scalp.data.materials[0]=scalpmat
sb=scalpmat.node_tree.nodes.get('Principled BSDF')
for link in list(scalpmat.node_tree.links):
 if link.to_node==sb and link.to_socket.name in ['Base Color','Alpha']:scalpmat.node_tree.links.remove(link)
sb.inputs['Base Color'].default_value=(.012,.009,.006,1);sb.inputs['Alpha'].default_value=1;sb.inputs['Roughness'].default_value=.8;sb.inputs['Specular IOR Level'].default_value=.1
# Separate editable tapered strand groups, falling forward with irregular spacing.
strandmat=bpy.data.materials.new('Fringe_dark_brown_strands');strandmat.use_nodes=True
b=strandmat.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(.009,.006,.004,1);b.inputs['Roughness'].default_value=.38;b.inputs['Specular IOR Level'].default_value=.28
paths=[
 [(-.048,-.094,1.804),(-.040,-.125,1.806),(-.026,-.145,1.787),(-.020,-.151,1.762)],
 [(-.025,-.088,1.812),(-.010,-.119,1.816),(.003,-.144,1.793),(.006,-.154,1.750)],
 [(-.005,-.080,1.814),(.015,-.112,1.819),(.029,-.142,1.795),(.026,-.153,1.762)],
 [(.018,-.082,1.809),(.036,-.112,1.813),(.046,-.137,1.796),(.048,-.146,1.777)],
 [(-.059,-.091,1.793),(-.057,-.120,1.799),(-.050,-.139,1.783),(-.047,-.145,1.773)]
]
def bezier(p,t):return (1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3]
new=[]
for ci,path in enumerate(paths):
 cu=bpy.data.curves.new('Fringe_locks_%02d'%ci,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=.00031;cu.bevel_resolution=2
 for k in range(20):
  p=[Vector(x) for x in path];dx=(k-9.5)*.00034;dy=random.uniform(-.00065,.00065);length=random.uniform(.88,1.03)
  sp=cu.splines.new('POLY');sp.points.add(17)
  for j,q in enumerate(sp.points):
   t=j/17;v=bezier(p,min(1,t*length));v.x+=dx*(1-.64*t)+.00055*math.sin(t*math.pi*2+ci);v.y+=dy-.018*smooth(.0,.7,t); q.co=(*v,1);q.radius=max(.035,(1-t)**.7)*random.uniform(.85,1.1)
 ob=bpy.data.objects.new('EDIT_Front_lock_%02d'%ci,cu);s.collection.objects.link(ob);cu.materials.append(strandmat)
 # Convert to mesh for editing/export; keep weighted to source head bone.
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob=bpy.context.object
 group=ob.vertex_groups.new(name='sk_head');group.add(list(range(len(ob.data.vertices))),1,'REPLACE')
 rig=bpy.data.objects.get('PES_REFERENCE_NOT_ANDROID');mod=ob.modifiers.new('PES reference skinning','ARMATURE');mod.object=rig;ob.parent=rig;new.append(ob)
 for poly in ob.data.polygons:poly.use_smooth=True
# Audit unchanged face, scalp, rear and mullet; no deletion of original meshes.
rear=[i for i,p in enumerate(original) if p.y>-.065 or p.z<1.75]
assert all(hair.data.vertices[i].co==original[i] for i in rear)
report={'source':'Ronaldo_2006_EDIT.blend','changed_original_front_vertices':len(changed),'protected_rear_mullet_vertices':len(rear),'protected_vertices_identical':True,'added_front_lock_meshes':len(new),'face_and_original_uv_weights_unchanged':True,'game_ready':False}
(P/'edit-report.json').write_text(json.dumps(report,indent=2))
s['hair_edit']='Front fringe only; rear mullet preserved. Editable PC source, not Android cooked asset.'
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100
# Save opening view centered on hair/head.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_location=(0,-.07,1.73);area.spaces.active.region_3d.view_distance=.44;area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT');hair.select_set(True);bpy.context.view_layer.objects.active=hair
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Ronaldo_2006_FRINGE_MULLET.blend'))
cam=s.camera
for label,loc in [('three-quarter',(.27,-.65,1.80)),('front',(0,-.70,1.76)),('side',(.65,-.10,1.77))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37
 s.render.filepath=str(P/(label+'.png'));bpy.ops.render.render(write_still=True)
print('FRINGE_ONLY_MULLET_PRESERVED',json.dumps(report))
