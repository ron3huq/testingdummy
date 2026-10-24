from pathlib import Path
s=Path('/workspace/ronaldo-work/73-ui/test_native.py').read_text().split("for tid,ids in cfg['native_rosters'].items():")[0];exec(s)
for cid in [89136418985303,89136418985302]:
 n=call(symbols['editor_add_player'],cid,0,3);assert n
 for typ,mode in [(4,2),(5,1),(6,2),(7,2)]:assert call(symbols['editor_accessory'],n,typ,mode)==1
 for index,values in [(43,[0,1]),(47,[140,187,220]),(48,[40,83,127,128,130]),(60,[0,16,22,90,127])]:
  for value in values:
   call(0x82a907c,players[cid],index,value);assert get(players[cid],index)==value
assert call(symbols['editor_commit'])==1
config=0x33230000;vector=0x33231000;spec=0x33232000
u.mem_write(config,b'\0'*0x230);w(config+0x210,'QQQ',vector,vector,vector+18*12)
for typ in range(18):call(0x68cff80,config,typ,0xffffffff,1)
def original_build(uc,addr,size,data):
 if addr==0x33000090:uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,original_build);call(symbols['configure_appearance_build'],0,0x33000090)
for cid in [89136418985303,89136418985302]:
 w(config+0x50,'I',0);w(spec+8,'Q',cid);call(symbols['appearance_build_hook'],config,spec)
 assert struct.unpack('<I',u.mem_read(config+0x50,4))[0]==1
 assert [u.mem_read(vector+typ*12+8,1)[0]for typ in range(4,8)]==[1,0,1,1]
w(config+0x50,'I',0);w(spec+8,'Q',123);call(symbols['appearance_build_hook'],config,spec);assert u.mem_read(config+0x50,4)==b'\0'*4
Path('/workspace/ronaldo-work/73-ui/sleeves-validation.json').write_text(json.dumps({'passed':True,'checks':['both custom64 cards: appearance build hook sets long sleeves and accessory entries before entity dispatch','unrelated card sleeve unchanged','all physical field bounds round-trip through actual73 getter/setter'],'device_tested':False},indent=2));print('SLEEVES_PASS')
