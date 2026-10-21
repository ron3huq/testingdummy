from pathlib import Path
import ast,json,hashlib,re,zipfile,struct
from elftools.elf.elffile import ELFFile
r=Path(__file__).parent
files=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json']
for name in files:
 if name.endswith('.py'):ast.parse((r/name).read_text())
c=json.loads((r/'myleague_custom.json').read_text());old=json.loads((r.parent/'hotfix-v6/myleague_custom.json').read_text())
assert c['version']=='native-hotfix-v7.1' and len(c['classic_teams'])==12 and sum(len(t['slots']) for t in c['classic_teams'].values())==190 and len(c['classic_profiles'])==179
for tid in ['108','114','127','45','116','18961']:assert c['native_rosters'][tid]==old['native_rosters'][tid]
for pid,rule in old['card_overrides'].items():assert c['card_overrides'][pid]==rule
assert c['classic_teams']['1220']['slots'][8]['player_id']==70373039149482 and c['classic_teams']['1220']['slots'][10]['player_id']==88045755861672
for tid,t in c['classic_teams'].items():
 assert c['native_rosters'][tid]==[s['player_id'] for s in t['slots']]
 assert len({s['shirt'] for s in t['slots']})==len(t['slots'])
 assert len(t['formation'])==11 and all(0<=v<11 for v in t['set_piece_taker']+[t['responsibilities']['captain']])
for cid in ['125','549']:assert c['leagues'][cid]==old['leagues'][cid]
assert re.search("HOOK_SHA = '([^']+)'",(r/'select_team_runtime.py').read_text()).group(1)==hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()
keys=('native_rosters','base_overrides','card_overrides','base_adjustments','team_names','league_logos','shirt_overrides','global_player_rules','classic_teams','classic_profiles','visual_aliases','ovr_policy','match_environment','messi_ids','defender_skill_policy');pin={k:c[k] for k in keys};pin['leagues']=c['leagues']
assert hashlib.sha256(json.dumps(pin,sort_keys=True,separators=(',',':')).encode()).hexdigest()==re.search("EXPECTED_NATIVE_CONFIG_SHA='([^']+)'",(r/'myleague_worlds.py').read_text()).group(1)
with (r/'libselect_team.so').open('rb') as f:
 e=ELFFile(f)
 for s in e.iter_sections():
  if s.name.startswith('.rela'):
   for rel in s.iter_relocations():assert rel['r_info_type']==1027
reports=['native-validation.json','roster-source-validation.json','menu-validation.json','presentation-validation.json','worlds-validation.json','asia-pacific-validation.json','classic-gateway-validation.json','global-rules-validation.json','regression-validation.json','card-handlers-validation.json','corpus-validation.json','club-policy-validation.json','v7-rules-validation.json','environment-validation.json','entry-crash-validation.json']
for name in reports:
 row=json.loads((r/name).read_text());assert any(s in row['status'] for s in ['PASS','VALIDATED']),(name,row['status'])
stadium=json.loads((r/'stadium-capabilities.json').read_text());assert not any(x['snow_capability'] for x in stadium['rows'] if x['id'] in [1,7,30,51,52,85])
status=dict(version='native-hotfix-v7.1',status='ENTRY_CRASH_FIX_VALIDATED_DEVICE_UNTESTED_ENVIRONMENT_DISABLED',device_tested=False,classic_teams=12,classic_slots=190,classic_unique_ids=179,roster_era_accuracy='hybrid where unavailable; exact per-team exceptions documented',neutral_ovr=c['ovr_policy'],owned_database_rewritten=False,club_outcomes=c['club_outcome_policy'],stadium_100_guaranteed_removed_on_every_device=False,snow_verified_available_in_supplied_source=False,environment_policy=c['match_environment'],limits=['Phone match/render verification remains pending','Retro rosters include documented former-club substitutes; not all exactly match requested season','Original club assets reused; no historical-season kit textures imported','All stage hooks/probes and weather overrides disabled in7.1; original native stage selection retained','Snow/rain/random seasons and time disabled in7.1; fine/summer/day baseline retained','v7 incorrect no-argument member call crash reproduced at0x3033e64 reading0x28; removed in7.1','Neutral source-primary OVR excludes manager/conditional boosts and relocated-position OVR','No goal-minute CPU protocol; no fabricated late goals/pressing','Power Tackle, hair and long-sleeve edits from earlier requests remain unapplied'])
(r/'RELEASE_STATUS.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n')
extras=['HUONG_DAN.md','DOI_HINH_CO_DIEN.md','classic-replacements.json','RELEASE_STATUS.json']
name='efootxi-1.3.2-native-hotfix-v7.1.zip'
with zipfile.ZipFile(r/name,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(r/f,'install/work/tools/'+f)
 for f in extras:z.write(r/f,f)
 for f in reports+['stadium-capabilities.json']:z.write(r/f,'validation/'+f)
 for f in ['select_team.c','build.sh']:z.write(r/f,'source/'+f)
with zipfile.ZipFile(r/name) as z:assert z.testzip() is None
manifest=dict(status='PACKAGE_PASS',device_tested=False,files={f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in files},zip_sha256=hashlib.sha256((r/name).read_bytes()).hexdigest(),zip_bytes=(r/name).stat().st_size)
(r/'package-validation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
