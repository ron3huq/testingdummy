import bpy,bmesh,sys,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).parent;ROOT=Path('/workspace/analysis/ronaldo-2006-viewer')
sys.path.insert(0,'/workspace/analysis/my-league/ronaldo-pc-conversion/pes-fmdl-blender/pes-fmdl');from FmdlFile import FmdlFile
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,r=.55):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;return m
red=mat('MASK_crimson_fabric',(.24,.005,.014),.65);black=mat('MASK_graphite_web_and_rims',(.008,.009,.011),.52);white=mat('MASK_silver_optical_lenses',(.68,.71,.72),.35)
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(ob);me.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 return ob
models={}
for n in ['face_high','hair_high']:
 f=FmdlFile();f.readFile(str(ROOT/'source-extracted'/(n+'.fmdl')));models[n]=f
cv=lambda v:(v.position.x,-v.position.z,v.position.y)
# Exactly the user's 2006 neck, with original UV and weights preserved.
m=models['face_high'].meshes[0];ids={id(v):i for i,v in enumerate(m.vertices)}
neckmat=mat('RONALDO_2006_ORIGINAL_NECK_SKIN',(.5,.26,.17));im=bpy.data.images.load(str(ROOT/'converted/face_bsm_alp.png'));im.pack();im.alpha_mode='NONE';tex=neckmat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;neckmat.node_tree.links.new(tex.outputs['Color'],neckmat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
neck=mesh('RONALDO_2006_NECK_UNCHANGED',list(map(cv,m.vertices)),[[ids[id(v)]for v in reversed(t.vertices)]for t in m.faces if max(v.position.y for v in t.vertices)<1.635],neckmat);uv=neck.data.uv_layers.new(name='UV0')
for l in neck.data.loops:v=m.vertices[l.vertex_index];uv.data[l.index].uv=(v.uv[0].u,1-v.uv[0].v)
for i,v in enumerate(m.vertices):
 for b,w in v.boneMapping.items():
  g=neck.vertex_groups.get(b.name)or neck.vertex_groups.new(name=b.name);g.add([i],w,'REPLACE')
# Retain the source under-chin/throat skin to close the original multi-mesh neck seam.
m=models['face_high'].meshes[2];selected=[t for t in m.faces if max(v.position.y for v in t.vertices)<1.630];used={id(v):v for t in selected for v in t.vertices};vv=list(used.values());ii={id(v):i for i,v in enumerate(vv)}
throat=mesh('RONALDO_2006_ORIGINAL_THROAT',list(map(cv,vv)),[[ii[id(v)]for v in reversed(t.vertices)]for t in selected],neckmat);uv=throat.data.uv_layers.new(name='UV0')
for l in throat.data.loops:v=vv[l.vertex_index];uv.data[l.index].uv=(v.uv[0].u,1-v.uv[0].v)
for i,v in enumerate(vv):
 for b,w in v.boneMapping.items():
  g=throat.vertex_groups.get(b.name)or throat.vertex_groups.new(name=b.name);g.add([i],w,'REPLACE')
# Only the upper overlap is tucked beneath the mask. Visible lower neck is unchanged.
for ob in [neck,throat]:
 for v in ob.data.vertices:
  t=max(0,min(1,(v.co.z-1.603)/.015));v.co.x*=1-.12*t;v.co.y+=.022*t
# Build the covered shell from real head anatomy. No parametric egg profile.
cloud=[]
for mm in [models['face_high'].meshes[0],models['face_high'].meshes[2],models['hair_high'].meshes[0]]:
 for v in mm.vertices:
  x,y,z=cv(v)
  if z<1.603:continue
  x=max(-.077,min(.077,x));y=max(y,-.175) # covered ears and smoothed nose, not protruding bare ears/nose
  cloud.append((x,y,z))
bm=bmesh.new()
for p in cloud:bm.verts.new(p)
bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
# Remove loose source vertices left inside the convex envelope.
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
me=bpy.data.meshes.new('Anatomical_mask_shell');bm.to_mesh(me);bm.free();shell=bpy.data.objects.new('SPIDERMAN_ANATOMICAL_HEAD',me);bpy.context.collection.objects.link(shell);me.materials.append(red);bpy.context.view_layer.objects.active=shell;shell.select_set(True)
sub=shell.modifiers.new('Smooth anatomical envelope','SUBSURF');sub.levels=2;bpy.ops.object.modifier_apply(modifier=sub.name)
for p in shell.data.polygons:p.use_smooth=True
bpy.context.view_layer.update();bvh=BVHTree.FromObject(shell,bpy.context.evaluated_depsgraph_get())
def front(x,z,off=.001):
 p,n,_,_=bvh.ray_cast(Vector((x,-.5,z)),Vector((0,1,0)))
 if p is None:raise RuntimeError('Eye extends off anatomical head '+str((x,z)))
 return p+n*off
center=Vector((0,-.066,1.714))
def surf(r,a,off=.0008):
 d=Vector((math.sin(r)*math.sin(a),-math.cos(r),math.sin(r)*math.cos(a)));p,n,_,_=bvh.ray_cast(center,d)
 if p is None:raise RuntimeError('Anatomical shell ray miss')
 return p+n*off
# Continuous radial film-style web, centred between the eyes.
def curve(n,pts,w=.00055):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=w;c.bevel_resolution=2;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);c.materials.append(black)
for j in range(16):curve('WEB_radial_%02d'%j,[surf(.006+i*(math.pi-.012)/160,j*math.pi/8)for i in range(161)])
for k,r in enumerate([.24,.45,.68,.92,1.18,1.45,1.73,2.0,2.27,2.51,2.75]):curve('WEB_ring_%02d'%k,[surf(r-.018*math.sin(8*a)**2,a)for a in [i*2*math.pi/256 for i in range(257)]])
def bez(p0,p1,p2,p3,t):return tuple((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i]for i in range(2))
p0=(.012,1.714);p1=(.064,1.756)
outline=[bez(p0,(.028,1.731),(.052,1.747),p1,i/48)for i in range(48)]+[bez(p1,(.067,1.706),(.042,1.688),p0,i/48)for i in range(48)]
for sign in [-1,1]:
 c=(.041,1.722);L=len(outline);v=[front(sign*c[0],c[1],.0045)]
 for k in range(1,13):
  t=k/12
  for x,z in outline:v.append(front(sign*(c[0]+(x-c[0])*t),c[1]+(z-c[1])*t,.003+.0015*(1-t*t)))
 f=[(0,1+j,1+(j+1)%L)for j in range(L)]
 for k in range(11):
  a=1+k*L;b=a+L;f.extend((a+j,b+j,b+(j+1)%L,a+(j+1)%L)for j in range(L))
 mesh(('LEFT'if sign<0 else'RIGHT')+'_LENS',v,f,white)
 v=[]
 for sc,off in [(1.13,.002),(1,.004)]:
  for x,z in outline:v.append(front(sign*(c[0]+(x-c[0])*sc),c[1]+(z-c[1])*sc,off))
 ob=mesh(('LEFT'if sign<0 else'RIGHT')+'_FRAME',v,[(j,(j+1)%L,L+(j+1)%L,L+j)for j in range(L)],black);mod=ob.modifiers.new('Frame thickness','SOLIDIFY');mod.thickness=.0008
