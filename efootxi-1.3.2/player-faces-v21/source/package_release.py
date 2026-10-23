from pathlib import Path
import hashlib,json,zipfile,shutil,importlib.util

r=Path(__file__).resolve().parent;O=r.parent;root=r/'deploy'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((O/'asset-validation.json').read_text())['status']=='V21_INDEPENDENT_READER_RIG_GLYPH_JAW_AND_CARD_PASS'
assert json.loads((O/'native-validation.json').read_text())['status']=='V21_SCOPE_FALLBACK_NATIVE_HEAD_LIFECYCLE_PASS'
assert json.loads((O/'squad-abi-validation.json').read_text())['status']=='OLD_CRASH_REPRODUCED_NEW_23_ARGUMENTS_PASS'
assert json.loads((O/'runtime-validation.json').read_text())['status']=='V21_BUNDLE_HASH_17_IDS_MANIFEST_PLUS39_IDEMPOTENCE_FAILURE_FALLBACK_PASS'
spec=importlib.util.spec_from_file_location('v21_package',root/'work/tools/noodle_hair.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.bundle()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+ext for ext in ['pak','utoc','ucas']]
def put(z,name,data):
    info=zipfile.ZipInfo(name,(2026,10,24,0,0,0));info.external_attr=0o100644<<16
    z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
main=O/'Faces-v21-native-heads-cards-kits.zip'
with zipfile.ZipFile(main,'w')as z:
    put(z,'HUONG_DAN.md',(O/'HUONG_DAN.md').read_bytes())
    for name in files:put(z,name,(root/name).read_bytes())
with zipfile.ZipFile(main)as z:
    assert z.testzip()is None and set(z.namelist())==set(files+['HUONG_DAN.md'])
    for name in files:assert hashlib.sha256(z.read(name)).hexdigest()==sha(root/name)
    assert len(z.read('work/tools/gateway_runtime.py'))==2441
report={'status':'V21_COMPLETE_ZIP_CRC_CHECKSUM_AND_SCOPED_PAYLOAD_PASS','main_sha256':sha(main),'main_bytes':main.stat().st_size,'files':{name:{'bytes':(root/name).stat().st_size,'sha256':sha(root/name)}for name in files},'target_ids':17,'native_checks':len(json.loads((O/'native-validation.json').read_text())['checks']),'phone_tested':False,'black_faces_device_verified_fixed':False,'jersey_names_device_verified_fixed':False}
(O/'package-validation.json').write_text(json.dumps(report,indent=2))
source=O/'Faces-v21-source-and-research.zip'
with zipfile.ZipFile(source,'w')as z:
    for p in sorted(O.glob('*.json')):put(z,p.name,p.read_bytes())
    for name in ['BUILD.md','HUONG_DAN.md','Card-layout-preview.png']:put(z,name,(O/name).read_bytes())
    for p in sorted(r.iterdir()):
        if p.is_file()and p.suffix in ['.py','.c','.sh','.so','.txt']:put(z,'source/'+p.name,p.read_bytes())
    for folder in ['original-inputs','art','studio-review','reader-logs']:
        for p in sorted((O/folder).rglob('*')):
            if p.is_file():put(z,str(p.relative_to(O)),p.read_bytes())
    # Actual recovered source closes the input-dependency gap for the new face.
    source_root=Path('/workspace/ronaldo-work/v21-input/diomande')
    for p in sorted(source_root.rglob('*')):
        if p.is_file():put(z,'recovered-diomande/'+str(p.relative_to(source_root)),p.read_bytes())
with zipfile.ZipFile(source)as z:assert z.testzip()is None
(O/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.name+'\n'for p in [main,source]))
print(json.dumps({'main':main.name,'bytes':main.stat().st_size,'sha256':sha(main),'source_bytes':source.stat().st_size,'native_checks':report['native_checks']}))
