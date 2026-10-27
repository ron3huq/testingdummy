import bpy,json,numpy as np,math,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');bpy.ops.wm.open_mainfile(filepath=str(R/'RONALDO_2009_COLOUR_PREP.blend'));skin=bpy.data.objects['face_high_2_fox_skin_mat'].data.materials[0];coords=[];polys=[];source_uvs=[]
for name in ['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat','hair_high_0_fox_skin_mat']:
 o=bpy.data.objects[name];off=len(coords);coords +=[v.co.copy()for v in o.data.vertices];polys +=[[i+off for i in p.vertices]for p in o.data.polygons];source_uvs +=[[Vector((*o.data.uv_layers[0].data[li].uv,0))for li in p.loop_indices]for p in o.data.polygons]
bv=BVHTree.FromPolygons(coords,polys)
d=P/'android-hair-v1/original-export/Game/Assets/character/RealFace';g=json.loads((d/'SK_4522_Face.gltf').read_text());raw=(d/g['buffers'][0]['uri']).read_bytes()
def arr(i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];n={'VEC2':2,'VEC3':3,'VEC4':4,'SCALAR':1}[a['type']];out=np.frombuffer(raw,dtype={5126:'<f4',5123:'<u2',5121:'u1'}[a['componentType']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),count=a['count']*n).reshape(-1,n);return out/255 if a.get('normalized')and a['componentType']==5121 else out
prim=g['meshes'][0]['primitives'][0];a=prim['attributes'];pp=arr(a['POSITION']);uv=arr(a['TEXCOORD_0']);js=arr(a['JOINTS_0']);ws=arr(a['WEIGHTS_0']);bones=[g['nodes'][i]['name']for i in g['skins'][0]['joints']];tt=arr(prim['indices']).reshape(-1,3);positions=[];locked=[];distances=[];sample_uv=[]
for i,p in enumerate(pp):
 v=Vector((p[0],-p[2],p[1]));orbit=min(math.sqrt(((v.x-c)/.035)**2+((v.z-1.7135)/.027)**2)for c in [.025596,-.035]);keep=1. if orbit<=1 and v.y<-.105 else max(0,1-(orbit-1)/.65)if v.y<-.105 else 0.
 q=v.copy();hit,n,idx,dist=bv.find_nearest(q)
 if hit is None:hit=v
 co=v.lerp(hit,1-keep);positions.append(co)
 from mathutils.geometry import barycentric_transform
 ids=polys[idx][:3];ps=[coords[k]for k in ids];sample_uv.append(barycentric_transform(hit,*ps,*source_uvs[idx][:3]))
 if keep==1:locked.append(i);assert (co-v).length<1e-9
 if keep==0:distances.append(float(bv.find_nearest(co)[3]))
for o in list(bpy.data.objects):
 if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
me=bpy.data.meshes.new('Native face topology with 2006 surface transfer');me.from_pydata(positions,[],tt.tolist());me.materials.append(skin);o=bpy.data.objects.new('NATIVE_2009_FACE_SKIN',me);bpy.context.collection.objects.link(o);layer=me.uv_layers.new(name='UV0')
for l in me.loops:u,v=uv[l.vertex_index];layer.data[l.index].uv=(u,1-v)
suv=me.uv_layers.new(name='Source2009SampleUV')
for l in me.loops:suv.data[l.index].uv=sample_uv[l.vertex_index].xy
me.uv_layers.active=layer;layer.active_render=True
for n in skin.node_tree.nodes:
 if n.type=='UVMAP':n.uv_map='Source2009SampleUV'
for i in range(len(positions)):
 for j,w in zip(js[i],ws[i]):
  if w>0:
   name=bones[int(j)];vg=o.vertex_groups.get(name)or o.vertex_groups.new(name=name);vg.add([i],float(w),'REPLACE')
for p in me.polygons:p.use_smooth=True
native_fields={'uv1':arr(a['TEXCOORD_1']).tolist(),'color':arr(a['COLOR_0']).tolist(),'tangent':arr(a['TANGENT']).tolist(),'normal':arr(a['NORMAL']).tolist()};(R/'original-native-fields.json').write_text(json.dumps(native_fields))
# The game uses shader flags in UV1/vertex colours for its eye overlays; emulate
# those transparent overlays only in the Blender preview, keeping game triangles.
par=list(range(len(positions)))
def root(i):
 while par[i]!=i:par[i]=par[par[i]];i=par[i]
 return i
