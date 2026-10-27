import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/analysis/five-faces-2026')
def material(name,rgb,rough=.65):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Specular IOR Level'].default_value=.15;m.diffuse_color=(*rgb,1);return m

def scene_setup(size=.43,target=(0,-.065,1.66)):
 s=bpy.context.scene
 for o in list(bpy.data.objects):
  if o.type in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
 s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.resolution_x=800;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.035,.035,.035,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.4
 s.view_settings.view_transform='AgX'
 for name,loc,power in [('Key',(-.4,-.6,2.05),5),('Fill',(.4,-.3,1.85),2),('Rim',(.1,.3,2),6)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=power;d.size=.5;a=bpy.data.objects.new(name,d);s.collection.objects.link(a);a.location=loc;a.rotation_euler=(Vector(target)-a.location).to_track_quat('-Z','Y').to_euler()
 d=bpy.data.cameras.new('Preview camera');c=bpy.data.objects.new('Preview camera',d);s.collection.objects.link(c);s.camera=c;d.type='ORTHO';d.ortho_scale=size
 return s

def render_views(folder,size=.43,target=(0,-.065,1.66)):
 s=scene_setup(size,target)
 for name,ang in [('front',0),('quarter',35),('profile',90),('back',180)]:
  a=math.radians(ang);s.camera.location=(.8*math.sin(a),target[1]-.8*math.cos(a),1.73);s.camera.rotation_euler=(Vector(target)-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(folder/(name+'.png'));bpy.ops.render.render(write_still=True)
 a=math.radians(35);s.camera.location=(.8*math.sin(a),target[1]-.8*math.cos(a),1.73);s.camera.rotation_euler=(Vector(target)-s.camera.location).to_track_quat('-Z','Y').to_euler()
 for area in bpy.context.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_extras=False;area.spaces.active.region_3d.view_perspective='CAMERA'

def cut_above(o,z):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,0,z),plane_no=(0,0,1),clear_inner=True,dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(o.data);bm.free();o.data.update()

def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def native_weights(p):
 x,y,z=p;h=smooth((z-1.405)/.200);c=smooth((z-1.445)/.10);chest=(1-h)*(1-c);return {'sk_head':h,'sk_cervicalspine_02':1-h-chest,'sk_spine_03':chest}
def assign_weights(o):
 for g in list(o.vertex_groups):o.vertex_groups.remove(g)
 for name in ['sk_head','sk_cervicalspine_02','sk_spine_03']:o.vertex_groups.new(name=name)
 custom=json.loads(o.get('bridge_weights_json','{}'))
 for v in o.data.vertices:
  w=custom.get(str(v.index),native_weights(o.matrix_world@v.co))if o.get('source_ronaldo_2006_neck')else{'sk_head':1}
  for name,value in w.items():
   if value>1e-8:o.vertex_groups[name].add([v.index],value,'REPLACE')

def append_neck(tint='human'):
 with bpy.data.libraries.load(str(R/'NECK_RONALDO_2006.blend'),link=False)as(a,b):b.objects=['NECK_RONALDO_2006_ORIGINAL']
 o=b.objects[0];bpy.context.scene.collection.objects.link(o);o.name='NECK_RONALDO_2006_'+tint.upper();o['source_ronaldo_2006_neck']=True
 # Continue the actual source cut boundary into a short fitted upper bridge.
 from mathutils.bvhtree import BVHTree
 from mathutils.geometry import barycentric_transform
 base_z=1.55
 if tint=='hulk':
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,0,base_z),plane_no=(0,0,1),clear_outer=True,dist=1e-7);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(o.data);bm.free();o['upper_boundary_vertex_indices']=[v.index for v in o.data.vertices if abs(v.co.z-base_z)<1e-5]
 ref=json.loads((R/'neck-reference.json').read_text());tree=BVHTree.FromPolygons(ref['vertices'],ref['faces']);old=o.data;coords=[v.co.copy()for v in old.vertices];faces=[list(p.vertices)for p in old.polygons];uvs=[[old.uv_layers[0].data[li].uv.copy()for li in p.loop_indices]for p in old.polygons];ring=list(o['upper_boundary_vertex_indices']);center=sum((coords[i]for i in ring),Vector())/len(ring);ring.sort(key=lambda i:math.atan2(coords[i].y-center.y,coords[i].x-center.x));rx=max(abs(coords[i].x-center.x)for i in ring);ry=max(abs(coords[i].y-center.y)for i in ring)
 profile={'hulk':(1.68,0,-.060,.065,.062),'human':(1.68,-.0047,-.060,.064,.065),'joker':(1.635,-.0047,-.065,.050,.042),'naruto':(1.625,0,-.105,.040,.040)}[tint];top,cx,cy,tx,ty=profile;previous=ring;custom_weights={};base_weights=native_weights(Vector((0,0,base_z)))
 head=next((q for q in bpy.data.objects if q.type=='MESH'and q.get('neck_join_ring_json')),None);join=None
 if head:
  join=[Vector(p)for p in json.loads(head['neck_join_ring_json'])];jc=sum(join,Vector())/len(join);angles=[math.atan2(p.y-jc.y,p.x-jc.x)for p in join];order=sorted(range(len(join)),key=lambda i:angles[i]);join=[join[i]for i in order];angles=[angles[i]for i in order];jn=Vector(head['neck_join_normal']);o['joins_actual_head_boundary']=True
 def endpoint(original):
  if join:
   angle=math.atan2(original.y-center.y,original.x-center.x);aa=np.asarray(angles);hi=int(np.searchsorted(aa,angle));lo=(hi-1)%len(join);hi%=len(join);a0=angles[lo];a1=angles[hi]
   if a1<=a0:a1+=math.tau
   if angle<a0:angle+=math.tau
   t=(angle-a0)/max(1e-9,a1-a0);return join[lo].lerp(join[hi],t)+jn*.0012
  return Vector((cx+(original.x-center.x)/rx*tx,cy+(original.y-center.y)/ry*ty,top))

 for step in range(1,7):
  t=step/6;blend=smooth(t);current=[]
  for index in ring:
   original=coords[index];target=endpoint(original);point=original.lerp(target,blend);point.z=base_z+(target.z-base_z)*t;current.append(len(coords));custom_weights[str(len(coords))]={k:w*(1-blend)+(blend if k=='sk_head'else 0)for k,w in base_weights.items()};coords.append(point)
  for k in range(len(ring)):faces.append([previous[k],previous[(k+1)%len(ring)],current[(k+1)%len(ring)],current[k]])
  previous=current
 faces.append(previous);mesh=bpy.data.meshes.new('Ronaldo 2006 source neck with fitted upper boundary');mesh.from_pydata(coords,[],faces);mesh.materials.append(old.materials[0]);layer=mesh.uv_layers.new(name='SourceUV')
 for i,poly in enumerate(mesh.polygons):
  for j,li in enumerate(poly.loop_indices):
   if i<len(uvs):u=uvs[i][j]
   else:
    point=mesh.vertices[mesh.loops[li].vertex_index].co;hit,n,pi,d=tree.find_nearest(point);u=barycentric_transform(hit,*[Vector(ref['vertices'][k])for k in ref['faces'][pi]],*[Vector((*q,0))for q in ref['uv'][pi]]).xy
   layer.data[li].uv=u
 o.data=mesh;bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 for poly in mesh.polygons:poly.use_smooth=True
 o['upper_bridge_rings']=6;o['original_neck_preserved_below_z']=base_z;o['bridge_weights_json']=json.dumps(custom_weights)
 mat=o.data.materials[0].copy();o.data.materials[0]=mat
 if tint!='human':
  n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');tex=next(t for t in n if t.type=='TEX_IMAGE');gray=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],gray.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.05;r.color_ramp.elements[1].position=.5
  if tint=='hulk':cols=[(.025,.035,.013,1),(.16,.20,.085,1)]
  elif tint=='joker':cols=[(.25,.28,.26,1),(.72,.76,.70,1)]
  else:cols=[(.35,.20,.10,1),(1.0,.75,.50,1)]
  for e,c in zip(r.color_ramp.elements,cols):e.color=c
  l.new(gray.outputs[0],r.inputs[0]);l.new(r.outputs[0],bs.inputs['Base Color'])
 assign_weights(o);return o

