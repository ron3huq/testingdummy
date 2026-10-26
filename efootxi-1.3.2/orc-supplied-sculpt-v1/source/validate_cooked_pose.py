import bpy,math,json,numpy as np
from pathlib import Path
R=Path(__file__).parent;f=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-orc-v1/export-final/Game/Assets/character/RealFace/SK_ND01_Face.gltf');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(f));arm=next(o for o in bpy.data.objects if o.type=='ARMATURE');mesh=next(o for o in bpy.data.objects if o.type=='MESH');mesh.data.calc_loop_triangles();tris=np.array([t.vertices[:]for t in mesh.data.loop_triangles])
def pos():
 bpy.context.view_layer.update();ev=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([list(mesh.matrix_world@v.co)for v in m.vertices]);ev.to_mesh_clear();return p
base=pos();n=np.cross(base[tris[:,1]]-base[tris[:,0]],base[tris[:,2]]-base[tris[:,0]]);area=np.linalg.norm(n,axis=1);good=area>1e-10;stats=[]
for axis,angle in [(0,20),(1,-20),(2,-30),(2,30)]:
 for pb in arm.pose.bones:pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,0)
 arm.pose.bones['sk_head'].rotation_euler[axis]=math.radians(angle);p=pos();nn=np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]]);flips=np.flatnonzero((np.sum(nn*n,axis=1)<0)&good);centers=base[tris[flips]].mean(axis=1)if len(flips)else np.empty((0,3));stats.append({'axis':axis,'angle':angle,'reversed_triangles':len(flips),'bounds':[centers.min(axis=0).tolist(),centers.max(axis=0).tolist()]if len(flips)else None});print(stats[-1],flush=True)
report={'phone_tested':False,'source':'independent cooked readback including quantized 8-bit bone weights','poses':stats};(R/'cooked-pose-validation.json').write_text(json.dumps(report,indent=2));assert all(row['reversed_triangles']==0 for row in stats),stats;print('COOKED_8BIT_WEIGHT_POSES_PASS',flush=True)
