from pathlib import Path
import json,hashlib,zipfile,shutil,difflib
P=Path('/workspace/ronaldo-work/73-ui6');repo=Path('/workspace/testingdummy/73-v16-ui6');src=repo/'source';src.mkdir(parents=True,exist_ok=True);sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
# Never publish failed synthetic-test snapshots as on-device runtime status.
for f in(P/'payload/work/tools').glob('*status.json'):f.write_text(json.dumps({'state':'PENDING_DEVICE_START','version':'73-ui6','phone_verified':False},indent=2))
manifest=json.loads(Path('/workspace/ronaldo-work/73-ui5/release-manifest.json').read_text());remove={'coach_changes.py','rolled_runtime.py','rolled_bundle.json'};rows={r['path']:r for r in manifest['files']if Path(r['path']).name not in remove and not any(s in r['path']for s in['pc9299_mobile_and.','pc9301_mobile_and.'])}
for f in(P/'payload').rglob('*'):
 if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':
  n=f.relative_to(P/'payload').as_posix();rows[n]={'path':n,'bytes':f.stat().st_size,'sha256':sha(f)}
manifest['release_id']='73-v16-v25-ui6-persistent-native-sleeves-y08-20261025';manifest['files']=list(rows.values());(P/'release-manifest.json').write_text(json.dumps(manifest,indent=2))
entries={'classes5.dex':P/'classes5.dex','assets/gateway-release/release-manifest.json':P/'release-manifest.json'}
for folder,prefix in[(P/'payload','assets/gateway-release/'),(P/'apk-assets','')]:
 for f in folder.rglob('*'):
  if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':entries[prefix+f.relative_to(folder).as_posix()]=f
out=repo/'V25-73-UI6-Persistent-NativeSleeves-Y08-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,f in sorted(entries.items()):z.write(f,n)
with zipfile.ZipFile(out)as z:assert z.testzip()is None
(repo/'inventory.json').write_text(json.dumps({n:{'bytes':f.stat().st_size,'sha256':sha(f)}for n,f in sorted(entries.items())},indent=2))
for f in(P/'payload/work/tools').iterdir():
 if f.suffix in['.py','.json']and not f.name.endswith('status.json'):shutil.copy2(f,src/f.name)
for name in['build_resources.py','prepare_cpk_kits.py','static_glyph_layouts.py','build_cpk.py','refresh.py','generate_repair_manifest.py','test_startup.py','test_native.py','test_faces.py','test_sleeves.py','test_resources.py','test_myleague.py','test_dex.py','read_parameter_enum.py','package.py']:
 shutil.copy2(P/name,src/name)
shutil.copy2(P/'java/org/efootballrevival/runtimeprobe/ModPayloadRepair.java',src/'ModPayloadRepair.java');shutil.copy2(P/'repair-test-source/RepairTest.java',src/'RepairTest.java')
patch=[];old=Path('/workspace/ronaldo-work/73-ui5/smali');new=P/'smali'
for name in sorted(set(f.relative_to(old).as_posix()for f in old.rglob('*.smali'))|set(f.relative_to(new).as_posix()for f in new.rglob('*.smali'))):
 a=old/name;b=new/name;patch.extend(difflib.unified_diff(a.read_text().splitlines(True)if a.exists()else[],b.read_text().splitlines(True)if b.exists()else[],fromfile='a/'+name if a.exists()else'/dev/null',tofile='b/'+name if b.exists()else'/dev/null'))
(src/'ui5-to-ui6-smali.patch').write_text(''.join(patch));validation=repo/'validation';validation.mkdir(exist_ok=True)
for f in P.glob('*-validation.json'):shutil.copy2(f,validation/f.name)
for name in['resources-build.json','cpk-kits-build.json','kit-slots.json','skills-report.json','celebrations-report.json','performance-audit.json','parameter-enum.json']:shutil.copy2(P/name,validation/name)
(repo/'SHA256SUMS.txt').write_text(sha(out)+'  '+out.name+'\n');print('PACKAGED',out.stat().st_size,sha(out))
