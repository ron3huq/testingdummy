import bpy,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from scipy.ndimage import distance_transform_edt
R=Path(__file__).parent;sys.path.insert(0,str(R));from common import *;from paint import paint
kind=sys.argv[sys.argv.index('--')+1];out=R/kind;bpy.ops.wm.open_mainfile(filepath=str(out/(kind.upper()+'_SOURCE_NECK2006.blend')));s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.use_denoising=False;s.cycles.samples=8
meshes=[o for o in bpy.data.objects if o.type=='MESH']
for o in list(bpy.data.objects):
 if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
# Preserve each source's true image UV before making the independent mobile atlas.
for o in meshes:
 desired=o.data.uv_layers.get(o.get('source_uv_name',''))or o.data.uv_layers.active
 data=[u.uv.copy()for u in desired.data]if desired else[(0.,0.)for l in o.data.loops]
 for old in list(o.data.uv_layers):o.data.uv_layers.remove(old)
 u=o.data.uv_layers.new(name='SourceUV')
 for a,b in zip(u.data,data):a.uv=b
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 n=mat.node_tree.nodes;uv=n.new('ShaderNodeUVMap');uv.uv_map='SourceUV'
 for t in list(n):
  if t.type=='TEX_IMAGE':mat.node_tree.links.new(uv.outputs[0],t.inputs['Vector'])
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();o=bpy.context.object;o.name=kind.upper()+'_GAME_HEAD_NECK';me=o.data
if kind in ['orc','naruto']:
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000015);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for poly in me.polygons:poly.use_smooth=True
if kind in ['orc','naruto']:
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
 from mathutils.bvhtree import BVHTree
 from mathutils.geometry import barycentric_transform
 from scipy.spatial import cKDTree
 me.calc_loop_triangles();oldcoords=[v.co.copy()for v in me.vertices];oldtri=[list(t.vertices)for t in me.loop_triangles];oldm=[me.polygons[t.polygon_index].material_index for t in me.loop_triangles];olduv=[[me.uv_layers.active.data[li].uv.copy()for li in t.loops]for t in me.loop_triangles];tree=BVHTree.FromPolygons(oldcoords,oldtri,all_triangles=True);oldweights=[{o.vertex_groups[g.group].name:g.weight for g in v.groups}for v in me.vertices];kd=cKDTree(np.array(oldcoords))
 mod=o.modifiers.new('Continuous skin junction','REMESH');mod.mode='VOXEL';mod.voxel_size=.0010;mod.use_remove_disconnected=False;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('Smooth repaired junction','SMOOTH');mod.factor=.45;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 o.data.calc_loop_triangles();nt=len(o.data.loop_triangles)
 if nt>60000:
  mod=o.modifiers.new('Mobile surface','DECIMATE');mod.ratio=60000/nt;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 me=o.data
 if kind=='orc':
  vg=o.vertex_groups.new(name='Repair neck contour')
  for v in me.vertices:
   z=v.co.z;y=v.co.y
   w=max(0,min(1,(z-1.50)/.035))*max(0,min(1,(1.72-z)/.035))
   if y<-.09 and z>1.63:w*=max(0,1-(z-1.63)/.02)
   if w>0:vg.add([v.index],w,'REPLACE')
  mod=o.modifiers.new('Natural neck contour','SMOOTH');mod.factor=.75;mod.iterations=100;mod.vertex_group=vg.name;bpy.ops.object.modifier_apply(modifier=mod.name);me=o.data
 for vg in list(o.vertex_groups):o.vertex_groups.remove(vg)
 for name in ['sk_head','sk_cervicalspine_02','sk_spine_03']:o.vertex_groups.new(name=name)
 _,nearest=kd.query(np.array([v.co[:]for v in me.vertices]))
 for v,nearidx in zip(me.vertices,nearest):
  for name,w in native_weights(v.co).items():
   if w>1e-8:o.vertex_groups[name].add([v.index],w,'REPLACE')
 uvnew=me.uv_layers.new(name='SourceUV')
 for poly in me.polygons:
  hit,n,pi,d=tree.find_nearest(poly.center);poly.material_index=oldm[pi];poly.use_smooth=True
  for li in poly.loop_indices:
   point=me.vertices[me.loops[li].vertex_index].co;hit,n,pi2,d=tree.find_nearest(point);uvnew.data[li].uv=barycentric_transform(hit,*[oldcoords[k]for k in oldtri[pi2]],*[Vector((*q,0))for q in olduv[pi2]]).xy

uv=me.uv_layers.new(name='GameAtlas');me.uv_layers.active=uv;uv.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.25,island_margin=.003);bpy.ops.object.mode_set(mode='OBJECT');s.render.bake.use_selected_to_active=False;s.render.bake.use_clear=True;s.render.bake.margin=6
materials=[m for m in me.materials if m];original=[]
for mat in materials:
 output=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL');original.append((mat,output.inputs['Surface'].links[0].from_socket if output.inputs['Surface'].links else None))
