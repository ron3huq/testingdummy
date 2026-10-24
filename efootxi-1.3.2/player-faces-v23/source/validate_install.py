from pathlib import Path
import importlib.util,struct,types,tempfile,json,ctypes,hashlib
r=Path(__file__).parent;src=r.parent/'android-hair-v1'
spec=importlib.util.spec_from_file_location('tested_hair',r/'noodle_hair.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.jump(0x123456789abcdef)==struct.pack('<IIQ',0x58000050,0xd61f0200,0x123456789abcdef)
engine=Path('/workspace/ronaldo-work/apk/lib/arm64-v8a/libUE4.so').read_bytes();assert hashlib.sha256(engine).hexdigest()==m.ENGINE_SHA
base=0x10000000;entries={entry:engine[entry-0x4000:entry-0x4000+16] for entry in [0x3883248,0x38809bc,0x330ae54,0x39bc570,0x39bc5ac,0x39c0420,0x823be04,0x82a1e48,0x3a908a0,0x39cb75c,0x45b58b0,0x39d3604,0x39d3e1c,0x39cd71c,0x39cdb10]}
for entry,p in entries.items():assert engine[entry-0x4000:entry-0x4000+16]==p
class Fn:
 def __init__(self,fn=lambda *a:0,address=0x70000000):self.fn=fn;self.address=address
 def __call__(self,*args):return self.fn(*args)
class Lib:
 def __getattr__(self,n):
  v=Fn();setattr(self,n,v);return v
hook=Lib();libc=Lib();writes=[];copies=[];protections=[];configured=[]
libc.mmap=Fn(lambda *a:base+0x9000000);libc.mprotect=Fn(lambda *a:(protections.append(a),0)[1]);libc.munmap=Fn()
hook.store_instruction=Fn(lambda *a:writes.append(a));hook.configure_load=Fn(lambda *a:configured.append(('load',a)));hook.configure_done=Fn(lambda *a:configured.append(('done',a)))
fake=types.SimpleNamespace(**{n:getattr(ctypes,n) for n in ['c_size_t','c_void_p','c_uint32','c_uint64','c_int','c_long','c_uint','sizeof']})
fake.CDLL=lambda name,**kw:libc if name=='libc.so' else hook
fake.string_at=lambda addr,n:entries[addr-base][:n]
fake.cast=lambda fn,tp:types.SimpleNamespace(value=fn.address)
fake.memmove=lambda addr,data,n:copies.append((addr,bytes(data[:n])))
fake.get_errno=lambda:0;m.C=fake
m.maps=lambda:[(base,base+0x9000000,'r-xp',0,'/fake/libUE4.so'),(base+0x9002000,base+0x9003000,'r--p',0,'/fake/other')]
m.digest=lambda path:m.ENGINE_SHA if str(path).endswith('libUE4.so') else m.HOOK_SHA
for entry,name,cfg in [(0x3883248,'noodle_card_data_ext_hook','configure_card_data_ext'),(0x38809bc,'noodle_card_data_hook','configure_card_data'),(0x330ae54,'noodle_icon_data_hook','configure_icon_data'),(0x39bc570,'noodle_shirt_char_hook','configure_shirt_char'),(0x39bc5ac,'noodle_shirt_string_hook','configure_shirt_string'),(0x39c0420,'noodle_shirt_key_hook','configure_shirt_key'),(0x823be04,'noodle_record_lookup_hook','configure_record_lookup'),(0x82a1e48,'noodle_record_name_hook','configure_record_name'),(0x3a908a0,'noodle_player_name_hook','configure_player_name'),(0x39cb75c,'noodle_bake_hook','configure_bake'),(0x45b58b0,'noodle_path_hook','configure_path'),(0x39d3604,'noodle_texture_done_hook','configure_texture_done'),(0x39d3e1c,'noodle_done_hook','configure_done'),(0x39cd71c,'noodle_load_hook','configure_load'),(0x39cdb10,'noodle_outer_hook','configure_outer')]:
 assert m.install(base,'/fake/libUE4.so',entry,entries[entry],name,cfg) is hook
assert len(writes)==15 and len(copies)==15 and [x[0] for x in configured]==['done','load']
for (addr,data),(target,instruction) in zip(copies,writes):
 assert len(data)==52 and data[:16]==m.jump(0x70000000)
 assert data[32:36]==entries[target-base][:4]
 assert instruction==m.branch(target,addr)
class Stop(BaseException):pass
m.bundle=lambda:{};m.platform.machine=lambda:'aarch64';m.configuration=lambda:True
m.time=types.SimpleNamespace(time=__import__('time').time,sleep=lambda *a:(_ for _ in ()).throw(Stop()))
with tempfile.TemporaryDirectory() as d:
 m.HERE=Path(d)
 try:m.worker()
 except Stop:pass
 report=json.loads((m.HERE/'player-faces-v23-status.json').read_text());assert json.loads((m.HERE/'noodle-hair-status.json').read_text())==report;assert report['session_id'] and report['runtime_path'].endswith('noodle_hair.py') and report['runtime_sha256'];assert report['state']=='HOOK_ACTIVE' and report['error'] is None and report['version']=='player-faces-v23-source-rebuild-stability'
(r/'hook-install-validation.json').write_text(json.dumps({'fixed_jump_executed':True,'fifteen_full_python_install_paths_executed':True,'worker_reaches_hook_active':True,'original_engine_hash_and_both_prologues_verified':True,'native_boundary':'ctypes mmap, memory writes and native functions modeled; no phone renderer tested','phone_tested':False},indent=2));print('FIFTEEN_INSTALL_PATHS_AND_WORKER_HOOK_ACTIVE_PASS')
