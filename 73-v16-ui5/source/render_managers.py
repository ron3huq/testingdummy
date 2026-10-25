import bpy,json,math
from pathlib import Path
from mathutils import Vector
P=Path('/workspace/ronaldo-work/73-ui5');bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for variant,x in [('1sp00v0052',-.16),('26sp00v0047',.16)]:
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(P/'new-export/Game/Assets/character/DemoFace/Manager'/('SK_'+variant+'_Face.gltf')))
 objects=set(bpy.data.objects)-before
 for obj in objects:
  if obj.parent is None:obj.location.x+=x
  if obj.type=='MESH':
   for i,slot in enumerate(obj.material_slots):
    m=bpy.data.materials.new('review-'+variant+str(i));m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');shader=n.new('ShaderNodeBsdfPrincipled');shader.inputs['Roughness'].default_value=.72;m.node_tree.links.new(shader.outputs['BSDF'],out.inputs['Surface'])
    label='Hair' if variant=='26sp00v0047'and i==1 else 'Face';f=P/(variant+'-'+label+'.png')
    if f.exists():
     t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(f));m.node_tree.links.new(t.outputs['Color'],shader.inputs['Base Color'])
     if label=='Hair':m.node_tree.links.new(t.outputs['Alpha'],shader.inputs['Alpha']);m.surface_render_method='DITHERED'
    else:shader.inputs['Base Color'].default_value=(.12,.07,.05,1)
    slot.material=m
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.world.color=(.20,.20,.20)
bpy.ops.object.camera_add(location=(0,-1.1,1.71));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,1.65))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=.65;scene.camera=camera
for pos,power,size in [((-.5,-.8,2.2),50,.8),((.6,-.4,1.8),25,.7)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.65))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=1000;scene.render.resolution_y=600;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(P/'native-managers-preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(P/'native-manager-review.blend'));bpy.ops.render.render(write_still=True)
