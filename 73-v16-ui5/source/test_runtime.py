from pathlib import Path
import sys,json,types,hashlib,re,ast
from elftools.elf.elffile import ELFFile
P=Path('/workspace/ronaldo-work/73-ui5');tools=P/'payload/work/tools';sys.path.insert(0,str(tools));import rolled_runtime,extras_runtime,manager_runtime,select_team_runtime as runtime
value={'version_file':json.dumps({'version':100,'dt880':[{'name':'pc9298','x':1}]}),'livedata_list':[{'name':'pc9298_mobile_and.pak','size':9,'url':'retained'}]};out=value
for module in[rolled_runtime,extras_runtime,manager_runtime]:
 out=module.advertise(out,8085);assert module.advertise(out,8085)==out
assert json.loads(out['version_file'])['version']==216 and len(out['livedata_list'])==10;assert out['livedata_list'][0]==value['livedata_list'][0]
f=open('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so','rb');elf=ELFFile(f);segments=list(elf.iter_segments())
def read(addr,n):
 for s in segments:
  if s['p_type']=='PT_LOAD'and s['p_vaddr']<=addr<s['p_vaddr']+s['p_filesz']:f.seek(s['p_offset']+addr-s['p_vaddr']);return f.read(n)
 raise AssertionError(hex(addr))
runtime.C=types.SimpleNamespace(string_at=read);runtime.preflight(0,f.name)
s=(tools/'select_team_runtime.py').read_text();entries=ast.literal_eval(re.search(r'for entry,expected in (\[.*?\]):',s).group(1));assert len(entries)==25
extra=re.findall(r'entry=(0x[0-9a-f]+),prologue=bytes.fromhex\(\x27([0-9a-f]+)\x27\)',s)
for addr,expected in extra:assert read(int(addr,16),16)==bytes.fromhex(expected),(addr,expected)
runtime.C.string_at=lambda addr,n:b'\0'*n if addr==0x39cefe4 else read(addr,n)
try:runtime.preflight(0,f.name);raise AssertionError('conflict accepted')
except RuntimeError:pass
assert runtime.HOOK_SHA==hashlib.sha256((tools/'libselect_team.so').read_bytes()).hexdigest()
(P/'runtime-validation.json').write_text(json.dumps({'passed':True,'mandatory_hook_prologues':len(entries),'inline_hook_prologues_checked':len(extra),'resource_containers_idempotent':3,'original_face_advertisement_preserved':True,'native_SHA_verified':True,'android_device_tested':False},indent=2));print('RUNTIME_PASS',len(entries),len(extra))
