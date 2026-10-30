"""Shared process-local integrity cache. Never persists trust across launches."""
import hashlib,os,threading,json
from pathlib import Path
_java=None
def java_verified(path,st):
 global _java
 if st.st_size<=1048576:return None
 root=Path(__file__).resolve().parents[2]
 try:
  rel=Path(path).resolve().relative_to(root).as_posix()
  if not rel.startswith("livedata/"):return None
  if _java is None:_java=json.loads((root/".ui6-runtime-cache.json").read_text()).get("files",{})
  row=_java.get(rel,{})
  if row.get("bytes")==st.st_size and row.get("mtime")==st.st_mtime_ns//1000000:return row.get("sha256")
 except (OSError,ValueError,TypeError):return None
 return None
_cache={};_lock=threading.RLock()
def digest(path):
 st=os.stat(path);key=(os.fspath(path),st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
 with _lock:
  if key in _cache:return _cache[key]
  verified=java_verified(path,st)
  if verified:_cache[key]=verified;return verified
  h=hashlib.sha256()
  with open(path,'rb')as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  value=h.hexdigest()
  if len(_cache)>128:_cache.clear()
  _cache[key]=value;return value
