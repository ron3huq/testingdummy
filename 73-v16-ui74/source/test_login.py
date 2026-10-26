from pathlib import Path
import zipfile,tempfile,shutil,json,sys,types,marshal,importlib.util,hashlib
P=Path('/workspace/ronaldo-work/73-ui74');r=Path(tempfile.mkdtemp(prefix='ui74-login-'))/'embedded-gateway';r.mkdir();t=r/'work/tools';t.mkdir(parents=True);(r/'outputs').mkdir();(r/'outputs/efootball').mkdir();reference=Path('/workspace/ronaldo-work/73-v25-full/test-gateway/outputs/reference');(r/'outputs/reference').symlink_to(reference,target_is_directory=True)
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui74/V25-73-UI7.4-FULL-Part2-Main-MT.zip')as patch:
 app=patch.read('assets/chaquopy/app.imy')
 for n in patch.namelist():
  if n.startswith('assets/gateway-release/work/tools/')or n.startswith('assets/gateway-release/livedata/'):
   dest=r/n.removeprefix('assets/gateway-release/');dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(patch.read(n))
for f in Path('/workspace/ronaldo-work/73-ui7/carry/livedata').glob('pc9298_mobile_and.*'):(r/'livedata'/f.name).symlink_to(f)
with zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 for n in base.namelist():
  if n.startswith('assets/gateway-release/work/templates/'):
   d=r/n.removeprefix('assets/gateway-release/');d.parent.mkdir(exist_ok=True,parents=True);d.write_bytes(base.read(n))
import io
app=zipfile.ZipFile(io.BytesIO(app));sys.path.insert(0,str(t));pr=types.ModuleType('_protected_runtime');pr.__file__=str(t/'_protected_runtime.py');sys.modules[pr.__name__]=pr;exec(marshal.loads(app.read('_protected_runtime.pyc')[16:]),pr.__dict__);pr.install_root(r)
mod=types.ModuleType('embedded_gateway');mod.__file__=str(t/'embedded_gateway.py');sys.modules[mod.__name__]=mod;exec(marshal.loads(app.read('embedded_gateway.pyc')[16:]),mod.__dict__)
import diy_startup,legends_v10
# Keep the actual legacy dt870 restorer; unrelated large player packs and
# Android-only DIY/binding setup are outside this host protocol regression.
diy_startup.initialize=lambda *a:None;diy_startup.installed_resources=lambda *a:None
legends_v10.ROOT=r;legends_v10._SOURCE_CHECKS=[x for x in legends_v10._SOURCE_CHECKS if x['name']=='dt870_mobile_and.cpk'];legends_v10._ACTIVE_CHECKS=[x for x in legends_v10._ACTIVE_CHECKS if x['source']=='dt870_mobile_and.cpk'];legends_v10._active_fingerprint=None;legends_v10._source_verified={}
source=r/'custom-resources/legends-v10';source.mkdir(parents=True);shutil.copy2('/workspace/ronaldo-work/73-ui6/original-dt870.cpk',source/'dt870_mobile_and.cpk')
legends_v10.activate=lambda *args:legends_v10._resources()
# Reproduce an upgrade where the old shared path initially contains UI7's mod.
shutil.copy2('/workspace/ronaldo-work/73-ui71/payload/livedata/dt870_mobile_and.cpk',r/'livedata/dt870_mobile_and.cpk')
assert json.loads(mod.initialize(str(r),9))['ready'];assert (r/'livedata/dt870_mobile_and.cpk').stat().st_size==16961869
req=mod.make_login_request();wire=mod.handle('/pes22/gate/gate_CMD_LOGIN.php',req);reply=json.loads(mod.verify_login(wire));assert reply['result']=='NOERR'and reply['wire_roundtrip']=='PASS'
# Use the actual recursive73 URL conversion around an isolated version object.
value={'version_file':json.dumps({'version':1,'dt880':[],'dt870Hash':'stock'}),'livedata_list':[]};a=mod._local_urls({'nested':value});b=mod._local_urls(a);assert a==b
row=next(x for x in a['nested']['livedata_list']if x['name']=='dt870_mobile_and.cpk');assert row['url'].endswith('/dt870_ui74_mobile_and.cpk');payload=(r/'livedata/dt870_ui74_mobile_and.cpk').read_bytes();assert hashlib.sha256(payload).hexdigest()==json.loads(a['nested']['version_file'])['dt870Hash']
report={'passed':True,'actual73_gateway_initialize_and_CMD_LOGIN':True,'legacy_dt870_restore_executed_in_initialize':True,'old_shared_mod_CPK_replaced_with_valid_stock':True,'login_result':reply['result'],'wire_roundtrip':reply['wire_roundtrip'],'recursive_local_URL_conversion_keeps_isolated_CPK':True,'repeated_URL_conversion_idempotent':True,'advertised_hash_matches_download_bytes':True,'unrelated_Android_resource_setup_stubbed':True,'device_tested':False};(P/'login-validation.json').write_text(json.dumps(report,indent=2));print('LOGIN_PASS',report)

shutil.rmtree(r.parent)
