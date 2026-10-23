"""Replace only Sparta351 outfield p1/p2 native ETC2 atlases. Original mip
metadata, package identity, font assets, GK and all other team assets retained.
FTEX top level recovered separately; malformed source small mips are discarded.
"""
from pathlib import Path
import struct,hashlib,zlib,json,shutil
from PIL import Image
import etcpak,texture2ddecoder
from iostore import Toc,parse_header,store_entry,build_store,dir_index
from zen_clone import pid
out=Path(__file__).resolve().parent.parent
base=Toc(str(out.parent/'player-faces-v18/container/pc9298_mobile_and.utoc'))
templates=out/'references/sparta-native';native_meta=json.loads((templates/'templates.json').read_text())
h=parse_header(base.read(next(i for i,x in enumerate(base.ids) if x[11]==10)))

chunks=[];paths={};pids=[];stores=[];rows=[]
for path,ix in sorted(base.files.items(),key=lambda x:x[1]):
 body=base.read(ix);paths[path]=len(chunks);chunks.append((base.ids[ix],body,hashlib.sha1(body).digest()+b'\0'*12+b'\1'))
 if path.endswith('.uasset'):
  pk=struct.unpack_from('<Q',base.ids[ix])[0];pids.append(pk);stores.append(store_entry(h['store'],h['pids'].index(pk)))
for slot,source in [('p1','u0109p1_home'),('p2','u0109p1_third')]:
 path='Uniform/LowTextures/T_u0351'+slot+'_Uni_D.uasset';meta=native_meta[path];original=(templates/meta['file']).read_bytes();assert hashlib.sha256(original).hexdigest()==meta['sha256'];raw=bytearray(original);fmt=b'PF_ETC2_RGB\0';pos=raw.rfind(fmt);assert pos>0
 at=pos+len(fmt);first,count=struct.unpack_from('<II',raw,at);assert first==0;at+=8
 im=Image.open(out/'kit-inputs'/(source+'.png')).convert('RGBA');source_sha=hashlib.sha256((out/'kit-inputs'/(source+'.png')).read_bytes()).hexdigest();bulk=bytearray();dims=[];decoded=None
 originalbulkpath=path.replace('.uasset','.ubulk');oldbulk=b'' # Both audited native templates keep their sole1024 level inline.
 if oldbulk:bulk=bytearray(oldbulk)
 for level in range(count):
  assert struct.unpack_from('<I',raw,at)[0]==1;at+=4
  flags,num,size,offset=struct.unpack_from('<IIIq',raw,at);assert num==size
  sizepos=at;at+=20
  if flags&0x100: # external bulk
   dw,dh,d=struct.unpack_from('<III',raw,at);at+=12
  else:
   dw,dh,d=struct.unpack_from('<III',raw,at+num);at+=num+12
  assert d==1 and dw>=4 and dh>=4 and num==dw*dh//2
  levelim=im.resize((dw,dh),Image.Resampling.LANCZOS);payload=etcpak.compress_etc2_rgb(levelim.tobytes(),dw,dh);assert len(payload)==num
  if flags&0x100:
   assert offset>=0 and offset+num<=len(bulk);bulk[offset:offset+num]=payload
  else:raw[sizepos+20:sizepos+20+num]=payload
  dims.append([dw,dh])
  if level==0:
   decoded=Image.frombytes('RGBA',(dw,dh),texture2ddecoder.decode_etc2(payload,dw,dh),'raw','BGRA');decoded.save(out/'kit-previews'/('Sparta351-'+slot+'-ETC2.png'))
 assert len(raw)==len(original)
 fullpath='character/'+path;idb=bytes.fromhex(meta['chunk_id']);pk=struct.unpack_from('<Q',idb)[0];assert pk==pid('/Game/Assets/character/Uniform/LowTextures/T_u0351'+slot+'_Uni_D')
 paths[fullpath]=len(chunks);chunks.append((idb,bytes(raw),hashlib.sha1(raw).digest()+b'\0'*12+b'\1'));pids.append(pk);stores.append((bytes.fromhex(meta['fixed_store']),meta['imports']))
 rows.append({'team_id':351,'native_name':'Sparta Rotterdam','slot':slot,'source_file':source+'.ftex','native_texture':fullpath,'mips':dims,'original_texture_serialized_size_preserved':True,'source_png_sha256':source_sha,'GPU_renderer_verified':False,'UV_mapping':'source full-kit atlas resampled as a whole; no invented shirt/pants geometry','source_small_mips_discarded_native_mips_reencoded':True})
name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];st=build_store(stores);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
dest=out/'container';dest.mkdir(exist_ok=True);ids=[];ols=[];blocks=[];voff=0;block=65536
with (dest/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for a in range(0,len(body),block):
   raw=body[a:a+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
mount='../../../PesMobile/Content/Assets/';di=dir_index(mount,paths);header=bytearray(base.raw[:base.hs]);struct.pack_into('<9I',header,20,base.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',header,56,cid);header[64:80]=b'\0'*16;header[80]=9
blob=bytes(header)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(dest/(name+'.utoc')).write_bytes(blob);shutil.copyfile(out.parent/'player-faces-v18/container'/(name+'.pak'),dest/(name+'.pak'))
t=Toc(str(dest/(name+'.utoc')))
for path,i in base.files.items():assert t.read(t.files[path])==base.read(i)
for path,i in paths.items():assert t.read(t.files[path])==chunks[i][1]
report={'status':'SPARTA351_ONLY_TWO_NATIVE_ETC2_UNIFORM_TEXTURES_PASS','kits':rows,'existing_v18_chunks_unchanged':len(base.files),'new_chunks':len(paths)-len(base.files),'phone_verified':False};(out/'kit-build.json').write_text(json.dumps(report,indent=2));print(report['status'],report['existing_v18_chunks_unchanged'],report['new_chunks'])
