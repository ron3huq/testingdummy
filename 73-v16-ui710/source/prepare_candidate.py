from pathlib import Path
import json,hashlib,re,shutil,zipfile
P=Path('/tmp/73-ui710');T=P/'build/payload/work/tools';L=P/'build/payload/livedata';sha=lambda b:hashlib.sha256(b).hexdigest()
L.mkdir(exist_ok=True)
for folder in ['fixed-spider','fixed-new','art-pack']:
 for f in(P/folder/'livedata').glob('*'):shutil.copy2(f,L/f.name)
removed={'custom_skin.py','skin_iostore.py','skin_templates.zlib'}
for n in removed:(T/n).unlink(missing_ok=True)
for f in T.glob('*.py'):
 s=f.read_text().replace('73-ui7.9-faces-rgb','73-ui7.10-native-equipment').replace('73-ui7.9','73-ui7.10')
 f.write_text(s)
meta={'version':'73-ui7.10','files':{f.name:{'size':f.stat().st_size,'sha256':sha(f.read_bytes())}for f in L.glob('pc930[567]_mobile_and.*')}};assert len(meta['files'])==9;(T/'private_bundles.json').write_text(json.dumps(meta,indent=2))
for name,lib in [('noodle_hair.py','libnoodle_hair.so'),('select_team_runtime.py','libselect_team.so')]:
 f=T/name;s=f.read_text();s,n=re.subn("HOOK_SHA='[0-9a-f]+'","HOOK_SHA='"+sha((T/lib).read_bytes())+"'",s);assert n==1;f.write_text(s)
f=T/'noodle_bundle.json';d=json.loads(f.read_text());d['native_sha256']=sha((T/'libnoodle_hair.so').read_bytes());d['editor_ui']='73-ui7.10';d['version']='73-ui7.10-native-equipment'
for pid in ['105804908868664','105873896755947']:
 if pid not in d['target_card_ids']:d['target_card_ids'].append(pid)
for n in removed:d['appearance_files'].pop(n,None)
for name in ['appearance_gear.py','appearance_choices.py','private_bundles.py','private_bundles.json','myleague_editor_runtime.py','libselect_team.so']:d['appearance_files'][name]='pending'
for name in d['appearance_files']:d['appearance_files'][name]=sha((T/name).read_bytes())
d['appearance_overlay_sha256']=sha((T/'myleague_editor_runtime.py').read_bytes());d.pop('body_RGB',None);d['native_skin_only']=True;d['hero_face_source']='User supplied Android trial geometry; native73 skeleton166 and both full inline LODs restored for Spider/Naruto/Orc';f.write_text(json.dumps(d,indent=2))
with zipfile.ZipFile('/tmp/73-ui79/publish/73-v16-ui79/V25-73-UI7.9-FULL-Part2-Main-MT.zip')as z:entries={n:z.read(n)for n in z.namelist()}
for name in removed:entries.pop('assets/gateway-release/work/tools/'+name,None)
for folder in ['work/tools','livedata']:
 for f in(P/'build/payload'/folder).glob('*'):
  if f.is_file():entries['assets/gateway-release/'+folder+'/'+f.name]=f.read_bytes()
entries['classes5.dex']=(P/'build/classes5-ui710.dex').read_bytes()
addons=['work/tools/appearance_gear.py']+['livedata/'+f.name for f in L.glob('pc930[567]_mobile_and.*')]
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 key='assets/gateway-release/'+name;d=json.loads(entries[key]);d['release_id'if name.startswith('release')else'version']='73-ui7.10-20261027';d['files']=[r for r in d['files']if r['path']not in ['work/tools/'+n for n in removed]];existing={r['path']for r in d['files']}
 for path in addons:
  if path not in existing:d['files'].append({'path':path})
 for row in d['files']:
  path='assets/gateway-release/'+row['path']
  if path in entries:row.update(bytes=len(entries[path]),sha256=sha(entries[path]))
 entries[key]=json.dumps(d,indent=2).encode()
for n,b in entries.items():
 if n.endswith('.py'):compile(b,n,'exec')
out=P/'build/UI710-INTERNAL-CANDIDATE-NOT-FULL.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in entries.items():z.writestr(n,b)
print('FULL_CANDIDATE_READY',out.stat().st_size,sha(out.read_bytes()))
