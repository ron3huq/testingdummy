from pathlib import Path
from elftools.elf.elffile import ELFFile
import json,ast,hashlib,re,zipfile,base64
r=Path(__file__).parent;a=r.parent/'editor-v18'
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json','myleague_editor_runtime.py','myleague_editor.json','myleague_packs.py','myleague_team_snapshot.py']
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
for n in ['gateway_runtime.py','myleague_realism.py','myleague_balance.py','myleague_packs.py']:assert(r/n).read_bytes()==(r.parent/'hotfix-v17'/n).read_bytes(),n
old=json.loads((r.parent/'hotfix-v17/myleague_custom.json').read_text());new=json.loads((r/'myleague_custom.json').read_text());old.pop('version');new.pop('version');assert old==new
with(r/'libselect_team.so').open('rb')as f:
 e=ELFFile(f);names={s.name for s in e.get_section_by_name('.dynsym').iter_symbols()};assert 'editor_body'not in names and {'team_capture_copy','team_capture_generation','editor_team_plan'}<=names
 for sec in e.iter_sections():
  if sec.name.startswith('.rela'):
   for rel in sec.iter_relocations():assert rel['r_info_type']==1027
reports=['native-validation.json','cached-detours-validation.json','entry-crash-validation.json','regression-validation.json','appearance-runtime-validation.json','appearance-validation.json','weather-validation.json','editor-validation.json','snapshot-validation.json','packs-validation.json']
for n in reports:assert any(tag in json.loads((r/n).read_text())['status']for tag in ['PASS','VALIDATED'])
assert json.loads((a/'catalog-validation.json').read_text())['no_inferred_team_lineups']is True
assert json.loads((a/'browser-validation.json').read_text())['passive_snapshot_import']is True
html=(a/'MyLeagueEditor.html').read_text();embedded=json.loads(re.search(r'<script id="payload" type="application/json">(.*?)</script>',html,re.S).group(1));assert len(embedded)==10
for n,b64 in embedded.items():assert base64.b64decode(b64)==(r/n).read_bytes()
def zipwrite(path,pairs):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)as z:
  for source,target in pairs:z.write(source,target)
 with zipfile.ZipFile(path)as z:assert z.testzip()is None
upgrade=r/'efootxi-v18-lineup-readback-update.zip'
pairs=[(r/n,'install/work/tools/'+n)for n in files if n!='myleague_editor.json']+[(r/n,n)for n in ['HUONG_DAN.md','NGHIEN_CUU.md','RELEASE_STATUS.json']]+[(r/n,'validation/'+n)for n in reports]
zipwrite(upgrade,pairs)
with zipfile.ZipFile(upgrade)as z:
 runtime=[n for n in z.namelist()if n.startswith('install/')];assert len(runtime)==10 and all(not n.endswith('/myleague_editor.json')for n in runtime)
app=a/'MyLeagueStudio-v18-offline.zip';pairs=[(a/n,n)for n in ['MyLeagueEditor.html','HUONG_DAN.md','NGHIEN_CUU.md','RELEASE_STATUS.json']]+[(a/n,'validation/'+n)for n in ['browser-validation.json','catalog-validation.json','embedded-payload-sha256.json']]+[(r/n,'validation/'+n)for n in ['editor-validation.json','snapshot-validation.json']];zipwrite(app,pairs)
report={'status':'LINEUP_UPDATE_PRESERVES_PROJECT_AND_APP_PAYLOAD_PASS','device_tested':False,'bootstrap_update_files':10,'custom_export_files':11,'existing_project_json_not_shipped_in_bootstrap':True,'hair_face_body_changes_included':False,'files':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in [upgrade,app]},'runtime_hashes':{n:hashlib.sha256((r/n).read_bytes()).hexdigest()for n in files}}
(r/'package-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
