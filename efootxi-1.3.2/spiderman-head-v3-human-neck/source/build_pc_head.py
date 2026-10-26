"""Cook actual supplied PC face/neck/scalp mesh against the unchanged native rig."""
from pathlib import Path
import sys,json,struct,re,hashlib,math
import numpy as np
import cityhash
r=Path(__file__).parent;p=r.parent;sys.path.insert(0,str(p/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
variant=sys.argv[1] if len(sys.argv)>1 else '4522ep00v0313';source=p/'pc3700-new/extracted'/('SK_'+variant+'_Face.uasset');b=source.read_bytes();fields=struct.unpack_from('<16I',b);em=fields[11];delta=fields[13]+fields[14]+struct.unpack_from('<Q',b,em+8)[0]-struct.unpack_from('<Q',b,em+72)[0]
log=(p/'android-hair-v1'/('layout-'+variant+'.log')).read_text();ranges={k:int(v)+delta for k,v in re.findall(r'RANGE (\w+) (\d+)',log)}
orig=json.loads((p/'android-hair-v1/original-export/Game/Assets/character/RealFace'/('SK_'+variant+'_Face.gltf')).read_text());bones=[orig['nodes'][n]['name'] for n in orig['skins'][0]['joints']];assert len(bones)==166
boneids={n:i for i,n in enumerate(bones)};face=FmdlFile();face.readFile(str(p/'new-face-4522/models/face_high.fmdl'));hair=FmdlFile();hair.readFile(str(p/'new-face-4522/models/hair_high.fmdl'))
# Explicit reduced facial mapping: preserve named jaw/lid controls; upper lip stays with head.
# Unsupported fine lip/brow controls are reduced, never guessed as opaque numbered bones.
alias={'sk_neck':'sk_cervicalspine_02','sk_chest':'sk_spine_03','dsk_neckback':'sk_cervicalspine_01','dsk_scm':'sk_cervicalspine_02','dsk_clavicle_l':'sk_shoulder_l','dsk_clavicle_r':'sk_shoulder_r'}
policies={}
def mapped(name):
 if name in boneids:out={boneids[name]:1.}
 elif name in alias:out={boneids[alias[name]]:1.}
 elif name.startswith('skf_lip_b_') or name=='skf_doublechin':out={boneids['skf_jaw']:1.}
 elif name.startswith('skf_lip_s_') or name=='skf_lip_volume':out={boneids['sk_head']:.5,boneids['skf_jaw']:.5}
 elif name.startswith('skf_cheek'):out={boneids['sk_head']:.8,boneids['skf_jaw']:.2}
 elif name.startswith('skf_'):out={boneids['sk_head']:1.}
 else:raise ValueError('unmapped bone '+name)
 policies[name]={bones[k]:v for k,v in out.items()};return out
from types import SimpleNamespace as NS
geo=json.loads(Path('/workspace/analysis/spiderman-v3/native_geometry.json').read_text())
def fake(row):
 x,y,z=row['p'];nx,ny,nz=row['n'];normal=NS(x=nx,y=nz,z=-ny)
 # A stable tangent orthogonal to the normal; masks use diffuse, not a normal map.
 tangent=np.cross([nx,ny,nz],[0,0,1.])
 if np.linalg.norm(tangent)<.001:tangent=np.array([1.,0,0])
 tangent=tangent/np.linalg.norm(tangent);tx,ty,tz=tangent
 return NS(position=NS(x=x,y=z,z=-y),normal=normal,tangent=NS(x=tx,y=tz,z=-ty,w=1),uv=[NS(u=row['uv'][0],v=1-row['uv'][1]),NS(u=0.,v=0.)])
# Native face slot is a hidden triangle; all visible mask + real-neck geometry
# resides in the atlas material slot, so no original face texture can overwrite it.
dummies=[{'p':[0,-.06,1.72],'n':[0,-1,0],'uv':[0,0]}, {'p':[.0001,-.06,1.72],'n':[0,-1,0],'uv':[0,0]}, {'p':[0,-.06,1.7201],'n':[0,-1,0],'uv':[0,0]}]
verts=list(map(fake,dummies));faces=[[0,1,2]];nface=3;ntri=1
hmesh=NS(vertices=list(map(fake,geo['vertices'])),faces=geo['triangles']);n=len(hmesh.vertices);atlas=np.array([[row['uv'][0],1-row['uv'][1]]for row in geo['vertices']])
allweights=[[(boneids['sk_head'],1.)]]*3
for row in geo['vertices']:
 ww={}
 for name,w in row['weights'].items():
  for k,a in mapped(name).items():ww[k]=ww.get(k,0)+w*a
 rr=sorted(ww.items(),key=lambda q:-q[1])[:4];total=sum(w for k,w in rr);allweights.append([(k,w/total)for k,w in rr])
used_bones={k for row in allweights for k,w in row if w>0};face_bonemap=[7,6,5,4]+sorted(used_bones-{7,6,5,4});assert len(face_bonemap)<=75;local={v:i for i,v in enumerate(face_bonemap)}
hairfaces=[[nface+i for i in t]for t in hmesh.faces];idx=[i for t in faces+hairfaces for i in t];nv=nface+n
indices=struct.pack('<BII',2,2,len(idx))+struct.pack('<%dH'%len(idx),*idx)
points=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for v in verts+hmesh.vertices]);positions=struct.pack('<4I',12,nv,12,nv)+points.astype('<f4').tobytes()
def sn(x):return max(-127,min(127,round(x*127)))
tangents=[];uv=[]
for i,v in enumerate(verts+hmesh.vertices):
 t=v.tangent;normal=v.normal;tangents.append(struct.pack('<8b',sn(t.x),sn(t.z),sn(t.y),127,sn(normal.x),sn(normal.z),sn(normal.y),sn(-t.w)))
 uv.append(struct.pack('<eeee',0.,0.,0.,0.)if i<nface else struct.pack('<eeee',*atlas[i-nface],0.,0.))
