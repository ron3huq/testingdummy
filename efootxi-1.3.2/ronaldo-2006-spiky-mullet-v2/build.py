import bpy,math,random,json
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
from pathlib import Path
P=Path('/workspace/ronaldo-work/hair-2006-spikes');random.seed(200617)
s=bpy.context.scene;h=bpy.data.objects['hair_high_1_fox_hair_mat'];before=[v.co.copy() for v in h.data.vertices]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
# Preserve all original nape/tail, groom only upper hair into a tight base.
for v,p in zip(h.data.vertices,before):
 x,y,z=p
 w=smooth(1.73,1.785,z)*(1-smooth(-.035,.005,y))
 if not w:continue
 side=smooth(.038,.083,abs(x));v.co.x=x*(1-.12*side*w)
 # Reduce broad flopping cards to a compact base under the upright locks.
 roof=1.803-.020*(abs(x)/.09)**1.7
 v.co.z=z-max(0,z-roof)*.84*w
 v.co.y=y+.003*w
 if y<-.115 and z>1.74:
  fw=smooth(.115,.15,-y)*smooth(1.74,1.77,z);v.co.y+=.012*fw;v.co.z+=.010*fw
h.data.normals_split_custom_set([(0,0,0)]*len(h.data.loops))
for f in h.data.polygons:f.use_smooth=True
# Original skin material remains below hairline. A height mask darkens only scalp,
# never the nape; this prevents the previous full-mesh black override.
scalp=bpy.data.objects['hair_high_0_fox_skin_mat'];scalpmat=scalp.data.materials[0].copy();scalpmat.name='Scalp_only_mask_original_nape';scalp.data.materials[0]=scalpmat
sn=scalpmat.node_tree.nodes;sl=scalpmat.node_tree.links;sb=sn.get('Principled BSDF');st=next(n for n in sn if n.type=='TEX_IMAGE')
geo=sn.new('ShaderNodeNewGeometry');sep=sn.new('ShaderNodeSeparateXYZ');sl.new(geo.outputs['Position'],sep.inputs[0])
mask=sn.new('ShaderNodeMapRange');mask.clamp=True;mask.interpolation_type='SMOOTHERSTEP';mask.inputs['From Min'].default_value=1.775;mask.inputs['From Max'].default_value=1.795;sl.new(sep.outputs['Z'],mask.inputs['Value'])
mix=sn.new('ShaderNodeMixRGB');mix.blend_type='MIX';sl.new(mask.outputs['Result'],mix.inputs[0]);sl.new(st.outputs['Color'],mix.inputs[1]);mix.inputs[2].default_value=(.009,.006,.004,1);sl.new(mix.outputs[0],sb.inputs['Base Color']);sb.inputs['Roughness'].default_value=.8;sb.inputs['Specular IOR Level'].default_value=.08
bpy.context.view_layer.update();bvh=BVHTree.FromObject(scalp,bpy.context.evaluated_depsgraph_get())
# Hair cards use texture alpha and a restrained diffuse shader in Blender.
im=bpy.data.images['hair_parts_bsm_alp.png'];im.alpha_mode='STRAIGHT'
m=h.data.materials[0];nodes=m.node_tree.nodes;links=m.node_tree.links;bs=nodes.get('Principled BSDF');tex=next(n for n in nodes if n.type=='TEX_IMAGE')
bs.inputs['Roughness'].default_value=.9;bs.inputs['Specular IOR Level'].default_value=0
mul=nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.35,.35,.35,1);links.new(tex.outputs['Color'],mul.inputs[1]);links.new(mul.outputs[0],bs.inputs['Base Color'])
# 3D wet-look separated spike bundles, all individually tapered, no hanging bangs.
materials=[]
for k,c in enumerate([(.012,.009,.006),(.020,.015,.009),(.029,.022,.014)]):
 mat=bpy.data.materials.new('Spike_strands_%d'%k);mat.use_nodes=True;b=mat.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=.42;b.inputs['Specular IOR Level'].default_value=.23;materials.append(mat)
