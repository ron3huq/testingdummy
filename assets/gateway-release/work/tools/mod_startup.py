"""Require verified runtime patches before login and match preparation."""
import functools,json,platform,threading,time,traceback
from pathlib import Path
_lock=threading.Lock();_verified=False;_python_ready=False

_error_lock=threading.RLock()
def record_error(stage,error):
 """Keep the last failure across relaunches; never include save/player data."""
 try:
  with _error_lock:
   tools=Path(__file__).parent
   report={'version':'73-ui7.13','time_unix':time.time(),'stage':stage,'error':str(error),'traceback':traceback.format_exc()}
   for name in ['mod-startup-status.json','select-team-status.json','noodle-hair-status.json']:
    try:report[name]=json.loads((tools/name).read_text())
    except Exception:pass
   temp=tools/'mod-last-error.tmp';temp.write_text(json.dumps(report,indent=2));temp.replace(tools/'mod-last-error.json')
 except Exception:pass

_requests=[]
def record_request(path,state,elapsed=0):
 # Sixty-four startup requests maximum; no ongoing logging in matches or editors.
 try:
  with _error_lock:
   if state=='begin':
    if len(_requests)>=64:return
    _requests.append({'path':str(path).split('?',1)[0][:100],'time_unix':time.time(),'state':state})
   elif _requests:
    _requests[-1].update(state=state,elapsed_ms=round(elapsed*1000,1))
   tools=Path(__file__).parent;temp=tools/'ui71-gateway-startup.tmp';temp.write_text(json.dumps(_requests,indent=2));temp.replace(tools/'ui71-gateway-startup.json')
 except Exception:pass

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
   _verified=True;status={'state':'READY','version':'73-ui7.13','original_fallback':False}
  except Exception as exc:
   record_error('login-readiness',exc)
   status={'state':'BLOCKED_MOD_NOT_READY','version':'73-ui7.13','error':str(exc),'original_fallback':False}
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
