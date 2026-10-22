from pathlib import Path
import ast,hashlib,json
r=Path(__file__).parent;old=Path('/workspace/analysis/my-league/hotfix-v18/select_team_runtime.py').read_text();tree=ast.parse(old)
helper=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['branch','jump','maps','digest','install']:
  text=ast.get_source_segment(old,node)
  if node.name=='install':
   text=text.replace("'libselect_team.so'","'libnoodle_hair.so'").replace("    hook.status.argtypes = [C.c_uint]\n    hook.status.restype = C.c_uint\n",'')
  helper.append(text)
prefix='''"""Experimental exact-card noodle hair; engine calls occur only in native callbacks."""
import ctypes as C
import hashlib,json,os,platform,threading,time
from pathlib import Path
ENGINE_SHA='3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98'
HOOK_SHA='''+repr(hashlib.sha256((r/'libnoodle_hair.so').read_bytes()).hexdigest())+'''
GETTER=0x39cdb10
PROLOGUE=bytes.fromhex('ff4307d1fd7b17a9fcc300f9fa6719a9')
HERE=Path(__file__).resolve().parent
_keep=[]
_digest_cache={}
_started=False
_advertised=0
_handle=None
_payload_ok=False
_state='STARTING'
_error=None
'''
(r/'noodle_hair.py').write_text(prefix+'\n\n'.join(helper)+'\n\n'+(r/'runtime_tail.py').read_text())
