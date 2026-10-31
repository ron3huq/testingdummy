"""Runtime photograph IoStore writer. No network, external encoder or trial code."""
from pathlib import Path
import struct,hashlib,zlib,shutil,base64,json,types
class cityhash:
 @staticmethod
 def CityHash64(value):
  from diy_iostore import city64
  return city64(value)
def wstr(s):
 b=s.encode('latin1')+b'\0';return struct.pack('<i',len(b))+b
ENTRY=16
MASK=(1<<62)-1
def pid(s):return cityhash.CityHash64(s.lower().encode('utf-16-le'))
def objid(s):return (pid(s)&MASK)|(2<<62)
def rename(data,replacements,own_old=None,own_new=None,imports=None):
 b=bytearray(data);f=list(struct.unpack_from('<16I',b));ns,nsize,hs,hsize=f[6:10];at=ns;names=[];count=(hsize-8)//8;batch=bytearray();hashes=bytearray(b[hs:hs+hsize])
 for i in range(count):
  h=int.from_bytes(b[at:at+2],'big');at+=2;w=h>>15;n=h&32767;name=bytes(b[at:at+n*(2 if w else 1)]).decode('utf-16-le' if w else 'utf8');at+=n*(2 if w else 1)
  new=replacements.get(name,name);raw=new.encode('utf-16-le' if w else 'utf8');batch+=((len(new)|(w<<15))).to_bytes(2,'big')+raw;names.append((name,new))
  if new!=name:struct.pack_into('<Q',hashes,8+i*8,cityhash.CityHash64(new.lower().encode('utf-16-le' if w else 'utf8')))
 assert at==ns+nsize
 newhs=(ns+len(batch)+7)&~7;new=bytearray(b[:ns])+batch+b'\0'*(newhs-ns-len(batch))+hashes+b[hs+hsize:];shift=newhs-hs
 f[7]=len(batch);f[8]=newhs
 for j in [10,11,12,13]:f[j]+=shift
 struct.pack_into('<16I',new,0,*f)
 em=f[11];export_count=(f[12]-em)//72
 if own_old and own_new:
  oldbase=own_old.rsplit('/',1)[-1];newbase=own_new.rsplit('/',1)[-1]
  for i in range(export_count):
   field=em+72*i+56;v=struct.unpack_from('<Q',new,field)[0]
   if v==objid(own_old+'/'+oldbase):struct.pack_into('<Q',new,field,objid(own_new+'/'+newbase))
 for old,renamed in (imports or {}).items():
  oldval=objid(old+'/'+old.rsplit('/',1)[-1]);newval=objid(renamed+'/'+renamed.rsplit('/',1)[-1])
  for field in range(f[10],f[11],8):
   if struct.unpack_from('<Q',new,field)[0]==oldval:struct.pack_into('<Q',new,field,newval)
  gs=f[13];ge=gs+f[14];chunk=bytes(new[gs:ge]);chunk=chunk.replace(struct.pack('<Q',pid(old)),struct.pack('<Q',pid(renamed)));new[gs:ge]=chunk
 return bytes(new)

def build_store(entries):
    n = len(entries)
    head = bytearray(); tail = bytearray(); tail_base = ENTRY * n
    for i, (fixed, imports) in enumerate(entries):
        e = bytearray(fixed)
        field = ENTRY * i + 8
        if imports:
            pos = tail_base + len(tail); tail += struct.pack("<%dQ" % len(imports), *imports)
            e += struct.pack("<II", len(imports), pos - field)
        else:
            e += struct.pack("<II", 0, 0)
        head += e
    return bytes(head + tail)


def dir_index(mount, paths_to_index):
    """FIoDirectoryIndexResource with the given relative paths -> toc entry index."""
    strings, sidx = [], {}
    def S(x):
        if x not in sidx:
            sidx[x] = len(strings); strings.append(x)
        return sidx[x]
    dirs = [[0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]]  # root
    files = []
    children = {0: {}}
    for path, idx in sorted(paths_to_index.items()):
        parts = path.split("/")
        d = 0
        for part in parts[:-1]:
            ch = children[d]
            if part not in ch:
                nd = len(dirs); dirs.append([S(part), 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF]); children[nd] = {}
                # prepend as first child
                dirs[nd][2] = dirs[d][1]; dirs[d][1] = nd; ch[part] = nd
            d = ch[part]
        fi = len(files); files.append([S(parts[-1]), dirs[d][3], idx]); dirs[d][3] = fi
    out = bytearray(wstr(mount))
    out += struct.pack("<I", len(dirs)) + b"".join(struct.pack("<IIII", *x) for x in dirs)
    out += struct.pack("<I", len(files)) + b"".join(struct.pack("<III", *x) for x in files)
    out += struct.pack("<I", len(strings)) + b"".join(wstr(x) for x in strings)
    return bytes(out)