# Micro textile bump on mask only. Neck texture remains original.
n=red.node_tree.nodes;l=red.node_tree.links;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=2500;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.13;b.inputs['Distance'].default_value=.0002;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=720;scene.render.resolution_y=900;scene.world.color=(.1,.1,.1)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for n,loc,power in [('Key',(-.35,-.5,2.05),4),('Fill',(.4,-.4,1.8),2),('Rim',(.2,.2,2.0),5)]:
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.size=.4;o=bpy.data.objects.new(n,d);scene.collection.objects.link(o);o.location=loc;aim(o,(0,-.06,1.7))
d=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.ortho_scale=.38
scene['status']='ANATOMICAL_HEAD_WITH_ORIGINAL_2006_NECK_NOT_DEVICE_VERIFIED';scene['neck_source']='Original face_high.fmdl mesh0, exact vertex positions UVs and bone weights'
# Raw mesh export for native asset building; curve geometry included after evaluation.
records=[]
for o in list(scene.objects):
 if o.type not in ['MESH','CURVE']:continue
 dep=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dep);mm=ev.to_mesh();mm.calc_loop_triangles();records.append({'name':o.name,'vertices':[list(v.co)for v in mm.vertices],'triangles':[list(t.vertices)for t in mm.loop_triangles]});ev.to_mesh_clear()
(R/'geometry.json').write_text(json.dumps(records))
for name,ang in [('front',0),('three_quarter',40),('left',90),('right',-90),('back',180)]:
 a=math.radians(ang);cam.location=(.8*math.sin(a),-.06-.8*math.cos(a),1.72);aim(cam,(0,-.06,1.65));scene.render.filepath=str(R/(name+'.png'))
 if name=='front':bpy.ops.wm.save_as_mainfile(filepath=str(R/'SpiderMan_v3_HUMAN_NECK.blend'))
 bpy.ops.render.render(write_still=True)
