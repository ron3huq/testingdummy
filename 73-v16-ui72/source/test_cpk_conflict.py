from pathlib import Path
import tempfile,shutil,importlib.util,json,hashlib,types
import sys,marshal,zipfile
fixture=Path('/workspace/ronaldo-work/73-v25-full/test-gateway')
sys.path.insert(0,str(fixture/'work/tools'))
with zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy')as app:
 pr=types.ModuleType('_protected_runtime');pr.__file__=str(fixture/'work/tools/_protected_runtime.py');sys.modules[pr.__name__]=pr;exec(marshal.loads(app.read('_protected_runtime.pyc')[16:]),pr.__dict__);pr.install_root(fixture)
import legends_v10
P=Path('/workspace/ronaldo-work/73-ui72');tmp=Path(tempfile.mkdtemp(prefix='ui72-cpk-conflict-'));r=tmp/'embedded-gateway';t=r/'work/tools';t.mkdir(parents=True);live=r/'livedata';live.mkdir();source=r/'custom-resources/legends-v10';source.mkdir(parents=True)
base=Path('/workspace/ronaldo-work/73-ui6/original-dt870.cpk');old=Path('/workspace/ronaldo-work/73-ui71/payload/work/tools');modcpk=Path('/workspace/ronaldo-work/73-ui71/payload/livedata/dt870_mobile_and.cpk');source.joinpath(base.name.replace('original-dt870','dt870_mobile_and')).write_bytes(base.read_bytes())
# Exact original73 resource-restoration function and its real dt870 checks;
# unrelated209MB player bundles are excluded from this isolated regression.
legends_v10.ROOT=r;legends_v10._SOURCE_CHECKS=[x for x in legends_v10._SOURCE_CHECKS if x['name']=='dt870_mobile_and.cpk'];legends_v10._ACTIVE_CHECKS=[x for x in legends_v10._ACTIVE_CHECKS if x['source']=='dt870_mobile_and.cpk'];legends_v10._active_fingerprint=None;legends_v10._source_verified={}
shutil.copy2(old/'kits_bundle.json',t/'kits_bundle.json')
for f in Path('/workspace/ronaldo-work/73-ui71/payload/livedata').glob('pc9303_mobile_and.*'):shutil.copy2(f,live/f.name)
shutil.copy2(modcpk,live/'dt870_mobile_and.cpk')
def load(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.HERE=t;return m
before=load('kits_before',old/'kits_runtime.py');before.verified();result=legends_v10._resources();assert result['status']=='ready';assert (live/'dt870_mobile_and.cpk').read_bytes()==base.read_bytes();before.verified.cache_clear()
try:before.verified();raise AssertionError('old conflict did not reproduce')
except ValueError as exc:assert 'Shirt/coach payload does not match manifest: dt870_mobile_and.cpk'in str(exc)
after=load('kits_after',P/'payload/work/tools/kits_runtime.py');shutil.copy2(modcpk,live/after.CPK_SOURCE)
value={'version_file':json.dumps({'version':1,'dt880':[],'dt870Hash':'stock'}),'livedata_list':[]};out=after.advertise(value,8085);again=after.advertise(out,8085);assert again==out
row=next(x for x in out['livedata_list']if x['name']=='dt870_mobile_and.cpk');assert row['url'].endswith('/'+after.CPK_SOURCE);advertised=json.loads(out['version_file']);assert advertised['dt870Hash']==hashlib.sha256(modcpk.read_bytes()).hexdigest()
# Re-run the real stock restoration after both old target paths are disturbed.
(live/'dt870_mobile_and.cpk').write_bytes(b'old mutable path');legends_v10._active_fingerprint=None;assert legends_v10._resources()['status']=='ready';after.verified.cache_clear();assert after.advertise(value,8085)==out;assert (live/after.CPK_SOURCE).read_bytes()==modcpk.read_bytes();assert (live/'dt870_mobile_and.cpk').read_bytes()==base.read_bytes()
# Still reject damage to the isolated resource; no checksum bypass.
data=(live/after.CPK_SOURCE).read_bytes();(live/after.CPK_SOURCE).write_bytes(b'x'+data[1:]);after.verified.cache_clear()
try:after.verified();raise AssertionError('bad isolated resource accepted')
except ValueError:pass
report={'passed':True,'original73_legends_resources_executed':True,'exact_UI71_error_reproduced_after_stock_resource_repair':True,'stock_CPK_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'isolated_mod_CPK_sha256':hashlib.sha256(modcpk.read_bytes()).hexdigest(),'stock_paths_can_be_restored_without_changing_mod_source':True,'logical_dt870_metadata_matches_isolated_download_bytes':True,'advertising_idempotent':True,'damaged_isolated_CPK_still_rejected':True,'device_tested':False};(P/'cpk-conflict-validation.json').write_text(json.dumps(report,indent=2));print('CPK_CONFLICT_PASS')
