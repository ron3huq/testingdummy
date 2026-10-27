import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-five-combined');targets=json.loads((R/'targets.json').read_text());report={'phone_tested':False,'source':'independent cooked meshes and 8-bit weights','heads':{}}
for kind,info in targets.items():
 bpy.ops.wm.read_factory_settings(use_empty=True);f=P/'export-final/Game/Assets/character/RealFace'/('SK_'+info['prefix']+'_Face.gltf');bpy.ops.import_scene.gltf(filepath=str(f));arm=next(o for o in bpy.data.objects if o.type=='ARMATURE');o=max((o for o in bpy.data.objects if o.type=='MESH'),key=lambda x:len(x.data.vertices));o.data.calc_loop_triangles();tri=np.array([t.vertices[:]for t in o.data.loop_triangles]);stats=[]
 def pos():
  bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([list(o.matrix_world@v.co)for v in m.vertices]);ev.to_mesh_clear();return p
 initial={b.name:b.matrix_basis.copy()for b in arm.pose.bones};base=pos();n=np.cross(base[tri[:,1]]-base[tri[:,0]],base[tri[:,2]]-base[tri[:,0]]);area=np.linalg.norm(n,axis=1);good=area>1e-9
 for axis,deg in [(0,20),(1,-20),(2,-30),(2,30)]:
  for b in arm.pose.bones:b.matrix_basis=initial[b.name]
  arm.pose.bones['sk_head'].matrix_basis=initial['sk_head']@Matrix.Rotation(math.radians(deg),4,'XYZ'[axis]);p=pos();assert np.isfinite(p).all();nn=np.cross(p[tri[:,1]]-p[tri[:,0]],p[tri[:,2]]-p[tri[:,0]]);bad=np.flatnonzero((np.sum(nn*n,axis=1)<0)&good);stats.append({'head_local_axis':axis,'degrees':deg,'finite':True,'reversed_triangles':len(bad),'reversed_total_rest_area_m2':float(area[bad].sum()/2)})
  # Original photo hair cards can be close to degenerate. New neck area must not fold.
  centers=base[tri[bad]].mean(axis=1)if len(bad)else np.empty((0,3));visible_neck=((centers[:,2]>=1.52)&(centers[:,2]<1.60))if len(bad)else np.array([],bool)
  stats[-1]['visible_neck_reversed_triangles']=int(visible_neck.sum())
  if visible_neck.any():
   neckarea=area[bad[visible_neck]].sum()/2;stats[-1]['visible_neck_reversed_area_m2']=float(neckarea);assert neckarea<2e-6,(kind,axis,deg,len(bad),neckarea)
 for b in arm.pose.bones:b.matrix_basis=initial[b.name]
 bpy.context.view_layer.update();rest=pos();tree=BVHTree.FromPolygons([Vector(p)for p in rest],tri.tolist());rays=[]
 for z in [1.46,1.50,1.54,1.58]:
  hit=tree.ray_cast(Vector((0,.5,z)),Vector((0,-1,0)),1.);assert hit[0] is not None,(kind,z);rays.append({'z':z,'posterior_y':hit[0].y})
 report['heads'][kind]={'native_bones':len(arm.data.bones),'poses':stats,'posterior_neck_rays':rays,'jaw_bone_available':'skf_jaw'in arm.data.bones}
 print('POSED',kind,stats,flush=True)
(P/'pose-validation.json').write_text(json.dumps(report,indent=2));print('FIVE_COOKED_HEAD_POSES_AND_POSTERIOR_NECK_CHECK_COMPLETE',flush=True)
