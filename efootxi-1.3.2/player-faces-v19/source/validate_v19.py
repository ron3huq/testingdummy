"""Native regression plus UI copy scopes, original delegate ABI, secondary common
head render flag isolation and restoration. Engine/GPU boundaries are explicit.
"""
exec((__import__('pathlib').Path(__file__).parent/'validate_native.py').read_text())
import random
card_stub=0x33018000;icon_stub=card_stub+16;name_chars=0x30280000;delegate_events=[]
u.mem_write(card_stub,struct.pack('<I',0xd65f03c0));u.mem_write(icon_stub,struct.pack('<I',0xd65f03c0))
def additional(uc,addr,size,data):
 if addr in [card_stub,icon_stub]:
  delegate_events.append((addr,tuple(uc.reg_read(reg) for reg in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4])));return
 if addr==0x4415ac8:
  nameptr=uc.reg_read(UC_ARM64_REG_X0);outptr=uc.reg_read(UC_ARM64_REG_X1);key=struct.unpack('<Q',uc.mem_read(nameptr,8))[0];word=names[key]
  fstring(outptr,word,name_chars);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
 if addr==0x42cc968:
  assert uc.reg_read(UC_ARM64_REG_X0)==name_chars;uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
u.hook_add(UC_HOOK_CODE,additional)
call(syms['configure_card_data'],0,card_stub);call(syms['configure_icon_data'],0,icon_stub)
vn=[88045755960841,88038776539586,105643042189511,106728863696709,105848932271764,105874433662542];speed=88033139360669
ui=0x30500020;rng=random.Random(190351)
for icon in [False,True]:
 for pid in vn+[speed,105765448873424,target,89135066911146,vn[0]+(1<<32),vn[0]^(1<<32),0]:
  for enabled in [0,1]:
   original=bytearray(rng.randbytes(0x140));struct.pack_into('<Q',original,0x10 if icon else 0x20,pid)
   u.mem_write(ui-16,b'\xa5'*16+original+b'\x5a'*16);call(syms['noodle_enable'],enabled)
   args=(0x30600000,0x30600010,0x30600020,0x30600030,ui) if icon else (ui,0x30600000,12,34)
   call(syms['noodle_icon_data_hook' if icon else 'noodle_card_data_hook'],*args)
   assert delegate_events[-1][0]==(icon_stub if icon else card_stub)
   assert delegate_events[-1][1][:len(args)]==args
   expected=bytearray(original)
   if enabled and (pid in vn or pid==speed):
    team=0x3ffff if pid in vn else 18961;country=38 if pid in vn else 228
    if icon:
     for offset,value in [(0x40,team),(0x48,team),(0x50,0),(0x54,team),(0x58,0),(0x64,country)]:struct.pack_into('<I',expected,offset,value)
     expected[0x4c]=0
     if pid in vn:
      for offset,value in [(0x5c,0x3ffff),(0x60,0)]:struct.pack_into('<I',expected,offset,value)
    else:
     for offset,value in [(0x28,team),(0x2c,team),(0x34,0),(0x38,country),(0x10c,team)]:struct.pack_into('<I',expected,offset,value)
     expected[0x30]=0
   assert bytes(u.mem_read(ui-16,0x160))==b'\xa5'*16+expected+b'\x5a'*16
   checks.append('v19_UI_'+str(icon)+'_'+str(pid)+'_'+str(enabled))