def bake(name,typ,mode=None):
 im=bpy.data.images.new(name,2048,2048,alpha=True,float_buffer=bool(mode));im.generated_color=(0,0,0,0)
 if mode:im.colorspace_settings.name='Non-Color'
 for mat,orig in original:
  n=mat.node_tree.nodes;l=mat.node_tree.links;output=next(n for n in n if n.type=='OUTPUT_MATERIAL')
  if mode:
   em=n.new('ShaderNodeEmission')
   if mode=='position':
    g=n.new('ShaderNodeNewGeometry');add=n.new('ShaderNodeVectorMath');add.operation='ADD';add.inputs[1].default_value=(.25,.35,-1.3);l.new(g.outputs['Position'],add.inputs[0]);l.new(add.outputs[0],em.inputs['Color'])
   else:em.inputs['Color'].default_value=(mat.get('paint_id',0)/10,0,0,1)
   l.new(em.outputs[0],output.inputs['Surface'])
  t=n.new('ShaderNodeTexImage');t.image=im;n.active=t
 s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True;bpy.ops.object.bake(type=typ)
 for mat,orig in original:
  if orig:
   output=next(n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL');mat.node_tree.links.new(orig,output.inputs['Surface'])
 a=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(a);return im,a.reshape(-1,4)
base,colour=bake('Source diffuse','DIFFUSE');valid=colour[:,3]>.5;near=None
if not valid.all():
 idx=distance_transform_edt(~valid.reshape(2048,2048),return_distances=False,return_indices=True);near=(idx[0]*2048+idx[1]).reshape(-1);colour[~valid,:3]=colour[near[~valid],:3]
if kind in ['joker','naruto','orc']:
 pim,p=bake('World paint coordinates','EMIT','position');iim,ids=bake('Source part IDs','EMIT','id')
 if near is not None:p[~valid]=p[near[~valid]];ids[~valid]=ids[near[~valid]]
 pos=p[:,:3]-np.array([.25,.35,-1.3]);codes=np.rint(ids[:,0]*10).astype(np.int32);colour[:,:3]=paint(kind,pos,codes,colour[:,:3])
 if kind=='naruto':colour[codes==0,:3]=(.90,.64,.40)
 if kind=='orc':
  # One human skin palette for both sculpt and neck; retain surface variation.
  lum=colour[:,:3].mean(axis=1);skin=(pos[:,2]<1.61)|((pos[:,2]<1.665)&(pos[:,1]>-.12))|(colour[:,1]>colour[:,0]*1.15)
  variation=np.ones_like(lum);colour[skin,:3]=np.array([.48,.29,.18])*variation[skin,None]
 _,ao=bake('Source sculpt cavity','AO');ao=np.clip(ao[:,0],0,1)
 if near is not None:ao[~valid]=ao[near[~valid]]
 colour[:,:3]*=(.80+.20*ao[:,None])
colour[:,3]=1;atlas=bpy.data.images.new(kind.upper()+' final game atlas',2048,2048,alpha=True);atlas.pixels.foreach_set(colour.reshape(-1));atlas.filepath_raw=str(out/'atlas.png');atlas.file_format='PNG';atlas.save();atlas.pack()
mat=material(kind.upper()+' decoded-style game preview',(.5,.5,.5),.78 if kind=='hulk'else.67);n=mat.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=atlas;mat.node_tree.links.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);n.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.05 if kind=='hulk'else.15;me.materials.clear();me.materials.append(mat)
for p in me.polygons:p.material_index=0
# Export UV seams with exact per-source head positions and native neck weights.
me.calc_loop_triangles();verts=[];tri=[];lookup={};names={g.index:g.name for g in o.vertex_groups}
for face in me.loop_triangles:
 row=[]
 for li in face.loops:
  lp=me.loops[li];v=me.vertices[lp.vertex_index];u=uv.data[li].uv;normal=me.corner_normals[li].vector;key=(v.index,round(u.x,7),round(u.y,7))
  if key not in lookup:
   weights={names[g.group]:g.weight for g in v.groups if g.weight>1e-8};total=sum(weights.values());assert total>0;weights={n:w/total for n,w in weights.items()};lookup[key]=len(verts);verts.append({'p':list(v.co),'n':list(normal),'uv':list(u),'weights':weights})
  row.append(lookup[key])
 tri.append(row)
assert len(verts)<65532,(kind,len(verts));(out/'native_geometry.json').write_text(json.dumps({'vertices':verts,'triangles':tri}));(out/'export-validation.json').write_text(json.dumps({'kind':kind,'vertices':len(verts),'triangles':len(tri),'neck_source':'Ronaldo 2006 actual source mesh; lower neck coordinates preserved, upper overlap fitted','head_geometry_source':'supplied model'if kind in ['joker','naruto','orc']else'previous delivered Hulk LOD','new_authored_colour':kind in ['joker','naruto'],'fixed_facial_expression':True,'phone_tested':False},indent=2));print('EXPORT',kind,len(verts),len(tri),flush=True)
# The preview rig is the same native rest rig used by the cooked builder.
old=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath='/workspace/analysis/my-league/ronaldo-pc-conversion/android-hair-v1/original-export/Game/Assets/character/RealFace/SK_4522_Face.gltf');new=set(bpy.data.objects)-old;arm=next(x for x in new if x.type=='ARMATURE')
for ob in new:
 if ob.type=='MESH':bpy.data.objects.remove(ob,do_unlink=True)
arm.name=kind.upper()+'_NATIVE_166_BONE_RIG';mod=o.modifiers.new('Native head and neck rig','ARMATURE');mod.object=arm;o.parent=arm;o.matrix_parent_inverse=arm.matrix_world.inverted();arm.hide_render=True
# Purge bake-only images and unused source material blocks while keeping the packed final atlas.
bpy.ops.outliner.orphans_purge(do_recursive=True);render_views(out,.47 if kind=='hulk'else.45 if kind=='orc'else.43);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.wm.save_as_mainfile(filepath=str(out/(kind.upper()+'_NECK2006_GAME.blend')),compress=True);print('COMPLETE',kind,flush=True)
