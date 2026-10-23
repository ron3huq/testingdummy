"""Add two exact-ID UI portraits; copy every existing head chunk verbatim.
Image resized solely for native texture encoding; artwork authored by imagegen.
"""
from pathlib import Path
import struct,hashlib,json,zlib,shutil,sys
import etcpak
from PIL import Image
from iostore import Toc,parse_header,store_entry,build_store,dir_index
out=Path(__file__).resolve().parent.parent;work=Path('/workspace/ronaldo-work');old=Toc(str(out.parent/'player-faces-v12/container/pc9298_mobile_and.utoc'));native=Toc(str(next((work/'resources').rglob('pc1000_mobile_and.utoc'))));chunks=[];paths={}
hd=parse_header(old.read(next(i for i,c in enumerate(old.ids) if c[11]==10)));pids=list(hd['pids']);entries=[store_entry(hd['store'],i) for i in range(len(pids))]
for path,i in sorted(old.files.items(),key=lambda x:x[1]):
 if path.startswith('ui/'):continue
 data=old.read(i);paths[path]=len(chunks);chunks.append((old.ids[i],data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
art=out/'card-art-research/xuan-son/Nguyen-Xuan-Son-Epic.png';image=Image.open(art).convert('RGBA');rows=[]
nh=parse_header(native.read(next(i for i,c in enumerate(native.ids) if c[11]==10)))
for name in ['88045755960841_','88045755960841_l']:
 path='ui/Data/Thumbnail/Player/Variation2022/'+name+'.uasset';i=native.files[path];raw=bytearray(native.read(i));original=bytes(raw);at=raw.rfind(b'PF_ETC2_RGBA\0');assert at>0
 at+=len(b'PF_ETC2_RGBA\0');first,count=struct.unpack_from('<II',raw,at);at+=8;assert first==0 and count in (1,8);dims=[]
 for level in range(count):
  cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and flags==72 and n==size
  w,h,depth=struct.unpack_from('<III',raw,at+n);assert depth==1
  pixels=image.resize((max(4,w),max(4,h)),Image.Resampling.LANCZOS)
  payload=etcpak.compress_etc2_rgba(pixels.tobytes(),pixels.width,pixels.height);assert len(payload)==n,(name,level,w,h,n,len(payload));raw[at:at+n]=payload;at+=n+12;dims.append([w,h,n])
 assert len(raw)==len(original)
 packageid=struct.unpack_from('<Q',native.ids[i])[0];assert packageid in pids # Replace existing UI package, preserve its store entry
 paths[path]=len(chunks);chunks.append((native.ids[i],bytes(raw),hashlib.sha1(raw).digest()+b'\0'*12+b'\1'));rows.append({'path':path,'package_id':packageid,'mips':dims,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'native_header_and_size_preserved':True})
# Append isolated 2008 packages; all pre-existing head chunks above are verbatim.
newhead=Toc(str(out/'2008-container/pc9298_mobile_and.utoc'));hh=parse_header(newhead.read(next(i for i,c in enumerate(newhead.ids) if c[11]==10)))
assert not set(pids)&set(hh['pids'])
pids+=hh['pids'];entries += [store_entry(hh['store'],i) for i in range(len(hh['pids']))]
for path,i in sorted(newhead.files.items(),key=lambda x:x[1]):
 data=newhead.read(i);paths['character/'+path]=len(chunks);chunks.append((newhead.ids[i],data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
# Make a NEW container, never write through the preserved v11 symlink.
dest=out/'container'
if dest.is_symlink():dest.unlink()
dest.mkdir(exist_ok=True);name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];st=build_store(entries);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
ids=[];ols=[];blocks=[];voff=0;block=65536
with (dest/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for a in range(0,len(body),block):
   raw=body[a:a+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
di=dir_index(native.mount,paths);h=bytearray(old.raw[:old.hs]);struct.pack_into('<9I',h,20,old.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
blob=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(dest/(name+'.utoc')).write_bytes(blob);shutil.copyfile(out.parent/'player-faces-v12/container'/ (name+'.pak'),dest/(name+'.pak'))
t=Toc(str(dest/(name+'.utoc')))
for path,ix in paths.items():assert t.read(t.files[path])==chunks[ix][1]
report={'status':'EXACT_CARD_TWO_NATIVE_PORTRAITS_AND_ALL_HEAD_CHUNKS_PRESERVED_PASS','card_id':'88045755960841','artwork_sha256':hashlib.sha256(art.read_bytes()).hexdigest(),'head_chunks_copied_verbatim':sum(not p.startswith('ui/') for p in old.files),'textures':rows,'container_sha256':hashlib.sha256((dest/(name+'.ucas')).read_bytes()).hexdigest(),'phone_tested':False,'native_UI_overlays_preserved':True}
(out/'card-art-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(pids),'packages')

# Full build inventory for independent dependency and skeletal checks.
prior=json.loads((out.parent/'player-faces-v12/build-report.json').read_text());extra=json.loads((out/'2008-build-report.json').read_text());prior['meshes']+=extra['meshes'];prior['textures']+=extra['textures'];prior['packages']=[]
for i,packageid in enumerate(pids):
 name=next(Path(path).stem for path,ix in paths.items() if struct.unpack_from('<Q',chunks[ix][0])[0]==packageid and path.endswith('.uasset'))
 prior['packages'].append({'name':name,'package_id':packageid,'imports':entries[i][1]})
prior['status']='BUILT_PRESERVED_12_HEADS_PLUS_2008_AND_SINGLE_PORTRAIT_NOT_PHONE_VERIFIED';(out/'build-report.json').write_text(json.dumps(prior,indent=2))
