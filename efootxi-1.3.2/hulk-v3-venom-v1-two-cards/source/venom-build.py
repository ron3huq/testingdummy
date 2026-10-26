import bpy,bmesh,math,random,json
from mathutils import Vector
from pathlib import Path
R=Path(__file__).parent;random.seed(38);bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(n,c,r=.3):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;return m
black=mat('Living symbiote black',(.0015,.0025,.0035),.30);white=mat('Organic ivory eye membranes',(.57,.60,.57),.42);gums=mat('Dark organic gingiva',(.015,.006,.008),.42);ivory=mat('Uneven natural fangs',(.62,.51,.31),.30);oral=mat('Deep open mouth',(.001,.001,.001),.9)
for ma,scale,dist in [(black,180,.0007),(white,450,.00018),(gums,250,.0002)]:
 n=ma.node_tree.nodes;l=ma.node_tree.links;no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=scale;no.inputs['Detail'].default_value=3;bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.22;bu.inputs['Distance'].default_value=dist;l.new(no.outputs['Fac'],bu.inputs['Height']);l.new(bu.outputs[0],n.get('Principled BSDF').inputs['Normal'])
def mesh(n,v,f,ma):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.materials.append(ma);o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 return o
# A sculpted symbiote cranium and jaw; anterior mouth region is genuinely open.
def surface(theta,z):
 t=(z-1.545)/.295;width=.101*(max(.001,math.sin(math.pi*t))**.37);depth=.102*(max(.001,math.sin(math.pi*t))**.32)
 jaw=math.exp(-((z-1.599)/.050)**2);width*=1+.14*jaw
 x=width*math.sin(theta);y=-.063-depth*math.cos(theta)
 if math.cos(theta)>0:
  y-=.010*math.exp(-((abs(x)-.067)/.026)**2-((z-1.655)/.047)**2)
  y+=.010*math.exp(-(x/.025)**2-((z-1.690)/.032)**2)
 y+=.0008*math.sin(x*120+z*90)*math.exp(-((z-1.75)/.08)**2)
 x*=1+.13*math.exp(-((z-1.75)/.065)**2)
 return Vector((x,y,z))
def upper(x):return 1.641+.024*(abs(x)/.090)**1.65
def lower(x):return 1.570+.087*(abs(x)/.090)**2.3
vs=[];fs=[];N=160;M=116
for j in range(M+1):
 z=1.545+.295*(j+.001)/(M+.002)
 for i in range(N):vs.append(surface((i/N-.5)*math.tau,z))
for j in range(M):
 for i in range(N):
  ids=(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i);c=sum([vs[k]for k in ids],Vector())/4
  if c.y<-.095 and abs(c.x)<.091 and lower(c.x)<c.z<upper(c.x):continue
  fs.append(ids)
head=mesh('VENOM_CRANIUM_OPEN_JAW',vs,fs,black)
# Mouth cavity occupies the opening, back surface remains well inside the skull.
vs=[];fs=[]
for j in range(23):
 t=j/22
 for i in range(81):
  x=-.09+.18*i/80;z=lower(x)*(1-t)+upper(x)*t;y=-.085+.010*math.sin(math.pi*t)*(1-(x/.095)**2);vs.append((x,y,z))
  if j and i:fs.append(((j-1)*81+i-1,(j-1)*81+i,j*81+i,j*81+i-1))
mesh('MOUTH_CAVITY',vs,fs,oral)
def tube(n,points,radius,ma,sides=8):
 vs=[];fs=[]
 for j,p in enumerate(points):
  p=Vector(p);di=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
  if di.length<1e-7:di=Vector((0,0,1))
  di.normalize();a=di.cross(Vector((0,1,0)))
  if a.length<.01:a=di.cross(Vector((1,0,0)))
  a.normalize();b=di.cross(a);rr=radius if isinstance(radius,float)else radius[j]
  for k in range(sides):vs.append(p+rr*(math.cos(k*math.tau/sides)*a+math.sin(k*math.tau/sides)*b))
  if j:
   for k in range(sides):fs.append(((j-1)*sides+k,(j-1)*sides+(k+1)%sides,j*sides+(k+1)%sides,j*sides+k))
 fs.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+k for k in range(sides))]);return mesh(n,vs,fs,ma)
# Uneven fleshy lips and gums roll around the entire crescent opening.
for top in [True,False]:
 points=[]
 for i in range(91):
  x=-.090+.180*i/90;z=upper(x)if top else lower(x);p=surface(math.asin(max(-.999,min(.999,x/.104))),z);points.append((x,p.y-.001,z))
 tube('UPPER_GUM'if top else 'LOWER_GUM',points,.0035,gums,10)
 tube('UPPER_BLACK_LIP'if top else 'LOWER_BLACK_LIP',[(x,y+.0005,z+(.0038 if top else -.0038))for x,y,z in points],.0038,black,8)
