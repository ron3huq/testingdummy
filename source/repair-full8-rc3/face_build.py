"""V8 skin + native animated oral/eye geometry; independent native low LOD.
No source script from the uploaded archive is executed.
"""
from pathlib import Path
import sys,struct,json,inspect,collections,hashlib
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image,ImageDraw
sys.path[:0]=['/workspace/work/full8/recovered-tools','/workspace/ronaldo-work/pes-fmdl-blender/pes-fmdl']
from iostore import Toc
from bundle_tools import Bundle,decode_first_texture,replace_texture
from mesh_tools import Mesh,quantize,platform_lod_properties
from shading_tools import repair_frame
from zen_clone import rename,pid
from FmdlFile import FmdlFile
R=Path('/workspace/work/full8-rc3/face');PAY=Path('/workspace/work/full8/candidate');LIVE=PAY/'assets/gateway-release/livedata';BASE='/Game/Assets/character/RealFace/'
old=Toc(str(LIVE/'pc9317_mobile_and.utoc'));donor=Toc(str(LIVE/'pc9298_mobile_and.utoc'))
original=Bundle(old);out=Bundle(old);out.files={};out.entries={}
def get(t,n,e='uasset'):return t.read(t.files['character/RealFace/'+n+'.'+e])
def put(n,data,template,remap=None,e='uasset'):
 key='character/RealFace/'+template+'.uasset';pk=int.from_bytes(old.ids[old.files[key]][:8],'little');fixed,deps=original.entries[pk]
 entry=(fixed,[(remap or{}).get(x,x)for x in deps])if e=='uasset'else None
 out.put('character/RealFace/'+n+'.'+e,struct.pack('<Q',pid(BASE+n))+b'\0\0\0'+(b'\2'if e=='uasset'else b'\3'),data,entry)
def model(p):f=FmdlFile();f.readFile(str(p));return f
face=model(R/'models/face_high.fmdl');pc_hair=model(R/'models/hair_high.fmdl');donor_pc=model(R/'donor_face_high.fmdl')
skin=[m for m in face.meshes if m.materialInstance.name=='fox_skin_mat']+[m for m in pc_hair.meshes if m.materialInstance.name=='fox_head_shell_mat']
def arrays(meshes):
 pp=[];uv=[];tri=[];tan=[]
 for m in meshes:
  ix={id(v):len(pp)+i for i,v in enumerate(m.vertices)}
  for v in m.vertices:
   pp.append([v.position.x*100,v.position.z*100,v.position.y*100]);uv.append([v.uv[0].u,v.uv[0].v]);tan.append([v.tangent.x,v.tangent.z,v.tangent.y,v.tangent.w,v.normal.x,v.normal.z,v.normal.y,-v.tangent.w])
  tri.extend([[ix[id(v)]for v in reversed(t.vertices)]for t in m.faces])
 return np.asarray(pp,dtype='<f4'),np.asarray(uv),np.asarray(tri,dtype='<u2'),np.clip(np.rint(np.asarray(tan)*127),-127,127).astype('i1').view('u1')
pcpos,pcuv,pctri,pctan=arrays(skin)
hair=np.load(R/'hair-native.npz');hairpos=hair['positions'];hairuv=hair['uv'];hairtri=hair['triangles'];hairtan=hair['tangents']
g=json.loads(Path('/workspace/ronaldo-work/native-export/Game/Assets/character/RealFace/SK_4522_Face.gltf').read_text());names=[g['nodes'][j]['name']for j in g['skins'][0]['joints']];boneids={n:i for i,n in enumerate(names)}
aliases={'sk_neck':6,'sk_chest':4,'dsk_neckback':5,'dsk_scm':6,'dsk_clavicle_l':4,'dsk_clavicle_r':4}
def mapped(n):
 if n in boneids:return {boneids[n]:1.}
 if n in aliases:return {aliases[n]:1.}
 if n.startswith('skf_lip_b_')or n=='skf_doublechin':return {8:1.}
 if n.startswith('skf_lip_s_')or n=='skf_lip_volume':return {7:.5,8:.5}
 if n.startswith('skf_cheek'):return {7:.8,8:.2}
 if n.startswith(('skf_nose','skf_nasolabial','skf_lip_t_','skf_brow','skf_orbicularisoculi','skf_glabella')):return {7:1.}
 raise ValueError('Unmapped source bone: '+n)
