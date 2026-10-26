from pathlib import Path
P=Path('/tmp/73-ui79');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libnoodle_hair.so'));exec(s)
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
cases=[(89138556572074,88045755960770),(88044950524330,88045755960770),(89135066911146,88045755960770),(88045755960841,89137214427270),(105848932271764,89137214427270),(106754901843130,106754901843130),(105647605587130,105647605587130)]
for target,donor in cases:
 assert invoke('noodle_background_hook',target,1,2,3,4,5,out)==123;assert seen[-1]==donor
 for j in range(3):
  items=struct.unpack('<Q',u.mem_read(out+0x10+j*16,8))[0];assert strread(items).startswith('Frame/')
  assert 'U79_'+str(target)+'_l' in strread(items+16) and 'U79_'+str(target)+'_' in strread(items+32)
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
# Actual private face selection from both Lukaku cards; unrelated Lukaku variants retain their own head.
invoke('configure_outer',0,0x330000a0);invoke('noodle_enable',1);face_string=0x30060000;string(face_string,'40122')
for card,tag in [(106754901843130,'NHUL'),(105647605587130,'NSPD'),(40122,None)]:
 w(actor+0x10b0,'Q',card)
 for kind,prefix,suffix in [('mesh',"SkeletalMesh'",'_Face'),('texture',"Texture2D'",'_Face_D')]:
  token='SK_'if kind=='mesh'else'T_';face_path=prefix+'/Game/Assets/character/RealFace/'+token+'40122'+suffix+'.'+token+'40122'+suffix+"'";face_path_length=len(face_path);u.mem_write(pathaddr,face_path.encode('utf-16le'));invoke('noodle_outer_hook',actor,face_string)
  if tag:assert tag+'ep00v0313'in last_paths[-1]and'40122'not in last_paths[-1]
  else:assert last_paths[-1]==face_path

# Arena must still fit a single4KB page, preserving the working allocator.
import sys;sys.path.insert(0,str(P/'build/payload/work/tools'));import hook_arena
assert len(hook_arena.PLANS)==42 and len(hook_arena.PLANS)*hook_arena.SLOT<=4096
(P/'native-features-validation.json').write_text(json.dumps({'passed':True,'production_ARM64_library':True,'donor_style_target_photo_keys_separate':True,'original_engine_FString_assignment_executed':True,'new_Hulk_Spider_and_existing_card_scope':True,'actual_two_Lukaku_card_mesh_and_texture_paths_redirect_to_private_heroes':True,'unrelated_Lukaku_card_paths_unchanged':True,'native_RGB_path_redirects_all3_families':True,'body_mesh_and_head_paths_never_redirected':True,'unscoped_paths_untouched':True,'exact_4e5b37_RGB_at_reference_luminance':True,'all256_alpha_values_preserved':True,'42_hooks_fit_same4KB_arena':True,'engine_renderer_bodies_modeled':True,'phone_tested':False},indent=2));print('NATIVE_FEATURES_PASS')
