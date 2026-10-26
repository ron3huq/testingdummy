from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so','/workspace/ronaldo-work/73-ui77/payload/work/tools/libselect_team.so'))
relocs=json.loads(Path('/workspace/ronaldo-work/73-ui/relocs.json').read_text())
for a,v in relocs.items():
 addr=int(a)
 if 0x988e000<=addr<0x9891000:w(addr,'Q',int(v))
def cstr(addr):
 out=bytearray()
 for i in range(128):
  v=u.mem_read(addr+i,1)[0]
  if not v:break
  out.append(v)
 return bytes(out)
def stub(uc,addr,size,data):
 if addr==0x8c1efd0:
  a=cstr(uc.reg_read(UC_ARM64_REG_X0));b=cstr(uc.reg_read(UC_ARM64_REG_X1));uc.reg_write(UC_ARM64_REG_X0,0 if a==b else 1);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);body=0x30010000;name=0x30011000;u.mem_write(body,b'\0'*64);u.mem_write(body,struct.pack('<f',180));u.mem_write(name,b'sk_upperarm_l\0')
def scale():
 call(0x68d2b4c,body,name);return struct.unpack('<4f',u.reg_read(UC_ARM64_REG_Q0).to_bytes(16,'little'))[:3]
baseline=scale();u.mem_write(body+0x20,struct.pack('<f',1));longarm=scale();u.mem_write(body+0x20,struct.pack('<f',-1));shortarm=scale();assert longarm[0]>baseline[0]>shortarm[0],(baseline,longarm,shortarm)
Path('/workspace/ronaldo-work/73-ui77/bone-consumer-validation.json').write_text(json.dumps({'passed':True,'actual_original73_skeletal_bone_scale_consumer':'0x68d2b4c','body_field_offset':'0x20 arm length','bone':'sk_upperarm_l','native_neutral_scale':baseline,'native_max_scale':longarm,'native_min_scale':shortarm,'native_function_table_relocations_applied':True,'strcmp_boundary_stubbed':True,'device_tested':False},indent=2));print('BONE_CONSUMER_PASS',baseline,longarm,shortarm)

from unicorn import UC_HOOK_INTR
pid=88045755960841;spec=body-0x10;dest=body+0x2000
u.mem_write(body,b'\0'*64);u.mem_write(body,struct.pack('<f',180));w(spec+8,'Q',pid)
assert call(symbols['model_add'],pid,sum((14 if i==0 else 15)<<(i*4)for i in range(11)))==1;call(symbols['model_commit'])
call(symbols['configure_appearance_build'],0,0x33000120)
def builder(uc,addr,size,data):
 if addr==0x33000120:uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
def intr(uc,number,data):
 assert uc.reg_read(UC_ARM64_REG_X8)==178;uc.reg_write(UC_ARM64_REG_X0,1234)
u.hook_add(UC_HOOK_CODE,builder);u.hook_add(UC_HOOK_INTR,intr);call(symbols['appearance_build_hook'],dest,spec);result=scale();assert abs(result[0]-1.05)<1e-6;assert call(symbols['model_status'],4)==1
path=Path('/workspace/ronaldo-work/73-ui77/bone-consumer-validation.json');report=json.loads(path.read_text());report.update(production_model_configuration_through_build_hook_to_original_bone_consumer=True,final_write_telemetry_verified=True,end_to_end_arm_scale=result);path.write_text(json.dumps(report,indent=2));print('MODEL_TO_BONE_PASS',result)
