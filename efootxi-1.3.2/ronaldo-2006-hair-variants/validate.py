import bpy,json,sys,math,hashlib
from pathlib import Path
R=Path('/workspace/ronaldo-work');P=R/'new-hair-sources';sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
bpy.ops.wm.open_mainfile(filepath=str(R/'input-0/Ronaldo_2006_EDIT.blend'))
def snap(o):return {'co':[tuple(v.co) for v in o.data.vertices],'tri':[list(p.vertices) for p in o.data.polygons],'uv':[[list(x.uv) for x in u.data] for u in o.data.uv_layers],'weights':[[(g.group,g.weight) for g in v.groups] for v in o.data.vertices],'mat':[m.name for m in o.data.materials]}
original={o.name:snap(o) for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('face_high')}
original_cap=snap(bpy.data.objects['hair_high_0_fox_skin_mat'])
f=FmdlFile();f.readFile(str(P/'2017/fpk/hair_high.fmdl'));hair=f.meshes[0]
for label,folder,file in [('hybrid','hybrid-2006-2017','Ronaldo_2006_FACE_2017_HAIR.blend'),('2014','2014-blender','Ronaldo_2014_PHOTO_HAIR_2006_FACE.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(P/folder/file));rig=bpy.data.objects['PES_REFERENCE_NOT_ANDROID'];report={'variant':label,'blender':bpy.app.version_string,'face_2006_geometry_uv_weights_materials_identical':False,'packed_images':False,'new_mesh_weights_valid':False,'android_verified':False,'missing_common_eye_textures_in_original':True}
 for name,before in original.items():assert snap(bpy.data.objects[name])==before,name
 report['face_2006_geometry_uv_weights_materials_identical']=True
 current_cap=snap(bpy.data.objects['hair_high_0_fox_skin_mat'])
 for key in ['co','tri','weights']:assert current_cap[key]==original_cap[key]
 report['original_2006_scalp_neck_geometry_weights_unchanged']=True
 assert not any(o.name.startswith('EDIT_Spiky') or o.name.startswith('EDIT_Front_lock') for o in bpy.data.objects)
 for im in bpy.data.images:
  if im.source=='FILE':assert im.packed_file,im.name
 report['packed_images']=True
 objs=[o for o in bpy.data.objects if o.type=='MESH' and (o.name=='HAIR_2017_FROM_USER_RAR' if label=='hybrid' else o.name in ['2014_CROPPED_HAIR_CAP','2014_HAIR_BASE_NOT_FACE','EDIT_2014_Swept_Hair','2014_Side_Part','2014_Temple_Zigzag_A','2014_Temple_Zigzag_B'])]
 assert objs
 for ob in objs:
  assert any(m.type=='ARMATURE' and m.object==rig for m in ob.modifiers),ob.name
  for v in ob.data.vertices:
   assert all(math.isfinite(x) for x in v.co)
   assert abs(sum(g.weight for g in v.groups)-1)<.002,(ob.name,v.index)
   for g in v.groups:assert ob.vertex_groups[g.group].name in rig.data.bones,(ob.name,g.group)
 report['new_mesh_weights_valid']=True
 if label=='hybrid':
  ob=objs[0];assert len(ob.data.vertices)==len(hair.vertices)
  for i,v in enumerate(ob.data.vertices):
   source=hair.vertices[i];expect=(source.position.x,-source.position.z,source.position.y);assert max(abs(v.co[k]-expect[k]) for k in range(3))<1e-7
   assert {ob.vertex_groups[g.group].name:round(g.weight,6) for g in v.groups}=={b.name:round(w,6) for b,w in source.boneMapping.items() if w>0}
  idx={id(v):i for i,v in enumerate(hair.vertices)};assert [list(p.vertices) for p in ob.data.polygons]==[[idx[id(v)] for v in reversed(ff.vertices)] for ff in hair.faces]
  for ui in range(hair.vertexFields.uvCount):
   uv=ob.data.uv_layers[f'UV{ui}']
   for loop in ob.data.loops:
    src=hair.vertices[loop.vertex_index].uv[ui];a=uv.data[loop.index].uv;assert abs(a.x-src.u)<1e-6 and abs(a.y-(1-src.v))<1e-6
  report['hair_2017_source_geometry_two_uvs_weights_exact']=True
 (P/folder/'validation.json').write_text(json.dumps(report,indent=2));print('PASS',label,report)
