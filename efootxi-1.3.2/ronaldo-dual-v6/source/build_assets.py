"""Build dual-card trial from v4a, public Android data, and supplied PC 2006 FMDL.
Usage: python build_assets.py WORKDIR. Does not modify any input or original game asset.
"""
from pathlib import Path
import sys,struct,json,re,subprocess,hashlib
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image,ImageFilter
import etcpak,texture2ddecoder
from mesh_tools import Mesh,quantize
from zen_clone import rename,pid
from iostore import Toc,parse_header,store_entry,build_store,dir_index
R=Path(sys.argv[1]).resolve();OUT=Path(__file__).resolve().parent.parent;ASSET=OUT/'asset';ASSET.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
BASE='/Game/Assets/character/RealFace/';SUFFIX=['','lg00v0000','ep01v0291','ep00v0313']
old=Toc(str(R/'v4a/livedata/pc9298_mobile_and.utoc'));heads=Toc(str(next((R/'resources').rglob('pc3700_mobile_and.utoc'))));mats=Toc(str(next((R/'resources').rglob('pc3611_mobile_and.utoc'))))
ref=Toc(str(R/'apk/assets/gateway-release/livedata/pc9257_mobile_and.utoc'))
recipes=[];reports=[];texture_reports=[]
def extract(t,path):return t.read(t.files[path])
def add(name,data,template,source,imports=None,bulk=None):
 (ASSET/(name+'.uasset')).write_bytes(data)
 if bulk is not None:(ASSET/(name+'.ubulk')).write_bytes(bulk)
 recipes.append((name,template,source,imports or {}))
def read_model(path):
 f=FmdlFile();f.readFile(str(path));return f
oldpc=read_model(R/'ronaldo-noodle-source/source-extracted/face_high.fmdl')
newroot=next((R/'input-1').rglob('face_high.fmdl')).parent
newface=read_model(newroot/'face_high.fmdl');newhair=read_model(newroot/'hair_high.fmdl')
# Exactly the same named skeleton as v4a. No guessed mapping for numbered bones.
gltf=json.loads((R/'native-export/Game/Assets/character/RealFace/SK_4522ep00v0313_Face.gltf').read_text());bones=[gltf['nodes'][i]['name'] for i in gltf['skins'][0]['joints']];boneids={v:i for i,v in enumerate(bones)};assert len(bones)==166
alias={'sk_neck':'sk_cervicalspine_02','sk_chest':'sk_spine_03','dsk_neckback':'sk_cervicalspine_01','dsk_scm':'sk_cervicalspine_02','dsk_clavicle_l':'sk_spine_03','dsk_clavicle_r':'sk_spine_03'}
def mapped(name):
 if name in boneids:return {boneids[name]:1.}
 if name in alias:return {boneids[alias[name]]:1.}
 if name.startswith('skf_lip_b_') or name=='skf_doublechin':return {boneids['skf_jaw']:1.}
 if name.startswith('skf_lip_s_') or name=='skf_lip_volume':return {boneids['sk_head']:.5,boneids['skf_jaw']:.5}
 if name.startswith('skf_cheek'):return {boneids['sk_head']:.8,boneids['skf_jaw']:.2}
 if name.startswith('skf_'):return {boneids['sk_head']:1.}
 raise ValueError(name)
def pc_arrays(meshes):
 verts=[];tri=[];rows=[]
 for m in meshes:
  start=len(verts);ids={id(v):start+i for i,v in enumerate(m.vertices)};verts+=m.vertices;tri += [[ids[id(v)] for v in reversed(t.vertices)] for t in m.faces]
  for v in m.vertices:
   row={}
   for b,w in v.boneMapping.items():
    for k,ww in mapped(b.name).items():row[k]=row.get(k,0)+w*ww
   rows.append(row)
 pos=np.array([[v.position.x*100,v.position.z*100,v.position.y*100] for v in verts],dtype='<f4')
 def sn(x):return max(-127,min(127,round(x*127)))
 tan=np.array([[sn(v.tangent.x),sn(v.tangent.z),sn(v.tangent.y),127,sn(v.normal.x),sn(v.normal.z),sn(v.normal.y),sn(-v.tangent.w)] for v in verts],dtype='i1').view('u1')
 uv=np.array([[v.uv[0].u,v.uv[0].v,3.0517578125e-5,3.0517578125e-5] for v in verts],dtype='<f2')
 return pos,tan,uv,rows,np.array(tri,dtype='<u2')

