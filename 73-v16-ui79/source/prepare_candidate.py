from pathlib import Path
import json,hashlib,re,shutil,zipfile
P=Path('/tmp/73-ui79');T=P/'build/payload/work/tools';L=P/'build/payload/livedata';sha=lambda b:hashlib.sha256(b).hexdigest()
for f in(P/'art-pack/livedata').glob('pc9306_mobile_and.*'):shutil.copy2(f,L/f.name)
meta={'version':'73-ui7.9','files':{f.name:{'size':f.stat().st_size,'sha256':sha(f.read_bytes())}for f in L.glob('pc930[56]_mobile_and.*')}};(T/'private_bundles.json').write_text(json.dumps(meta,indent=2));assert len(meta['files'])==6
f=T/'noodle_hair.py';s=f.read_text();s=re.sub("HOOK_SHA='[0-9a-f]+'","HOOK_SHA='"+sha((T/'libnoodle_hair.so').read_bytes())+"'",s);f.write_text(s)
f=T/'mod_startup.py';f.write_text(f.read_text().replace('73-ui7.8','73-ui7.9'))
f=T/'noodle_bundle.json';d=json.loads(f.read_text());d['native_sha256']=sha((T/'libnoodle_hair.so').read_bytes());d['editor_ui']='73-ui7.9';d['version']='73-ui7.9-faces-rgb'
for pid in ['106754901843130','105647605587130']:
 if pid not in d['target_card_ids']:d['target_card_ids'].append(pid)
addons=['level100.py','custom_skin.py','skin_iostore.py','skin_templates.zlib','private_bundles.py','private_bundles.json','native_skin_previews.json','editor_names.py']
for name in addons:d['appearance_files'][name]='pending'
for name in d['appearance_files']:d['appearance_files'][name]=sha((T/name).read_bytes())
d['appearance_overlay_sha256']=sha((T/'myleague_editor_runtime.py').read_bytes());d['hero_face_source']='User-supplied Android trials; private NHUL/NSPD namespace; original73runtime retained';d['body_RGB']='Private BGRA skin/body/lowbody textures; alpha preserved';f.write_text(json.dumps(d,indent=2))
with zipfile.ZipFile(P/'build/ui78-main.zip')as z:entries={n:z.read(n)for n in z.namelist()}
for folder in ['work/tools','livedata']:
 for f in(P/'build/payload'/folder).glob('*'):
  if f.is_file():entries['assets/gateway-release/'+folder+'/'+f.name]=f.read_bytes()
if(P/'build/classes5-ui79.dex').exists():entries['classes5.dex']=(P/'build/classes5-ui79.dex').read_bytes()
changed=sorted(n for n in entries if n.startswith('assets/gateway-release/')and n not in ['assets/gateway-release/release-manifest.json','assets/gateway-release/ui6-runtime-manifest.json'])
for name in ['release-manifest.json','ui6-runtime-manifest.json']:
 key='assets/gateway-release/'+name;d=json.loads(entries[key]);d['release_id'if name.startswith('release')else'version']='73-ui7.9-20261027';existing={r['path']for r in d['files']}
 for addon in addons+[f'livedata/{f.name}'for f in L.glob('pc930[56]_mobile_and.*')]:
  path=addon if addon.startswith('livedata/')else'work/tools/'+addon
  if path not in existing:d['files'].append({'path':path})
 for row in d['files']:
  path='assets/gateway-release/'+row['path']
  if path in entries:row.update(bytes=len(entries[path]),sha256=sha(entries[path]))
 entries[key]=json.dumps(d,indent=2).encode()
out=P/'build/UI79-INTERNAL-CANDIDATE-NOT-FULL.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in entries.items():z.writestr(n,b)
print('FULL_CANDIDATE_READY',out.stat().st_size)
