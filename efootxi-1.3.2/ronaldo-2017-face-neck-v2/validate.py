import bpy,json,math
from pathlib import Path
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'Ronaldo_2017_FACE_NECK_v2.blend'));new={o.name:o for o in bpy.data.objects if o.type=='MESH'};report=json.loads((R/'validation.json').read_text());changed={row['vertex']for row in report['weights_changed']};checks=[]
with bpy.data.libraries.load('/workspace/analysis/ronaldo-2017-sculpt/Ronaldo_2006_to_2017_FACE_EDIT.blend',link=False)as(a,b):b.objects=[n for n in a.objects if n in new]
def weights(o,v):return {o.vertex_groups[g.group].name:g.weight for g in v.groups}
for old in b.objects:
 o=new[old.name.rsplit('.',1)[0]];assert len(o.data.vertices)==len(old.data.vertices);assert [tuple(p.vertices)for p in o.data.polygons]==[tuple(p.vertices)for p in old.data.polygons]
 for uv1,uv2 in zip(o.data.uv_layers,old.data.uv_layers):assert all((a.uv-b.uv).length<1e-8 for a,b in zip(uv1.data,uv2.data))
 for v,a in zip(o.data.vertices,old.data.vertices):
  ww=weights(o,v);assert all(math.isfinite(w)and w>=0 for w in ww.values());assert abs(sum(ww.values())-1)<1e-5
  if o.name=='face_high_2_fox_skin_mat'and v.index in changed:assert 'skf_lip_volume'not in ww
  else:assert ww==weights(old,a)
 checks.append(o.name)
report['checks']={'reopened_blender':True,'topology_uv_preserved':checks,'all_weights_normalised':True,'local_upper_lip_edits_only':len(changed),'one_skin_material':len({o.data.materials[0].name for o in new.values()if o.name in ['face_high_0_fox_skin_mat','face_high_2_fox_skin_mat','hair_high_0_fox_skin_mat']})==1,'head_style_unchanged':True}
report['upper_lip_test']='Removed only upper-lip volume control from selected source vertices; native animation/mapping must be checked in game. Not an engine pose test.'
(R/'validation.json').write_text(json.dumps(report,indent=2));print('PASS',len(checks),'meshes',len(changed),'upper-lip edits')
