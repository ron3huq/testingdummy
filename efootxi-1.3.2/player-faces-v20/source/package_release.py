"""Package only complete, checked deploy files. Tests are host/asset checks;
Android visual success is deliberately not advertised.
"""
from pathlib import Path
import hashlib,json,zipfile
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';sha=lambda b:hashlib.sha256(b).hexdigest()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
for n in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:(out/n).write_bytes((r/n).read_bytes())
native=json.loads((out/'native-validation.json').read_text());assets=json.loads((out/'asset-validation.json').read_text());kits=json.loads((out/'kit-build.json').read_text());art=json.loads((out/'card-art-validation.json').read_text());repro=json.loads((out/'rebuild-reproducibility.json').read_text())
assert native['status']=='V20_NATIVE_SCOPE_POSITIONS_OZIL_EDITOR_PASS'and len(native['checks'])>=791
assert assets['status']=='V20_INDEPENDENT_MESH_CARD_FONT_CONTAINER_VALIDATION_PASS'and len(assets['new_mesh_LODs'])==22 and assets['glyph_assets_original_EAC_alpha_exact']==32 and len(assets['card_textures_independent_pixel_match'])==12
assert assets['approved_prior_head_hair_chunks_byte_identical']==187 and assets['container_sha256']==repro['ucas_sha256']==sha((out/'container/pc9298_mobile_and.ucas').read_bytes())
assert len(kits['kits'])==8 and art['count']==12 and native['font_paths_sizes_and_config_unchanged']
assert json.loads((out/'hook-install-validation.json').read_text())['fifteen_full_python_install_paths_executed']
for ext in ['pak','utoc','ucas']:assert (out/'container'/('pc9298_mobile_and.'+ext)).read_bytes()==(deploy/'livedata'/('pc9298_mobile_and.'+ext)).read_bytes()
for n in ['noodle_hair.py','libnoodle_hair.so','myleague_editor_runtime.py']:assert (r/n).read_bytes()==(deploy/'work/tools'/n).read_bytes()
pins=json.loads((out/'references/pinned-runtime.json').read_text())
for n in ['libselect_team.so','select_team_runtime.py']:assert sha((deploy/'work/tools'/n).read_bytes())==pins['appearance/'+n]
assert len((deploy/'work/tools/gateway_runtime.py').read_bytes())==2441 and sha((deploy/'work/tools/gateway_runtime.py').read_bytes())==pins['gateway_runtime.py']
for p in r.glob('*.py'):compile(p.read_bytes(),str(p),'exec')
name='Faces-v20-14-cards-4-teams.zip'
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n in files:z.write(deploy/n,n)
 z.write(out/'HUONG_DAN.md','HUONG_DAN.md')
with zipfile.ZipFile(out/name)as z:
 assert z.testzip()is None and set(z.namelist())==set(files+['HUONG_DAN.md']);meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['native_sha256']==native['hook_sha256']==sha(z.read('work/tools/libnoodle_hair.so'))and meta['native_sha256']in z.read('work/tools/noodle_hair.py').decode();assert meta['version']=='player-faces-v20-source-topology-kits'and len(meta['target_card_ids'])==14
 for n,row in meta['files'].items():
  b=z.read('livedata/'+n);assert len(b)==row['size']and sha(b)==row['sha256']
 for n,expected in meta['appearance_files'].items():assert sha(z.read('work/tools/'+n))==expected
report={'status':'V20_INSTALL_ZIP_HASHES_CRC_NATIVE_SCOPES_15_INSTALL_PATHS_ASSET_READBACK_PASS','installed_files':11,'native_cases':len(native['checks']),'Python_install_paths':15,'new_head_LODs_validated':22,'approved_head_hair_chunks_byte_identical':187,'glyph_alpha_assets_byte_preserved':32,'kits':8,'kit_preview_textures':16,'card_portrait_textures':12,'native_sha256':native['hook_sha256'],'artifacts':{name:{'bytes':(out/name).stat().st_size,'sha256':sha((out/name).read_bytes())}},'device_verified':False,'black_face_fixed_on_android_verified':False,'latest_original_Konami_Big_Time_background_verified':False};(out/'package-validation.json').write_text(json.dumps(report,indent=2))
source=[p for p in r.iterdir()if p.suffix in ['.py','.c','.sh','.txt']]+list(out.glob('*.md'))+list(out.glob('*.json'))+[out/'Card-layout-preview.png']
for folder in ['references','reader-logs','original-inputs','kit-previews','art']:
 for p in (out/folder).rglob('*'):
  if not p.is_file():continue
  if folder=='references'and p.parent.name=='sparta-inputs'and p.suffix=='.png':continue # rebuilt from included FTEX
  source.append(p)
source_name='Faces-v20-source-and-research.zip'
with zipfile.ZipFile(out/source_name,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for p in sorted(set(source)):z.write(p,p.relative_to(out))
with zipfile.ZipFile(out/source_name)as z:
 assert z.testzip()is None and len([p for p in z.namelist()if p.startswith('original-inputs/')and p.endswith('.rar')])==6
for n in [name,source_name]:assert (out/n).stat().st_size<100*1024*1024
(out/'SHA256SUMS').write_text(''.join(sha((out/n).read_bytes())+'  '+n+'\n'for n in [name,source_name]));print(json.dumps(report,indent=2));print('SOURCE_ZIP_BYTES',(out/source_name).stat().st_size)
