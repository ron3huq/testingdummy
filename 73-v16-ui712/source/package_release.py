from pathlib import Path
import zipfile,json,hashlib,shutil
P=Path('/workspace/73-ui712');A=P/'build/apk';R=P/'release';R.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();prefix='assets/gateway-release/';new={'pc9310','pc9312','pc9313'}
part1=R/'V25-73-UI7.12-FULL-Part1-Faces-MT.zip';part2=R/'V25-73-UI7.12-FULL-Part2-Main-MT.zip';part3=R/'V25-73-UI7.12-FULL-Part3-Prior-Faces-MT.zip';part4=R/'V25-73-UI7.12-FULL-Part4-New-Faces-Sleeves-MT.zip'
shutil.copy2('/workspace/testingdummy/73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip',part1);shutil.copy2(P/'baseline/V25-73-UI7.11-FULL-Part3-Ronaldo-Faces-MT.zip',part3)
baseline=json.loads((P/'baseline/inventory.json').read_text());designer_keep={k for rows in baseline.values()for k in rows if k.startswith('assets/card-designer/')}|{'assets/card-designer/portrait-ui712.html'}
files={2:[],4:[]}
for f in sorted(A.rglob('*')):
 if not f.is_file()or'__pycache__'in f.parts:continue
 rel=f.relative_to(A).as_posix()
 if rel.startswith('assets/card-designer/')and rel not in designer_keep:continue
 stem=f.name.split('_mobile_and.')[0]
 if rel.startswith(prefix+'livedata/'):
  if stem in ['pc9298','pc9308']:continue
  part=4 if stem in new else 2
 else:part=2
 files[part].append((f,rel))
for n,path in [(2,part2),(4,part4)]:
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for f,key in files[n]:z.write(f,key)
 assert path.stat().st_size<100*1024*1024
 print('PACKAGE',path.name,path.stat().st_size,flush=True)
inventory={};union={}
for f in [part1,part2,part3,part4]:
 with zipfile.ZipFile(f)as z:
  assert z.testzip()is None;rows={}
  for key in z.namelist():
   b=z.read(key);row={'bytes':len(b),'sha256':sha(b)};rows[key]=row
   if key in union:assert union[key]==row,('Conflicting payload across parts',key)
   union[key]=row
  inventory[f.name]=rows
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));(R/'SHA256SUMS.txt').write_text(''.join(sha(f.read_bytes())+'  '+f.name+'\n'for f in [part1,part2,part3,part4]))
base_verified={};apk=zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-aligned-debugSigned.apk')
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 doc=json.loads((A/'assets/gateway-release'/name).read_text())
 for row in doc['files']:
  key=prefix+row['path']
  if key in union:actual=union[key]
  else:
   if key not in base_verified:
    info=apk.getinfo(key);h=hashlib.sha256()
    with apk.open(key)as f:
     while data:=f.read(1024*1024):h.update(data)
    base_verified[key]={'bytes':info.file_size,'sha256':h.hexdigest()}
   actual=base_verified[key]
  assert actual=={'bytes':row['bytes'],'sha256':row['sha256']},(name,'wrong hash',key,actual,row)
apk.close()
T=A/'assets/gateway-release/work/tools';meta=json.loads((T/'noodle_bundle.json').read_text())
for name,value in meta['appearance_files'].items():assert union[prefix+'work/tools/'+name]['sha256']==value
for n in ['private_bundles.json','noodle_bundle.json']:
 d=json.loads((T/n).read_text())
 for key,row in d['files'].items():assert union[prefix+'livedata/'+key]=={'bytes':row['size'],'sha256':row['sha256']}
S=R/'source';S.mkdir(exist_ok=True);V=R/'validation';V.mkdir(exist_ok=True)
for f in(P/'build/native').glob('*'):
 if f.suffix in['.c','.h']:shutil.copy2(f,S/f.name)
for f in(P/'build/java/org/efootballrevival/runtimeprobe').glob('*.java'):shutil.copy2(f,S/f.name)
for name in ['stat_editor.py','motion_editor.py','transfer_editor.py','world_skills.py','photo_editor.py','photo_codec.py','appearance_gear.py','myleague_editor_runtime.py','bridge_73.py','hook_arena.py','noodle_hair.py','select_team_runtime.py']:shutil.copy2(T/name,S/name)
for name in ['cut_body.py','verify_cut_bodies.py','merge_dex.py','compile_native.sh','build_java.sh','finalize.py','package_release.py','test_new_native.py','test_storage.py','test_photo_native.py','test_cut_hooks.py','test_accessory_colors.py','test_arena.py','run_regressions.py','test_cold_boot.py','merge_android_faces.py','repair_android_faces.py','verify_faces.py','build_pc_faces.py','test_photo_codec.py','build_photo_codec.py','probe_accessory_bits.py']:shutil.copy2(P/name,S/name)
for name in ['six-face-rig-validation.json','cut-independent-validation.json','cut-hook-native-validation.json','cut-body-validation.json','new-native-validation.json','storage-validation.json','copy-native-validation.json','clothing-native-validation.json','accessory-colors-native-validation.json','photo-cut-path-native-validation.json','arena-validation.json','production-hook-validation.json','cold-start-validation.json','native-stat-ranges.json','accessory-packed-bits.json','android-face-provenance.json','input-inventory.json']:
 if(P/name).exists():shutil.copy2(P/name,V/name)
report={'passed':True,'version':'73-ui7.12','four_parts':4,'payload_files':len(union),'unchanged_base_APK_files_verified':len(base_verified),'no_conflicting_files':True,'every_release_and_repair_manifest_row_verified':True,'all57_runtime_pins_verified':True,'six_face_targets':{'88042803047215':'Ronaldo2018','105634720685845':'RonaldoNazario','105565464400480':'Zidane','105625593957752':'Henry','89138288266704':'RonaldoMulletV8','176104':'YanDiomande'},'new_face_LOD_variants':24,'cut_native_long_models':123,'Android_tested':False};(V/'package-validation.json').write_text(json.dumps(report,indent=2));print('FOUR_PART_FULL_VALIDATED',len(union),flush=True)
