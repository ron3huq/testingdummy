from pathlib import Path
import sys,json,types,hashlib,importlib.util
from elftools.elf.elffile import ELFFile
p=Path('/workspace/ronaldo-work/73-ui4');tools=p/'payload/work/tools';sys.path.insert(0,str(tools));import rolled_runtime,select_team_runtime as runtime
meta=rolled_runtime.verified();assert len(meta['files'])==3
value={'version_file':json.dumps({'version':100,'dt880':[{'name':'pc9298','x':1}]}),'livedata_list':[{'name':'pc9298_mobile_and.pak','size':9,'url':'retained'}]}
a=rolled_runtime.advertise(value,8085);b=rolled_runtime.advertise(a,8085);assert a==b and json.loads(a['version_file'])['version']==119
assert a['livedata_list'][0]==value['livedata_list'][0];assert len(a['livedata_list'])==4;assert rolled_runtime.advertise({'not':'game'},8085)=={'not':'game'}
assert value['livedata_list']==[{'name':'pc9298_mobile_and.pak','size':9,'url':'retained'}]
f=open('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so','rb');elf=ELFFile(f);segments=list(elf.iter_segments())
def read(addr,n):
 for s in segments:
  if s['p_type']=='PT_LOAD'and s['p_vaddr']<=addr<s['p_vaddr']+s['p_filesz']:f.seek(s['p_offset']+addr-s['p_vaddr']);return f.read(n)
 raise AssertionError(hex(addr))
runtime.C=types.SimpleNamespace(string_at=read);runtime.preflight(0,f.name)
entries=json.loads((p/'hook-entries.json').read_text());assert len(entries)==28
runtime.C.string_at=lambda addr,n:b'\0'*n if addr==0x39cefe4 else read(addr,n)
try:runtime.preflight(0,f.name);raise AssertionError('conflict accepted')
except RuntimeError:pass
face={0x3883248,0x38809bc,0x330ae54,0x39c0420,0x39bc570,0x39bc5ac,0x823be04,0x82a1e48,0x3a908a0,0x39cb75c,0x45b58b0,0x39d3604,0x39d3e1c,0x39cd71c,0x39cdb10};assert not face&{e[0]for e in entries}
assert runtime.HOOK_SHA==hashlib.sha256((tools/'libselect_team.so').read_bytes()).hexdigest()
import extras_runtime
c=extras_runtime.advertise(a,8085);assert extras_runtime.advertise(c,8085)==c;assert len(c['livedata_list'])==7;assert json.loads(c['version_file'])['version']==140
(p/'runtime-validation.json').write_text(json.dumps({'passed':True,'checks':['pc9299 payload verifies once; advertisement idempotent; face rows and source reply retained','28 hook prologues match original73 engine; added-helper conflict caught before patching','no overlap with fifteen working face hooks','runtime native SHA matches compiled library']},indent=2));print('RUNTIME_PASS')
