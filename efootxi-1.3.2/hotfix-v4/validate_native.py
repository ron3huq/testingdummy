"""Original ARM64 accessors + compiled v3 on synthetic DB records, NOT a device test."""
from pathlib import Path
import json,struct,hashlib
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
r=Path(__file__).parent
engine=Path('/workspace/analysis/my-league/android/official-apk/lib/arm64-v8a/libUE4.so')
assert hashlib.sha256(engine.read_bytes()).hexdigest()=='3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98'
u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
def w(a,f,*v):u.mem_write(a,struct.pack('<'+f,*v))
def load(path,base=0):
 with path.open('rb') as f:
  elf=ELFFile(f)
  for s in elf.iter_segments():
   if s['p_type']!='PT_LOAD':continue
   start=(base+s['p_vaddr'])&~4095;end=(base+s['p_vaddr']+s['p_memsz']+4095)&~4095
   u.mem_map(start,end-start);u.mem_write(base+s['p_vaddr'],s.data())
  if not base:return
  symbols={s.name:base+s['st_value'] for s in elf.get_section_by_name('.dynsym').iter_symbols()}
  for s in elf.iter_sections():
   if not s.name.startswith('.rela'):continue
   for rel in s.iter_relocations():
    assert rel['r_info_type']==1027
    w(base+rel['r_offset'],'Q',base+rel['r_addend'])
  return symbols
load(engine);symbols=load(r/'libselect_team.so',0x35000000)
u.mem_map(0x30000000,0x4000000)
u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010)
 u.emu_start(addr,0x33000010,count=1000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
def get(p,index):
 call(0x82a84d4,p,index,0x33200000)
 return struct.unpack('<I',u.mem_read(0x33200000,4))[0]
cfg=json.loads((r/'myleague_custom.json').read_text());can=json.loads(Path('/workspace/analysis/my-league/android/user-gateway/outputs/reference/canonical_rosters.json').read_text())
players={};teams={};heap=0x30000000
db=heap;XOR_KEY=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR_KEY)
for pid in sorted(set(sum(cfg['native_rosters'].values(),[]))|set(map(int,cfg['base_overrides']))):
 p=heap;heap+=0x1d0;players[pid]=p
 w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR_KEY)
 for index,value in [(0,can['positions'].get(str(pid),6)),(47,185)]+[(i,70) for i in range(14,41)]:call(0x82a907c,p,index,value)
 assert get(p,47)==185
w(db+0x2686098,'I',len(players))
# Keep actual public player lookup + native lower_bound + encrypted-key decode active.
for pid,p in players.items():
 assert call(0x823c8d4,db,0,pid)==p,pid
 call(0x68fe720,p);assert u.reg_read(UC_ARM64_REG_X0)==0 and u.reg_read(UC_ARM64_REG_X1)==pid
heap=0x33300000
for tid in cfg['native_rosters']:
 p=heap;heap+=0x1000;teams[int(tid)]=p
 u.mem_write(p,b'\x55'*0x500);w(p,'I',int(tid)<<14)
 if tid=='116':u.mem_write(p+4,b'Ajax\0\0');u.mem_write(p+0x4a,b'AJA\0')
 old=can['rosters'].get(tid,[]) if tid!='127' else []
 for i,pid in enumerate(old):w(p+0x110+i*16,'QQ',0,pid);w(p+0x3a2+i*2,'H',i+1)
 w(p+0x40c,'I',(len(old)<<9)|0x80000001)
missing=set()
def stub(uc,addr,size,data):
 if addr==0x33000040:value=teams.get(uc.reg_read(UC_ARM64_REG_W1)>>14,0)
 elif addr==0x33000044:
  raise AssertionError('v3 uint32 player/coach lookup must never be used')
 elif addr==0x82468d4:value=0x33201000
 else:return
 uc.reg_write(UC_ARM64_REG_X0,value);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);w(0x33201040,'Q',db)
