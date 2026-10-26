from pathlib import Path
import sys,json,sqlite3,types,struct
P=Path('/workspace/ronaldo-work/73-ui76');sys.path.insert(0,str(P/'payload/work/tools'))
# Actual protected identity validation: preserve ownership and serial uniqueness.
exec(Path('/workspace/ronaldo-work/73-ui75/inspect_wire.py').read_text().split('import my_league')[0])
import player_identity,multi_cards
c=sqlite3.connect(':memory:');c.execute('CREATE TABLE gameplayers(id INTEGER,serial INTEGER,json TEXT)');ids=[88044950524330,89135066911146]
for i,pid in enumerate(ids):c.execute('INSERT INTO gameplayers VALUES(?,?,?)',(pid,i+1,'{}'))
squad={'player_list':[{'gameplayer_id':{'id':pid,'serial':i+1}}for i,pid in enumerate(ids)]}
try:player_identity.validate_squad(c,squad);raise AssertionError('stock unexpectedly allowed')
except ValueError as e:assert 'Cristiano'in str(e)
multi_cards.install();player_identity.validate_squad(c,squad)
player_identity.validate_match_request(c,'CMD_SET_MYCLUB_SPECIAL_DREAM_SQUAD_INFO',{'special_squad_data':{'squad_data':squad}})
for bad in [{'player_list':[squad['player_list'][0]]*2},{'player_list':[{'gameplayer_id':{'id':999,'serial':3}}]}]:
 try:player_identity.validate_squad(c,bad);raise AssertionError('invalid allowed')
 except ValueError:pass
import player_model as m
assert m.baseline(str(ids[0])) and len(m.baseline(str(ids[0])))==11
# Run production native hook with a delegate that simulates the late base-body reset.
s=Path('/workspace/ronaldo-work/73-ui75/test_model_native.py').read_text();s=s.replace("P=Path('/workspace/ronaldo-work/73-ui75')","P=Path('/workspace/ronaldo-work/73-ui76')").replace("/workspace/ronaldo-work/73-ui75/payload/work/tools/libselect_team.so","/workspace/ronaldo-work/73-ui76/payload/work/tools/libselect_team.so")
# Old test builds library path dynamically from P; retained165 native decoder checks.
exec(s)
# Existing build hook wrote final model values after original delegate returned.
for off in [0x20,0x14,8,0x18,0xc,0x10,0x30,0x28,0x1c,0x24,0x2c]:assert abs(struct.unpack('<f',u.mem_read(spec+0x10+off,4))[0]+1)<1e-6
# Exact requested card sleeve and other four Ronaldo modes.
for card,mode in [(89138556572074,0),(88044950524330,1),(89135066911146,1),(89136418985303,1),(89136418985302,1)]:
 w(spec+8,'Q',card);call(symbols['appearance_build_hook'],dest,spec);assert struct.unpack('<I',u.mem_read(dest+0x50,4))[0]==mode
report={'passed':True,'stock_restriction_reproduced':True,'two_owned_Ronaldo_cards_accepted':True,'duplicate_instance_and_unowned_cards_rejected':True,'baseline11_fields_from_actual_appearance_table':True,'native_final_body_values_after_builder':True,'requested_short_sleeve_card_only':True,'synthetic_records':True,'device_tested':False};(P/'changes-validation.json').write_text(json.dumps(report,indent=2));print('CHANGES_PASS')
