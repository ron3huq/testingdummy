import bpy,json
from pathlib import Path
P=Path('/workspace/ronaldo-work/73-ui4');source=next((P/'ronaldo-native').rglob('SK_4522ep00v0313_Face.gltf'));rows=json.loads((P/'ronaldo-blender-source.json').read_text());out=P/'blender-output';out.mkdir(exist_ok=True)
for cid,row in rows.items():
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
 scene=bpy.context.scene;scene['card_id']=cid;scene['source_model']=row['source_model'];scene['appearance_payload_sha256']=row['appearance_payload_sha256'];scene['inspection_note']='Native Epic Ronaldo source; both supplied card appearance payloads are identical. Original UV, rig, weights and textures imported; no face sculpt.'
 for mat in bpy.data.materials:
  if not mat.use_nodes or '4522' not in mat.name:continue
  hair='Hair'in mat.name;texture=source.parent/('T_4522ep00v0313_Hair_D.tga'if hair else'T_4522ep00v0313_Face_D.tga')
  node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(texture),check_existing=True);shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Metallic'].default_value=0;shader.inputs['Roughness'].default_value=.6;mat.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
  if hair:mat.node_tree.links.new(node.outputs['Alpha'],shader.inputs['Alpha']);mat.surface_render_method='DITHERED'
 for image in bpy.data.images:
  if image.source=='FILE':image.pack()
 bpy.ops.wm.save_as_mainfile(filepath=str(out/('Ronaldo_'+cid+'_NATIVE.blend')),compress=True)
 print('RONALDO_BLEND_SAVED',cid,len([o for o in scene.objects if o.type=='MESH']),len([o for o in scene.objects if o.type=='ARMATURE']))
