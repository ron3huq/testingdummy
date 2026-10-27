from pathlib import Path
P=Path('/tmp/73-ui710');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libnoodle_hair.so'));exec(s)
def invoke(name,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(symbols.get(name,name),0x33000010,count=2000000);assert u.reg_read(UC_ARM64_REG_PC)==0x33000010;return u.reg_read(UC_ARM64_REG_X0)

from unicorn import UC_HOOK_MEM_INVALID
def badmem(uc,access,addr,size,value,data):
 print('BADMEM',hex(addr),'PC',hex(uc.reg_read(UC_ARM64_REG_PC)),'X0',hex(uc.reg_read(UC_ARM64_REG_X0)),'X1',hex(uc.reg_read(UC_ARM64_REG_X1)),'X19',hex(uc.reg_read(UC_ARM64_REG_X19)),'X23',hex(uc.reg_read(UC_ARM64_REG_X23)),flush=True);return False
u.hook_add(UC_HOOK_MEM_INVALID,badmem)
seen=[];last_paths=[];heap=0x30100000

def string(addr,text):
 global heap
 raw=(text+'\0').encode('utf-16le');ptr=heap;heap+=2048;u.mem_write(ptr,raw);w(addr,'Qii',ptr,len(raw)//2,1024)
def strread(addr):
 ptr,n,cap=struct.unpack('<Qii',u.mem_read(addr,16));return bytes(u.mem_read(ptr,n*2)).decode('utf-16le').rstrip('\0')
def observer(uc,addr,size,data):
 global heap
 if addr==0x42ccbbc:pass # engine allocation-size quantization boundary
 elif addr==0x42cca20:
  old=uc.reg_read(UC_ARM64_REG_X0);n=uc.reg_read(UC_ARM64_REG_X1);new=heap;heap+=(n+4095)&~4095
  if old and n:uc.mem_write(new,bytes(uc.mem_read(old,min(n,2048))))
  uc.reg_write(UC_ARM64_REG_X0,new)
 elif addr==0x42cc968:pass
 elif addr in [0x8c1bc60,0x8c1bc70]:
  dest=uc.reg_read(UC_ARM64_REG_X0);src=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_X2);uc.mem_write(dest,bytes(uc.mem_read(src,n)))
 elif addr==0x33000040:
  id=uc.reg_read(UC_ARM64_REG_X0);out=uc.reg_read(UC_ARM64_REG_X6);seen.append(id);w(out,'III',id>>44&15,id>>40&15,id>>28&4095)
  for j in range(3):
   items=heap;heap+=16*3;w(out+0x10+j*16,'Qii',items,3,3)
   prefix=f'{id>>44&15:02x}{id>>40&15:02x}_{id>>28&4095}'
   string(items,'Frame/'+prefix+'_f01');string(items+16,"Texture2D'/Game/Assets/ui/Data/Thumbnail/Player/Variation2022/"+str(id)+'_l.'+str(id)+"_l'");string(items+32,'ui/Data/Thumbnail/Player/Variation2022/'+str(id)+'_')
  uc.reg_write(UC_ARM64_REG_X0,123)
 elif addr==0x33000060:
  ptr=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_W2);last_paths.append(bytes(uc.mem_read(ptr,n*2)).decode('utf-16le').rstrip('\0'));uc.reg_write(UC_ARM64_REG_X0,321)
 elif addr==0x330000a0:
  uc.reg_write(UC_ARM64_REG_X0,0x30010000);uc.reg_write(UC_ARM64_REG_X1,0x30040000);uc.reg_write(UC_ARM64_REG_X2,face_path_length);uc.reg_write(UC_ARM64_REG_PC,symbols['noodle_path_hook']);return
 elif addr==0x33000080:seen.append(('body',uc.reg_read(UC_ARM64_REG_X0)))
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,observer)
invoke('configure_background',0,0x33000040);out=0x30010000
stock=123456780987;donor=88039313485858
assert invoke('noodle_background_add',stock,donor)==1
assert invoke('noodle_background_add',106754901843130,donor)==1
invoke('noodle_background_commit')
cases=[(89138556572074,88045755960770),(88044950524330,88045755960770),(89135066911146,88045755960770),(88045755960841,89137214427270),(105848932271764,89137214427270),(106754901843130,donor),(105647605587130,105647605587130)]
for target,donor in cases:
 assert invoke('noodle_background_hook',target,1,2,3,4,5,out)==123;assert seen[-1]==donor
 for j in range(3):
  items=struct.unpack('<Q',u.mem_read(out+0x10+j*16,8))[0];assert strread(items).startswith('Frame/')
  assert ('U710_'if target==106754901843130 else'U79_')+str(target)+'_l' in strread(items+16) and ('U710_'if target==106754901843130 else'U79_')+str(target)+'_' in strread(items+32)
