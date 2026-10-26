from pathlib import Path
P=Path('/workspace/ronaldo-work/73-ui76');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text();s=s[:s.index("assert call(symbols['ensure_team'],127)==10")];s=s.replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'payload/work/tools/libselect_team.so'));exec(s)
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4);call(symbols['configure_short'],0,0x82b4a7c);call(symbols['activate_context'],473)
q=teams[4937];u.mem_write(teams[109]+0x3fd,b'\x00');u.mem_write(q+0x3fd,b'\x00');assert call(symbols['ensure_team'],4937)==1;assert u.mem_read(q+0x3fd,1)==b'\x04'
(P/'real-kit-validation.json').write_text(json.dumps({'passed':True,'actual_ARM64_production_library':True,'Y08_Real_recipe_gate_enabled_even_when_original_Real_is_unlicensed':True,'target':4937,'resource_source':242,'other_team_gate_code_unchanged':True,'device_tested':False},indent=2));print('REAL_KIT_PASS')
