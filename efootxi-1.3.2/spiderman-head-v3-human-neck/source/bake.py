import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'SpiderMan_v3_HUMAN_NECK.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type=='CURVE':o.data.bevel_resolution=0
 if o.type in ['MESH','CURVE']:o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.object.convert(target='MESH')
# Explicit original UV lookup survives creation of a second atlas UV set.
for o in bpy.context.selected_objects:
 if o.type!='MESH':continue
 if o.data.uv_layers:o.data.uv_layers.active.name='SourceUV'
 else:o.data.uv_layers.new(name='SourceUV')
for m in bpy.data.materials:
 if m.name.startswith('RONALDO_2006'):
  n=m.node_tree.nodes;uv=n.new('ShaderNodeUVMap');uv.uv_map='SourceUV'
  for t in n:
   if t.type=='TEX_IMAGE':m.node_tree.links.new(uv.outputs['UV'],t.inputs['Vector'])
bpy.ops.object.join();o=bpy.context.object;o.name='ANDROID_EXPORT_MASK_AND_2006_NECK';uv=o.data.uv_layers.new(name='Atlas');o.data.uv_layers.active=uv;uv.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.003);bpy.ops.object.mode_set(mode='OBJECT')
im=bpy.data.images.new('SPIDERMAN_AND_REAL_NECK_ATLAS',2048,2048,alpha=True);im.generated_color=(.1,0,0,1)
for m in o.data.materials:
 n=m.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=im;n.active=t
s=bpy.context.scene;s.cycles.samples=1;s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True;s.render.bake.margin=6
bpy.ops.object.bake(type='DIFFUSE');im.filepath_raw=str(R/'atlas.png');im.file_format='PNG';im.save()
o.data.calc_loop_triangles();vv=[];tt=[];lookup={};names={g.index:g.name for g in o.vertex_groups}
for tri in o.data.loop_triangles:
 face=[]
 for li in tri.loops:
  loop=o.data.loops[li];v=o.data.vertices[loop.vertex_index];uv=o.data.uv_layers['Atlas'].data[li].uv;key=(loop.vertex_index,round(uv.x,7),round(uv.y,7))
  if key not in lookup:
   weights={names[g.group]:g.weight for g in v.groups if g.weight>0};weights=weights or {'sk_head':1.0}
   normal=v.normal;lookup[key]=len(vv);vv.append({'p':list(v.co),'n':list(normal),'uv':list(uv),'weights':weights})
  face.append(lookup[key])
 tt.append(face)
assert len(vv)<65532
(R/'native_geometry.json').write_text(json.dumps({'vertices':vv,'triangles':tt}));print('BAKED_EXPORT',len(vv),len(tt))
