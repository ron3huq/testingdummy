from pathlib import Path
import json,hashlib,re,shutil,zipfile
P=Path('/workspace/73-ui712');A=P/'build/apk';T=A/'assets/gateway-release/work/tools';L=T.parents[1]/'livedata';sha=lambda b:hashlib.sha256(b).hexdigest()
for folder in ['pc-faces','fixed-android','cut-bodies']:
 for f in(P/folder/'livedata').glob('*'):shutil.copy2(f,L/f.name)
for unit in ['select_team','noodle_hair']:
 p=T/(unit+'_runtime.py'if unit=='select_team'else'noodle_hair.py');s=p.read_text();s=re.sub(r"HOOK_SHA='[0-9a-f]+'","HOOK_SHA='"+sha((T/('lib'+unit+'.so')).read_bytes())+"'",s);p.write_text(s)
meta=json.loads((T/'noodle_bundle.json').read_text());added=['88042803047215','105634720685845','105565464400480','105625593957752','89138288266704'];old=meta['target_card_ids'];new=old+[x for x in added if x not in old];meta['target_card_ids']=new
p=T/'noodle_hair.py';s=p.read_text().replace(str(old).replace(', ',','),str(new).replace(', ',','));p.write_text(s)
for p in T.glob('*.py'):
 s=p.read_text().replace('73-ui7.11','73-ui7.12').replace('UI7.11','UI7.12');p.write_text(s)
p=T/'private_bundles.py';s=p.read_text().replace("['pc9305','pc9306','pc9307','pc9308','pc9310','pc9313']","['pc9305','pc9306','pc9307','pc9308','pc9310','pc9313','pc9312']");p.write_text(s)
d=json.loads((T/'private_bundles.json').read_text())
for stem in ['pc9310','pc9313','pc9312']:
 for ext in ['pak','utoc','ucas']:
  f=L/(stem+'_mobile_and.'+ext);d['files'][f.name]={'size':f.stat().st_size,'sha256':sha(f.read_bytes())}
(T/'private_bundles.json').write_text(json.dumps(d,indent=2))
exclude={'noodle_bundle.json','myleague_editor.json'}
# Exact runtime code/data audit; mutable user profiles stay outside the copy/repair lists.
for f in T.iterdir():
 if f.is_file()and f.name not in exclude and f.suffix in ['.py','.so','.json','.gz','.zlib']and not any(x in f.name for x in ['status','diagnostic']):meta['appearance_files'][f.name]=sha(f.read_bytes())
meta['appearance_files']={n:sha((T/n).read_bytes())for n in meta['appearance_files']};meta['appearance_overlay_sha256']=sha((T/'myleague_editor_runtime.py').read_bytes());meta['editor_ui']='73-ui7.12';(T/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 p=A/'assets/gateway-release'/name;d=json.loads(p.read_text());d['release_id'if name.startswith('release')else'version']='73-ui7.12-20261028';paths={r['path']for r in d['files']}
 for f in T.iterdir():
  key='work/tools/'+f.name
  if f.is_file()and f.name!='myleague_editor.json'and key not in paths:d['files'].append({'path':key});paths.add(key)
 for stem in ['pc9310','pc9313','pc9312']:
  for ext in ['pak','utoc','ucas']:
   key='livedata/'+stem+'_mobile_and.'+ext
   if key not in paths:d['files'].append({'path':key});paths.add(key)
 for row in d['files']:
  f=A/'assets/gateway-release'/row['path']
  if f.is_file():row.update(bytes=f.stat().st_size,sha256=sha(f.read_bytes()))
 p.write_text(json.dumps(d,indent=2))
p=A/'assets/card-designer/MANIFEST.json';d=json.loads(p.read_text());f=p.parent/'portrait-ui712.html';d[f.name]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())};p.write_text(json.dumps(d,indent=2))
shutil.copy2(P/'build/classes5-ui712.dex',A/'classes5.dex')
# No generated test caches or private user diagnostics in any package.
for folder in A.rglob('__pycache__'):shutil.rmtree(folder)
print('FINAL_RUNTIME_PINS',len(meta['appearance_files']),'FACE_IDS',len(new))
