from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
pid=89136418985303;p=0x30000000
for i in range(147):call(0x82a907c,p,i,1)
before=[get(p,i)for i in range(147)];call(symbols['configure_team'],0,0);row=call(symbols['editor_add_player'],pid,0,0);assert row
assert call(symbols['editor_parameter'],row,47,190)==1;assert call(symbols['editor_parameter'],row,48,88)==1;assert call(symbols['editor_commit'])==1
for cid in[0,473,518,122]:
 call(symbols['activate_context'],cid);call(symbols['editor_apply_player'],p,pid);after=[get(p,i)for i in range(147)];expected=list(before);expected[47:49]=[190,88];assert after==expected
report={'passed':True,'checks':['unchanged production ARM64 editor writes exact height47/weight48','original73 native parameter getters read back190cm/88kg','all other145 parameters unchanged','works global/Y08/Y17/other competition scopes'],'synthetic_records':True,'device_tested':False}
Path('/workspace/ronaldo-work/73-ui7/native-dimensions-validation.json').write_text(json.dumps(report,indent=2));print('NATIVE_DIMENSIONS_PASS')
