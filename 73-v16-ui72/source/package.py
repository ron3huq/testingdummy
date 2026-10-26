from pathlib import Path
import zipfile,json,hashlib,shutil
P=Path('/workspace/ronaldo-work/73-ui72');R=Path('/workspace/testingdummy/73-v16-ui72');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui71/V25-73-UI7.1-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
prefix='assets/gateway-release/';old=prefix+'livedata/dt870_mobile_and.cpk';private=prefix+'livedata/dt870_ui72_mobile_and.cpk';entries[private]=entries[old];entries[old]=Path('/workspace/ronaldo-work/73-ui6/original-dt870.cpk').read_bytes()
for n in['kits_runtime.py','mod_startup.py']:entries[prefix+'work/tools/'+n]=(P/'payload/work/tools'/n).read_bytes()
meta=json.loads(entries[prefix+'work/tools/noodle_bundle.json']);meta['appearance_files']={n:sha(entries[prefix+'work/tools/'+n])for n in meta['appearance_files']};meta['editor_ui']='73-ui7.2-isolated-kits-cpk-conflict-fix';entries[prefix+'work/tools/noodle_bundle.json']=json.dumps(meta,indent=2).encode()
entries['classes5.dex']=(P/'classes5.dex').read_bytes()
manifest=json.loads(entries[prefix+'release-manifest.json']);manifest['release_id']='73-v16-v25-ui7.2-isolated-dt870-20261026';manifest['files'].append({'path':'livedata/dt870_ui72_mobile_and.cpk'})
for row in manifest['files']:
 n=prefix+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries[prefix+'release-manifest.json']=json.dumps(manifest,indent=2).encode()
repair=json.loads(entries[prefix+'ui6-runtime-manifest.json']);repair['version']='73-ui7.2-isolated-dt870-20261026'
for row in repair['files']:
 if row['path']=='livedata/dt870_mobile_and.cpk':row['path']='livedata/dt870_ui72_mobile_and.cpk'
 n=prefix+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries[prefix+'ui6-runtime-manifest.json']=json.dumps(repair,indent=2).encode()
out=R/'V25-73-UI7.2-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(entries.items()):z.writestr(n,b)
(R/'SHA256SUMS.txt').write_text(sha(out.read_bytes())+'  '+out.name+'\n936558cb02c6aa480a66365c8e5dff7527b7ee3f06526403469613f1825d4e4f  ../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip\n')
(R/'inventory.json').write_text(json.dumps({n:{'bytes':len(b),'sha256':sha(b)}for n,b in sorted(entries.items())},indent=2))
for n in['kits_runtime.py','mod_startup.py']:(S/n).write_bytes(entries[prefix+'work/tools/'+n])
(S/'noodle_bundle.json').write_bytes(entries[prefix+'work/tools/noodle_bundle.json']);shutil.copy2(P/'java/org/efootballrevival/runtimeprobe/RuntimeDiagnostics.java',S/'RuntimeDiagnostics.java')
shutil.copy2(P/'package.py',S/'package.py');print('PACKAGED',out.stat().st_size,sha(out.read_bytes()))
