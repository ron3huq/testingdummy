from pathlib import Path
import ast,json,hashlib,re,zipfile
r=Path(__file__).parent
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_custom.json']
for n in files:
 if n.endswith('.py'):ast.parse((r/n).read_text())
c=json.loads((r/'myleague_custom.json').read_text());old=json.loads((r.parent/'hotfix-v5/myleague_custom.json').read_text())
assert len(c['classic_teams'])==12 and sum(len(t['slots']) for t in c['classic_teams'].values())==175
assert len(json.loads((r/'classic-replacements.json').read_text())['rows'])==47
for t in c['classic_teams'].values():assert len(set(s['shirt'] for s in t['slots']))==len(t['slots'])
assert set(c['native_rosters']['127'])==set(old['native_rosters']['127']) and c['shirt_overrides']['127']=={'47287':9,'119907':14,'129369':17,'138000':10}
for cid in ['125','549']:assert c['leagues'][cid]==old['leagues'][cid]
assert c['card_overrides']['105820209653455']['stats']==dict(acceleration=88,speed=88,tackling=90,defensive_awareness=90)
for pid,row in old['card_overrides'].items():assert c['card_overrides'][pid]==row
for pid in [17592722922839,88044145248321,88044145253792,88045755829934,88038776539586,88039044943928,88045755960771]:assert str(pid) in c['classic_profiles']
s=(r/'select_team_runtime.py').read_text();assert re.search("HOOK_SHA = '([0-9a-f]+)'",s).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
keys=('native_rosters','base_overrides','card_overrides','base_adjustments','team_names','league_logos','shirt_overrides','global_player_rules','classic_teams','classic_profiles');pin={k:c[k] for k in keys};pin['leagues']=c['leagues'];assert hashlib.sha256(json.dumps(pin,sort_keys=True,separators=(',',':')).encode()).hexdigest()==re.search("EXPECTED_NATIVE_CONFIG_SHA='([^']+)'",(r/'myleague_worlds.py').read_text()).group(1)
reports=['native-validation.json','roster-source-validation.json','menu-validation.json','presentation-validation.json','worlds-validation.json','asia-pacific-validation.json','classic-gateway-validation.json','global-rules-validation.json','regression-validation.json','card-handlers-validation.json','corpus-validation.json','club-policy-validation.json']
for n in reports:
 data=json.loads((r/n).read_text());assert any(word in data['status'] for word in ['PASS','VALIDATED']),(n,data['status'])
status=dict(version='native-hotfix-v6',status='COMPONENT_AND_GATEWAY_VALIDATED_DEVICE_UNTESTED',device_tested=False,baseline_bayern127_user_confirmed_on_v4_1=True,classic_teams=12,classic_slots=175,temporary_substitutions=47,classic_unique_ids=172,neutral_npc_ovr_cap=89,own_database_rewritten=False,player_rules=c['global_player_rules'],club_outcomes=c['club_outcome_policy'],limits=['New full64 classic NPC rosters/asset paths need phone validation','OVR cap is neutral base calculation; manager/conditional effects untested','No CPU goal-minute field; late-conceded events not implemented','Power Tackle, old hair/sleeve edits remain unverified/unapplied'])
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
name='efootxi-1.3.2-native-hotfix-v6.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED) as z:
 for n in files:z.write(r/n,'install/work/tools/'+n)
 for n in ['HUONG_DAN.md','DOI_HINH_CO_DIEN.md','classic-replacements.json','RELEASE_STATUS.json']:z.write(r/n,n)
 for n in reports:z.write(r/n,'validation/'+n)
 for n in ['select_team.c','build.sh']:z.write(r/n,'source/'+n)
manifest=dict(status='PACKAGE_PASS',device_tested=False,files={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in files},zip_sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),zip_bytes=(r/name).stat().st_size)
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
