from pathlib import Path
import zipfile,json,hashlib,re,ast
P=Path('/workspace/ronaldo-work/73-ui6');repo=Path('/workspace/testingdummy/73-v16-ui6');artifact=repo/'V25-73-UI6-Persistent-NativeSleeves-Y08-MT.zip';sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(artifact)as patch,zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 names=patch.namelist();assert len(names)==len(set(names));assert not any(n.endswith(('.efsave','.sqlite3','.db','.blend'))or'__pycache__'in n for n in names)
 assert not any('pc9301_mobile_and.'in n or 'pc9299_mobile_and.'in n or n.endswith('coach_changes.py')or n.endswith('rolled_runtime.py')for n in names)
 manifest=json.loads(patch.read('assets/gateway-release/release-manifest.json'))
 for row in manifest['files']:
  n='assets/gateway-release/'+row['path'];data=(patch if n in names else base).read(n);assert len(data)==row['bytes']and sha(data)==row['sha256'],row['path']
 repair=json.loads(patch.read('assets/gateway-release/ui6-runtime-manifest.json'))
 for row in repair['files']:
  n='assets/gateway-release/'+row['path'];data=(patch if n in names else base).read(n);assert len(data)==row['bytes']and sha(data)==row['sha256'],row['path']
 assert not any(r['path'].endswith('myleague_editor.json')or'local-club.sqlite3'in r['path']for r in repair['files'])
 prefix='assets/gateway-release/work/tools/';meta=json.loads(patch.read(prefix+'noodle_bundle.json'))
 for name,h in meta['appearance_files'].items():assert sha(patch.read(prefix+name))==h,name
 assert meta['native_sha256']==sha(patch.read(prefix+'libnoodle_hair.so'))
 old=json.loads(Path('/workspace/ronaldo-work/73-v25-full/payload/work/tools/noodle_bundle.json').read_text());assert meta['files']==old['files'];assert set(meta['target_card_ids'])==set(old['target_card_ids'])|{'89138556572074','89136418985303'}
 assert len(meta['target_card_ids'])==19 and not any('pc9298_mobile_and.'in n for n in names)
 assert sha(patch.read(prefix+'libselect_team.so'))in patch.read(prefix+'select_team_runtime.py').decode()
 for file in ['extras_bundle.json','manager_bundle.json','kits_bundle.json']:
  rows=json.loads(patch.read(prefix+file))['files']
  for name,row in rows.items():
   data=patch.read('assets/gateway-release/livedata/'+name);assert len(data)==row['size']and sha(data)==row['sha256'],name
 designer=json.loads(patch.read('assets/card-designer/MANIFEST.json'))
 for n,row in designer.items():
  data=patch.read('assets/card-designer/'+n);assert len(data)==row['bytes']and sha(data)==row['sha256']
 cfg=json.loads(patch.read(prefix+'myleague_custom.json'));assert len(cfg['classic_profiles'])==286;assert len(cfg['leagues']['473']['teams'])==10
 assert {k:cfg['kit_aliases'][k]for k in ['1706','4937','1220','1222']}=={'1706':352,'4937':242,'1220':351,'1222':245}
 runtime=patch.read(prefix+'select_team_runtime.py').decode();assert not any('entry='+a in runtime for a in ['0x39ce7d8','0x39cefe4','0x6917eb0','0x823cb04','0x8294a7c'])
 pairs=ast.literal_eval(re.search(r'for entry,expected in (\[.*?\]):',runtime).group(1));assert len(pairs)==23
 assert 'keepExisting' in (P/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
 reports=['native-validation','ui-validation','myleague-api-validation','cpk-validation','repair-validation','startup-validation','resources-validation','static-glyphs-validation','face-copy-validation','sleeves-coaches-validation']
 for name in reports:
  v=json.loads((P/(name+'.json')).read_text());assert v.get('passed')is True or v.get('status')=='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',name
report={'passed':True,'manifest_entries':len(manifest['files']),'patch_entries':len(names),'repair_manifest_immutable_entries':len(repair['files']),'all_repair_sources_exist_in_APK_or_patch':True,'original_face_assets_unchanged':True,'19_face_targets_with_two_exact_aliases':True,'10_component_reports_passed':True,'save_and_mutable_editor_configuration_not_repaired_over':True,'ZIP_SHA256':sha(artifact.read_bytes()),'device_tested':False}
(repo/'validation/package-validation.json').write_text(json.dumps(report,indent=2));print('PACKAGE_PASS',report)
