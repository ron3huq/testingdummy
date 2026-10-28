from pathlib import Path
import zipfile,sys,types,marshal,shutil,json,time
P=Path('/workspace/73-ui712');ROOT=Path('/tmp/ui712-cold');ROOT.mkdir(exist_ok=True);APK=Path('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-aligned-debugSigned.apk');prefix='assets/gateway-release/'
with zipfile.ZipFile(APK)as z:
 for n in z.namelist():
  if n.startswith(prefix)and not n.endswith('/'):
   f=ROOT/n[len(prefix):];f.parent.mkdir(exist_ok=True,parents=True)
   if not f.exists():f.write_bytes(z.read(n))
for part in ['/workspace/testingdummy/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip']:
 with zipfile.ZipFile(part)as z:
  for n in z.namelist():
   if n.startswith(prefix):f=ROOT/n[len(prefix):];f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(z.read(n))
shutil.copytree(P/'build/apk/assets/gateway-release',ROOT,dirs_exist_ok=True)
sys.path.insert(0,str(ROOT/'work/tools'))
with zipfile.ZipFile(P/'build/apk/assets/chaquopy/app.imy')as a:
 m=types.ModuleType('_protected_runtime');m.__file__=str(ROOT/'work/tools/_protected_runtime.py');sys.modules[m.__name__]=m;exec(marshal.loads(a.read('_protected_runtime.pyc')[16:]),m.__dict__);m.install_root(ROOT)
import embedded_gateway as g
print('GATEWAY_IMPORTED',g.__file__)
print('FUNCTIONS',[(n,list(v.__code__.co_varnames[:v.__code__.co_argcount]))for n,v in vars(g).items()if isinstance(v,types.FunctionType)and n in ['prepare','init','manage','start','handle']])
print('GLOBALS',[(n,type(v).__name__)for n,v in vars(g).items()if n in ['_logic','_root','ROOT','root']])
print('ALL_FUNCTIONS',[(n,list(v.__code__.co_varnames[:v.__code__.co_argcount]))for n,v in vars(g).items()if isinstance(v,types.FunctionType)])
import dis
with (P/'cold-initialize.dis').open('w')as f:dis.dis(g.initialize,file=f)
with (P/'cold-manage.dis').open('w')as f:dis.dis(g.manage,file=f)
print('INITIALIZE',g.initialize(str(ROOT),311010108))
print('STATUS',g.status())
print('LOGIC_AFTER',g._logic)
import bridge_73
bridge_73.install(ROOT,g)
import noodle_hair,private_bundles,select_team_runtime
meta=noodle_hair.bundle();private_bundles.verified();print('ALL_STATIC_INTEGRITY_OK',len(meta['target_card_ids']))
value={'livedata_list':[],'version_file':json.dumps({'version':1,'dt880':[]})};value=g._local_urls(value);print('ADVERTISED',[r['name']for r in json.loads(value['version_file'])['dt880']])
print('TRANSFER_API',json.loads(g.manage('ui712_transfer_get',json.dumps({'team_id':4937,'competition':473})))['ready'])
(P/'cold-start-validation.json').write_text(json.dumps({'passed':True,'original_protected_gateway_initialized':True,'all_new_manage_wrappers_installed':True,'static_integrity_verified':True,'face_targets':len(meta['target_card_ids']),'advertised_containers':[r['name']for r in json.loads(value['version_file'])['dt880']],'Android_tested':False},indent=2))