def native_accessories(mesh,pcface):
 # Classify connected geometry; preserve internal mouth surfaces, never ear/skin seams.
 q=mesh.info[0];tri=mesh.indices[:q['tris']];n=q['verts'];rows=np.r_[tri[:,0],tri[:,1],tri[:,2]];cols=np.r_[tri[:,1],tri[:,2],tri[:,0]]
 nc,labels=connected_components(coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(n,n)),directed=False)
 selected=[];weights={};groups=[];eyeids={}
 for c in range(nc):
  ids=np.where(labels==c)[0];pos=mesh.positions[ids];uv=mesh.uv[ids,:2].astype(float)
  if len(ids)>500:continue
  if uv[:,0].min()>.87 and uv[:,1].min()>.87:
   side='l' if pos[:,0].mean()>0 else 'r';groups.append(dict(kind='eye_'+side,count=len(ids)));selected+=list(ids);eyeids.setdefault(side,[]).extend(ids)
   for i in ids:weights[i]={boneids['skf_eye_'+side]:1.}
  elif (uv[:,0].max()<.13 and uv[:,1].min()>.87) or (pos[:,1].min()>10 and pos[:,1].max()<17 and pos[:,2].min()>162 and pos[:,2].max()<168):
   selected+=list(ids)
   if uv[:,0].max()<.13:lower=uv[:,1].min()>.94;kind='lower_teeth' if lower else 'upper_teeth';w={boneids['skf_jaw' if lower else 'sk_head']:1.}
   else:kind='mouth_cavity';w={boneids['sk_head']:.5,boneids['skf_jaw']:.5}
   groups.append(dict(kind=kind,count=len(ids)))
   for i in ids:weights[i]=w
 assert sum(g['count'] for g in groups if g['kind'].startswith('eye'))==88
 assert len(selected)==135,(len(selected),groups)
 selected=sorted(selected);lookup={int(v):i for i,v in enumerate(selected)};tri=np.array([[lookup[int(v)] for v in t] for t in tri if all(int(v) in lookup for v in t)],dtype='<u2')
 pos=mesh.positions[selected].copy();fit={}
 # Translate the native eye surfaces into each supplied PC eye opening without sculpting skin.
 occlusion=next(m for m in pcface.meshes if m.materialInstance.name=='fox_eyeOcclusion_mat')
 oc=np.array([[v.position.x*100,v.position.z*100,v.position.y*100] for v in occlusion.vertices])
 for side,ids in eyeids.items():
  source=oc[oc[:,0]>0] if side=='l' else oc[oc[:,0]<0]
  delta=source.mean(0)-mesh.positions[ids].mean(0);assert np.linalg.norm(delta)<2
  for i in ids:pos[lookup[int(i)]]+=delta
  fit[side]=delta.tolist()
 return pos,mesh.tangents[selected].copy(),mesh.uv[selected].copy(),[weights[i] for i in selected],mesh.colors[selected].copy(),tri,groups,fit

def tex_export(name):
 out=R/'texture-export';path=out/'Game/Assets/character/RealFace'/(name+'.png')
 if not path.exists():
  cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'reader-input'),'-out='+str(out),name]
  result=subprocess.run(cmd,capture_output=True,check=True);(OUT/(name+'-reader.log')).write_bytes(result.stdout+result.stderr)
 im=Image.open(path).convert('RGBA');assert min(im.size)>=128,(name,im.size)
 return im

