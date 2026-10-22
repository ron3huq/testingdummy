import bpy,math,json
from pathlib import Path
from mathutils import Vector
r=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-hair-v2');bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(r/'full-export/Game/Assets/character/RealFace/SK_ND01ep00v0313_Face.gltf'))
face=bpy.data.materials.new('Neutral clay — geometry inspection only');face.use_nodes=True;bs=face.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.30,.22,.16,1);bs.inputs['Roughness'].default_value=.65
hair=bpy.data.materials.new('Decoded Android ETC2 color and alpha');hair.use_nodes=True;nodes=hair.node_tree.nodes;links=hair.node_tree.links;bs=nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.46;bs.inputs['Specular IOR Level'].default_value=.25;tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(r/'atlas-ETC2-decoded.png'));uv=nodes.new('ShaderNodeUVMap');links.new(uv.outputs['UV'],tex.inputs['Vector']);links.new(tex.outputs['Color'],bs.inputs['Base Color']);links.new(tex.outputs['Alpha'],bs.inputs['Alpha']);hair.surface_render_method='DITHERED'
for ob in bpy.context.scene.objects:
 if ob.type=='MESH':
  slots=[p.material_index for p in ob.data.polygons];ob.data.materials.clear();ob.data.materials.append(face);ob.data.materials.append(hair)
  for poly,slot in zip(ob.data.polygons,slots):poly.material_index=slot
  for poly in ob.data.polygons:poly.use_smooth=True
  uv.uv_map=ob.data.uv_layers[0].name
bpy.ops.object.camera_add(location=(.32,-.64,1.84));camera=bpy.context.object;camera.rotation_euler=(Vector((0,-.03,1.735))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=.32;bpy.context.scene.camera=camera
for pos,power,size in [((.5,-.5,2.1),90,.55),((-.4,-.3,1.9),40,.5),((.1,.25,2.1),70,.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,1.75))-l.location).to_track_quat('-Z','Y').to_euler()
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.world.color=(.15,.15,.15);s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.view_settings.exposure=-2;s.render.image_settings.file_format='PNG';s.render.filepath=str(r/'offline-geometry-hair-preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(r/'offline-preview.blend'));bpy.ops.render.render(write_still=True)
