from pathlib import Path
P=Path('/tmp/73-ui711');s=Path('/tmp/73-ui79/test_native_features.py').read_text();s=s[:s.index("invoke('configure_background',")].replace("P=Path('/tmp/73-ui79')","P=Path('/tmp/73-ui711')");exec(s)
pid=105837926394281;unicode_id=123456789876;shirt_id=123456789877;display=0x30050000;shirt=0x30050100;record=0x30060000;native_name=0x30070000;out=0x30071000;XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
u.mem_write(display,b'C.Ronaldo\0');u.mem_write(shirt,b'Ronaldo\0');u.mem_write(native_name,b'Native Player\0');assert invoke('noodle_identity_add',pid,display,shirt,109,228,119,15,6)==1
u.mem_write(display,'Nguyễn Ronaldo\0'.encode());assert invoke('noodle_identity_add',unicode_id,display,0,0,0,0,4,0)==1;assert invoke('noodle_identity_add',shirt_id,0,shirt,0,0,0,8,0)==1
assert invoke('noodle_identity_add',pid,display,shirt,109,228,119,15,6)==0
invoke('noodle_identity_commit');invoke('noodle_enable',1);invoke('configure_record_lookup',0,0x33000210);invoke('configure_record_name',0,0x33000220);invoke('configure_player_name',0,0x33000230);invoke('configure_shirt_char',0,0x33000240);invoke('configure_card_data',0,0x33000250);invoke('configure_icon_data',0,0x33000250);observed=[]
def observe(uc,addr,size,data):
 if addr==0x33000210:uc.reg_write(UC_ARM64_REG_X0,record)
 elif addr==0x33000220:uc.reg_write(UC_ARM64_REG_X0,native_name)
 elif addr==0x33000230:observed.append('original_name')
 elif addr==0x33000240:
  ptr=uc.reg_read(UC_ARM64_REG_X1);raw=bytes(uc.mem_read(ptr,61)).split(b'\0')[0];observed.append(raw)
 elif addr==0x33000250:pass
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,observe)
def init(id):
 u.mem_write(record,bytes(0x1d0));w(record+0x38,'I',0);w(record+0x40,'Q',id^XOR)
 for off in [0x4c,0x89,0xc6,0x103]:u.mem_write(record+off,b'Native Player\0')
 w(record+0x198,'H',16);w(record+0x140,'I',396<<14)
init(pid);assert invoke('noodle_record_lookup_hook',0,0,pid)==record
for off in [0x4c,0x89,0xc6,0x103]:assert bytes(u.mem_read(record+off,61)).split(b'\0')[0]==b'C.Ronaldo'
assert struct.unpack('<H',u.mem_read(record+0x198,2))[0]==228 and struct.unpack('<I',u.mem_read(record+0x140,4))[0]==109<<14
init(unicode_id);invoke('noodle_record_lookup_hook',0,0,unicode_id);assert bytes(u.mem_read(record+0x4c,61)).split(b'\0')[0].decode()=='Nguyễn Ronaldo';assert struct.unpack('<H',u.mem_read(record+0x198,2))[0]==16
u.mem_write(out,bytes(64));invoke('noodle_player_name_hook',0,unicode_id,out);assert strread(out)=='Nguyễn Ronaldo' and 'original_name'not in observed
init(shirt_id);assert invoke('noodle_record_name_hook',record)==native_name
actor=0x30080000;u.mem_write(actor,bytes(0x2000));w(actor+0x10b0,'Q',pid);invoke('noodle_shirt_char_hook',actor,native_name);assert observed[-1]==b'RONALDO'
for icon in [False,True]:
 u.mem_write(out,bytes([0x66])*0x200);w(out+(0x10 if icon else 0x20),'Q',pid)
 if icon:invoke('noodle_icon_data_hook',0,0,0,0,out)
 else:invoke('noodle_card_data_hook',out,0,0,0)
 if icon:
  assert struct.unpack('<I',u.mem_read(out+0x54,4))[0]==109 and struct.unpack('<I',u.mem_read(out+0x64,4))[0]==228;assert struct.unpack('<I',u.mem_read(out+0x5c,4))[0]==6
 else:
  assert struct.unpack('<2I',u.mem_read(out+0x28,8))==(109,109)and u.mem_read(out+0x30,1)==b'\0'and struct.unpack('<I',u.mem_read(out+0x34,4))[0]==119 and struct.unpack('<I',u.mem_read(out+0x38,4))[0]==228
init(pid+1000);before=bytes(u.mem_read(record,0x1d0));invoke('noodle_record_lookup_hook',0,0,pid+1000);assert bytes(u.mem_read(record,0x1d0))==before
(P/'identity-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'all_four_UTF8_record_name_fields':True,'engine_FString_UTF16_unicode_name':True,'jersey_native_setter_and_uppercase_lettering':True,'shirt_only_profile_preserves_original_display_name':True,'Real_team109_packed_and_Portugal_country228':True,'Portugal_national_team6_in_icon':True,'card_and_icon_presentation_updated':True,'arbitrary_renamed_card_country_not_changed_to_Vietnam':True,'unrelated_record_unchanged':True,'Android_tested':False},indent=2));print('IDENTITY_NATIVE_PASS')
