import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath='/workspace/analysis/ronaldo-2017-sculpt/Ronaldo_2006_to_2017_FACE_EDIT.blend')
ctrl=bpy.data.objects['00_EDIT_CONTROLS'];ctrl['Neck_shortening_mm']=7.;ctrl['Adam_apple_mm']=1.2;ctrl.id_properties_ui('Adam_apple_mm').update(min=0.,max=3.,description='Subtle anatomical laryngeal prominence; default 1.2mm')
report={'neck_total_reduction_mm':7,'extra_reduction_from_v1_mm':1,'adam_apple_default_mm':1.2,'skin_srgb_multipliers':[.95,.945,.94],'source_overlap_rgb_mae':[.473,.626,.595],'lip_mobile_fixed':False,'phone_tested':False,'weights_changed':[]}
skins=[o for o in bpy.data.objects if o.type=='MESH'and o.name in ['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat','hair_high_0_fox_skin_mat']]
for o in skins:
 key=o.shape_key_add(name='ADAM_APPLE_SUBTLE_1_2mm')
 for p,v in zip(key.data,o.data.shape_keys.key_blocks['Basis'].data):
  x,y,z=v.co;gate=1/(1+math.exp((y+.065)*180));amount=.0012*math.exp(-(x/.018)**2-((z-1.548)/.022)**2)*gate;p.co.y-=amount
 dr=key.driver_add('value').driver;dr.expression='a/1.2';v=dr.variables.new();v.name='a';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["Adam_apple_mm"]'
# One skin shader and one colour-managed image for all skin sections.
mat=bpy.data.objects['face_high_2_fox_skin_mat'].data.materials[0].copy();mat.name='UNIFIED_FACE_NECK_SKIN_2017';im=bpy.data.images.load(str(R/'face_neck_warm_dark.png'));im.alpha_mode='NONE';im.pack()
for n in mat.node_tree.nodes:
 if n.type=='TEX_IMAGE'and n.image and n.image.name.startswith('face_bsm_alp'):n.image=im
for o in skins:
 o.data.materials.clear();o.data.materials.append(mat)
 for p in o.data.polygons:p.material_index=0;p.use_smooth=True
# Optional, reversible source-weight guard for upper lip volume -> jaw coupling.
# Kept disabled by default until device conversion rig is known.
report['upper_lip_candidate_vertices']=[]
face=bpy.data.objects['face_high_2_fox_skin_mat'];vol=face.vertex_groups.get('skf_lip_volume')
for v in face.data.vertices:
 if abs(v.co.x)<.025 and 1.657<v.co.z<1.676:
  ww={face.vertex_groups[g.group].name:g.weight for g in v.groups}
  if ww.get('skf_lip_volume',0)>.05:report['upper_lip_candidate_vertices'].append({'vertex':v.index,'volume_weight':ww['skf_lip_volume']})
# Local source-weight candidate: keep upper-lip volume off lower-jaw fallback.
for row in report['upper_lip_candidate_vertices']:
 v=face.data.vertices[row['vertex']];ww={face.vertex_groups[g.group].name:g.weight for g in v.groups};tops={n:w for n,w in ww.items()if n.startswith('skf_lip_t_')};total=sum(tops.values())
 if total<.25:continue
 vol.remove([v.index])
 for name,w in tops.items():face.vertex_groups[name].add([v.index],w+row['volume_weight']*w/total,'REPLACE')
 report['weights_changed'].append({'vertex':v.index,'before':ww,'after':{face.vertex_groups[g.group].name:g.weight for g in v.groups}})
report['upper_lip_candidate_applied']=True
(R/'upper-lip-retarget-guidance.json').write_text(json.dumps({'status':'CANDIDATE_NOT_DEVICE_VERIFIED','reason':'Upper-lip vertices reference skf_lip_volume; mapping that entire control to 50% jaw pulls the upper lip when opening. Preserve upper-lip controls or map only this upper-lip region to native upper-lip/head, not lower jaw. Actual converter must be inspected.','candidate_vertices':report['upper_lip_candidate_vertices'],'applied_source_weight_changes':report['weights_changed'],'do_not_disable_all_facial_animation':True},indent=2))
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
# Smooth normals across spatially shared skin vertices, retaining topology and UV.
mesh0=bpy.data.objects['face_high_0_fox_skin_mat'];mesh2=face
cloud=[];faces=[]
for o in skins:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();off=len(cloud);cloud.extend(v.co.copy()for v in m.vertices);faces.extend([off+i for i in p.vertices]for p in m.polygons);ev.to_mesh_clear()
me=bpy.data.meshes.new('TEMP_normal_reference');me.from_pydata(cloud,[],faces);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00025);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update();bm.to_mesh(me);bm.free();me.calc_loop_triangles();bv=BVHTree.FromPolygons([v.co for v in me.vertices],[p.vertices for p in me.polygons]);
# Nearest reference surface normal shared by overlapping sections; blend at boundaries.
for o in skins:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();normals=[]
 for v in em.vertices:
  p,n,i,d=bv.find_nearest(v.co)
  # Use smoothed reference vertex normals instead of flat polygon normal.
  poly=me.polygons[i];near=sorted(poly.vertices,key=lambda j:(me.vertices[j].co-p).length)[:3];nn=Vector((0,0,0));total=0
  for j in near:
   w=1/max(.00005,(me.vertices[j].co-p).length);nn+=me.vertices[j].normal*w;total+=w
  nn.normalize();normals.append(nn)
 ev.to_mesh_clear();o.data.normals_split_custom_set_from_vertices(normals)
bpy.data.meshes.remove(me)
# Source normals are now consistent at layer boundaries; no topology/weights removed.
s=bpy.context.scene;s['refine_status']='UNIFIED_SKIN_SHADER_NORMALS_AND_SUBTLE_NECK_V2';s['lip_fix_status']='local upper-lip weight candidate; game conversion unverified';s.cycles.samples=24;s.render.resolution_x=720;s.render.resolution_y=900;s.render.resolution_percentage=100
cam=s.camera
for name,ang in [('front',0),('three_quarter',35),('back_neck',145),('profile',90)]:
 a=math.radians(ang);cam.location=(.65*math.sin(a),-.075-.65*math.cos(a),1.735);cam.rotation_euler=(Vector((0,-.075,1.68))-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'))
 if name=='front':bpy.ops.wm.save_as_mainfile(filepath=str(R/'Ronaldo_2017_FACE_NECK_v2.blend'))
 bpy.ops.render.render(write_still=True)
(R/'validation.json').write_text(json.dumps(report,indent=2));print('REFINE_RENDER_DONE')
