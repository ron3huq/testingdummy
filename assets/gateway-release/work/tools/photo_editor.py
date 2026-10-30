"""Explicit photo imports in immutable per-generation native containers; no per-frame work."""
from pathlib import Path
import json,base64,hashlib,zlib,threading,functools,re,shutil,ctypes as C
import body_dimensions as body
HERE=Path(__file__).resolve().parent;LIVE=HERE.parents[1]/'livedata/ui712-photos';STATE=HERE/'ui712-photo-state.json';KEY='ui712_photos';_lock=threading.RLock();_profiles={};_conn=None

SUPPLIED_ART_IDS={'89138288266704','105625593957752','106781476920663','88042803047215','106654775417922','105565464400480','105756321970183','105647605587130','105634720685845','105794439855675','105568954067359'}
def apply_new_supplied_art_once(c,profiles):
 # The user explicitly supplied replacements for these11cards. Back up only
 # their older custom crops, then let the new bundled art display. Subsequent
 # imports keep their normal priority; unrelated card photos/save are untouched.
 marker='ui716_supplied_art_v1'
 if c.execute('SELECT 1 FROM meta WHERE key=?',(marker,)).fetchone():return profiles
 replaced={k:v for k,v in profiles.items()if k in SUPPLIED_ART_IDS};updated={k:v for k,v in profiles.items()if k not in replaced}
 if c.in_transaction:raise ValueError('Finish the active save transaction before applying supplied portraits')
 try:
  c.execute('BEGIN IMMEDIATE')
  if replaced:
   c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',('ui716_previous_custom_portraits',json.dumps(replaced,separators=(',',':'))))
   c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))))
  c.execute('INSERT INTO meta(key,value)VALUES(?,?)',(marker,'1'));c.commit()
 except Exception:c.rollback();raise
 return updated

def diagnostic(advertised=False):
 try:
  d=json.loads(STATE.read_text())if STATE.exists()else{};out={'version':'73-ui7.16','custom_cards':len(_profiles),'generation':d.get('generation'),'advertised':advertised,'files':{n:{'size':r['size'],'sha256':r['sha256']}for n,r in d.get('files',{}).items()},'pixel_data_included':False};path=HERE/'ui716-photo-status.json';tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(out,indent=2));tmp.replace(path)
 except (OSError,ValueError,KeyError):pass

def load(c):
 global _conn,_profiles
 if c is _conn:return
 row=c.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone();_profiles=json.loads(row[0])if row else{}
 if not isinstance(_profiles,dict)or len(_profiles)>256:raise ValueError('Maximum256 custom photo cards')
 for pid in _profiles:body.identity(pid)
 _profiles=apply_new_supplied_art_once(c,_profiles)
 if _profiles:ensure_saved_generation()
 _conn=c
 diagnostic()

def unpack_saved(photos):
 out={}
 for pid,pair in photos.items():
  if not isinstance(pair,list)or len(pair)!=2:raise ValueError('Invalid saved portrait pair')
  images=[]
  for text,size in zip(pair,[128*128*4,184*256*4]):
   raw=base64.b64decode(text,validate=True);codec=zlib.decompressobj();image=codec.decompress(raw,size+1)
   if len(image)!=size or not codec.eof or codec.unconsumed_tail or codec.unused_data:raise ValueError('Invalid saved portrait dimensions')
   images.append(image)
  out[pid]=images
 return out

def ensure_saved_generation():
 # Save Manager restores SQL records independently from generated files. Rebuild
 # missing resources from the exact saved crops, before advertising any download.
 previous={}
 try:
  previous=json.loads(STATE.read_text())
  expected=hashlib.sha256(b''.join(pid.encode()+b''.join(images)for pid,images in sorted(unpack_saved(_profiles).items()))).hexdigest()[:24]
  if previous.get('pak_schema')!=17:raise ValueError('Upgrade photo PAK layout')
  if previous.get('generation')!=expected:raise ValueError('Saved photo profiles changed')
  from mod_integrity import digest
  if len(previous['files'])!=3:raise ValueError('Incomplete portrait generation')
  for row in previous['files'].values():
   p=(LIVE.parent/row['relative']).resolve()
   if not p.is_relative_to(LIVE.resolve())or p.stat().st_size!=row['size']or digest(p)!=row['sha256']:raise ValueError('Portrait generation needs repair')
  return
 except (OSError,ValueError,KeyError,TypeError):pass
 meta=generation(unpack_saved(_profiles));meta['revision']=int(previous.get('revision',0))+1
 temp=STATE.with_suffix('.repair.tmp');temp.write_text(json.dumps(meta));temp.replace(STATE)

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
 return {'generation':digest,'files':files,'count':len(photos),'pak_schema':17}

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
  photos=unpack_saved(updated);meta=generation(photos);before=STATE.read_bytes()if STATE.exists()else None;meta['revision']=(json.loads(before).get('revision',0)if before else 0)+1
  if body.engine_loaded():raise ValueError('Game started during import; reopen and import again')
  try:
   c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(updated,separators=(',',':'))));tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(meta));tmp.replace(STATE);c.commit()
  except Exception:
   c.rollback()
   if before is None:STATE.unlink(missing_ok=True)
   else:tmp=STATE.with_suffix('.rollback');tmp.write_bytes(before);tmp.replace(STATE)
   raise
  _profiles=updated
  diagnostic()
  prune_generations(meta['generation'],json.loads(before).get('generation')if before else None)
  return {'saved':True,'card_id':pid,'generation':meta['generation']}

def advertise(value,port):
 if not isinstance(value,dict)or not isinstance(value.get('livedata_list'),list)or not isinstance(value.get('version_file'),str):return value
 if not _profiles:
  ver=json.loads(value['version_file']);prior=ver.get('dt880',[]);filtered=[x for x in prior if not isinstance(x,dict)or x.get('name')!='pc9311'];names={'pc9311_mobile_and.'+ext for ext in ['pak','utoc','ucas']};files=[x for x in value['livedata_list']if not isinstance(x,dict)or x.get('name')not in names]
  if prior==filtered and files==value['livedata_list']:return value
  ver['dt880']=filtered;ver['version']+=716;return dict(value,version_file=json.dumps(ver,separators=(',',':')),livedata_list=files)
 from mod_integrity import digest
 d=json.loads(STATE.read_text());r={ext:d['files']['pc9311_mobile_and.'+ext]for ext in ['pak','utoc','ucas']}
 for row in r.values():
  p=(LIVE.parent/row['relative']).resolve()
  if not p.is_relative_to(LIVE.resolve())or p.stat().st_size!=row['size']or digest(p)!=row['sha256']:raise ValueError('Custom photo payload mismatch')
 ver=json.loads(value['version_file']);item={'name':'pc9311','hash':r['pak']['sha256'],'hashFileSize':r['pak']['size'],'ucas':r['ucas']['sha256'],'ucasFileSize':r['ucas']['size'],'utoc':r['utoc']['sha256'],'utocFileSize':r['utoc']['size']}
 if not any(x==item for x in ver['dt880']):ver['version']+=712+int(d.get('revision',1))
 ver['dt880']=[x for x in ver['dt880']if x.get('name')!='pc9311']+[item];out=dict(value);names={'pc9311_mobile_and.'+x for x in r};out['livedata_list']=[x for x in value['livedata_list']if x.get('name')not in names]+[{'name':'pc9311_mobile_and.'+ext,'size':row['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+row['relative']}for ext,row in r.items()];out['version_file']=json.dumps(ver,separators=(',',':'));diagnostic(True);return out

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
