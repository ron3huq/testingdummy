"""Exact Transfer player overrides, after native classic/world/rating layers.
Observed player records stay private on-device; diagnostics expose counters only.
"""
from pathlib import Path
import ctypes as C,json,hashlib,os,time
HERE=Path(__file__).parent
HOOK_SHA='6d21e71ee21b113512268ebf1a1ceb477c9e23bc2628c740c41971e3f7f5dc21'
_handle=None;_keep=[];_last_generation=0;_last_write=0
OBSERVED=HERE/'transfer-native-observed.private.json'
class Observed(C.Structure):_fields_=[('id',C.c_uint64),('cid',C.c_uint32),('stamp',C.c_uint32),('values',C.c_uint16*147),('pad',C.c_uint16)]
def install(base,previous,editor):
 global _handle
 if _handle is not None:return
 import hook_arena,transfer_player_editor as players,myleague_editor_runtime as config
 from mod_integrity import digest
 path=HERE/'libtransfer_final.so'
 if digest(path)!=HOOK_SHA:raise RuntimeError('Final Transfer bridge checksum mismatch')
 h=C.CDLL(str(path));h.final_bind.argtypes=[C.c_size_t]*3;h.final_bind.restype=C.c_uint
 h.final_add.argtypes=[C.c_uint64,C.c_uint];h.final_add.restype=C.c_uint
 h.final_parameter.argtypes=[C.c_uint]*3;h.final_parameter.restype=C.c_uint
 h.final_commit.argtypes=[];h.final_commit.restype=None
 h.final_status.argtypes=[C.c_uint];h.final_status.restype=C.c_uint64
 h.final_copy_observed.argtypes=[C.c_void_p,C.c_uint];h.final_copy_observed.restype=C.c_uint
 if h.final_bind(base,C.cast(previous.tactics_player_hook,C.c_void_p).value,C.cast(editor.environment_status,C.c_void_p).value)!=1:raise RuntimeError('Final Transfer binding rejected')
 for key,v in players._profiles.items():
  cid,pid=key.split(':');players.validate(v);row=h.final_add(int(pid),int(cid))
  if not row:raise ValueError('Final Transfer exact-ID scope rejected')
  fields=players.runtime_fields(pid,int(cid),v)
  for field,value in fields.items():
   if h.final_parameter(row,int(field),value)!=1:raise ValueError('Final Transfer field rejected: '+field)
 h.final_commit()
 # Three callbacks in the declared extra ELF segments; existing exports/state stay intact.
 editor_base=C.cast(editor.editor_apply_player,C.c_void_p).value-0x33ca8
 configure=C.CFUNCTYPE(None,C.c_size_t,C.c_size_t,C.c_size_t)(editor_base+0x10c1000)
 configure(C.cast(h.final_before_record,C.c_void_p).value,C.cast(h.final_after_record,C.c_void_p).value,C.cast(h.final_skip_balance,C.c_void_p).value)
 _keep.append(configure)
 with hook_arena._LOCK:
  pool=next(p for p in hook_arena._ARENAS[base]if 0x823c8d4 in p.index)
  pool.bind(0x823c8d4,C.cast(h.final_player,C.c_void_p).value)
 _handle=h;_keep.extend([h,previous,editor])
def status():
 global _last_generation,_last_write
 h=_handle
 if h is None:return {'ready':False}
 names=['ready','profiles','lookup_calls','applies','restores','rejected','last_player_id','last_competition','observed_records','observed_generation','balance_skips','verified_fields','mismatched_fields','padded_keys'];out={name:int(h.final_status(i))for i,name in enumerate(names)}
 generation=out['observed_generation']
 if generation!=_last_generation and time.monotonic()-_last_write>=1:
  rows=(Observed*512)();n=h.final_copy_observed(C.byref(rows),C.sizeof(rows))
  if n<=512:
   try:doc=json.loads(OBSERVED.read_text())
   except(OSError,ValueError):doc={'schema':1,'records':{}}
   if doc.get('schema')!=1 or not isinstance(doc.get('records'),dict):doc={'schema':1,'records':{}}
   for r in list(rows)[:n]:doc['records'][str(r.cid)+':'+str(r.id)]={'parameters':list(r.values),'pid':os.getpid(),'observed_unix':int(time.time())}
   if len(doc['records'])>4096:doc['records']=dict(list(doc['records'].items())[-4096:])
   tmp=OBSERVED.with_suffix('.tmp');tmp.write_text(json.dumps(doc,separators=(',',':')));tmp.replace(OBSERVED);_last_generation=generation;_last_write=time.monotonic()
 return out
