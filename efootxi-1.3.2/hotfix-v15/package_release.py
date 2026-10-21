from pathlib import Path
from elftools.elf.elffile import ELFFile
import ast,json,hashlib,re,zipfile,copy
r=Path(__file__).parent;old=r.parent/'hotfix-v14'
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json']
c=json.loads((r/'myleague_custom.json').read_text());before=json.loads((old/'myleague_custom.json').read_text())
assert {k for k in c if c[k]!=before[k]}=={'version','requested_appearance'} and c['version']=='native-hotfix-v15'
assert c['requested_appearance']['sleeve_copy']['rolled_trial']['enabled']is False
for n in ['gateway_runtime.py','myleague_realism.py','myleague_balance.py']:assert (r/n).read_bytes()==(old/n).read_bytes()
assert (r/'select_team.c').read_bytes().startswith((r.parent/'hotfix-v10/select_team.c').read_bytes())
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
with (r/'libselect_team.so').open('rb')as f:
 for section in ELFFile(f).iter_sections():
  if section.name.startswith('.rela'):
   for rel in section.iter_relocations():assert rel['r_info_type']==1027
reports=['appearance-runtime-validation.json','appearance-validation.json','native-validation.json','cached-detours-validation.json','entry-crash-validation.json','regression-validation.json']
for n in reports:assert any(x in json.loads((r/n).read_text())['status']for x in ['PASS','VALIDATED'])
assert json.loads((r/'appearance-validation.json').read_text())['status']=='SCOPED_NAMED_SLEEVES_AND_GATED_TRIAL_PASS'
status=dict(version='native-hotfix-v15',status='SCOPED_LONG_SLEEVES_VALIDATED_SEPARATE_UNVERIFIED_ROLLED_VALUE_TRIAL',device_tested=False,prior_device_confirmation={'version':'native-hotfix-v14','normal_long_sleeves_worked':True,'source':'user confirmation'},competition_targets=c['requested_appearance']['sleeve_copy']['competition_targets'],legacy_global_ids=['89138556572074','88044950524330'],trial=c['requested_appearance']['sleeve_copy']['rolled_trial'],trial_visual_proven=False,simulation_code_byte_identical_to='native-hotfix-v10',v10_native_source_preserved_as_exact_prefix=True,source_tables_modified=False,source_db_modified=False,hair_transplant_applied=False,new_native_entries=[],new_status_fields=['appearance_policy_matches','appearance_trial_enabled','appearance_trial_error'],limits=['New targets not device-tested','Packed mode3/config2 is unused in supplied source records; not identified as rolled sleeves','Native trial forwards config2 to LoadUniShirt with short-resource branch, not proof of mesh result','Database/resource boundaries modeled in Unicorn','Roster14 from previous device log remains unchanged'])
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n')
trial=copy.deepcopy(c);trial['requested_appearance']['sleeve_copy']['rolled_trial']['enabled']=True
trial_bytes=(json.dumps(trial,indent=2,ensure_ascii=False)+'\n').encode();(r/'myleague_custom-gullit-trial.json').write_bytes(trial_bytes)
source=['select_team.c','build.sh','refresh_hashes.py','validate_appearance.py','validate_appearance_runtime.py','validate_native.py','validate_cached_detours.py','validate_entry_crash.py','validate_regressions.py','package_release.py']
variants={}
for variant,name in [('standard','efootxi-1.3.2-native-hotfix-v15-long-sleeve.zip'),('gullit_trial','efootxi-1.3.2-native-hotfix-v15-gullit-sleeve-trial.zip')]:
 payload={n:(trial_bytes if n=='myleague_custom.json'and variant=='gullit_trial'else(r/n).read_bytes())for n in files}
 with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED)as z:
  for n,data in payload.items():z.writestr('install/work/tools/'+n,data)
  for n in ['HUONG_DAN.md','NGOAI_HINH.md','RELEASE_STATUS.json','sleeve-targets.json']:z.write(r/n,n)
  for n in reports:z.write(r/n,'validation/'+n)
  for n in source:z.write(r/n,'source/'+n)
  z.write(r/'sleeve-assets.json','research/sleeve-assets.json')
 with zipfile.ZipFile(r/name)as z:assert z.testzip()is None and len([n for n in z.namelist()if n.startswith('install/')])==7
 variants[variant]=dict(filename=name,trial_enabled=variant=='gullit_trial',sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),bytes=(r/name).stat().st_size,files={n:hashlib.sha256(data).hexdigest()for n,data in payload.items()})
assert {n for n in files if variants['standard']['files'][n]!=variants['gullit_trial']['files'][n]}=={'myleague_custom.json'}
manifest=dict(status='PACKAGE_PASS',device_tested=False,variants=variants)
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
