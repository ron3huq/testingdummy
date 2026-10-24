import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/ronaldo-work');P=R/'new-hair-sources';sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
base=bpy.data.objects['hair_high_1_fox_hair_mat'];bpy.data.objects.remove(base,do_unlink=True)
# Delete degenerate old head shell too, retain original face and neck/scalp.
old=bpy.data.objects.get('hair_high_2_fox_head_shell_mat')
if old:bpy.data.objects.remove(old,do_unlink=True)
f=FmdlFile();f.readFile(str(P/'2017/fpk/hair_high.fmdl'));src=f.meshes[0]
mat=bpy.data.materials.new('2017_Original_2UV_Color_and_Alpha');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.65;bs.inputs['Specular IOR Level'].default_value=.08
for file,uvname,target in [('hair_parts_bsm_alp.png','UV1','Base Color'),('hair_alpha8.png','UV0','Alpha')]:
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(P/'2017/converted'/file));tex.image.alpha_mode='CHANNEL_PACKED' if target=='Alpha' else 'STRAIGHT';tex.image.pack();uv=n.new('ShaderNodeUVMap');uv.uv_map=uvname;l.new(uv.outputs['UV'],tex.inputs['Vector']);l.new(tex.outputs['Alpha' if target=='Alpha' else 'Color'],bs.inputs[target])
mat.surface_render_method='DITHERED'
def cv(p):return(p.x,-p.z,p.y)
indices={id(v):i for i,v in enumerate(src.vertices)};mesh=bpy.data.meshes.new('2017_source_hair_mesh');mesh.from_pydata([cv(v.position) for v in src.vertices],[],[[indices[id(v)] for v in reversed(face.vertices)] for face in src.faces]);mesh.update()
ob=bpy.data.objects.new('HAIR_2017_FROM_USER_RAR',mesh);bpy.context.scene.collection.objects.link(ob);mesh.materials.append(mat)
for ui in range(src.vertexFields.uvCount):
 uv=mesh.uv_layers.new(name=f'UV{ui}')
 for loop in mesh.loops:
  value=src.vertices[loop.vertex_index].uv[ui];uv.data[loop.index].uv=(value.u,1-value.v)
mesh.normals_split_custom_set([cv(src.vertices[loop.vertex_index].normal) for loop in mesh.loops])
for b in f.bones:
 ids=[]
 for i,v in enumerate(src.vertices):
  w=(v.boneMapping or {}).get(b,0)
  if w:
   if b.name not in ob.vertex_groups:ob.vertex_groups.new(name=b.name)
   ob.vertex_groups[b.name].add([i],w,'REPLACE')
rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID'];ob.parent=rig;mod=ob.modifiers.new('PES reference skinning','ARMATURE');mod.object=rig
for poly in mesh.polygons:poly.use_smooth=True
ob['source']='ronaldo2017.rar hair_high.fmdl Material.002; original source geometry/UV0/UV1/weights'
# Transfer donor scalp UV onto unchanged 2006 scalp geometry by nearest triangle.
# Keep original neck skin color below 1.70m; no replacement of face geometry.
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
cap=bpy.data.objects['hair_high_0_fox_skin_mat'];donor=f.meshes[1]
di={id(v):i for i,v in enumerate(donor.vertices)};dverts=[Vector(cv(v.position)) for v in donor.vertices];dfaces=[[di[id(v)] for v in reversed(ff.vertices)] for ff in donor.faces];tree=BVHTree.FromPolygons(dverts,dfaces)
uv=cap.data.uv_layers.new(name='2017_SCALP_UV')
for loop in cap.data.loops:
 point=cap.data.vertices[loop.vertex_index].co;hit,normal,fi,dist=tree.find_nearest(point);ids=dfaces[fi]
 coords=[Vector((donor.vertices[i].uv[0].u,1-donor.vertices[i].uv[0].v,0)) for i in ids]
 q=barycentric_transform(hit,*[dverts[i] for i in ids],*coords);uv.data[loop.index].uv=(q.x,q.y)
cm=cap.data.materials[0].copy();cm.name='2006_Neck_and_2017_Scalp';cap.data.materials[0]=cm;cn=cm.node_tree.nodes;cl=cm.node_tree.links;cb=cn.get('Principled BSDF');originaltex=next(t for t in cn if t.type=='TEX_IMAGE')
t=cn.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(P/'2017/converted/face_bsm_alp.png'));t.image.alpha_mode='NONE';t.image.pack();uvn=cn.new('ShaderNodeUVMap');uvn.uv_map=uv.name;cl.new(uvn.outputs[0],t.inputs['Vector'])
geom=cn.new('ShaderNodeNewGeometry');sep=cn.new('ShaderNodeSeparateXYZ');cl.new(geom.outputs['Position'],sep.inputs[0]);mask=cn.new('ShaderNodeMapRange');mask.clamp=True;mask.inputs['From Min'].default_value=1.68;mask.inputs['From Max'].default_value=1.73;cl.new(sep.outputs['Z'],mask.inputs['Value']);mix=cn.new('ShaderNodeMixRGB');cl.new(mask.outputs[0],mix.inputs[0]);cl.new(originaltex.outputs['Color'],mix.inputs[1]);cl.new(t.outputs['Color'],mix.inputs[2]);cl.new(mix.outputs[0],cb.inputs['Base Color']);cb.inputs['Roughness'].default_value=.8;cb.inputs['Specular IOR Level'].default_value=.1
# Include only original face objects; no face geometry or skin shaders from 2017.
s=bpy.context.scene;bpy.data.objects['Rim'].data.energy=2.0;s['variant']='Original 2006 face and scalp + supplied 2017 hair. Not Android cooked.'
for obj in bpy.data.objects:
 if obj.type in ['ARMATURE','LIGHT','CAMERA']:obj.hide_set(True)
for scr in bpy.data.screens:
 for a in scr.areas:
  if a.type=='VIEW_3D':a.spaces.active.overlay.show_overlays=False;a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_location=(0,-.06,1.72);a.spaces.active.region_3d.view_distance=.44
bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100
out=P/'hybrid-2006-2017';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Ronaldo_2006_FACE_2017_HAIR.blend'))
cam=s.camera
for label,loc in [('front',(0,-.70,1.77)),('three-quarter',(.27,-.65,1.80)),('side',(.65,.03,1.74))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37;s.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True)
print('HYBRID_DONE',len(mesh.vertices),len(mesh.polygons))
