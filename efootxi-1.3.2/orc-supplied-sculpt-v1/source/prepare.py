import bpy,bmesh,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
R=Path(__file__).parent
bpy.ops.wm.open_mainfile(filepath=str(R/'ORC_INSPECTION.blend'))
for ob in list(bpy.data.objects):
 if ob.type!='MESH':bpy.data.objects.remove(ob,do_unlink=True)
low=bpy.data.objects['ORC_SUPPLIED_SCULPT'];low.name='ORC_GAME_LOD'
shift=Vector((-.0047,.0253,.1072))
for v in low.data.vertices:v.co+=shift
bpy.context.view_layer.objects.active=low;low.select_set(True)
m=low.modifiers.new('Mobile LOD preserve supplied silhouette','DECIMATE');m.ratio=90000/184133;m.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=m.name)
# Exact same translation, with no nonuniform deformation, for the supplied sculpt.
with bpy.data.libraries.load(str(R/'ORC_SOURCE_FULL.blend'),link=False) as(a,b):b.objects=['ORC_SUPPLIED_SCULPT']
high=b.objects[0];bpy.context.scene.collection.objects.link(high);high.name='ORC_SUPPLIED_FULL_SCULPT'
for v in high.data.vertices:v.co+=shift

def srgb(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
def material(name,rgb,rough=.65):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(srgb(c)for c in rgb)+(1,);bs.inputs['Roughness'].default_value=rough;bs.inputs['Specular IOR Level'].default_value=.25;mat.diffuse_color=tuple(srgb(c)for c in rgb)+(1,);return mat
skin=material('ORC olive skin - authored colour - source had no texture',(.36,.42,.26));bone=material('Original sculpt tusks - ivory',(.78,.72,.55),.48)
eyes=[]
for sign in [-1,1]:
 center=Vector((sign*.03305, -.16035,1.6063))+shift;front=center+Vector((0,-.0174,.001))
 mat=material('Original sculpt eye '+str(sign),(.58,.54,.40),.3);n=mat.node_tree.nodes;l=mat.node_tree.links;g=n.new('ShaderNodeNewGeometry');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=front;l.new(g.outputs['Position'],dist.inputs[0]);r=n.new('ShaderNodeValToRGB');l.new(dist.outputs['Value'],r.inputs[0]);cr=r.color_ramp
 cr.elements.remove(cr.elements[1]);cr.elements[0].position=0;cr.elements[0].color=(.0015,.001,.0005,1)
 for pos,rgb in [(.0027,(.008,.006,.002)),(.0034,(.27,.20,.025)),(.0062,(.16,.11,.012)),(.007,(.035,.025,.007)),(.0075,(.58,.54,.40))]:
  e=cr.elements.new(pos);e.color=tuple(srgb(c)for c in rgb)+(1,)
 l.new(r.outputs[0],n.get('Principled BSDF').inputs['Base Color']);eyes.append(mat)
mats=[skin,bone,*eyes]
# Connected components select existing tusks and existing eyeballs. No extra geometry.
def assign(obj):
 mesh=obj.data;nv=len(mesh.vertices);ed=np.empty(len(mesh.edges)*2,dtype=np.int32);mesh.edges.foreach_get('vertices',ed);ed=ed.reshape(-1,2);graph=coo_matrix((np.ones(len(ed),dtype=np.uint8),(ed[:,0],ed[:,1])),shape=(nv,nv)).tocsr();count,labels=connected_components(graph,directed=False);coords=np.empty(nv*3,np.float32);mesh.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);choice=np.zeros(count,np.int32);report=[]
 for ci in range(count):
  ids=np.flatnonzero(labels==ci);lo=coords[ids].min(axis=0);hi=coords[ids].max(axis=0);center=(lo+hi)/2
  if len(ids)<nv*.05:
   if center[2]>1.68:choice[ci]=2 if center[0]<0 else 3
   else:choice[ci]=1
  report.append({'vertices':len(ids),'bounds':[lo.tolist(),hi.tolist()],'material':int(choice[ci])})
 mesh.materials.clear()
 for mat in mats:mesh.materials.append(mat)
 # Face first vertex is always in the same connected component.
 starts=np.empty(len(mesh.polygons),np.int32);mesh.polygons.foreach_get('loop_start',starts);vi=np.empty(len(mesh.loops),np.int32);mesh.loops.foreach_get('vertex_index',vi);mi=choice[labels[vi[starts]]];mesh.polygons.foreach_set('material_index',mi);mesh.polygons.foreach_set('use_smooth',np.ones(len(mesh.polygons),dtype=bool));mesh.update();print('COMPONENTS',obj.name,report,flush=True);return report
reports={'source_components':assign(high),'game_components':assign(low)}
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.use_denoising=False;s.cycles.samples=16
# UV atlas only on the game LOD. Supplied sculpt remains at its original topology.
bpy.ops.object.select_all(action='DESELECT');low.select_set(True);bpy.context.view_layer.objects.active=low

for olduv in list(low.data.uv_layers):low.data.uv_layers.remove(olduv)
uv=low.data.uv_layers.new(name='OrcAtlas');low.data.uv_layers.active=uv;uv.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.2,island_margin=.004);bpy.ops.object.mode_set(mode='OBJECT')
# Selected-to-active source bake, including the sculpt's small wrinkles/cavities.
def bake(name,kind,filepath):
 im=bpy.data.images.new(name,2048,2048,alpha=True);im.generated_color=(.05,.05,.05,1)
 for mat in mats:
  t=mat.node_tree.nodes.new('ShaderNodeTexImage');t.image=im;mat.node_tree.nodes.active=t
 high.select_set(True);low.select_set(True);bpy.context.view_layer.objects.active=low;s.render.bake.use_selected_to_active=True;s.render.bake.cage_extrusion=.003;s.render.bake.max_ray_distance=.012;s.render.bake.margin=8
 if kind=='DIFFUSE':s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True
 if kind=='AO':s.world=bpy.data.worlds.new('AO World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[1].default_value=.15
 bpy.ops.object.bake(type=kind);im.filepath_raw=str(R/filepath);im.file_format='PNG';im.save();im.pack();print('BAKED',kind,flush=True);return im
color=bake('Orc source material diffuse','DIFFUSE','diffuse.png')
ao=bake('Orc high sculpt cavity','AO','ao.png')
normal=bake('Orc high sculpt tangent normals','NORMAL','normal.png');normal.colorspace_settings.name='Non-Color'
# Keep the full sculpt separately, so opening the game scene stays practical.
high.hide_render=False;high.hide_set(False);low.hide_render=True;low.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'ORC_FULL_SCULPT.blend'),compress=True)
bpy.data.objects.remove(high,do_unlink=True);low.hide_render=False;low.hide_set(False)
reports.update({'source_vertices':3684505,'source_faces':3682944,'game_vertices_before_uv_split':len(low.data.vertices),'game_faces':len(low.data.polygons),'uniform_scale':.44/(2.9096182584762573),'translation_from_inspection':list(shift),'source_geometry_resculpted':False,'texture_origin':'authored olive skin and ivory tusks; archive contains no source textures','expression':'fixed supplied sculpt expression; head and neck animate','phone_tested':False})
(R/'preparation-validation.json').write_text(json.dumps(reports,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'ORC_BAKED_STAGE.blend'),compress=True)
print('PREPARED',reports,flush=True)
