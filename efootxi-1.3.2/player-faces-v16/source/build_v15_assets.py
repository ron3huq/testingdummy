"""Runtime-only head experiment plus exact-ID native card texture replacements.
Preserve ALL 13 head/hair packages and large Xuan Son portrait byte-for-byte.
"""
from pathlib import Path
import struct,hashlib,json,zlib,shutil
import etcpak
from PIL import Image,ImageOps
from iostore import Toc,parse_header,store_entry,build_store,dir_index
out=Path(__file__).resolve().parent.parent;work=Path('/workspace/ronaldo-work');old=Toc(str(out.parent/'player-faces-v14/container/pc9298_mobile_and.utoc'))
natives=[Toc(str(next((work/'resources').rglob('pc100'+str(i)+'_mobile_and.utoc')))) for i in [0,1]]
choices={card:card for card in ['105848932271764','88033139360669','88038776539586','105643042189511','89135066911146','106726716084650','106781745353130','88044950524330','105765448873424','88045755960841','106728863696709']}
replacements={};new_entries={};rows=[]
for card,filename in list(choices.items()):
 for suffix in ['_','_l']:
  stem=card+suffix;native,path=next((t,p) for t in natives for p in t.files if Path(p).name==stem+'.uasset');destpath=path.removeprefix('Assets/')
  original=native.read(native.files[path]);raw=bytearray(original);source=out/'art'/(card+('-small.png' if suffix=='_' else '-large.png'));image=Image.open(source).convert('RGBA');fmt=raw.rfind(b'PF_ETC2_RGBA\0');assert fmt>0
  at=fmt+len(b'PF_ETC2_RGBA\0');first,count=struct.unpack_from('<II',raw,at);at+=8;assert first==0;dims=[]
  for level in range(count):
   cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and flags==72 and n==size
   w,h,z=struct.unpack_from('<III',raw,at+n);assert z==1
   pixels=ImageOps.fit(image,(max(4,w),max(4,h)),Image.Resampling.LANCZOS);payload=etcpak.compress_etc2_rgba(pixels.tobytes(),pixels.width,pixels.height);assert len(payload)==n
   raw[at:at+n]=payload;at+=n+12;dims.append([w,h])
  assert len(raw)==len(original)
  i=native.files[path];idb=native.ids[i];replacements[destpath]=(idb,bytes(raw));pid=struct.unpack_from('<Q',idb)[0]
  hd=parse_header(native.read(next(i for i,c in enumerate(native.ids) if c[11]==10)));new_entries[pid]=store_entry(hd['store'],hd['pids'].index(pid))
  rows.append({'card_id':card,'file':source.name,'path':destpath,'dimensions':dims,'source_container':['pc1000_mobile_and','pc1001_mobile_and'][natives.index(native)],'package_id':pid,'sha256':hashlib.sha256(raw).hexdigest(),'source_image_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
from head_mq_and_seams import head_changes
head_replacements,head_entries,head_report=head_changes(old,out)
replacements.update(head_replacements);new_entries.update(head_entries)
chunks=[];paths={};hd=parse_header(old.read(next(i for i,c in enumerate(old.ids) if c[11]==10)));pids=list(hd['pids']);entries=[store_entry(hd['store'],i) for i in range(len(pids))]
for path,i in sorted(old.files.items(),key=lambda x:x[1]):
 if path in replacements:continue
 data=old.read(i);paths[path]=len(chunks);chunks.append((old.ids[i],data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
for path,(idb,data) in replacements.items():
 pid=struct.unpack_from('<Q',idb)[0]
 if pid not in pids:pids.append(pid);entries.append(new_entries[pid])
 else:entries[pids.index(pid)]=new_entries[pid]
 paths[path]=len(chunks);chunks.append((idb,data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'))
dest=out/'container';dest.mkdir(exist_ok=True);name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];st=build_store(entries);hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
ids=[];ols=[];blocks=[];voff=0;block=65536
with (dest/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for a in range(0,len(body),block):
   raw=body[a:a+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
mount='../../../PesMobile/Content/Assets/';di=dir_index(mount,paths);h=bytearray(old.raw[:old.hs]);struct.pack_into('<9I',h,20,old.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
blob=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks);(dest/(name+'.utoc')).write_bytes(blob);shutil.copyfile(out.parent/'player-faces-v14/container'/(name+'.pak'),dest/(name+'.pak'))
t=Toc(str(dest/(name+'.utoc')))
for path,ix in paths.items():assert t.read(t.files[path])==chunks[ix][1]
head_count=0
for path,i in old.files.items():
 if path.startswith('character/'):
  if path not in head_replacements:assert old.read(i)==t.read(t.files[path]);head_count+=1
report={'status':'V15_NATIVE_MQ_FOUR_HEADS_DINH_BAC_SEAMS_AND_11_CARD_PAIRS_PASS','cards':rows,'changed_UI_textures':len(rows),'head_chunks_byte_identical':head_count,'head_changes':head_report,'ignored_input':'ronaldo 2008 plus.png','phone_tested':False,'container_sha256':hashlib.sha256((dest/(name+'.ucas')).read_bytes()).hexdigest()};(out/'card-art-validation.json').write_text(json.dumps(report,indent=2));(out/'head-changes.json').write_text(json.dumps(head_report,indent=2))
build=json.loads((out.parent/'player-faces-v14/build-report.json').read_text());build['packages']=[]
for i,packageid in enumerate(pids):
 stem=next(Path(path).stem for path,ix in paths.items() if struct.unpack_from('<Q',chunks[ix][0])[0]==packageid and path.endswith('.uasset'));build['packages'].append({'name':stem,'package_id':packageid,'imports':entries[i][1]})
(out/'build-report.json').write_text(json.dumps(build,indent=2));print(report['status'],head_count,'head chunks',len(pids),'packages')
