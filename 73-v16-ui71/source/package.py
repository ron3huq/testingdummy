from pathlib import Path
import zipfile,json,hashlib,importlib.util,marshal,struct,time,shutil
P=Path('/workspace/ronaldo-work/73-ui71');R=Path('/workspace/testingdummy/73-v16-ui71');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();t=P/'payload/work/tools'
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui7/V25-73-UI7-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
changes=['mod_startup.py','noodle_hair.py','select_team_runtime.py'];meta=json.loads((t/'noodle_bundle.json').read_text());meta['appearance_files']={n:sha((t/n).read_bytes())for n in meta['appearance_files']};meta['editor_ui']='73-ui7.1-earth-startup-diagnostics';(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2));changes.append('noodle_bundle.json')
for n in changes:entries['assets/gateway-release/work/tools/'+n]=(t/n).read_bytes()
entries['classes5.dex']=(P/'classes5.dex').read_bytes()
# Retain every original protected module and the archive format; replace the
# single bootstrap pyc only. No business-module source rewrite.
import io
with zipfile.ZipFile(io.BytesIO(entries['assets/chaquopy/app.imy']))as old:
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w')as new:
  for info in old.infolist():
   data=old.read(info.filename)
   if info.filename=='embedded_gateway.pyc':
    source=(P/'embedded_gateway_wrapper.py').read_text();code=compile(source,'embedded_gateway.py','exec');data=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(time.time()),len(source.encode()))+marshal.dumps(code)
   new.writestr(info,data)
 entries['assets/chaquopy/app.imy']=out.getvalue()
manifest=json.loads(entries['assets/gateway-release/release-manifest.json']);manifest['release_id']='73-v16-v25-ui7.1-startup-diagnostics-20261026'
for row in manifest['files']:
 n='assets/gateway-release/'+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries['assets/gateway-release/release-manifest.json']=json.dumps(manifest,indent=2).encode()
repair=json.loads(entries['assets/gateway-release/ui6-runtime-manifest.json']);repair['version']='73-ui7.1-startup-diagnostics-20261026'
for row in repair['files']:
 n='assets/gateway-release/'+row['path']
 if n in entries:row['bytes']=len(entries[n]);row['sha256']=sha(entries[n])
entries['assets/gateway-release/ui6-runtime-manifest.json']=json.dumps(repair,indent=2).encode()
file=R/'V25-73-UI7.1-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(file,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,data in sorted(entries.items()):z.writestr(n,data)
(R/'SHA256SUMS.txt').write_text(sha(file.read_bytes())+'  '+file.name+'\n'+'936558cb02c6aa480a66365c8e5dff7527b7ee3f06526403469613f1825d4e4f  ../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip\n')
for n in changes:shutil.copy2(t/n,S/n)
for n in['RuntimeDiagnostics.java','EarthTheme.java']:shutil.copy2(P/'java/org/efootballrevival/runtimeprobe'/n,S/n)
for n in['embedded_gateway_wrapper.py','package.py']:shutil.copy2(P/n,S/n)
(P/'entries.json').write_text(json.dumps({n:{'bytes':len(data),'sha256':sha(data)}for n,data in entries.items()},indent=2))
print('PACKAGED',file.stat().st_size,sha(file.read_bytes()))
