from pathlib import Path
P=Path('/tmp/73-ui710');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE
# Six real native accessory enums, including two mutually exclusive tights families.
import sys
mode=int(sys.argv[1])if len(sys.argv)>1 else 2
card=88044950524330;config=0x30020000;vector=0x30021000
call(symbols['configure'],0,0,0,0,0)
n=call(symbols['editor_add_player'],card,0,mode);assert n
for typ,gear_mode in [(0,1),(1,2),(4,2),(5,1),(6,2),(7,2)]:assert call(symbols['editor_accessory'],n,typ,gear_mode)==1
for typ in [2,3,8,17,99]:assert call(symbols['editor_accessory'],n,typ,2)==0
assert call(symbols['editor_commit'])==1
u.mem_write(config,bytes(0x230));w(config+0x210,'QQQ',vector,vector+18*12,vector+18*12)
for i in range(18):w(vector+i*12,'IIB3x',i,0xaabbccdd,0)
before=bytes(u.mem_read(vector,216));call(symbols['editor_apply_accessories'],config,card);after=bytes(u.mem_read(vector,216));expected=bytearray(before)
for typ in [1,4,6,7]:expected[typ*12+8]=1
struct.pack_into('<I',expected,4*12+4,0xffffffff)
assert after==expected
u.mem_write(vector,before);call(symbols['editor_apply_accessories'],config,123);assert bytes(u.mem_read(vector,216))==before
# Call static production appearance_mode via local symbol table; configurable choice must win over Ronaldo's bundled long sleeves.
with (P/'build/payload/work/tools/libselect_team.so').open('rb')as f:
 elf=ELFFile(f);st=elf.get_section_by_name('.symtab');m={x.name:0x35000000+x['st_value']for x in st.iter_symbols()};assert'appearance_mode'in m
for context in [0,473,518,122]:
 call(symbols['activate_context'],context);actual=call(m['appearance_mode'],card);assert actual==mode-1,(mode,context,actual)
(P/('gear-native-mode'+str(mode)+'-validation.json')).write_text(json.dumps({'passed':True,'production_ARM64':True,'six_native_types':[0,1,4,5,6,7],'unknown_and_GK_types_rejected':True,'all_other_accessory_fields_preserved':True,'Ronaldo_left_wrist_white_preserved':True,'user_sleeve_wins_all_contexts':True,'device_tested':False},indent=2));print('NATIVE_GEAR_PASS')
