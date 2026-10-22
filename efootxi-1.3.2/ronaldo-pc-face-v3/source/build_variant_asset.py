"""Rebuild one cooked UE4.26 skeletal mesh from a verified Android template.
Preserves native face and skeleton. Experimental geometry; original material refs.
"""
from pathlib import Path
import sys,json,struct,hashlib,math,re

import cityhash
import numpy as np
r=Path(__file__).resolve().parent;p=r.parent
sys.path.insert(0,str(p/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
atlas=np.load(r/'atlas_uv.npy')
pc_face_positions=np.load(r/'face_positions_cm.npy')
f=FmdlFile();f.readFile(str(p/'source-extracted/hair_high.fmdl'));hair=f.meshes[0]
assert len(hair.vertices)==5005 and len(hair.faces)==5179
for v in hair.vertices:assert {b.name:w for b,w in v.boneMapping.items() if w>0}=={'sk_head':1.0}
variant=sys.argv[1] if len(sys.argv)>1 else '4522'
assert variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']
newvariant=variant.replace('4522','ND01',1)
source=p/'pc3700-new/extracted'/('SK_'+variant+'_Face.uasset');b=source.read_bytes()
expected={Path(x['path']).name:x['sha256'] for x in json.loads((p/'pc3700-new/head-assets.json').read_text())};assert hashlib.sha256(b).hexdigest()==expected[source.name]
fields=struct.unpack_from('<16I',b);em=fields[11];header_size=fields[13]+fields[14];firstSize=struct.unpack_from('<Q',b,em+8)[0];cooked_off=struct.unpack_from('<Q',b,em+72)[0];real_off=header_size+firstSize;delta=real_off-cooked_off;assert -256<delta<0
ranges={k:int(n)+delta for k,n in re.findall(r'RANGE (\w+) (\d+)',(r/('layout-'+variant+'.log')).read_text())}
def cut(a,z):return b[ranges[a]:ranges[z]]
nface=743;oldnv=1344;nh=len(hair.vertices);nv=nface+nh
# Original native face buffers remain byte-for-byte identical.
oldidx=cut('INDICES_BEGIN','INDICES_END');assert struct.unpack_from('<BII',oldidx)==(2,2,5025)
faceidx=oldidx[9:9+3666*2];assert max(struct.unpack('<3666H',faceidx))<nface
vi={id(v):i+nface for i,v in enumerate(hair.vertices)}
hi=[vi[id(v)] for face in hair.faces for v in reversed(face.vertices)]
indices=struct.pack('<BII',2,2,3666+len(hi))+faceidx+struct.pack('<%dH'%len(hi),*hi)
oldpos=cut('POSITION_BEGIN','POSITION_END');assert struct.unpack_from('<4I',oldpos)==(12,oldnv,12,oldnv)
old_facepos=oldpos[16:16+nface*12];original_points=[struct.unpack_from('<fff',old_facepos,i*12) for i in range(nface)];sculpted=pc_face_positions;facepos=b''.join(struct.pack('<fff',*v) for v in sculpted);hairpos=b''.join(struct.pack('<fff',v.position.x*100,v.position.z*100,v.position.y*100) for v in hair.vertices)
positions=struct.pack('<4I',12,nv,12,nv)+facepos+hairpos
oldtu=cut('TANGENT_UV_BEGIN','TANGENT_UV_END');assert struct.unpack_from('<II',oldtu,2)==(2,oldnv)
assert struct.unpack_from('<II',oldtu,18)==(8,oldnv)
old_uv_at=26+oldnv*8;assert struct.unpack_from('<II',oldtu,old_uv_at)==(4,oldnv*2)
face_tan=bytearray(oldtu[26:26+nface*8]);face_original_tan=bytes(face_tan);face_uv=oldtu[old_uv_at+8:old_uv_at+8+nface*8]
# Recompute native facial normals/tangents for the transferred PC surface.
faces=np.frombuffer(faceidx,'<u2').reshape(-1,3);xyz=np.array(sculpted);texcoords=np.array([struct.unpack_from('<ee',face_uv,i*8) for i in range(nface)]);ns=np.zeros((nface,3));ts=np.zeros((nface,3))
for ids in faces:
 pa,pb,pc=xyz[ids];e1=pb-pa;e2=pc-pa;normal=np.cross(e1,e2);normal*=1 if np.dot(normal,np.array([struct.unpack_from('<8b',face_tan,int(ids[0])*8)[j]/127 for j in [4,5,6]]))>=0 else -1
 duv1=texcoords[ids[1]]-texcoords[ids[0]];duv2=texcoords[ids[2]]-texcoords[ids[0]];den=duv1[0]*duv2[1]-duv1[1]*duv2[0];tangent=(e1*duv2[1]-e2*duv1[1])/den if abs(den)>1e-10 else e1
 for i in ids:ns[i]+=normal;ts[i]+=tangent
for i in range(nface):
 raw=struct.unpack_from('<8b',face_tan,i*8);n=ns[i];n/=max(np.linalg.norm(n),1e-12);t=ts[i]-n*np.dot(ts[i],n);t/=max(np.linalg.norm(t),1e-12)
 pack=lambda v:[max(-127,min(127,round(float(x)*127))) for x in v]
 struct.pack_into('<8b',face_tan,i*8,*pack(t),raw[3],*pack(n),raw[7])
face_tan=bytes(face_tan)
def packsn(x):return max(-127,min(127,round(x*127)))
ht=[];hu=[]
for vertex_i,v in enumerate(hair.vertices):
 t=v.tangent;n=v.normal
 ht.append(struct.pack('<8b',packsn(t.x),packsn(t.z),packsn(t.y),127,packsn(n.x),packsn(n.z),packsn(n.y),packsn(-t.w)))
 hu.append(struct.pack('<eeee',*atlas[vertex_i],v.uv[1].u,v.uv[1].v))
head=bytearray(oldtu[:18]);struct.pack_into('<I',head,6,nv)
tangent_uv=bytes(head)+struct.pack('<II',8,nv)+face_tan+b''.join(ht)+struct.pack('<II',4,nv*2)+face_uv+b''.join(hu)
oldsw=cut('SKIN_WEIGHTS_BEGIN','SKIN_WEIGHTS_END');assert struct.unpack_from('<5I',oldsw,2)==(0,4,oldnv*4,oldnv,0)
assert struct.unpack_from('<II',oldsw,22)==(1,oldnv*8)
facesw=oldsw[30:30+nface*8];lookup=oldsw[30+oldnv*8:];assert len(lookup)==14 and lookup[2:6]==b'\0'*4
swhead=bytearray(oldsw[:22]);struct.pack_into('<II',swhead,10,nv*4,nv)
weights=bytes(swhead)+struct.pack('<II',1,nv*8)+facesw+b'\0\0\0\0\xff\0\0\0'*nh+lookup
oldcol=cut('SKIN_WEIGHTS_END','STREAM_END');assert struct.unpack_from('<4I',oldcol,2)==(4,oldnv,4,oldnv)
facecol=oldcol[18:18+nface*4];profiles=oldcol[18+oldnv*4:];assert profiles==b'\0'*4
colors=oldcol[:2]+struct.pack('<4I',4,nv,4,nv)+facecol+b'\xff'*4*nh+profiles
stream=cut('STREAM_BEGIN','INDICES_BEGIN')+indices+positions+tangent_uv+weights+colors
prefix=bytearray(b[:ranges['STREAM_BEGIN']]);struct.pack_into('<I',prefix,ranges['BUFFERS_SIZE'],len(stream))
# Second section points at the replacement hair, with the same one-bone map [7].
assert struct.unpack_from('<I',prefix,ranges['SECTION_BEGIN']+8)[0]==453
struct.pack_into('<I',prefix,ranges['SECTION_BEGIN']+8,len(hair.faces));struct.pack_into('<I',prefix,ranges['BONEMAP_END'],nh)
# Bounds cover native face plus new hair in Unreal centimeters.
pts=[struct.unpack_from('<fff',facepos,i*12) for i in range(nface)]+[struct.unpack_from('<fff',hairpos,i*12) for i in range(nh)]
lo=[min(v[j] for v in pts) for j in range(3)];high=[max(v[j] for v in pts) for j in range(3)];center=[(a+z)/2 for a,z in zip(lo,high)];extent=[(z-a)/2 for a,z in zip(lo,high)];radius=math.sqrt(sum(x*x for x in extent));assert ranges['BOUNDS_END']-ranges['BOUNDS_BEGIN']==28
struct.pack_into('<7f',prefix,ranges['BOUNDS_BEGIN'],*center,*extent,radius)
new=bytearray(bytes(prefix)+stream+b[ranges['STREAM_END']:]);sizeChange=len(new)-len(b);struct.pack_into('<Q',new,em+72+8,struct.unpack_from('<Q',b,em+72+8)[0]+sizeChange)
# Same-length name replacement keeps summary/name/bundle offsets intact.
ns,nsize,hs,hsize=struct.unpack_from('<4I',new,24);at=ns;name_changes=[]
for i in range((hsize-8)//8):
 h=int.from_bytes(new[at:at+2],'big');at+=2;assert h<32768
 name=bytes(new[at:at+h]).decode();renamed=name.replace('SK_'+variant+'_Face','SK_'+newvariant+'_Face')
 if renamed!=name:
  assert len(renamed)==h;new[at:at+h]=renamed.encode();struct.pack_into('<Q',new,hs+8+i*8,cityhash.CityHash64(renamed.lower().encode()));name_changes.append([name,renamed])
 at+=h
assert len(name_changes)==2
oldpath='/Game/Assets/character/RealFace/SK_'+variant+'_Face';newpath=oldpath.replace('SK_'+variant+'_Face','SK_'+newvariant+'_Face')
def globalidx(path):return (cityhash.CityHash64(path.lower().encode('utf-16-le'))&((1<<62)-1))|(2<<62)
assert struct.unpack_from('<Q',new,em+72+56)[0]==globalidx(oldpath+'/SK_'+variant+'_Face')
struct.pack_into('<Q',new,em+72+56,globalidx(newpath+'/SK_'+newvariant+'_Face'))
assert struct.unpack_from('<Q',new,em+56)[0]==0xffffffffffffffff
out=r/'asset';out.mkdir(exist_ok=True);(out/('SK_'+newvariant+'_Face.uasset')).write_bytes(new)
report={'source':str(source),'source_sha256':hashlib.sha256(b).hexdigest(),'asset_sha256':hashlib.sha256(new).hexdigest(),'bytes':len(new),'new_path':newpath,'new_package_id':cityhash.CityHash64(newpath.lower().encode('utf-16-le')),'face_vertices':nface,'hair_vertices':nh,'triangles':len(hi)//3+1222,'vertex_count':nv,'native_face_buffer_hashes':{k:hashlib.sha256(v).hexdigest() for k,v in [('positions',facepos),('indices',faceidx),('tangents',face_tan),('uv',face_uv),('weights',facesw),('colors',facecol)]},'material_status':'PC face surface/color adaptation plus v2 baked hair atlas', 'face_sculpt_max_cm':float(max(np.linalg.norm(np.array(v)-w) for v,w in zip(original_points,sculpted))), 'face_original_positions_sha256':hashlib.sha256(old_facepos).hexdigest(), 'face_original_tangents_sha256':hashlib.sha256(face_original_tan).hexdigest(),'name_changes':name_changes,'native_device_verified':False}
(r/('asset-build-'+variant+'.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
