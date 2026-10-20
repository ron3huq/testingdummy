"""Compare complete uint64 gameplayer IDs in the real supplied Player.bin."""
import argparse,json,struct,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--player-bin',required=True,type=Path);a=p.parse_args();r=Path(__file__).parent
raw=a.player_bin.read_bytes();assert len(raw)%400==0
full={struct.unpack_from('<Q',raw,i+8)[0] for i in range(0,len(raw),400)}
cfg=json.loads((r/'myleague_custom.json').read_text());old=json.loads(Path('/workspace/analysis/my-league/hotfix-v4/myleague_custom.json').read_text())
missing={tid:[pid for pid in ids if pid not in full] for tid,ids in cfg['native_rosters'].items()};assert not any(missing.values()),missing
assert 59835 not in full and 52776558193083 in full and (52776558193083&0xffffffff)==59835
assert all(pid in full for ids in cfg['simulation_rosters'].values() for pid in ids)
assert cfg['native_rosters']['127'][:11]==old['native_rosters']['127'][:11]
assert len(cfg['native_rosters']['127'])==22 and set(old['native_rosters']['127'])-set(cfg['native_rosters']['127'])=={59835}
report=dict(status='EXACT64_SOURCE_AUDIT_PASS',source_sha256=hashlib.sha256(raw).hexdigest(),record_size=400,id_offset=8,id_width=8,native_roster_counts={t:len(ids) for t,ids in cfg['native_rosters'].items()},missing_exact_ids=missing,removed_invalid_base_id=59835,existing_full_card_id=52776558193083,starting_xi_unchanged=True,limits='Source ID existence; Android runtime match still requires device verification.')
(r/'roster-source-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
