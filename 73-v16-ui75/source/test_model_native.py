from pathlib import Path
import struct,json
from unicorn import UC_HOOK_INTR,UC_HOOK_CODE
from unicorn.arm64_const import *
P=Path('/workspace/ronaldo-work/73-ui75')
s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace("/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so",str(P/'payload/work/tools/libselect_team.so'))
exec(s)
pid=89136418985303;other=89136418985302;dest=0x30000000;source=0x30001000;spec=0x30002000;packed=0x30003000
nibbles=[7,3,0,4,1,2,10,8,5,6,9];float_offsets=[0x20,0x14,8,0x18,0xc,0x10,0x30,0x28,0x1c,0x24,0x2c]
# separate cards test all raw0..14 values, every exposed field.
for value in range(15):assert call(symbols['model_add'],pid+value,sum(value<<(i*4)for i in range(11)))==1
call(symbols['model_commit'])
original=bytes.fromhex('77777777777777')+bytes(range(7,52))
for value in range(15):
 u.mem_write(dest,original);assert call(symbols['model_patch'],dest,pid+value)==1;data=bytes(u.mem_read(dest,52));assert data[7:]==original[7:];assert all(((data[n//2]>>((n%2)*4))&15)==7 for n in [11,12,13])
 for i,n in enumerate(nibbles):assert (data[n//2]>>((n%2)*4))&15==value
 call(0x68d288c,source,dest)
 for off in float_offsets:assert abs(struct.unpack('<f',u.mem_read(source+off,4))[0]-(value/7-1))<1e-6,(value,off)
# Full64 equality and unedited players remain untouched.
u.mem_write(dest,original);assert call(symbols['model_patch'],dest,pid+1000)==0;assert bytes(u.mem_read(dest,52))==original
# Actual build hook establishes a scope; source appearance ID intentionally differs.
u.mem_write(source,b'\x33'*24+original);w(spec+8,'Q',pid)
call(symbols['configure_appearance_serialize'],0,0x33000100);call(symbols['configure_appearance_build'],0,0x33000120)
# tiny delegate tail-calls the actual production serialize hook, then returns through builder.
def stub(uc,addr,size,data):
 if addr==0x33000100:
  src=uc.reg_read(UC_ARM64_REG_X0);out=uc.reg_read(UC_ARM64_REG_X1);uc.mem_write(out,bytes(uc.mem_read(src+24,52)));uc.reg_write(UC_ARM64_REG_X0,1);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 elif addr==0x33000120:
  uc.reg_write(UC_ARM64_REG_X0,source);uc.reg_write(UC_ARM64_REG_X1,packed);uc.reg_write(UC_ARM64_REG_PC,symbols['appearance_serialize_hook'])
def intr(uc,intno,data):
 assert uc.reg_read(UC_ARM64_REG_X8)==178
 uc.reg_write(UC_ARM64_REG_X0,1234)
u.hook_add(UC_HOOK_CODE,stub);u.hook_add(UC_HOOK_INTR,intr)
call(symbols['appearance_build_hook'],dest,spec);assert call(symbols['model_status'],2)==16
data=bytes(u.mem_read(packed,52));assert all(((data[n//2]>>((n%2)*4))&15)==0 for n in nibbles)
# Scope cleared: background serializer must not inherit the previous card.
u.mem_write(packed,b'\x99'*52);call(symbols['appearance_serialize_hook'],source,packed);assert bytes(u.mem_read(packed,52))==original
report={'passed':True,'production_ARM64_library':True,'original_73_body_decoder':True,'values_tested':list(range(15)),'fields':11,'native_float_conversion_all_165_cases':True,'all_face_hair_sleeve_and_other_packed_bits_preserved':True,'exact64_card_scope_even_with_different_appearance_id':True,'scope_cleared_after_build':True,'synthetic_records':True,'device_tested':False};(P/'model-native-validation.json').write_text(json.dumps(report,indent=2));print('MODEL_NATIVE_PASS')