source_weights=[];source_features=[]
for m in skin:
 for v in m.vertices:
  row=collections.defaultdict(float)
  upper=sum(w for bone,w in v.boneMapping.items()if bone.name.startswith('skf_lip_t_'))
  lower=sum(w for bone,w in v.boneMapping.items()if bone.name.startswith('skf_lip_b_')or bone.name in ['skf_jaw','skf_doublechin'])
  lip_jaw=lower/(upper+lower)if upper+lower>.05 else .5
  for bone,w in v.boneMapping.items():
   targets={7:1-lip_jaw,8:lip_jaw}if bone.name.startswith('skf_lip_s_')or bone.name=='skf_lip_volume'else mapped(bone.name)
   # The PC lip-volume/corner controls serve both lips. A fixed 50% jaw
   # assignment drags the upper lip through itself when the jaw opens.
   for k,factor in targets.items():row[k]+=w*factor
  assert row and min(row.values())>=0
  source_weights.append(dict(row))
  dominant=max(v.boneMapping,key=v.boneMapping.get).name
  source_features.append(dominant if dominant.startswith(('skf_lip_t_','skf_lip_b_','skf_lip_s_','skf_eyelid_'))else'skin')
def accumulate(pairs):
 # Repeated lanes must add, never dict(pairs).
 d=collections.defaultdict(float)
 for k,v in pairs:d[k]+=v
 return dict(d)
def lip_anchor(f):
 p=[];weights=[]
 for m in f.meshes:
  if m.materialInstance.name!='fox_skin_mat':continue
  for v in m.vertices:
   w=sum(w for b,w in v.boneMapping.items()if b.name.startswith('skf_lip_'))
   if w>.3:p.append([v.position.x*100,v.position.z*100,v.position.y*100]);weights.append(w)
 return np.average(p,axis=0,weights=weights),np.std(np.array(p)[:,0])
anchor,width=lip_anchor(face);donor_anchor,donor_width=lip_anchor(donor_pc)

def pack(a):return struct.pack('<I',len(a))+struct.pack('<%dH'%len(a),*a)
def lod_blob(template,native,lod,positions,tangents,uv,rows,colors,tri,ns,nt):
 b=template.data;at=native.lods[lod];nreq=struct.unpack_from('<I',native.data,at+10)[0];req=list(struct.unpack_from('<%dH'%nreq,native.data,at+14));n=len(positions)
 if lod==0:
  skin_n=ns-135;skin_t=nt-len(atri)
  specs=[(template.info[0],skin_n,skin_t,0,0,rows[:skin_n],0),(template.info[1],n-ns,len(tri)-nt,nt*3,ns,[{7:255}]*(n-ns),1),(template.info[0],135,len(atri),skin_t*3,skin_n,rows[skin_n:],2)]
 else:specs=[(template.info[0],ns,nt,0,0,rows,2),(template.info[1],n-ns,len(tri)-nt,nt*3,ns,[{7:255}]*(n-ns),1)]
 specs.sort(key=lambda s:s[4])
 sections=[];weights=np.zeros((n,8),dtype='u1');used=set()
 for q,nv,ntri,bi,bv,r,material in specs:
  bm=sorted({k for row in r for k,v in row.items()if v>0});assert set(bm)<=set(req);used.update(bm)
  weights[bv:bv+nv]=quantize(r,bm)
  h=bytearray(q['head']);tail=bytearray(q['tail']);struct.pack_into('<H',h,2,material);struct.pack_into('<II',h,4,bi,ntri);struct.pack_into('<I',h,21,bv);struct.pack_into('<II',tail,0,nv,4);sections.append(bytes(h)+pack(bm)+tail)
 th=bytearray(template.tuhead);struct.pack_into('<I',th,6,n);sh=bytearray(template.swhead);struct.pack_into('<II',sh,10,n*4,n)
 stream=b[template.r['STREAM_BEGIN']:template.r['INDICES_BEGIN']]+struct.pack('<BII',2,2,tri.size)+tri.astype('<u2').tobytes()+struct.pack('<4I',12,n,12,n)+positions.astype('<f4').tobytes()
 stream+=bytes(th)+struct.pack('<II',8,n)+tangents.astype('u1').tobytes()+struct.pack('<II',4,n*2)+uv.astype('<f2').tobytes()
 stream+=bytes(sh)+struct.pack('<II',1,n*8)+weights.tobytes()+template.swtail+template.colhead+struct.pack('<4I',4,n,4,n)+colors.astype('u1').tobytes()+template.coltail
 active=used|{7}
 for k in list(active):
  while k>0:k=parents[k];active.add(k)
 assert active<=set(req)
 header=bytearray(b[template.lods[1]:template.lods[1]+10]);struct.pack_into('<II',header,2,0,1)
 return bytes(header)+pack(req)+struct.pack('<I',len(sections))+b''.join(sections)+pack(sorted(active))+struct.pack('<I',len(stream))+stream

