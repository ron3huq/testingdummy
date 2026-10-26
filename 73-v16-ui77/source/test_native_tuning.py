from pathlib import Path
P=Path('/workspace/ronaldo-work/73-ui77');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'payload/work/tools/libselect_team.so'));exec(s)
p=0x30010000;pid=88045755960841;call(symbols['configure_team'],0,0);row=call(symbols['editor_add_player'],pid,0,0)
for index,val in [(47,255),(48,250),(39,99),(70,0),(107,1),(125,1)]:assert call(symbols['editor_parameter'],row,index,val)==1
assert call(symbols['editor_parameter'],row,47,350)==0;assert call(symbols['editor_parameter'],row,48,251)==0;row2=call(symbols['editor_add_player'],pid+1,0,0);assert call(symbols['editor_parameter'],row2,107,1)==1;assert call(symbols['editor_commit'])==1
for cid in [0,473,518,122]:
 call(symbols['activate_context'],cid);call(symbols['editor_apply_player'],p,pid)
 assert [get(p,i)for i in [47,48,39,70,107,125]]==[255,250,99,0,1,1]
# Skill-only overrides work globally too, without forcing body/stat rows.
p2=p+0x800;call(symbols['activate_context'],0);call(symbols['editor_apply_player'],p2,pid+1);assert get(p2,107)==1
# independently confirm native byte overflow; no silent350->94 accepted by editor.
call(0x82a907c,p,47,350);assert get(p,47)==94
(P/'native-tuning-validation.json').write_text(json.dumps({'passed':True,'production_ARM64_editor':True,'native147_getter_readback_height255_weight250_jump99_and_skill_flags':True,'scopes':[0,473,518,122],'editor_rejects_height350':True,'original_native_height350_wraps_to94':True,'device_tested':False},indent=2));print('NATIVE_TUNING_PASS')
