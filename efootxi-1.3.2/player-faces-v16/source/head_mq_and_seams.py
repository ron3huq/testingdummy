"""Scoped native lit face shader substitution; skin seam normals after UV split.
No new material shader bytecode, no skeleton/LOD/BoneMap edits.
"""
from pathlib import Path
import struct,hashlib,cityhash
from collections import defaultdict
import numpy as np
from iostore import parse_header,store_entry
from zen_clone import rename
from mesh_tools import Mesh
BASE='/Game/Assets/character/RealFace/'
def name_list(b):
 f=struct.unpack_from('<16I',b);at=f[6];out=[]
 while at<f[6]+f[7]:
  n=int.from_bytes(b[at:at+2],'big');at+=2;w=n>>15;n&=32767;out.append(b[at:at+n*(2 if w else 1)].decode('utf-16-le' if w else 'utf8'));at+=n*(2 if w else 1)
 return out
def add_name(data,name):
 b=bytearray(data);f=list(struct.unpack_from('<16I',b));names=name_list(b)
 if name in names:return bytes(b),names.index(name)
 ns,nsize,hs,hsize=f[6:10];batch=bytes(b[ns:ns+nsize])+len(name).to_bytes(2,'big')+name.encode();newhs=(ns+len(batch)+7)&~7;hashes=bytes(b[hs:hs+hsize])+struct.pack('<Q',cityhash.CityHash64(name.lower().encode('utf-16-le')))
 result=bytearray(b[:ns])+batch+b'\0'*(newhs-ns-len(batch))+hashes+b[hs+hsize:];shift=newhs+len(hashes)-hs-hsize
 f[7]=len(batch);f[8]=newhs;f[9]=len(hashes)
 for j in [10,11,12,13]:f[j]+=shift
 struct.pack_into('<16I',result,0,*f);assert name_list(result)[-1]==name
 return bytes(result),len(names)
