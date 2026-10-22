from pathlib import Path
import sys,struct,zlib,hashlib,json
from zen_clone import pid
sys.path.insert(0,'/workspace/testingdummy/tools');from make_extra_pak import Toc,parse_header,store_entry,build_store,dir_index
r=Path(__file__).parent;p=r.parent
heads=Toc(str(p/'pc3700-new/pc3700_mobile_and.utoc'));mats=Toc('/workspace/analysis/my-league/android/official-apk/assets/gateway-release/livedata/pc9257_mobile_and.utoc')
def entry(t,path):
 h=parse_header(t.read(next(i for i,c in enumerate(t.ids) if c[11]==10)));i=t.files[path];oldpid=struct.unpack('<Q',t.ids[i][:8])[0];return store_entry(h['store'],h['pids'].index(oldpid))
base='/Game/Assets/character/RealFace/';headimport={pid(base+'MI_4522_Head_Hair_'+q):pid(base+'MI_ND0001_Head_Hair_'+q) for q in ['HQ','MQ']};matimport={pid(base+'T_133157_Hair_D'):pid(base+'T_ND0001_Hair_D')}
recipes=[]
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 remap={pid(base+'MI_'+variant+'_Head_Hair_'+q):pid(base+'MI_ND0001_Head_Hair_'+q) for q in ['HQ','MQ']}
 recipes.append(('SK_'+variant.replace('4522','ND01',1)+'_Face',heads,'RealFace/SK_'+variant+'_Face.uasset',remap))
recipes +=[(f'MI_ND0001_Head_Hair_{q}',mats,'character/RealFace/MI_133157_Head_Hair_MQ.uasset',matimport) for q in ['HQ','MQ']]
recipes +=[('T_ND0001_Hair_D',mats,'character/RealFace/T_133157_Hair_High_D.uasset',{})]
recipes +=[('T_'+v.replace('4522','ND01',1)+'_Face_D',mats,'character/RealFace/T_133157_Face_D.uasset',{}) for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']]
chunks=[];entries=[];pids=[];paths={};pkginfo=[]
for name,t,source,remap in recipes:
 newpid=pid(base+name);data=(r/'asset'/(name+'.uasset')).read_bytes();i=len(chunks);chunks.append((struct.pack('<Q',newpid)+b'\0\0\0\2',data,hashlib.sha1(data).digest()+b'\0'*12+b'\1'));paths['RealFace/'+name+'.uasset']=i
 bulk=r/'asset'/(name+'.ubulk')
 if bulk.exists():
  b=bulk.read_bytes();paths['RealFace/'+name+'.ubulk']=len(chunks);chunks.append((struct.pack('<Q',newpid)+b'\0\0\0\3',b,hashlib.sha1(b).digest()+b'\0'*12+b'\1'))
 fixed,imports=entry(t,source);imports=[remap.get(x,x) for x in imports];entries.append((fixed,imports));pids.append(newpid);pkginfo.append({'name':name,'package_id':newpid,'imports':imports})
name='pc9298_mobile_and';cid=struct.unpack('<Q',hashlib.sha256(name.encode()).digest()[:8])[0];block=65536;st=build_store(entries)
hb=struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)+struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0)
chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13))
out=r/'container';out.mkdir(exist_ok=True);ids=[];ols=[];blocks=[];voff=0
with (out/(name+'.ucas')).open('wb') as f:
 for idb,body,meta in chunks:
  ids.append(idb);ols.append((voff,len(body)))
  for at in range(0,len(body),block):
   raw=body[at:at+block];comp=zlib.compress(raw,9);method=int(len(comp)<len(raw));payload=comp if method else raw;blocks.append((f.tell(),len(payload),len(raw),method));f.write(payload)
  voff+=(len(body)+block-1)//block*block
di=dir_index(heads.mount,paths);h=bytearray(heads.raw[:heads.hs]);struct.pack_into('<9I',h,20,heads.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
blob=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(c[2] for c in chunks)
(out/(name+'.utoc')).write_bytes(blob);(out/(name+'.pak')).write_bytes((p/'pc3700-new/pc3700_mobile_and.pak').read_bytes())
t=Toc(str(out/(name+'.utoc')))
for path,i in paths.items():assert t.read(i)==(r/'asset'/Path(path).name).read_bytes()
newhdr=parse_header(t.read(len(chunks)-1));assert newhdr['pids']==pids
for i,e in enumerate(entries):assert store_entry(newhdr['store'],i)==e
(r/'container-validation.json').write_text(json.dumps({'packages':pkginfo,'asset_bulk_readback_identical':True,'private_dependencies_resolve':all(x in pids for x in headimport.values()) and all(x in pids for x in matimport.values()),'file_hashes':{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in [name+'.pak',name+'.utoc',name+'.ucas']}},indent=2));print('Four packages and ETC2 bulk round-trip; new imports resolve inside private container.')
