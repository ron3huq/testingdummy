from pathlib import Path
from elftools.elf.elffile import ELFFile
import json,ast,hashlib,re,zipfile,sys,base64
r=Path(__file__).parent;app=r.parent/'editor-app';sys.path.insert(0,str(r));import myleague_editor_runtime as editor
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json','myleague_editor_runtime.py','myleague_editor.json']
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
for n in ['myleague_realism.py','myleague_balance.py','gateway_runtime.py']:assert (r/n).read_bytes()==(r.parent/'hotfix-v15'/n).read_bytes()
with(r/'libselect_team.so').open('rb')as f:
 e=ELFFile(f)
 for section in e.iter_sections():
  if section.name.startswith('.rela'):
   for rel in section.iter_relocations():assert rel['r_info_type']==1027
cfg=editor.validate(json.loads((r/'myleague_editor.json').read_text()));assert cfg['players']==[]and cfg['teams']==[]and cfg['weather']['summer_end']==7 and cfg['weather']['winter_start']==8 and cfg['weather']['winter_end']==14
assert json.loads((r/'myleague_custom.json').read_text())['requested_appearance']['sleeve_copy']['rolled_trial']['enabled']is False
reports=['native-validation.json','cached-detours-validation.json','entry-crash-validation.json','regression-validation.json','appearance-runtime-validation.json','appearance-validation.json','weather-validation.json','editor-validation.json']
for n in reports:assert any(tag in json.loads((r/n).read_text())['status']for tag in ['PASS','VALIDATED'])
assert json.loads((app/'browser-validation.json').read_text())['status']=='BROWSER_EXPORT_IMPORT_PERSISTENCE_PASS'
html=(app/'MyLeagueEditor.html').read_text();embedded=json.loads(re.search(r'<script id="payload" type="application/json">(.*?)</script>',html,re.S).group(1));assert len(embedded)==8
for n,v in embedded.items():assert base64.b64decode(v)==(r/n).read_bytes(),n
source=['select_team.c','build.sh','refresh_hashes.py','myleague_editor_runtime.py','validate_native.py','validate_cached_detours.py','validate_entry_crash.py','validate_regressions.py','validate_appearance_runtime.py','validate_appearance.py','validate_weather.py','validate_editor.py','package_release.py']
name='efootxi-1.3.2-native-hotfix-v16-editor-weather.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED)as z:
 for n in files:z.write(r/n,'install/work/tools/'+n)
 for n in ['HUONG_DAN.md','NGOAI_HINH.md','RELEASE_STATUS.json']:z.write(r/n,n)
 for n in reports:z.write(r/n,'validation/'+n)
 for n in source:z.write(r/n,'source/'+n)
 z.write(app/'browser-validation.json','validation/browser-validation.json')
with zipfile.ZipFile(r/name)as z:assert z.testzip()is None and len([n for n in z.namelist()if n.startswith('install/')])==9
appzip='MyLeagueStudio-v16-offline.zip'
with zipfile.ZipFile(app/appzip,'w',zipfile.ZIP_DEFLATED)as z:
 for n in ['MyLeagueEditor.html','HUONG_DAN.md','RELEASE_STATUS.json']:z.write(app/n,n)
 for n in ['browser-validation.json','embedded-payload-sha256.json']:z.write(app/n,'validation/'+n)
 for n in ['editor-validation.json','weather-validation.json']:z.write(r/n,'validation/'+n)
with zipfile.ZipFile(app/appzip)as z:assert z.testzip()is None and z.read('MyLeagueEditor.html')==(app/'MyLeagueEditor.html').read_bytes()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'status':'PACKAGE_PASS','device_tested':False,'runtime':{'filename':name,'sha256':sha(r/name),'bytes':(r/name).stat().st_size,'files':{n:sha(r/n)for n in files}},'app':{'filename':appzip,'sha256':sha(app/appzip),'bytes':(app/appzip).stat().st_size,'html_sha256':sha(app/'MyLeagueEditor.html')},'browser_generated_zip_validated':True,'trial_retired':True}
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
