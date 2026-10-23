from pathlib import Path
import hashlib,json,zipfile
r=Path(__file__).resolve().parent;out=r.parent;deploy=r/'deploy';sha=lambda b:hashlib.sha256(b).hexdigest()
files=['work/tools/'+n for n in ['gateway_runtime.py','noodle_hair.py','libnoodle_hair.so','noodle_hair.json','noodle_bundle.json','myleague_editor_runtime.py','select_team_runtime.py','libselect_team.so']]+['livedata/pc9298_mobile_and.'+e for e in ['pak','utoc','ucas']]
for n in ['native-validation.json','hook-install-validation.json','runtime-validation.json']:(out/n).write_bytes((r/n).read_bytes())
native=json.loads((out/'native-validation.json').read_text());assets=json.loads((out/'asset-validation.json').read_text());assert len(native['checks'])==680;assert len(assets['meshes'])==10 and assets['unchanged_chunks']==209
assert native['font_paths_sizes_and_config_unchanged'] and native['native_no_club_setter_body_executed'] and native['original_font_glyph_metrics_executed']
assert assets['container_sha256']==sha((out/'container/pc9298_mobile_and.ucas').read_bytes())
for ext in ['pak','utoc','ucas']:assert (out/'container'/('pc9298_mobile_and.'+ext)).read_bytes()==(deploy/'livedata'/('pc9298_mobile_and.'+ext)).read_bytes()
for n in ['noodle_hair.py','libnoodle_hair.so']:assert (r/n).read_bytes()==(deploy/'work/tools'/n).read_bytes()
# Selector/sleeve/body appearance overlay is the same already-shipped baseline.
with zipfile.ZipFile(out.parent/'player-faces-v17/Faces-v17-jersey-nationality.zip') as z:
 for n in ['gateway_runtime.py','libselect_team.so','select_team_runtime.py','myleague_editor_runtime.py']:assert z.read('work/tools/'+n)==(deploy/'work/tools'/n).read_bytes()
for p in r.glob('*.py'):compile(p.read_bytes(),str(p),'exec')
name='Faces-v18-13-cards.zip'
with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in files:z.write(deploy/n,n)
 z.write(out/'HUONG_DAN.md','HUONG_DAN.md')
with zipfile.ZipFile(out/name) as z:
 assert z.testzip() is None and set(z.namelist())==set(files+['HUONG_DAN.md']);assert len(z.read('work/tools/gateway_runtime.py'))==2441
 meta=json.loads(z.read('work/tools/noodle_bundle.json'));assert meta['native_sha256']==native['hook_sha256']==sha(z.read('work/tools/libnoodle_hair.so'));assert meta['native_sha256'] in z.read('work/tools/noodle_hair.py').decode()
 assert meta['version']=='player-faces-v18-working-template-club-shirts' and len(meta['target_card_ids'])==13
 for n,row in meta['files'].items():
  data=z.read('livedata/'+n);assert len(data)==row['size'] and sha(data)==row['sha256']
 for n,expected in meta['appearance_files'].items():assert sha(z.read('work/tools/'+n))==expected
report={'status':'V18_COMPLETE_BUNDLE_HASHES_CRC_NATIVE_GLYPHS_NOCLUB_REBASED_LODS_PASS','installed_files':11,'native_cases':680,'independent_rebased_meshes':10,'independent_rebased_LODs':20,'approved_asset_chunks_unchanged':209,'all_rebased_LOD_bytes_reference_skeleton_and_bind_pose_preserved':True,'original_face_texture_mip_bulk_payloads_preserved':True,'font_assets_and_layout_config_untouched':True,'vietnam_club_clear_exact_cards':6,'phone_control_ND06_on_four_failing_cards_user_confirmed':True,'v18_renderer_and_black_face_fix_device_verified':False,'v18_jersey_and_club_UI_device_verified':False,'native_sha256':native['hook_sha256'],'artifacts':{name:{'bytes':(out/name).stat().st_size,'sha256':sha((out/name).read_bytes())}}};(out/'package-validation.json').write_text(json.dumps(report,indent=2))
source=[p for p in r.iterdir() if p.suffix in ['.py','.c','.sh']]+list(out.glob('*.md'))+list(out.glob('*.json'))+[p for p in (out/'references').rglob('*') if p.is_file()]+[p for p in (out/'reader-logs').rglob('*') if p.is_file()]
with zipfile.ZipFile(out/'Faces-v18-source-and-research.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(source):z.write(p,p.relative_to(out))
with zipfile.ZipFile(out/'Faces-v18-source-and-research.zip') as z:assert z.testzip() is None
names=[name,'Faces-v18-source-and-research.zip'];(out/'SHA256SUMS').write_text(''.join(sha((out/n).read_bytes())+'  '+n+'\n' for n in names));print(json.dumps(report,indent=2))
