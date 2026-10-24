import bpy,json,math,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/ronaldo-work');O=R/'hair-repair-v3'
bpy.ops.wm.open_mainfile(filepath=str(R/'input-0/Ronaldo_2006_EDIT.blend'))
def snap(o):
 return {'co':np.array([tuple(v.co) for v in o.data.vertices]),'polys':[tuple(p.vertices) for p in o.data.polygons],'uv':[np.array([tuple(q.uv) for q in u.data]) for u in o.data.uv_layers],'groups':[g.name for g in o.vertex_groups],'weights':[[(q.group,q.weight) for q in v.groups] for v in o.data.vertices],'normals':np.array([tuple(q.vector) for q in o.data.corner_normals])}
original={o.name:snap(o) for o in bpy.data.objects if o.type=='MESH'}
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
original_face_pixels=np.array(bpy.data.images['face_bsm_alp.png'].pixels[:],np.float32).reshape(1024,1024,4)
for year in ['2017','2014']:
 p=O/year;bpy.ops.wm.open_mainfile(filepath=str(p/f'Ronaldo_{year}_REPAIR_V3.blend'));rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID'];report={'year':year,'blender_reopen':bpy.app.version_string,'android_verified':False,'original_cap_geometry_uv_normals_weights_exact':False,'face_topology_uv_weights_preserved':False,'all_new_textures_packed_and_png_hashes_match':False,'reference_rig_weights_valid':False}
 cap=bpy.data.objects['SCALP_NATIVE_2006_BAKED_DONOR_COLOR'];a=snap(cap);b=original['hair_high_0_fox_skin_mat']
 for k in ['polys','groups','weights']:assert a[k]==b[k],k
 for k in ['co','normals']:assert np.array_equal(a[k],b[k]),k
 assert len(a['uv'])==len(b['uv'])
 for x,y in zip(a['uv'],b['uv']):assert np.array_equal(x,y)
 report['original_cap_geometry_uv_normals_weights_exact']=True
 moves={}
 for name,old in original.items():
  if not name.startswith('face_high'):continue
  ob=bpy.data.objects[name];new=snap(ob)
  for k in ['polys','groups','weights']:assert new[k]==old[k],(name,k)
  for x,y in zip(new['uv'],old['uv']):assert np.array_equal(x,y)
  delta=np.linalg.norm(new['co']-old['co'],axis=1);moves[name]=float(delta.max())
  if year=='2014' or name not in ['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat']:assert delta.max()==0,name
  else:assert .001<delta.max()<.008,(name,delta.max())
  assert np.isfinite(new['normals']).all()
 report['face_topology_uv_weights_preserved']=True;report['max_face_vertex_displacements_m']=moves
 # Protect the original central face from the temple texture cleanup.
 ob=bpy.data.objects['face_high_2_fox_skin_mat'];im=next(n.image for n in ob.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and 'Temples_Clean' in n.image.name);a=np.array(im.pixels[:],np.float32).reshape(im.size[1],im.size[0],4);errors=[]
 for loop in ob.data.loops:
  pos=ob.data.vertices[loop.vertex_index].co
  if abs(pos.x)<.04 and pos.y<-.145 and pos.z<1.735:
   q=ob.data.uv_layers[0].data[loop.index].uv;x=min(1023,max(0,round(q.x*1023)));y=min(1023,max(0,round(q.y*1023)));errors.append(float(np.abs(a[y,x,:3]-original_face_pixels[y,x,:3]).max()))
 assert errors and max(errors)<.005,max(errors)
 report['protected_nose_lips_central_face_texture_max_error']=max(errors)
 hashes={};usedimages=set()
 for ob in bpy.data.objects:
  if ob.type!='MESH':continue
  for mat in ob.data.materials:
   if mat and mat.use_nodes:
    for node in mat.node_tree.nodes:
     if node.type=='TEX_IMAGE' and node.image:usedimages.add(node.image)
 for im in usedimages:
  assert im.packed_file,im.name
  if '_BAKED' in im.name:
   path=Path(im.filepath_raw);assert path.is_file(),path
   packed=hashlib.sha256(bytes(im.packed_file.data)).hexdigest();external=hashlib.sha256(path.read_bytes()).hexdigest();assert packed==external,(im.name,'packed mismatch');hashes[im.name]=packed
 assert len(hashes)>=4
 report['all_new_textures_packed_and_png_hashes_match']=True;report['baked_texture_sha256']=hashes
 for ob in [cap]+[o for o in bpy.data.objects if o.name.startswith(year+'_AUTHORED_HAIR')]:
  assert any(m.type=='ARMATURE' and m.object==rig for m in ob.modifiers),ob.name
  for v in ob.data.vertices:
   assert all(math.isfinite(q) for q in v.co)
   assert abs(sum(g.weight for g in v.groups)-1)<.002,(ob.name,v.index)
   for g in v.groups:assert ob.vertex_groups[g.group].name in rig.data.bones,(ob.name,g.group)
 report['reference_rig_weights_valid']=True
 report['total_source_mesh_vertices']=sum(len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH')
 if year=='2017':
  f=FmdlFile();f.readFile(str(R/'new-hair-sources/2017/fpk/hair_high.fmdl'));source=f.meshes[0];ob=bpy.data.objects['2017_AUTHORED_HAIR_0'];assert len(ob.data.vertices)==len(source.vertices)
  for v,q in zip(ob.data.vertices,source.vertices):assert (v.co-Vector((q.position.x,-q.position.z,q.position.y))).length<1e-7
  for ui in range(source.vertexFields.uvCount):
   for loop in ob.data.loops:
    q=source.vertices[loop.vertex_index].uv[ui];uv=ob.data.uv_layers[ui].data[loop.index].uv;assert abs(uv.x-q.u)<1e-6 and abs(uv.y-(1-q.v))<1e-6
  report['supplied_2017_hair_geometry_and_two_uvs_preserved']=True

 assert not any(o.name.startswith(('EDIT_Spiky','EDIT_2014_Swept','2014_Temple_Zigzag','2014_Side_Part')) for o in bpy.data.objects)
 build=json.loads((p/'build-report.json').read_text())
 if year=='2014':
  assert build['shaved_line_texture_pixels']>500
  assert sum(len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH')<20000
  report['shaved_lines_in_baked_texture_no_floating_line_meshes']=True
 # Exercise actual Blender deformation once; never save the posed scene.
 bone=rig.pose.bones['sk_head'];bone.rotation_mode='XYZ';bone.rotation_euler.y=.08;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for ob in [cap]+[o for o in bpy.data.objects if o.name.startswith(year+'_AUTHORED_HAIR')]:
  ev=ob.evaluated_get(dg)
  assert all(all(math.isfinite(q) for q in v.co) for v in ev.data.vertices)
 report['reference_head_pose_finite']=True
 (p/'validation.json').write_text(json.dumps(report,indent=2));print('REPAIR_V3_VALIDATION_PASS',year,flush=True)
