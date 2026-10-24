import bpy,numpy as np
from pathlib import Path
from mathutils import Vector
P=Path('/workspace/ronaldo-work/hair-repair-v3/2014')
# Recolour directly from supplied source texture, retaining authored alpha.
src=bpy.data.images.load('/workspace/ronaldo-work/input-2013/converted/hair_parts_bsm_alp.png',check_existing=False);src.alpha_mode='CHANNEL_PACKED';a=np.array(src.pixels[:],np.float32).reshape(src.size[1],src.size[0],4);lum=a[:,:,:3].mean(axis=2);a[:,:,:3]=np.array([.065,.045,.030])+lum[:,:,None]*np.array([.140,.100,.060]);src.pixels.foreach_set(a.ravel());src.name='2014_Hair_Dark_BAKED';src.filepath_raw=str(P/'2014_Hair_Dark_BAKED.png');src.file_format='PNG';src.save();src.pack()
for m in bpy.data.materials:
 if not m.name.startswith('2014_Hair_Material_'):continue
 n=m.node_tree.nodes;l=m.node_tree.links;old=n.get('Principled BSDF');tex=next(x for x in n if x.type=='TEX_IMAGE');tex.image=src
 diffuse=n.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Roughness'].default_value=.6;l.new(tex.outputs['Color'],diffuse.inputs['Color']);trans=n.new('ShaderNodeBsdfTransparent');cut=n.new('ShaderNodeMath');cut.operation='GREATER_THAN';cut.inputs[1].default_value=.34;l.new(tex.outputs['Alpha'],cut.inputs[0]);mix=n.new('ShaderNodeMixShader');l.new(cut.outputs[0],mix.inputs[0]);l.new(trans.outputs[0],mix.inputs[1]);l.new(diffuse.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
s=bpy.context.scene;s.cycles.samples=24
for label,loc in [('front',(0,-.70,1.77)),('right',(-.65,-.04,1.74)),('left',(.65,-.04,1.74)),('back',(0,.65,1.73)),('three-quarter',(-.27,-.65,1.80))]:
 cam=s.camera;cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37;s.render.filepath=str(P/(label+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Ronaldo_2014_REPAIR_V3.blend'))
print('2014_MASKED_HAIR_PASS')
