from pathlib import Path
import json,hashlib,re,shutil,zipfile
P=Path('/tmp/73-ui711');T=P/'build/payload/work/tools';L=P/'build/payload/livedata';sha=lambda b:hashlib.sha256(b).hexdigest()
for f in(P/'art-pack/livedata').glob('*'):shutil.copy2(f,L/f.name)
for f in(P/'fixed-faces/livedata').glob('*'):shutil.copy2(f,L/f.name)
new=json.loads((P/'new-targets.json').read_text())['targets']
f=T/'noodle_bundle.json';d=json.loads(f.read_text());oldtargets=d['target_card_ids'];targets=list(dict.fromkeys(oldtargets+new));assert len(targets)==28
for f in T.glob('*.py'):
 s=f.read_text().replace('73-ui7.10-native-equipment','73-ui7.11-body-motion').replace('73-ui7.10','73-ui7.11')
 if f.name=='noodle_hair.py':
  before=repr(oldtargets).replace(', ', ',');after=repr(targets).replace(', ', ',');assert s.count(before)==2;s=s.replace(before,after)
 if f.name=='private_bundles.py':s=s.replace("['pc9305','pc9306','pc9307']","['pc9305','pc9306','pc9307','pc9308']")
 f.write_text(s)
meta={'version':'73-ui7.11','files':{f.name:{'size':f.stat().st_size,'sha256':sha(f.read_bytes())}for f in L.glob('pc930[5678]_mobile_and.*')}};assert len(meta['files'])==12;(T/'private_bundles.json').write_text(json.dumps(meta,indent=2))
for name,lib in [('noodle_hair.py','libnoodle_hair.so'),('select_team_runtime.py','libselect_team.so')]:
 f=T/name;s=f.read_text();s,n=re.subn("HOOK_SHA='[0-9a-f]+'","HOOK_SHA='"+sha((T/lib).read_bytes())+"'",s);assert n==1;f.write_text(s)
d['native_sha256']=sha((T/'libnoodle_hair.so').read_bytes());d['editor_ui']='73-ui7.11';d['version']='73-ui7.11-body-motion';d['target_card_ids']=targets
for name in ['profile_editor.py','profile_options.json']:d['appearance_files'][name]='pending'
for name in d['appearance_files']:d['appearance_files'][name]=sha((T/name).read_bytes())
d['appearance_overlay_sha256']=sha((T/'myleague_editor_runtime.py').read_bytes());d['new_five_faces']={'filename_ID_mapping_confirmed_by_user':True,'profiles':json.loads((P/'new-targets.json').read_text())['face_namespaces'],'skeleton_bones':166,'both_LODs_full':True,'body_motion_source':'89138556572074','Android_tested':False};(T/'noodle_bundle.json').write_text(json.dumps(d,indent=2))
with zipfile.ZipFile('/tmp/73-ui79/publish/73-v16-ui710/V25-73-UI7.10-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
for folder in ['work/tools','livedata']:
 for f in(P/'build/payload'/folder).glob('*'):
  if f.is_file():entries['assets/gateway-release/'+folder+'/'+f.name]=f.read_bytes()
entries['classes5.dex']=(P/'build/classes5-ui711.dex').read_bytes()
addons=['work/tools/profile_editor.py','work/tools/profile_options.json']+['livedata/'+f.name for f in L.glob('pc9308_mobile_and.*')]
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 key='assets/gateway-release/'+name;d=json.loads(entries[key]);d['release_id'if name.startswith('release')else'version']='73-ui7.11-20261027';existing={r['path']for r in d['files']}
 for path in addons:
  if path not in existing:d['files'].append({'path':path})
 for row in d['files']:
  path='assets/gateway-release/'+row['path']
  if path in entries:row.update(bytes=len(entries[path]),sha256=sha(entries[path]))
 entries[key]=json.dumps(d,indent=2).encode()
for n,b in entries.items():
 if n.endswith('.py'):compile(b,n,'exec')
parts={2:{n:b for n,b in entries.items()if not Path(n).name.startswith('pc9308_mobile_and.')},3:{n:b for n,b in entries.items()if Path(n).name.startswith('pc9308_mobile_and.')}}
for num,data in parts.items():
 out=P/f'build/UI711-INTERNAL-Part{num}.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for n,b in data.items():z.writestr(n,b)
 print('CANDIDATE_PART',num,out.stat().st_size,sha(out.read_bytes()));assert out.stat().st_size<100*1024*1024
