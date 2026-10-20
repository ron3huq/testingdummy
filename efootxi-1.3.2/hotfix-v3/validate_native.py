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
u.mem_map(0x30000000,0x2000000);u.mem_map(0x33000000,0x2000)
u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010)
 u.emu_start(addr,0x33000010,count=1000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
def get(p,index):
 call(0x82a84d4,p,index,0x30000000)
 return struct.unpack('<I',u.mem_read(0x30000000,4))[0]
cfg=json.loads((r/'myleague_custom.json').read_text());can=json.loads(Path('/workspace/analysis/my-league/android/user-gateway/outputs/reference/canonical_rosters.json').read_text())
players={};teams={};heap=0x30100000
for pid in set(sum(cfg['native_rosters'].values(),[]))|set(map(int,cfg['base_overrides'])):
 p=heap;heap+=0x100;players[pid]=p
 w(p+0x38,'I',0);w(p+0x40,'Q',pid)
 for index,value in [(0,can['positions'].get(str(pid),6)),(47,185)]+[(i,70) for i in range(14,41)]:call(0x82a907c,p,index,value)
 assert get(p,47)==185
for tid in cfg['native_rosters']:
 p=heap;heap+=0x1000;teams[int(tid)]=p
 u.mem_write(p,b'\x55'*0x500);w(p,'I',int(tid)<<14)
 old=can['rosters'].get(tid,[]) if tid!='127' else []
 for i,pid in enumerate(old):w(p+0x110+i*16,'QQ',0,pid);w(p+0x3a2+i*2,'H',i+1)
 w(p+0x40c,'I',(len(old)<<9)|0x80000001)
missing=set()
def stub(uc,addr,size,data):
 if addr==0x33000040:value=teams.get(uc.reg_read(UC_ARM64_REG_W1)>>14,0)
 elif addr==0x33000044:
  pid=uc.reg_read(UC_ARM64_REG_W1);value=0 if pid in missing else players.get(pid,0)
 elif addr==0x82468d4:value=0x30001000
 else:return
 uc.reg_write(UC_ARM64_REG_X0,value);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);w(0x30001040,'Q',0x30002000)
assert call(symbols['ensure_team'],127)==10
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x33000044)
# Fail closed before ANY roster write if a required player is absent.
p=teams[127];before=bytes(u.mem_read(p,0x500));missing.add(47287)
assert call(symbols['ensure_team'],127)==13 and bytes(u.mem_read(p,0x500))==before
missing.clear()
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
 allowed=set(range(0x110,0x110+len(ids)*16))|set(range(0x3a2,0x3a2+len(ids)*2))|set(range(0x40c,0x410))
 assert all(before[i]==after[i] for i in range(0x500) if i not in allowed)
 assert call(symbols['ensure_team'],int(tid))==1 and bytes(u.mem_read(p,0x500))==after
stat={'speed':34,'acceleration':35,'curl':28}
for pid,rule in cfg['base_overrides'].items():
 p=players[int(pid)];before=[get(p,i) for i in range(147)]
 assert call(symbols['player_hook'],0x30002000,int(pid))==p
 edits={stat[k]:v for k,v in rule['stats'].items()};edits.update({i:1 for i in rule['skill_flags_add']})
 after=[get(p,i) for i in range(147)]
 assert all(after[i]==edits.get(i,before[i]) for i in range(147)),pid
 assert 125 not in edits
# Native signatures on exact uploaded ELF, before enabling an atomic detour.
for addr,sig in [(0x823c9d4,'ffc300d1fd7b01a9f44f02a9fd430091'),(0x823cfd0,'fd7bbea9f44f01a9fd030091f30300aa')]:assert bytes(u.mem_read(addr,16)).hex()==sig
report=dict(status='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',device_tested=False,synthetic_database=True,native_roster_counts={k:len(v) for k,v in cfg['native_rosters'].items()},base_players_checked=len(cfg['base_overrides']),checks=['real original ARM64 packed setters/getters, all 147 fields preserved except requested edits','real original ARM64 roster count and typed-key accessors','missing player blocks roster write','23-player Bayern native roster, no inline opponent payload','idempotent roster edits; unrelated native bytes unchanged','exact resolver prologues verified','no new Power Tackle or Long Range Tackle'])
(r/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
