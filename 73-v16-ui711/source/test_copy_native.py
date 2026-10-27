from pathlib import Path
P=Path('/tmp/73-ui711');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE
pid=105837926394281;donor=89138556572074;dst=0x30020000;src=0x30021000;ctx=0x30022000;db=0x30023000;XOR=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR)
for ptr,id in [(dst,pid),(src,donor)]:u.mem_write(ptr,bytes(0x500));w(ptr+0x38,'I',0);w(ptr+0x40,'Q',id^XOR)
w(ctx+0x40,'Q',db)
fields={43:1,47:195,48:87,50:2,51:1,52:5,53:12,54:6,55:11,56:17,57:6,58:10,59:109,60:3,63:1,64:0,65:1,66:0,67:1,68:0,69:1}
for ix in range(147):call(0x82a907c,dst,ix,0)
for ix,v in fields.items():assert call(0x82a907c,src,ix,v)
for ix,v in [(0,9),(14,88),(20,93),(33,2),(42,1),(46,23),(70,1),(143,1)]:call(0x82a907c,dst,ix,v)
original=[get(dst,i)for i in range(147)];source_before=bytes(u.mem_read(src,0x500))
valid=[True]
def stub(uc,addr,size,data):
 if addr==0x82468d4:uc.reg_write(UC_ARM64_REG_X0,ctx)
 elif addr==0x33000120:
  assert uc.reg_read(UC_ARM64_REG_X2)==donor;uc.reg_write(UC_ARM64_REG_X0,src if valid[0]else 0)
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);call(symbols['configure_team'],0,0x33000130);call(symbols['configure_player'],0,0x33000120)
n=call(symbols['editor_add_player'],pid,0,0);assert n;assert call(symbols['editor_parameter'],n,43,0)==1;assert call(symbols['editor_parameter'],n,46,29)==1

for ix,v in [(33,3),(42,2),(45,3)]:assert call(symbols['editor_parameter'],n,ix,v)==1
assert call(symbols['editor_commit'])==1;assert call(symbols['editor_copy_add'],pid,donor)==1;call(symbols['editor_copy_commit']);call(symbols['editor_apply_player'],dst,pid)
values=[get(dst,i)for i in range(147)];expect=dict(fields,**{})
for i in range(147):assert values[i]==({33:3,42:2,43:0,45:3,46:29}.get(i,fields.get(i,original[i]))),(i,values[i])
assert call(symbols['editor_copy_status'],2)==1;before=bytes(u.mem_read(dst,0x1d0));call(symbols['editor_apply_player'],dst,pid);assert bytes(u.mem_read(dst,0x1d0))==before
valid[0]=False;call(symbols['editor_apply_player'],dst,pid);assert call(symbols['editor_copy_status'],3)==1;assert bytes(u.mem_read(dst,0x1d0))==before
assert bytes(u.mem_read(src,0x500))==source_before
(P/'copy-native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64':True,'original_native147_getter_and_setter_used':True,'21_body_foot_motion_celebration_AI_fields_copied':list(fields),'target_explicit_age_and_foot_override_win':True,'weak_foot_usage_accuracy_injury_editor_native_setters_verified':True,'all_unrelated_parameters_and_fullID_unchanged':True,'idempotent':True,'missing_donor_safely_rejected':True,'source_record_unmodified':True,'Android_tested':False,'all_identity_keyed_signature_animations_verified':False},indent=2));print('COPY_NATIVE_PASS')
