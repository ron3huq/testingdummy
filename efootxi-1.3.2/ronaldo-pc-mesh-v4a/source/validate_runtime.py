from pathlib import Path
import sys,json,copy,importlib.util,tempfile,shutil,ast
r=Path(__file__).parent;root=r/'deploy';p=root/'work/tools/noodle_hair.py';s=importlib.util.spec_from_file_location('noodle_hair',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.bundle()
source=json.loads(Path('/workspace/analysis/my-league/android/official-apk/assets/gateway-release/work/templates/CMD_LOGIN_LIVEDATA.json').read_text());before=copy.deepcopy(source)
out=m.advertise(source,18247);assert source==before
v=json.loads(out['version_file']);old=json.loads(source['version_file']);assert v['version']==old['version']+22
assert [x for x in v['dt880'] if x.get('name')!='pc9298']==old['dt880']
assert len(out['livedata_list'])==len(source['livedata_list'])+3
for x in out['livedata_list'][-3:]:assert x['url']=='http://127.0.0.1:18247/livedata/'+x['name'] and (root/'livedata'/x['name']).stat().st_size==x['size']
assert m.advertise(out,18247)==out
assert m.advertise({'other':1},18247)=={'other':1}
# Disabling visuals keeps the mounted manifest/version stable; prevents rollback churn.
control=p.parent/'noodle_hair.json';control.write_text('{"enabled":false}');assert not m.configuration();assert m.advertise(source,18247)==out;control.write_text('{"enabled":true}')
# Corrupt asset is never advertised; original response is returned without mutation.
f=root/'livedata/pc9298_mobile_and.utoc';original=f.read_bytes();f.write_bytes(b'broken');assert m.advertise(source,18247)==source;f.write_bytes(original)
(root/'work/tools/noodle-advertise-error.txt').unlink(missing_ok=True)
# Execute the complete gateway wrapper with native startup suppressed.
m.start=lambda:None;sys.modules['noodle_hair']=m
mod=importlib.util.spec_from_file_location('gateway_runtime_trial',root/'work/tools/gateway_runtime.py');g=importlib.util.module_from_spec(mod);mod.loader.exec_module(g)
wrapped=g.rewrite_live_urls(source,18247);wv=json.loads(wrapped['version_file']);assert wv['version']==old['version']+22
assert len(wrapped['livedata_list'])==len(source['livedata_list'])+3
assert all(x['url'].startswith('http://127.0.0.1:18247/livedata/') for x in wrapped['livedata_list'])
assert g.rewrite_live_urls(wrapped,18247)==wrapped
assert all(k in wrapped for k in source)
# Installer retains single 4-byte atomic patch and validates engine/prologues/digests.
code=p.read_text();assert 'hook.store_instruction(target,branch(target,cave))' in code and 'MAP_FIXED' in code and 'C.string_at(target,16) != prologue' in code
for name in ['noodle_hair.py','gateway_runtime.py']:compile((p.parent/name).read_text(),name,'exec')
report={'status':'MANIFEST_SCOPE_HASH_FAILURE_DISABLE_AND_GATEWAY_WRAPPER_PASS','original_response_unchanged':True,'original_dt880_entries_unchanged':True,'new_files':3,'idempotent':True,'disabled_visuals_manifest_stable':True,'checksum_failure_passthrough':True,'network_on_android_tested':False,'native_startup_in_test':'suppressed on host'}
(r/'runtime-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
