"""Run the real v18-compatible shirt hook AND original UE selector to LoadUniShirt.
Only kit availability/resource IDs and virtual update are modeled, not the sleeve branch.
Test with editor uninitialized and after an explicit conflicting short override.
"""
from pathlib import Path
import struct,json,hashlib,re
from unicorn import UC_HOOK_CODE
from unicorn.arm64_const import *
r=Path(__file__).resolve().parent
baseline=r.parents[1]/'hotfix-v18'
if not baseline.exists():baseline=r.parent/'references/v18'
s=(baseline/'validate_native.py').read_text().split('import sys,sqlite3')[0].replace("r=Path(__file__).parent","r=Path(__file__).resolve().parent").replace('/workspace/analysis/my-league/android/official-apk','/workspace/ronaldo-work/apk');exec(compile(s,'actual-elf-loader','exec'),globals())
import select_team_runtime as runtime
engine_bytes=engine.read_bytes();owner=0x30800000;actor=0x30810000;vt=0x30820000;noop=0x30821000;kit_control=0x30822000
w(owner+0x4d8,'Q',actor);w(vt+0x6b0,'Q',noop);u.mem_write(noop,bytes.fromhex('c0035fd6'));modeled=set()
def boundary(uc,addr,size,data):
 x0,x1,x2=[uc.reg_read(z) for z in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2]]
 if addr==0x3a8486c:ret=kit_control
 elif addr==0x3a84aec:assert x0==kit_control;w(x2+0x190,'IIII',100,101,200,201);ret=0
 elif addr==0x3a0d3fc:assert x0==actor+0xe18;ret=1
 elif addr==noop:ret=0
 else:return
 modeled.add(hex(addr));uc.reg_write(UC_ARM64_REG_X0,ret);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,boundary)
def prepare(pid,before):
 u.mem_write(actor,b'\0'*0x2000);w(actor,'Q',vt);w(actor+0x10b0,'Q',pid);w(actor+0x10f0,'I',before)
def run(kit):
 u.reg_write(UC_ARM64_REG_X0,owner);u.reg_write(UC_ARM64_REG_X1,kit);u.reg_write(UC_ARM64_REG_SP,0x32fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010);u.emu_start(0x3a0b28c,0x3a0b5f8,count=500000);assert u.reg_read(UC_ARM64_REG_PC)==0x3a0b5f8
 return bytes(u.mem_read(actor,0x2000)),tuple(u.reg_read(z) for z in [UC_ARM64_REG_W1,UC_ARM64_REG_W2,UC_ARM64_REG_W3])
targets={89135066911146,17592722922839,88044950524330,89138556572074,106781745353130};pids=list(targets)+[89135066911147,89135066911146+(1<<32),17592722922839+(1<<32),106781745353130,106734785925546,4522,52776558193083,105765448873424,88045755960841,88038776539586]
policy_source=(r/'select_team.c').read_text();named={cid:set(map(int,re.findall(r'(\d+)ULL',re.search('appearance_targets_'+str(cid)+r'\[\]=\{([^}]+)',policy_source).group(1)))) for cid in [518,122]}
old={}
for pid in pids:
 for before in [0,1]:
  for kit in [0,1,5]:prepare(pid,before);old[pid,before,kit]=run(kit)
entry=0x3a0b28c;cave=0xb000000;u.mem_map(cave,4096);body=engine_bytes[entry-0x4000:entry-0x4000+16];assert body.hex()=='fd7bbaa9fc6f01a9fa6702a9f85f03a9'
u.mem_write(cave,runtime.jump(symbols['appearance_shirt_hook'])+b'\0'*16+body[:4]+runtime.jump(entry+4));call(symbols['configure_appearance_shirt'],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
checks=[]
for editor_ready in [False,True]:
 if editor_ready:
  # These deliberately conflict with the requested long sleeves; runtime policy must win.
  for pid in [89135066911146,17592722922839]:assert call(symbols['editor_add_player'],pid,0,2)>0
  assert call(symbols['editor_commit'])==1
 for cid in [0,122,518,566,128,549]:
  call(symbols['activate_context'],cid)
  for (pid,before,kit),(old_actor,old_args) in old.items():
   prepare(pid,before);new,args=run(kit);want=bytearray(old_actor)
   # Original v18 also has explicit named competition policies for base Ronaldo.
   long=pid in targets or pid in named.get(cid,set())
   if pid==106734785925546:struct.pack_into('<I',want,0x10f0,0)
   elif long:struct.pack_into('<I',want,0x10f0,1)
   assert new==want,(editor_ready,cid,pid,before,kit)
   expected=(100,101,0) if pid==106734785925546 else (200,201,1) if long else old_args
   assert args==expected,(editor_ready,cid,pid,args,expected)
   checks.append([editor_ready,cid,pid,before,kit])
w(owner+0x4d8,'Q',0);call(entry,owner,1)
report={'status':'REAL_UE_SHIRT_SELECTION_WITH_AND_WITHOUT_EDITOR_PASS','cases':len(checks),'checks':checks,'engine_entry':'0x3a0b28c','stop_before_virtual_LoadUniShirt':'0x3a0b5f8','modeled_boundaries':sorted(modeled),'short_resource_sentinels':[100,101,0],'long_resource_sentinels':[200,201,1],'only_actor_sleeve_word_changes':True,'requires_editor_overlay_to_work':False,'rendered_long_sleeve_on_phone_verified':False,'hook_sha256':hashlib.sha256((r/'libselect_team.so').read_bytes()).hexdigest()}
(r.parent/'sleeve-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'cases')
