from pathlib import Path
P=Path('/workspace/73-ui712');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/apk/assets/gateway-release/work/tools/libselect_team.so'));exec(s)
pid=123456789876;other=123456789877;cfg=0x30020000;vec=0x30021000
n=call(symbols['editor_add_player'],pid,0,0);assert n;palette={0:0xff00aaff,1:0xff112233,4:0xffff0000,5:0xff00ff00,6:0xff0000ff,7:0xffffff00,8:0xffaa00bb,9:0xff554433}
for typ,color in palette.items():assert call(symbols['editor_accessory_color'],n,typ,color)==1
for typ in [2,3,10,17,23]:assert call(symbols['editor_accessory_color'],n,typ,0xffabcdef)==0
assert call(symbols['editor_accessory_color'],n,4,0x00ff0000)==0;call(symbols['editor_commit'])
u.mem_write(cfg,bytes(0x230));w(cfg+0x210,'QQQ',vec,vec,vec+18*12)
for typ in range(18):call(0x68cff80,cfg,typ,0xffeeddcc,1)
before=bytes(u.mem_read(vec,18*12));call(symbols['editor_apply_accessories'],cfg,pid)
for typ in range(18):
 expected=palette.get(1)if typ in [2,3]else palette.get(typ,0xffeeddcc)
 assert struct.unpack('<I',u.mem_read(vec+typ*12+4,4))[0]==expected,(typ,hex(expected));assert u.mem_read(vec+typ*12+8,1)==b'\1'
# Native FColor is stored BGRA in little endian: red carries B0 G0 R255 A255.
assert bytes(u.mem_read(vec+4*12+4,4))==bytes([0,0,255,255])
u.mem_write(vec,before);call(symbols['editor_apply_accessories'],cfg,other);assert bytes(u.mem_read(vec,18*12))==before
(P/'accessory-colors-native-validation.json').write_text(json.dumps({'passed':True,'exact_card_scope':True,'eight_exposed_types':list(palette),'native_append_routine_used':True,'opaque_BGRA_word_layout':True,'unsupported_goalkeeper_flags_and_transparent_alpha_rejected':True,'visibility_flags_not_modified_by_color':True,'unrelated_player_unchanged':True,'Android_tested':False},indent=2));print('ACCESSORY_COLORS_NATIVE_PASS')
