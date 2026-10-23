"""Rebase four private asset stacks onto the phone-proven ND06 serialization.
Original four geometries, weights, UVs and texture payloads are retained. Approved
nine heads and all UI/card-art chunks are copied byte-identically. Device untested.
"""
from pathlib import Path
import struct,hashlib,json,zlib,shutil
import numpy as np
from iostore import Toc,parse_header,store_entry,build_store,dir_index
from zen_clone import rename,pid
from mesh_tools import Mesh,write_native_lods,platform_lod_properties
from head_mq_and_seams import name_list
out=Path(__file__).resolve().parent.parent;old=Toc(str(out.parent/'player-faces-v16/container/pc9298_mobile_and.utoc'));work=Path('/workspace/ronaldo-work');BASE='/Game/Assets/character/RealFace/'
h=parse_header(old.read(next(i for i,x in enumerate(old.ids) if x[11]==10)));changes={};entries={};rows=[]
def read(name,ext='uasset'):return old.read(old.files['character/RealFace/'+name+'.'+ext])
def entry_for(name):
 ix=old.files['character/RealFace/'+name+'.uasset'];return store_entry(h['store'],h['pids'].index(struct.unpack_from('<Q',old.ids[ix])[0]))
def put(name,body,source,imports=None,ext='uasset'):
 path='character/RealFace/'+name+'.'+ext;own=BASE+name;changes[path]=(struct.pack('<Q',pid(own))+b'\0\0\0'+(b'\x02' if ext=='uasset' else b'\x03'),body)
 if ext=='uasset':
  fixed,im=entry_for(source);entries[pid(own)]=(fixed,[(imports or {}).get(p,p) for p in im])
