import pathlib,importlib.util,types,sys,json,zipfile,marshal,hashlib,tempfile,ctypes
from elftools.elf.elffile import ELFFile
BASE=pathlib.Path('/workspace/ronaldo-work/73-v25-port');PKG=BASE/'package';checks=[]
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('v25_73_validate',PKG/'payload/work/tools/noodle_hair.py');meta=m.bundle();assert meta['base_package']=='com.efootball.revival.local';checks.append('all_payload_hashes_and_native_hash_verified')
engine=pathlib.Path('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so');assert hashlib.sha256(engine.read_bytes()).hexdigest()==m.ENGINE_SHA
with engine.open('rb') as f:
 elf=ELFFile(f);segs=list(elf.iter_segments());raw=engine.read_bytes()
 def at(addr,n):
  for s in segs:
   if s['p_type']=='PT_LOAD' and s['p_vaddr']<=addr<s['p_vaddr']+s['p_filesz']:
    off=s['p_offset']+addr-s['p_vaddr'];return raw[off:off+n]
  raise AssertionError(hex(addr))
m.C=types.SimpleNamespace(string_at=at);m.preflight(0,engine);checks.append('all_15_hook_prologues_match_real_73_engine')
old=m.digest;m.digest=lambda p:'wrong'
try:m.preflight(0,engine);raise AssertionError('wrong engine accepted')
except RuntimeError:checks.append('wrong_engine_rejected')
m.digest=old;good=at;m.C.string_at=lambda a,n:b'\0'*n if a==0x39cdb10 else good(a,n)
try:m.preflight(0,engine);raise AssertionError('late conflict accepted')
except RuntimeError:checks.append('last_entry_conflict_rejected_before_any_install')
# Check wrappers without executing any protected game business code.
protected=types.ModuleType('_protected_runtime');calls=[]
def populate(name,g):
 g['initialize']=lambda root,installed_version=None:('original',root,installed_version)
 g['_local_urls']=lambda value:dict(value,original_73_preserved=True)
protected.exec_into=populate
oldprotected=sys.modules.get('_protected_runtime');oldnoodle=sys.modules.get('noodle_hair')
sys.modules['_protected_runtime']=protected
fake=types.ModuleType('noodle_hair');fake.start=lambda:calls.append('start');fake.advertise=lambda v,p:dict(v,port=p)
sys.modules['noodle_hair']=fake
mod=types.ModuleType('_test_73_gateway');sys.modules[mod.__name__]=mod
with zipfile.ZipFile(PKG/'app-v25.imy') as z:
 code=marshal.loads(z.read('embedded_gateway.pyc')[16:]);exec(code,mod.__dict__)
 result=mod.initialize(str(PKG/'payload'),123)
 assert result==('original',str(PKG/'payload'),123);assert calls==['start'];assert mod._local_urls({'x':1})=={'x':1,'original_73_preserved':True,'port':8085}
 first=mod._local_urls;mod.initialize(str(PKG/'payload'),123);assert mod._local_urls is first
checks+=['original_initialize_result_retained','73_local_url_conversion_retained','bridge_starts_native_worker','bridge_wrapper_idempotent']
with zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy') as a,zipfile.ZipFile(PKG/'app-v25.imy') as b:
 assert set(a.namelist())==set(b.namelist());changed=[n for n in a.namelist() if a.read(n)!=b.read(n)];assert changed==['embedded_gateway.pyc']
checks.append('all_original_encrypted_python_modules_byte_exact')
if oldprotected is None:sys.modules.pop('_protected_runtime',None)
else:sys.modules['_protected_runtime']=oldprotected
if oldnoodle is None:sys.modules.pop('noodle_hair',None)
else:sys.modules['noodle_hair']=oldnoodle
r={'checks':checks,'passed':True,'phone_tested':False,'gpu_render_verified':False,'native_code':'V25 library unchanged; only engine SHA allowlist and all-entry preflight adapted','base_apk_sha256':'04f3e86e129bc7ef1705120caa93e43284f2033fffc376c4d597e5c7ddc15499'}
(BASE/'validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
