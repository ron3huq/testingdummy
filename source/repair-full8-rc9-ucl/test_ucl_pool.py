"""Field changes must never select an absent or retro-mapped team ID."""
from pathlib import Path
import json,hashlib,collections

def run():
    source=Path(__file__).parent;root=source.parents[1];field=json.loads((source/'runtime/ucl_lp_draws.json').read_text());audit=json.loads((source/'native_pool.json').read_text());cfgpath=root/'assets/gateway-release/work/tools/myleague_custom.json';cfg=json.loads(cfgpath.read_text());teams=field['teams'];ids={r['team_id']for r in teams};metadata={r['team_id']:r for r in audit['teams']}
    assert len(teams)==len(ids)==36 and ids==set(metadata)
    assert 4219 in ids and 116 not in ids
    assert next(t for t in teams if t['team_id']==4219)['association']=='ITA'
    assert next(t for t in teams if t['team_id']==4219)['roster_count']==30
    assert not ids&{126,128,226,231,131,132}
    retro={t for key in('473','518')for t in cfg['leagues'][key]['teams']}|{int(k)for k in cfg.get('classic_teams',{})};assert not ids&retro
    assert hashlib.sha256(cfgpath.read_bytes()).hexdigest()==audit['rc7_roster_config_sha256']
    for t in teams:
        assert t['name']==metadata[t['team_id']]['name']and t['roster_count']>=18
        override=cfg['native_rosters'].get(str(t['team_id']))
        if override:assert len(override)==t['roster_count']
    assert collections.Counter(t['association']for t in teams)['ITA']==7
    print(json.dumps(dict(passed=True,teams=36,ajax_removed=True,como_id=4219,como_roster_count=30,italian_clubs=7,no_classic_or_retro_team_ids=True,missing_roster_ids_excluded=True),indent=2))
if __name__=='__main__':run()
