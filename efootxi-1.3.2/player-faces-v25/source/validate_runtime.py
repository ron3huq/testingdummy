from pathlib import Path
import importlib.util,json,copy,hashlib

r=Path(__file__).resolve().parent;tools=r/'deploy/work/tools'
spec=importlib.util.spec_from_file_location('hair_v25_runtime',tools/'noodle_hair.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
meta=m.bundle();assert meta['version']=='player-faces-v25-2017-blender-v3-test'and len(meta['target_card_ids'])==17
assert hashlib.sha256((tools/'libnoodle_hair.so').read_bytes()).hexdigest()==m.HOOK_SHA==meta['native_sha256']
assert (tools/'gateway_runtime.py').stat().st_size==2441
original=json.loads(Path('/workspace/ronaldo-work/apk/assets/gateway-release/work/templates/CMD_LOGIN_LIVEDATA.json').read_text());snapshot=copy.deepcopy(original)
result=m.advertise(original,18247);assert original==snapshot and result!=original
assert json.loads(result['version_file'])['version']==json.loads(original['version_file'])['version']+43
assert m.advertise(result,18247)==result
assert m.advertise({'other':True},18247)=={'other':True}
assert [x for x in json.loads(result['version_file'])['dt880']if x.get('name')!='pc9298']==[x for x in json.loads(original['version_file'])['dt880']if x.get('name')!='pc9298']
control=tools/'noodle_hair.json';old=control.read_bytes();control.write_text('{"enabled":false}')
assert not m.configuration()and m.advertise(original,18247)==result;control.write_bytes(old)
for file in [tools/'libnoodle_hair.so',tools/'myleague_editor_runtime.py',tools/'libselect_team.so',r/'deploy/livedata/pc9298_mobile_and.utoc']:
    old=file.read_bytes()
    try:file.write_bytes(b'corrupt');assert m.advertise(original,18247)==original
    finally:file.write_bytes(old)
(tools/'noodle-advertise-error.txt').unlink(missing_ok=True)
for p in tools.glob('*.py'):compile(p.read_text(),str(p),'exec')
report={'status':'V25_BUNDLE_HASH_17_IDS_MANIFEST_PLUS43_IDEMPOTENCE_FAILURE_FALLBACK_PASS','gateway_bytes':2441,'myleague_user_configuration_files_not_in_package':True,'appearance_overlay_and_native_module_byte_identical_to_v20':True,'phone_tested':False}
(r.parent/'runtime-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
