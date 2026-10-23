"""Rebuild five heads using the phone-proven ND06 exterior topology and rig.
UV correspondence transfers supplied PC shape to that topology. Source hair
uses original geometry/alpha. This changes the failing vertex layout, unlike
v18's header-only rebase. No Android renderer verification is claimed.
"""
from pathlib import Path
import sys,struct,json,hashlib,ast
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image
from iostore import Toc
from bundle_tools import Bundle,replace_texture,decode_first_texture
from mesh_tools import Mesh,write_native_lods,platform_lod_properties
from zen_clone import rename,pid
R=Path('/workspace/ronaldo-work');O=Path(__file__).resolve().parent.parent;BASE='/Game/Assets/character/RealFace/'
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
old=Toc(str(O.parent/'player-faces-v19/container/pc9298_mobile_and.utoc'));bundle=Bundle(old)
# Superseded failing private namespaces are no longer selected. Keep their
# original hair assets and every approved head; avoid two copies of large stacks.
for path in list(bundle.files):
 if any(Path(path).name.startswith(prefix+profile) for prefix in ['SK_','T_','MI_'] for profile in ['NV01','NV27','NVJR','NVHD']):bundle.files.pop(path)
def read(n,e='uasset'):return old.read(old.files['character/RealFace/'+n+'.'+e])
def put(n,b,template,imports=None,e='uasset'):
 source='character/RealFace/'+template+'.uasset';pk=int.from_bytes(old.ids[old.files[source]][:8],'little');fixed,im=bundle.entries[pk];entry=(fixed,[(imports or {}).get(k,k) for k in im]) if e=='uasset' else None
 bundle.put('character/RealFace/'+n+'.'+e,struct.pack('<Q',pid(BASE+n))+b'\0\0\0'+(b'\2' if e=='uasset' else b'\3'),b,entry)
def model(p):f=FmdlFile();f.readFile(str(p));return f
def arrays(meshes):
 pp=[];uu=[];tt=[];nn=[]
 for m in meshes:
  off=len(pp);ix={id(v):off+i for i,v in enumerate(m.vertices)}
  for v in m.vertices:pp.append([v.position.x*100,v.position.z*100,v.position.y*100]);uu.append([v.uv[0].u,v.uv[0].v]);nn.append([v.tangent.x,v.tangent.z,v.tangent.y,v.tangent.w,v.normal.x,v.normal.z,v.normal.y,-v.tangent.w])
  tt.extend([[ix[id(v)] for v in reversed(t.vertices)] for t in m.faces])
 return np.array(pp,dtype='<f4'),np.array(uu),np.array(tt,dtype='<u2'),np.clip(np.rint(np.array(nn)*127),-127,127).astype('i1').view('u1')
def transfer(target_uv,donor_pos,pos,uv,tri):
 a=uv[tri];v0=a[:,1]-a[:,0];v1=a[:,2]-a[:,0];det=v0[:,0]*v1[:,1]-v1[:,0]*v0[:,1];valid=np.abs(det)>1e-10;a=a[valid];tri=tri[valid];v0=v0[valid];v1=v1[valid];det=det[valid];tree=cKDTree(a.mean(1));_,candidates=tree.query(target_uv,k=min(96,len(a)));out=[];errors=[]
 for q,p,ids in zip(target_uv,donor_pos,candidates):
  d=q-a[ids,0];b=(d[:,0]*v1[ids,1]-d[:,1]*v1[ids,0])/det[ids];c=(v0[ids,0]*d[:,1]-v0[ids,1]*d[:,0])/det[ids];w=np.stack([1-b-c,b,c],axis=1);inside=w.min(1)>=-1e-4;clamped=np.maximum(w,0);clamped/=clamped.sum(1)[:,None];xyz=np.einsum('ij,ijk->ik',clamped,pos[tri[ids]]);uvq=np.einsum('ij,ijk->ik',clamped,a[ids]);uvdist=np.linalg.norm(uvq-q,axis=1);score=np.linalg.norm(xyz-p,axis=1)+uvdist*1000+np.where(inside,0,1);i=score.argmin();out.append(xyz[i]);errors.append(float(uvdist[i]))
 return np.array(out,dtype='<f4'),errors
