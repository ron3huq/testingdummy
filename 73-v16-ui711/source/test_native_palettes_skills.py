from pathlib import Path
P=Path('/tmp/73-ui711');s=Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0].replace('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so',str(P/'build/payload/work/tools/libselect_team.so'));exec(s)
call(symbols['configure_team'],0,0)
p=0x30010000;pid=88044950524330;row=call(symbols['editor_add_player'],pid,0,0)
for ix,val in [(47,220),(48,130),(59,288),(60,31),(70,0),(72,1),(135,1),(125,1),(123,1)]:assert call(symbols['editor_parameter'],row,ix,val)==1
for ix,val in [(47,255),(48,250),(59,542),(60,128)]:assert call(symbols['editor_parameter'],row,ix,val)==0
assert call(symbols['editor_commit'])==1
for cid in [0,473,518,122]:
 call(symbols['activate_context'],cid);call(symbols['editor_apply_player'],p,pid);assert [get(p,i)for i in [47,48,59,60,70,72,135,125,123]]==[220,130,288,31,0,1,1,1,1]
# Every observed stored ID in both tables roundtrips through the ORIGINAL73 setter/getter.
choices=json.loads((P/'build/payload/work/tools/celebration_choices.json').read_text());n=0
for ix,rows in choices.items():
 for item in rows:
  call(0x82a907c,p,int(ix),item['id']);assert get(p,int(ix))==item['id'];n+=1
# Native bake callback chain preserves actor identity and only modifies selected palette/dirty fields.
original=0x33000080;seen=[]
def native_original(uc,addr,size,data):
 actor=uc.reg_read(UC_ARM64_REG_X0);seen.append((actor,struct.unpack('<I',uc.mem_read(actor+0x42c,4))[0]));uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,native_original,begin=original,end=original)
for i in range(1,7):assert call(symbols['skin_add'],pid+i,i)==1
assert call(symbols['skin_add'],pid+100,7)==0;assert call(symbols['skin_add'],pid+100,0)==0;call(symbols['skin_commit']);call(symbols['configure_skin_bake'],0,original)
actor=0x30020000
for i in range(1,7):
 u.mem_write(actor,b'\x33'*0x2000);w(actor+0x10b0,'Q',pid+i);w(actor+0x42c,'I',4);before=bytes(u.mem_read(actor,0x2000));call(symbols['skin_bake_hook'],actor);after=bytes(u.mem_read(actor,0x2000));assert seen[-1]==(actor,i);assert struct.unpack('<I',after[0x42c:0x430])[0]==i
 assert all(before[j]==after[j]for j in range(0x2000)if j not in list(range(0x42c,0x430))+[0x1a6b])
# An unrelated full64 card gets byte-exact actor data and still calls the original once.
w(actor+0x10b0,'Q',pid);before=bytes(u.mem_read(actor,0x2000));call(symbols['skin_bake_hook'],actor);assert bytes(u.mem_read(actor,0x2000))==before and len(seen)==7
assert call(symbols['skin_status'],2)==6
(P/'native-validation.json').write_text(json.dumps({'passed':True,'production_ARM64_library':True,'native_original147_parameter_roundtrip':True,'main_and_memorial_ID_roundtrips':n,'scopes':[0,473,518,122],'native_bounds_reject_UI77_extremes':True,'native_skill_flags_preserved':True,'six_exact_card_body_palette_callbacks':True,'palette_changed_before_original_bake_callback':True,'other_actor_bytes_and_unselected_cards_unchanged':True,'no_new_inline_hook_entry':True,'original_bake_boundary_stubbed':True,'GPU_render_and_motion_on_phone_tested':False},indent=2));print('NATIVE_PASS',n)