# Common head branch: only named head mesh in the exact native attachment;
# original engine SetRenderInMainPass body executes. Body mesh remains visible.
common=0x30400000;legacycomp=0x30410000;call(syms['noodle_enable'],1)
for pid,word,hide in [(target,'SK_Base_Face',True),(106734785925546,'SK_Base_Face',True),(105765448873424,'SK_Base_Face',True),(105643042189511,'SK_Base_Face',True),(target,'SK_4522ep00v0313_Face',True),(target,'SK_Base_Body',False),(106726716084650,'SK_Base_Face',False)]:
 request(pid,'4522ep00v0313');fake_material(pid)
 u.mem_write(actor+0x1900,struct.pack('<Q',common));u.mem_write(common+0x18,struct.pack('<Q',intern_key(word)))
 u.mem_write(actor+0x1a70,struct.pack('<Qii',ref,1,1));u.mem_write(ref,struct.pack('<Q',legacycomp));u.mem_write(legacycomp+0x468,struct.pack('<Q',common));u.mem_write(legacycomp+0x212,b'\x04')
 u.mem_write(actor+0x228,struct.pack('<Q',comp));u.mem_write(comp+0x468,struct.pack('<Q',meshobj));u.mem_write(comp,struct.pack('<Q',vt));slots_live[comp]=[mic,0x30099910]
 u.mem_write(actor+0x1a80,b'\0'*16);u.mem_write(actor+0x1ad0,b'\0'*16)
 u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',meshobj));call(done,closure,result,detail)
 assert bytes(u.mem_read(legacycomp+0x212,1))==(b'\0' if hide else b'\x04')
 assert struct.unpack('<Q',u.mem_read(comp+0x468,8))[0]==meshobj and slots_live[comp]==[mic,0x30099910]
 checks.append('v19_exact_common_head_'+str(pid)+'_'+word)
 if hide:
  last=''.join(chr(call(syms['noodle_common_char'],i)) for i in range(96)).split('\0')[0];assert last==word
  before=call(syms['noodle_stat'],83);call(bake,actor);assert call(syms['noodle_stat'],83)==before
  # Actor switched to another card: restore flag on the engine callback, never poller thread.
  request(89135066911146,'4522ep00v0313');assert bytes(u.mem_read(legacycomp+0x212,1))==b'\x04'
  checks.append('v19_common_head_idempotent_restored_'+str(pid))
# Verify native depth-property SetBit directly, and exercise all combinations
# of the three render flags. Unrelated bits and original states must survive.
for bits in range(8):
 request(target,'4522ep00v0313');fake_material(target)
 u.mem_write(actor+0x1900,struct.pack('<Q',common));u.mem_write(common+0x18,struct.pack('<Q',intern_key('SK_Base_Face')))
 u.mem_write(actor+0x1a70,struct.pack('<Qii',ref,1,1));u.mem_write(ref,struct.pack('<Q',legacycomp));u.mem_write(legacycomp+0x468,struct.pack('<Q',common));u.mem_write(actor+0x228,struct.pack('<Q',comp));u.mem_write(comp+0x468,struct.pack('<Q',meshobj));slots_live[comp]=[mic,0x30099910]
 flags=0x80000201 | (0x40000 if bits&1 else 0) | (0x80000 if bits&2 else 0) | (0x10000000 if bits&4 else 0)
 # Original generated setter must affect exactly the audited depth bit.
 u.mem_write(legacycomp+0x210,struct.pack('<I',flags&~0x80000));call(0x62fc300,legacycomp)
 assert struct.unpack('<I',u.mem_read(legacycomp+0x210,4))[0]==flags|0x80000
 u.mem_write(legacycomp+0x210,struct.pack('<I',flags));call(done,closure,result,detail)
 assert struct.unpack('<I',u.mem_read(legacycomp+0x210,4))[0]==flags&~0x100c0000
 # Disabling must restore all three original values, including false values.
 call(syms['noodle_enable'],0);call(bake,actor)
 assert struct.unpack('<I',u.mem_read(legacycomp+0x210,4))[0]==flags
 checks.append('v19_main_depth_shadow_exact_flags_disable_restore_'+str(bits))
 call(syms['noodle_enable'],1)
u.mem_write(actor+0x1900,b'\0'*8)
report.update(status='V19_NATIVE_UI_COPY_SCOPES_SECONDARY_HEAD_RESTORE_PASS',checks=checks,common_head_main_and_cast_shadow_setters_original_body_executed=True,depth_bit_generated_setter_original_body_executed=True,card_data_and_gameplan_original_delegate_ABI_forwarded=True,UI_teams_source='native PlayerCardData builder0x38809bc / GamePlan0x330ae54',phone_tested=False)
(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