class Bundle:
 def __init__(self,t):
  self.base=t;self.files={p:(t.ids[i],t.read(i)) for p,i in t.files.items()};h=parse_header(t.read(next(i for i,x in enumerate(t.ids) if x[11]==10)));self.entries={p:store_entry(h['store'],i) for i,p in enumerate(h['pids'])}
 def put(self,path,idb,data,entry=None):
  self.files[path]=(idb,bytes(data))
  if entry is not None:self.entries[int.from_bytes(idb[:8],'little')]=entry
 def native(self,t,path,data):
  i=t.files[path];h=parse_header(t.read(next(i for i,x in enumerate(t.ids) if x[11]==10)));pk=int.from_bytes(t.ids[i][:8],'little');dest=t.mount+path;dest=dest.split('/Content/Assets/',1)[1];self.put(dest,t.ids[i],data,store_entry(h['store'],h['pids'].index(pk)))
 def write(self,out):
  out=Path(out);out.mkdir(parents=True,exist_ok=True);name='pc9311_mobile_and';cid=int.from_bytes(hashlib.sha256(name.encode()).digest()[:8],'little');chunks=[];paths={};pids=[]
  for p,(idb,b) in self.files.items():
   paths[p]=len(chunks);chunks.append((idb,b,hashlib.sha1(b).digest()+b'\0'*12+b'\1'))
   if p.endswith('.uasset'):pids.append(int.from_bytes(idb[:8],'little'))
  assert len(set(pids))==len(pids);st=build_store([self.entries[p] for p in pids]);hb=struct.pack('<QIiiiQ',cid,len(pids),0,8,0,0) if False else struct.pack('<QI',cid,len(pids))+struct.pack('<i',0)+struct.pack('<iQ',8,0xC1640000)
  hb+=struct.pack('<i',len(pids))+struct.pack('<%dQ'%len(pids),*pids)+struct.pack('<i',len(st))+st+struct.pack('<ii',0,0);chunks.append((struct.pack('<Q',cid)+b'\0\0\0\x0a',hb,hashlib.sha1(hb).digest()+b'\0'*13));ids=[];ols=[];blocks=[];voff=0;block=65536
  with (out/(name+'.ucas')).open('wb') as f:
   for idb,body,meta in chunks:
    ids.append(idb);ols.append((voff,len(body)))
    for a in range(0,len(body),block):
     raw=body[a:a+block];comp=zlib.compress(raw,3);method=int(len(comp)<len(raw));p=comp if method else raw;blocks.append((f.tell(),len(p),len(raw),method));f.write(p)
    voff+=(len(body)+block-1)//block*block
  di=dir_index('../../../PesMobile/Content/Assets/',paths);h=bytearray(self.base.raw[:self.base.hs]);struct.pack_into('<9I',h,20,self.base.hs,len(ids),len(blocks),12,1,32,block,len(di),0);struct.pack_into('<Q',h,56,cid);h[64:80]=b'\0'*16;h[80]=9
  data=bytes(h)+b''.join(ids)+b''.join(a.to_bytes(5,'big')+b.to_bytes(5,'big') for a,b in ols)+b''.join(a.to_bytes(5,'little')+b.to_bytes(3,'little')+c.to_bytes(3,'little')+bytes([m]) for a,b,c,m in blocks)+b'Zlib'.ljust(32,b'\0')+di+b''.join(x[2] for x in chunks);(out/(name+'.utoc')).write_bytes(data);shutil.copyfile(self.base.path[:-5]+'.pak',out/(name+'.pak'))
  return out

def templates():return json.loads(zlib.decompress(Path(__file__).with_name('photo_templates.zlib').read_bytes()))
def _pak_aes(data,encrypt):
 # Android's platform AES; the host fallback is only for build/readback tests.
 try:
  from java import jclass,jarray,jbyte
 except ImportError:
  from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
  cipher=Cipher(algorithms.AES(bytes.fromhex('4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295')),modes.ECB())
  c=cipher.encryptor()if encrypt else cipher.decryptor();return c.update(data)+c.finalize()
 key=bytes.fromhex('4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295')
 def arr(b):return jarray(jbyte)([v if v<128 else v-256 for v in b])
 c=jclass('javax.crypto.Cipher').getInstance('AES/ECB/NoPadding');c.init(1 if encrypt else 2,jclass('javax.crypto.spec.SecretKeySpec')(arr(key),'AES'))
 return bytes(v&255 for v in c.doFinal(arr(data)))

