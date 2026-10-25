from pathlib import Path
import sys,types,threading,importlib,ctypes as ctypes0,json
P=Path('/workspace/ronaldo-work/73-ui6');sys.path.insert(0,str(P/'payload/work/tools'));checks=[]
class StopLoop(BaseException):pass
class Fn:
 def __init__(self,value=0):self.value=value;self.calls=[]
 def __call__(self,*args):self.calls.append(args);return self.value
class Hook:
 def __init__(self):self.fns={}
 def __getattr__(self,n):return self.fns.setdefault(n,Fn(1 if n=="configure_owned_cards"else 0))
for name in['noodle_hair','select_team_runtime']:
 m=importlib.import_module(name);hook=Hook();entries=[];reports=[]
 m.maps=lambda:[(0x1000,0x2000,'r-xp',0,'/fake/libUE4.so')];m.preflight=lambda *a:None;m.bundle=lambda:{}
 m.platform=types.SimpleNamespace(machine=lambda:'aarch64');m.C=types.SimpleNamespace(**{n:getattr(ctypes0,n)for n in['c_uint','c_uint32','c_uint64','c_size_t','c_void_p','POINTER','sizeof']},CDLL=lambda path:hook,cast=lambda *a:types.SimpleNamespace(value=0x4000))
 m.install=lambda *a,**kw:(entries.append(kw.get('entry',m.GETTER))or hook)
 m.time=types.SimpleNamespace(sleep=lambda n:(_ for _ in()).throw(StopLoop()))
 m.report=lambda:reports.append(m._state) if name=='noodle_hair'else None
 m.diagnostic=lambda state,**kw:reports.append((state,kw))
 if name=='select_team_runtime':
  # The real editor is tested by the native suite; startup exercises ctypes
  # wiring and catches missing locals after the obsolete hooks were removed.
  real=sys.modules.get('myleague_editor_runtime');sys.modules['myleague_editor_runtime']=types.SimpleNamespace(install_native=lambda h:None,config=lambda:{'teams':[]})
  m.activate_context(473)
 try:m._worker_once()
 except StopLoop:pass
 assert m._ready.is_set(),(name,reports)
 if name=='select_team_runtime':
  assert hook.activate_context.calls==[(473,)]
  assert not({0x39ce7d8,0x39cefe4,0x823cb04,0x8294a7c}&set(entries));sys.modules['myleague_editor_runtime']=real
 checks.append(name+': actual worker setup reaches READY; required names and ctypes wiring valid')
 # Remaining in an editor longer than the old300-iteration limit must not
 # consume the only native-init attempt. Simulate700seconds without sleeping.
 count=[0];m._ready.clear()
 def delayed_maps():
  count[0]+=1
  return []if count[0]<=350 else[(0x1000,0x2000,'r-xp',0,'/fake/libUE4.so')]
 m.maps=delayed_maps
 def delayed_sleep(n):
  if n==10:raise StopLoop()
 m.time=types.SimpleNamespace(sleep=delayed_sleep)
 if name=='select_team_runtime':sys.modules['myleague_editor_runtime']=types.SimpleNamespace(install_native=lambda h:None,config=lambda:{'teams':[]})
 try:m._worker_once()
 except StopLoop:pass
 assert m._ready.is_set()and count[0]==351,(name,count,reports)
 if name=='select_team_runtime':sys.modules['myleague_editor_runtime']=real
 checks.append(name+': still initializes after350 pre-game polls; no old five-minute expiry')

 # Exercise retry control without patching another process's memory.
 attempts=[];m._ready.clear()
 def attempt():
  attempts.append(1)
  if len(attempts)==3:m._ready.set()
 m._worker_once=attempt;m.time=types.SimpleNamespace(sleep=lambda n:None);m.worker();assert len(attempts)==3
 checks.append(name+': partial failures retry; third successful attempt completes')
# Reload untouched installer functions and prove own branches are recognized;
# another branch cannot be accepted as an installed mod.
for name in['noodle_hair','select_team_runtime']:
 m=importlib.reload(sys.modules[name]);entry=0x1200;cave=0x2000;prologue=b'abcdefghijklmnop';hook=Hook();m._installed_hooks[(0,entry)]=(entry,cave,hook)
 memory={entry:m.branch(entry,cave).to_bytes(4,'little'),entry+4:prologue[4:]}
 m.C=types.SimpleNamespace(string_at=lambda addr,n:memory[addr][:n]);m.digest=lambda path:m.ENGINE_SHA if str(path)=='engine'else m.HOOK_SHA
 assert m.install(0,'engine',entry=entry,prologue=prologue)is hook
 memory[entry]=b'\0'*4
 try:m.install(0,'engine',entry=entry,prologue=prologue);raise AssertionError('foreign branch accepted')
 except RuntimeError:pass
 checks.append(name+': existing own hook idempotent; foreign mutation rejected')
# The login guard must wait, and must recheck after a previously ready runtime fails.
import mod_startup as guard
face=sys.modules['noodle_hair'];native=sys.modules['select_team_runtime'];face._ready.set();native._ready.set();calls=[]
face.wait_ready=lambda timeout:calls.append('face');native.wait_ready=lambda timeout:calls.append('native');guard.platform=types.SimpleNamespace(machine=lambda:'aarch64');guard._python_ready=True;guard.require_ready();assert calls==['face','native'];guard.require_ready();assert len(calls)==2
native._ready.clear()
def fail(timeout):raise RuntimeError('deliberate initialization failure')
native.wait_ready=fail
try:guard.require_ready();raise AssertionError('silent original fallback')
except RuntimeError:pass
guard._python_ready=False
try:guard.require_ready();raise AssertionError('Python adapter silently bypassed')
except RuntimeError:pass
checks.append('Login readiness guard blocks missing patches, fast path is rechecked after failure')
(P/'startup-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'device_tested':False},indent=2));print('STARTUP_PASS',len(checks))
