from pathlib import Path
P=Path('/tmp/73-ui711');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE,UC_HOOK_INTR
source=0x30020000;packed=0x30021000;config=0x30022000;spec=0x30023000;actor=0x30024000;v=0x30027000
original=bytes.fromhex('7777777777777725c5427777')+bytes(range(12,52));assert len(original)==52
ids=[123456789876,123456789877,123456789878]
for i,id in enumerate(ids):assert call(symbols['editor_socks_add'],id,i+1)==1;assert call(symbols['model_add'],id,(1<<44)-1)==1
call(symbols['editor_socks_commit']);call(symbols['model_commit']);call(symbols['configure_appearance_serialize'],0,0x33000100);call(symbols['configure_appearance_build'],0,0x33000120)
u.mem_write(source+24,original)
def stub(uc,addr,size,data):
 if addr==0x33000100:uc.mem_write(packed,bytes(uc.mem_read(source+24,52)));uc.reg_write(UC_ARM64_REG_X0,1)
 elif addr==0x33000120:uc.reg_write(UC_ARM64_REG_X0,source);uc.reg_write(UC_ARM64_REG_X1,packed);uc.reg_write(UC_ARM64_REG_PC,symbols['appearance_serialize_hook']);return
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
def intr(uc,n,data):assert uc.reg_read(UC_ARM64_REG_X8)==178;uc.reg_write(UC_ARM64_REG_X0,1234)
u.hook_add(UC_HOOK_CODE,stub);u.hook_add(UC_HOOK_INTR,intr);w(0x99e53a8,'Q',v);u.mem_write(v,struct.pack('<4f',1,1,1,1));proof=[]
for i,id in enumerate(ids):
 w(spec+8,'Q',id);call(symbols['appearance_build_hook'],config,spec);out=bytes(u.mem_read(packed,52));want=bytearray(original);want[8]=(want[8]&~12)|(i<<2);assert out==want
 # Run original73 packed-to-character-config instructions, not a mirrored implementation.
 u.reg_write(UC_ARM64_REG_X0,config);u.reg_write(UC_ARM64_REG_X1,packed);u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.emu_start(0x68d1fbc,0x68d205c,count=1000);assert struct.unpack('<I',u.mem_read(config+0x54,4))[0]==i
 u.mem_write(actor+0x10a0,bytes(u.mem_read(config,0x230)));u.reg_write(UC_ARM64_REG_X0,actor);u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.emu_start(0x39c6e88,0x39c6f10,count=1000);sp=u.reg_read(UC_ARM64_REG_SP);scalar=struct.unpack('<f',u.mem_read(sp+8,4))[0];assert scalar==i+1
 proof.append({'native_socks_enum':i,'material_scalar':scalar})
# All eight exposed accessory types are accepted; goalkeeper entries remain outside selection.
assert call(symbols['editor_add_player'],ids[0],0,2)==1
for typ in [0,1,4,5,6,7,8,9]:assert call(symbols['editor_accessory'],1,typ,2)==1
for typ in [2,3,10,17,23,24]:assert call(symbols['editor_accessory'],1,typ,2)==0
call(symbols['editor_commit']);u.mem_write(config,bytes(0x230));w(config+0x210,'QQQ',v,v+216,v+216)
for typ in range(18):w(v+typ*12,'IIB3x',typ,0xaabbccdd,0)
call(symbols['editor_apply_accessories'],config,ids[0])
for typ in range(18):assert u.mem_read(v+typ*12+8,1)==(b'\1'if typ in [0,1,4,5,6,7,8,9]else b'\0');assert struct.unpack('<I',u.mem_read(v+typ*12+4,4))[0]==0xaabbccdd
(P/'clothing-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'original73_converter_and_socks_material_prefix_executed':proof,'serialized_other_fields_unchanged':True,'eight_accessory_flags_and_colors_verified':True,'native_undershirt_types':[8,9],'Android_tested':False},indent=2));print('CLOTHING_NATIVE_PASS')
