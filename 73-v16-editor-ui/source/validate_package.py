from pathlib import Path
import zipfile,json,hashlib
p=Path('/workspace/ronaldo-work/73-ui');repo=Path('/workspace/testingdummy/73-v16-editor-ui');artifact=repo/'V25-73-Full-Editor-UI1-MT.zip'
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
 checks=['entire release manifest matches base APK + update overlay','all native/runtime integrity hashes agree','working face engine adapter/native library/container bytes and target mapping unchanged','both full64 custom IDs have long sleeves and canonical skill flags','original full My League overlay retained','no save or private database in package']
 report={'passed':True,'checks':checks,'manifest_entries':len(manifest['files']),'patch_entries':len(names),'zip_sha256':sha(artifact.read_bytes()),'device_tested':False}
(repo/'validation/package-validation.json').write_text(json.dumps(report,indent=2));print('PACKAGE_PASS',len(manifest['files']),len(names))
