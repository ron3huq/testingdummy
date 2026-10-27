import bpy,json,numpy as np,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-hair-v1/original-export/Game/Assets/character/RealFace');g=json.loads((P/'SK_4522_Face.gltf').read_text());a=g['accessors'][g['meshes'][0]['primitives'][0]['attributes']['POSITION']];v=g['bufferViews'][a['bufferView']];b=(P/g['buffers'][v['buffer']]['uri']).read_bytes();pp=np.frombuffer(b,dtype='<f4',offset=v.get('byteOffset',0)+a.get('byteOffset',0),count=a['count']*3).reshape(-1,3);native=np.column_stack([pp[:,0],-pp[:,2],pp[:,1]])
bpy.ops.wm.open_mainfile(filepath=str(R/'RONALDO_2009_NATIVE.blend'));o=bpy.data.objects['NATIVE_2009_FACE_SKIN'];geo=json.loads((R/'game_geometry.json').read_text());locked=[];blended=[]
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
for i,point in enumerate(native):
 x,y,z=point;w=smooth((abs(x)-.044)/.014)*smooth((y+.125)/.022)*smooth((z-1.61)/.025)*smooth((1.805-z)/.025)
 if w<=0:continue
 old=o.data.vertices[i].co.copy();co=old.lerp(Vector(point),w);o.data.vertices[i].co=co;geo['face'][i]['p']=list(co)
 if w>.99999:locked.append(i)
 else:blended.append(i)
for tri in [[406,399,405],[23,24,25]]:assert all(i in locked for i in tri),(tri,locked)
(R/'game_geometry.json').write_text(json.dumps(geo));(R/'native-ear-validation.json').write_text(json.dumps({'native_ear_vertices_kept_exact':locked,'native_ear_transition_vertices':blended,'native_eye_flags_uvs_weights_unchanged':True,'reason':'source projection introduced tiny ear triangle reversals absent in the original native model','phone_tested':False},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'RONALDO_2009_NATIVE.blend'),compress=True)
s=bpy.context.scene;s.cycles.samples=16;s.cycles.use_denoising=False
for name,angle in [('front',0),('three_quarter',35),('profile',90)]:
 t=math.radians(angle);s.camera.location=(.65*math.sin(t),-.075-.65*math.cos(t),1.735);s.camera.rotation_euler=(Vector((0,-.075,1.68))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
print('NATIVE_EAR_CORE_RESTORED',len(locked),len(blended),flush=True)
