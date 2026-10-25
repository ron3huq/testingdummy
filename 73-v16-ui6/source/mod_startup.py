"""Require verified runtime patches before login and match preparation."""
import functools,json,platform,threading,time
from pathlib import Path
_lock=threading.Lock();_verified=False;_python_ready=False

def require_ready():
 global _verified
 if platform.machine().lower()not in('aarch64','arm64'):return
 if not _python_ready:raise RuntimeError('Mod Python adapter is not initialized; original fallback is blocked.')
 import noodle_hair,select_team_runtime
 if _verified and noodle_hair._ready.is_set()and select_team_runtime._ready.is_set():return
 if platform.machine().lower()not in('aarch64','arm64'):return
 with _lock:
  if _verified and noodle_hair._ready.is_set()and select_team_runtime._ready.is_set():return
  import noodle_hair,select_team_runtime
  try:
   noodle_hair.wait_ready(15);select_team_runtime.wait_ready(15)
   _verified=True;status={'state':'READY','version':'73-ui6','original_fallback':False}
  except Exception as exc:
   status={'state':'BLOCKED_MOD_NOT_READY','version':'73-ui6','error':str(exc),'original_fallback':False}
   Path(__file__).with_name('mod-startup-status.json').write_text(json.dumps(status,indent=2))
   raise
  Path(__file__).with_name('mod-startup-status.json').write_text(json.dumps(status,indent=2))

def install():
 import gate_logic
 original=gate_logic.GateLogic.handle
 if getattr(original,'_ui6_guard',False):return False
 @functools.wraps(original)
 def handle(self,mid,req):
  if mid in('CMD_LOGIN','CMD_START_GAME','CMD_GET_VSCOM_OPPONENT'):require_ready()
  return original(self,mid,req)
 handle._ui6_guard=True;gate_logic.GateLogic.handle=handle;return True
