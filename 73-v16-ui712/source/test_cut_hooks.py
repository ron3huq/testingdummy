from pathlib import Path
P=Path('/workspace/73-ui712');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/apk/assets/gateway-release/work/tools/libselect_team.so'));exec(s)
from unicorn import UC_HOOK_CODE
pid=123456789876;actor=0x30020000;w(actor+0x10b0,'Q',pid);events=[]
def stub(uc,at,size,data):
 if at==0x33000100:events.append(('begin',uc.reg_read(UC_ARM64_REG_X0)));uc.reg_write(UC_ARM64_REG_X0,3)
 elif at==0x33000110:events.append(('end',uc.reg_read(UC_ARM64_REG_X0)))
 elif at in [0x33000120,0x33000130]:events.append(('detail'if at==0x33000120 else'common',[uc.reg_read(r)for r in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5]]))
 else:return
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);call(symbols['configure_cut_scope'],0x33000100,0x33000110);call(symbols['configure_cut_detail'],0,0x33000120);call(symbols['configure_cut_common'],0,0x33000130);assert call(symbols['editor_cut_add'],pid)==1;call(symbols['editor_cut_commit'])
for name in ['detail','common']:
 for id,model,var,expected in [(pid,15,7,True),(pid,901,1,True),(pid+1,15,7,False),(pid,999,77,False)]:
  w(actor+0x10b0,'Q',id);events.clear();u.reg_write(UC_ARM64_REG_X5,19);call(symbols['cut_'+name+'_hook'],actor,model,0,var,0)
  if expected:assert events==[('begin',actor),(name,[actor,model,1,var,0,19]),('end',3)],events
  else:assert events==[(name,[actor,model,0,var,0,19])],events
(P/'cut-hook-native-validation.json').write_text(json.dumps({'passed':True,'only_explicit_card_selection':True,'original_model_ID_unchanged':True,'detail_common_routes_remain_separate':True,'native_long_selected_only_for_cut_choice':True,'unsupported_variant_uses_original':True,'scope_closed_after_loader':True,'six_argument_forwarding':True,'Android_tested':False},indent=2));print('CUT_HOOKS_NATIVE_PASS')
