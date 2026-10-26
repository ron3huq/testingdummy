import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).parent;r=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-spiderman-v3')
bpy.ops.wm.open_mainfile(filepath=str(R/'SpiderMan_v3_HUMAN_NECK.blend'))
for o in list(bpy.data.objects):
 if o.type in ['MESH','CURVE']:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(r/'export/Game/Assets/character/RealFace/SK_ND01ep00v0313_Face.gltf'))
m=bpy.data.materials.new('ACTUAL_ANDROID_ATLAS_PREVIEW');m.use_nodes=True;n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.55;im=bpy.data.images.load(str(r/'atlas-ETC2-decoded.png'));im.pack();im.alpha_mode='NONE';t=n.new('ShaderNodeTexImage');t.image=im;m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
for o in bpy.data.objects:
 if o.type=='MESH':
  o.data.materials.clear();o.data.materials.append(m)
  for f in o.data.polygons:f.material_index=0
cam=bpy.context.scene.camera;cam.location=(.8*math.sin(math.radians(40)),-.06-.8*math.cos(math.radians(40)),1.72);cam.rotation_euler=(Vector((0,-.06,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();s=bpy.context.scene;s.cycles.samples=16;s.render.filepath=str(R/'cooked_asset_preview.png');bpy.ops.render.render(write_still=True)
