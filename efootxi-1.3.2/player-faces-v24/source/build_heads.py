"""Four supplied Ronaldo source sets; explicit PES17/FMDL models and native rig.
Only the native skeleton, accessory geometry and material templates are reused.
No Android renderer verification is claimed.
"""
from pathlib import Path
import sys,struct,json,hashlib,ast
import numpy as np
from scipy.spatial import cKDTree
from PIL import Image
from iostore import Toc
from bundle_tools import Bundle,replace_texture,decode_first_texture
from mesh_tools import Mesh,write_native_lods,platform_lod_properties
from shading_tools import repair_frame
from zen_clone import rename,pid
R=Path('/workspace/ronaldo-work');O=Path(__file__).resolve().parent.parent;BASE='/Game/Assets/character/RealFace/'
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
old=Toc(str(O.parent/'player-faces-v23/container/pc9298_mobile_and.utoc'));bundle=Bundle(old)
# Four targets now select new independent profiles; prune their superseded skins.
for path in list(bundle.files):
 if any(Path(path).name.startswith(prefix+code)for prefix in ['SK_','T_','MI_']for code in ['NW01','NW27','NWJR']):bundle.files.pop(path)
from source_models import load
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
# Each selected card gets an independent profile; retained assets stay byte exact.
profiles=[('rp','NX01','NXH1',['','lg00v0000','ep01v0291','ep00v0313']),('prince','NXJR','NXHJ',['ep00v0313']),('fifa','NXNC','NXHN',['ep00v0313']),('2027','NX27','NXH7',['','lg00v0000','ep01v0291','ep00v0313'])];rows=[]
for label,profile,haircode,suffixes in profiles:
 root,f,hair=load(label)
 skinmeshes=[mm for mm in f.meshes if mm.materialInstance.name.startswith('fox_skin_mat')and not getattr(mm,'skip_native',False)]+[mm for mm in hair.meshes if mm.materialInstance.name.startswith('fox_skin_mat')and not getattr(mm,'skip_native',False)]
 pos,uv,tri,tan=arrays(skinmeshes)
 if label!='fifa':tri=tri[:,::-1].copy()  # ModelFile vs FMDL index convention differs.
 # Preserve every real opaque head/neck/scalp pass; do not discard head_phong.
 hairmeshes=[mm for mm in hair.meshes if not getattr(mm,'skip_native',False)and mm.materialInstance.name not in ['fox_skin_mat','fox_head_shell_mat'] and 'eye'not in mm.materialInstance.name and any(role=='Base_Tex_SRGB'for role,t in mm.materialInstance.textures)]
 hp,hu,ht,hn=arrays(hairmeshes);assert len(hp)>100
 if label!='fifa':ht=ht[:,::-1].copy()
 face_name='face_bsm_alp.png'if label=='fifa'else'face.png';srcface=Image.open(root/'converted'/face_name).convert('RGBA').resize((1024,1024));face_atlas=Image.new('RGBA',(2048,1024));face_atlas.paste(srcface,(0,0));face_atlas.paste(srcface,(1024,0))
 cursor=0
 for mm in skinmeshes:
  if getattr(mm,'base_is_hair',False):
   tex=next(t.filename for role,t in mm.materialInstance.textures if role=='Base_Tex_SRGB');face_atlas.paste(Image.open(root/'converted'/Path(tex).with_suffix('.png').name).convert('RGBA').resize((1024,1024)),(1024,0));uv[cursor:cursor+len(mm.vertices),0]+=1
  cursor+=len(mm.vertices)
 hairatlas=Image.new('RGBA',(2048,2048),(0,0,0,0));textures={};cursor=0
 for mm in hairmeshes:
  tex=next(t.filename for role,t in mm.materialInstance.textures if role=='Base_Tex_SRGB')
  # Preserve the prior phone-visible FIFA hair representation; complex FOX
  # dual-texture shading is not a native shader port.
  if label=='fifa':tex='hair_parts_bsm_alp.dds'
  if tex not in textures:
   tile=len(textures);assert tile<4;textures[tex]=tile;hairatlas.paste(Image.open(root/'converted'/Path(tex).with_suffix('.png').name).convert('RGBA').resize((1024,1024)),(tile%2*1024,tile//2*1024))
  tile=textures[tex];hu[cursor:cursor+len(mm.vertices)]=(hu[cursor:cursor+len(mm.vertices)]+[tile%2,tile//2])/2;cursor+=len(mm.vertices)
 for suffix in suffixes:
  template='SK_ND06'+suffix+'_Face';data=read(template);log=(O.parent/'player-faces-v20/references/ND06'/('v10-ND06'+suffix+'.log')).read_text();m=Mesh(data,log,0);native=Mesh(data,log,1);ns=m.info[0]['verts'];pcns=ns-135;nt=m.info[0]['tris'];p=m.positions[:ns].copy()
  # Donor accessory geometry follows supplied eye opening and mouth without
  # transferring PC bone indices. Named Android eye/jaw weights are unchanged.
  oc=[x for x in f.meshes if any(t.filename.startswith('eye_occlusion') for role,t in x.materialInstance.textures)];op=np.array([[v.position.x*100,v.position.z*100,v.position.y*100] for mm in oc for v in mm.vertices]);weights=[dict(r) for r in m.global_weights(0)]
  for side,bone in [('l',14),('r',15)]:
   ids=[i for i in range(pcns,ns) if weights[i].get(bone,0)>127];target=op[op[:,0]>0] if side=='l' else op[op[:,0]<0]
   if not len(target) or not ids:continue
   delta=target.mean(0)-p[ids].mean(0)
   if np.linalg.norm(delta)<3:p[ids]+=delta
  # Translate internal mouth from the proven donor lip anchor to supplied
  # target lips. Native jaw/head weights, 135 accessory vertices stay native.
  donorface=model(O.parent/'player-faces-v20/references/ND06/face_high.fmdl')
  def lip_anchor(face):
   ps=[];ws=[]
   for mm in face.meshes:
    if not mm.materialInstance.name.startswith('fox_skin_mat'):continue
    for vv in mm.vertices:
     w=sum(w for bone,w in vv.boneMapping.items() if (bone if isinstance(bone,str)else bone.name).startswith('skf_lip_'))
     if w>.3:ps.append([vv.position.x*100,vv.position.z*100,vv.position.y*100]);ws.append(w)
   return np.average(ps,axis=0,weights=ws),np.std(np.array(ps)[:,0])
  src_anchor,src_width=lip_anchor(f);donor_anchor,donor_width=lip_anchor(donorface);delta=src_anchor-donor_anchor;assert np.linalg.norm(delta)<4
  oral=[i for i in range(pcns,ns) if 14 not in weights[i] and 15 not in weights[i]]
  p[oral,0]=donor_anchor[0]+(p[oral,0]-donor_anchor[0])*np.clip(src_width/donor_width,.75,1.25);p[oral]+=delta
  # Keep supplied topology and UVs; no donor UV-based shape interpolation.
  donor_pcns=pcns;donor_ns=ns
  bone_names=json.loads((R/'native-export/Game/Assets/character/RealFace/SK_4522ep00v0313_Face.gltf').read_text());boneids={bone_names['nodes'][v]['name']:i for i,v in enumerate(bone_names['skins'][0]['joints'])}
  alias={'sk_neck':'sk_cervicalspine_02','sk_chest':'sk_spine_03','dsk_neckback':'sk_cervicalspine_01','dsk_scm':'sk_cervicalspine_02','dsk_clavicle_l':'sk_spine_03','dsk_clavicle_r':'sk_spine_03'}
  def mapped(name):
   if name in boneids:return {boneids[name]:1.}
   if name in alias:return {boneids[alias[name]]:1.}
   if name.startswith('dsk_ear'):return {7:1.}
   if name.startswith('dsk_collar'):return {boneids['sk_cervicalspine_02']:1.}
   if name.startswith('skf_lip_b_') or name=='skf_doublechin':return {8:1.}
   if name.startswith('skf_lip_s_') or name=='skf_lip_volume':return {7:.5,8:.5}
   if name.startswith('skf_cheek'):return {7:.8,8:.2}
   if name.startswith('skf_'):return {7:1.}
   raise ValueError(name)
  source_rows=[]
  for mm in skinmeshes:
   for v in mm.vertices:
    row={}
    for bone,w in v.boneMapping.items():
     for k,factor in mapped(bone if isinstance(bone,str)else bone.name).items():row[k]=row.get(k,0)+w*factor
    source_rows.append(row)
  # Low neck uses nearby donor neck weights; no shoulder/limb bone guesses.
  donor_rows=[dict(row)for row in m.global_weights(0)];low=np.flatnonzero((pos[:,2]<161.5)&(pos[:,1]<13.5));native_ids=np.flatnonzero((m.positions[:donor_pcns,2]<163)&(m.positions[:donor_pcns,1]<13.5));tree=cKDTree(m.positions[native_ids]);_,nearest=tree.query(pos[low])
  for i,j in zip(low,nearest):source_rows[int(i)]=donor_rows[int(native_ids[j])].copy()
  # UV-split skin seams move together, excluding deliberate upper/lower lips.
  shared={}
  for i,pt in enumerate(pos):shared.setdefault(tuple(np.round(pt,3)),[]).append(i)
  for ids in shared.values():
   if len(ids)<2:continue
   palette=set().union(*(source_rows[i]for i in ids))
   sameuv=np.max(np.linalg.norm(uv[ids]-uv[ids[0]],axis=1))<.0001
   if not sameuv and not palette<={4,5,6,7}:continue
   row={k:sum(source_rows[i].get(k,0)for i in ids)/len(ids)for k in palette}
   for i in ids:source_rows[i]=row.copy()
  acc_tri=m.indices[:nt];acc_tri=acc_tri[(acc_tri>=donor_pcns).all(1)]-donor_pcns
  pcns=len(pos);ns=pcns+135
  skin_uv=np.c_[uv*.5,np.full((pcns,2),3.0517578125e-5)].astype('<f2')
  source_tan=repair_frame(pos,tan,skin_uv,tri,derive=True);hn=repair_frame(hp,hn,hu,ht,derive=True)
  pp=np.concatenate([pos,p[donor_pcns:donor_ns],hp]);tn=np.concatenate([source_tan,m.tangents[donor_pcns:donor_ns],hn]);uvs=np.concatenate([skin_uv,m.uv[donor_pcns:donor_ns],np.c_[hu,np.full((len(hu),2),3.0517578125e-5)].astype('<f2')]);colors=np.concatenate([np.full((pcns,4),255,dtype='u1'),m.colors[donor_pcns:donor_ns],np.full((len(hp),4),255,dtype='u1')]);tr=np.concatenate([tri,acc_tri+pcns,ht+ns]);weights=source_rows+donor_rows[donor_pcns:donor_ns];nt=len(tri)+len(acc_tri);active=list(range(16))
  raw=write_native_lods(native,native,pp,tn,uvs,weights,colors,tr,ns,nt,active)
  name='SK_'+profile+suffix+'_Face';kind='FaceUpcon' if suffix=='lg00v0000' else 'FaceLegacy';im={}
  for q in ['HQ','MQ']:
   im[BASE+'MI_ND0006_Head_Hair_'+q]=BASE+'MI_'+haircode+'_Head_Hair_'+q;im[BASE+'MI_ND06'+suffix+'_Head_'+kind+'_'+q]=BASE+'MI_'+profile+suffix+'_Head_'+kind+'_'+q
  rep={BASE+template:BASE+name,template:name}
  for a,b in im.items():rep[a]=b;rep[a.split('/')[-1]]=b.split('/')[-1]
  raw=rename(raw,rep,BASE+template,BASE+name,imports=im);raw,_=platform_lod_properties(raw,True);put(name,raw,template,{pid(a):pid(b) for a,b in im.items()})
  for channel in ['D','N','SRO']:
   template_tex='T_ND06'+suffix+'_Face_'+channel;newtex='T_'+profile+suffix+'_Face_'+channel;raw=read(template_tex);bulk=read(template_tex,'ubulk')
   if channel in ['D','N','SRO']:
    # Preserve native eye/oral atlas and donor mip descriptors exactly; only
    # substitute the source skin quadrant, never an engine bake/render target.
    atlas=decode_first_texture(raw,bulk)
    if channel=='D':src=face_atlas
    elif channel=='N':
     a=np.array(Image.open(root/'converted'/('face_nrm.png'if label=='fifa'else'face_normal.png')).convert('RGBA'),dtype=float)/255;x=a[:,:,3]*2-1;y=a[:,:,1]*2-1;length=np.maximum(1,np.sqrt(x*x+y*y));x/=length;y/=length;z=np.sqrt(np.maximum(0,1-x*x-y*y));rgb=(np.stack([x,y,z],axis=-1)+1)*127.5;src=Image.fromarray(np.uint8(np.clip(rgb,0,255))).convert('RGBA')
    else:
     # Use the proven native skin response, without projecting old UV-specific AO.
     a=np.array(atlas.crop((0,0,1024,1024)));color=tuple(np.median(a[256:700,256:780].reshape(-1,4),axis=0).astype('u1'));src=Image.new('RGBA',(1024,1024),color)
    atlas.paste(src,(0,0));
    if src.width==1024:atlas.paste(src,(1024,0))
    if channel=='N'and label!='fifa':atlas.paste(Image.new('RGBA',(1024,1024),(128,128,255,255)),(1024,0))
    raw,bulk,_,_=replace_texture(raw,atlas,bulk)
   raw=rename(raw,{BASE+template_tex:BASE+newtex,template_tex:newtex},BASE+template_tex,BASE+newtex);put(newtex,raw,template_tex);put(newtex,bulk,template_tex,e='ubulk')
  for q in ['HQ','MQ']:
   template_mat='MI_ND06'+suffix+'_Head_'+kind+'_'+q;name='MI_'+profile+suffix+'_Head_'+kind+'_'+q;im={BASE+'T_ND06'+suffix+'_Face_'+c:BASE+'T_'+profile+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+template_mat:BASE+name,template_mat:name}
   for a,b in im.items():rep[a]=b;rep[a.split('/')[-1]]=b.split('/')[-1]
   put(name,rename(read(template_mat),rep,BASE+template_mat,BASE+name,imports=im),template_mat,{pid(a):pid(b) for a,b in im.items()})
  rows.append({'label':label,'profile':profile+suffix,'skin_topology_vertices':pcns,'accessory_vertices':135,'hair_vertices':len(hp),'source_UVs_preserved_except_explicit_scalp_atlas_tile':True,'all_opaque_source_face_neck_scalp_passes_kept':True,'native166_skeleton_unchanged':True,'full_native_required_bones_per_LOD':True,'source_skin_geometry_UVs_and_triangles_preserved':True,'named_retarget_to_native_skeleton':True,'source_hair_geometry_used':True,'phone_verified':False})
 # Each profile has independent native hair materials and a multi-texture atlas.
 template='T_ND0006_Hair_D';name='T_'+haircode+'_Hair_D';raw,bulk,dims,_=replace_texture(read(template),hairatlas,read(template,'ubulk'));raw=rename(raw,{BASE+template:BASE+name,template:name},BASE+template,BASE+name);put(name,raw,template);put(name,bulk,template,e='ubulk')
 for q in ['HQ','MQ']:
  t='MI_ND0006_Head_Hair_'+q;n='MI_'+haircode+'_Head_Hair_'+q;im={BASE+template:BASE+name};rep={BASE+t:BASE+n,t:n,BASE+template:BASE+name,template:name};put(n,rename(read(t),rep,BASE+t,BASE+n,imports=im),t,{pid(a):pid(b)for a,b in im.items()})
bundle.write(O/'container');(O/'head-build.json').write_text(json.dumps({'status':'BUILT_NOT_DEVICE_VERIFIED','method':'three independent supplied 2017 sources plus supplied 2027 PES17, native rig and all opaque skin/head/scalp passes','heads':rows,'black_face_root_cause_proven':False,'phone_tested':False},indent=2));print('Built',len(rows),'head variants')
