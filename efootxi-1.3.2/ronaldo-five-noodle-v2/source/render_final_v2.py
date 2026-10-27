import bpy,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).parent;V=R/'v2';P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/'android-r5-v2-combined';sys.path.insert(0,'/workspace/analysis/five-faces-2026');from common import material,render_views,scene_setup
import common
original_scene_setup=common.scene_setup
def final_scene_setup(*a,**kw):
 s=original_scene_setup(*a,**kw);s.render.resolution_percentage=75;s.cycles.samples=12;return s
common.scene_setup=final_scene_setup
scene_setup=final_scene_setup
report={}
for card,row in json.loads((V/'targets.json').read_text()).items():
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(N/'export-final/Game/Assets/character/RealFace'/('SK_'+row['prefix']+'_Face.gltf')));arm=next(o for o in bpy.data.objects if o.type=='ARMATURE');o=max((o for o in bpy.data.objects if o.type=='MESH'),key=lambda o:len(o.data.vertices));out=V/card/'previews';out.mkdir(exist_ok=True);C=P/('android-r5-v2-'+card)
 for i,part in enumerate(['face','hair']):
  mat=material(part,(.4,.3,.2));n=mat.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(C/('pc-face-ETC2-decoded.png'if part=='face'else'atlas-ETC2-decoded.png')));t.image.pack();mat.node_tree.links.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
  if part=='face':
   normal=n.new('ShaderNodeTexImage');normal.image=bpy.data.images.load(str(V/card/'face-N-ETC2-decoded.png'));normal.image.colorspace_settings.name='Non-Color';normal.image.pack();separate=n.new('ShaderNodeSeparateColor');combine=n.new('ShaderNodeCombineColor');flip=n.new('ShaderNodeMath');flip.operation='SUBTRACT';flip.inputs[0].default_value=1;mat.node_tree.links.new(normal.outputs['Color'],separate.inputs[0]);mat.node_tree.links.new(separate.outputs['Red'],combine.inputs['Red']);mat.node_tree.links.new(separate.outputs['Green'],flip.inputs[1]);mat.node_tree.links.new(flip.outputs[0],combine.inputs['Green']);mat.node_tree.links.new(separate.outputs['Blue'],combine.inputs['Blue']);nm=n.new('ShaderNodeNormalMap');mat.node_tree.links.new(combine.outputs[0],nm.inputs['Color']);mat.node_tree.links.new(nm.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
   sro=n.new('ShaderNodeTexImage');sro.image=bpy.data.images.load(str(V/card/'face-SRO-ETC2-decoded.png'));sro.image.colorspace_settings.name='Non-Color';sro.image.pack();split=n.new('ShaderNodeSeparateColor');mat.node_tree.links.new(sro.outputs['Color'],split.inputs[0]);mat.node_tree.links.new(split.outputs['Green'],n.get('Principled BSDF').inputs['Roughness']);mat.node_tree.links.new(split.outputs['Red'],n.get('Principled BSDF').inputs['Specular IOR Level'])
  if part=='hair':mat.node_tree.links.new(t.outputs['Alpha'],n.get('Principled BSDF').inputs['Alpha']);mat.surface_render_method='DITHERED'
  o.data.materials[i]=mat
 render_views(out,.43);bpy.ops.wm.save_as_mainfile(filepath=str(out/(card+'_V2_GAME_RIG.blend')),compress=True)
 # Record actual cooked controls, keeping the imported bind pose intact.
 initial={b.name:b.matrix_basis.copy()for b in arm.pose.bones}
 def reset():
  for b in arm.pose.bones:b.matrix_basis=initial[b.name]
  bpy.context.view_layer.update()
 def points():
  bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();p=np.array([tuple(o.matrix_world@v.co)for v in me.vertices]);ev.to_mesh_clear();return p
 base=points();stats={}
 for name in ['skf_eye_l','skf_eye_r','skf_jaw','skf_eyelid_t_l','skf_eyelid_t_r','skf_eyelid_b_l','skf_eyelid_b_r']:
  reset();b=arm.pose.bones[name];b.matrix_basis=initial[name]@Matrix.Rotation(math.radians(8 if name=='skf_jaw'else 5),4,'X');pp=points();delta=np.linalg.norm(pp-base,axis=1);assert np.isfinite(pp).all()and delta.max()>1e-7,(card,name);stats[name]={'moved_vertices':int((delta>1e-7).sum()),'max_move_m':float(delta.max())}
 reset();s=scene_setup(.43);s.cycles.samples=12;target=Vector((0,-.065,1.66));s.camera.location=(.8*math.sin(math.radians(20)),-.065-.8*math.cos(math.radians(20)),1.73);s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler()
 b=arm.pose.bones['skf_jaw'];b.matrix_basis=initial[b.name]@Matrix.Rotation(math.radians(8),4,'X');s.render.filepath=str(out/'jaw-test.png');bpy.ops.render.render(write_still=True);reset()
 for name in ['skf_eye_l','skf_eye_r']:
  b=arm.pose.bones[name];w=arm.matrix_world@b.matrix;pivot=w.translation.copy();b.matrix=arm.matrix_world.inverted()@Matrix.Translation(pivot)@Matrix.Rotation(math.radians(10),4,'Z')@Matrix.Translation(-pivot)@w
 s.render.filepath=str(out/'gaze-test.png');bpy.ops.render.render(write_still=True);reset()
 for name,shift in [('skf_eyelid_t_l',-.004),('skf_eyelid_t_r',-.004),('skf_eyelid_b_l',.002),('skf_eyelid_b_r',.002)]:
  b=arm.pose.bones[name];m=arm.matrix_world@b.matrix;m.translation+=Vector((0,0,shift));b.matrix=arm.matrix_world.inverted()@m
 s.render.filepath=str(out/'blink-test.png');bpy.ops.render.render(write_still=True);reset()
 b=arm.pose.bones['sk_head'];w=arm.matrix_world@b.matrix;pivot=w.translation.copy();b.matrix=arm.matrix_world.inverted()@Matrix.Translation(pivot)@Matrix.Rotation(math.radians(25),4,'Z')@Matrix.Translation(-pivot)@w;s.render.filepath=str(out/'headturn-test.png');bpy.ops.render.render(write_still=True);reset();report[card]=stats;(V/'controls-validation.json').write_text(json.dumps({'phone_tested':False,'synthetic_poses':True,'cards':report},indent=2));print('FINAL_V2_COOKED_PREVIEW_AND_CONTROLS_COMPLETE',card,flush=True)