def stamp_empty_pak(path,digest):
 # Native version11 empty PAK: exactly144B encrypted indexes +221B footer.
 # Vary the existing PathHashSeed of a zero-entry index, then recompute its
 # SHA1 and encrypt. No inserted gap, trailer or custom marker is necessary.
 p=Path(path);b=p.read_bytes();footer=bytearray(b[-221:])
 if len(b)not in(365,405)or footer[17:21]!=bytes.fromhex('e1126f5a')or struct.unpack_from('<Iqq',footer,21)!=(11,0,112):raise ValueError('Unrecognized native empty PAK')
 plain=bytearray(_pak_aes(b[:144],False))
 if plain[:10]!=bytes.fromhex('020000002f0000000000'):raise ValueError('PAK has entries or an unexpected mount point')
 # Verify the old authenticated index before modifying its legitimate seed.
 if hashlib.sha1(plain[:112]).digest()!=footer[41:61]:raise ValueError('Empty PAK index SHA1 mismatch')
 struct.pack_into('<Q',plain,10,int.from_bytes(bytes.fromhex(digest)[:8],'little'))
 footer[41:61]=hashlib.sha1(plain[:112]).digest()
 p.write_bytes(_pak_aes(bytes(plain),True)+footer)

def downsample_bgra(src,w,h):
 # Alpha-weighted box filter; never mixes a transparent black edge into skin.
 nw,nh=max(1,w//2),max(1,h//2);out=bytearray(nw*nh*4)
 for y in range(nh):
  for x in range(nw):
   points=[(min(h-1,y*2+dy)*w+min(w-1,x*2+dx))*4 for dy in [0,1]for dx in [0,1]];alpha=sum(src[j+3]for j in points);k=(y*nw+x)*4;out[k+3]=(alpha+2)//4
   if alpha:
    for c in range(3):out[k+c]=(sum(src[j+c]*src[j+3]for j in points)+alpha//2)//alpha
 return bytes(out),nw,nh

def portrait_payload(row,image):
 raw=base64.b64decode(row['data']);fmt=raw.rfind(b'PF_B8G8R8A8\0');first=fmt+len(b'PF_B8G8R8A8\0')+8;count=struct.unpack_from('<I',raw,first-4)[0]
 if count<1 or count>16:raise ValueError('Invalid portrait mip template')
 end=first
 for i in range(count):
  n=struct.unpack_from('<I',raw,end+8)[0];end+=24+n+12
 if end>len(raw):raise ValueError('Truncated portrait mip template')
 body=bytearray();pixels=image;w,h=row['w'],row['h']
 for i in range(count):
  if len(pixels)!=w*h*4:raise ValueError('BGRA mip size mismatch')
  body+=struct.pack('<IIIIq',1,0x48,len(pixels),len(pixels),0)+pixels+struct.pack('<III',w,h,1)
  if i+1<count:pixels,w,h=downsample_bgra(pixels,w,h)
 data=bytearray(raw[:first])+body+raw[end:];delta=len(data)-len(raw);f=struct.unpack_from('<16I',raw)
 struct.pack_into('<Q',data,f[11]+8,struct.unpack_from('<Q',raw,f[11]+8)[0]+delta)
 struct.pack_into('<Q',data,fmt-24,struct.unpack_from('<Q',raw,fmt-24)[0]+delta)
 return data

def create(out,photos):
 Path(out).mkdir(parents=True,exist_ok=True)
 doc=templates();header=base64.b64decode(doc['header']);pak=Path(out).parent/'empty-photo.pak';pak.write_bytes(base64.b64decode(doc['pak']))
 obj=Bundle.__new__(Bundle);obj.base=types.SimpleNamespace(raw=header,hs=len(header),path=str(pak)[:-4]+'.utoc');obj.files={};obj.entries={}
 for card,images in sorted(photos.items()):
  for row,image in zip(doc['rows'],images):
   raw=bytearray(base64.b64decode(row['data']));n=row['w']*row['h']*4
   if len(image)!=n:raise ValueError('Portrait dimensions mismatch')
   raw=portrait_payload(row,image);old=row['old'];new='U712_'+card+('_l'if old.endswith('_l')else'_');own=row['path'];dest=own.replace(old,new);data=rename(raw,{old:new,own:dest},own,dest);key=pid(dest);path=dest.split('/Game/Assets/',1)[1]+'.uasset';obj.put(path,struct.pack('<Q',key)+b'\0\0\0\2',data,(base64.b64decode(row['fixed']),row['imports']))
   alias=dest.replace('/Player/Variation2022/','/Player/');aliasdata=rename(data,{dest:alias},dest,alias);obj.put(alias.split('/Game/Assets/',1)[1]+'.uasset',struct.pack('<Q',pid(alias))+b'\0\0\0\2',aliasdata,(base64.b64decode(row['fixed']),row['imports']))
 obj.write(out);h=hashlib.sha256()
 for ext in ['utoc','ucas']:
  with (Path(out)/('pc9311_mobile_and.'+ext)).open('rb')as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
 stamp_empty_pak(Path(out)/'pc9311_mobile_and.pak',h.hexdigest());pak.unlink()
