from pathlib import Path
import struct,json
P=Path('/workspace/ronaldo-work/73-ui6');s=(P/'test_native.py').read_text();exec(s[:s.index('import sys,sqlite3')]);owner=0x30008000;actor=0x30010000;cfg=0x30020000;spec=0x30030000;packed=0x30040000;stub=0x33000180
u.mem_write(stub,bytes.fromhex('20008052c0035fd6'))
for label in['appearance_shirt','appearance_build','appearance_serialize']:call(symbols['configure_'+label],0,stub)
proof=[]
for pid in[88044950524330,89135066911146,89136418985303,89136418985302]:
 for cid in[0,473,518,122]:
  call(symbols['activate_context'],cid)
  for team in[100,242,245,351,352,1706,4937,999]:
   for slot in[0,1,2]:
    w(owner+0x4d8,'Q',actor);u.mem_write(actor,b'\0'*0x2000);w(actor+0x10b0,'Q',pid);w(actor+0x12a4,'I',(team<<14)|slot);w(actor+0x10f0,'I',0);call(symbols['appearance_shirt_hook'],owner,(team<<14)|slot);assert struct.unpack('<I',u.mem_read(actor+0x10f0,4))[0]==1,(pid,cid,team,slot)
  u.mem_write(cfg,b'\0'*0x230);w(spec+8,'Q',pid);call(symbols['appearance_build_hook'],cfg,spec);assert struct.unpack('<I',u.mem_read(cfg+0x50,4))[0]==1
  w(spec,'Q',pid);u.mem_write(packed,b'\x15'*52);assert call(symbols['appearance_serialize_hook'],spec,packed)==1;assert bytes(u.mem_read(packed+7,1))[0]>>6==2
 call(symbols['rolled_enable'],1);assert call(symbols['rolled_pick'],pid,351<<14,15,7,0)==0
 proof.append({'id':pid,'all_8_kits_3_slots_4_competition_contexts_long':True,'native_builder_long':True,'serialized_long':True,'obsolete_rolled_model_disabled':True})
# The raw manager table must pass unmodified, including both original rows.
coach=Path('/workspace/ronaldo-work/73-ui4/Coach-decoded.bin').read_bytes();u.mem_write(cfg,coach);assert call(symbols['patch_decoded'],cfg,len(coach))==0;assert bytes(u.mem_read(cfg,len(coach)))==coach
(P/'sleeves-coaches-validation.json').write_text(json.dumps({'passed':True,'compiled_ARM64':True,'sleeves':proof,'entire_original_coach_table_unchanged':True,'phone_tested':False},indent=2));print('SLEEVES_COACHES_PASS')