for oldprofile,newprofile,suffixes in [('NF01','NV01',['','lg00v0000','ep01v0291','ep00v0313']),('NF27','NV27',['','lg00v0000','ep01v0291','ep00v0313']),('NFJR','NVJR',['ep00v0313']),('NDHD','NVHD',['ep00v0313'])]:
 for suffix in suffixes:
  source='SK_'+oldprofile+suffix+'_Face';template='SK_ND06'+suffix+'_Face';dest='SK_'+newprofile+suffix+'_Face';raw=read(source);base=read(template)
  before=Mesh(raw,(out/'references/original'/('v10-'+oldprofile+suffix+'.log')).read_text(),0);tmpl=Mesh(base,(out/'references/original'/('v10-ND06'+suffix+'.log')).read_text(),1)
  ns=before.info[0]['verts'];nt=before.info[0]['tris'];skinrows=[dict(r) for r in before.global_weights(0)];active=list(struct.unpack_from('<%dH'%struct.unpack_from('<I',raw,before.r['ACTIVE_BEGIN'])[0],raw,before.r['ACTIVE_BEGIN']+4))
  # Preserve the already-tested complete LOD records literally, including each
  # section palette/weight ordering. Re-quantizing equivalent weights can reorder
  # byte influences; that is unnecessary and would weaken cutscene preservation.
  rebuilt=bytearray(base[:tmpl.lods[0]]+raw[before.lods[0]:])
  lo=before.positions.min(0);hi=before.positions.max(0);center=(hi+lo)/2;extent=(hi-lo)/2
  struct.pack_into('<7f',rebuilt,tmpl.r['BOUNDS_BEGIN'],*center,*extent,float(np.linalg.norm(extent)))
  em=struct.unpack_from('<I',base,44)[0];struct.pack_into('<Q',rebuilt,em+80,struct.unpack_from('<Q',base,em+80)[0]+len(rebuilt)-len(base))
  # Hair asset names remain the existing private hair MICs; no new hair texture.
  oldnames=[n for n in name_list(raw) if n.startswith(BASE+'MI_')];templnames=[n for n in name_list(base) if n.startswith(BASE+'MI_')];assert len(oldnames)==len(templnames)==4
  imports={}
  for oldmat,tempmat in zip(oldnames,templnames):
   isface='_Head_Face' in oldmat;newmat=oldmat.replace(oldprofile,newprofile) if isface else oldmat;imports[tempmat]=newmat
  replacements={BASE+template:BASE+dest,template:dest}
  for a,b in imports.items():replacements[a]=b;replacements[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
  rebuilt=rename(rebuilt,replacements,BASE+template,BASE+dest,imports=imports);rebuilt,_=platform_lod_properties(rebuilt,True)
  put(dest,rebuilt,template,{pid(a):pid(b) for a,b in imports.items()})
  # All texture descriptors start with the working template's serialized header.
  # Preserve the original four face texture platform/mip payload and bulk bytes.
  for channel in ['D','N','SRO']:
   original='T_'+oldprofile+suffix+'_Face_'+channel;template_tex='T_ND06'+suffix+'_Face_'+channel;newtex='T_'+newprofile+suffix+'_Face_'+channel;src=read(original);b=read(template_tex)
   a=src.rfind(b'PF_ETC2_RGB\0')-16;z=b.rfind(b'PF_ETC2_RGB\0')-16;assert a>0 and z>0
   assert struct.unpack_from('<III',src,a)==struct.unpack_from('<III',b,z)==(2048,2048,1)
   # Header sizes and export serial accounting stay identical for 4-character profiles.
   assert len(src)==len(b) and a==z,(original,len(src),len(b),a,z)
   body=bytearray(b[:z]+src[a:]);body=rename(body,{BASE+template_tex:BASE+newtex,template_tex:newtex},BASE+template_tex,BASE+newtex)
   bulk=read(original,'ubulk');put(newtex,body,template_tex);put(newtex,bulk,template_tex,ext='ubulk')
  for quality in ['HQ','MQ']:
   kind='FaceUpcon' if suffix=='lg00v0000' else 'FaceLegacy';template_mat='MI_ND06'+suffix+'_Head_'+kind+'_'+quality;newmat='MI_'+newprofile+suffix+'_Head_'+kind+'_'+quality
   remap={BASE+'T_ND06'+suffix+'_Face_'+c:BASE+'T_'+newprofile+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+template_mat:BASE+newmat,template_mat:newmat}
   for a,b in remap.items():rep[a]=b;rep[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1]
   body=rename(read(template_mat),rep,BASE+template_mat,BASE+newmat,imports=remap);put(newmat,body,template_mat,{pid(a):pid(b) for a,b in remap.items()})
  rows.append({'old_profile':oldprofile+suffix,'new_profile':newprofile+suffix,'mesh':dest,'template':template,'original_mesh_sha256':hashlib.sha256(raw).hexdigest(),'new_mesh_sha256':hashlib.sha256(rebuilt).hexdigest(),'source_geometry_positions_indices_UVs_weights_preserved':True,'reference_skeleton_source':'phone-proven ND06, native166','phone_verified':False})
# Remove superseded bad mesh/face material/face texture chunks, retain their hair.
remove=lambda path:any(Path(path).name.startswith(prefix+profile) for profile in ['NF01','NF27','NFJR','NDHD'] for prefix in ['SK_','T_','MI_'])
chunks=[];paths={};pids=[];stores=[]
for path,i in sorted(old.files.items(),key=lambda x:x[1]):
 if remove(path):continue
 body=old.read(i);paths[path]=len(chunks);chunks.append((old.ids[i],body,hashlib.sha1(body).digest()+b'\0'*12+b'\1'));package=struct.unpack_from('<Q',old.ids[i])[0]
 if path.endswith('.uasset'):
  pids.append(package);stores.append(store_entry(h['store'],h['pids'].index(package)))
for path,(idb,body) in changes.items():
 paths[path]=len(chunks);chunks.append((idb,body,hashlib.sha1(body).digest()+b'\0'*12+b'\1'))
 if path.endswith('.uasset'):
  package=struct.unpack_from('<Q',idb)[0];pids.append(package);stores.append(entries[package])
name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];st=build_store(stores);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
dest=out/'container';dest.mkdir(exist_ok=True);ids=[];ols=[];blocks=[];voff=0;block=65536
with (dest/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for a in range(0,len(body),block):
   raw=body[a:a+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
mount='../../../PesMobile/Content/Assets/';di=dir_index(mount,paths);header=bytearray(old.raw[:old.hs]);struct.pack_into('<9I',header,20,old.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',header,56,cid);header[64:80]=b'\0'*16;header[80]=9
blob=bytes(header)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(dest/(name+'.utoc')).write_bytes(blob);shutil.copyfile(out.parent/'player-faces-v16/container'/(name+'.pak'),dest/(name+'.pak'))
t=Toc(str(dest/(name+'.utoc')))
for path,ix in paths.items():assert t.read(t.files[path])==chunks[ix][1]
unchanged=sum(not remove(p) for p in old.files);assert len(rows)==10
report={'status':'FOUR_HEAD_ASSET_STACKS_REBASED_FROM_PHONE_PROVEN_ND06_SERIALIZATION_PASS','changed_meshes':rows,'unchanged_chunks':unchanged,'original_four_face_and_hair_geometry_and_texture_payloads_preserved':True,'phone_tested':False,'black_face_fixed_on_device':False,'container_sha256':hashlib.sha256((dest/(name+'.ucas')).read_bytes()).hexdigest()};(out/'asset-rebase-build.json').write_text(json.dumps(report,indent=2));print(report['status'],unchanged,'unchanged chunks',len(changes),'replacement chunks')