def fit_upper_neck():
 from mathutils.bvhtree import BVHTree
 heads=[o for o in bpy.data.objects if o.type=='MESH'and not o.get('source_ronaldo_2006_neck')];necks=[o for o in bpy.data.objects if o.type=='MESH'and o.get('source_ronaldo_2006_neck')];pp=[];ff=[]
 for o in heads:
  k=len(pp);pp.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[k+i for i in p.vertices]for p in o.data.polygons])
 tree=BVHTree.FromPolygons(pp,ff);count=0
 for o in necks:
  for v in o.data.vertices:
   z=v.co.z
   if z<o.get('fit_start_z',1.605):continue
   plane=o.get('head_join_plane')
   if plane and z<plane[0]+plane[1]*v.co.y+.001:continue
   front=tree.ray_cast(Vector((0,-1,z)),Vector((0,1,0)),2.)[0];back=tree.ray_cast(Vector((0,1,z)),Vector((0,-1,0)),2.)[0]
   if front is None or back is None or back.y-front.y<.09:continue
   center=Vector((0,(front.y+back.y)/2,z));d=v.co-center;d.z=0
   if d.length<1e-6:continue
   direction=d.normalized();hit=tree.ray_cast(center,direction,1.)[0]
   if hit is None:continue
   limit=max(.001,(hit-center).length-.0015)
   if d.length>limit:v.co=center+direction*limit;count+=1
  o['upper_neck_vertices_tucked_inside_supplied_head']=count
 print('UPPER_NECK_FIT',count,flush=True)

