"""PES source inspection scene, NOT an Android cooked asset."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
import PesSkeletonData
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene['target_card_id']='88044950524330'
scene['status']='SOURCE_CONVERSION_ONLY_NOT_GAME_READY'
scene['source_author']='NEUBE (user-supplied PES 2021 PC mod)'
scene['rig_status']='PES reference rig; NOT retargeted to eFootball Android'
models={}
for name in ['face_high','hair_high','oral']:
 f=FmdlFile();f.readFile(str(ROOT/'source-extracted'/f'{name}.fmdl'));models[name]=f
# Keep original skin weight names. Reference bone positions follow the source addon.
bones={b.name:b for f in models.values() for b in f.bones}
arm=bpy.data.armatures.new('PES_REFERENCE_NOT_ANDROID');rig=bpy.data.objects.new('PES_REFERENCE_NOT_ANDROID',arm);scene.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def cv(t):return(t[0],-t[2],t[1])
for name,b in bones.items():
 ref=PesSkeletonData.bones.get(name);eb=arm.edit_bones.new(name)
 if ref:eb.head=cv(ref.startPosition);eb.tail=cv(ref.endPosition)
 else:
  p=b.globalPosition;eb.head=cv((p.x,p.y,p.z));eb.tail=eb.head+Vector((0,0,.005))
 if(eb.tail-eb.head).length<1e-6:eb.tail=eb.head+Vector((0,0,.005))
for name,b in bones.items():
 ref=PesSkeletonData.bones.get(name);parent=ref.renderParent if ref else (b.parent.name if b.parent else None)
 while parent and parent not in bones:
  parent=PesSkeletonData.bones[parent].renderParent if parent in PesSkeletonData.bones else None
 if parent:arm.edit_bones[name].parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False)
materials={};missing=[]
def loadtex(nodes,links,filename,uvindex=0,noncolor=False):
 p=ROOT/'converted'/(Path(filename).stem+'.png')
 if not p.exists():return None
 node=nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(p),check_existing=True);node.label=filename
 if noncolor:node.image.colorspace_settings.name='Non-Color'
 if Path(filename).stem in ['face_bsm_alp','hair_parts_bsm_alp']:node.image.alpha_mode='NONE'
 if Path(filename).stem=='hair_alpha8':node.image.alpha_mode='CHANNEL_PACKED'
 uv=nodes.new('ShaderNodeUVMap');uv.uv_map=f'UV{uvindex}';links.new(uv.outputs['UV'],node.inputs['Vector']);return node
for model,f in models.items():
 for m in f.materialInstances:
  key=(model,m.name);mat=bpy.data.materials.new(model+'_'+m.name);mat.use_nodes=True
  mat['fox_shader']=m.shader;mat['fox_technique']=m.technique
  mat['fox_texture_bindings']=json.dumps([(r,t.filename) for r,t in m.textures])
  nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF');bsdf.inputs['Roughness'].default_value=.58
  maps={r:t.filename for r,t in m.textures}
  for r,t in m.textures:
   if not (ROOT/'converted'/(Path(t.filename).stem+'.png')).exists():missing.append(t.directory+t.filename)
  if m.name=='Material.002':
   color=loadtex(nodes,links,maps['Base_Tex_2_SRGB'],1);alpha=loadtex(nodes,links,maps['Base_Tex_SRGB'],0)
   if alpha:links.new(alpha.outputs['Color'],bsdf.inputs['Base Color'])
   if alpha:links.new(alpha.outputs['Alpha'],bsdf.inputs['Alpha'])
   mat.surface_render_method='DITHERED'
  elif 'Base_Tex_SRGB' in maps:
   tex=loadtex(nodes,links,maps['Base_Tex_SRGB'])
   if tex:links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
  else:bsdf.inputs['Base Color'].default_value=(.025,.018,.015,1)
  # Hide PC common overlay meshes lacking their authored textures; keep them in the file.
  materials[key]=mat
objects=[]
for model,f in models.items():
 for index,m in enumerate(f.meshes):
  name=f'{model}_{index}_{m.materialInstance.name}';mesh=bpy.data.meshes.new(name)
  verts=[cv((v.position.x,v.position.y,v.position.z)) for v in m.vertices]
  indices={id(v):i for i,v in enumerate(m.vertices)}
  faces=[[indices[id(v)] for v in reversed(face.vertices)] for face in m.faces]
  mesh.from_pydata(verts,[],faces);mesh.update()
  obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj);objects.append(obj)
  obj['source_fmdl']=model+'.fmdl';obj['source_material']=m.materialInstance.name
  mesh.materials.append(materials[(model,m.materialInstance.name)])
  for ui in range(m.vertexFields.uvCount):
   uv=mesh.uv_layers.new(name=f'UV{ui}')
   for loop in mesh.loops:
    v=m.vertices[loop.vertex_index];uv.data[loop.index].uv=(v.uv[ui].u,1-v.uv[ui].v)
  if m.vertexFields.hasNormal:
   ns=[]
   for loop in mesh.loops:
    n=m.vertices[loop.vertex_index].normal;ns.append(cv((n.x,n.y,n.z)))
   mesh.normals_split_custom_set(ns)
  groups={}
  for vi,v in enumerate(m.vertices):
   for b,w in (v.boneMapping or {}).items():
    if b.name not in groups:groups[b.name]=obj.vertex_groups.new(name=b.name)
    if w>0:groups[b.name].add([vi],w,'REPLACE')
  mod=obj.modifiers.new('PES reference skinning','ARMATURE');mod.object=rig;obj.parent=rig
  if m.materialInstance.name in ['eyeline_SG','collar_ao','fox_eyelash_mat']:
   obj.hide_render=True;obj['missing_common_textures']=True
# Reference only: no generated replacement eyes/face/sculpt.
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=False
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.color=(.13,.13,.13)
allco=[v.co for o in objects for v in o.data.vertices]
mins=[min(v[i] for v in allco) for i in range(3)];maxs=[max(v[i] for v in allco) for i in range(3)]
print('MESH_BOUNDS',mins,maxs,flush=True)
target=Vector((0,-.075,1.70))
def aim(obj,p):obj.rotation_euler=(Vector(p)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(.35,-.45,2.1),10,.5),('Fill',(-.4,-.25,1.8),5,.5),('Rim',(.1,.3,2),12,.4)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
 ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=loc;aim(ob,target)
camdata=bpy.data.cameras.new('Preview_camera');cam=bpy.data.objects.new('Preview_camera',camdata);scene.collection.objects.link(cam);cam.location=(.27,-.65,1.80);camdata.type='ORTHO';camdata.ortho_scale=.43;aim(cam,target);scene.camera=cam
scene.view_settings.view_transform='AgX'
# Package editable original geometry, both UV sets and original skin weights.
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
(ROOT/'conversion-notes.json').write_text(json.dumps({'bounds_blender_meters':{'min':mins,'max':maxs},'missing_common_textures':sorted(set(missing)),'rig':'PES reference; Android retargeting pending','hair_material':'Preview approximation: primary Base_Tex UV0 color/alpha; secondary UV1 texture retained in nodes. FOX two-layer shader not ported.'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'converted'/'Ronaldo_88044950524330_SOURCE.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in objects+[rig]:o.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(ROOT/'converted'/'Ronaldo_88044950524330_SOURCE.fbx'),use_selection=True,add_leaf_bones=False,bake_anim=False,path_mode='COPY',embed_textures=True,axis_forward='-Z',axis_up='Y')
bpy.ops.export_scene.gltf(filepath=str(ROOT/'converted'/'Ronaldo_88044950524330_SOURCE.glb'),export_format='GLB',use_selection=True,export_animations=False)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:
 if o.name.startswith('hair_high_0_'):o.select_set(True)
rig.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(ROOT/'converted'/'Ronaldo_NOODLE_HAIR_ONLY_REFERENCE.fbx'),use_selection=True,add_leaf_bones=False,bake_anim=False,path_mode='COPY',embed_textures=True,axis_forward='-Z',axis_up='Y')
scene.render.filepath=str(ROOT/'converted'/'Ronaldo_source_preview.png');bpy.ops.render.render(write_still=True)
print('SOURCE_CONVERSION_FINISHED',flush=True)