# An unrelated card retains both its native style and native photo filenames.
invoke('noodle_background_hook',1234567,1,2,3,4,5,out);items=struct.unpack('<Q',u.mem_read(out+0x10,8))[0];assert 'U79_'not in strread(items+16)
# Exact actor/card/thread RGB paths, never body meshes or head textures.
hulk=106754901843130;spider=105647605587130;actor=0x30030000;u.mem_write(actor,bytes(0x2000));w(actor+0x10b0,'Q',hulk)
assert invoke('noodle_rgb_add',hulk,1)==1;assert invoke('noodle_rgb_add',hulk+1,65)==0;invoke('noodle_rgb_commit');invoke('configure_rgb_selector',0,0x33000080);invoke('configure_path',0,0x33000060)
invoke('noodle_rgb_selector_hook',actor);assert struct.unpack('<I',u.mem_read(actor+0x42c,4))[0]==1 and u.mem_read(actor+0x1a6b,1)==b'\1'
token=invoke('noodle_body_begin',actor);pathaddr=0x30040000
for part in ['Body','Skin','Lowbody']:
 path="Texture2D'/Game/Assets/MaterialLibrary/Character/Body/CommonTextures/T_Sk6_"+part+'_D.T_Sk6_'+part+"_D'";u.mem_write(pathaddr,path.encode('utf-16le'));assert invoke('noodle_path_hook',out,pathaddr,len(path))==321;assert 'T_C790001_'+part+'_D' in last_paths[-1]
for path in ["SkeletalMesh'/Game/Assets/character/Body/SK_002a01.SK_002a01'","Texture2D'/Game/Assets/character/RealFace/T_4522_Face_D.T_4522_Face_D'"]:
 u.mem_write(pathaddr,path.encode('utf-16le'));invoke('noodle_path_hook',out,pathaddr,len(path));assert last_paths[-1]==path
invoke('noodle_body_end',token);path="/Game/Assets/MaterialLibrary/Character/Body/CommonTextures/T_Sk6_Skin_D.T_Sk6_Skin_D";u.mem_write(pathaddr,path.encode('utf-16le'));invoke('noodle_path_hook',out,pathaddr,len(path));assert last_paths[-1]==path
# RGB codec keeps ALL alpha bytes, including0, and represents exact requested RGB at reference luminance.
src=0x30050000;dst=src+4096;pixels=b''.join(bytes([143,143,143,a])for a in range(256));u.mem_write(src,pixels);invoke('tint_bgra',src,dst,256,0x4e5b37,143);result=bytes(u.mem_read(dst,len(pixels)));assert all(result[i:i+3]==bytes([55,91,78])and result[i+3]==pixels[i+3]for i in range(0,len(result),4))

# The background donor changes native style, while stock photos keep their original keys.
donor=88039313485858
seen.clear();invoke('noodle_background_hook',stock,1,2,3,4,5,out);assert seen==[stock,donor],seen
for j in range(3):
 items=struct.unpack('<Q',u.mem_read(out+0x10+j*16,8))[0];assert str(donor>>28&4095)in strread(items);assert str(stock)+'_l'in strread(items+16)and'U79_'not in strread(items+16)
seen.clear();invoke('noodle_background_hook',stock,1,2,3,4,5,out);assert seen==[donor],seen
# New characters own photo aliases and only exactfullcard IDs have modified heads.
for target in [105804908868664,105873896755947]:
 invoke('noodle_background_hook',target,1,2,3,4,5,out);items=struct.unpack('<Q',u.mem_read(out+0x10,8))[0];assert 'U79_'+str(target)in strread(items+16)
(P/'background-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'native_donor_style_and_own_photo_separate':True,'private_hero_foreground_used_for_changed_background':True,'native_original_photo_keys_cached_once':True,'unrelated_card_unchanged':True,'new_hero_private_photo_aliases':True,'device_tested':False},indent=2));print('NATIVE_BACKGROUND_PASS')
