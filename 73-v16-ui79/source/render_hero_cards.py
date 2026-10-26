"""Portraits rendered from the supplied hero meshes; no face generation or remodel."""
import bpy,struct,sys,math,json
from pathlib import Path
from mathutils import Vector
P=Path('/tmp/73-ui79');R=P/'hero-pack/full-export/Game/Assets/character/RealFace';O=P/'art';report=[]
def psk(path):
 data=path.read_bytes();at=0;chunks={}
 while at<len(data):
  name,flags,size,count=struct.unpack_from('<20siii',data,at);at+=32;chunks[name.rstrip(b'\0').decode()]=(data[at:at+size*count],size,count);at+=size*count
 points=[p for p in struct.iter_unpack('<fff',chunks['PNTS0000'][0])];wedges=[]
 raw,size,count=chunks['VTXW0000']
 for i in range(count):
  point,u,v,mat=struct.unpack_from('<IffB',raw,i*size);wedges.append((point,u,v,mat))
 raw,size,count=chunks['FACE0000'];faces=[];mats=[]
 for i in range(count):
  a,b,c,mat=struct.unpack_from('<HHHB',raw,i*size);faces.append((a,b,c));mats.append(mat)
 return [(points[p][0]*.01,points[p][1]*.01,points[p][2]*.01)for p,u,v,m in wedges],[(u,1-v)for p,u,v,m in wedges],faces,mats
for tag,hair,target in [('NHUL','NH0001','106754901843130'),('NSPD','NS0001','105647605587130')]:
 bpy.ops.wm.read_factory_settings(use_empty=True);verts,uv,faces,mats=psk(R/('SK_'+tag+'_Face.psk'));mesh=bpy.data.meshes.new(tag);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(tag,mesh);bpy.context.collection.objects.link(obj);uvmap=mesh.uv_layers.new(name='UVMap')
 for poly,mat in zip(mesh.polygons,mats):
  poly.material_index=mat;poly.use_smooth=True
  for li,vi in zip(poly.loop_indices,poly.vertices):uvmap.data[li].uv=uv[vi]
 for i in range(2):
  name='T_'+hair+'_Hair_D.tga'if tag=='NHUL'or i==1 else'T_4522_Face_D.tga';m=bpy.data.materials.new(tag+str(i));m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');shader=nodes.new('ShaderNodeBsdfPrincipled');tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/name));m.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color']);shader.inputs['Roughness'].default_value=.9;shader.inputs['Specular IOR Level'].default_value=0;m.node_tree.links.new(tex.outputs['Alpha'],shader.inputs['Alpha']);m.surface_render_method='DITHERED';m.node_tree.links.new(shader.outputs['BSDF'],out.inputs['Surface']);mesh.materials.append(m)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=736;scene.render.resolution_y=1024;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=-.3;scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.59,.65,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
 aim=Vector((0,-.05,1.66 if tag=='NHUL'else 1.67))
 def light(name,loc,power,size,col):
  data=bpy.data.lights.new(name,'AREA');data.energy=power;data.size=size;data.color=col;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(aim-o.location).to_track_quat('-Z','Y').to_euler()
 light('Key',(-.5,-.9,2.25),24,.8,(1,.92,.78));light('Fill',(.5,-.8,1.8),10,.7,(.72,.83,1));light('Rim',(.3,.3,2),6,.5,(.9,.95,1))
 camera_data=bpy.data.cameras.new('Portrait');camera=bpy.data.objects.new('Portrait',camera_data);scene.collection.objects.link(camera);camera.location=(.035,-1.4,1.70);camera.rotation_euler=(aim-camera.location).to_track_quat('-Z','Y').to_euler();camera_data.type='ORTHO';camera_data.ortho_scale=.56 if tag=='NHUL'else .51;scene.camera=camera;scene.render.filepath=str(O/(target+'-render.png'));bpy.ops.render.render(write_still=True);report.append({'id':target,'source_mesh':str(R/('SK_'+tag+'_Face.psk')),'method':'CPU Blender render from the supplied mesh and its source diffuse textures','geometry_modified':False,'output':scene.render.filepath,'face_vertices':len(verts),'triangles':len(faces)})
(P/'hero-art-provenance.json').write_text(json.dumps(report,indent=2))
