from pathlib import Path
import zipfile,json,hashlib
P=Path('/workspace/ronaldo-work/73-ui5');repo=Path('/workspace/testingdummy/73-v16-ui5');artifact=repo/'V25-73-UI5-Fixes-MT.zip';sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(artifact)as patch,zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 names=patch.namelist();assert len(names)==len(set(names));assert not any(n.endswith(('.efsave','.sqlite3','.db','.blend','.blend1'))or '__pycache__'in n or 'save-audit'in n for n in names)
 assert {'classes5.dex','assets/card-designer/index.html','assets/editor-english.json'}<=set(names)
 manifest=json.loads(patch.read('assets/gateway-release/release-manifest.json'))
 for row in manifest['files']:
  n='assets/gateway-release/'+row['path'];data=(patch if n in names else base).read(n);assert len(data)==row['bytes']and sha(data)==row['sha256'],row['path']
 prefix='assets/gateway-release/work/tools/';meta=json.loads(patch.read(prefix+'noodle_bundle.json'))
 for name,h in meta['appearance_files'].items():assert sha(patch.read(prefix+name))==h,name
 assert sha(patch.read(prefix+'myleague_editor_runtime.py'))==meta['appearance_overlay_sha256'];assert sha(patch.read(prefix+'libnoodle_hair.so'))==meta['native_sha256']
 old=json.loads(Path('/workspace/ronaldo-work/73-v25-full/payload/work/tools/noodle_bundle.json').read_text());assert meta['files']==old['files']and meta['target_card_ids']==old['target_card_ids']
 assert not any('pc9298_mobile_and.'in n for n in names)
 oldface=Path('/workspace/ronaldo-work/73-v25-port/package/payload/work/tools/noodle_hair.py').read_text();newface=patch.read(prefix+'noodle_hair.py').decode();assert newface.replace(meta['native_sha256'],'7cb158c8a7b758f2c0809edb0edada81a33f6b5c4ea7317a58353dcd7add7d5b')==oldface
 assert meta['native_sha256']in newface
 for stem,filename in [('pc9301','rolled_bundle.json'),('pc9300','extras_bundle.json'),('pc9302','manager_bundle.json')]:
  rows=json.loads(patch.read(prefix+filename))['files'];assert len(rows)==3
  for name,row in rows.items():
   assert name.startswith(stem);data=patch.read('assets/gateway-release/livedata/'+name);assert len(data)==row['size']and sha(data)==row['sha256']
 designer=json.loads(patch.read('assets/card-designer/MANIFEST.json'))
 for name,row in designer.items():
  data=patch.read('assets/card-designer/'+name);assert len(data)==row['bytes']and sha(data)==row['sha256'],name
 original_designer={n for n in base.namelist()if n.startswith('assets/card-designer/')and not n.endswith('/')};assert len(original_designer)>=330 and original_designer<=set(names)
 for name in original_designer-{'assets/card-designer/index.html','assets/card-designer/MANIFEST.json','assets/card-designer/background-picker.js','assets/card-designer/mobile-ui.js','assets/card-designer/card-suites.js','assets/card-designer/phone-layout.css'}:assert sha(patch.read(name))==sha(base.read(name)),name
 cfg=json.loads(patch.read(prefix+'myleague_custom.json'));assert len(cfg['classic_profiles'])==286
 for profile in cfg['classic_profiles'].values():assert profile['competition']in[518,473]and profile['all_positions']and 92<=profile['target_ovr']<=100
 assert {k:cfg['kit_aliases'][k]for k in ['1706','4937','1220','1222']}=={'1706':352,'4937':242,'1220':351,'1222':245}
 assert len(cfg['leagues']['473']['teams'])==10 and cfg['league_names']['473']=='Y08 Champion League'
 ids=[i for tid in cfg['leagues']['473']['teams']for i in cfg['native_rosters'][str(tid)]];assert len(ids)==len(set(ids))==110
 assert{88037702766648,89135066911146,88046292734664,88046312750111,89136418985301,89136409091415,89067152870864,89066884435465}<=set(ids)
 assert patch.read('classes5.dex')[:8]==b'dex\n037\x00'
 assert sha(patch.read(prefix+'libselect_team.so'))in patch.read(prefix+'select_team_runtime.py').decode()
 for name in ['ui-validation','native-validation','runtime-validation','codec-validation','body-assets-validation','myleague-api-validation','designer-validation','regression-validation','art-assets-validation','pose-validation']:
  v=json.loads((P/(name+'.json')).read_text());assert v.get('passed')is True or v.get('status')=='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',name
 assert not any('editor_details.py'in n or 'editor_skill_labels.json'in n or 'pc9299_mobile_and.'in n for n in names)
report={'passed':True,'manifest_entries':len(manifest['files']),'patch_entries':len(names),'zip_sha256':sha(artifact.read_bytes()),'face_container_and_mapping_unchanged':True,'face_loader_only_integrity_pin_changed':True,'three_added_resource_containers':True,'all_10_component_reports_pass':True,'no_user_save_or_database':True,'android_device_tested':False}
(repo/'validation/package-validation.json').write_text(json.dumps(report,indent=2));print('PACKAGE_PASS',report)
