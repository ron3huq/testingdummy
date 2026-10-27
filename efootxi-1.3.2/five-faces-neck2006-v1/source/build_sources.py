import bpy,bmesh,sys,json,numpy as np,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).parent;sys.path.insert(0,str(R));from common import *
kind=sys.argv[sys.argv.index('--')+1];out=R/kind;out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
if kind=='hulk':
 bpy.ops.wm.open_mainfile(filepath='/workspace/analysis/hulk-game-v3/GAME_EXPORT_LOD.blend');o=next(o for o in bpy.data.objects if o.type=='MESH');o.name='HULK_HEAD_PRESERVED'
 # Identify and remove only the old full neck component in the joined, already delivered LOD.
 bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();seen=set();components=[]
 for v in bm.verts:
  if v in seen:continue
  stack=[v];seen.add(v);comp=[]
  while stack:
   a=stack.pop();comp.append(a)
   for e in a.link_edges:
    q=e.other_vert(a)
    if q not in seen:seen.add(q);stack.append(q)
  components.append(comp)
 # Source-aware component classification removes every old neck UV island.
 from mathutils.bvhtree import BVHTree
 with bpy.data.libraries.load('/workspace/analysis/hulk-game-v3/HULK_GAME_V3.blend',link=False)as(aa,bb):bb.objects=['face_high_0_fox_skin_mat','HULK_FACE_SCULPT','hair_high_0_fox_skin_mat']
 refs=bb.objects;trees=[BVHTree.FromPolygons([v.co for v in q.data.vertices],[p.vertices for p in q.data.polygons])for q in refs];classes=[]
 for comp in components:
  fs=set(f for v in comp for f in v.link_faces)
  if not fs or any(f.material_index!=0 for f in fs):classes.append(-1);continue
  sample=comp[::max(1,len(comp)//30)];scores=[sum(tree.find_nearest(v.co)[3]for v in sample)/len(sample)for tree in trees];classes.append(int(np.argmin(scores)))
 oldneck=[c for c,cl in zip(components,classes)if cl==0];scalp=[c for c,cl in zip(components,classes)if cl==2 and min(v.co.z for v in c)<1.655];removed=sum(map(len,oldneck));print('CLASSIFIED_OLD_NECK',len(oldneck),removed,'SCALP',len(scalp),flush=True)
 for q in refs:bpy.data.objects.remove(q,do_unlink=True)
 bmesh.ops.delete(bm,geom=[v for c in oldneck for v in c],context='VERTS');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(o.data);bm.free()
 
 for v in o.data.vertices:v.co.z+=.04
 o['native_registration_translation_m']=[0,0,.04]
 cap_clip(o,(0,0,1.707),(0,-.8,1),skin_only=True)
 # The exact previously delivered head atlas remains the head's source material.
 image=bpy.data.images.load('/workspace/analysis/hulk-game-v3/atlas.png',check_existing=True);image.pack();mat=material('Hulk preserved delivered head atlas',(.1,.2,.06));n=mat.node_tree.nodes;tex=n.new('ShaderNodeTexImage');tex.image=image;uv=n.new('ShaderNodeUVMap');uv.uv_map='Atlas';mat.node_tree.links.new(uv.outputs[0],tex.inputs['Vector']);mat.node_tree.links.new(tex.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);o.data.materials.clear();o.data.materials.append(mat)
 for p in o.data.polygons:p.material_index=0
 o['source_uv_name']='Atlas';o['old_neck_vertices_removed']=removed;assign_weights(o);append_neck('hulk')
elif kind=='orc':
 bpy.ops.wm.open_mainfile(filepath='/workspace/analysis/orc-source/ORC_GAME_RIGGED.blend');o=bpy.data.objects['ORC_GAME_LOD'];o.name='ORC_HEAD_SOURCE'
 for ob in list(bpy.data.objects):
  if ob!=o:bpy.data.objects.remove(ob,do_unlink=True)
 o.parent=None;o.matrix_world=Matrix.Identity(4)
 for m in list(o.modifiers):o.modifiers.remove(m)
 # Remove the original Orc bust/neck, retaining chin and facial geometry.
 cap_clip(o,(0,0,1.65),(0,-.25,1));o['source_uv_name']='OrcAtlas';assign_weights(o);append_neck('human')
elif kind=='joker':
 bpy.ops.wm.open_mainfile(filepath=str(R/'JOKER_INSPECTION.blend'));o=next(o for o in bpy.data.objects if o.type=='MESH');o.name='JOKER_SUPPLIED_HEAD'
 for v in o.data.vertices:v.co.x-=.0047;v.co.z-=.0079
 o['native_eye_alignment_translation_m']=[-.0047,0,-.0079]
 for ob in list(bpy.data.objects):
  if ob!=o:bpy.data.objects.remove(ob,do_unlink=True)
 # Preserve the actual face and hair sculpt; native neck joins below the jaw.
 cap_clip(o,(0,0,1.677),(0,-.38,1)) # Preserve the face and join at the anatomical underside of the jaw.
 # Reduce to the mobile index budget; the full input blend is left unchanged.
 o.data.calc_loop_triangles();n=len(o.data.loop_triangles)
 if n>82000:
  bpy.context.view_layer.objects.active=o;o.select_set(True);m=o.modifiers.new('Mobile source head reduction','DECIMATE');m.ratio=82000/n;m.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=m.name)
 mat=material('Joker new authored film-inspired makeup',(.7,.75,.7));mat['paint_id']=1;o.data.materials.clear();o.data.materials.append(mat)
 for p in o.data.polygons:p.material_index=0;p.use_smooth=True
 assign_weights(o);append_neck('joker')
elif kind=='naruto':
 data=json.loads((R/'naruto-3ds.json').read_text());keep=['kepala','rambut','ikat_kepal','mata','mulut'];scale=.0112;eye_z=(125.26360321044922+132.1110076904297)/2;dz=1.7135-eye_z*scale;dy=-.135-((-4.086900234222412+2.916599988937378)/2)*scale;dx=.00020664
 colors={1:(.72,.43,.22),2:(.95,.57,.025),3:(.012,.025,.07),4:(.018,.008,.006),5:(.8,.8,.7)};mats={i:material('Naruto authored part '+str(i),rgb)for i,rgb in colors.items()}
 for i,m in mats.items():m['paint_id']=i
 for row in data['objects']:
  name=row['name']
  if name not in keep:continue
  verts=[(p[0]*scale+dx,p[1]*scale+dy+.02,p[2]*scale+dz)for p in row['vertices']];me=bpy.data.meshes.new(name);me.from_pydata(verts,[],row['faces']);me.update();ob=bpy.data.objects.new('NARUTO_'+name,me);bpy.context.scene.collection.objects.link(ob);pid={'kepala':1,'rambut':2,'ikat_kepal':3,'mata':5,'mulut':4}[name];me.materials.append(mats[pid])
  if name=='mulut':
   me.materials.append(mats[1]);body=set(row['face_materials'].get('body',[]))
   for p in me.polygons:p.material_index=int(p.index in body)
  uv=me.uv_layers.new(name='SourceUV')
  if 'uv'in row:
   for l in me.loops:uv.data[l.index].uv=row['uv'][l.vertex_index]
  for p in me.polygons:p.use_smooth=True
  if name=='kepala':cap_clip(ob,(0,0,1.608),(0,0,1))
  assign_weights(ob)
 append_neck('naruto')
else:raise ValueError(kind)
for ob in list(bpy.data.objects):
 if ob.type!='MESH':bpy.data.objects.remove(ob,do_unlink=True)
for o in bpy.data.objects:
 if o.type=='MESH':
  for m in list(o.modifiers):o.modifiers.remove(m)
  for mat in o.data.materials:
   if mat and mat.use_nodes:
    for n in mat.node_tree.nodes:
     if n.type=='TEX_IMAGE'and n.image and n.image.source!='VIEWER':n.image.pack()
scene_setup(.47 if kind=='hulk'else .45 if kind=='orc'else .43);bpy.ops.wm.save_as_mainfile(filepath=str(out/(kind.upper()+'_SOURCE_NECK2006.blend')),compress=True)

if '--no-render' not in sys.argv:render_views(out,.47 if kind=='hulk'else .45 if kind=='orc'else .43)
print('SOURCE_READY',kind,flush=True)
