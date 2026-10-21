from pathlib import Path
import ast,json,hashlib,re,zipfile
r=Path(__file__).parent
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_custom.json']
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
c=json.loads((r/'myleague_custom.json').read_text());old=json.loads((r.parent/'hotfix-v4.1/myleague_custom.json').read_text())
assert c['leagues']['125']['teams']==c['leagues']['125']['original_teams']
assert c['leagues']['549']['name']=='Asia-Pacific League' and c['leagues']['549']['legs']==3 and len(c['leagues']['549']['teams'])==8
assert set(c['league_logos'])=={'122','566','128','549'}
assert c['native_rosters']['127'][7:10]==[129369,119907,138000]
assert set(c['native_rosters']['127'])==set(old['native_rosters']['127'])
for tid,ids in old['native_rosters'].items():assert set(c['native_rosters'][tid])==set(ids)
for pid,row in old['card_overrides'].items():
 if pid!='106746580456800':assert c['card_overrides'][pid]==row
assert c['unresolved_skill_names']==['Power Tackle']
s=(r/'select_team_runtime.py').read_text();assert re.search("HOOK_SHA = '([0-9a-f]+)'",s).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
pin={k:c[k] for k in ('native_rosters','base_overrides','base_adjustments','team_names','league_logos')};pin['leagues']=c['leagues']
assert hashlib.sha256(json.dumps(pin,sort_keys=True,separators=(',',':')).encode()).hexdigest()==re.search("EXPECTED_NATIVE_CONFIG_SHA='([^']+)'",(r/'myleague_worlds.py').read_text()).group(1)
reports=['native-validation.json','roster-source-validation.json','menu-validation.json','presentation-validation.json','worlds-validation.json','asia-pacific-validation.json','regression-validation.json','card-handlers-validation.json','corpus-validation.json','club-policy-validation.json']
for n in reports:
 data=json.loads((r/n).read_text());assert any(word in data['status'] for word in ('PASS','VALIDATED')),(n,data['status'])
status=dict(version='native-hotfix-v5',status='COMPONENT_AND_GATEWAY_VALIDATED_DEVICE_UNTESTED',device_tested=False,baseline=dict(version='native-hotfix-v4.1',bayern_match_user_confirmed=True),asia_pacific=dict(competition_id=549,teams=8,legs=3,rounds=21,matches=84),eredivisie=dict(competition_id=125,restored_original18=True),new_card_ids=['106786040464076','106746580456800'],base_players=len(c['base_overrides']),relative_players=len(c['base_adjustments']),unimplemented=['Power Tackle: distinct native flag unverified','Prior hair-only/sleeve edits'],limits=['New native hooks and layouts need Android verification','Logo symbol selection verified, asset rendering/cache not executed','Native DB synthetic; gateway readiness stubbed; source save untouched'])
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
name='efootxi-1.3.2-native-hotfix-v5.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED) as z:
 for n in files:z.write(r/n,'install/work/tools/'+n)
 for n in ['HUONG_DAN.md','RELEASE_STATUS.json']:z.write(r/n,n)
 for n in reports:z.write(r/n,'validation/'+n)
 for n in ['select_team.c','build.sh']:z.write(r/n,'source/'+n)
manifest=dict(status='PACKAGE_PASS',device_tested=False,files={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in files},zip_sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),zip_bytes=(r/name).stat().st_size)
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
