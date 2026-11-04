"""Run the unchanged LOGIN readiness guard with real asset checks and mocked ARM workers.
No real account/save is read. Status output stays in a temporary test directory.
"""
from pathlib import Path
import sys,types,tempfile,threading

def run(root):
 t=Path(root)/'assets/gateway-release/work/tools';sys.path.insert(0,str(t))
 import noodle_hair,private_bundles,mod_integrity
 saved_modules={k:sys.modules.get(k)for k in ['gate_logic','select_team_runtime','myleague_condition','single_player_runtime']}
 import platform
 original_machine=platform.machine;old_wait=noodle_hair.wait_ready;original_ready=noodle_hair._ready.is_set();data=(t/'private_bundles.json').read_bytes();original_calls=[]
 def checks(timeout=15):
  mod_integrity._cache.clear();private_bundles.verified.cache_clear();noodle_hair.bundle();private_bundles.verified();noodle_hair._ready.set();return True
 class GateLogic:
  def handle(self,mid,req):original_calls.append(mid);return {'original_handler_reached':True,'mid':mid}
 try:
  platform.machine=lambda:'aarch64';noodle_hair.wait_ready=checks;noodle_hair._ready.clear()
  sys.modules['gate_logic']=types.SimpleNamespace(GateLogic=GateLogic)
  sys.modules['select_team_runtime']=types.SimpleNamespace(_ready=threading.Event(),wait_ready=lambda timeout:True);sys.modules['select_team_runtime']._ready.set()
  for name in ['myleague_condition','single_player_runtime']:sys.modules[name]=types.SimpleNamespace(ready=lambda:True,require_ready=lambda timeout:True)
  with tempfile.TemporaryDirectory()as td:
   guard=types.ModuleType('guard_test');guard.__file__=str(Path(td)/'mod_startup.py');exec(compile((t/'mod_startup.py').read_text(),str(t/'mod_startup.py'),'exec'),guard.__dict__);guard._python_ready=True;guard.record_error=lambda *args:None;guard.install()
   # Deliberately corrupt a dependency: do not update any expected checksum.
   (t/'private_bundles.json').write_bytes(data+b' ')
   try:GateLogic().handle('CMD_LOGIN',{});raise AssertionError('corruption passed LOGIN guard')
   except ValueError as error:assert 'checksum mismatch: private_bundles.json'in str(error)
   assert not original_calls
   (t/'private_bundles.json').write_bytes(data)
   response=GateLogic().handle('CMD_LOGIN',{});assert response['original_handler_reached']and original_calls==['CMD_LOGIN']
  return dict(actual_login_guard_executed=True,corrupt_nested_dependency_blocks_login=True,valid_dependency_chain_reaches_original_login_handler=True,ARM_workers_mocked=True,real_phone_login_verified=False)
 finally:
  (t/'private_bundles.json').write_bytes(data);noodle_hair.wait_ready=old_wait
  if original_ready:noodle_hair._ready.set()
  else:noodle_hair._ready.clear()
  platform.machine=original_machine;mod_integrity._cache.clear();private_bundles.verified.cache_clear()
  for name,module in saved_modules.items():
   if module is None:sys.modules.pop(name,None)
   else:sys.modules[name]=module
