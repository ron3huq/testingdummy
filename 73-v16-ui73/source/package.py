from pathlib import Path
import json,zipfile,hashlib,shutil
P=Path('/workspace/ronaldo-work/73-ui73');R=Path('/workspace/testingdummy/73-v16-ui73');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();prefix='assets/gateway-release/'
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui72/V25-73-UI7.2-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
changes=['hook_arena.py','noodle_hair.py','select_team_runtime.py','mod_startup.py']
for n in changes:
 data=(P/'payload/work/tools'/n).read_bytes();compile(data,n,'exec');entries[prefix+'work/tools/'+n]=data
entries['classes5.dex']=(P/'classes5.dex').read_bytes()
meta=json.loads(entries[prefix+'work/tools/noodle_bundle.json']);meta['appearance_files']['hook_arena.py']='';meta['appearance_files']={n:sha(entries[prefix+'work/tools/'+n])for n in meta['appearance_files']};meta['editor_ui']='73-ui7.3-shared-hook-arena';entries[prefix+'work/tools/noodle_bundle.json']=json.dumps(meta,indent=2).encode()
manifest=json.loads(entries[prefix+'release-manifest.json']);manifest['release_id']='73-v16-v25-ui7.3-shared-hook-arena-20261026';manifest['files'].append({'path':'work/tools/hook_arena.py'})
for row in manifest['files']:
 n=prefix+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries[prefix+'release-manifest.json']=json.dumps(manifest,indent=2).encode()
repair=json.loads(entries[prefix+'ui6-runtime-manifest.json']);repair['version']='73-ui7.3-shared-hook-arena-20261026';repair['files'].append({'path':'work/tools/hook_arena.py'})
for row in repair['files']:
 n=prefix+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries[prefix+'ui6-runtime-manifest.json']=json.dumps(repair,indent=2).encode()
file=R/'V25-73-UI7.3-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(file,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(entries.items()):z.writestr(n,b)
(R/'SHA256SUMS.txt').write_text(sha(file.read_bytes())+'  '+file.name+'\n936558cb02c6aa480a66365c8e5dff7527b7ee3f06526403469613f1825d4e4f  ../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip\n')
(R/'inventory.json').write_text(json.dumps({n:{'bytes':len(b),'sha256':sha(b)}for n,b in sorted(entries.items())},indent=2))
for n in changes:(S/n).write_bytes(entries[prefix+'work/tools/'+n])
(S/'noodle_bundle.json').write_bytes(entries[prefix+'work/tools/noodle_bundle.json'])
for n in ['package.py','test_arena.py','test_startup.py','research_celebrations.py','check_celebration_parameters.py']:shutil.copy2(P/n,S/n)
shutil.copy2(P/'java/org/efootballrevival/runtimeprobe/RuntimeDiagnostics.java',S/'RuntimeDiagnostics.java')
print('PACKAGED',file.stat().st_size,sha(file.read_bytes()))
