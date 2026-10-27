import bpy,json
from pathlib import Path
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'RONALDO_2009_NATIVE.blend'))
def rows(o):
 uv=o.data.uv_layers[0];first={}
 for l in o.data.loops:first.setdefault(l.vertex_index,l.index)
 names={g.index:g.name for g in o.vertex_groups};out=[]
 for v in o.data.vertices:
  li=first.get(v.index,0);n=o.data.corner_normals[li].vector if o.data.loops else v.normal;out.append({'p':list(o.matrix_world@v.co),'n':list(n),'uv':list(uv.data[li].uv),'weights':{names[g.group]:g.weight for g in v.groups if g.weight>0}})
 o.data.calc_loop_triangles();return out,[list(t.vertices)for t in o.data.loop_triangles]
face=[];tri=[]
for name in ['NATIVE_2009_FACE_SKIN']:
 v,t=rows(bpy.data.objects[name]);off=len(face);face+=v;tri +=[[i+off for i in p]for p in t]
f=json.loads((R/'original-native-fields.json').read_text());locked=set(json.loads((R/'native-wrap-validation.json').read_text())['native_orbital_vertices_kept_exact'])
for i,v in enumerate(face):
 v['uv2']=f['uv1'][i];v['color']=f['color'][i];tx,tz,ny,w=f['tangent'][i];v['tangent']=[tx,-ny,tz,w]
 if i in locked:nx,nz,ny=f['normal'][i];v['n']=[nx,-ny,nz]
hair,ht=rows(bpy.data.objects['RONALDO_2009_ON_2006_HAIR']);g={'face':face,'face_triangles':tri,'hair':hair,'hair_triangles':ht};(R/'game_geometry.json').write_text(json.dumps(g));print('EXPORT',len(face),len(hair))
