from pathlib import Path
import zipfile,shutil,json,hashlib
r=Path(__file__).resolve().parent;O=r.parent;old=O.parent/'player-faces-v24';root=r/'deploy';tools=root/'work/tools';live=root/'livedata'
with zipfile.ZipFile(old/'Faces-v24-three-2017-and-new-2027.zip')as z:
 for name in z.namelist():
  if name.startswith('work/'):
   p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
for n in ['noodle_hair.py','libnoodle_hair.so']:shutil.copyfile(r/n,tools/n)
live.mkdir(exist_ok=True)
for e in ['pak','utoc','ucas']:shutil.copyfile(O/('container/pc9298_mobile_and.'+e),live/('pc9298_mobile_and.'+e))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((tools/'noodle_bundle.json').read_text());meta.update(version='player-faces-v25-2017-blender-v3-test',native_sha256=sha(tools/'libnoodle_hair.so'),asset_revision='v25-only-R2017-V3-on-working-2006-base',experimental_changed_card_ids=['88044950524330'],new_2017_profile='NV17',all_other_v24_assets_byte_exact=True,black_faces_verified_fixed=False,device_verified=False);meta['source_profiles']['88044950524330']='NV17-2006-base-R2017-Blender-V3';meta['files']={p.name:{'size':p.stat().st_size,'sha256':sha(p)}for p in sorted(live.iterdir())};(tools/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
s=(old/'source/validate_runtime.py').read_text().replace('v24','v25').replace('V24','V25').replace('three-2017-new-sources','2017-blender-v3-test').replace('+42','+43').replace('PLUS42','PLUS43');(r/'validate_runtime.py').write_text(s)
print('V25_STAGED')