def existing_mips(name):
 raw=extract(old,'RealFace/'+name+'.uasset');bulk=extract(old,'RealFace/'+name+'.ubulk');fmt=raw.rfind(b'PF_ETC2_RGB\0');end=fmt+len(b'PF_ETC2_RGB\0');first,count=struct.unpack_from('<II',raw,end);assert first==0
 at=end+8;out=[]
 for i in range(count):
  cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);assert cooked==1 and n==size;at+=24
  if flags==66817:payload=bulk[offset:offset+n]
  elif flags==72:payload=raw[at:at+n];at+=n
  else:raise ValueError(flags)
  w,h,z=struct.unpack_from('<III',raw,at);at+=12;assert z==1;out.append((payload,w,h))
 return out

def texture(template,t,source,name,image,rgba=False,preserve_mips=None):
 """Reuse the audited native Texture2D properties; rebuild all mips and bulk descriptors."""
 raw=extract(t,source);f=struct.unpack_from('<16I',raw);em=f[11];delta=f[13]+f[14]-struct.unpack_from('<Q',raw,em)[0]
 # Native ETC2 template serializes platform dimensions, pixel format FString, FirstMip and NumMips.
 w,h=image.size;fmtpos=raw.rfind(b'PF_ETC2_RGBA\0' if rgba else b'PF_ETC2_RGB\0');start=fmtpos-16;assert start>800
 ow,oh,slices=struct.unpack_from('<III',raw,start);assert slices==1 and ow in (128,256) and oh==ow
 oldsize=ow*oh//(1 if rgba else 2);oldmips=raw.find(struct.pack('<IIIq',66817,oldsize,oldsize,0),start)
 if oldmips<0:raise ValueError('unknown ETC2 template '+source)
 pre_end=oldmips-4;pre=bytearray(raw[:pre_end]);struct.pack_into('<II',pre,start,w,h)
 levels=1+int(np.log2(max(w,h)));struct.pack_into('<I',pre,pre_end-4,levels);body=bytearray();bulk=bytearray();mips=[]
 for level in range(levels):
  dimw=max(4,w>>level);dimh=max(4,h>>level);im=image.resize((dimw,dimh),Image.Resampling.LANCZOS)
  payload=(etcpak.compress_etc2_rgba if rgba else etcpak.compress_etc2_rgb)(im.tobytes(),dimw,dimh);assert len(payload)==dimw*dimh//(1 if rgba else 2)
  if preserve_mips and level<len(preserve_mips):
   previous,pw,ph=preserve_mips[level];blocks_w=dimw//4;old_w=max(4,pw)//4;old_h=max(4,ph)//4;assert not rgba and old_w<=blocks_w
   compressed=bytearray(payload)
   for row in range(old_h):compressed[row*blocks_w*8:row*blocks_w*8+old_w*8]=previous[row*old_w*8:(row+1)*old_w*8]
   payload=bytes(compressed)
  mips.append(payload);body+=struct.pack('<I',1);virtual=len(pre)+len(body)-delta
  if max(dimw,dimh)>64:body+=struct.pack('<IIIq',66817,len(payload),len(payload),len(bulk));bulk+=payload
  else:body+=struct.pack('<IIIq',72,len(payload),len(payload),virtual+20)+payload
  body+=struct.pack('<III',dimw,dimh,1)
 new=pre+body+raw[-12:];struct.pack_into('<Q',new,start-8,len(pre)+len(body)+4-delta);struct.pack_into('<Q',new,em+8,struct.unpack_from('<Q',raw,em+8)[0]+len(new)-len(raw))
 oldname=Path(source).stem;new=rename(new,{BASE+oldname:BASE+name,oldname:name},BASE+oldname,BASE+name)
 add(name,new,t,source,bulk=bulk)
 decoded=texture2ddecoder.decode_etc2a8(mips[0],w,h) if rgba else texture2ddecoder.decode_etc2(mips[0],w,h)
 Image.frombytes('RGBA',(w,h),decoded,'raw','BGRA').save(OUT/(name+'-decoded.png'))
 texture_reports.append(dict(name=name,size=[w,h],mips=[len(p) for p in mips],alpha=rgba))

