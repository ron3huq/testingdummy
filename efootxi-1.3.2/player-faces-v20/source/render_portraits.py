"""Blender studio inspection only; not an Android shader/renderer test."""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/ronaldo-work/v20-export/Game/Assets/character/RealFace');O=Path('/workspace/ronaldo-work/v20-studio');O.mkdir(exist_ok=True)
for profile,hair in [('NW01','ND0001'),('NW27','ND0027'),('NWJR','ND00JR'),('NWHD','ND00HD'),('NWOZ','NW00OZ'),('NDTL','ND00TL')]:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/('SK_'+profile+'ep00v0313_Face.gltf')))
 for o in bpy.context.scene.objects:
  if o.type=='MESH':
   for i,slot in enumerate(o.material_slots):
    mat=slot.material;mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');tex=nt.nodes.new('ShaderNodeTexImage');name='T_'+profile+'ep00v0313_Face_D.png' if i==0 else 'T_'+hair+'_Hair_D.png';tex.image=bpy.data.images.load(str(R/name));nt.links.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.68
    if i==1:nt.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);mat.blend_method='HASHED';mat.use_nodes=True
    nt.links.new(bs.outputs[0],out.inputs[0]);mat.use_backface_culling=False
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.resolution_x=768;scene.render.resolution_y=768;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 world=bpy.data.worlds.new('Studio');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.68,.74,1);world.node_tree.nodes['Background'].inputs[1].default_value=.7
 target=Vector((0,-.1,1.69))
 def light(name,loc,power,size):
  d=bpy.data.lights.new(name,'AREA');d.energy=power;d.size=size;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 light('key',(.7,-1.1,2.1),35,1.0);light('fill',(-.5,-.8,1.8),15,1.0);light('rim',(.3,.5,1.9),25,.5)
 d=bpy.data.cameras.new('Camera');c=bpy.data.objects.new('Camera',d);scene.collection.objects.link(c);c.location=(.025,-1.2,1.72);c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=.36;scene.camera=c;scene.render.filepath=str(O/(profile+'.png'));bpy.ops.render.render(write_still=True)
