from pathlib import Path
import json,struct
P=Path('/workspace/ronaldo-work/73-ui5');source=Path('/workspace/ronaldo-work/73-ui4/test_native.py').read_text().replace('73-ui4','73-ui5');exec(source[:source.index('import sys,sqlite3')]);face=load(P/'payload/work/tools/libnoodle_hair.so',0x36000000);fixture=load(P/'fixture.so',0x37000000)
checks=[];actor=0x30001000;inputp=0x33310000;cfg=0x33320000;vec=0x33321000;spec=0x33322000
call(symbols['configure_body_path_scope'],face['noodle_body_begin'],face['noodle_body_end']);call(face['configure_path'],0,fixture['record_path']);call(symbols['configure_rolled_detail'],0,fixture['detail']);call(symbols['configure_rolled_common'],0,fixture['common']);call(symbols['rolled_enable'],1)
firstmsg=json.loads((P/'skill-message-map.json').read_text())[0]['message_id'];call(fixture['prepare'],face['noodle_path_hook'],symbols['skill_text_hook'],firstmsg,0)
def setpath(path):
 b=path.encode('utf-16-le')+b'\0\0';u.mem_write(inputp,b);call(fixture['set_path'],inputp,len(b)//2);return b
def output():
 p=call(fixture['value'],7);n=call(fixture['value'],8);return bytes(u.mem_read(p,n*2)).decode('utf-16-le').rstrip('\0')
original="SkeletalMesh'/Game/Assets/character/Body/SK_015a07.SK_015a07'";setpath(original)
for pid in [88044950524330,89135066911146,89136418985303,89136418985302,123,89136418985303+(1<<32)]:
 for team,slot in [(351,0),(352,1),(351,2),(242,0)]:
  w(actor+0x10b0,'Q',pid);w(actor+0x12a4,'I',(team<<14)|slot);u.reg_write(UC_ARM64_REG_X5,19);call(symbols['rolled_detail_hook'],actor,15,1,7,0)
  selected=pid in[88044950524330,89135066911146,89136418985303,89136418985302]and team in[351,352]and slot<2
  assert output()==(original.replace('015a07','4015a07')if selected else original),(pid,team,slot,output())
  assert call(fixture['value'],1)==15 and call(fixture['value'],2)==(0 if selected else 1)and call(fixture['value'],5)==19
# Nested resource calls never leak the substitution beyond the native body load.
b=setpath(original);call(face['noodle_path_hook'],0,inputp,len(b)//2);assert output()==original
w(actor+0x10b0,'Q',88044950524330);w(actor+0x12a4,'I',351<<14);u.reg_write(UC_ARM64_REG_X5,33);call(symbols['rolled_common_hook'],actor,0,0,0,0);assert call(fixture['value'],1)==0 and call(fixture['value'],5)==33 and output()==original
# Physics/subobjects are not redirected to nonexistent private packages.
for path in ["PhysicsAsset'/Game/Assets/character/Body/SK_015a07.SK_015a07_PhysicsAsset'","/Game/Assets/character/Body/SK_015a07_PhysicsAsset.SK_015a07_PhysicsAsset"]:
 setpath(path);call(symbols['rolled_detail_hook'],actor,15,1,7,0);assert output()==path
checks+=['Actual compiled select-team->face-library->soft-path chain; native model15 and six arguments preserved; exact four IDs/two kits/two slots only','Common/low-body loader remains native; no forced detailed mesh; resource substitution ends with body call; physics paths untouched']
# Tape applies even before the optional editor transaction is installed.
u.mem_write(cfg,b'\0'*0x230);w(cfg+0x210,'3Q',vec,vec,vec+216)
for typ in range(18):call(0x68cff80,cfg,typ,0xaabbccdd,int(typ==5))
before=bytes(u.mem_read(vec,216));call(symbols['editor_apply_accessories'],cfg,88044950524330);after=bytes(u.mem_read(vec,216));expected=bytearray(before);struct.pack_into('<I',expected,4*12+4,0xffffffff);expected[4*12+8]=1;expected[5*12+8]=0;assert after==expected
call(symbols['configure_appearance_build'],0,fixture['build']);w(spec+8,'Q',88044950524330);w(cfg+0x50,'I',1);call(symbols['appearance_build_hook'],cfg,spec);assert struct.unpack('<I',u.mem_read(cfg+0x50,4))[0]==0
checks.append('Original native18-entry accessory vector: left tape white/on, right off, other bytes exact; applies before editor ready; rolled-card appearance starts with accessory-compatible short flag')
# Real original parameter->message mapping; same24-byte libc++ string ABI as UI.
call(symbols['configure_skill_text'],0,fixture['original_text']);call(symbols['configure_skill_page'],0,fixture['original_page'])
def readshort(addr):
 b=bytes(u.mem_read(addr,24));assert not(b[0]&1);return b[1:1+(b[0]>>1)].decode()
for row in json.loads((P/'skill-message-map.json').read_text()):
 w(inputp,'I',row['parameter']);assert call(0x82bb60c,inputp)==row['message_id'];call(fixture['prepare'],face['noodle_path_hook'],symbols['skill_text_hook'],row['message_id'],0);assert call(symbols['skill_text_hook'],cfg,row['message_id'])==1;assert readshort(cfg)==row['label']
row=json.loads((P/'skill-message-map.json').read_text())[0];call(fixture['prepare'],face['noodle_path_hook'],symbols['skill_text_hook'],row['message_id'],1);call(symbols['skill_page_hook'],0,89136418985303);assert readshort(call(fixture['value'],9))==row['label'];call(symbols['skill_page_hook'],0,123);assert readshort(call(fixture['value'],9))=='Native text';call(symbols['skill_text_hook'],cfg,0xdeadbeef);assert readshort(cfg)=='Native text'
checks.append('68 skill message IDs checked through actual82bb60c; missing names obtain valid short UTF8 strings; custom-card page scope repairs names, unrelated nonempty messages preserved')
# FString sret convention and native buffer ownership remain intact for all6 logos.
call(symbols['configure_competition_logo'],0,fixture['original_logo'])
def reserve(uc,addr,size,data):
 if addr==0x286ff60:
  ptr=uc.reg_read(UC_ARM64_REG_X0);need=uc.reg_read(UC_ARM64_REG_W1);old,_,cap=struct.unpack('<QII',uc.mem_read(ptr,16));assert cap>=need and old;uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,reserve)
for cid,code in [(473,'Y08'),(518,'Y17'),(122,'UCL'),(549,'AP'),(128,'WORLD'),(566,'AFC'),(125,None)]:
 for size in [0,1,2]:
  w(inputp,'II',cid,0);u.mem_write(cfg,b'\0'*16);u.reg_write(UC_ARM64_REG_X8,cfg);call(symbols['competition_logo_hook'],inputp,size,0);ptr,n,cap=struct.unpack('<QII',u.mem_read(cfg,16));text=bytes(u.mem_read(ptr,n*2)).decode('utf-16-le').rstrip('\0')
  if code:
   assert 'emblemOther-UI5_'+code in text and ('_s' in text)==(size==1)and('_l'in text)==(size==2),text
  else:assert 'UI5_'not in text
checks.append('Six league-logo FString returns: hiddenX8, original allocator/ownership, small/large suffix and quote/object syntax retained; unrelated125 uses original path')
(P/'regression-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'android_phone_tested':False},indent=2));print('REGRESSIONS_PASS',len(checks))
