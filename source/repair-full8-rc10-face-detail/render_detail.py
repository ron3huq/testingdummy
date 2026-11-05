import bpy,numpy as np,math,json
from pathlib import Path
from mathutils import Vector,Matrix
r=Path('/workspace/apk73-face-detail/preview');d=np.load(r/'asset.npz');p=d['p'];f=d['f'];uv=d['uv'];ntri=int(d['skin_tris']);tri=p[f];drawn=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)>1e-9;original_face_ids=np.flatnonzero(drawn);f=f[drawn];bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.resolution_x=700;scene.render.resolution_y=850;scene.render.resolution_percentage=100;scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
mesh=bpy.data.meshes.new('Readback');pp=p*np.array([1,-1,1])/100;mesh.from_pydata(pp.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new('RONALDO2027-ID89138556572074',mesh);scene.collection.objects.link(o);uvlayer=mesh.uv_layers.new()
for poly in mesh.polygons:
 poly.use_smooth=True
 for li,vi in zip(poly.loop_indices,poly.vertices):uvlayer.data[li].uv=(float(uv[vi,0]),float(1-uv[vi,1]))
def mat(name,image,hair=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(r/image));m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.62;bs.inputs['Specular IOR Level'].default_value=.25
 if not hair:
  sro=m.node_tree.nodes.new('ShaderNodeTexImage');sro.image=bpy.data.images.load(str(r/'skin-SRO.png'));sro.image.colorspace_settings.name='Non-Color';sep=m.node_tree.nodes.new('ShaderNodeSeparateXYZ');m.node_tree.links.new(sro.outputs['Color'],sep.inputs[0]);m.node_tree.links.new(sep.outputs['Y'],bs.inputs['Roughness']);m.node_tree.links.new(sep.outputs['X'],bs.inputs['Specular IOR Level'])
  nt=m.node_tree.nodes.new('ShaderNodeTexImage');nt.image=bpy.data.images.load(str(r/'skin-N.png'));nt.image.colorspace_settings.name='Non-Color';sep=m.node_tree.nodes.new('ShaderNodeSeparateXYZ');m.node_tree.links.new(nt.outputs['Color'],sep.inputs[0]);inv=m.node_tree.nodes.new('ShaderNodeMath');inv.operation='SUBTRACT';inv.inputs[0].default_value=1;m.node_tree.links.new(sep.outputs['Y'],inv.inputs[1]);combine=m.node_tree.nodes.new('ShaderNodeCombineXYZ');m.node_tree.links.new(sep.outputs['X'],combine.inputs[0]);m.node_tree.links.new(inv.outputs[0],combine.inputs[1]);m.node_tree.links.new(sep.outputs['Z'],combine.inputs[2]);normal=m.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.65;m.node_tree.links.new(combine.outputs[0],normal.inputs['Color']);m.node_tree.links.new(normal.outputs[0],bs.inputs['Normal'])
 if hair:
  cut=m.node_tree.nodes.new('ShaderNodeMath');cut.operation='GREATER_THAN';cut.inputs[1].default_value=.333;m.node_tree.links.new(tex.outputs['Alpha'],cut.inputs[0]);m.node_tree.links.new(cut.outputs[0],bs.inputs['Alpha']);m.surface_render_method='DITHERED'
 return m
mesh.materials.append(mat('Packaged face diffuse','skin-D.png'));mesh.materials.append(mat('Retained packaged hair','hair-D.png',True))
for i,poly in enumerate(mesh.polygons):poly.material_index=int(original_face_ids[i]>=ntri)
native_normals=d['tan'][:,4:7].copy().view('i1').astype(float)*np.array([1,-1,1]);native_normals/=np.maximum(np.linalg.norm(native_normals,axis=1)[:,None],1e-9);mesh.normals_split_custom_set([native_normals[loop.vertex_index].tolist()for loop in mesh.loops])
for name,loc,power,size in [('Key',(-2,-3,4),380,3),('Fill',(2,-1,2.5),180,3),('Rim',(0,2,3),280,2)]:
 light=bpy.data.lights.new(name,'AREA');light.energy=power;light.size=size;lo=bpy.data.objects.new(name,light);scene.collection.objects.link(lo);lo.location=loc;lo.rotation_euler=(Vector((0,0,1.65))-lo.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.48;target=Vector((0,-.05,1.63));scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.render.image_settings.file_format='PNG'
for name,loc in [('front',(0,-3,1.65)),('left',(3,0,1.65)),('right',(-3,0,1.65)),('rear',(0,3,1.65))]:
 cam.location=loc;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(r/(name+'.png'));bpy.ops.render.render(write_still=True)
# Detail views use the same Android readback, without photo compositing.
cam.data.ortho_scale=.085;scene.render.resolution_x=1000;scene.render.resolution_y=500;detail_target=Vector((0,-.145,1.704));cam.location=(0,-3,1.71);cam.rotation_euler=(detail_target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(r/'eyes-close.png');bpy.ops.render.render(write_still=True)
cam.data.ortho_scale=.48;scene.render.resolution_x=700;scene.render.resolution_y=850
# Evaluate jaw movement through the packaged reference hierarchy and weights.
weights=d['weights'];rest=d['rest'];local=d['local'];parents=d['parents'];reports={}
for angle in [0,-10,-20]:
 posed=[]
 for i in range(len(parents)):
  a=local[i].copy()
  if i==8:a=a@np.array(Matrix.Rotation(math.radians(angle),4,'Z'))
  posed.append(a if parents[i]<0 else posed[parents[i]]@a)
 posed=np.array(posed);trans=posed@np.linalg.inv(rest);q=np.einsum('vij,vj->vi',np.einsum('vb,bij->vij',weights,trans),np.c_[p,np.ones(len(p))])[:,:3];assert np.isfinite(q).all();reports[str(angle)]={'finite':True,'maximum_displacement_cm':float(np.linalg.norm(q-p,axis=1).max())}
 if angle==-20:
  for v,xyz in zip(mesh.vertices,q*np.array([1,-1,1])/100):v.co=xyz
  mesh.update();cam.location=(0,-3,1.65);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(r/'jaw20.png');bpy.ops.render.render(write_still=True)
cam.data.ortho_scale=.09;scene.render.resolution_x=800;scene.render.resolution_y=600;detail_target=Vector((0,-.16,1.63));cam.location=(0,-3,1.65);cam.rotation_euler=(detail_target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(r/'mouth-open-close.png');bpy.ops.render.render(write_still=True)
(r/'pose-readback.json').write_text(json.dumps(reports,indent=2))