# Triangle-surface interpolation keeps the low neck on the native body seam.
def surface_point(p,triangles):
 a,b,c=triangles[:,0],triangles[:,1],triangles[:,2];ab=b-a;ac=c-a;ap=p-a
 d00=(ab*ab).sum(1);d01=(ab*ac).sum(1);d11=(ac*ac).sum(1);d20=(ap*ab).sum(1);d21=(ap*ac).sum(1);den=d00*d11-d01*d01
 v=np.divide(d11*d20-d01*d21,den,out=np.zeros(len(den)),where=abs(den)>1e-12);w=np.divide(d00*d21-d01*d20,den,out=np.zeros(len(den)),where=abs(den)>1e-12)
 candidates=[]
 bary=np.c_[1-v-w,v,w];point=np.einsum('ij,ijk->ik',bary,triangles);dist=((point-p)**2).sum(1);dist[(bary<0).any(1)|(abs(den)<1e-12)]=np.inf;candidates.append((point,bary,dist))
 for i,j in [(0,1),(1,2),(2,0)]:
  a=triangles[:,i];d=triangles[:,j]-a;t=np.clip(((p-a)*d).sum(1)/np.maximum((d*d).sum(1),1e-12),0,1);q=a+t[:,None]*d;bary=np.zeros((len(t),3));bary[:,i]=1-t;bary[:,j]=t;candidates.append((q,bary,((q-p)**2).sum(1)))
 choice=min((float(x[2][k]),c,k)for c,x in enumerate(candidates)for k in range(len(triangles)));_,ci,ti=choice
 return candidates[ci][0][ti],candidates[ci][1][ti],ti

