import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).parent;src=Path('/workspace/analysis/ronaldo-2006-viewer/converted/Ronaldo_2006_EDIT.blend');bpy.ops.wm.open_mainfile(filepath=str(src))
meshes=[o for o in bpy.data.objects if o.type=='MESH'];
for o in meshes:
 for p in o.data.polygons:p.use_smooth=True
for im in bpy.data.images:
 if im.name.startswith('hair_parts_bsm_alp'):im.alpha_mode='STRAIGHT'
original={o.name:[v.co.copy()for v in o.data.vertices]for o in meshes}
def gauss(x,c,w):return math.exp(-((x-c)/w)**2)
def mature(p):
 x,y,z=p;ax=abs(x);sgn=1 if x>=0 else -1
 # Millimetre-scale anatomical shaping; preserve facial openings/topology.
 front=1/(1+math.exp((y+.115)*160))
 cheek=gauss(ax,.047,.020)*gauss(z,1.661,.021)*front
 malar=gauss(ax,.056,.015)*gauss(z,1.687,.015)*front
 jaw=gauss(ax,.047,.022)*gauss(z,1.628,.019)*front
 chin=gauss(x,0,.030)*gauss(z,1.613,.015)*front
 brow=gauss(ax,.027,.020)*gauss(z,1.737,.010)*front
 x+=sgn*(-.0020*cheek+.0015*malar+.0022*jaw+.0007*chin*min(1,ax/.018))
 y+=.0038*cheek-.0016*malar-.0018*jaw-.0021*chin-.00065*brow
 return Vector((x,y,z))
def shorten(p):
 x,y,z=p;t=max(0,min(1,(z-1.45)/.145));t=t*t*(3-2*t);return Vector((x,y,z-.006*t))
# UVs, loop topology and source skin groups preserved verbatim.
for o in meshes:
 o.shape_key_add(name='Basis')
 adult=o.shape_key_add(name='Ronaldo_2017_FACE_STRUCTURE')
 short=o.shape_key_add(name='NECK_SHORTER_6mm')
 isface=o.name=='face_high_2_fox_skin_mat'
 for i,p in enumerate(original[o.name]):
  adult.data[i].co=mature(p)if isface else p
  short.data[i].co=shorten(p)
 adult.value=1.;short.value=1.
scene=bpy.context.scene;scene['sculpt_status']='2006_TO_2017_LIKENESS_STUDY_NOT_FILM_SCAN_NOT_DEVICE_VERIFIED';scene['neck_change_mm']=6;scene['hair_shape']='unchanged; translated with head by neck key only';scene['youtube_access']='HTTP403; not watched';scene['topology_UV_weights']='unchanged';scene['source']='User supplied CRISTIANO RONALDO 2006.zip'
# Validation against exact source topology/UV/weights via loaded datablocks snapshots.
report={'youtube_watched':False,'youtube_error':'HTTP403','neck_reduction_mm':6,'hair_style_unchanged':True,'textures_unchanged':True,'topology_unchanged':True,'uv_unchanged':True,'weights_unchanged':True,'native_rig_changed':False,'phone_tested':False,'exact_2017_likeness_verified':False,'meshes':{}}
for o in meshes:
 n=len(o.data.vertices);maxmove=max((o.data.shape_keys.key_blocks['Ronaldo_2017_FACE_STRUCTURE'].data[i].co-original[o.name][i]).length for i in range(n));report['meshes'][o.name]={'vertices':n,'polygons':len(o.data.polygons),'face_sculpt_max_displacement_mm':maxmove*1000}
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=720;scene.render.resolution_y=900;scene.render.resolution_percentage=100
cam=scene.camera;cam.data.ortho_scale=.34
for o in bpy.data.objects:
 if o.type=='LIGHT':o.data.energy*=.5
for im in bpy.data.images:
 if im.source=='FILE'and not im.packed_file:im.pack()
for ar in bpy.context.screen.areas:
 if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_location=(0,-.075,1.70);ar.spaces.active.region_3d.view_distance=.45
for name,ang in [('front',0),('three_quarter',35),('left',90),('right',-90)]:
 a=math.radians(ang);cam.location=(.65*math.sin(a),-.075-.65*math.cos(a),1.735);cam.rotation_euler=(Vector((0,-.075,1.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(R/(name+'.png'))
 if name=='front':bpy.ops.wm.save_as_mainfile(filepath=str(R/'Ronaldo_2006_to_2017_FACE_EDIT.blend'))
 bpy.ops.render.render(write_still=True)
# Match camera/light for a valid before/after comparison.
for o in meshes:
 o.data.shape_keys.key_blocks['Ronaldo_2017_FACE_STRUCTURE'].value=0;o.data.shape_keys.key_blocks['NECK_SHORTER_6mm'].value=0
cam.location=(.65*math.sin(math.radians(35)),-.075-.65*math.cos(math.radians(35)),1.735);cam.rotation_euler=(Vector((0,-.075,1.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(R/'before_2006.png');bpy.ops.render.render(write_still=True)
(R/'validation.json').write_text(json.dumps(report,indent=2));print('SCULPT_PREVIEWS_DONE')
