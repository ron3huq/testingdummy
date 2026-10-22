"""Fit extracted PC curls onto the exported Android reference head. Not cooked for game."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parent;p=r.parent;out=r/'fit';out.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(r/'export/Game/Assets/character/RealFace/SK_4522_Face.gltf'))
rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE');rig.name='ANDROID_EXPORTED_REFERENCE_166_BONES'
original=next(o for o in bpy.context.scene.objects if o.type=='MESH');bpy.ops.object.select_all(action='DESELECT');original.select_set(True);bpy.context.view_layer.objects.active=original
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.separate(type='MATERIAL');bpy.ops.object.mode_set(mode='OBJECT')
parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];oldhair=next(o for o in parts if any(m and m.name.startswith('dummy_material_1') for m in o.data.materials) and len(o.data.vertices)==601);face=next(o for o in parts if o!=oldhair)
face.name='ANDROID_FACE_UNCHANGED';oldhair.name='ANDROID_ORIGINAL_HAIR_REFERENCE_HIDDEN';oldhair.hide_render=True;oldhair.hide_set(True)
faceco=[tuple(v.co) for v in face.data.vertices]
with bpy.data.libraries.load(str(p/'converted/Ronaldo_88044950524330_SOURCE.blend'),link=False) as (data,to):to.objects=[n for n in data.objects if n.startswith('hair_high_0_')]
hair=to.objects[0];bpy.context.scene.collection.objects.link(hair);hair.name='PC_NOODLE_CURLS_ON_ANDROID_sk_head'
world=hair.matrix_world.copy();hair.parent=rig;hair.matrix_world=world
for mod in list(hair.modifiers):hair.modifiers.remove(mod)
mod=hair.modifiers.new('Android head bone reference binding','ARMATURE');mod.object=rig
assert len(hair.vertex_groups)==1 and hair.vertex_groups[0].name=='sk_head'
assert 'sk_head' in rig.data.bones
# Keep source UVs and masks, use a conservative cutout preview rather than FOX shader emulation.
mat=hair.data.materials[0].copy();mat.name='NOODLE_PREVIEW_NOT_PORTED_FOX_SHADER';hair.data.materials[0]=mat
nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF')
for link in list(bsdf.inputs['Base Color'].links):links.remove(link)
bsdf.inputs['Base Color'].default_value=(.025,.018,.012,1);bsdf.inputs['Roughness'].default_value=.8;bsdf.inputs['Specular IOR Level'].default_value=.12
alpha=next(n for n in nodes if n.type=='TEX_IMAGE' and n.image and n.image.name.startswith('hair_alpha8'))
cut=nodes.new('ShaderNodeMath');cut.operation='GREATER_THAN';cut.inputs[1].default_value=.45;links.new(alpha.outputs['Alpha'],cut.inputs[0]);links.new(cut.outputs[0],bsdf.inputs['Alpha'])
face.data.materials.clear();clay=bpy.data.materials.new('ANDROID_FACE_CLAY_MISSING_ORIGINAL_MATERIAL');clay.diffuse_color=(.5,.43,.37,1);clay.use_nodes=True;clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.43,.37,1);clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8;face.data.materials.append(clay)
scene=bpy.context.scene;scene['status']='REFERENCE_FIT_NOT_ANDROID_COOKED';scene['target_card_id']='88044950524330';scene['target_card_variant_verified']=False;scene['native_face_geometry_preserved']=True;scene['source_author']='NEUBE';scene['native_lod_warning']='UEViewer reported LOD 0 has no indices; exported available fallback LOD only.'
# Verify the new hair is genuinely bound to the exported Android head bone.
deps=bpy.context.evaluated_depsgraph_get();rest=[(hair.matrix_world@v.co).copy() for v in hair.evaluated_get(deps).data.vertices]
bone=rig.pose.bones['sk_head'];bone.rotation_mode='XYZ';bone.rotation_euler.y=.08;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();posed=[(hair.matrix_world@v.co).copy() for v in hair.evaluated_get(deps).data.vertices];moved=sum((a-b).length>1e-5 for a,b in zip(rest,posed));assert moved==5005
bone.rotation_euler=(0,0,0);bpy.context.view_layer.update();assert [tuple(v.co) for v in face.data.vertices]==faceco
report={'status':'ANDROID_REFERENCE_FIT_ONLY','target_card_id':'88044950524330','native_card_variant_verified':False,'android_face_vertices':len(face.data.vertices),'android_face_triangles':sum(len(f.vertices)-2 for f in face.data.polygons),'old_hair_hidden':True,'pc_curl_vertices':len(hair.data.vertices),'pc_curl_triangles':sum(len(f.vertices)-2 for f in hair.data.polygons),'native_bones':len(rig.data.bones),'hair_weights':'100% Android sk_head','vertices_following_test_head_rotation':moved,'native_face_vertex_coordinates_unchanged':True,'android_asset_cooked':False,'phone_tested':False,'alignment':'Original world coordinates, same meter scale, no manual corrective offsets. Visual reference only; no animation/collision/closeup approval.'}
(out/'fit-validation.json').write_text(json.dumps(report,indent=2))
# Export only the face, replacement curls and native reference rig. Keep old hair hidden in .blend.
bpy.ops.object.select_all(action='DESELECT')
for o in [face,hair,rig]:o.hide_set(False);o.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(out/'Ronaldo_ANDROID_REFERENCE_NOODLE_NOT_COOKED.fbx'),use_selection=True,add_leaf_bones=False,bake_anim=False,path_mode='COPY',embed_textures=True)
bpy.ops.export_scene.gltf(filepath=str(out/'Ronaldo_ANDROID_REFERENCE_NOODLE_NOT_COOKED.glb'),export_format='GLB',use_selection=True,export_animations=False)
# Proof preview of actual Android face + supplied PC curls, no generated replacement head.
scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=False;scene.world.color=(.12,.12,.12)
scene.render.resolution_x=900;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
center=Vector((0,-.075,1.70))
def aim(o):o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,energy in [('Key',(.4,-.5,2.0),10),('Fill',(-.4,-.2,1.9),5),('Rim',(.1,.3,2),12)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.size=.5;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;aim(o)
data=bpy.data.cameras.new('Reference_Camera');cam=bpy.data.objects.new('Reference_Camera',data);scene.collection.objects.link(cam);cam.location=(.25,-.65,1.78);data.type='ORTHO';data.ortho_scale=.47;aim(cam);scene.camera=cam
for image in bpy.data.images:
 if image.source=='FILE':image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Ronaldo_ANDROID_REFERENCE_NOODLE_NOT_COOKED.blend'))
scene.render.filepath=str(out/'Android-head-PC-hair-reference.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report),flush=True)
