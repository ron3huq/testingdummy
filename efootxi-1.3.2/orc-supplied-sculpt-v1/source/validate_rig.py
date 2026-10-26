import bpy,numpy as np,json,math
from pathlib import Path
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'ORC_GAME_RIGGED.blend'));o=bpy.data.objects['ORC_GAME_LOD'];arm=bpy.data.objects['ORC_NATIVE_166_BONE_RIG'];arm.animation_data_clear();s=bpy.context.scene
base=np.array([list(v.co)for v in o.data.vertices]);edges=np.array([list(e.vertices)for e in o.data.edges]);lengths=np.linalg.norm(base[edges[:,0]]-base[edges[:,1]],axis=1);valid=lengths>1e-5;stats=[]
def positions():
 bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();out=np.array([list(o.matrix_world@v.co)for v in mesh.vertices]);ev.to_mesh_clear();assert np.isfinite(out).all();return out
for axis,angle in [('rest',0),('local_x',20),('local_y',-20),('local_z',-30),('local_z',30)]:
 for pb in arm.pose.bones:pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,0)
 if angle:arm.pose.bones['sk_head'].rotation_euler['xyz'.index(axis[-1])]=math.radians(angle)
 p=positions();ratio=np.linalg.norm(p[edges[valid,0]]-p[edges[valid,1]],axis=1)/lengths[valid];row={'pose':axis,'angle':angle,'edge_ratio_min':float(ratio.min()),'edge_ratio_max':float(ratio.max()),'finite':True}
 if not angle:row['rest_pose_error_m']=float(np.abs(p-base).max());assert row['rest_pose_error_m']<1e-5,row
 assert ratio.min()>.1 and ratio.max()<3,row
 stats.append(row)
# Source posterior neck must be present, not merely an opaque viewport flag.
for pb in arm.pose.bones:pb.rotation_euler=(0,0,0)
bpy.context.view_layer.update();from mathutils import Vector
from mathutils.bvhtree import BVHTree
tree=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get());rays=[]
for z in [1.55,1.58,1.61]:
 hit=tree.ray_cast(Vector((-.0047,.5,z)),Vector((0,-1,0)),1.)
 assert hit[0] is not None,(z,hit);rays.append({'z':z,'posterior_hit_y':hit[0].y})
report={'phone_tested':False,'native_armature_bones':len(arm.data.bones),'poses':stats,'posterior_neck_rays':rays,'fixed_original_face_expression':True};assert len(arm.data.bones)==166;(R/'rig-validation.json').write_text(json.dumps(report,indent=2));print('REST_HEAD_NECK_POSES_AND_POSTERIOR_NECK_PASS',flush=True)