def neck_fix(pos,tan,uv,rows,tri,native):
 # Preserve all positions. Transfer only the low neck to native neck/spine weights.
 from scipy.spatial import cKDTree
 native_ids=np.where((native.positions[:743,2]<162)&(native.positions[:743,1]<13.5))[0]
 native_rows=native.global_weights(0)
 low=(pos[:,2]<161.5)&(pos[:,1]<13.5)
 tree=cKDTree(native.positions[native_ids]);distance,nearest=tree.query(pos[low],k=4)
 for i,dist,ix in zip(np.where(low)[0],distance,nearest):
  f=1/np.maximum(dist,.03)**2;f/=f.sum();row={}
  for j,v in zip(native_ids[ix],f):
   for bone,w in native_rows[j]:row[bone]=row.get(bone,0)+v*w/255
  rows[i]=row
 for row in rows:
  for bone in [boneids['sk_shoulder_l'],boneids['sk_shoulder_r']]:
   if bone in row:row[boneids['sk_spine_03']]=row.get(boneids['sk_spine_03'],0)+row.pop(bone)
 # Weld shading normals across coincident neck vertices, without moving the mesh.
 blend=np.clip((164-pos[:,2])/5,0,1)*np.clip((14.5-pos[:,1])/3,0,1)
 normals=tan[:,4:7].view('i1').astype(float)/127;face=np.cross(pos[tri[:,1]]-pos[tri[:,0]],pos[tri[:,2]]-pos[tri[:,0]])
 if np.sum(face*normals[tri].mean(1))<0:face=-face
 summed=np.zeros_like(normals)
 for j in range(3):np.add.at(summed,tri[:,j],face)
 _,groups=np.unique(np.round(pos,3),axis=0,return_inverse=True);weld=np.zeros((groups.max()+1,3));np.add.at(weld,groups,summed);n=weld[groups];n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-10)
 n=normals*(1-blend[:,None])+n*blend[:,None];n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-10)
 tangent=tan[:,:3].view('i1').astype(float)/127;tangent-=n*np.sum(tangent*n,axis=1,keepdims=True);tangent/=np.maximum(np.linalg.norm(tangent,axis=1,keepdims=True),1e-10)
 tan=tan.copy();change=blend>0;tan[change,4:7]=np.rint(n[change]*127).astype('i1').view('u1');tan[change,:3]=np.rint(tangent[change]*127).astype('i1').view('u1')
 # Rasterize the same anatomical neck region in source PC UV space.
 mask=np.zeros((1024,1024),dtype=float);pixel=uv[:,:2].astype(float)*1023
 for face in tri:
  if not np.any(blend[face]>.001):continue
  v=pixel[face];lo=np.maximum(v.min(0).astype(int),0);hi=np.minimum(np.ceil(v.max(0)).astype(int),1023)
  if (lo>hi).any():continue
  x,y=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));den=(v[1,1]-v[2,1])*(v[0,0]-v[2,0])+(v[2,0]-v[1,0])*(v[0,1]-v[2,1])
  if abs(den)<1e-9:continue
  a=((v[1,1]-v[2,1])*(x-v[2,0])+(v[2,0]-v[1,0])*(y-v[2,1]))/den;b=((v[2,1]-v[0,1])*(x-v[2,0])+(v[0,0]-v[2,0])*(y-v[2,1]))/den;c=1-a-b;inside=(a>=0)&(b>=0)&(c>=0);value=(a*blend[face[0]]+b*blend[face[1]]+c*blend[face[2]])*inside;sl=mask[lo[1]:hi[1]+1,lo[0]:hi[0]+1];np.maximum(sl,value,out=sl)
 return tan,rows,Image.fromarray(np.uint8(mask*255)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2)),int(low.sum())

