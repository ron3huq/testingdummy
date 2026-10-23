from pathlib import Path
import hashlib,json,zipfile
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';sha=lambda b:hashlib.sha256(b).hexdigest()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
for n in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:(out/n).write_bytes((r/n).read_bytes())
native=json.loads((out/'native-validation.json').read_text());assets=json.loads((out/'asset-validation.json').read_text());kits=json.loads((out/'kit-build.json').read_text())
assert len(native['checks'])==752 and native['status']=='V19_NATIVE_UI_COPY_SCOPES_SECONDARY_HEAD_RESTORE_PASS'
assert assets['unchanged_v18_chunks']==299 and assets['new_uniform_chunks']==2 and assets['independent_ETC2_readback_pixel_match']
assert assets['container_sha256']==sha((out/'container/pc9298_mobile_and.ucas').read_bytes())
assert native['font_paths_sizes_and_config_unchanged'] and native['depth_bit_generated_setter_original_body_executed'] and native['common_head_main_and_cast_shadow_setters_original_body_executed']
for ext in ['pak','utoc','ucas']:assert (out/'container'/('pc9298_mobile_and.'+ext)).read_bytes()==(deploy/'livedata'/('pc9298_mobile_and.'+ext)).read_bytes()
for n in ['noodle_hair.py','libnoodle_hair.so']:assert (r/n).read_bytes()==(deploy/'work/tools'/n).read_bytes()
with zipfile.ZipFile(out.parent/'player-faces-v18/Faces-v18-13-cards.zip') as z:
 for n in ['gateway_runtime.py','libselect_team.so','select_team_runtime.py','myleague_editor_runtime.py']:assert z.read('work/tools/'+n)==(deploy/'work/tools'/n).read_bytes()
for p in r.glob('*.py'):compile(p.read_bytes(),str(p),'exec')
name='Faces-v19-13-cards-Sparta-kits.zip'
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in files:z.write(deploy/n,n)
 z.write(out/'HUONG_DAN.md','HUONG_DAN.md')
with zipfile.ZipFile(out/name) as z:
 assert z.testzip() is None and set(z.namelist())==set(files+['HUONG_DAN.md']) and len(z.read('work/tools/gateway_runtime.py'))==2441
 meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['native_sha256']==native['hook_sha256']==sha(z.read('work/tools/libnoodle_hair.so')) and meta['native_sha256'] in z.read('work/tools/noodle_hair.py').decode()
 assert meta['version']=='player-faces-v19-common-head-card-clubs' and len(meta['target_card_ids'])==13
 for n,row in meta['files'].items():
  data=z.read('livedata/'+n);assert len(data)==row['size'] and sha(data)==row['sha256']
 for n,expected in meta['appearance_files'].items():assert sha(z.read('work/tools/'+n))==expected
report={'status':'V19_COMPLETE_BUNDLE_CHECKSUMS_CRC_752_NATIVE_14_INSTALLS_TWO_KITS_PASS','installed_files':11,'native_cases':752,'Python_install_paths':14,'all_v18_face_hair_card_asset_chunks_unchanged':299,'only_new_asset_chunks':'Sparta351p1,p2 Uni_D','common_head_guard_scope':'four failing cards; named native common face attachment only; main/depth/shadow suppression with original-state restoration','card_ui_club_scope':'six Vietnam cards no-club/no-league; Speed AlNassr18961 Portugal228','all_visual_changes_device_verified':False,'black_face_cure_device_verified':False,'native_sha256':native['hook_sha256'],'artifacts':{name:{'bytes':(out/name).stat().st_size,'sha256':sha((out/name).read_bytes())}}};(out/'package-validation.json').write_text(json.dumps(report,indent=2))
source=[p for p in r.iterdir() if p.suffix in ['.py','.c','.sh','.txt']]+list(out.glob('*.md'))+list(out.glob('*.json'))+[p for p in (out/'references').rglob('*') if p.is_file()]+[p for p in (out/'reader-logs').rglob('*') if p.is_file()]+list((out/'kit-inputs').glob('*.ftex'))+list((out/'kit-previews').glob('*.png'))
with zipfile.ZipFile(out/'Faces-v19-source-and-research.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(source):z.write(p,p.relative_to(out))
with zipfile.ZipFile(out/'Faces-v19-source-and-research.zip') as z:
 assert z.testzip() is None and len([n for n in z.namelist() if n.endswith('.ftex')])==2
names=[name,'Faces-v19-source-and-research.zip'];(out/'SHA256SUMS').write_text(''.join(sha((out/n).read_bytes())+'  '+n+'\n' for n in names));print(json.dumps(report,indent=2))
