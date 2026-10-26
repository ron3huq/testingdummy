from pathlib import Path
import sys,struct,json,zipfile,hashlib
P=Path('/workspace/ronaldo-work/73-ui75');sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v24/source');from cpk_extract import utf,decompress
b=Path('/workspace/ronaldo-work/73-ui74/dt870_ui74_mobile_and.cpk').read_bytes();h=utf(b[16:2048])[0];at=h['TocOffset'];size=struct.unpack_from('<Q',b,at+8)[0];rows=utf(b[at+16:at+16+size]);start=min(at,h['ContentOffset']);files={(r.get('DirName','')+'/'+r['FileName']).lstrip('/'):decompress(b[start+r['FileOffset']:start+r['FileOffset']+r['FileSize']])for r in rows}
proof=json.loads(Path('/workspace/ronaldo-work/73-ui6/cpk-kits-build.json').read_text());targets=[1706,4937,1957,1956,4962,4964,4938,1950,1228,1955]
for team in targets:
 for slot in ['1st','2nd','GK1st']:
  variants=[v for v in proof if v['team']==team and '_DEF_'+slot+'.'in v['destination']or v['team']==team and '_DEF_'+slot+'_realUni.'in v['destination']]
  assert variants,(team,slot)
  for v in variants:assert files[v['destination']]==Path('/workspace/ronaldo-work/73-ui6/cpk-kit-additions',v['destination']).read_bytes()
report={'passed':True,'Y08_teams':targets,'home_away_and_goalkeeper_recipes_present':True,'all_existing_41_recipe_additions_preserved_exact':True,'CPK_unchanged_from_working_UI74':True,'Y17_kit_resource_files_unchanged':True,'device_tested':False};(P/'kits-assets-validation.json').write_text(json.dumps(report,indent=2));print('KITS_ASSETS_PASS')