def cap_clip(o,co,normal,skin_only=False):
 from mathutils.bvhtree import BVHTree
 from mathutils.geometry import barycentric_transform
 me=o.data;oldp=[v.co.copy()for v in me.vertices];oldf=[tuple(p.vertices)for p in me.polygons];oldu=[[me.uv_layers.active.data[li].uv.copy()for li in p.loop_indices]for p in me.polygons];tree=BVHTree.FromPolygons(oldp,oldf)
 bm=bmesh.new();bm.from_mesh(me);tag=bm.faces.layers.int.new('cut_cap')
 selected=[f for f in bm.faces if not skin_only or f.material_index==0];vv=set(v for f in selected for v in f.verts);ee=set(e for f in selected for e in f.edges)
 result=bmesh.ops.bisect_plane(bm,geom=list(vv)+list(ee)+selected,plane_co=co,plane_no=normal,clear_inner=True,dist=1e-7);cut=set(v for e in result['geom_cut']if isinstance(e,bmesh.types.BMEdge)for v in e.verts)
 unique={tuple(round(c,7)for c in v.co):v for v in cut};cut=list(unique.values());assert len(cut)>8,(o.name,len(cut));center=sum((v.co for v in cut),Vector())/len(cut);cut.sort(key=lambda v:math.atan2(v.co.y-center.y,v.co.x-center.x));o['neck_join_ring_json']=json.dumps([list(v.co)for v in cut]);o['neck_join_normal']=list(Vector(normal).normalized())
 cap=bm.faces.new(list(reversed(cut)));cap[tag]=1;cap.material_index=0;bmesh.ops.triangulate(bm,faces=[cap]);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.faces.ensure_lookup_table();ids=[i for i,f in enumerate(bm.faces)if f[tag]==1];bm.to_mesh(me);bm.free()
 for pi in ids:
  for li in me.polygons[pi].loop_indices:
   p=me.vertices[me.loops[li].vertex_index].co;hit,n,idx,d=tree.find_nearest(p);uv=barycentric_transform(hit,*[oldp[k]for k in oldf[idx][:3]],*[Vector((*a,0))for a in oldu[idx][:3]]);me.uv_layers.active.data[li].uv=uv.xy
 me.update();o['closed_neck_join_cap_faces']=len(ids)
