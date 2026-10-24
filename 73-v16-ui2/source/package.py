from pathlib import Path
import json,hashlib,zipfile,shutil,difflib
p=Path('/workspace/ronaldo-work/73-ui2');repo=Path('/workspace/testingdummy/73-v16-ui2');src=repo/'source';repo.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
# Final files only: never copy the user save/test DBs into the deliverable.
manifest=json.loads(Path('/workspace/ronaldo-work/73-ui/release-manifest.json').read_text());rows={r['path']:r for r in manifest['files']}
for f in (p/'payload').rglob('*'):
 if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':
  n=f.relative_to(p/'payload').as_posix();rows[n]={'path':n,'bytes':f.stat().st_size,'sha256':sha(f)}
manifest['release_id'] += '-ui2-fast-cuffs-20261025';manifest['files']=list(rows.values());(p/'release-manifest.json').write_text(json.dumps(manifest,indent=2))
entries={'classes5.dex':p/'classes5.dex','assets/gateway-release/release-manifest.json':p/'release-manifest.json'}
for folder,prefix in [(p/'payload','assets/gateway-release/'),(p/'apk-assets','')]:
 for f in folder.rglob('*'):
  if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':entries[prefix+f.relative_to(folder).as_posix()]=f
out=repo/'V25-73-UI2-Fast-Catalogue-Ronaldo-Cuffs-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,f in sorted(entries.items()):z.write(f,n)
with zipfile.ZipFile(out)as z:assert z.testzip()is None
inventory={n:{'bytes':f.stat().st_size,'sha256':sha(f)}for n,f in sorted(entries.items())}
(repo/'inventory.json').write_text(json.dumps(inventory,indent=2))
(repo/'SHA256SUMS.txt').write_text(sha(out)+'  '+out.name+'\n')
patch=[]
old=Path('/workspace/ronaldo-work/73-ui/original-smali');new=p/'smali'
for name in sorted(set(f.relative_to(old).as_posix()for f in old.rglob('*.smali'))|set(f.relative_to(new).as_posix()for f in new.rglob('*.smali'))):
 a=old/name;b=new/name;s1=a.read_text().splitlines(True)if a.exists()else[];s2=b.read_text().splitlines(True)if b.exists()else[]
 patch.extend(difflib.unified_diff(s1,s2,fromfile='a/'+name if a.exists()else'/dev/null',tofile='b/'+name if b.exists()else'/dev/null'))
(src/'ui-smali.patch').write_text(''.join(patch))

for n in ['build_rolled.py','test_api.py','test_runtime.py','test_mesh.py','test_native.py','test_dex.py','browser-final.js','benchmark.py','editor-english.js']:
 shutil.copy2(p/n,src/n)
for n in ['DexTool.java','Compile.java','english-words.json']:
 shutil.copy2(Path('/workspace/ronaldo-work/73-ui')/n,src/n)
shutil.copy2(p/'payload/work/tools/myleague_editor_runtime.py',src/'myleague_editor_runtime.py')
checks=repo/'validation';checks.mkdir(exist_ok=True)
for f in list(p.glob('*-validation.json'))+[p/'benchmark.json']:shutil.copy2(f,checks/f.name)
print('PACKAGE',out.name,out.stat().st_size,sha(out),'files',len(entries))
