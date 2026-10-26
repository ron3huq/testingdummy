import bpy,numpy as np,math,json
from pathlib import Path
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'ORC_GAME_RIGGED.blend'));o=bpy.data.objects['ORC_GAME_LOD'];arm=bpy.data.objects['ORC_NATIVE_166_BONE_RIG'];arm.animation_data_clear();base=np.array([v.co[:]for v in o.data.vertices]);edges=np.array([e.vertices[:]for e in o.data.edges]);length=np.linalg.norm(base[edges[:,0]]-base[edges[:,1]],axis=1);valid=length>1e-4;o.data.calc_loop_triangles();tris=np.array([t.vertices[:]for t in o.data.loop_triangles]);rn=np.cross(base[tris[:,1]]-base[tris[:,0]],base[tris[:,2]]-base[tris[:,0]]);areas=np.linalg.norm(rn,axis=1);good=areas>1e-10
names=['sk_head','sk_cervicalspine_02','sk_spine_03']
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def weights(x,y,z,mode):
 start=.43+1 if mode==1 else 1.405 if mode==2 else 1.38 if mode==3 else 1.405
 h=smooth((z-start)/(1.605-start));c=smooth((z-1.445)/.10);chest=(1-h)*(1-c)
 if mode==4:
  factor=smooth((abs(x+.0047)-.08)/.13)*smooth((1.60-z)/.15);chest+=(1-chest)*factor;h*=1-factor
 return [h,1-h-chest,chest]
reports=[];chosen=None
for mode in [1,2,3,4]:
 for g in list(o.vertex_groups):o.vertex_groups.remove(g)
 for name in names:o.vertex_groups.new(name=name)
 for v in o.data.vertices:
  for name,w in zip(names,weights(*v.co,mode)):
   if w>1e-8:o.vertex_groups[name].add([v.index],w,'REPLACE')
 stats=[];ok=True
 for axis,angle in [(0,20),(1,-20),(2,-30),(2,30)]:
  for pb in arm.pose.bones:pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,0)
  arm.pose.bones['sk_head'].rotation_euler[axis]=math.radians(angle);bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([list(o.matrix_world@v.co)for v in m.vertices]);ev.to_mesh_clear();rat=np.linalg.norm(p[edges[valid,0]]-p[edges[valid,1]],axis=1)/length[valid];pn=np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]]);dots=np.sum(pn*rn,axis=1);flipped=np.flatnonzero((dots<0)&good);centers=base[tris[flipped]].mean(axis=1)if len(flipped)else np.empty((0,3));row={'axis':axis,'degrees':angle,'min':float(rat.min()),'max':float(rat.max()),'folds':len(flipped),'fold_bounds':[centers.min(axis=0).tolist(),centers.max(axis=0).tolist()]if len(flipped)else None};stats.append(row)
  if len(flipped)>0 or rat.min()<.25 or rat.max()>2.5:ok=False
 print('MODE',mode,stats,flush=True);reports.append({'mode':mode,'stats':stats,'pass':ok})
 if ok:chosen=mode;break
(R/'weight-tuning.json').write_text(json.dumps(reports,indent=2))
assert chosen is not None,reports
for pb in arm.pose.bones:pb.rotation_euler=(0,0,0)
bpy.context.scene.frame_set(1)
# Keep game geometry identical; replace only the three native influence weights.
g=json.loads((R/'native_geometry.json').read_text())
for row in g['vertices']:
 vals=weights(*row['p'],chosen);total=sum(w for w in vals if w>1e-8);row['weights']={n:w/total for n,w in zip(names,vals)if w>1e-8}
(R/'native_geometry.json').write_text(json.dumps(g));bpy.ops.wm.save_as_mainfile(filepath=str(R/'ORC_GAME_RIGGED.blend'),compress=True);print('CHOSEN_WEIGHT_MODE',chosen,flush=True)