oldtu=b[ranges['TANGENT_UV_BEGIN']:ranges['TANGENT_UV_END']];head=bytearray(oldtu[:18]);struct.pack_into('<I',head,6,nv);tangent_uv=bytes(head)+struct.pack('<II',8,nv)+b''.join(tangents)+struct.pack('<II',4,nv*2)+b''.join(uv)
oldsw=b[ranges['SKIN_WEIGHTS_BEGIN']:ranges['SKIN_WEIGHTS_END']];weightbytes=[]
for row in allweights:
 inds=[local[k] for k,w in row];vals=[round(w*255) for k,w in row];vals[0]+=255-sum(vals);assert all(0<=v<=255 for v in vals)
 weightbytes.append(bytes(inds+[0]*(4-len(inds))+vals+[0]*(4-len(vals))))
swhead=bytearray(oldsw[:22]);struct.pack_into('<II',swhead,10,nv*4,nv);weights=bytes(swhead)+struct.pack('<II',1,nv*8)+b''.join(weightbytes)+oldsw[30+1344*8:]
oldcol=b[ranges['SKIN_WEIGHTS_END']:ranges['STREAM_END']];colors=oldcol[:2]+struct.pack('<4I',4,nv,4,nv)+b'\xff'*(nv*4)+b'\0'*4
stream=b[ranges['STREAM_BEGIN']:ranges['INDICES_BEGIN']]+indices+positions+tangent_uv+weights+colors
# Update sections and both active/required lists. All body/hand/foot bones remain available
# when replay switches the face component's animation/LOD mode.
section_starts=[int(x)+delta for x in re.findall(r'RANGE SECTION_BEGIN (\d+)',log)];assert len(section_starts)==2
s0,s1=section_starts;end=ranges['SECTIONS_END'];sections=[]
for si,(a,z,bm,numverts,tris,baseidx,basevert) in enumerate([(s0,s1,face_bonemap,nface,ntri,0,0),(s1,end,face_bonemap,n,len(hmesh.faces),ntri*3,nface)]):
 section=b[a:z];old_count=struct.unpack_from('<I',section,29)[0];old_end=33+old_count*2;assert len(section)==old_end+30+4 and section[1]&1
 header=bytearray(section[:29]);struct.pack_into('<ii',header,4,baseidx,tris);struct.pack_into('<I',header,21,basevert);tail=bytearray(section[old_end:]);struct.pack_into('<II',tail,0,numverts,4)
 sections.append(bytes(header)+struct.pack('<I',len(bm))+struct.pack('<%dH'%len(bm),*bm)+tail)
