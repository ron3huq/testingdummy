from pathlib import Path
import zipfile,json,hashlib,shutil,difflib
P=Path('/workspace/ronaldo-work/73-ui75');R=Path('/workspace/testingdummy/73-v16-ui75');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);prefix='assets/gateway-release/';sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui74/V25-73-UI7.4-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
for n in ['libselect_team.so','select_team_runtime.py','bridge_73.py','player_model.py','myleague_73.py']:entries[prefix+'work/tools/'+n]=(P/'payload/work/tools'/n).read_bytes()
s=entries[prefix+'work/tools/mod_startup.py'].decode().replace('73-ui7.4','73-ui7.5').replace('Eight startup requests maximum','Sixty-four startup requests maximum');entries[prefix+'work/tools/mod_startup.py']=s.encode()
meta=json.loads(entries[prefix+'work/tools/noodle_bundle.json']);meta['appearance_files']['player_model.py']=sha(entries[prefix+'work/tools/player_model.py']);meta['appearance_files']={n:sha(entries[prefix+'work/tools/'+n])for n in meta['appearance_files']};meta['editor_ui']='73-ui7.5-y08-kit-gate-player-model';entries[prefix+'work/tools/noodle_bundle.json']=json.dumps(meta,indent=2).encode()
entries['classes5.dex']=(P/'classes5.dex').read_bytes()
for n in ['release-manifest.json','ui6-runtime-manifest.json']:
 doc=json.loads(entries[prefix+n]);doc['release_id'if n.startswith('release')else'version']='73-ui7.5-y08-kit-gate-player-model-20261026'
 path='work/tools/player_model.py';doc['files'].append({'path':path,'bytes':len(entries[prefix+path]),'sha256':sha(entries[prefix+path])})
 for row in doc['files']:
  key=prefix+row['path']
  if key in entries:row['bytes']=len(entries[key]);row['sha256']=sha(entries[key])
 entries[prefix+n]=json.dumps(doc,indent=2).encode()
out=R/'V25-73-UI7.5-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(entries.items()):z.writestr(n,b)
(R/'SHA256SUMS.txt').write_text(sha(out.read_bytes())+'  '+out.name+'\n936558cb02c6aa480a66365c8e5dff7527b7ee3f06526403469613f1825d4e4f  ../73-v16-ui7/V25-73-UI7-FULL-Part1-Faces-MT.zip\n')
(R/'inventory.json').write_text(json.dumps({n:{'bytes':len(b),'sha256':sha(b)}for n,b in entries.items()},indent=2))
for n in ['select_team_runtime.py','bridge_73.py','player_model.py','myleague_73.py','noodle_bundle.json']:(S/n).write_bytes(entries[prefix+'work/tools/'+n])
for n in ['select_team.c','rolled-models.h','resource_codec.h','skill-text.h']:shutil.copy2(P/'native'/n,S/n)
for n in ['PlayerModelEditor.java']:shutil.copy2(P/'java/org/efootballrevival/runtimeprobe'/n,S/n)
for n in ['test_model.py','test_model_native.py','test_native_regression.py','morph_tables.py','native_dis.py','change_native.py','package.py']:shutil.copy2(P/n,S/n)
a=P.with_name('73-ui74')/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali';b=P/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali';(S/'PlayerEditorPanel.patch').write_text(''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile='a/PlayerEditorPanel.smali',tofile='b/PlayerEditorPanel.smali')))
print('PACKAGED',out.stat().st_size,sha(out.read_bytes()))
