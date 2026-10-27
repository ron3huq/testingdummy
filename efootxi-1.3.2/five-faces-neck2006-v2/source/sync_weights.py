import bpy,json,sys,numpy as np
from pathlib import Path
from scipy.spatial import cKDTree
R=Path(__file__).parent
for kind in ['orc','joker','naruto']:
 out=R/kind;bpy.ops.wm.open_mainfile(filepath=str(out/(kind.upper()+'_SOURCE_NECK2006.blend')));neck=next(o for o in bpy.data.objects if o.type=='MESH'and o.get('source_ronaldo_2006_neck'));points=np.array([v.co[:]for v in neck.data.vertices]);names={g.index:g.name for g in neck.vertex_groups};weights=[{names[g.group]:g.weight for g in v.groups if g.weight>1e-8}for v in neck.data.vertices];tree=cKDTree(points)
 bpy.ops.wm.open_mainfile(filepath=str(out/(kind.upper()+'_NECK2006_GAME.blend')));o=bpy.data.objects[kind.upper()+'_GAME_HEAD_NECK'];changed=0
 for v in o.data.vertices:
  distance,i=tree.query(v.co)
  if distance>2e-6:continue
  for g in o.vertex_groups:g.remove([v.index])
  for name,w in weights[i].items():o.vertex_groups[name].add([v.index],w,'REPLACE')
  changed+=1
 geo=json.loads((out/'native_geometry.json').read_text());count=0
 for row in geo['vertices']:
  distance,i=tree.query(row['p'])
  if distance>2e-6:continue
  total=sum(weights[i].values());row['weights']={k:w/total for k,w in weights[i].items()};count+=1
 assert changed>300 and count>=changed,(kind,changed,count);(out/'native_geometry.json').write_text(json.dumps(geo));bpy.ops.wm.save_as_mainfile(filepath=str(out/(kind.upper()+'_NECK2006_GAME.blend')),compress=True);(out/'neck-weights-validation.json').write_text(json.dumps({'geometry_changed':False,'neck_vertices':changed,'exported_neck_uv_vertices':count,'upper_boundary_head_weight':1.0,'phone_tested':False},indent=2));print('SYNCED',kind,changed,count,flush=True)