def head_changes(old,out):
 h=parse_header(old.read(next(i for i,c in enumerate(old.ids) if c[11]==10)));replacements={};entries={};report={'mq_shader_substitutions':[],'dinh_bac':{},'phone_tested':False,'root_cause_proven':False}
 def add(path,data,entry):
  ix=old.files[path];idb=old.ids[ix];replacements[path]=(idb,data);entries[struct.unpack_from('<Q',idb)[0]]=entry
 for path,ix in old.files.items():
  if not (path.endswith('_Head_FaceLegacy_HQ.uasset') or path.endswith('_Head_FaceUpcon_HQ.uasset')) or not Path(path).name.startswith(('MI_NF01','MI_NF27','MI_NFJR','MI_NDHD')):continue
  mq=path.replace('_HQ.uasset','_MQ.uasset');j=old.files[mq];source=old.read(j);oldname=Path(mq).stem;newname=Path(path).stem
  data=rename(source,{BASE+oldname:BASE+newname,oldname:newname},BASE+oldname,BASE+newname)
  names=name_list(data);assert BASE+newname in names and 'M_Head_Face_MQ' in names and 'NormalMap' not in names and 'SROMap' not in names
  entry=store_entry(h['store'],h['pids'].index(struct.unpack_from('<Q',old.ids[j])[0]));add(path,data,entry)
  report['mq_shader_substitutions'].append({'path':path,'parent':'/Game/Assets/MaterialLibrary/Character/Head/MasterMaterials/M_Head_Face_MQ','diffuse_parameter':'BaseColorMap','original_HQ_package_id_preserved':True,'mesh_unchanged':True,'sha256':hashlib.sha256(data).hexdigest()})
 assert len(report['mq_shader_substitutions'])==10
 path='character/RealFace/SK_NDDBep00v0313_Face.uasset';ix=old.files[path];data=old.read(ix);updated=bytearray(data);log=(out/'references/NDDBep00v0313.log').read_text();lodreports=[]
 for lod in [0,1]:
  m=Mesh(data,log,lod);n=m.info[0]['verts']-135;groups=defaultdict(list)
  for i,p in enumerate(m.positions[:n]):
   # exclude mouth/eyelids/eyeballs and internal accessories; preserve expression creases
   if abs(p[0])<5.2 and p[1]>13.5 and p[2]>161:continue
   groups[tuple(np.round(p,3))].append(i)
  tan=m.tangents.view('i1').copy();changed=[]
  for group in groups.values():
   if len(group)<2:continue
   normals=tan[group,4:7].astype(float);normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-9)
   # Only smooth exterior seam faces with compatible normal hemispheres.
   if np.min(normals@normals.T)<.15:continue
   normal=normals.sum(0);normal/=np.linalg.norm(normal)
   before=float(np.max(np.arccos(np.clip(normals@normal,-1,1)))*180/np.pi)
   if before<.1:continue
   for i in group:
    tangent=tan[i,:3].astype(float);tangent-=normal*np.dot(tangent,normal)
    if np.linalg.norm(tangent)<1e-6:continue
    tangent/=np.linalg.norm(tangent);tan[i,:3]=np.clip(np.rint(tangent*127),-127,127).astype('i1');tan[i,4:7]=np.clip(np.rint(normal*127),-127,127).astype('i1')
   changed.append({'vertices':group,'prior_normal_deviation_deg':before})
  at=m.r['TANGENT_UV_BEGIN']+26;updated[at:at+len(tan)*8]=tan.view('u1').tobytes()
  # Diffuse/normal/SRO PC quadrant has no atlas wrap gutter. Prevent UV boundary
  # samples from blending neighboring black atlas blocks. Internal UVs untouched.
  uv=m.uv.copy();uv[:n,:2]=np.clip(uv[:n,:2],2/2048,(1024-2)/2048).astype('<f2')
  uv_at=at+len(tan)*8+8;updated[uv_at:uv_at+uv.nbytes]=uv.tobytes()
  lodreports.append({'lod':lod,'smoothed_skin_seam_groups':len(changed),'groups':changed,'atlas_edge_uv_vertices_clamped':int(np.any(uv[:n]!=m.uv[:n],axis=1).sum()),'UV_edge_guard_atlas_pixels':2})
 assert all(x['atlas_edge_uv_vertices_clamped']>0 for x in lodreports)
 # positions, indices, weights and all bone metadata must remain byte-identical.
 for lod in [0,1]:
  before=Mesh(data,log,lod);after=Mesh(bytes(updated),log,lod)
  for attr in ['positions','indices','weights','colors']:assert np.array_equal(getattr(before,attr),getattr(after,attr)),attr
  assert before.info[0]['bones']==after.info[0]['bones'];assert before.tangents.shape==after.tangents.shape
 entry=store_entry(h['store'],h['pids'].index(struct.unpack_from('<Q',old.ids[ix])[0]));add(path,bytes(updated),entry)
 report['dinh_bac']['normal_seams']=lodreports
 clips=[]
 for q in ['HQ','MQ']:
  path='character/RealFace/MI_ND00DB_Head_Hair_'+q+'.uasset';ix=old.files[path];original=old.read(ix);b=bytearray(original);names=name_list(b);f=struct.unpack_from('<16I',b)
  at=b.find(struct.pack('<II',names.index('OpacityMaskClipValue'),0),f[13]+f[14]);assert at>0 and names[struct.unpack_from('<I',b,at+8)[0]]=='FloatProperty' and struct.unpack_from('<II',b,at+16)==(4,0) and b[at+24]==0
  oldclip=struct.unpack_from('<f',b,at+25)[0];assert .3<oldclip<.4;struct.pack_into('<f',b,at+25,.20)
  # Explicit override flag is necessary: float alone otherwise inherits parent clip.
  raw,flagidx=add_name(bytes(b),'bOverride_OpacityMaskClipValue');b=bytearray(raw);names=name_list(b);f=struct.unpack_from('<16I',b)
  start=b.find(struct.pack('<II',names.index('BasePropertyOverrides'),0),f[13]+f[14]);size=struct.unpack_from('<I',b,start+16)[0];payload=start+49;end=payload+size
  assert b[end-8:end]==struct.pack('<II',names.index('None'),0)
  tag=struct.pack('<IIIIII',flagidx,0,names.index('BoolProperty'),0,0,0)+b'\1\0';assert len(tag)==26
  b[end-8:end-8]=tag;struct.pack_into('<I',b,start+16,size+len(tag));em=f[11];struct.pack_into('<Q',b,em+8,struct.unpack_from('<Q',b,em+8)[0]+len(tag))
  assert 'bOverride_OpacityMaskClipValue' in name_list(b)
  entry=store_entry(h['store'],h['pids'].index(struct.unpack_from('<Q',old.ids[ix])[0]));add(path,bytes(b),entry);clips.append({'path':path,'before':oldclip,'after':.20,'hair_texture_RGBA_preserved':True,'explicit_override_flag':True})
 report['dinh_bac']['hair_mask_clip']=clips
 return replacements,entries,report