def pc_normal(profile,neck_mask):
 im=Image.open(R/'ronaldo-noodle-source/converted/face_nrm.png') if profile=='ND01' else Image.open(next((R/'input-1').rglob('face_nrm.dds')))
 a=np.array(im.convert('RGBA'),dtype=float)/255
 if profile=='ND01':x=a[:,:,3]*2-1;y=a[:,:,1]*2-1;z=np.sqrt(np.maximum(0,1-x*x-y*y));rgb=(np.stack([x,y,z],axis=-1)+1)/2*255
 else:rgb=a[:,:,:3]*255
 weight=np.array(neck_mask,dtype=float)[:,:,None]/255;rgb=rgb*(1-weight)+np.array([128,128,255])*weight
 return Image.fromarray(np.uint8(np.clip(rgb,0,255))).convert('RGBA')

for suffix in SUFFIX:
 variant='4522'+suffix;srcname='SK_ND01'+suffix+'_Face';oldraw=extract(old,'RealFace/'+srcname+'.uasset');m=Mesh(oldraw,(R/('v4a-'+suffix+'.log')).read_text());native=Mesh(extract(heads,'RealFace/SK_'+variant+'_Face.uasset'),(R/('native-'+suffix+'.log')).read_text())
 for profile,pcface in [('ND01',oldpc),('ND06',newface)]:
  accpos,acctan,accuv,accrows,acccol,acctri,groups,fit=native_accessories(native,pcface)
  if profile=='ND01':
   ns=m.info[0]['verts'];nh=m.info[1]['verts'];skinpos=m.positions[:ns].copy();skintan=m.tangents[:ns].copy();skinuv=m.uv[:ns].copy();skinrows=[dict(row) for row in m.global_weights(0)];skintri=m.indices[:m.info[0]['tris']].copy();hairpos=m.positions[ns:].copy();hairtan=m.tangents[ns:].copy();hairuv=m.uv[ns:].copy();hairtri=m.indices[m.info[0]['tris']:].copy()-ns
  else:
   skinpos,skintan,skinuv,skinrows,skintri=pc_arrays([newface.meshes[0],newface.meshes[2],newhair.meshes[0]])
   hairpos,hairtan,hairuv,_,hairtri=pc_arrays([newhair.meshes[1]]);ns=len(skinpos);nh=len(hairpos)
  skintan,skinrows,neck_mask,neck_count=neck_fix(skinpos,skintan,skinuv,skinrows,skintri,native)
  # Texture atlas retains 1024x1024 PC diffuse at full resolution in top-left,
  # native diffuse (eyes/teeth/cavity) in bottom-left; normal/SRO use the same layout.
  skinuv[:,:2]*=.5;accuv[:,:2]*=.5;accuv[:,1]+=.5
  bm=sorted({k for row in skinrows+accrows for k in row});sw=quantize(skinrows+accrows,bm);hw=np.tile(np.array([0,0,0,0,255,0,0,0],dtype='u1'),(nh,1))
  pos=np.concatenate([skinpos,accpos,hairpos]);tan=np.concatenate([skintan,acctan,hairtan]);uv=np.concatenate([skinuv,accuv,hairuv]);weights=np.concatenate([sw,hw]);colors=np.concatenate([np.full((ns,4),255,dtype='u1'),acccol,np.full((nh,4),255,dtype='u1')]);tri=np.concatenate([skintri,acctri+ns,hairtri+ns+len(accpos)]);nst=len(skintri)+len(acctri)
  parents={}
  for parent,node in enumerate(gltf['nodes']):
   for child in node.get('children',[]):parents[child]=parent
  jointnodes=gltf['skins'][0]['joints'];nodebone={n:i for i,n in enumerate(jointnodes)};active=set(bm)|{7}
  for bone in list(active):
   node=jointnodes[bone]
   while node in parents:
    node=parents[node]
    if node in nodebone:active.add(nodebone[node])
  active=sorted(active);assert len(active)<25 and not any('hand' in bones[i] or 'foot' in bones[i] for i in active)
  new=m.write(pos,tan,uv,weights,colors,tri,ns+len(accpos),nst,bm,active);newname='SK_'+profile+suffix+'_Face'
  oldpath=BASE+srcname;newpath=BASE+newname;imports={}
  for quality in ['HQ','MQ']:
   imports[BASE+'MI_ND0001_Head_Hair_'+quality]=BASE+'MI_'+('ND0001' if profile=='ND01' else 'ND0006')+'_Head_Hair_'+quality
   facekind='FaceUpcon' if suffix=='lg00v0000' else 'FaceLegacy';imports[BASE+'MI_'+variant+'_Head_'+facekind+'_'+quality]=BASE+'MI_'+profile+suffix+'_Head_'+facekind+'_'+quality
  repl={oldpath:newpath,srcname:newname}
  for a,b in imports.items():repl[a]=b;repl[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
  new=rename(new,repl,oldpath,newpath,imports=imports);add(newname,new,old,'RealFace/'+srcname+'.uasset',{pid(a):pid(b) for a,b in imports.items()})
  for channel in ['D','N','SRO']:
   nativeim=tex_export('T_'+variant+'_Face_'+channel).resize((1024,1024),Image.Resampling.LANCZOS);atlas=Image.new('RGBA',(2048,2048));atlas.paste(nativeim,(0,1024));atlas.paste(nativeim,(1024,1024))
   if channel=='D':
    pcim=Image.open(R/'ronaldo-noodle-source/converted/face_bsm_alp.png') if profile=='ND01' else Image.open(next((R/'input-1').rglob('face_bsm_alp.dds')))
    pcim=pcim.convert('RGBA');assert pcim.size==(1024,1024);atlas.paste(pcim,(0,0));atlas.paste(pcim,(1024,0))
   elif channel=='N':
    normal=pc_normal(profile,neck_mask);atlas.paste(normal,(0,0));atlas.paste(normal,(1024,0))
   else:atlas.paste(nativeim,(0,0));atlas.paste(nativeim,(1024,0))
   name='T_'+profile+suffix+'_Face_'+channel
   texture('face',ref,'character/RealFace/T_133157_Face_'+channel+'.uasset',name,atlas,preserve_mips=existing_mips('T_ND01'+suffix+'_Face_D') if profile=='ND01' and channel=='D' else None)
  for quality in ['HQ','MQ']:
   oldname='MI_'+variant+'_Head_'+facekind+'_'+quality;newname='MI_'+profile+suffix+'_Head_'+facekind+'_'+quality;imp={BASE+'T_'+variant+'_Face_'+c:BASE+'T_'+profile+suffix+'_Face_'+c for c in ['D','N','SRO']};repl={BASE+oldname:BASE+newname,oldname:newname}
   for a,b in imp.items():repl[a]=b;repl[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
   raw=extract(mats,'RealFace/'+oldname+'.uasset');raw=rename(raw,repl,BASE+oldname,BASE+newname,imports=imp);add(newname,raw,mats,'RealFace/'+oldname+'.uasset',{pid(a):pid(b) for a,b in imp.items()})
  reports.append(dict(profile=profile,variant=variant,skin_vertices=ns,accessory_vertices=len(accpos),hair_vertices=nh,triangles=len(tri),bone_map={str(k):bones[k] for k in bm},native_accessory_groups=groups,eye_fit_translation_cm=fit,skin_and_hair_positions_preserved=profile=='ND01',active_bones=active,low_neck_native_weight_vertices=neck_count,phone_verified=False))
# Preserve v4a noodle hair materials and compressed texture byte for byte.
for name in ['MI_ND0001_Head_Hair_HQ','MI_ND0001_Head_Hair_MQ','T_ND0001_Hair_D']:
 bulk=old.files.get('RealFace/'+name+'.ubulk');add(name,extract(old,'RealFace/'+name+'.uasset'),old,'RealFace/'+name+'.uasset',bulk=old.read(bulk) if bulk is not None else None)
# 2006 hair uses its actual supplied alpha texture, not the noodle atlas.
im=Image.open(next((R/'input-1').rglob('hair_parts_bsm_alp.dds'))).convert('RGBA');alpha=im.getchannel('A');im=im.filter(ImageFilter.UnsharpMask(radius=1,percent=110,threshold=3));im.putalpha(alpha);texture('hair',ref,'character/RealFace/T_133157_Hair_High_D.uasset','T_ND0006_Hair_D',im,True)
# Native high-quality masked shader for BOTH quality slots of the 2006 head.
for quality in ['HQ','MQ']:
 oldname='MI_133157_Head_Hair_HQ';newname='MI_ND0006_Head_Hair_'+quality
 imp={BASE+'T_133157_Hair_High_D':BASE+'T_ND0006_Hair_D'};repl={BASE+oldname:BASE+newname,oldname:newname}
 for a,b in imp.items():repl[a]=b;repl[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
 raw=rename(extract(ref,'character/RealFace/'+oldname+'.uasset'),repl,BASE+oldname,BASE+newname,imports=imp);add(newname,raw,ref,'character/RealFace/'+oldname+'.uasset',{pid(a):pid(b) for a,b in imp.items()})
 # Existing HQ SRO remains the native supported common/reference shader input.
# Keep true 2048x512 source texels and choose the standard character texture group.
p=ASSET/'T_ND0006_Hair_D.uasset';p.write_bytes(rename(p.read_bytes(),{'TEXTUREGROUP_Project06':'TEXTUREGROUP_Character'}))
# Rebuild a single replacement container so old pc9298 is superseded through the same manifest mechanism.
def entry(t,path):
 h=parse_header(t.read(next(i for i,c in enumerate(t.ids) if c[11]==10)));i=t.files[path];oldpid=struct.unpack('<Q',t.ids[i][:8])[0];return store_entry(h['store'],h['pids'].index(oldpid))
chunks=[];entries=[];pids=[];paths={};package_info=[]
for name,t,source,remap in recipes:
 newpid=pid(BASE+name);data=(ASSET/(name+'.uasset')).read_bytes();paths['RealFace/'+name+'.uasset']=len(chunks);chunks.append((struct.pack('<Q',newpid)+b'\0\0\0\2',data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
 bulk=ASSET/(name+'.ubulk')
 if bulk.exists():
  b=bulk.read_bytes();paths['RealFace/'+name+'.ubulk']=len(chunks);chunks.append((struct.pack('<Q',newpid)+b'\0\0\0\3',b,hashlib.sha1(b).digest()+b'\0'*12+b'\1'))
 fixed,imports=entry(t,source);imports=[remap.get(x,x) for x in imports];entries.append((fixed,imports));pids.append(newpid);package_info.append(dict(name=name,package_id=newpid,imports=imports))
assert len(set(pids))==len(pids)
name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];block=65536;st=build_store(entries);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
out=OUT/'container';out.mkdir(exist_ok=True);ids=[];ols=[];blocks=[];voff=0
import zlib
with (out/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for at in range(0,len(body),block):
   raw=body[at:at+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
di=dir_index(old.mount,paths);h=bytearray(old.raw[:old.hs]);struct.pack_into('<9I',h,20,old.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
blob=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(out/(name+'.utoc')).write_bytes(blob);(out/(name+'.pak')).write_bytes((R/'v4a/livedata'/ (name+'.pak')).read_bytes())
t=Toc(str(out/(name+'.utoc')))
for path,i in paths.items():assert t.read(i)==(ASSET/Path(path).name).read_bytes()
(OUT/'build-report.json').write_text(json.dumps(dict(status='BUILT_NOT_PHONE_VERIFIED',meshes=reports,textures=texture_reports,packages=package_info,container_roundtrip=True),indent=2));print('Built',len(recipes),'packages; independently export/read and validate before packaging.')