report=[]
for suffix,nlog in [('', 'native-.log'),('ep00v0313','native-ep00v0313.log'),('ep01v0291','native-ep01v0291.log'),('lg00v0000','native-lg00v0000.log')]:
 current='SK_NQ27'+suffix+'_Face';new='SK_RV8C'+suffix+'_Face';oldraw=get(old,current)
 oldmesh=Mesh(oldraw,(R/'logs'/(current+'.log')).read_text(),1)
 donorname='SK_ND06'+suffix+'_Face';dm=Mesh(get(donor,donorname),(R/'logs'/(donorname+'.log')).read_text(),0)
 native_raw=Path('/workspace/ronaldo-work/ronaldo-android-fit/extracted/SK_4522'+suffix+'_Face.uasset').read_bytes();nm=Mesh(native_raw,Path('/workspace/ronaldo-work',nlog).read_text(),1)
 na=nm.r['REF_BEGIN'];oa=oldmesh.r['REF_BEGIN'];count=struct.unpack_from('<I',native_raw,na)[0];assert count==166==struct.unpack_from('<I',oldraw,oa)[0]
 parents=[struct.unpack_from('<i',native_raw,na+4+i*12+8)[0]for i in range(166)]
 native_pose=native_raw[na+4+166*12+4:na+4+166*12+4+166*40]
 # Source skin with native surface and weights along the lower neck only.
 pos=pcpos.copy();rows=[dict(w)for w in source_weights];nns=nm.info[0]['verts'];ntri=nm.indices[:nm.info[0]['tris']];tree=cKDTree(nm.positions[ntri].mean(1));nrows=[accumulate(p)for p in nm.global_weights(0)]
 lower=np.flatnonzero(pos[:,2]<159);moves=[]
 for i in lower:
  _,near=tree.query(pos[i],k=min(32,len(ntri)));q,bary,at=surface_point(pos[i],nm.positions[ntri[near]]);ids=ntri[near[at]]
  blend=float(np.clip((159-pos[i,2])/5,0,1));blend=blend*blend*(3-2*blend);moves.append(float(np.linalg.norm(q-pos[i]))*blend);pos[i]=pos[i]*(1-blend)+q*blend
  combined=collections.defaultdict(float)
  for k,v in rows[i].items():combined[k]+=v*(1-blend)
  for j,factor in zip(ids,bary):
   for k,v in nrows[j].items():combined[k]+=v/255*factor*blend
  rows[i]=dict(combined)
 # Make UV-split neck duplicates share weights and positions, without merging lips.
 shared=collections.defaultdict(list)
 for i,p in enumerate(pcpos):
  category='neck'if p[2]<159 else source_features[i]
  shared[(tuple(np.round(p,3)),category)].append(i)
 for ix in shared.values():
  if len(ix)<2:continue
  avg=np.mean(pos[ix],axis=0);keys=set().union(*(rows[i]for i in ix));w={k:sum(rows[i].get(k,0)for i in ix)/len(ix)for k in keys}
  for i in ix:pos[i]=avg;rows[i]=w.copy()
 # The native eye/oral sections remain independently weighted, not fixed to head.
 # Recover genuine native4522 eye/oral islands by triangle connectivity.
 parent=list(range(nns))
 def root(v):
  while parent[v]!=v:v=parent[v]
  return v
 for tr in ntri:
  for v in tr[1:]:parent[root(int(v))]=root(int(tr[0]))
 groups=collections.defaultdict(list)
 for v in range(nns):groups[root(v)].append(v)
 native_acc=sorted(v for group in groups.values()if 1<len(group)<100 for v in group if v>=9 or v in range(3,9))
 assert len(native_acc)==135
 accpos=nm.positions[native_acc].copy();accuv=nm.uv[native_acc].copy();acctan=nm.tangents[native_acc].copy();acccolor=nm.colors[native_acc].copy();inverse={v:i for i,v in enumerate(native_acc)}
 atri=np.array([[inverse[int(v)]for v in tr]for tr in ntri if all(int(v)in inverse for v in tr)],dtype='<u2')
 accrows=[];mouth=[]
 for i,v in enumerate(native_acc):
  pt=nm.positions[v];uvn=nm.uv[v]
  if pt[2]>169:accrows.append({14 if pt[0]>0 else 15:255})
  else:accrows.append({8 if uvn[1]>.938 or pt[2]<165 or v in range(6,9) else 7:255});mouth.append(i)
 # Fit only the ocular surround to the native facial surface. Keep authored
 # facial weights; do not collapse eyelids to the head bone.
 main=max(groups.values(),key=len);mainset=set(main);eye_tri=ntri[np.array([all(int(v)in mainset for v in tr)for tr in ntri])];eye_tree=cKDTree(nm.positions[eye_tri].mean(1))
 eye_occlusion=next(m for m in face.meshes if m.materialInstance.name=='fox_eyeOcclusion_mat')
 source_occlusion=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for v in eye_occlusion.vertices]);source_centers=[];target_centers=[]
 for sign,bone in [(1,14),(-1,15)]:
  source_centers.append(source_occlusion[source_occlusion[:,0]*sign>0].mean(0));target_centers.append(accpos[[i for i,row in enumerate(accrows)if bone in row]].mean(0))
 source_centers=np.array(source_centers);target_centers=np.array(target_centers)
 for i,point in enumerate(pos.copy()):
  side=0 if point[0]>0 else 1;distance=np.linalg.norm((source_centers[side]-point)*np.array([1,.5,1]));blend=float(np.clip((3.1-distance)/1.4,0,1));blend=blend*blend*(3-2*blend)
  if blend<=0:continue
  shifted=point+(target_centers[side]-source_centers[side])*blend
  _,near=eye_tree.query(shifted,k=min(24,len(eye_tri)));q,_,_=surface_point(shifted,nm.positions[eye_tri[near]]);pos[i]=point*(1-blend)+q*blend
 # Latest user choice: supplied V8 hair, with its original topology and UVs.
 oldns=oldmesh.info[0]['verts'];hp=hairpos;hu=hairuv;ht=hairtri
 ns=len(pos)+135;uv=np.c_[pcuv*.5,np.full((len(pos),2),3.0517578125e-5)].astype('<f2');tn=repair_frame(pos,pctan,uv,pctri,derive=True)
 high=(np.concatenate([pos,accpos,hp]),np.concatenate([tn,acctan,hairtan]),np.concatenate([uv,accuv,hu]),rows+accrows,np.concatenate([np.full((len(pos),4),255,dtype='u1'),acccolor,np.full((len(hp),4),255,dtype='u1')]),np.concatenate([pctri,atri+len(pos),ht+ns]),ns,len(pctri)+len(atri))
 # Low LOD uses genuine native Ronaldo skin and native compact bones, not
 # PC facial weights collapsed to head. Hair remains the selected custom hair.
 lowuv=nm.uv[:nns].copy()
 low=(np.concatenate([nm.positions[:nns],hp]),np.concatenate([nm.tangents[:nns],hairtan]),np.concatenate([lowuv,hu]),nrows,np.concatenate([nm.colors[:nns],np.full((len(hp),4),255,dtype='u1')]),np.concatenate([ntri,ht+nns]),nns,len(ntri))
 prefix=bytearray(oldraw[:oldmesh.lods[0]])
 for i,parent in enumerate(parents):struct.pack_into('<i',prefix,oa+4+i*12+8,parent)
 poseat=oa+4+166*12+4;prefix[poseat:poseat+166*40]=native_pose
 pp=high[0];lo=pp.min(0);hi=pp.max(0);center=(hi+lo)/2;extent=(hi-lo)/2;struct.pack_into('<7f',prefix,oldmesh.r['BOUNDS_BEGIN'],*center,*extent,float(np.linalg.norm(extent)))
 data=bytearray(prefix+lod_blob(oldmesh,nm,0,*high)+lod_blob(oldmesh,nm,1,*low)+bytes.fromhex('020200000000'))
 em=struct.unpack_from('<I',oldraw,44)[0];struct.pack_into('<Q',data,em+80,struct.unpack_from('<Q',oldraw,em+80)[0]+len(data)-len(oldraw))
 kind='FaceUpcon'if suffix=='lg00v0000'else'FaceLegacy';mapping={BASE+'MI_NQ27'+suffix+'_Head_'+kind+'_'+q:BASE+'MI_RV8C'+suffix+'_Head_'+kind+'_'+q for q in ['HQ','MQ']}
 mapping.update({BASE+'MI_HQR7_Head_Hair_'+q:BASE+'MI_HV8C_Head_Hair_'+q for q in ['HQ','MQ']})
 mapping.update({BASE+'MI_HQR7_Head_FaceLegacy_'+q:BASE+'MI_RV8C'+suffix+'_Head_'+kind+'_'+q for q in ['HQ','MQ']})
 native_mat=BASE+'MI_4522'+suffix+'_Head_'+kind+'_HQ'
 mapping['/Game/Assets/MaterialLibrary/Character/Head/MasterMaterials/MI_Head_Eyelash01Occlusion00']=native_mat
 replacements={BASE+current:BASE+new,current:new}
 for a,b in mapping.items():replacements[a]=b;replacements[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
 data=rename(data,replacements,BASE+current,BASE+new,imports=mapping);data,lodprops=platform_lod_properties(data,True)
 # LOD1 originally redirects skin/hair to shared MQ slots 3/4. Keep its
 # native skin on isolated slot2 and V8 hair on slot1 instead.
 data=bytearray(data);f=struct.unpack_from('<16I',data);a=f[6];names2=[]
 for _ in range((f[9]-8)//8):
  h=int.from_bytes(data[a:a+2],'big');a+=2;n2=h&32767;wide=h>>15;names2.append(bytes(data[a:a+n2*(1+wide)]).decode('utf-16-le'if wide else'utf8'));a+=n2*(1+wide)
 key=struct.pack('<II',names2.index('LODMaterialMap'),0);a=f[13]+f[14];patched=0
 while (a:=data.find(key,a))>=0:
  if struct.unpack_from('<II',data,a+16)==(12,0)and struct.unpack_from('<III',data,a+33)==(2,3,4):struct.pack_into('<II',data,a+37,2,1);patched+=1
  a+=1
 assert patched==1
 data=bytes(data)
 put(new,data,current,{pid(a):pid(b)for a,b in mapping.items()})
 for channel in ['D','N','SRO']:
  template='T_NQ27'+suffix+'_Face_'+channel;newtex='T_RV8C'+suffix+'_Face_'+channel
  # Retain native eye/oral atlas; source skin uses its own authored UV quadrant.
  raw=get(old,template);bulk=get(old,template,'ubulk');atlas=decode_first_texture(get(donor,'T_ND06'+suffix+'_Face_'+channel),get(donor,'T_ND06'+suffix+'_Face_'+channel,'ubulk'))
  if channel=='D':
   im=Image.open(R/'textures/face_bsm_alp.png').convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS);im.putalpha(255)
  elif channel=='N':
   a=np.asarray(Image.open(R/'textures/face_nrm.png').convert('RGBA').resize((1024,1024)),dtype=float);x=a[:,:,0]/127.5-1;y=-(a[:,:,1]/127.5-1);length=np.maximum(1,np.sqrt(x*x+y*y));x/=length;y/=length;z=np.sqrt(np.maximum(0,1-x*x-y*y));im=Image.fromarray(np.uint8(np.clip((np.stack([x,y,z],axis=-1)+1)*127.5,0,255))).convert('RGBA')
  else:im=atlas.crop((0,0,1024,1024))
  native_texture=Path('/workspace/ronaldo-work/texture-export/Game/Assets/character/RealFace/T_4522'+suffix+'_Face_'+channel+'.png')
  assert native_texture.exists(),native_texture
  atlas.paste(im,(0,0));atlas.paste(Image.open(native_texture).convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS),(1024,0))
  raw,bulk,_,_=replace_texture(raw,atlas,bulk);raw=rename(raw,{BASE+template:BASE+newtex,template:newtex},BASE+template,BASE+newtex);put(newtex,raw,template);put(newtex,bulk,template,e='ubulk')
 for quality in ['HQ','MQ']:
  template='MI_NQ27'+suffix+'_Head_'+kind+'_'+quality;newmat='MI_RV8C'+suffix+'_Head_'+kind+'_'+quality;mapping={BASE+'T_NQ27'+suffix+'_Face_'+c:BASE+'T_RV8C'+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+template:BASE+newmat,template:newmat}
  for a,b in mapping.items():rep[a]=b;rep[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
  put(newmat,rename(get(old,template),rep,BASE+template,BASE+newmat,imports=mapping),template,{pid(a):pid(b)for a,b in mapping.items()})
 np.savez_compressed(R/('audit'+suffix+'.npz'),high_positions=high[0],high_triangles=high[5],high_skin_vertices=ns,high_weights=quantize(high[3],sorted({k for w in high[3]for k,v in w.items()if v>0})),high_bonemap=sorted({k for w in high[3]for k,v in w.items()if v>0}),native_pose=np.frombuffer(native_pose,dtype='<f4').reshape(166,10),mouth_indices=np.asarray(mouth)+len(pos))
 report.append(dict(asset=new,high_vertices=len(high[0]),low_vertices=len(low[0]),source_skin_vertices=len(pos),native_animated_accessories=135,face_bones=[8,10,11,12,13,14,15],low_native_required_bones=153,high_native_required_bones=166,body_bind_pose='exact native4522',neck_vertices_interpolated=len(lower),maximum_neck_surface_correction_cm=max(moves),native_lod_properties=lodprops,hair='V8 hair unchanged; native4522 ocular/oral geometry; PC diffuse alpha converted to native opaque alpha',hair_vertices=len(hp),hair_triangles=len(ht),device_verified=False))
# Hair texture/material get their own namespace; no inherited HQR7 textures.
template='T_HQR7_Hair_D';name='T_HV8C_Hair_D';raw,bulk,_,_=replace_texture(get(old,template),Image.open(R/'hair-native-uv0.png'),get(old,template,'ubulk'));raw=rename(raw,{BASE+template:BASE+name,template:name},BASE+template,BASE+name);put(name,raw,template);put(name,bulk,template,e='ubulk')
for q in ['HQ','MQ']:
 template='MI_HQR7_Head_Hair_'+q;name='MI_HV8C_Head_Hair_'+q;mapping={BASE+'T_HQR7_Hair_D':BASE+'T_HV8C_Hair_D'};rep={BASE+template:BASE+name,template:name,BASE+'T_HQR7_Hair_D':BASE+'T_HV8C_Hair_D','T_HQR7_Hair_D':'T_HV8C_Hair_D'};put(name,rename(get(old,template),rep,BASE+template,BASE+name,imports=mapping),template,{pid(a):pid(b)for a,b in mapping.items()})
container_report=[]
for number,marker in [(9336,None),(9337,'ep00v0313'),(9338,'ep01v0291'),(9339,'lg00v0000')]:
 part=Bundle.__new__(Bundle);part.base=out.base;part.entries=out.entries
 part.files={p:v for p,v in out.files.items()if(marker in p if marker else not any(s in p for s in ['ep00v0313','ep01v0291','lg00v0000']))}
 src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc"+str(number)+"_mobile_and'");scope={};exec('class Writer:\n'+src,Bundle.write.__globals__,scope);scope['Writer'].write(part,R/'built');container_report.append({'container':number,'files':len(part.files)})
(R/'containers.json').write_text(json.dumps(container_report,indent=2))
(R/'asset-build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
