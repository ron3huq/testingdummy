# Keep the original encrypted73 gateway; never mask a failed mod bootstrap.
import _protected_runtime
_protected_runtime.exec_into(__name__, globals())
_v25_original_initialize=initialize

def initialize(root,installed_version=None):
 result=_v25_original_initialize(root,installed_version)
 try:
  import importlib.util,sys
  from pathlib import Path
  tools=Path(root)/'work/tools';name='_v25_bridge_73';bridge=sys.modules.get(name)
  if bridge is None:
   spec=importlib.util.spec_from_file_location(name,tools/'bridge_73.py');bridge=importlib.util.module_from_spec(spec);sys.modules[name]=bridge;spec.loader.exec_module(bridge)
  bridge.install(root,sys.modules[__name__])
 except Exception as exc:
  try:
   import mod_startup
   mod_startup.record_error('python-bootstrap',exc)
   (Path(root)/'work/tools/v25-73-bootstrap-error.txt').write_text(str(exc))
  except Exception:pass
  raise RuntimeError('Mod startup failed. Open Runtime Diagnostics: '+str(exc))from exc
 return result

_v25_original_handle=handle
_request_count=0
def _startup_note(path,state,elapsed=0):
 try:
  import mod_startup
  mod_startup.record_request(path,state,elapsed)
 except Exception:pass

def handle(path,body):
 global _request_count
 import time
 started=time.monotonic();tracked=_request_count<8;_request_count+=1
 try:
  if tracked:_startup_note(path,'begin')
  value=_v25_original_handle(path,body)
  if tracked:_startup_note(path,'ok',time.monotonic()-started)
  return value
 except Exception as exc:
  try:
   import mod_startup
   mod_startup.record_error('gateway-request:'+str(path).split('?',1)[0][:100],exc)
   if tracked:_startup_note(path,'error',time.monotonic()-started)
  except Exception:pass
  raise
