import bpy,numpy as np,ast,math,json
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/ronaldo-work');P=R/'v25';P.mkdir(exist_ok=True)
# Record source 2006 vertex order/UV, then export only the accepted 2017 V3.
bpy.ops.wm.open_mainfile(filepath=str(R/'input-0/Ronaldo_2006_EDIT.blend'))
(P/'base_skin.png').write_bytes(bytes(bpy.data.images['face_bsm_alp.png'].packed_file.data))
names=['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat','hair_high_0_fox_skin_mat'];old={n:np.array([tuple(v.co)for v in bpy.data.objects[n].data.vertices])for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'hair-repair-v3/2017/Ronaldo_2017_REPAIR_V3.blend'))
tree=ast.parse((R/'hair-repair-v3/build.py').read_text());scope={'Vector':Vector,'math':math,'YEAR':'2017'}
for name in ['smooth','shape_face']:
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name);exec(compile(ast.Module(body=[node],type_ignores=[]),'<sculpt>','exec'),scope)
skinpos=[];delta=[];skinuv=[];skintri=[];jac=[];D=np.diag([1.,-1.,1.]);offset=0;objects=[]
for i,n in enumerate(names):
 ob=bpy.data.objects[n if i<2 else 'SCALP_NATIVE_2006_BAKED_DONOR_COLOR'];objects.append(ob);m=ob.data;co=np.array([tuple(v.co)for v in m.vertices]);skinpos.extend(co@D*100);delta.extend((co-old[n])@D*100)
 uvby={}
 for loop in m.loops:
  u,v=m.uv_layers[0].data[loop.index].uv;uvby[loop.vertex_index]=(u,1-v)
 skinuv.extend(uvby[j]for j in range(len(co)));skintri.extend([[offset+j for j in p.vertices]for p in m.polygons]);offset+=len(co)
 for p in old[n]:
  J=np.eye(3)
  if i<2:
   eps=1e-5;cols=[]
   for axis in range(3):
    a=Vector(p);b=Vector(p);a[axis]+=eps;b[axis]-=eps;cols.append(tuple((scope['shape_face'](a)-scope['shape_face'](b))/(2*eps)))
   J=np.array(cols).T
  jac.append(D@J@D)
hair=bpy.data.objects['2017_AUTHORED_HAIR_0'];m=hair.data
bpy.ops.object.select_all(action='DESELECT');hair.select_set(True);bpy.context.view_layer.objects.active=hair
atlas=m.uv_layers.new(name='MobileUniqueAtlas');m.uv_layers.active_index=len(m.uv_layers)-1
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.003,area_weight=0,correct_aspect=True,scale_to_bounds=False);bpy.ops.object.mode_set(mode='OBJECT')
m=hair.data;atlas=m.uv_layers['MobileUniqueAtlas'];m.calc_loop_triangles();hp=[];hu=[];sourceuv0=[];sourceuv1=[];hn=[];ht=[];keys={}
for tri in m.loop_triangles:
 row=[]
 for li in tri.loops:
  vi=m.loops[li].vertex_index;u,v=atlas.data[li].uv;n=m.corner_normals[li].vector;key=(vi,round(u,8),round(v,8),*tuple(round(q,6)for q in n))
  if key not in keys:
   keys[key]=len(hp);hp.append(tuple(m.vertices[vi].co@__import__('mathutils').Matrix(D.tolist())*100));hu.append((u,1-v));a,b=m.uv_layers['UV0'].data[li].uv;sourceuv0.append((a,1-b));a,b=m.uv_layers['UV1'].data[li].uv;sourceuv1.append((a,1-b));hn.append(tuple(n@__import__('mathutils').Matrix(D.tolist())))
  row.append(keys[key])
 ht.append(row)
assert np.isfinite(np.array(hu)).all() and np.min(hu)>=-.0001 and np.max(hu)<=1.0001
np.savez_compressed(P/'export.npz',skinpos=skinpos,skin_delta=delta,skin_uv=skinuv,skin_tri=skintri,skin_jac=jac,hairpos=hp,hairuv=hu,hair_source_uv0=sourceuv0,hair_source_uv1=sourceuv1,hairnormal=hn,hairtri=ht)
(P/'export.json').write_text(json.dumps({'skin_vertices':offset,'hair_vertices':len(hp),'hair_triangles':len(ht),'source':'Ronaldo_2017_REPAIR_V3.blend','unique_hair_uv':True},indent=2));print('V25_BLENDER_EXPORT_PASS',offset,len(hp),len(ht))
