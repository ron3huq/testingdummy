"""RGB body albedo assets; generated before engine load, with immutable colour generations."""
import base64,ctypes as C,functools,hashlib,json,platform,re,threading,zlib
from pathlib import Path
import skin_iostore
HERE=Path(__file__).resolve().parent;DEFAULTS={'106754901843130':'4e5b37'};ROOT=None;_lock=threading.RLock();_selected=None;_keep=[]
def colour(value):
 if value is None:return None
 if not isinstance(value,str)or not re.fullmatch(r'#[0-9a-fA-F]{6}|[0-9a-fA-F]{6}',value):raise ValueError('RGB colour must be exactly6 hex digits; alpha is not editable')
 return value.lstrip('#').lower()
def effective(profiles):
 out=dict(DEFAULTS)
 for pid,row in profiles.items():
  if 'rgb'in row:
   v=colour(row['rgb'])
   if v is None:out.pop(pid,None)
   else:out[pid]=v
  elif 'skin'in row:out.pop(pid,None)
 if len(out)>1024:raise ValueError('Maximum1024 custom-colour card profiles, including the default Hulk profile')
 if len(set(out.values()))>64:raise ValueError('Maximum64 distinct custom RGB colours; reuse a colour or remove a custom setting')
 return out
@functools.lru_cache(maxsize=1)
def templates():return json.loads(zlib.decompress((HERE/'skin_templates.zlib').read_bytes()))
@functools.lru_cache(maxsize=3)
def source(part):return zlib.decompress(base64.b64decode(templates()['source'][part]['pixels']))
@functools.lru_cache(maxsize=1)
def codec():
 if platform.machine().lower()not in ['aarch64','arm64']:return None
 import noodle_hair
 from mod_integrity import digest
 path=HERE/'libnoodle_hair.so'
 if digest(path)!=noodle_hair.HOOK_SHA:raise ValueError('RGB pixel-codec hash mismatch')
 lib=C.CDLL(str(path));lib.tint_bgra.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint,C.c_uint];lib.tint_bgra.restype=None;_keep.append(lib);return lib

def tint(data,rgb,reference):
 value=int(rgb,16);out=bytearray(len(data));lib=codec()
 if lib is not None:
  src=(C.c_ubyte*len(data)).from_buffer_copy(data);dst=(C.c_ubyte*len(out)).from_buffer(out);lib.tint_bgra(src,dst,len(data)//4,value,reference)
 else:
  r,g,b=value>>16,(value>>8)&255,value&255
  for i in range(0,len(data),4):
   y=(data[i+2]*54+data[i+1]*183+data[i]*19)>>8;out[i]=min(255,(y*b+reference//2)//reference);out[i+1]=min(255,(y*g+reference//2)//reference);out[i+2]=min(255,(y*r+reference//2)//reference);out[i+3]=data[i+3]
 return bytes(out)

def prepare(root,profiles):
 root=Path(root);values=effective(profiles);colours=sorted(set(values.values()));fingerprint=hashlib.sha256((HERE/'skin_templates.zlib').read_bytes()+json.dumps(colours).encode()).hexdigest();stem='pc9304_rgb'+fingerprint[:12]+'_mobile_and';live=root/'livedata';live.mkdir(parents=True,exist_ok=True);cached=live/(stem+'.json');slots={rgb:i+1 for i,rgb in enumerate(colours)}
 if cached.exists():
  doc=json.loads(cached.read_text())
  if all((live/(stem+'.'+ext)).exists()and(live/(stem+'.'+ext)).stat().st_size==row['size']and __import__('mod_integrity').digest(live/(stem+'.'+ext))==row['sha256']for ext,row in doc['files'].items()):return doc
 table=templates();files=[]
 for rgb in colours:
  slot=str(slots[rgb])
  for part,row in table['slots'][slot].items():
   data=bytearray(zlib.decompress(base64.b64decode(row['data'])));pixels=tint(source(part),rgb,table['source'][part]['reference']);at=0
   for pos,n,w,h in row['spans']:data[pos:pos+n]=pixels[at:at+n];at+=n
   assert at==len(pixels);files.append((row['path'],bytes.fromhex(row['id']),bytes(data),(base64.b64decode(row['fixed']),row['imports'])))
 stage=live/('.ui79-rgb-'+fingerprint[:12]);meta=skin_iostore.write(stage,stem,base64.b64decode(table['header']),base64.b64decode(table['pak']),files)
 doc={'schema':1,'fingerprint':fingerprint,'stem':stem,'slots':slots,'files':meta,'alpha_unchanged':True,'pixel_format':'PF_B8G8R8A8'}
 for ext in ['pak','utoc','ucas']:(stage/(stem+'.'+ext)).replace(live/(stem+'.'+ext))
 stage.rmdir();temp=cached.with_suffix('.tmp');temp.write_text(json.dumps(doc,indent=2));temp.replace(cached);return doc

def activate(root,profiles,doc=None):
 global ROOT,_selected
 with _lock:ROOT=Path(root);_selected=doc or prepare(root,profiles)
def configure_native(hook,profiles):
 values=effective(profiles);doc=_selected
 if doc is None:raise ValueError('RGB texture generation not prepared')
 hook.noodle_rgb_add.argtypes=[C.c_uint64,C.c_uint];hook.noodle_rgb_add.restype=C.c_uint
 for pid,rgb in values.items():
  if hook.noodle_rgb_add(int(pid),doc['slots'][rgb])!=1:raise ValueError('RGB native card profile rejected')
 hook.noodle_rgb_commit.argtypes=[];hook.noodle_rgb_commit.restype=None;hook.noodle_rgb_commit()
def advertise(value,port):
 if not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 with _lock:doc=_selected
 if not doc or not doc['slots']:return value
 version=json.loads(value['version_file']);r=doc['files'];logical='pc9304_mobile_and';item={'name':'pc9304','hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']};prior=next((x for x in version['dt880']if isinstance(x,dict)and x.get('name')=='pc9304'),None)
 if prior!=item:version['version']+=10000+int(doc['fingerprint'][:6],16)
 if version['version']>=2**31:raise ValueError('Resource version overflow')
 version['dt880']=[x for x in version['dt880']if not isinstance(x,dict)or x.get('name')!='pc9304']+[item];out=dict(value);out['version_file']=json.dumps(version,separators=(',',':'));names={logical+'.'+ext for ext in r};out['livedata_list']=[x for x in value['livedata_list']if not isinstance(x,dict)or x.get('name')not in names];out['livedata_list'] +=[{'name':logical+'.'+ext,'size':r[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+doc['stem']+'.'+ext}for ext in ['pak','utoc','ucas']];return out
