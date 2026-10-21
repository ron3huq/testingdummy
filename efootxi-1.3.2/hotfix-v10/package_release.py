from pathlib import Path
import ast,hashlib,json,re,zipfile
r=Path(__file__).parent;old=r.parent/'hotfix-v9';files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json']
c=json.loads((r/'myleague_custom.json').read_text());before=json.loads((old/'myleague_custom.json').read_text());assert c['version']=='native-hotfix-v10'
for k in ['native_rosters','classic_teams','classic_profiles','base_overrides','card_overrides','base_adjustments','team_names','league_names','league_logos','shirt_overrides','global_player_rules','visual_aliases','ovr_policy','match_environment','defender_skill_policy']:
 assert c[k]==before[k],k
for name in ['select_team.c','libselect_team.so','myleague_balance.py']:assert (r/name).read_bytes()==(old/name).read_bytes(),name
assert {k:v['teams'] for k,v in c['leagues'].items()}=={k:v['teams'] for k,v in before['leagues'].items()}
for name in files:
 if name.endswith('.py'):ast.parse((r/name).read_text())
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
keys=('native_rosters','base_overrides','card_overrides','base_adjustments','team_names','league_logos','shirt_overrides','global_player_rules','classic_teams','classic_profiles','visual_aliases','ovr_policy','match_environment','messi_ids','defender_skill_policy','league_names');pin={k:c[k] for k in keys};pin['leagues']=c['leagues']
assert hashlib.sha256(json.dumps(pin,sort_keys=True,separators=(',',':')).encode()).hexdigest()==re.search("EXPECTED_NATIVE_CONFIG_SHA='([^']+)'",(r/'myleague_worlds.py').read_text()).group(1)
reports=['simulation-validation.json','regression-validation.json','classic-gateway-validation.json','asia-pacific-validation.json','environment-validation.json']
for n in reports:assert 'PASS' in json.loads((r/n).read_text())['status']
sim=json.loads((r/'simulation-validation.json').read_text());assert sum(x['matches'] for x in sim['reports'].values())==6744
baseline=['native-validation.json','cached-detours-validation.json','stage-detours-validation.json','ui-names-validation.json','weather-validation.json','live-contract-validation.json']
status=dict(version=c['version'],status='V10_CPU_SIMULATION_VALIDATED_DEVICE_UNTESTED',device_tested=False,native_binary_unchanged_from='v9',native_sha256=hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest(),previous_results_rewritten=False,rosters_roles_shirts_stats_proficiency_weather_unchanged=True,simulation=c['simulation_policy'],test_matches=6744,metrics=sim['reports'],limits=['CPU simulation only; no fake injuries/cards/goal minutes','Probability and seasonal totals approximate; user match immutable','Scottish retains12teams22rounds','No Android device/render test; prior missing-kit-texture limits persist'])
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n')
name='efootxi-1.3.2-native-hotfix-v10.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED) as z:
 for n in files:z.write(r/n,'install/work/tools/'+n)
 for n in ['HUONG_DAN.md','DOI_HINH_CO_DIEN.md','classic-replacements.json','RELEASE_STATUS.json']:z.write(r/n,n)
 for n in reports:z.write(r/n,'validation/'+n)
 for n in baseline:z.write(old/n,'validation/baseline-v9/'+n)
 for n in ['select_team.c','build.sh','refresh_hashes.py','validate_simulation.py','validate_regressions.py','validate_classic_gateway.py','validate_environment.py','validate_asia_pacific.py']:z.write(r/n,'source/'+n)
with zipfile.ZipFile(r/name) as z:assert z.testzip() is None and len([n for n in z.namelist() if n.startswith('install/')])==7
manifest=dict(status='PACKAGE_PASS',device_tested=False,native_binary_unchanged_from='v9',files={n:hashlib.sha256((r/n).read_bytes()).hexdigest()for n in files},zip_sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),zip_bytes=(r/name).stat().st_size)
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
