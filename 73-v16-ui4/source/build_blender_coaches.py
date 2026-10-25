import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
P=Path('/workspace/ronaldo-work/73-ui4');label=sys.argv[-1];d=json.loads((P/label/'blender-model.json').read_text());bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
arm=bpy.data.armatures.new('Supplied_PES_skeleton');rig=bpy.data.objects.new('Source_Rig',arm);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for name,row in d['bones'].items():
 b=arm.edit_bones.new(name);b.head=row['head'];b.tail=Vector(b.head)+Vector((0,0,.012))
for name,row in d['bones'].items():
 if row['parent'] and row['parent']in arm.edit_bones:arm.edit_bones[name].parent=arm.edit_bones[row['parent']]
bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
for row in d['meshes']:
 m=bpy.data.meshes.new(row['name']);m.from_pydata(row['positions'],[],row['triangles']);m.update();o=bpy.data.objects.new(row['name'],m);bpy.context.collection.objects.link(o);uv=m.uv_layers.new(name='UVMap')
 for loop in m.loops:uv.data[loop.index].uv=row['uv'][loop.vertex_index]
 for p in m.polygons:p.use_smooth=True
 for vi,mapping in enumerate(row['weights']):
  for name,w in mapping.items():
   g=o.vertex_groups.get(name)or o.vertex_groups.new(name=name);g.add([vi],w,'REPLACE')
 mod=o.modifiers.new('Source skeleton','ARMATURE');mod.object=rig;o.parent=rig
 mat=bpy.data.materials.new(row['material']);mat.use_nodes=True;n=mat.node_tree.nodes;shader=n.get('Principled BSDF');shader.inputs['Roughness'].default_value=.68
 if row['texture']:
  tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(row['texture']);mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
  if any(x in row['material'].lower()for x in['hair_mat','head_shell','eyelash','eyeline','occlusion','collar']):mat.node_tree.links.new(tex.outputs['Alpha'],shader.inputs['Alpha']);mat.surface_render_method='DITHERED'
 o.data.materials.append(mat)
 if 'collar'in row['material'].lower()or(row['texture']is None):o.hide_render=True
# Supplied PC packs rely on the game's common eye meshes. Add simple eye
# geometry for the independent Blender preview; source facial meshes stay exact.
for side in ['l','r']:
 centers=[]
 for lid in ['t','b']:
  bone='skf_eyelid_'+lid+'_'+side;weighted=Vector();total=0
  for row in d['meshes']:
   if row['material']!='fox_skin_mat':continue
   for pos,weights in zip(row['positions'],row['weights']):
    w=weights.get(bone,0)
    if w>.3:weighted+=Vector(pos)*w;total+=w
  if total:centers.append(weighted/total)
 if len(centers)!=2:continue
 center=sum(centers,Vector())/2;center.y+=.0115
 def ball(name,loc,scale,color):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=scale
  for p in ob.data.polygons:p.use_smooth=True
  mat=bpy.data.materials.new(name);mat.diffuse_color=(*color,1);mat.use_nodes=True;sh=mat.node_tree.nodes.get('Principled BSDF');sh.inputs['Base Color'].default_value=(*color,1);sh.inputs['Roughness'].default_value=.3;ob.data.materials.append(mat)
 ball('Common eye sclera',center,(.011,.011,.010),(.65,.65,.62))
 ball('Common eye iris',center+Vector((0,-.0106,0)),(.0045,.001,.0045),(.13,.18,.23)if label=='ferguson'else(.16,.12,.055))
 ball('Common eye pupil',center+Vector((0,-.0115,0)),(.0022,.0005,.0022),(.003,.003,.003))
bpy.context.view_layer.update()
meshobs=[o for o in bpy.data.objects if o.type=='MESH'and not o.hide_render and not o.name.startswith('suit')];pts=[o.matrix_world@v.co for o in meshobs for v in o.data.vertices];mins=Vector([min(p[i]for p in pts)for i in range(3)]);maxs=Vector([max(p[i]for p in pts)for i in range(3)]);target=(mins+maxs)*.5
# FMDL faces face toward -Y in Blender after source-axis conversion.
def aim(obj,p):obj.rotation_euler=(p-obj.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=target+Vector((.045,-.85,.03)));cam=bpy.context.object;aim(cam,target);cam.data.type='ORTHO';cam.data.ortho_scale=max(maxs.z-mins.z,maxs.x-mins.x)*1.18;bpy.context.scene.camera=cam
for loc,power,size in[((-.45,-.6,.5),7,.5),((.4,-.3,.15),4,.45),((0,.3,.45),5,.4)]:
 bpy.ops.object.light_add(type='AREA',location=target+Vector(loc));l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;aim(l,target)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=512;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.2,.2,.2);scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(P/label/'coach-portrait.png')
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
scene['source_archive']=label+'.rar';scene['native_game_render_verified']=False
bpy.ops.wm.save_as_mainfile(filepath=str(P/label/(label+'_SOURCE_REVIEW.blend')),compress=True);bpy.ops.render.render(write_still=True);print('BLENDER_COACH_READY',label,mins,maxs)
