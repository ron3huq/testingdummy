"""Route direct cached GamePlan consumers through the scoped native editor."""
from pathlib import Path
import ctypes as C,struct
from mod_integrity import digest
from select_team_runtime import maps,branch
HERE=Path(__file__).parent
ENGINE_SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
HOOK_SHA='a10411ad99a77f733db3a3794d08f35f216d6f9f902575feb33005958d07fe74'
HOOKS=((0x8294a5c,bytes.fromhex('280040b9093a82520a3180520900098b'),'cached_plan_index','configure_cached_plan_index'),(0x8294a7c,bytes.fromhex('ff4301d1fd7b02a9f65703a9f44f04a9'),'cached_plan_find','configure_cached_plan_find'))
_installed_hooks={};_keep=[];_helper=None
def owned_entry(base,entry,expected):
 item=_installed_hooks.get((base,entry))
 if item is None:return False
 target,cave,_=item
 return C.string_at(target,4)==struct.pack('<I',branch(target,cave))and C.string_at(target+4,len(expected)-4)==expected[4:]
def install(base,path,editor):
 global _helper
 if _helper is not None:return
 import hook_arena
 p=HERE/'libtactics_bridge.so'
 if digest(p)!=HOOK_SHA:raise RuntimeError('Cached GamePlan bridge checksum mismatch')
 h=C.CDLL(str(p));h.cached_plan_bind.argtypes=[C.c_size_t]*2;h.cached_plan_bind.restype=None
 h.cached_plan_bind(C.cast(editor.editor_tactics_hook,C.c_void_p).value,C.cast(editor.cached_team_hook,C.c_void_p).value)
 for entry,prologue,name,configure in HOOKS:
  hook_arena.PLANS[entry]=prologue.hex()
  hook_arena.install(globals(),base,path,entry,prologue,name,configure)
 import cached_lookup_runtime,select_team_runtime
 previous=cached_lookup_runtime._handle
 if previous is None:raise RuntimeError('Player identity bridge is not initialized')
 h.tactics_player_bind.argtypes=[C.c_size_t]*3;h.tactics_player_bind.restype=None
 h.tactics_player_bind(base,C.cast(previous.cached_lookup_player,C.c_void_p).value,C.cast(editor.environment_status,C.c_void_p).value)
 target,cave,_=select_team_runtime._installed_hooks[(base,0x823c8d4)]
 with hook_arena._LOCK:
  arena=next(a for a in hook_arena._ARENAS[base]if a.address<=cave<a.address+a.span)
  arena.bind(0x823c8d4,C.cast(h.tactics_player_hook,C.c_void_p).value)
 select_team_runtime._keep.append(h)
 _helper=h

def configure_boosters():
 import myleague_editor_runtime as editor
 h=_helper
 if h is None:raise RuntimeError('Native Transfer trait bridge is not initialized')
 h.transfer_booster_add.argtypes=[C.c_size_t,C.c_uint,C.c_uint,C.c_uint,C.c_uint];h.transfer_booster_add.restype=C.c_uint
 h.transfer_booster_commit.argtypes=[];h.transfer_booster_commit.restype=None
 for row in editor.requested_long_sleeves(editor.config())['players']:
  if 'boosters'in row and h.transfer_booster_add(int(row['id']),row['competition'],*row['boosters'])!=1:raise ValueError('Native Transfer boosters rejected')
 h.transfer_booster_commit()

def status():
 if _helper is None:return {'ready':False}
 _helper.cached_plan_status.argtypes=[C.c_uint];_helper.cached_plan_status.restype=C.c_size_t
 return dict(ready=True,**{n:int(_helper.cached_plan_status(i))for i,n in enumerate(['index_calls','find_calls','edited_plans','layout_rejections','booster_applies'])})
