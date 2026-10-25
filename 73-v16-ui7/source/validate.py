from pathlib import Path
import zipfile,json,hashlib,zlib,struct,re,ast
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
P=Path('/workspace/ronaldo-work/73-ui7');R=Path('/workspace/testingdummy/73-v16-ui7');sha=lambda b:hashlib.sha256(b).hexdigest();entries={}
for f in R.glob('*.zip'):
 with zipfile.ZipFile(f)as z:
  assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
  for n in z.namelist():assert n not in entries;entries[n]=z.read(n)
assert not any(n.endswith(('.db','.sqlite3','.efsave','.pyc'))or'__pycache__'in n for n in entries)
stock=json.loads(Path('/workspace/ronaldo-work/73-inspect/v16-meta/assets/gateway-release/release-manifest.json').read_text());sr={r['path']:r for r in stock['files']};manifest=json.loads(entries['assets/gateway-release/release-manifest.json']);changed=[]
for row in manifest['files']:
 n='assets/gateway-release/'+row['path']
 if n in entries:assert len(entries[n])==row['bytes']and sha(entries[n])==row['sha256'];changed.append(row['path'])
 else:assert row['path']in sr and row==sr[row['path']],row['path']
repair=json.loads(entries['assets/gateway-release/ui6-runtime-manifest.json'])
for row in repair['files']:
 n='assets/gateway-release/'+row['path'];assert n in entries and sha(entries[n])==row['sha256']and len(entries[n])==row['bytes']
assert not any(r['path'].endswith('myleague_editor.json')for r in repair['files']);assert all('assets/gateway-release/livedata/pc9298_mobile_and.'+ext in entries for ext in['pak','utoc','ucas'])
prefix='assets/gateway-release/work/tools/';meta=json.loads(entries[prefix+'noodle_bundle.json'])
for n,h in meta['appearance_files'].items():assert sha(entries[prefix+n])==h,n
assert meta['native_sha256']==sha(entries[prefix+'libnoodle_hair.so']);assert len(meta['target_card_ids'])==19
# All native face, roster, kit, coach restoration and own-team cap fixes remain byte-identical to UI6.
for n,data in entries.items():
 if n.endswith(('.so','.cpk','.pak','.ucas','.utoc'))or n.removeprefix(prefix)in['myleague_custom.json','myleague_73.py','kits_runtime.py','extras_runtime.py','manager_runtime.py','mod_startup.py','noodle_hair.py','select_team_runtime.py','myleague_editor_runtime.py']:
  local=P.parent/'73-ui6/payload'/n.removeprefix('assets/gateway-release/')
  if local.exists():assert local.read_bytes()==data,n
with zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 designer=json.loads(base.read('assets/card-designer/MANIFEST.json'))
 if 'assets/card-designer/MANIFEST.json'in entries:designer=json.loads(entries['assets/card-designer/MANIFEST.json'])
 for n,row in designer.items():
  name='assets/card-designer/'+n;data=entries[name]if name in entries else base.read(name);assert len(data)==row['bytes']and sha(data)==row['sha256'],name
# Loader modification restricted to gateway bootstrap; protected business modules unchanged.
import io
with zipfile.ZipFile(io.BytesIO(entries['assets/chaquopy/app.imy']))as mod,zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy')as original:
 assert set(mod.namelist())==set(original.namelist());delta=[n for n in original.namelist()if mod.read(n)!=original.read(n)];assert delta==['embedded_gateway.pyc'],delta
b=entries['classes5.dex'];assert b[:8]==b'dex\n037\0'and hashlib.sha1(b[32:]).digest()==b[12:32]and zlib.adler32(b[12:])&0xffffffff==struct.unpack_from('<I',b,8)[0]
d=DEX(b);classes={c.get_name():c for c in d.get_classes()};old=DEX(Path('/workspace/ronaldo-work/73-inspect/v16-meta/classes5.dex').read_bytes());assert {c.get_name()for c in old.get_classes()}<=set(classes)
for c in classes.values():
 m=[(v.get_name(),v.get_descriptor())for v in c.get_methods()];assert len(set(m))==len(m)
C='Lorg/efootballrevival/runtimeprobe/'
for cls in['EditorSearch','PlayerSearchIndex','CatalogFilter','BodyEditor','EarthTheme','ModPayloadRepair','ResponsiveUi']:assert C+cls+';'in classes
u=classes[C+'UiStrings;'];assert len(list(u.get_methods()))>5 # Actual original, not compile stub.
assert b'Height / skills'not in b and b'Body & motion'not in b
sm=(P/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali').read_text();assert 'BodyEditor;->attach'in sm and 'EditorSearch;->matchesPrepared'in sm and 'EditorSearch;->fold'in sm and 'CatalogFilter;->refresh'in sm
s=(P/'smali/org/efootballrevival/runtimeprobe/GatewayBootActivity.smali').read_text();render=s[s.index('.method private render(Z)V'):];render=render[:render.index('.end method')];assert render.count('EarthTheme;->apply')==render.count('return-void')
assert 'ModPayloadRepair;->ensure'in(P/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
report={'passed':True,'full_clean_stock_closure':True,'stock_manifest_entries':len(sr),'full_manifest_entries':len(manifest['files']),'gateway_overrides_included':len(changed),'critical_payload_files':len(repair['files']),'two_zip_paths_nonoverlapping':True,'native_UI6_changes_preserved_byte_exact':True,'no_user_save_bundled':True,'loader_only_embedded_gateway_changed':True,'card_designer_manifest_complete_against_stock':True,'original_dex_classes':len(old.get_classes()),'updated_dex_classes':len(classes),'device_tested':False};(P/'package-validation.json').write_text(json.dumps(report,indent=2));print('FULL_PACKAGE_PASS',report)
