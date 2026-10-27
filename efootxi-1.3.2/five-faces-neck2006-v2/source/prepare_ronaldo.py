import bpy,sys,json
from pathlib import Path
R=Path(__file__).parent;sys.path.insert(0,str(R));from common import scene_setup,material
out=R/'ronaldo';bpy.ops.wm.open_mainfile(filepath='/workspace/analysis/ronaldo-2006-viewer/converted/Ronaldo_2006_EDIT.blend');tex=R/'source/ronaldo2009/png'
skin=material('Ronaldo 2009 supplied diffuse on 2006 geometry',(.5,.3,.2));n=skin.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(tex/'face_bsm_alp.png'));t.image.alpha_mode='NONE';t.image.pack();uv=n.new('ShaderNodeUVMap');uv.uv_map='UV0';skin.node_tree.links.new(uv.outputs[0],t.inputs[0]);skin.node_tree.links.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
hair=material('Ronaldo 2009 supplied hair diffuse on 2006 hair',(.02,.01,.008),.65);n=hair.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(tex/'hair_parts_bsm_alp.png'));t.image.pack();uv=n.new('ShaderNodeUVMap');uv.uv_map='UV0';hair.node_tree.links.new(uv.outputs[0],t.inputs[0]);hair.node_tree.links.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);hair.node_tree.links.new(t.outputs['Alpha'],n.get('Principled BSDF').inputs['Alpha']);hair.surface_render_method='DITHERED'
keep=['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat','hair_high_0_fox_skin_mat','hair_high_1_fox_hair_mat']
for o in list(bpy.data.objects):
 if o.name not in keep:bpy.data.objects.remove(o,do_unlink=True);continue
 for m in list(o.modifiers):o.modifiers.remove(m)
 o.data.materials.clear();o.data.materials.append(hair if o.name==keep[-1]else skin);o.hide_set(False);o.hide_render=False
 for p in o.data.polygons:p.material_index=0
scene_setup(.43);bpy.ops.wm.save_as_mainfile(filepath=str(out/'RONALDO_2009_COLOUR_PREP.blend'),compress=True);print('2009_TEXTURES_ON_ORIGINAL_2006_SOURCE_READY')
