from pathlib import Path
P=Path('/workspace/73-ui712');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/apk/assets/gateway-release/work/tools/libnoodle_hair.so'));exec(s)
from unicorn import UC_HOOK_CODE
REGS=[UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]
def invoke(name,*args):
 for r,v in zip(REGS,args):u.reg_write(r,v)
 return call(symbols[name])
heap=0x30080000;seen=[]
def putstr(at,text):
 global heap
 b=(text+'\0').encode('utf-16-le');u.mem_write(heap,b);w(at,'Qii',heap,len(b)//2,len(b)//2);heap+=len(b)+16

def getstr(at):
 ptr,n,cap=struct.unpack('<Qii',u.mem_read(at,16));return bytes(u.mem_read(ptr,2*(n-1))).decode('utf-16-le')
info=0x30050000;items=0x30051000;target=88044950524330
original_paths=['Texture2D\'/Game/Assets/ui/Data/Thumbnail/Player/Variation2021/'+str(target)+'_l.'+str(target)+'_l\'','/Game/Assets/ui/Data/Card/FrameStyleX']
def stub(uc,addr,size,data):
 global heap
 if addr==0x33000100:
  for i,text in enumerate(original_paths):putstr(items+i*16,text.replace(str(target),str(uc.reg_read(UC_ARM64_REG_X0))))
  w(info+0x10,'Qii',items,2,2);w(info+0x20,'Qii',0,0,0);w(info+0x30,'Qii',0,0,0);uc.reg_write(UC_ARM64_REG_X0,info)
 elif addr==0x286da2c:
  dest=uc.reg_read(UC_ARM64_REG_X0);src=uc.reg_read(UC_ARM64_REG_X1);putstr(dest,getstr(src));uc.reg_write(UC_ARM64_REG_X0,dest)
 elif addr==0x33000120:
  out=uc.reg_read(UC_ARM64_REG_X0);ptr=uc.reg_read(UC_ARM64_REG_X1);n=uc.reg_read(UC_ARM64_REG_X2);text=bytes(uc.mem_read(ptr,n*2)).decode('utf-16-le').rstrip('\0');seen.append(text);uc.reg_write(UC_ARM64_REG_X0,123)
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);invoke('configure_background',0,0x33000100);assert invoke('noodle_photo_add',target)==1;invoke('noodle_photo_commit');invoke('noodle_background_hook',target,0,0,0,0,0,info)
assert getstr(items)=="Texture2D'/Game/Assets/ui/Data/Thumbnail/Player/Variation2022/U712_88044950524330_l.U712_88044950524330_l'",getstr(items);assert getstr(items+16)==original_paths[1]
# The new body namespace resolves only in an explicit body scope, and keeps detail/low type.
invoke('configure_path',0,0x33000120);actor=0x30060000;w(actor+0x10b0,'Q',target);buf=0x30070000
for style in ['a','b','d','e']:
 model='901'if style in['d','e']else'015';variant='01'if style in['d','e']else'07';text='/Game/Assets/character/Body/SK_'+model+style+variant+'.SK_'+model+style+variant;u.mem_write(buf,text.encode('utf-16-le'));invoke('noodle_path_hook',0,buf,len(text));assert seen[-1]==text
 token=invoke('noodle_body_begin',actor);assert token;invoke('noodle_path_hook',0,buf,len(text));wanted=text.replace('SK_'+model,'SK_'+str(int(model)+6000))if style in['b','e']else text;assert seen[-1]==wanted,(style,seen[-1]);invoke('noodle_body_end',token)
(P/'photo-cut-path-native-validation.json').write_text(json.dumps({'passed':True,'custom_photos_override_private_photos':True,'older_portrait_paths_normalized_to_actual_container_folder':True,'card_frame_keys_preserved':True,'cut_long_body_paths_only_inside_scope':True,'detail_and_lowbody_type_preserved':True,'short_and_original_long_unchanged_outside_scope':True,'Android_tested':False},indent=2));print('PHOTO_AND_CUT_PATH_NATIVE_PASS')
