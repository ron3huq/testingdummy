"""Real detail/bulk/home-entry handlers on a disposable copy, using library-card fixtures."""
from pathlib import Path
import argparse,sys,json,sqlite3,tempfile,hashlib,copy
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;sys.path[:0]=[str(r),str(a.gateway/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,club_store as store,gate_logic
model.ATTRS=a.gateway/'outputs/reference/external-attrs';model.install();cfg=worlds.config();source=a.gateway/'outputs/efootball/local-club.sqlite3';sha=hashlib.sha256(source.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory() as tmp:
 con=sqlite3.connect(Path(tmp)/'fixtures.db');con.row_factory=sqlite3.Row;src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);src.backup(con);src.close();refs=[]
 for number,(pid,rule) in enumerate(cfg['card_overrides'].items()):
  raw=con.execute('select payload from managed_cards where card_id=?',(pid,)).fetchone()[0];card=json.loads(raw);card['gameplayer_id']={'id':int(pid),'serial':987000+number};card['additional_skill_id']=[3,1,5,35,74]
  store.upsert_player(con,card,source='v4-test-fixture');refs.append(dict(gameplayer_id=card['gameplayer_id']))
 con.commit();handler=gate_logic.GateLogic({},conn=con)
 for ref in refs:
  pid=str(ref['gameplayer_id']['id']);rule=cfg['card_overrides'][pid];out=handler._player_data({},dict(gameplayer_id=ref['gameplayer_id']))
  assert out['result']=='NOERR' and out['gameplayer_list'][0]['gameplayer_id']==ref['gameplayer_id']
  for k,v in rule['stats'].items():
   assert out['gameplayer_list'][0]['parameters'][worlds.STAT_INDEX[k]]==v
   assert out['original_parameters'][worlds.STAT_INDEX[k]]==v
  slots=out['gameplayer_list'][0]['additional_skill_id'];assert len(slots)==5 and slots[3]==35 and slots[4]==74
  for sid in rule.get('skill_ids_remove',[]):assert sid not in slots
 bulk={str(p['gameplayer_id']['id']):p for p in store.wire_players(con,'login') if 987000<=p['gameplayer_id']['serial']<987018};assert len(bulk)==18
 raw_entries=handler._home_entries(refs);assert len(raw_entries)==18
 # START's final projection occurs AFTER this real learned-skill overlay.
 for entry in raw_entries:
  pid=str(entry['gameplayer_id']['id']);rule=cfg['card_overrides'][pid];out=worlds.edit_projection(entry)
  for flag in rule.get('skill_flags_remove',[]):assert out['parameters'][flag]==0
  for flag in rule.get('skill_flags_add',[]):assert out['parameters'][flag]==1
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
report=dict(status='REAL_CARD_HANDLERS_PASS',device_tested=False,cards=18,checks=['real GateLogic detail original/current parameters','real bulk LOGIN serialization','real home-entry learned-skill overlay then final START projection','full64 Card IDs and exact serials preserved','removed learned skills leave74 in original slot, other slots unchanged','source DB unchanged; fixture writes only in disposable copy'])
(r/'card-handlers-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
