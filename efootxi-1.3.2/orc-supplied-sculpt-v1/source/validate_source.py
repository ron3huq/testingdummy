import bpy,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent
bpy.ops.wm.open_mainfile(filepath=str(R/'ORC_FULL_SCULPT.blend'));high=bpy.data.objects['ORC_SUPPLIED_FULL_SCULPT'];low=bpy.data.objects['ORC_GAME_LOD']
# Source full sculpt matches the original imported vertices plus only the recorded shift.
with bpy.data.libraries.load(str(R/'ORC_SOURCE_FULL.blend'),link=False) as(a,b):b.objects=['ORC_SUPPLIED_SCULPT']
original=b.objects[0];bpy.context.scene.collection.objects.link(original);original.name='VALIDATION_ORIGINAL'
a=np.empty(len(high.data.vertices)*3,np.float32);high.data.vertices.foreach_get('co',a);a=a.reshape(-1,3);b=np.empty(len(original.data.vertices)*3,np.float32);original.data.vertices.foreach_get('co',b);b=b.reshape(-1,3);shift=np.array([-.0047,.0253,.1072]);err=float(np.abs(a-b-shift).max());assert err<2e-7,err;assert len(high.data.polygons)==len(original.data.polygons)==3682944
# Original polygon vertex indices are unchanged, including existing eye and tusk components.
la=np.empty(len(high.data.loops),np.int32);lb=np.empty(len(original.data.loops),np.int32);high.data.loops.foreach_get('vertex_index',la);original.data.loops.foreach_get('vertex_index',lb);assert np.array_equal(la,lb)
bpy.data.objects.remove(original,do_unlink=True)
# Quantify the necessary mobile reduction against the supplied sculpt's actual surface.
print('BUILD_SOURCE_BVH',flush=True);high.hide_set(False);high.hide_render=False;bpy.context.view_layer.update();fulltree=BVHTree.FromObject(high,bpy.context.evaluated_depsgraph_get());print('SOURCE_BVH_READY',flush=True)
dist=[]
for v in low.data.vertices:
 hit=fulltree.find_nearest(v.co);assert hit is not None;dist.append(hit[3])
lowtree=BVHTree.FromObject(low,bpy.context.evaluated_depsgraph_get());rng=np.random.default_rng(6117);sample=rng.choice(len(a),min(len(a),50000),replace=False);back=[lowtree.find_nearest(Vector(a[i]))[3]for i in sample]
report={'phone_tested':False,'full_sculpt_vertices':len(a),'full_sculpt_faces':len(high.data.polygons),'full_sculpt_geometry_unchanged_except_uniform_scale_translation':True,'full_sculpt_vertex_max_error_m':err,'full_sculpt_original_loop_indices_exact':True,'game_to_source_distance_m':{'max':float(np.max(dist)),'p99':float(np.quantile(dist,.99)),'median':float(np.median(dist))},'source_to_game_sample_distance_m':{'samples':len(back),'max':float(np.max(back)),'p99':float(np.quantile(back,.99)),'median':float(np.median(back))},'source_colour_texture_provided':False,'new_eye_or_tusk_geometry_added':False}
(R/'source-shape-validation.json').write_text(json.dumps(report,indent=2));print('SOURCE_GEOMETRY_AND_LOD_CHECKED',report,flush=True)
# Camera and lights from the finished game preview; high sculpt opens visible in the camera.
for o in list(bpy.data.objects):
 if o!=high:bpy.data.objects.remove(o,do_unlink=True)
with bpy.data.libraries.load(str(R/'ORC_GAME_RIGGED.blend'),link=False) as(src,dst):dst.objects=[n for n in src.objects if n in ['Key','Fill','Rim','Orc preview camera']]
for obj in dst.objects:
 if obj:bpy.context.scene.collection.objects.link(obj)
s=bpy.context.scene;s.camera=bpy.data.objects.get('Orc preview camera');s.world=bpy.data.worlds.new('Source studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.04,.04,.04,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3;s.render.engine='CYCLES';s.cycles.use_denoising=False;s.cycles.samples=16;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100
# Remove unconnected bake target nodes to avoid carrying unrelated intermediate images.
for mat in high.data.materials:
 for n in list(mat.node_tree.nodes):
  if n.type=='TEX_IMAGE':mat.node_tree.nodes.remove(n)
bpy.ops.outliner.orphans_purge(do_recursive=True)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_extras=False;area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.context.view_layer.objects.active=high;high.select_set(True);bpy.ops.wm.save_as_mainfile(filepath=str(R/'ORC_FULL_SCULPT.blend'),compress=True)
s.render.filepath=str(R/'orc_original_comparison.png');bpy.ops.render.render(write_still=True)
print('FULL_SOURCE_SAVED',flush=True)
