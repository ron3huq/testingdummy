from pathlib import Path
import json,re,hashlib
r=Path(__file__).parent;c=json.loads((r/'myleague_custom.json').read_text());keys=('native_rosters','base_overrides','card_overrides','base_adjustments','team_names','league_logos','shirt_overrides','global_player_rules','classic_teams','classic_profiles','visual_aliases','ovr_policy','match_environment','messi_ids','defender_skill_policy');pin={k:c[k] for k in keys};pin['leagues']=c['leagues']
p=r/'myleague_worlds.py';p.write_text(re.sub("EXPECTED_NATIVE_CONFIG_SHA='[^']+'","EXPECTED_NATIVE_CONFIG_SHA='"+hashlib.sha256(json.dumps(pin,sort_keys=True,separators=(',',':')).encode()).hexdigest()+"'",p.read_text()))
p=r/'select_team_runtime.py';p.write_text(re.sub("HOOK_SHA = '[^']+'","HOOK_SHA = '"+hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()+"'",p.read_text()))
