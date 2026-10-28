"""Explicit photo imports in immutable per-generation native containers; no per-frame work."""
from pathlib import Path
import json,base64,hashlib,zlib,threading,functools,re,shutil,ctypes as C
import body_dimensions as body
HERE=Path(__file__).resolve().parent;LIVE=HERE.parents[1]/'livedata/ui712-photos';STATE=HERE/'ui712-photo-state.json';KEY='ui712_photos';_lock=threading.RLock();_profiles={};_conn=None

def load(c):
 global _conn,_profiles
 if c is _conn:return
 row=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();_profiles=json.loads(row[0])if row else{}
 if not isinstance(_profiles,dict)or len(_profiles)>256:raise ValueError('Maximum256 custom photo cards')
 for pid in _profiles:body.identity(pid)
 if _profiles and not STATE.is_file():raise ValueError('Custom photo resources missing; import your images again')
 _conn=c

def decode(text,w,h):
 if not isinstance(text,str)or not text.startswith('data:image/png;base64,')or len(text)>6*1024*1024:raise ValueError('Invalid portrait PNG')
 from diy_iostore import rgba_png
 raw=rgba_png(base64.b64decode(text.split(',',1)[1],validate=True));assert len(raw)==512*512*4
 cropped=b''.join(raw[y*2048:y*2048+w*4]for y in range(h));out=bytearray(len(cropped));out[0::4]=cropped[2::4];out[1::4]=cropped[1::4];out[2::4]=cropped[0::4];out[3::4]=cropped[3::4]
 return bytes(out)

def generation(photos):
 from photo_codec import create
 digest=hashlib.sha256(b''.join(pid.encode()+b''.join(images)for pid,images in sorted(photos.items()))).hexdigest()[:24];folder=LIVE/('g_'+digest);folder.mkdir(parents=True,exist_ok=True)
 create(folder,photos);files={}
 for ext in ['pak','utoc','ucas']:
  p=folder/('pc9311_mobile_and.'+ext);files[p.name]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'relative':str(p.relative_to(LIVE.parent))}
 return {'generation':digest,'files':files,'count':len(photos)}

def prune_generations(current,previous):
 # Retain the current and immediately previous immutable download generations.
 # No game engine is loaded while importing; already-open HTTP file handles remain valid.
 keep={'g_'+current}
 if previous:keep.add('g_'+previous)
 for folder in LIVE.iterdir():
  if folder.name not in keep and re.fullmatch(r'g_[0-9a-f]{24}',folder.name)and folder.is_dir()and not folder.is_symlink():
   try:shutil.rmtree(folder)
   except OSError:pass

def manage(c,action,req):
 global _profiles
 with _lock,body._lock:
  load(c);pid,player=body.owned(c,req)
  if action.endswith('_get'):return {'custom':pid in _profiles,'limit':256,'mini':[128,128],'large':[184,256]}
  if body.engine_loaded():raise ValueError('Close and reopen the app; import photos before Enter Game')
  if c.in_transaction:raise ValueError('Another save operation is active')
  images=[decode(req.get('mini'),128,128),decode(req.get('large'),184,256)];updated=dict(_profiles);updated[pid]=[base64.b64encode(zlib.compress(x,6)).decode()for x in images]
  if len(updated)>256:raise ValueError('Maximum256 custom photo cards')
  photos={p:[zlib.decompress(base64.b64decode(x))for x in pair]for p,pair in updated.items()};meta=generation(photos);before=STATE.read_bytes()if STATE.exists()else None;meta['revision']=(json.loads(before).get('revision',0)if before else 0)+1
  if body.engine_loaded():raise ValueError('Game started during import; reopen and import again')
  try:
   c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(meta));tmp.replace(STATE);c.commit()
  except Exception:
   c.rollback()
   if before is None:STATE.unlink(missing_ok=True)
   else:tmp=STATE.with_suffix('.rollback');tmp.write_bytes(before);tmp.replace(STATE)
   raise
  _profiles=updated
  prune_generations(meta['generation'],json.loads(before).get('generation')if before else None)
  return {'saved':True,'card_id':pid,'generation':meta['generation']}

def advertise(value,port):
 if not _profiles or not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 from mod_integrity import digest
 d=json.loads(STATE.read_text());r={ext:d['files']['pc9311_mobile_and.'+ext]for ext in ['pak','utoc','ucas']}
 for row in r.values():
  p=(LIVE.parent/row['relative']).resolve()
  if not p.is_relative_to(LIVE.resolve())or p.stat().st_size!=row['size']or digest(p)!=row['sha256']:raise ValueError('Custom photo payload mismatch')
 ver=json.loads(value['version_file']);item={'name':'pc9311','hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']}
 if not any(x==item for x in ver['dt880']):ver['version']+=712+int(d.get('revision',1))
 ver['dt880']=[x for x in ver['dt880']if x.get('name')!='pc9311']+[item];out=dict(value);names={'pc9311_mobile_and.'+x for x in r};out['livedata_list']=[x for x in value['livedata_list']if x.get('name')not in names]+[{'name':'pc9311_mobile_and.'+ext,'size':row['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+row['relative']}for ext,row in r.items()];out['version_file']=json.dumps(ver,separators=(',',':'));return out

def configure(h):
 h.noodle_photo_add.argtypes=[C.c_uint64];h.noodle_photo_add.restype=C.c_uint
 for pid in _profiles:
  if h.noodle_photo_add(int(pid))!=1:raise ValueError('Custom photo ID rejected')
 h.noodle_photo_commit.argtypes=[];h.noodle_photo_commit.restype=None;h.noodle_photo_commit()

def install(module):
 if getattr(module.manage,'_ui712_photo',False):return
 load(module._logic.conn);old=module.manage
 @functools.wraps(old)
 def wrapper(action,payload=''):
  if action in ['ui712_photo_get','ui712_photo_apply']:return json.dumps(manage(module._logic.conn,action,json.loads(payload or'{}')))
  return old(action,payload)
 wrapper._ui712_photo=True;module.manage=wrapper
