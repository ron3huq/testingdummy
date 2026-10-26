from pathlib import Path
import zipfile,json,hashlib,shutil,difflib
P=Path('/workspace/ronaldo-work/73-ui77');R=Path('/workspace/testingdummy/73-v16-ui77');R.mkdir(exist_ok=True);S=R/'source';S.mkdir(exist_ok=True);prefix='assets/gateway-release/work/tools/';sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile('/workspace/testingdummy/73-v16-ui76/V25-73-UI7.6-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
changed=['select_team_runtime.py','libselect_team.so','body_dimensions.py','myleague_editor_runtime.py','bridge_73.py','player_tuning.py','innate_skill_labels.json']
for n in changed:entries[prefix+n]=(P/'payload/work/tools'/n).read_bytes()
meta=json.loads(entries[prefix+'noodle_bundle.json']);meta['appearance_files'].update({n:sha(entries[prefix+n])for n in changed});meta['appearance_files']={n:sha(entries[prefix+n])for n in meta['appearance_files']};meta['appearance_overlay_sha256']=sha(entries[prefix+'myleague_editor_runtime.py']);meta['editor_ui']='73-ui7.7';entries[prefix+'noodle_bundle.json']=json.dumps(meta,indent=2).encode();entries[prefix+'mod_startup.py']=entries[prefix+'mod_startup.py'].replace(b'73-ui7.6',b'73-ui7.7');entries['classes5.dex']=(P/'classes5.dex').read_bytes()
for n in ['release-manifest.json','ui6-runtime-manifest.json']:
 key='assets/gateway-release/'+n;doc=json.loads(entries[key]);doc['release_id'if n.startswith('release')else'version']='73-ui7.7-20261026'
 for addon in ['player_tuning.py','innate_skill_labels.json']:doc['files'].append({'path':'work/tools/'+addon})
 for row in doc['files']:
  path='assets/gateway-release/'+row['path']
  if path in entries:row.update(bytes=len(entries[path]),sha256=sha(entries[path]))
 entries[key]=json.dumps(doc,indent=2).encode()
out=R/'V25-73-UI7.7-FULL-Part2-Main-MT.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in entries.items():z.writestr(n,b)
(R/'SHA256SUMS.txt').write_text(sha(out.read_bytes())+'  '+out.name+'\n');(R/'inventory.json').write_text(json.dumps({n:{'bytes':len(b),'sha256':sha(b)}for n,b in entries.items()},indent=2))
for n in changed:
 if n.endswith(('.py','.json')):shutil.copy2(P/'payload/work/tools'/n,S/n)
for n in ['select_team.c','resource_codec.h','rolled-models.h','skill-text.h']:shutil.copy2(P/'native'/n,S/n)
for n in ['TuningEditor.java','BodyEditor.java']:shutil.copy2(P/'java/org/efootballrevival/runtimeprobe'/n,S/n)
for n in ['prepare.py','package.py','test_tuning.py','test_native_tuning.py','test_bone_consumer.py','probe_dimensions.py','celebrations_six.py','find_body_calls.py']:shutil.copy2(P/n,S/n)
for n in ['celebration-six-cards.csv','celebrations-validation.json','bone-consumer-validation.json','tuning-storage-validation.json','native-tuning-validation.json']:shutil.copy2(P/n,R/n)
a=P.with_name('73-ui76')/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali';b=P/'smali/org/efootballrevival/runtimeprobe/PlayerEditorPanel.smali';(S/'PlayerEditorPanel.patch').write_text(''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile='a/PlayerEditorPanel.smali',tofile='b/PlayerEditorPanel.smali')))
print('PACKAGE',out.stat().st_size,sha(out.read_bytes()))
