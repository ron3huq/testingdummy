import bpy,json
from pathlib import Path
P=Path('/workspace/ronaldo-work/hair-2006-fringe')
bpy.ops.wm.open_mainfile(filepath='/workspace/ronaldo-work/input-0/Ronaldo_2006_EDIT.blend')
def snapshot(o):return {'co':[tuple(v.co) for v in o.data.vertices],'faces':[tuple(p.vertices) for p in o.data.polygons],'uv':[[tuple(x.uv) for x in u.data] for u in o.data.uv_layers],'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices]}
before={o.name:snapshot(o) for o in bpy.data.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(P/'Ronaldo_2006_FRINGE_MULLET.blend'))
for name,data in before.items():
 after=snapshot(bpy.data.objects[name]);assert after['faces']==data['faces'];assert after['uv']==data['uv'];assert after['weights']==data['weights']
 if name!='hair_high_1_fox_hair_mat':assert after['co']==data['co'],name
 else:
  for a,b in zip(data['co'],after['co']):
   if a[1]>-.065 or a[2]<1.75:assert a==b
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
assert len([o for o in bpy.data.objects if o.name.startswith('EDIT_Front_lock_')])==5
print('BLENDER_REOPEN_FACE_UV_WEIGHTS_AND_MULLET_UNCHANGED_PASS')
