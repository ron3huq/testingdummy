import bpy,json,math
from pathlib import Path
R=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(R/'Ronaldo_2006_to_2017_FACE_EDIT.blend'))
objs={o.name:o for o in bpy.data.objects if o.type=='MESH'}
with bpy.data.libraries.load('/workspace/analysis/ronaldo-2006-viewer/converted/Ronaldo_2006_EDIT.blend',link=False)as (a,b):b.objects=[n for n in a.objects if n in objs]
checks=[]
for old in b.objects:
 new=objs[old.name.rsplit('.',1)[0]]if old.name not in objs else objs[old.name]
 assert len(old.data.vertices)==len(new.data.vertices)
 assert [tuple(p.vertices)for p in old.data.polygons]==[tuple(p.vertices)for p in new.data.polygons]
 assert all((a.co-b.co).length<1e-8 for a,b in zip(old.data.vertices,new.data.shape_keys.key_blocks['Basis'].data))
 for a,b in zip(old.data.uv_layers,new.data.uv_layers):assert all((x.uv-y.uv).length<1e-8 for x,y in zip(a.data,b.data))
 def weights(o):
  names={g.index:g.name for g in o.vertex_groups};return [{names[g.group]:g.weight for g in v.groups}for v in o.data.vertices]
 assert weights(old)==weights(new)
 checks.append(new.name);bpy.data.objects.remove(old,do_unlink=True)
ctrl=bpy.data.objects.new('00_EDIT_CONTROLS',None);bpy.context.scene.collection.objects.link(ctrl);ctrl.empty_display_size=.025;ctrl.location=(.15,0,1.8);ctrl.hide_render=True
ctrl['Face2017_strength']=1.;ctrl['Neck_shortening_mm']=6.;ctrl.id_properties_ui('Face2017_strength').update(min=0.,max=1.5,description='0 = original 2006 structure, 1 = 2017 likeness study')
ctrl.id_properties_ui('Neck_shortening_mm').update(min=0.,max=10.,description='All meshes shift together; default shortens visible neck by 6 mm')
for o in objs.values():
 for key,prop,expr in [('Ronaldo_2017_FACE_STRUCTURE','Face2017_strength','n'),('NECK_SHORTER_6mm','Neck_shortening_mm','n/6')]:
  dr=o.data.shape_keys.key_blocks[key].driver_add('value').driver;dr.expression=expr;v=dr.variables.new();v.name='n';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+prop+'"]'
bpy.context.scene.frame_set(1)
# Select the face on opening; editing controls remain easy to find in the Outliner.
bpy.ops.object.select_all(action='DESELECT');o=objs['face_high_2_fox_skin_mat'];o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Ronaldo_2006_to_2017_FACE_EDIT.blend'))
report=json.loads((R/'validation.json').read_text());report['independent_reload_source_comparison']={'basis_topology_uv_weights_exact_match':checks,'controller_face_default':1,'controller_neck_default_mm':6};report['youtube_error']='Both supplied YouTube URLs return HTTP403; neither video watched';(R/'validation.json').write_text(json.dumps(report,indent=2));print('SOURCE_COMPARISON_AND_CONTROLS_PASS',len(checks))
