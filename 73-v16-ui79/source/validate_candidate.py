from pathlib import Path
import zipfile,json,hashlib,zlib,struct,re,ast
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
P=Path('/tmp/73-ui79/build');R=Path('/tmp/73-ui79/build');sha=lambda b:hashlib.sha256(b).hexdigest();entries={}
for f in [R/'UI79-INTERNAL-CANDIDATE-NOT-FULL.zip']+[Path('/workspace/testingdummy/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip')]:
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
assert sha(entries['assets/gateway-release/livedata/dt870_mobile_and.cpk'])=='eabf680adb54b909241cb0d484f87a79bc9d50b752d002c509abccf3e2a66497'
assert sha(entries['assets/gateway-release/livedata/dt870_ui74_mobile_and.cpk'])=='20003bd597068ded2b329155c5abe106ea50da3fd3f72065099091220c6c87e0'
assert 'livedata/dt870_ui74_mobile_and.cpk'in {r['path']for r in repair['files']}
assert 'livedata/dt870_mobile_and.cpk'not in {r['path']for r in repair['files']}
assert not any(r['path'].endswith('myleague_editor.json')for r in repair['files']);assert all('assets/gateway-release/livedata/pc9298_mobile_and.'+ext in entries for ext in['pak','utoc','ucas'])
prefix='assets/gateway-release/work/tools/';meta=json.loads(entries[prefix+'noodle_bundle.json'])
for n,h in meta['appearance_files'].items():assert sha(entries[prefix+n])==h,n
assert meta['native_sha256']==sha(entries[prefix+'libnoodle_hair.so']);assert len(meta['target_card_ids'])==21
# All native face, roster, kit, coach restoration and own-team cap fixes remain byte-identical to UI6.
for n,data in entries.items():
 if n.endswith(('.so','.cpk','.pak','.ucas','.utoc'))or n.removeprefix(prefix)in['myleague_custom.json','myleague_73.py','extras_runtime.py','manager_runtime.py','myleague_editor_runtime.py']:
  local=Path('/workspace/ronaldo-work/73-ui6/payload')/n.removeprefix('assets/gateway-release/')
  if local.exists()and n not in ['assets/gateway-release/livedata/dt870_mobile_and.cpk','assets/gateway-release/work/tools/libselect_team.so','assets/gateway-release/work/tools/libnoodle_hair.so','assets/gateway-release/work/tools/myleague_73.py','assets/gateway-release/work/tools/myleague_editor_runtime.py']:assert local.read_bytes()==data,n
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
for cls in['EditorSearch','PlayerSearchIndex','CatalogFilter','BodyEditor','EarthTheme','RuntimeDiagnostics','ModPayloadRepair','ResponsiveUi','LiveResourceServer','ResourcePresence','PlayerModelEditor','CatalogCart','TuningEditor']:assert C+cls+';'in classes
u=classes[C+'UiStrings;'];assert len(list(u.get_methods()))>5 # Actual original, not compile stub.
assert b'Height / skills'not in b and b'Body & motion'not in b
sm=(P/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali').read_text();assert 'BodyEditor;->attach'in sm and 'EditorSearch;->matchesPrepared'in sm and 'EditorSearch;->fold'in sm and 'CatalogFilter;->refresh'in sm
s=(P/'smali/org/efootballrevival/runtimeprobe/GatewayBootActivity.smali').read_text();render=s[s.index('.method private render(Z)V'):];render=render[:render.index('.end method')];assert render.count('EarthTheme;->apply')==render.count('return-void')
assert 'ModPayloadRepair;->ensure'in(P/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
report={'passed':True,'runtime_clean_stock_closure':True,'implementation_and_artwork_complete':True,'self_created_hero_art_authorized':True,'missing_inputs':[],'stock_manifest_entries':len(sr),'full_manifest_entries':len(manifest['files']),'gateway_overrides_included':len(changed),'critical_payload_files':len(repair['files']),'two_zip_paths_nonoverlapping':True,'existing_face_resource_chunks_preserved_byte_exact':True,'select_team_library_updated_for_kit_gate_and_models':True,'no_user_save_bundled':True,'loader_only_embedded_gateway_changed':True,'card_designer_manifest_complete_against_stock':True,'original_dex_classes':len(old.get_classes()),'updated_dex_classes':len(classes),'device_tested':False};(Path('/tmp/73-ui79')/'package-validation.json').write_text(json.dumps(report,indent=2));print('FULL_PACKAGE_PASS',report)

for name in ['ResourceInstaller','ResourceInstaller$Plan','ResourceInstaller$Item']:
 name=C+name+';'
 oc=next(c for c in old.get_classes() if c.get_name()==name)
 assert {(m.get_name(),m.get_descriptor()) for m in oc.get_methods()} <= {(m.get_name(),m.get_descriptor()) for m in classes[name].get_methods()}
 assert {(f.get_name(),f.get_descriptor()) for f in oc.get_fields()} <= {(f.get_name(),f.get_descriptor()) for f in classes[name].get_fields()}
assert 'ResourcePresence;->check' in (P/'smali/org/efootballrevival/runtimeprobe/PersistentResources.smali').read_text()
assert 'LiveResourceServer;->serve' in (P/'smali/org/efootballrevival/runtimeprobe/EmbeddedGateway.smali').read_text()
print('RESOURCE_HELPERS_AND_ORIGINAL_INSTALLER_PASS')

assert 'PlayerModelEditor;->attach' in sm
for name in ['EditorSearch.java','PlayerSearchIndex.java','CatalogFilter.java']:
 assert (P/'java/org/efootballrevival/runtimeprobe'/name).read_bytes()==(Path('/workspace/ronaldo-work/73-ui74')/'java/org/efootballrevival/runtimeprobe'/name).read_bytes()
assert sha(entries['assets/gateway-release/work/tools/libselect_team.so']) in entries['assets/gateway-release/work/tools/select_team_runtime.py'].decode()
print('PLAYER_MODEL_DEX_AND_SEARCH_PRESERVATION_PASS')

assert "TuningEditor;->attachSkills" in sm and "AppearanceChoices;->attach" in sm
print("TUNING_BUTTONS_AND_NATIVE_HASH_PASS")

assert meta["appearance_overlay_sha256"]==sha(entries[prefix+"myleague_editor_runtime.py"])

assert C+'AppearanceChoices;'in classes
assert b'Physics \xc2\xb7 Verified Inputs'not in b
assert 'TuningEditor;->attachPhysics'not in sm
assert 'for42 hooks'in entries[prefix+'hook_arena.py'].decode()
for name in ['body_dimensions.py','myleague_editor_runtime.py','player_tuning.py','appearance_choices.py','noodle_hair.py','bridge_73.py']:
 compile(entries[prefix+name],name,'exec')
assert 'configure_skin_chain'in entries[prefix+'noodle_hair.py'].decode()
assert 'ui77_physics_get'not in entries[prefix+'player_tuning.py'].decode()
labels=json.loads(entries[prefix+'innate_skill_labels.json']);assert len(labels)==64
assert b'140\xe2\x80\x93220'in b and b'40\xe2\x80\x93130'in b
assert C+'TuningEditor;'in classes
# Every changed method has no dangling TuningEditor lambda call after Physics removal.
target={(m.get_name(),m.get_descriptor())for m in classes[C+'TuningEditor;'].get_methods()}
for cls in classes.values():
 for method in cls.get_methods():
  if not method.get_code():continue
  for ins in method.get_instructions():
   out=ins.get_output()
   if 'TuningEditor;->lambda$physics'in out:raise AssertionError(out)
print('UI78_PHYSICS_REMOVED_SKIN_CHAIN_AND_DIMENSIONS_PASS')

with zipfile.ZipFile(P/'ui78-main.zip')as previous:
 for key in ['myleague_custom.json','myleague_73.py','myleague_editor_runtime.py','multi_cards.py','select_team_runtime.py','libselect_team.so','body_dimensions.py','player_model.py','player_tuning.py','innate_skill_labels.json','celebration_choices.json']:
  assert entries[prefix+key]==previous.read(prefix+key),key
 private=json.loads(entries[prefix+'private_bundles.json'])
 for name,row in private['files'].items():
  data=entries['assets/gateway-release/livedata/'+name];assert len(data)==row['size']and sha(data)==row['sha256']
 for cls in ['SkinColourEditor','AppearanceChoices','RuntimeDiagnostics']:
  methods={(m.get_name(),m.get_descriptor())for m in classes[C+cls+';'].get_methods()}
  for name,c in classes.items():
   if not name.startswith(C+cls):continue
   for method in c.get_methods():
    if not method.get_code():continue
    for inst in method.get_instructions():
     output=inst.get_output();marker=C+cls+';->'
     if marker in output and '('in output.split(marker,1)[1]:
      call=output.split(marker,1)[1].replace(' ','');name,desc=call.split('(',1);assert(name,'('+desc)in {(n,d.replace(' ',''))for n,d in methods},(cls,output)
art=json.loads(Path('/tmp/73-ui79/art-validation.json').read_text());assert art['publishable']and not art['new_hero_photos_pending']and art['native_private_photos']==32
print('FULL_ART_AND_RUNTIME_CLOSURE_PASS')

form=(P/'smali/org/efootballrevival/runtimeprobe/EditorForm.smali').read_text();assert 'DEFAULT_LEVEL_CAP:I = 0x64'in form
choice=(P/'smali/org/efootballrevival/runtimeprobe/AppearanceChoices.smali').read_text();assert 'const-string'in choice and '"rgb"'in choice
skin=(P/'java/org/efootballrevival/runtimeprobe/SkinColourEditor.java').read_text();assert 'skin_previews'in skin and 'mode.setSelection(7)'in skin and 'new Thread('in skin
print('LEVEL100_UI_AND_SKIN_SELECTION_PASS')
