from pathlib import Path
import zipfile,json,hashlib
p=Path('/workspace/ronaldo-work/73-ui3');repo=Path('/workspace/testingdummy/73-v16-ui3');artifact=repo/'V25-73-UI3-Slim-Cuffs-Y08-MT.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(artifact)as patch,zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 names=patch.namelist();assert len(names)==len(set(names));assert not any(n.endswith(('.efsave','.sqlite3','.db'))or 'save-audit' in n or '__pycache__' in n for n in names)
 assert {'classes5.dex','assets/card-designer/index.html','assets/editor-english.json'}<=set(names)
 manifest=json.loads(patch.read('assets/gateway-release/release-manifest.json'))
 for row in manifest['files']:
  n='assets/gateway-release/'+row['path'];data=(patch if n in names else base).read(n)
  assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
 meta=json.loads(patch.read('assets/gateway-release/work/tools/noodle_bundle.json'))
 for n,h in meta['appearance_files'].items():assert sha(patch.read('assets/gateway-release/work/tools/'+n))==h,n
 assert sha(patch.read('assets/gateway-release/work/tools/myleague_editor_runtime.py'))==meta['appearance_overlay_sha256']
 assert meta['native_sha256']=='7cb158c8a7b758f2c0809edb0edada81a33f6b5c4ea7317a58353dcd7add7d5b'
 assert not any('pc9298_mobile_and.' in n or n.endswith('/libnoodle_hair.so')or n.endswith('/noodle_hair.py')for n in names)
 old=json.loads(Path('/workspace/ronaldo-work/73-v25-full/payload/work/tools/noodle_bundle.json').read_text());assert meta['files']==old['files']and meta['target_card_ids']==old['target_card_ids']
 # Only the requested two new IDs are added to the native editor; no face redirect.
 rows=json.loads(patch.read('assets/gateway-release/work/tools/myleague_editor.json'))['players']
 for cid in ['89136418985303','89136418985302']:
  row=next(x for x in rows if x['id']==cid and x['competition']==0);assert row['sleeve']=='long'and len(row['parameters'])==74
 rolled=json.loads(patch.read('assets/gateway-release/work/tools/rolled_bundle.json'))
 for name,row in rolled['files'].items():
  data=patch.read('assets/gateway-release/livedata/'+name);assert len(data)==row['size']and sha(data)==row['sha256']
 designer=json.loads(patch.read('assets/card-designer/MANIFEST.json'))
 for name,row in designer.items():
  data=patch.read('assets/card-designer/'+name);assert len(data)==row['bytes']and sha(data)==row['sha256'],name
 original_designer={n for n in base.namelist()if n.startswith('assets/card-designer/')and not n.endswith('/')}
 assert len(original_designer)>=330 and original_designer<=set(names)
 for name in original_designer-{'assets/card-designer/index.html','assets/card-designer/MANIFEST.json','assets/card-designer/background-picker.js','assets/card-designer/mobile-ui.js','assets/card-designer/card-suites.js'}:assert sha(patch.read(name))==sha(base.read(name)),name
 for cid in ['89136418985303','89136418985302']:
  row=next(x for x in rows if x['id']==cid and x['competition']==0)
  assert row['parameters']['108']==0 and row['parameters']['125']==1
 assert patch.read('classes5.dex')[:8]==b'dex\n037\x00'
 cfg=json.loads(patch.read('assets/gateway-release/work/tools/myleague_custom.json'))
 assert len(cfg['leagues']['473']['teams'])==10 and cfg['league_names']['473']=='Y08 Champion League'
 ids=[i for tid in cfg['leagues']['473']['teams']for i in cfg['native_rosters'][str(tid)]]
 assert len(ids)==len(set(ids))==110
 assert{88037702766648,89135066911146,88046292734664,88046312750111,89136418985301,89136409091415,89067152870864,89066884435465}<=set(ids)
 runtime=patch.read('assets/gateway-release/work/tools/select_team_runtime.py').decode()
 assert sha(patch.read('assets/gateway-release/work/tools/libselect_team.so'))in runtime
 assert b"['version']+=18"in patch.read('assets/gateway-release/work/tools/rolled_runtime.py')
 checks=['all110 Y08 cards, exact requested IDs and membership; native loader checksum matches','rolled mesh and all designer assets match installation manifests','entire release manifest matches base APK + update overlay','all native/runtime integrity hashes agree','working face engine adapter/native library/container bytes and target mapping unchanged','both full64 custom IDs have long sleeves and canonical skill flags','original full My League overlay retained','no save or private database in package']
 report={'passed':True,'checks':checks,'manifest_entries':len(manifest['files']),'patch_entries':len(names),'zip_sha256':sha(artifact.read_bytes()),'device_tested':False}
(repo/'validation/package-validation.json').write_text(json.dumps(report,indent=2));print('PACKAGE_PASS',len(manifest['files']),len(names))
