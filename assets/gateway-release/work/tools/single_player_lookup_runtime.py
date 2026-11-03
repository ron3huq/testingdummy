"""Resolve a configured full card ID to the live owned serial in its own XI."""
from pathlib import Path
import ctypes as C
from mod_integrity import digest
from select_team_runtime import maps,branch
HERE=Path(__file__).parent
ENGINE_SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
HOOK_SHA='efd0bfb467290ae4e607e690317446b31af355da8c876e93ddb4d2996ade725a'
ENTRY=0x72f2de0
PROLOGUE=bytes.fromhex('fd7bbea9f30b00f9fd030091f30300aa')
_installed_hooks={};_keep=[];_helper=None
def owned_entry(base,entry,expected):
 item=_installed_hooks.get((base,entry))
 if item is None:return False
 target,cave,_=item
 import struct
 return C.string_at(target,4)==struct.pack('<I',branch(target,cave))and C.string_at(target+4,len(expected)-4)==expected[4:]
def install(base,path,single):
 global _helper
 # These offsets match the pinned layout; the manual variant changes only its AI gate.
 import single_player_runtime as runtime,hook_arena
 if digest(HERE/'libsingle_player.so')!=runtime.HOOK_SHA:raise RuntimeError('Single-player module changed')
 hook_arena.PLANS[ENTRY]=PROLOGUE.hex()
 helper=hook_arena.install(globals(),base,path,ENTRY,PROLOGUE,'single_lookup_hook','configure_single_lookup')
 single_base=C.cast(single.single_update,C.c_void_p).value-0x10ca4
 helper.single_lookup_caller.argtypes=[C.c_size_t,C.c_size_t];helper.single_lookup_caller.restype=None
 helper.single_lookup_caller(single_base+0x10aec,single_base+0x12b00)
 _helper=helper
 return helper

def status():
 if _helper is None:return {"ready":False}
 _helper.single_lookup_status.argtypes=[];_helper.single_lookup_status.restype=C.c_uint64
 return {"ready":True,"live_key_resolutions":int(_helper.single_lookup_status())}