# Four legacy profiles are kept present for diagnostics; fresh profiles select
# only newly built assets. Other approved nine heads remain byte-identical.
profiles=[('2017','NW01','ND0001',['','lg00v0000','ep01v0291','ep00v0313']),('2027','NW27','ND0027',['','lg00v0000','ep01v0291','ep00v0313']),('junior','NWJR','ND00JR',['ep00v0313']),('hoang-duc','NWHD','ND00HD',['ep00v0313']),('ozil','NWOZ','NW00OZ',['ep00v0313'])];rows=[]
for label,profile,haircode,suffixes in profiles:
 root=R/'v20-input'/label if label in ['2017','2027','ozil'] else O/'references/source-models'/label
 f=model(next(root.rglob('face_high.fmdl')));hair=model(next(root.rglob('hair_high.fmdl')))
 skinmeshes=[m for m in f.meshes if m.materialInstance.name.startswith('fox_skin_mat')]+[m for m in hair.meshes if m.materialInstance.name.startswith(('fox_skin_mat','fox_head_shell_mat')) and any(role=='Base_Tex_SRGB' and t.filename=='face_bsm_alp.dds' for role,t in m.materialInstance.textures)]
 pos,uv,tri,tan=arrays(skinmeshes);hairmeshes=[m for m in hair.meshes if any(t.filename.startswith('hair_parts') and role in ['Base_Tex_SRGB','Base_Tex_2_SRGB'] for role,t in m.materialInstance.textures)];hp,hu,ht,hn=arrays(hairmeshes);assert len(hp)>100
 for suffix in suffixes:
  template='SK_ND06'+suffix+'_Face';data=read(template);log=(O/'references/ND06'/('v10-ND06'+suffix+'.log')).read_text();m=Mesh(data,log,0);native=Mesh(data,log,1);ns=m.info[0]['verts'];pcns=ns-135;nt=m.info[0]['tris'];p=m.positions[:ns].copy();newp,err=transfer(m.uv[:pcns,:2].astype(float)*2,p[:pcns],pos,uv,tri);# Retain the proven smooth lower neck; blend into source upper geometry.
  neck=(m.positions[:pcns,2]<165.5)&(m.positions[:pcns,1]<13.5);blend=np.clip((m.positions[:pcns,2]-161.5)/4.,0,1);newp[neck]=m.positions[:pcns][neck]*(1-blend[neck,None])+newp[neck]*blend[neck,None]
  # Preserve geometric seam closure of the donor exterior even when source
  # UV islands carry slightly different duplicate border positions.
  groups={}
  for i,pt in enumerate(m.positions[:pcns]):groups.setdefault(tuple(np.round(pt,3)),[]).append(i)
  for ids in groups.values():
   if len(ids)>1 and np.max(np.linalg.norm(newp[ids]-newp[ids[0]],axis=1))<.8:newp[ids]=newp[ids].mean(0)
  p[:pcns]=newp
  # Donor accessory geometry follows supplied eye opening and mouth without
  # transferring PC bone indices. Named Android eye/jaw weights are unchanged.
  oc=next(x for x in f.meshes if x.materialInstance.name.startswith('fox_eyeOcclusion_mat'));op=np.array([[v.position.x*100,v.position.z*100,v.position.y*100] for v in oc.vertices]);weights=[dict(r) for r in m.global_weights(0)]
  for side,bone in [('l',14),('r',15)]:
   ids=[i for i in range(pcns,ns) if weights[i].get(bone,0)>127];target=op[op[:,0]>0] if side=='l' else op[op[:,0]<0];delta=target.mean(0)-p[ids].mean(0)
   if np.linalg.norm(delta)<3:p[ids]+=delta
  # Translate internal mouth from the proven donor lip anchor to supplied
  # target lips. Native jaw/head weights, 135 accessory vertices stay native.
  donorface=model(O/'references/ND06/face_high.fmdl')
  def lip_anchor(face):
   ps=[];ws=[]
   for mm in face.meshes:
    if not mm.materialInstance.name.startswith('fox_skin_mat'):continue
    for vv in mm.vertices:
     w=sum(w for bone,w in vv.boneMapping.items() if bone.name.startswith('skf_lip_'))
     if w>.3:ps.append([vv.position.x*100,vv.position.z*100,vv.position.y*100]);ws.append(w)
   return np.average(ps,axis=0,weights=ws),np.std(np.array(ps)[:,0])
  src_anchor,src_width=lip_anchor(f);donor_anchor,donor_width=lip_anchor(donorface);delta=src_anchor-donor_anchor;assert np.linalg.norm(delta)<4
  oral=[i for i in range(pcns,ns) if 14 not in weights[i] and 15 not in weights[i]]
  p[oral,0]=donor_anchor[0]+(p[oral,0]-donor_anchor[0])*np.clip(src_width/donor_width,.75,1.25);p[oral]+=delta
  # Preserve full native RequiredBones and stable ND06 skin palettes/UV/frame.
  pp=np.concatenate([p,hp]);tn=np.concatenate([m.tangents[:ns],hn]);uvs=np.concatenate([m.uv[:ns],np.c_[hu,np.full((len(hu),2),3.0517578125e-5)].astype('<f2')]);colors=np.concatenate([m.colors[:ns],np.full((len(hp),4),255,dtype='u1')]);tr=np.concatenate([m.indices[:nt],ht+ns]);active=[0,1,2,3,4,5,6,7,8,10,11,12,13,14,15]
  raw=write_native_lods(native,native,pp,tn,uvs,weights,colors,tr,ns,nt,active)
  # Keep each proven donor LOD's exact influence bytes, including tie order
  # and pre-existing LOD1 rounding. Re-deriving LOD1 from quantized LOD0 can
  # shift a weight by one byte; that is unnecessary for a topology donor.
  sh=bytearray(native.swhead);struct.pack_into('<II',sh,10,len(pp)*4,len(pp));pattern=bytes(sh)+struct.pack('<II',1,len(pp)*8);found=[];at=0
  while True:
   at=raw.find(pattern,at)
   if at<0:break
   found.append(at+len(pattern));at+=len(pattern)
  assert len(found)==2 and m.info[0]['bones']==sorted({k for row in weights for k in row})
  raw=bytearray(raw)
  for at,donor in zip(found,[m,native]):raw[at:at+ns*8]=donor.weights[:ns].tobytes()
  raw=bytes(raw);name='SK_'+profile+suffix+'_Face';kind='FaceUpcon' if suffix=='lg00v0000' else 'FaceLegacy';im={}
  for q in ['HQ','MQ']:
   im[BASE+'MI_ND0006_Head_Hair_'+q]=BASE+'MI_'+haircode+'_Head_Hair_'+q;im[BASE+'MI_ND06'+suffix+'_Head_'+kind+'_'+q]=BASE+'MI_'+profile+suffix+'_Head_'+kind+'_'+q
  rep={BASE+template:BASE+name,template:name}
  for a,b in im.items():rep[a]=b;rep[a.split('/')[-1]]=b.split('/')[-1]
  raw=rename(raw,rep,BASE+template,BASE+name,imports=im);raw,_=platform_lod_properties(raw,True);put(name,raw,template,{pid(a):pid(b) for a,b in im.items()})
  for channel in ['D','N','SRO']:
   template_tex='T_ND06'+suffix+'_Face_'+channel;newtex='T_'+profile+suffix+'_Face_'+channel;raw=read(template_tex);bulk=read(template_tex,'ubulk')
   if channel=='D':
    # Preserve native eye/oral atlas and donor mip descriptors exactly; only
    # substitute the source skin quadrant, never an engine bake/render target.
    atlas=decode_first_texture(raw,bulk);src=Image.open(root/'converted/face_bsm_alp.png').convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS);atlas.paste(src,(0,0));atlas.paste(src,(1024,0));raw,bulk,_,_=replace_texture(raw,atlas,bulk)
   raw=rename(raw,{BASE+template_tex:BASE+newtex,template_tex:newtex},BASE+template_tex,BASE+newtex);put(newtex,raw,template_tex);put(newtex,bulk,template_tex,e='ubulk')
  for q in ['HQ','MQ']:
   template_mat='MI_ND06'+suffix+'_Head_'+kind+'_'+q;name='MI_'+profile+suffix+'_Head_'+kind+'_'+q;im={BASE+'T_ND06'+suffix+'_Face_'+c:BASE+'T_'+profile+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+template_mat:BASE+name,template_mat:name}
   for a,b in im.items():rep[a]=b;rep[a.split('/')[-1]]=b.split('/')[-1]
   put(name,rename(read(template_mat),rep,BASE+template_mat,BASE+name,imports=im),template_mat,{pid(a):pid(b) for a,b in im.items()})
  rows.append({'label':label,'profile':profile+suffix,'skin_topology_vertices':pcns,'accessory_vertices':135,'hair_vertices':len(hp),'UV_correspondence_max_error':max(err),'native166_skeleton_unchanged':True,'full_native_required_bones_per_LOD':True,'donor_skin_UV_weights_tangents_and_triangles_preserved':True,'source_hair_geometry_used':True,'phone_verified':False})
 # New Ozil hair material/texture, source alpha retained through ETC2RGBA.
 if label=='ozil':
  src=Image.open(root/'converted/hair_parts_bsm_alp.png').convert('RGBA');template='T_ND0006_Hair_D';name='T_'+haircode+'_Hair_D';raw,bulk,dims,_=replace_texture(read(template),src,read(template,'ubulk'));raw=rename(raw,{BASE+template:BASE+name,template:name},BASE+template,BASE+name);put(name,raw,template);put(name,bulk,template,e='ubulk')
  for q in ['HQ','MQ']:
   t='MI_ND0006_Head_Hair_'+q;n='MI_'+haircode+'_Head_Hair_'+q;im={BASE+template:BASE+name};rep={BASE+t:BASE+n,t:n,BASE+template:BASE+name,template:name};put(n,rename(read(t),rep,BASE+t,BASE+n,imports=im),t,{pid(a):pid(b) for a,b in im.items()})
bundle.write(O/'heads-container');(O/'head-build.json').write_text(json.dumps({'status':'BUILT_NOT_DEVICE_VERIFIED','method':'ND06 exterior topology UV correspondence, source shape and source hair','heads':rows,'black_face_root_cause_proven':False,'phone_tested':False},indent=2));print('Built',len(rows),'head variants')
