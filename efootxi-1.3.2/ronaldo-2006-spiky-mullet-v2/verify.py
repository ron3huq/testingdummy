import bpy,json
from pathlib import Path
P=Path('/workspace/ronaldo-work/hair-2006-spikes')
bpy.ops.wm.open_mainfile(filepath='/workspace/ronaldo-work/input-0/Ronaldo_2006_EDIT.blend')
def snap(o):return {'co':[tuple(v.co) for v in o.data.vertices],'faces':[tuple(p.vertices) for p in o.data.polygons],'uv':[[tuple(x.uv) for x in u.data] for u in o.data.uv_layers],'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],'materials':[m.name for m in o.data.materials]}
before={o.name:snap(o) for o in bpy.data.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(P/'Ronaldo_2006_SPIKY_MULLET_V2.blend'))
for name,data in before.items():
 after=snap(bpy.data.objects[name]);assert after['faces']==data['faces'];assert after['uv']==data['uv'];assert after['weights']==data['weights']
 if name!='hair_high_0_fox_skin_mat':assert after['materials']==data['materials']
 if name!='hair_high_1_fox_hair_mat':assert after['co']==data['co'],name
 else:
  for a,b in zip(data['co'],after['co']):
   if a[2]<=1.73 or a[1]>=.005:assert a==b
m=bpy.data.objects['hair_high_0_fox_skin_mat'].data.materials[0]
assert any(l.from_node.type=='TEX_IMAGE' and l.from_node.image.name=='face_bsm_alp.png' and l.to_node.type=='MIX_RGB' and l.to_socket.name=='Color1' for l in m.node_tree.links)
mask=next(n for n in m.node_tree.nodes if n.type=='MAP_RANGE');assert mask.clamp;assert abs(mask.inputs['From Min'].default_value-1.775)<.00001;assert abs(mask.inputs['From Max'].default_value-1.795)<.00001
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
assert len(bpy.data.objects['EDIT_Spiky_top_and_front'].data.vertices)>20000
print('V2_REOPEN_FACE_NAPE_MATERIAL_UV_WEIGHTS_MULLET_PASS')
