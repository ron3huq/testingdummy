from pathlib import Path
P=Path('/tmp/73-ui710');s=Path('/tmp/73-ui79/test_native_features.py').read_text();s=s[:s.index("invoke('configure_background',")];s=s.replace("P=Path('/tmp/73-ui79')","P=Path('/tmp/73-ui710')");exec(s)
actor=0x30030000;pathaddr=0x30040000;face_string=0x30060000
invoke('configure_path',0,0x33000060);invoke('configure_outer',0,0x330000a0);invoke('noodle_enable',1)
fixtures=[(106754901843130,'40122','NHUL'),(105647605587130,'40122','NSPD'),(105804908868664,'144440','NNAR'),(105873896755947,'119531','NORC'),(106783356083208,'144440',None),(70379213169392,'119531',None),(40122,'40122',None),(89136418985302,'4522',None)]
for card,face,tag in fixtures:
 w(actor+0x10b0,'Q',card);string(face_string,face)
 for variant in ['', 'ep00v0313','ep01v0291','lg00v0000']:
  for kind,prefix,suffix in [('mesh',"SkeletalMesh'",'_Face'),('texture',"Texture2D'",'_Face_D')]:
   tok='SK_'if kind=='mesh'else'T_';f=face+variant;face_path=prefix+'/Game/Assets/character/RealFace/'+tok+f+suffix+'.'+tok+f+suffix+"'";face_path_length=len(face_path);u.mem_write(pathaddr,face_path.encode('utf-16le'));invoke('noodle_outer_hook',actor,face_string)
   if tag:assert tag+'ep00v0313'in last_paths[-1],(card,variant,last_paths[-1])
   else:assert last_paths[-1]==face_path,(card,last_paths[-1])
assert invoke('noodle_cr2008_seen')==4
actual=''.join(chr(invoke('noodle_cr2008_char',i))for i in range(192)).split('\0',1)[0];assert '4522lg00v0000'in actual
(P/'face-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'all_four_variants_mesh_and_texture_paths':True,'Naruto_Orc_exact_targets':True,'trial_source_IDs_unmodified':True,'unrelated_Lukaku_cards_unmodified':True,'Ronaldo_2008_probe_does_not_redirect':True,'fixture_path_not_claimed_as_phone_evidence':True,'device_tested':False},indent=2));print('NATIVE_FACE_PASS')