cu=bpy.data.curves.new('SPIKY_TOP_EDITABLE','CURVE');cu.dimensions='3D';cu.bevel_depth=.00022;cu.bevel_resolution=1
for m in materials:cu.materials.append(m)
count=0
for yi,y in enumerate([-.143+i*.011 for i in range(14)]):
 for xi,x in enumerate([-.065+i*.010 for i in range(14)]):
  ellipse=(x/.089)**2+((y+.060)/.115)**2
  if ellipse>.95:continue
  x+=random.uniform(-.004,.004);y0=y+random.uniform(-.004,.004)
  hit,norm,idx,dist=bvh.ray_cast(Vector((x,y0,2)),Vector((0,0,-1)))
  if hit is None or hit.z<1.75:continue
  z=hit.z+.001
  # Front row roots are at hairline, lifted back/up; center has the tallest crest.
  lift=random.uniform(.012,.025)*(1-.35*abs(x)/.07)
  if yi<3:lift+=.003
  root=Vector((x,y0,z));tip=root+Vector((random.uniform(.006,.016),random.uniform(-.002,.010),lift))
  ctrl1=root+Vector((.003,-.005,lift*.60));ctrl2=tip+Vector((-.004,-.003,.002))
  for j in range(26):
   spread=Vector((random.uniform(-.0045,.0045),random.uniform(-.004,.004),random.uniform(-.0015,.0015)))
   endoffset=Vector((random.uniform(-.0009,.0009),random.uniform(-.0009,.0009),random.uniform(-.002,.002)))
   sp=cu.splines.new('POLY');sp.points.add(11);sp.material_index=random.choices([0,1,2],[.7,.25,.05])[0]
   for q,pt in enumerate(sp.points):
    t=q/11;pos=(1-t)**3*root+3*(1-t)**2*t*ctrl1+3*(1-t)*t*t*ctrl2+t**3*tip
    pos+=spread*(1-t)**1.4+endoffset*t
    pos.x+=.00055*math.sin(t*math.pi*2+xi*.6)*math.sin(t*math.pi)
    pt.co=(*pos,1);pt.radius=max(.015,(1-t)**.6)*random.uniform(.8,1.15)
  count+=1
# A close front row follows the hairline so the scalp is covered by actual strands.
for ci in range(27):
 x=-.065+ci*.005;edge=abs(x)/.07
 root=Vector((x,-.155+.017*edge**2,1.772+.009*(1-edge**1.6)))
 tip=root+Vector((.008, .026, random.uniform(.022,.031)))
 p1=root+Vector((.001,-.001,.014));p2=tip+Vector((-.004,-.005,.004))
 for j in range(36):
  spread=Vector((random.uniform(-.0034,.0034),random.uniform(-.0012,.0012),random.uniform(-.001,.001)))
  sp=cu.splines.new('POLY');sp.points.add(11);sp.material_index=0 if j%5 else 1
  for qi,pt in enumerate(sp.points):
   t=qi/11;v=(1-t)**3*root+3*(1-t)**2*t*p1+3*(1-t)*t*t*p2+t**3*tip+spread*(1-t)**1.3
   pt.co=(*v,1);pt.radius=max(.02,(1-t)**.65)*random.uniform(.85,1.1)
 count+=1
ob=bpy.data.objects.new('EDIT_Spiky_top_and_front',cu);s.collection.objects.link(ob);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob=bpy.context.object
rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID'];ob.parent=rig;g=ob.vertex_groups.new(name='sk_head');g.add(list(range(len(ob.data.vertices))),1,'REPLACE');mod=ob.modifiers.new('PES reference skinning','ARMATURE');mod.object=rig
for f in ob.data.polygons:f.use_smooth=True
protected=[i for i,p in enumerate(before) if p.z<=1.73 or p.y>=.005]
assert all(h.data.vertices[i].co==before[i] for i in protected)
(P/'report.json').write_text(json.dumps({'style':'upright separated spikes, shorter sides, original mullet','spike_bundles':count,'protected_tail_vertices':len(protected),'tail_coordinates_unchanged':True,'nape_skin_material':'original skin texture below 1.775m, scalp-only height mask above','android_game_ready':False},indent=2))
# Hide reference rig/light gizmos in viewport, retain armature for editing.
rig.hide_set(True)
for o in bpy.data.objects:
 if o.type in ['LIGHT','CAMERA']:o.hide_set(True)
for scr in bpy.data.screens:
 for a in scr.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.overlay.show_overlays=False;a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_location=(0,-.06,1.72);a.spaces.active.region_3d.view_distance=.42
   a.spaces.active.region_3d.view_rotation=Quaternion((1,0,0),math.radians(82))
s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100
bpy.ops.object.select_all(action='DESELECT');h.select_set(True);bpy.context.view_layer.objects.active=h
s['hair_edit']='Spiky short front/top + unchanged mullet. Original nape skin material restored.'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'Ronaldo_2006_SPIKY_MULLET_V2.blend'))
cam=s.camera
for label,loc in [('front',(0,-.70,1.77)),('three-quarter',(.27,-.65,1.80)),('nape-side',(.65,.03,1.74)),('back',(0,.65,1.73))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37
 s.render.filepath=str(P/(label+'.png'));bpy.ops.render.render(write_still=True)
print('SPIKY_MULLET_V2_COMPLETE',count)
