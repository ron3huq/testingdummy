from pathlib import Path
import json,zipfile,hashlib,struct,zlib,io,re
from loguru import logger
logger.remove()
from androguard.core.dex import DEX
P=Path('/tmp/73-ui710');B=P/'build';sha=lambda b:hashlib.sha256(b).hexdigest();base='assets/gateway-release/';prefix=base+'work/tools/';entries={}
for f in [B/'UI710-INTERNAL-CANDIDATE-NOT-FULL.zip',Path('/workspace/testingdummy/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip')]:
 with zipfile.ZipFile(f)as z:
  assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
  for n in z.namelist():assert n not in entries;entries[n]=z.read(n)
assert not any(n.endswith(('.db','.sqlite3','.efsave','.pyc'))or'__pycache__'in n for n in entries)
stock=json.loads(Path('/workspace/ronaldo-work/73-inspect/v16-meta/assets/gateway-release/release-manifest.json').read_text());sr={r['path']:r for r in stock['files']};manifest=json.loads(entries[base+'release-manifest.json']);repair=json.loads(entries[base+'ui6-runtime-manifest.json'])
for d in [manifest,repair]:
 paths=[r['path']for r in d['files']];assert len(set(paths))==len(paths)
 for row in d['files']:
  key=base+row['path']
  if key in entries:assert len(entries[key])==row['bytes']and sha(entries[key])==row['sha256'],key
  else:assert d is manifest and row==sr[row['path']],row
assert sha(entries[base+'livedata/dt870_mobile_and.cpk'])=='eabf680adb54b909241cb0d484f87a79bc9d50b752d002c509abccf3e2a66497'
assert sha(entries[base+'livedata/dt870_ui74_mobile_and.cpk'])=='20003bd597068ded2b329155c5abe106ea50da3fd3f72065099091220c6c87e0'
assert not any(r['path'].endswith(('myleague_editor.json','livedata/dt870_mobile_and.cpk'))for r in repair['files'])
meta=json.loads(entries[prefix+'noodle_bundle.json']);assert len(meta['target_card_ids'])==23
for n,h in meta['appearance_files'].items():assert sha(entries[prefix+n])==h,n
assert meta['native_sha256']==sha(entries[prefix+'libnoodle_hair.so']);assert meta['appearance_overlay_sha256']==sha(entries[prefix+'myleague_editor_runtime.py'])
assert sha(entries[prefix+'libselect_team.so'])in entries[prefix+'select_team_runtime.py'].decode()
private=json.loads(entries[prefix+'private_bundles.json']);assert len(private['files'])==9
for n,r in private['files'].items():data=entries[base+'livedata/'+n];assert len(data)==r['size']and sha(data)==r['sha256']
for name in ['custom_skin.py','skin_iostore.py','skin_templates.zlib']:assert prefix+name not in entries and name not in meta['appearance_files']
assert 'custom_skin'not in entries[prefix+'bridge_73.py'].decode();assert 'entry=0x39ca65c'not in entries[prefix+'noodle_hair.py'].decode()
with zipfile.ZipFile(io.BytesIO(entries['assets/chaquopy/app.imy']))as mod,zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy')as original:
 assert set(mod.namelist())==set(original.namelist());assert [n for n in original.namelist()if mod.read(n)!=original.read(n)]==['embedded_gateway.pyc']
b=entries['classes5.dex'];assert b[:8]==b'dex\n037\0'and hashlib.sha1(b[32:]).digest()==b[12:32]and zlib.adler32(b[12:])&0xffffffff==struct.unpack_from('<I',b,8)[0]
dex=DEX(b);classes={c.get_name():c for c in dex.get_classes()};original=DEX(Path('/workspace/ronaldo-work/73-inspect/v16-meta/classes5.dex').read_bytes());assert {c.get_name()for c in original.get_classes()}<=set(classes);C='Lorg/efootballrevival/runtimeprobe/'
for name in ['EquipmentEditor','SkinColourEditor','AppearanceChoices','EditorSearch','PlayerSearchIndex','CatalogFilter','BodyEditor','EarthTheme','RuntimeDiagnostics','ModPayloadRepair','ResponsiveUi','LiveResourceServer','ResourcePresence','PlayerModelEditor','CatalogCart','TuningEditor']:assert C+name+';'in classes
for cls in classes.values():
 methods=[(m.get_name(),m.get_descriptor())for m in cls.get_methods()];assert len(methods)==len(set(methods))
 for m in cls.get_methods():
  if not m.get_code():continue
  for ins in m.get_instructions():
   output=ins.get_output()
   if '->'not in output or '('not in output:continue
   for name in ['EquipmentEditor','SkinColourEditor','AppearanceChoices','TuningEditor']:
    marker=C+name+';->'
    if marker in output:
     tail=output.split(marker,1)[1].replace(' ','');n,desc=tail.split('(',1);assert(n,'('+desc)in{(x.get_name(),x.get_descriptor().replace(' ',''))for x in classes[C+name+';'].get_methods()},output
S=B/'smali/org/efootballrevival/runtimeprobe';sm=(S/'PlayerEditorPanel.smali').read_text()
for name in ['BodyEditor;->attach','EditorSearch;->matchesPrepared','EditorSearch;->fold','CatalogFilter;->refresh','PlayerModelEditor;->attach','TuningEditor;->attachSkills','AppearanceChoices;->attach']:assert name in sm
assert 'EquipmentEditor;->attach'in(S/'AppearanceChoices.smali').read_text();assert 'DEFAULT_LEVEL_CAP:I = 0x64'in(S/'EditorForm.smali').read_text()
assert b'Custom RGB'not in b and b'Physics \xc2\xb7 Verified Inputs'not in b
for n in ['EditorSearch.java','PlayerSearchIndex.java','CatalogFilter.java']:assert(B/'java/org/efootballrevival/runtimeprobe'/n).read_bytes()==(Path('/workspace/ronaldo-work/73-ui74/java/org/efootballrevival/runtimeprobe')/n).read_bytes()
with zipfile.ZipFile('/tmp/73-ui79/publish/73-v16-ui79/V25-73-UI7.9-FULL-Part2-Main-MT.zip')as previous:
 for n in ['myleague_custom.json','myleague_73.py','multi_cards.py','body_dimensions.py','player_model.py','player_tuning.py','innate_skill_labels.json','celebration_choices.json','level100.py']:
  assert entries[prefix+n]==previous.read(prefix+n),n
for n,data in entries.items():
 if n.endswith('.py'):compile(data,n,'exec')
assert len(json.loads(entries[prefix+'innate_skill_labels.json']))==64
report={'passed':True,'clean_APK_manifest_closure_verified':True,'repair_manifest_verified':True,'Part1_and_Main_paths_nonoverlapping':True,'native_and_resource_SHA_pins_verified':True,'original_dex_classes':len(original.get_classes()),'updated_dex_classes':len(classes),'DEX_helper_references_verified':True,'no_user_saves_bundled':True,'old_face_pack_unchanged':True,'search_code_byte_identical':True,'level100_and_prior_leagues_preserved':True,'custom_RGB_removed':True,'native_skin_palette_only':True,'new_private_resource_files':9,'device_tested':False,'Ronaldo_2008_actual_modded_head_extraction_complete':False,'AI_portrait_generated':False,'artwork_fallback':'Offline portraits rendered from supplied exact3Dmodels, hand-designed backgrounds'};(P/'package-validation.json').write_text(json.dumps(report,indent=2));print('FULL_PACKAGE_PASS',report)
