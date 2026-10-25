from pathlib import Path
import json,hashlib
P=Path('/workspace/ronaldo-work/73-ui4');s=(P/'test_native.py').read_text();exec(s[:s.index('import sys,sqlite3')]);face=load(P/'payload/work/tools/libnoodle_hair.so',0x36000000);record=0x30001000;key=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',key)
def backing(uc,addr,size,data):
 if addr==0x33000100:uc.reg_write(UC_ARM64_REG_X0,record);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,backing);call(face['configure_record_lookup'],0,0x33000100);call(face['noodle_enable'],1);call(symbols['configure_classic_notify'],face['noodle_set_league_scope'])
for pid in [88044950524330,89135066911146,106726716084650,89136418985303,89136418985302,123]:
 for cid in [518,473,0,122]:
  u.mem_write(record,b'\0'*0x200);w(record+0x38,'I',0);w(record+0x40,'Q',pid^key)
  for i,v in [(0,12),(47,185)]+[(i,2)for i in range(1,14)]:call(0x82a907c,record,i,v)
  call(symbols['activate_context'],cid);assert call(face['noodle_record_lookup_hook'],0,0,pid)==record
  actual=[get(record,i)for i in range(14)]
  if cid in [518,473]or pid not in [88044950524330,89135066911146,106726716084650]:assert actual==[12]+[2]*13,(pid,cid,actual)
  else:
   expected=[9]+[2 if i==3 else 0 for i in range(1,14)]if pid==88044950524330 else[10]+[2 if i in[9,4]else 0 for i in range(1,14)];assert actual==expected,(pid,cid,actual)
old=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source/noodle_hair.c').read_text();new=Path('/workspace/testingdummy/73-v16-ui4/source/noodle_hair.c').read_text()
for line in ['static volatile u32 classic_context;\n','__attribute__((visibility("default"))) void noodle_set_league_scope(u32 cid){__atomic_store_n(&classic_context,cid,__ATOMIC_RELEASE);}\n',' u32 cid=__atomic_load_n(&classic_context,__ATOMIC_ACQUIRE);if(cid==518||cid==473)return;\n']:new=new.replace(line,'')
assert new==old,'face source altered beyond explicit position guard'
(P/'face-scope-validation.json').write_text(json.dumps({'passed':True,'checks':['Compiled ARM64 callback reaches face library; all13 positions survive late face lookup in518/473','Original exact CR7 position policy retained outside the two leagues; custom cards/unrelated cards unchanged','Face native C source identical after removing three added scope-guard lines; renderer, material lifecycle, mappings, retargeting unchanged'],'phone_tested':False},indent=2));print('FACE_SCOPE_PASS')
