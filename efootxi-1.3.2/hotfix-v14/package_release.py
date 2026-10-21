from pathlib import Path
from elftools.elf.elffile import ELFFile
import ast,json,hashlib,re,zipfile
r=Path(__file__).parent;old=r.parent/'hotfix-v13';files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json']
c=json.loads((r/'myleague_custom.json').read_text());before=json.loads((old/'myleague_custom.json').read_text());assert {k for k in c if c[k]!=before[k]}=={'version','requested_appearance'}
assert c['version']=='native-hotfix-v14' and c['requested_appearance']['hair_copy']['target']=='88044950524330'
for name in ['myleague_realism.py','myleague_balance.py','gateway_runtime.py']:assert (r/name).read_bytes()==(old/name).read_bytes(),name
assert (r/'select_team.c').read_bytes().startswith((r.parent/'hotfix-v10/select_team.c').read_bytes())
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
with (r/'libselect_team.so').open('rb')as f:
 elf=ELFFile(f)
 for s in elf.iter_sections():
  if s.name.startswith('.rela'):
   for rel in s.iter_relocations():assert rel['r_info_type']==1027
reports=['appearance-runtime-validation.json','appearance-validation.json','native-validation.json','cached-detours-validation.json','entry-crash-validation.json','regression-validation.json']
for n in reports:assert any(x in json.loads((r/n).read_text())['status'] for x in ['PASS','VALIDATED'])
status={'version':'native-hotfix-v14','status':'OBSERVED_DEVICE_ID_REPLAY_VALIDATED_DEVICE_UNTESTED','device_tested':False,'previous_device_result':{'version':'native-hotfix-v13','competition':518,'build_calls':24,'build_matches':0,'shirt_calls':0,'entity_calls':0,'observed_ronaldo_id':'88044950524330','requested_original_id_present':False,'appearance_sleeve_applies':0},'appearance':c['requested_appearance'],'explicit_target_ids':['89138556572074','88044950524330'],'render_id_alias_relationship_proven':False,'shared_base_aliases_enabled':False,'simulation_code_byte_identical_to':'native-hotfix-v10','v10_native_source_preserved_as_exact_prefix':True,'source_tables_modified':False,'source_db_modified':False,'hair_transplant_applied':False,'new_native_entries':[],'new_status_fields':['appearance_build_matches_by_id','appearance_last_applied_id','appearance_build_after'],'unresolved_roster_status':{'1220':14,'1221':14,'meaning':'existing slot PlayerKey.kind low32 is not0; roster write safely skipped','guard_retained':True},'limits':['Android mesh/texture/render unverified','22 device-observed IDs replayed with modeled DB/resource boundaries','Roster14 requires actual slot-key data before changing its guard','Hair transplant remains unimplemented']}
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n')
name='efootxi-1.3.2-native-hotfix-v14-long-sleeve.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED)as z:
 for n in files:z.write(r/n,'install/work/tools/'+n)
 for n in ['HUONG_DAN.md','NGOAI_HINH.md','RELEASE_STATUS.json']:z.write(r/n,n)
 for n in reports:z.write(r/n,'validation/'+n)
 for n in ['select_team.c','build.sh','refresh_hashes.py','validate_appearance.py','validate_appearance_runtime.py','validate_native.py','validate_cached_detours.py','validate_entry_crash.py','validate_regressions.py']:z.write(r/n,'source/'+n)
 for n in ['research-face-redirects.json','research-model-assets.json']:z.write(r/n,'research/'+n)
with zipfile.ZipFile(r/name)as z:assert z.testzip()is None and len([n for n in z.namelist()if n.startswith('install/')])==7
manifest={'status':'PACKAGE_PASS','device_tested':False,'files':{n:hashlib.sha256((r/n).read_bytes()).hexdigest()for n in files},'zip_sha256':hashlib.sha256((r/name).read_bytes()).hexdigest(),'zip_bytes':(r/name).stat().st_size}
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