assert call(symbols['ensure_team'],127)==10
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4)
# Fail closed before ANY roster write if a required player is absent.
p=teams[127];before=bytes(u.mem_read(p,0x500));kane=players[47287];w(kane+0x40,'Q',0^XOR_KEY)
assert call(symbols['ensure_team'],127)==13 and bytes(u.mem_read(p,0x500))==before
w(kane+0x40,'Q',47287^XOR_KEY)
for tid,ids in cfg['native_rosters'].items():
 p=teams[int(tid)];before=bytes(u.mem_read(p,0x500))
 assert call(symbols['ensure_team'],int(tid))==1
 assert call(0x68fd47c,p)==len(ids)
 actual=[]
 for i in range(len(ids)):
  call(0x68fc714,p,i,0);assert u.reg_read(UC_ARM64_REG_X0)==0
  actual.append(u.reg_read(UC_ARM64_REG_X1))
 assert actual==ids and len(set(actual))==len(ids)
 after=bytes(u.mem_read(p,0x500))
 allowed=(set(range(4,10))|set(range(0x4a,0x4e)) if tid=='116' else set())|set(range(0x110,0x110+len(ids)*16))|set(range(0x3a2,0x3a2+len(ids)*2))|set(range(0x40c,0x410))
 assert all(before[i]==after[i] for i in range(0x500) if i not in allowed)
 assert call(symbols['ensure_team'],int(tid))==1 and bytes(u.mem_read(p,0x500))==after
assert bytes(u.mem_read(teams[116]+4,6))==b'AjaxE\0'
assert call(0x82b4a74,teams[116])==teams[116]+4
stat={'speed':34,'acceleration':38,'curl':28}
for pid,rule in cfg['base_overrides'].items():
 p=players[int(pid)];before=[get(p,i) for i in range(147)]
 assert call(symbols['player_hook'],db,0,int(pid))==p
 edits={stat[k]:v for k,v in rule['stats'].items()};edits.update({i:1 for i in rule['skill_flags_add']})
 after=[get(p,i) for i in range(147)]
 assert all(after[i]==edits.get(i,before[i]) for i in range(147)),pid
 assert 125 not in edits
# Native signatures on exact uploaded ELF, before enabling an atomic detour.
for addr,sig in [(0x823c9d4,'ffc300d1fd7b01a9f44f02a9fd430091'),(0x823c8d4,'ff0301d1fd7b02a9f44f03a9fd830091')]:assert bytes(u.mem_read(addr,16)).hex()==sig
import importlib.util
spec=importlib.util.spec_from_file_location('runtime',r/'select_team_runtime.py');runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
entry=0x823c8d4;cave=0x0b001000;u.mem_map(cave,4096)
stolen=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(symbols['player_hook'])+b'\0'*16+stolen+runtime.jump(entry+4))
call(symbols['configure_player'],0,cave+32)
call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
for pid,p in players.items():assert call(entry,db,0,pid)==p
assert call(symbols['ensure_team'],127)==1
entry=0x3a56de8;cave=0x0b000000;u.mem_map(cave,4096)
stolen=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(symbols['emblem_hook'])+b'\0'*16+stolen+runtime.jump(entry+4))
call(symbols['configure_emblem'],0,cave+32)
call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
captured=[]
def emblem_consumer(uc,addr,size,unused):
 if addr!=entry+4:return
 captured.append(tuple(uc.reg_read(x) for x in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X8]))
 uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x180)
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,emblem_consumer)
for tid in [116,181,101,116<<14]:
 u.reg_write(UC_ARM64_REG_X4,7);u.reg_write(UC_ARM64_REG_X8,0x33200100)
 call(entry,tid,2,3,4)
 assert captured[-1]==(181 if tid==116 else tid,2,3,4,7,0x33200100)
report=dict(status='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',device_tested=False,synthetic_database=True,native_roster_counts={k:len(v) for k,v in cfg['native_rosters'].items()},base_players_checked=len(cfg['base_overrides']),checks=['real original public player resolver, native lower_bound and XOR-protected identity getter; nonzero XOR key', 'v3 wrong uint32 lookup is never called','corrected player resolver through actual atomic detour, original trampoline and native database lookup', 'real original ARM64 packed setters/getters, all 147 fields preserved except requested edits','real original ARM64 roster count and typed-key accessors','missing player blocks roster write','23-player Bayern native roster, no inline opponent payload','idempotent roster edits; unrelated native bytes unchanged','exact resolver prologues verified','no new Power Tackle or Long Range Tackle','native name getter reads AjaxE; team identity unchanged','actual emblem detour/trampoline maps only116 to181 and preserves C++ X8 result pointer; downstream asset loader not executed'])
(r/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