allbones=struct.pack('<I',166)+struct.pack('<166H',*range(166));prefix=bytearray(b[:ranges['STREAM_BEGIN']]);struct.pack_into('<I',prefix,ranges['BUFFERS_SIZE'],len(stream));edits=[(s0,end,b''.join(sections)),(ranges['ACTIVE_BEGIN'],ranges['ACTIVE_END'],allbones)]
for lod in map(int,re.findall(r'RANGE LOD_BEGIN (\d+)',log)):
 a=lod+delta+10;count=struct.unpack_from('<I',b,a)[0];assert 0<count<=166;edits.append((a,a+4+2*count,allbones))
for a,z,v in sorted(edits,reverse=True):prefix[a:z]=v
pts=points;lo=pts.min(axis=0);hi=pts.max(axis=0);center=(lo+hi)/2;extent=(hi-lo)/2;struct.pack_into('<7f',prefix,ranges['BOUNDS_BEGIN'],*center,*extent,float(np.linalg.norm(extent)))
new=bytearray(prefix+stream+b[ranges['STREAM_END']:]);struct.pack_into('<Q',new,em+72+8,struct.unpack_from('<Q',b,em+72+8)[0]+len(new)-len(b))
# Change only the private mesh package/object names; ref skeleton and bind data stay native.
ns,nsize,hs,hsize=struct.unpack_from('<4I',new,24);at=ns
for i in range((hsize-8)//8):
 size=int.from_bytes(new[at:at+2],'big');at+=2;assert size<32768;name=bytes(new[at:at+size]).decode();renamed=name.replace('SK_'+variant+'_Face','SK_'+variant.replace('4522','ND01',1)+'_Face')
 if name!=renamed:new[at:at+size]=renamed.encode();struct.pack_into('<Q',new,hs+8+i*8,cityhash.CityHash64(renamed.lower().encode()))
 at+=size
oldpath='/Game/Assets/character/RealFace/SK_'+variant+'_Face';newpath=oldpath.replace('4522','ND01',1);newobj=newpath.rsplit('/',1)[1];gid=lambda s:(cityhash.CityHash64(s.lower().encode('utf-16le'))&((1<<62)-1))|(2<<62)
assert struct.unpack_from('<Q',new,em+72+56)[0]==gid(oldpath+'/'+oldpath.rsplit('/',1)[1]);struct.pack_into('<Q',new,em+72+56,gid(newpath+'/'+newobj))
(r/'asset').mkdir(exist_ok=True);(r/'asset'/(newobj+'.uasset')).write_bytes(new)
report={'target_card_id':'88044950524330','visible_vertices':n,'total_vertices':nv,'triangles':len(idx)//3,'native_bones':166,'bone_map':face_bonemap,'neck_source':'Ronaldo 2006 mesh0 and lower throat, source weights explicitly retargeted','mask_weight':'sk_head 1.0; no jaw/lip animation applied to rigid mask','phone_tested':False};(r/('asset-build-'+variant+'.json')).write_text(json.dumps(report,indent=2));print(variant,nv,'vertices',len(face_bonemap),'draw bones')
