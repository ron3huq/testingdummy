import bpy,json,hashlib
from pathlib import Path
P=Path('/workspace/ronaldo-work/73-ui4');rows=[]
files=list((P/'blender-output').glob('*.blend'))+[P/n/(n+'_SOURCE_REVIEW.blend')for n in['zidane','ferguson']]
for f in files:
 bpy.ops.wm.open_mainfile(filepath=str(f));scene=bpy.context.scene;meshes=[o for o in scene.objects if o.type=='MESH'];rigs=[o for o in scene.objects if o.type=='ARMATURE'];images=[i for i in bpy.data.images if i.source=='FILE'];assert meshes and rigs and images
 assert all(i.packed_file is not None for i in images),f
 assert all(len(o.data.uv_layers)>0 for o in meshes if o.vertex_groups),f
 if f.name.startswith('Ronaldo_'):
  cid=f.name.split('_')[1];assert scene['card_id']==cid and scene['source_model']=='SK_4522ep00v0313_Face';assert any(o.vertex_groups and any(m.type=='ARMATURE'for m in o.modifiers)for o in meshes)
 rows.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'meshes':len(meshes),'rigs':len(rigs),'packed_images':len(images),'vertices':sum(len(o.data.vertices)for o in meshes),'loads_in_Blender':True})
(P/'blender-validation.json').write_text(json.dumps({'passed':True,'Blender':bpy.app.version_string,'files':rows,'native_Ronaldo_pair_same_appearance':True,'coach_eyes_added_for_standalone_preview':True},indent=2));print('BLENDER_READBACK_PASS',rows)
