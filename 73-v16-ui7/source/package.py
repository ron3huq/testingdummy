from pathlib import Path
import json,hashlib,zipfile,shutil,difflib
P=Path('/workspace/ronaldo-work/73-ui7');repo=Path('/workspace/testingdummy/73-v16-ui7');repo.mkdir(exist_ok=True);src=repo/'source';src.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
for f in(P/'payload/work/tools').glob('*status.json'):f.write_text(json.dumps({'state':'PENDING_DEVICE_START','version':'73-ui7-full','phone_verified':False},indent=2))
# Refresh all code pins after adding dimensions and startup wiring.
t=P/'payload/work/tools';meta=json.loads((t/'noodle_bundle.json').read_text());meta['appearance_files']={k:sha((t/k).read_bytes())for k in meta['appearance_files']};meta['appearance_overlay_sha256']=sha((t/'myleague_editor_runtime.py').read_bytes());meta['editor_ui']='73-ui7-full-earth-accent-search-on-demand-dimensions';(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
for f in t.glob('*.py'):compile(f.read_text(),str(f),'exec')
stock=json.loads(Path('/workspace/ronaldo-work/73-inspect/v16-meta/assets/gateway-release/release-manifest.json').read_text());stockrows={r['path']:r for r in stock['files']}
manifest=json.loads(Path('/workspace/ronaldo-work/73-ui6/release-manifest.json').read_text());rows={r['path']:r for r in manifest['files']}
files={}
for f in(P/'payload').rglob('*'):
 if f.is_file()and '__pycache__'not in f.parts and f.suffix!='.pyc':
  n=f.relative_to(P/'payload').as_posix();files[n]=f;rows[n]={'path':n,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
# Closure against CLEAN stock73, not a previously modded APK.
with zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')as base:
 for n,row in rows.items():
  if n not in files and (n not in stockrows or row['sha256']!=stockrows[n]['sha256']):
   data=base.read('assets/gateway-release/'+n);assert len(data)==row['bytes']and sha(data)==row['sha256'],n
   f=P/'carry'/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data);files[n]=f
 # Only modified non-gateway assets are needed; untouched artwork remains stock.
 assets={}
 for f in(P/'apk-assets/assets').rglob('*'):
  if not f.is_file()or'gateway-release'in f.parts:continue
  n='assets/'+f.relative_to(P/'apk-assets/assets').as_posix();data=f.read_bytes()
  if n not in base.namelist()or sha(base.read(n))!=sha(data):assets[n]=f
# Critical immutable startup payload; mutable saves and editor config are excluded.
critical=[]
for n,f in files.items():
 if n.startswith('livedata/')or (n.startswith('work/tools/')and(f.suffix in['.py','.so']or f.name in['myleague_custom.json','ui2_skill_rules.json','myleague_base_rosters.json.gz','noodle_hair.json','noodle_bundle.json','extras_bundle.json','manager_bundle.json','kits_bundle.json'])):
  critical.append({'path':n,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
repair=P/'apk-assets/assets/gateway-release/ui6-runtime-manifest.json';repair.write_text(json.dumps({'version':'73-ui7-FULL-earth-20261026','files':sorted(critical,key=lambda r:r['path'])},indent=2))
manifest['release_id']='73-v16-v25-ui7-FULL-earth-20261026';manifest['files']=list(rows.values());mf=P/'release-manifest.json';mf.write_text(json.dumps(manifest,indent=2))
entries={'classes5.dex':P/'classes5.dex','assets/gateway-release/release-manifest.json':mf,'assets/gateway-release/ui6-runtime-manifest.json':repair,**assets}
entries.update({'assets/gateway-release/'+n:f for n,f in files.items()})
# This loader is essential: stock73's original app.imy never imports the mod bridge.
loader=P/'app.imy'
with zipfile.ZipFile('/workspace/testingdummy/73-v16-v25-port/V25-for-73-V16-MT-Manager.zip')as z:loader.write_bytes(z.read('assets/chaquopy/app.imy'))
entries['assets/chaquopy/app.imy']=loader
parts=[{},{}]
for n,f in entries.items():parts[0 if '/pc9298_mobile_and.'in n else 1][n]=f
assert len(parts[0])==3 and not(set(parts[0])&set(parts[1]))
outputs=[]
for part,label in zip(parts,['Part1-Faces','Part2-Main']):
 out=repo/('V25-73-UI7-FULL-'+label+'-MT.zip')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for n,f in sorted(part.items()):z.write(f,n)
 with zipfile.ZipFile(out)as z:assert z.testzip()is None
 outputs.append({'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'entries':len(part)})
(repo/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['file']+'\n'for r in outputs));(repo/'inventory.json').write_text(json.dumps({n:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}for n,f in sorted(entries.items())},indent=2))
(P/'package-build.json').write_text(json.dumps({'parts':outputs,'changed_gateway_files':len(files),'critical_files':len(critical),'changed_frontend_assets':len(assets),'stock_manifest_entries':len(stockrows),'full_manifest_entries':len(rows),'carried_from_v25':[n for n in files if n not in[f.relative_to(P/'payload').as_posix()for f in(P/'payload').rglob('*')if f.is_file()]]},indent=2))
for f in t.iterdir():
 if f.suffix in['.py','.json']and not f.name.endswith('status.json'):shutil.copy2(f,src/f.name)
for f in(P/'java/org/efootballrevival/runtimeprobe').glob('*.java'):shutil.copy2(f,src/f.name)
for name in['test_body.py','test_native_dimensions.py','SearchTest.java','package.py']:shutil.copy2(P/name,src/name)
patch=[];old=Path('/workspace/ronaldo-work/73-ui6/smali');new=P/'smali'
for name in sorted(set(f.relative_to(old).as_posix()for f in old.rglob('*.smali'))|set(f.relative_to(new).as_posix()for f in new.rglob('*.smali'))):
 a=old/name;b=new/name;patch.extend(difflib.unified_diff(a.read_text().splitlines(True)if a.exists()else[],b.read_text().splitlines(True)if b.exists()else[],fromfile='a/'+name if a.exists()else'/dev/null',tofile='b/'+name if b.exists()else'/dev/null'))
(src/'ui6-to-ui7-smali.patch').write_text(''.join(patch));print(json.dumps(outputs,indent=2))
