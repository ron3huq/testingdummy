from pathlib import Path
import json,re,hashlib
P=Path('/workspace/ronaldo-work/73-ui6');t=P/'payload/work/tools';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,name in [('pc9300','extras_bundle.json'),('pc9302','manager_bundle.json'),('pc9303','kits_bundle.json')]:
 rows={f.name:{'size':f.stat().st_size,'sha256':sha(f)}for f in(P/'payload/livedata').glob(stem+'_mobile_and.*')}
 if stem=='pc9303':
  f=P/'payload/livedata/dt870_mobile_and.cpk';rows[f.name]={'size':f.stat().st_size,'sha256':sha(f)}
 (t/name).write_text(json.dumps({'files':rows},indent=2))
for name,lib in[('noodle_hair.py','libnoodle_hair.so'),('select_team_runtime.py','libselect_team.so')]:
 f=t/name;s=f.read_text();s=re.sub(r"HOOK_SHA\s*=\s*'[a-f0-9]+'","HOOK_SHA='"+sha(t/lib)+"'",s);f.write_text(s)
p=t/'noodle_bundle.json';d=json.loads(p.read_text());d['native_sha256']=sha(t/'libnoodle_hair.so');d['appearance_files']={k:sha(t/k)for k in d['appearance_files']};d['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');d['editor_ui']='73-ui6-native-sleeves-persistent-runtime-restored-coaches';d.pop('rolled_cuffs',None);p.write_text(json.dumps(d,indent=2))
for f in t.glob('*.py'):compile(f.read_text(),str(f),'exec')
print('PINS_REFRESHED')
