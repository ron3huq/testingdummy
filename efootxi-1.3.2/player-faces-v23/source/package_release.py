from pathlib import Path
import hashlib,json,zipfile,importlib.util

r=Path(__file__).resolve().parent;O=r.parent;root=r/'deploy'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for filename,status in [
    ('asset-validation.json','V23_SOURCE_TOPOLOGY_NATIVE_RIG_AND_MINI_READBACK_PASS'),
    ('native-validation.json','V23_SCOPE_FALLBACK_NATIVE_HEAD_LIFECYCLE_PASS'),
    ('stability-validation.json','V23_V21_NATIVE_BASELINE_NO_DRAW_PROBE_FULL64_PASS'),
    ('squad-abi-validation.json','OLD_CRASH_REPRODUCED_NEW_23_ARGUMENTS_PASS'),
    ('runtime-validation.json','V23_BUNDLE_HASH_17_IDS_MANIFEST_PLUS41_IDEMPOTENCE_FAILURE_FALLBACK_PASS')]:
    assert json.loads((O/filename).read_text())['status']==status
assert json.loads((r/'hook-install-validation.json').read_text())['worker_reaches_hook_active']
spec=importlib.util.spec_from_file_location('v23_release_runtime',root/'work/tools/noodle_hair.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.bundle()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+ext for ext in ['pak','utoc','ucas']]
oldzip=O.parent/'player-faces-v21/Faces-v21-native-heads-cards-kits.zip'
with zipfile.ZipFile(oldzip)as z:
    for name in files:
        if name.startswith('work/')and Path(name).name not in ['noodle_hair.py','libnoodle_hair.so','noodle_bundle.json']:
            assert z.read(name)==(root/name).read_bytes()
def put(z,name,data):
    info=zipfile.ZipInfo(name,(2026,10,24,0,0,0));info.external_attr=0o100644<<16
    z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
main=O/'Faces-v23-source-heads-OzilV2-centered-minis.zip'
with zipfile.ZipFile(main,'w')as z:
    put(z,'HUONG_DAN.md',(O/'HUONG_DAN.md').read_bytes())
    for name in files:put(z,name,(root/name).read_bytes())
with zipfile.ZipFile(main)as z:
    assert z.testzip()is None and set(z.namelist())==set(files+['HUONG_DAN.md'])
    for name in files:assert hashlib.sha256(z.read(name)).hexdigest()==sha(root/name)
    assert len(z.read('work/tools/gateway_runtime.py'))==2441
report={'status':'V23_COMPLETE_ZIP_CRC_CHECKSUM_AND_SCOPED_PAYLOAD_PASS','main_sha256':sha(main),'main_bytes':main.stat().st_size,'files':{name:{'bytes':(root/name).stat().st_size,'sha256':sha(root/name)}for name in files},'target_ids':17,'native_checks':len(json.loads((O/'native-validation.json').read_text())['checks']),'phone_tested':False,'black_faces_device_verified_fixed':False,'jersey_names_device_verified_fixed':False,'unchanged_work_files_exact_to_published_v21':True}
(O/'package-validation.json').write_text(json.dumps(report,indent=2))
source=O/'Faces-v23-source-and-tests.zip'
with zipfile.ZipFile(source,'w')as z:
    for p in sorted(O.glob('*.json')):put(z,p.name,p.read_bytes())
    for name in ['BUILD.md','HUONG_DAN.md','Mini-preview.png']:put(z,name,(O/name).read_bytes())
    for p in sorted(r.iterdir()):
        if p.is_file()and p.suffix in ['.py','.c','.sh','.so','.txt','.inc','.json']:put(z,'source/'+p.name,p.read_bytes())
    for folder in ['art','references','reader-logs','original-inputs']:
        for p in sorted((O/folder).rglob('*')):
            if p.is_file():put(z,str(p.relative_to(O)),p.read_bytes())
with zipfile.ZipFile(source)as z:assert z.testzip()is None and 'original-inputs/Mesut_OZIL_V2.rar'in z.namelist()
(O/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.name+'\n'for p in [main,source]))
print(json.dumps({'main':main.name,'main_bytes':main.stat().st_size,'sha256':sha(main),'source_bytes':source.stat().st_size,'native_checks':report['native_checks']}))
