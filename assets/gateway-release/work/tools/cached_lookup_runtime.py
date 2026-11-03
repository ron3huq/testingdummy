"""Pin and connect the cached-index bridge to the existing player detour."""
from pathlib import Path
import ctypes as C
HERE=Path(__file__).parent
SHA='efd0bfb467290ae4e607e690317446b31af355da8c876e93ddb4d2996ade725a'
_handle=None
def install(runtime,hook,base):
 global _handle
 if _handle is not None:return
 from mod_integrity import digest
 path=HERE/'libcached_lookup.so'
 if digest(path)!=SHA:raise RuntimeError('Cached lookup bridge checksum mismatch')
 target,cave,_=runtime['_installed_hooks'][(base,0x823c8d4)]
 if not runtime['owned_entry'](base,0x823c8d4,bytes.fromhex('ff0301d1fd7b02a9f44f03a9fd830091')):raise RuntimeError('Cached lookup player detour changed')
 helper=C.CDLL(str(path));helper.cached_lookup_configure.argtypes=[C.c_size_t]*3;helper.cached_lookup_configure.restype=C.c_uint
 if helper.cached_lookup_configure(base,cave+32,C.cast(hook.player_hook,C.c_void_p).value)!=1:raise RuntimeError('Cached lookup configuration rejected')
 hook.configure_player.argtypes=[C.c_size_t,C.c_size_t];hook.configure_player.restype=None
 hook.configure_player(base,C.cast(helper.cached_lookup_original,C.c_void_p).value)
 import hook_arena
 with hook_arena._LOCK:
  arena=next(p for p in hook_arena._ARENAS[base]if p.address<=cave<p.address+p.span)
  arena.bind(0x823c8d4,C.cast(helper.cached_lookup_player,C.c_void_p).value)
 runtime['_keep'].append(helper);_handle=helper

def status():
 if _handle is None:return {"ready":False}
 _handle.cached_lookup_status.argtypes=[C.c_uint];_handle.cached_lookup_status.restype=C.c_uint64
 return dict(ready=True,**{name:int(_handle.cached_lookup_status(i))for i,name in enumerate(["hits","searches","canonicalized","rejected"])})