# Irregular narrow recurved teeth, upper and lower rows with a smaller inner row.
for top,count in [(True,27),(False,25)]:
 for i in range(count):
  x=-.084+.168*i/(count-1);z=upper(x)-.002 if top else lower(x)+.002;p=surface(math.asin(max(-.99,min(.99,x/.104))),z);length=random.uniform(.017,.028)*(1-.33*(abs(x)/.09)**2);sgn=-1 if top else 1;length=min(length,.65*max(.004,upper(x)-lower(x)))
  pts=[];radii=[]
  for k in range(7):
   t=k/6;pts.append((x+math.sin(i*4.3)*.002*t,p.y-.001-.003*math.sin(t*math.pi),z+sgn*length*t));radii.append(.0036*(1-t)**.65+.00007)
  tube(('UPPER'if top else 'LOWER')+'_FANG_%02d'%i,pts,radii,ivory,7)
# White eyes follow the swept organic silhouette, not human eye sockets.
outline=[(.014,1.700),(.035,1.704),(.060,1.718),(.079,1.738),(.090,1.762),(.086,1.733),(.087,1.716),(.072,1.697),(.047,1.685),(.026,1.689)]
# Subdivide the irregular outline into a membrane fan lying on the skull.
for side in [-1,1]:
 pts=[]
 for i,p in enumerate(outline):
  prev=Vector(outline[(i-1)%len(outline)]);a=Vector(p);b=Vector(outline[(i+1)%len(outline)]);nxt=Vector(outline[(i+2)%len(outline)])
  for k in range(8):
   t=k/8;q=.5*((2*a)+(-prev+b)*t+(2*prev-5*a+4*b-nxt)*t*t+(-prev+3*a-3*b+nxt)*t*t*t);pts.append(q)
 center=sum(pts,Vector((0,0)))/len(pts);verts=[];polys=[];rings=8;L=len(pts)
 for j in range(rings+1):
  t=(j+.001)/(rings+.001)
  for p in pts:
   q=center.lerp(p,t);x=side*q.x;z=q.y;width=.101*max(.001,math.sin(math.pi*(z-1.545)/.295))**.37;theta=math.asin(max(-.99,min(.99,x/width)));v=surface(theta,z);v.y-=.0020+.0015*(1-t*t);verts.append(v)
  if j:
   for i in range(L):polys.append(((j-1)*L+i,(j-1)*L+(i+1)%L,j*L+(i+1)%L,j*L+i))
 mesh('VENOM_WHITE_EYE_'+str(side),verts,polys,white)
# Use an anatomical source neck with a matching body rim, not a cylinder.
with bpy.data.libraries.load('/workspace/analysis/spiderman-original-neck-v6/SpiderMan_v6_ORIGINAL_2006_NECK.blend',link=False)as(src,dst):dst.objects=[n for n in src.objects if n=='ORIGINAL_2006_NECK_REPAIRED']
for ob in dst.objects:
 bpy.context.collection.objects.link(ob);ob.name='VENOM_NECK_REAL_ANATOMY';ob.data.materials.clear();ob.data.materials.append(black)
 for v in ob.data.vertices:
  z=v.co.z;t=max(0,min(1,(z-1.43)/.12));v.co.x*=1+.16*math.sin(t*math.pi);v.co.z-=.022*t
  if v.co.z>1.53:
   f=max(0,min(1,(v.co.z-1.53)/.035));v.co.x*=1-.20*f;v.co.y=max(v.co.y,-.12)+.014*f
 for p in ob.data.polygons:p.material_index=0;p.use_smooth=True
# Fine raised tendrils break up smooth surfaces, integrated black rather than grey webbing.
for side in [-1,1]:
 for k in range(19):
  angle=side*random.uniform(.45,2.3);z0=random.uniform(1.49,1.78);pts=[]
  for j in range(16):
   t=j/15;z=min(1.835,z0+.044*t);p=surface(angle+.06*math.sin(t*6+k),z);p+=Vector((math.sin(angle),-math.cos(angle),0))*.0005;pts.append(p)
  tube('FACIAL_ORGANIC_TENDRIL',pts,random.uniform(.00045,.00085),black,5)
# Compress the top of the skull and all attached details together.
for ob in bpy.data.objects:
 if ob.type=='MESH' and 'NECK' not in ob.name:
  for v in ob.data.vertices:
   if v.co.z>1.70:v.co.z=1.70+(v.co.z-1.70)*.88
# All mask parts are rigid to head; neck weighting is assigned at game export.
s=bpy.context.scene;s.world=bpy.data.worlds.new('Dark studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.06,.07,.09,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
bpy.ops.object.camera_add();s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=.49
for loc,pow,size,c in [((-.35,-.5,2.0),15,.42,(.8,.90,1)),((.4,-.2,1.8),5,.35,(1,.88,.73)),((.1,.25,1.95),20,.3,(.65,.8,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=pow;o.data.shape='DISK';o.data.size=size;o.data.color=c;o.rotation_euler=(Vector((0,-.05,1.66))-o.location).to_track_quat('-Z','Y').to_euler()
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.resolution_x=800;s.render.resolution_y=900;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX'
for name,ang in [('front',0),('three_quarter',35),('profile',90),('back',180)]:
 a=math.radians(ang);s.camera.location=(.7*math.sin(a),-.06-.7*math.cos(a),1.73);s.camera.rotation_euler=(Vector((0,-.06,1.65))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(R/(name+'.png'))
 if name=='three_quarter':bpy.ops.wm.save_as_mainfile(filepath=str(R/'VENOM_GAME_V1.blend'))
 bpy.ops.render.render(write_still=True)
