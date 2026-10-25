from pathlib import Path
import json,hashlib,zipfile,shutil,difflib
p=Path('/workspace/ronaldo-work/73-ui5');repo=Path('/workspace/testingdummy/73-v16-ui5');src=repo/'source';repo.mkdir(exist_ok=True);src.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name in ['myleague-73-status.json','myleague-environment-status.json']:(p/'payload/work/tools'/name).write_text(json.dumps({'state':'PENDING_DEVICE_START','version':'73-ui5','phone_verified':False},indent=2))
manifest=json.loads(Path('/workspace/ronaldo-work/73-ui4/release-manifest.json').read_text());rows={r['path']:r for r in manifest['files']if 'pc9299_mobile_and.'not in r['path']and Path(r['path']).name not in['editor_details.py','editor_skill_labels.json']}
for f in(p/'payload').rglob('*'):
 if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':
  n=f.relative_to(p/'payload').as_posix();rows[n]={'path':n,'bytes':f.stat().st_size,'sha256':sha(f)}
manifest['release_id']='v25-73-ui5-body-paths-owned-ratings-y08-kits-native-coaches-20261025';manifest['files']=list(rows.values());(p/'release-manifest.json').write_text(json.dumps(manifest,indent=2))
entries={'classes5.dex':p/'classes5.dex','assets/gateway-release/release-manifest.json':p/'release-manifest.json'}
for folder,prefix in[(p/'payload','assets/gateway-release/'),(p/'apk-assets','')]:
 for f in folder.rglob('*'):
  if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':entries[prefix+f.relative_to(folder).as_posix()]=f
out=repo/'V25-73-UI5-Fixes-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,f in sorted(entries.items()):z.write(f,n)
with zipfile.ZipFile(out)as z:assert z.testzip()is None
(repo/'inventory.json').write_text(json.dumps({n:{'bytes':f.stat().st_size,'sha256':sha(f)}for n,f in sorted(entries.items())},indent=2))
for f in(p/'payload/work/tools').iterdir():
 if f.suffix in['.py','.json']and f.name not in['myleague-73-status.json','myleague-environment-status.json']:shutil.copy2(f,src/f.name)
for name in ['build_rolled.py','build_manager_faces.py','build_ui_assets.py','test_native.py','test_regressions.py','test_codec.py','test_dex.py','test_myleague.py','test_runtime.py','test_body_assets.py','test_pose.py','test_art_assets.py','browser-test.js','package.py','refresh.py']:
 shutil.copy2(p/name,src/name)
shutil.copy2(p/'java/org/efootballrevival/runtimeprobe/ResponsiveUi.java',src/'ResponsiveUi.java')
patch=[];old=Path('/workspace/ronaldo-work/73-ui4/smali');new=p/'smali'
for name in sorted(set(f.relative_to(old).as_posix()for f in old.rglob('*.smali'))|set(f.relative_to(new).as_posix()for f in new.rglob('*.smali'))):
 a=old/name;b=new/name;patch.extend(difflib.unified_diff(a.read_text().splitlines(True)if a.exists()else[],b.read_text().splitlines(True)if b.exists()else[],fromfile='a/'+name if a.exists()else'/dev/null',tofile='b/'+name if b.exists()else'/dev/null'))
(src/'ui4-to-ui5-smali.patch').write_text(''.join(patch))
checks=repo/'validation';checks.mkdir(exist_ok=True)
for f in p.glob('*-validation.json'):shutil.copy2(f,checks/f.name)
for f in [p/'manager-build.json',p/'rolled-build.json',p/'logo-build.json']:shutil.copy2(f,checks/f.name)
(repo/'SHA256SUMS.txt').write_text(sha(out)+'  '+out.name+'\n');print('PACKAGED',out.stat().st_size,sha(out))