for tri in tt:
 for j in tri[1:]:par[root(int(j))]=root(int(tri[0]))
components={}
for i in range(len(positions)):components.setdefault(root(i),[]).append(i)
hide=set(i for comp in components.values()if len(comp)<60 and all(positions[j].z>1.69 for j in comp)for i in comp)
transparent=bpy.data.materials.new('PREVIEW_NATIVE_EYE_OVERLAY_SHADER_EMULATION');transparent.use_nodes=True;nodes=transparent.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');tr=nodes.new('ShaderNodeBsdfTransparent');transparent.node_tree.links.new(tr.outputs[0],out.inputs[0]);transparent.surface_render_method='DITHERED';me.materials.append(transparent)
for p in me.polygons:
 if all(i in hide for i in p.vertices):p.material_index=1

shutil.copyfile(R/'RONALDO_2009_COLOUR_PREP.blend','/tmp/ronaldo_hair_source_native.blend')
with bpy.data.libraries.load('/tmp/ronaldo_hair_source_native.blend',link=False)as(x,y):y.objects=['hair_high_1_fox_hair_mat']
for ob in y.objects:bpy.context.collection.objects.link(ob);ob.name='RONALDO_2009_ON_2006_HAIR'
mat=bpy.data.materials.new('PREVIEW_ONLY_COMMON_NATIVE_EYES');mat.use_nodes=True;n=mat.node_tree.nodes;t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(P/'converted/eye_sclera_bsm.png'));t.image.pack();mat.node_tree.links.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
for label,c in [('l',(.025596,-.134239,1.713447)),('r',(-.035,-.13572,1.713532))]:
 bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=.0133,location=c);ob=bpy.context.object;ob.name='PREVIEW_ONLY_COMMON_EYE_'+label;ob.data.materials.append(mat)
 for l in ob.data.loops:
  v=ob.data.vertices[l.vertex_index].co;ob.data.uv_layers[0].data[l.index].uv=(.5+v.x/.0266,.5+v.z/.0266)
 for p in ob.data.polygons:p.use_smooth=True
report={'source':'Original 2006 geometry with supplied 2009 textures, explicitly authorized','native_topology_vertices':len(positions),'native_topology_triangles':len(tt),'native_vertex_order_preserved':True,'native_uvs_weights_preserved':True,'native_orbital_vertices_kept_exact':locked,'max_surface_projection_error_outside_eye_blend_m':max(distances),'game_eyeballs_added':False,'phone_tested':False};(R/'native-wrap-validation.json').write_text(json.dumps(report,indent=2));# Bake the V2 surface colour into the original native UV layout.
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.use_denoising=False
bpy.ops.object.select_all(action='DESELECT');target=bpy.data.objects['NATIVE_2009_FACE_SKIN'];target.select_set(True);bpy.context.view_layer.objects.active=target;image=bpy.data.images.new('NATIVE_UV_2009_DIFFUSE',1024,1024,alpha=True)
for m in target.data.materials:
 n=m.node_tree.nodes;node=n.new('ShaderNodeTexImage');node.image=image;n.active=node
s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True;s.render.bake.margin=5;bpy.ops.object.bake(type='DIFFUSE');image.filepath_raw=str(R/'native_face_diffuse.png');image.file_format='PNG';image.save();image.pack()
s.cycles.samples=24;s.cycles.use_denoising=False

for name,ang in [('front',0),('three_quarter',35),('profile',90)]:
 a=math.radians(ang);s.camera.location=(.65*math.sin(a),-.075-.65*math.cos(a),1.735);s.camera.rotation_euler=(Vector((0,-.075,1.68))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'))
 if name=='three_quarter':bpy.ops.wm.save_as_mainfile(filepath=str(R/'RONALDO_2009_NATIVE.blend'))
 bpy.ops.render.render(write_still=True)
