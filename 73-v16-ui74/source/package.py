from pathlib import Path
import zipfile,json,hashlib,io,importlib.util,marshal,struct,time,shutil
P=Path('/workspace/ronaldo-work/73-ui74');R=Path('/workspace/testingdummy/73-v16-ui74');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();prefix='assets/gateway-release/'
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui73/V25-73-UI7.3-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
old='livedata/dt870_ui72_mobile_and.cpk';new='livedata/dt870_ui74_mobile_and.cpk';entries.pop(prefix+old);entries[prefix+new]=(P/'dt870_ui74_mobile_and.cpk').read_bytes()
for n in['kits_runtime.py','mod_startup.py']:entries[prefix+'work/tools/'+n]=(P/'payload/work/tools'/n).read_bytes()
kit=json.loads(entries[prefix+'work/tools/kits_bundle.json']);row=kit['files']['dt870_mobile_and.cpk'];row['size']=len(entries[prefix+new]);row['sha256']=sha(entries[prefix+new]);entries[prefix+'work/tools/kits_bundle.json']=json.dumps(kit,indent=2).encode()
meta=json.loads(entries[prefix+'work/tools/noodle_bundle.json']);meta['appearance_files']={n:sha(entries[prefix+'work/tools/'+n])for n in meta['appearance_files']};meta['editor_ui']='73-ui7.4-resource-transfer-and-cpk-format';entries[prefix+'work/tools/noodle_bundle.json']=json.dumps(meta,indent=2).encode();entries['classes5.dex']=(P/'classes5.dex').read_bytes()
with zipfile.ZipFile(io.BytesIO(entries['assets/chaquopy/app.imy']))as original:
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w')as z:
  for info in original.infolist():
   data=original.read(info.filename)
   if info.filename=='embedded_gateway.pyc':
    source=(P/'embedded_gateway_wrapper.py').read_text();data=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(time.time()),len(source.encode()))+marshal.dumps(compile(source,'embedded_gateway.py','exec'))
   z.writestr(info,data)
 entries['assets/chaquopy/app.imy']=out.getvalue()
for n,version in [('release-manifest.json','73-v16-v25-ui7.4-resource-transfer-20261026'),('ui6-runtime-manifest.json','73-ui7.4-resource-transfer-20261026')]:
 doc=json.loads(entries[prefix+n]);doc['release_id'if n.startswith('release')else'version']=version
 for row in doc['files']:
  if row['path']==old:row['path']=new
  key=prefix+row['path']
  if key in entries:row['bytes']=len(entries[key]);row['sha256']=sha(entries[key])
 entries[prefix+n]=json.dumps(doc,indent=2).encode()
out=R/'V25-73-UI7.4-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(entries.items()):z.writestr(n,b)
(R/'SHA256SUMS.txt').write_text(sha(out.read_bytes())+'  '+out.name+'\n936558cb02c6aa480a66365c8e5dff7527b7ee3f06526403469613f1825d4e4f  ../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip\n');(R/'inventory.json').write_text(json.dumps({n:{'bytes':len(b),'sha256':sha(b)}for n,b in sorted(entries.items())},indent=2))
for n in['kits_runtime.py','mod_startup.py','kits_bundle.json','noodle_bundle.json']:(S/n).write_bytes(entries[prefix+'work/tools/'+n])
for n in['LiveResourceServer.java','ResourcePresence.java','RuntimeDiagnostics.java']:shutil.copy2(P/'java/org/efootballrevival/runtimeprobe'/n,S/n)
for n in['package.py','prepare.py','HttpResourceTest.java','PresenceTest.java','embedded_gateway_wrapper.py']:shutil.copy2(P/n,S/n)
shutil.copy2('/workspace/ronaldo-work/73-ui74-build-cpk.py',S/'build_cpk.py')
# Reviewable diffs for the two changed existing Java methods.
import difflib
patch=[]
for name in['EmbeddedGateway.smali','PersistentResources.smali','UiStringsData.smali']:
 rel=Path('org/efootballrevival/runtimeprobe')/name;a=Path('/workspace/ronaldo-work/73-ui73/smali')/rel;b=P/'smali'/rel;patch.extend(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile='a/'+str(rel),tofile='b/'+str(rel)))
(S/'ui73-to-ui74-smali.patch').write_text(''.join(patch));print('PACKAGED',out.stat().st_size,sha(out.read_bytes()))
