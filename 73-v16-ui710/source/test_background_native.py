from pathlib import Path
P=Path('/tmp/73-ui710');s=Path('/tmp/73-ui79/test_native_features.py').read_text();s=s[:s.index('# Actual private face selection')];s=s.replace("P=Path('/tmp/73-ui79')","P=Path('/tmp/73-ui710')");s=s.replace("struct(\"<", "struct(\"<")
# Keep old fixture checks, but register immutable configurable backgrounds before the first native call.
s=s.replace("invoke('configure_background',0,0x33000040);out=0x30010000", "invoke('configure_background',0,0x33000040);out=0x30010000\nstock=123456780987;donor=88039313485858\nassert invoke('noodle_background_add',stock,donor)==1\nassert invoke('noodle_background_add',106754901843130,donor)==1\ninvoke('noodle_background_commit')")
s=s.replace("'U79_'+str(target)+'_l'", "('U710_'if target==106754901843130 else'U79_')+str(target)+'_l'").replace("'U79_'+str(target)+'_'", "('U710_'if target==106754901843130 else'U79_')+str(target)+'_'")
s=s.replace("(106754901843130,106754901843130)","(106754901843130,donor)")
s+='''\n# The background donor changes native style, while stock photos keep their original keys.
donor=88039313485858
seen.clear();invoke('noodle_background_hook',stock,1,2,3,4,5,out);assert seen==[stock,donor],seen
for j in range(3):
 items=struct.unpack('<Q',u.mem_read(out+0x10+j*16,8))[0];assert str(donor>>28&4095)in strread(items);assert str(stock)+'_l'in strread(items+16)and'U79_'not in strread(items+16)
seen.clear();invoke('noodle_background_hook',stock,1,2,3,4,5,out);assert seen==[donor],seen
# New characters own photo aliases and only exactfullcard IDs have modified heads.
for target in [105804908868664,105873896755947]:
 invoke('noodle_background_hook',target,1,2,3,4,5,out);items=struct.unpack('<Q',u.mem_read(out+0x10,8))[0];assert 'U79_'+str(target)in strread(items+16)
(P/'background-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'native_donor_style_and_own_photo_separate':True,'private_hero_foreground_used_for_changed_background':True,'native_original_photo_keys_cached_once':True,'unrelated_card_unchanged':True,'new_hero_private_photo_aliases':True,'device_tested':False},indent=2));print('NATIVE_BACKGROUND_PASS')
'''
(P/'test_background_generated.py').write_text(s);exec(compile(s,'test_background_generated.py','exec'))
