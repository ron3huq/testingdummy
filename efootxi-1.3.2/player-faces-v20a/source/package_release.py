"""Overlay only 3 runtime files onto the exact v20 package; validate before ZIP."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, tempfile, zipfile

r = Path(__file__).resolve().parent
out = r.parent
baseline = out.parent/'player-faces-v20/Faces-v20-14-cards-4-teams.zip'
sha = lambda data: hashlib.sha256(data).hexdigest()
assert sha(baseline.read_bytes()) == '5d754379d28f2c625e8dab42effbdee90907ba2d2d7a9c115dca5029b874b974'
spec = importlib.util.spec_from_file_location('hotfix_package',r/'noodle_hair.py')
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.HOOK_SHA == sha((r/'libnoodle_hair.so').read_bytes())
tools = r/'deploy/work/tools';tools.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(baseline) as z:
    old = json.loads(z.read('work/tools/noodle_bundle.json'))
    meta = dict(old, version='player-faces-v20a-squad-abi-fix', native_sha256=m.HOOK_SHA, phone_tested=False)
    for n in ['noodle_hair.py','libnoodle_hair.so']:shutil.copyfile(r/n,tools/n)
    (tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
    # Validate an actual full-v20 installation with only our 3-file overlay.
    with tempfile.TemporaryDirectory(prefix='v20a-install-') as tmp:
        root=Path(tmp);z.extractall(root)
        for f in tools.iterdir():shutil.copyfile(f,root/'work/tools'/f.name)
        m.HERE=root/'work/tools';assert m.bundle()['version']==meta['version']
        assert (m.HERE/'gateway_runtime.py').stat().st_size==2441
        for name in z.namelist():
            if name in ['work/tools/noodle_hair.py','work/tools/libnoodle_hair.so','work/tools/noodle_bundle.json']:continue
            if name.endswith('/'):continue
            assert (root/name).read_bytes()==z.read(name)
        response=json.loads(Path('/workspace/ronaldo-work/apk/assets/gateway-release/work/templates/CMD_LOGIN_LIVEDATA.json').read_text())
        result=m.advertise(response,18247)
        assert m.advertise(result,18247)==result
        assert json.loads(result['version_file'])['version']==json.loads(response['version_file'])['version']+38
        assert result!=response
        m.HERE.joinpath('libnoodle_hair.so').write_bytes(b'broken')
        assert m.advertise(response,18247)==response
assert meta['files']==old['files'] and meta['appearance_files']==old['appearance_files'] and meta['appearance_overlay_sha256']==old['appearance_overlay_sha256']
assert json.loads((out/'squad-abi-validation.json').read_text())['status']=='OLD_CRASH_REPRODUCED_NEW_23_ARGUMENTS_PASS'
assert len(json.loads((r/'native-validation.json').read_text())['checks'])==792
name=out/'Faces-v20a-squad-crash-hotfix.zip'
with zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED,9) as z:
    z.write(out/'HUONG_DAN.md','HUONG_DAN.md')
    for f in sorted(tools.iterdir()):z.write(f,'work/tools/'+f.name)
with zipfile.ZipFile(name) as z:
    assert z.testzip() is None and len(z.namelist())==4
report={'status':'V20_OVERLAY_HASH_MANIFEST_IDEMPOTENCE_AND_ZIP_PASS','files_replaced':3,'v20_all_other_files_byte_identical':True,'asset_manifest_revision_unchanged':True,'native_sha256':m.HOOK_SHA,'zip_sha256':sha(name.read_bytes()),'zip_size':name.stat().st_size,'phone_tested':False}
(out/'package-validation.json').write_text(json.dumps(report,indent=2))
with zipfile.ZipFile(out/'Faces-v20a-source-and-tests.zip','w',zipfile.ZIP_DEFLATED,9) as z:
    for p in sorted(out.glob('*.json')):z.write(p,p.name)
    for p in [out/'HUONG_DAN.md',out/'BUILD.md']:z.write(p,p.name)
    for p in sorted(r.iterdir()):
        if p.suffix in ['.c','.py','.sh']:z.write(p,'source/'+p.name)
    z.write(r/'libnoodle_hair.so','source/libnoodle_hair.so')
(out/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in [name,out/'Faces-v20a-source-and-tests.zip']))
print(json.dumps(report))
