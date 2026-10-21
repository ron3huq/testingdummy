"""Original ARM64 accessors + compiled v6 on synthetic DB records, NOT a device test."""
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
 u.emu_start(addr,0x33000010,count=20000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
def get(p,index):
 call(0x82a84d4,p,index,0x33200000)
 return struct.unpack('<I',u.mem_read(0x33200000,4))[0]

import sys,sqlite3
sys.path[:0]=[str(r),str(r.parent/'android/user-gateway/work/tools')]
import native_overall
cfg=json.loads((r/'myleague_custom.json').read_text());can=json.loads((r.parent/'android/user-gateway/outputs/reference/canonical_rosters.json').read_text())
players={};teams={};heap=0x30000000;db=heap;XOR_KEY=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR_KEY)
ids=set(sum(cfg['native_rosters'].values(),[]))|set(map(int,cfg['base_overrides']))|set(map(int,cfg['card_overrides']))|set(map(int,cfg['base_adjustments']))|{52776558193083}
source=(r.parent/'android/tables/Player.bin').read_bytes();spare=[]
for off in range(0,len(source),400):
 candidate=struct.unpack_from('<Q',source,off+8)[0]
 if candidate and candidate not in ids and candidate not in spare:spare.append(candidate)
 if len(spare)==6:break
ids.update(spare)
for pid in sorted(ids):
 p=heap;heap+=0x1d0;players[pid]=p;w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR_KEY)
 role=can['positions'].get(str(pid),6);classic=cfg['classic_profiles'].get(str(pid));role=classic['roles'][0] if classic else role
 for index,value in [(0,role),(47,185)]+[(i,96 if classic else 70) for i in range(14,41) if i!=33]+[(33,2),(72,1)]:call(0x82a907c,p,index,value)
 # Vary unmodified thresholds and ceiling without relying on any copied implementation.
 if pid not in map(int,cfg['base_overrides']) and not classic:
  for row in cfg['base_adjustments'].get(str(pid),[]):call(0x82a907c,p,{'defensive_awareness':15,'defensive_engagement':26,'tackling':24,'aggression':25,'low_pass':21,'lofted_pass':22}[row['stat']],[70,83,84,98,99][pid%5])
w(db+0x2686098,'I',len(players))
for pid,p in players.items():assert call(0x823c8d4,db,0,pid)==p
heap=0x33300000
for tid in dict.fromkeys(list(cfg['native_rosters'])+list(cfg['team_names'])+['103']):
 p=heap;heap+=0x1000;teams[int(tid)]=p;u.mem_write(p,b'\x55'*0x700);w(p,'I',int(tid)<<14)
 if tid=='116':u.mem_write(p+4,b'Ajax\0\0')
 old=can['rosters'].get(tid,[]) if tid!='127' else []
 for i,pid in enumerate(old):w(p+0x110+i*16,'QQ',0,pid);w(p+0x3a2+i*2,'H',i+1)
 w(p+0x40c,'I',(len(old)<<9)|0x80000001)
def stub(uc,addr,size,data):
 if addr==0x33000040:value=teams.get(uc.reg_read(UC_ARM64_REG_W1)>>14,0)
 elif addr==0x82468d4:value=0x33201000
 else:return
 uc.reg_write(UC_ARM64_REG_X0,value);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,stub);w(0x33201040,'Q',db)
assert call(symbols['ensure_team'],127)==10
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4);call(symbols['configure_short'],0,0x82b4a7c)
# Original lookup must distinguish59835 from the complete existing Guerreiro card.
assert call(0x823c8d4,db,0,59835)!=players[52776558193083]
assert call(symbols['ensure_team'],127)==1
p=teams[127];before=bytes(u.mem_read(p,0x700));kane=players[47287];w(kane+0x40,'Q',0^XOR_KEY)
assert call(symbols['ensure_team'],127)==13 and bytes(u.mem_read(p,0x700))==before
w(kane+0x40,'Q',47287^XOR_KEY)
for tid,ids in cfg['native_rosters'].items():
 p=teams[int(tid)];before=bytes(u.mem_read(p,0x700));assert call(symbols['ensure_team'],int(tid))==1
 assert call(0x68fd47c,p)==len(ids)
 for i,pid in enumerate(ids):
  call(0x68fc714,p,i,0x33200000);assert u.reg_read(UC_ARM64_REG_X0)==0 and u.reg_read(UC_ARM64_REG_X1)==pid
  wanted=cfg['shirt_overrides'].get(tid,{}).get(str(pid))
  if wanted:assert struct.unpack('<H',u.mem_read(0x33200000,2))[0]==wanted
 after=bytes(u.mem_read(p,0x700));allowed=set(range(0x110,0x110+len(ids)*16))|set(range(0x3a2,0x3a2+len(ids)*2))|set(range(0x40c,0x410))
 if tid in cfg['team_names']:allowed |=set(range(4,74))|set(range(0x4a,0x4e))
 if tid in cfg['classic_teams']:allowed |=set(range(0x478,0x478+34))|set(range(0x49a,0x49a+34))|set(range(0x4d8,0x4d8+34))|set(range(0x4fa,0x4fa+34))|set(range(0x538,0x56a))
 if tid in ['1986','131','1987']:allowed |=set(range(0x56f,0x5bf))
 assert all(before[i]==after[i] for i in range(0x700) if i not in allowed),tid
 assert call(symbols['ensure_team'],int(tid))==1 and bytes(u.mem_read(p,0x700))==after
 if tid in cfg['classic_teams']:
  plan=cfg['classic_teams'][tid]['formation']
  for off in [0x478,0x49a,0x4d8,0x4fa]:
   for i,(role,x,y) in enumerate(plan):
    assert call(0x82b5f10,p+off,i)==role
    ptr=call(0x82b5f30,p+off,i);assert bytes(u.mem_read(ptr,2))==bytes([x,y])
  assert list(u.mem_read(p+0x538,len(ids)))==list(range(len(ids)))
  for pid in ids:
   pp=players[pid];params=[get(pp,i) for i in range(147)];assert params[72]==0
   assert max(native_overall.rating(params,i) for i in range(13))<=89
   before_params=list(params)
   for repeat in range(4):call(symbols['player_hook'],db,0,pid)
   assert [get(pp,i) for i in range(147)]==before_params
for target,donor in [(1986,114),(131,173),(1987,103)]:assert bytes(u.mem_read(teams[target]+0x56f,80))==bytes(u.mem_read(teams[donor]+0x56f,80))
from myleague_worlds import STAT_INDEX as stat
for pid in set(cfg['base_overrides'])|set(cfg['base_adjustments'])|set(cfg['card_overrides']):
 if pid in cfg['classic_profiles']:continue # NPC cap takes precedence here; owned-card handlers tested separately.
 pp=players[int(pid)];before=[get(pp,i) for i in range(147)];rule=cfg['card_overrides'].get(pid)or cfg['base_overrides'].get(pid)or{};edits={}
 for row in cfg['base_adjustments'].get(pid,[]):
  ix=stat[row['stat']];edits[ix]=min(99,before[ix]+row['delta']) if before[ix]<row['below'] else before[ix]
 edits.update({stat[k]:v for k,v in rule.get('stats',{}).items()});edits.update({i:1 for i in rule.get('skill_flags_add',[])});edits.update({i:0 for i in rule.get('skill_flags_remove',[])})
 expected=[edits.get(i,before[i]) for i in range(147)];expected[37]=min(127,expected[37]+7) if expected[37]>84 else expected[37]
 if 4<=expected[0]<=12 and not(expected[127] or expected[120]):expected[103]=1
 assert call(symbols['player_hook'],db,0,int(pid))==pp
 actual=[get(pp,i) for i in range(147)]
 assert actual==expected,(pid,[(i,expected[i],actual[i]) for i in range(147) if expected[i]!=actual[i]])
 for repeat in range(3):call(symbols['player_hook'],db,0,int(pid))
 assert [get(pp,i) for i in range(147)]==actual
for tid,row in cfg['team_names'].items():
 pp=teams[int(tid)];before=bytes(u.mem_read(pp,0x700));assert call(symbols['ensure_team'],int(tid))==1
 assert bytes(u.mem_read(call(0x82b4a74,pp),len(row['name'])+1))==row['name'].encode()+b'\0'
 sp=call(symbols['short_hook'],pp);assert bytes(u.mem_read(sp,len(row['short'])+1))==row['short'].encode()+b'\0'
 #4-byte short field must not clobber adjacent uint16 country/flags at+4e.
 assert bytes(u.mem_read(pp+0x4e,2))==before[0x4e:0x50]
for pid,power,role,low,blitz in zip(spare,[83,84,85,94,120,127],[0,3,4,12,8,11],[0,0,0,1,0,0],[0,0,0,0,1,0]):
 pp=players[pid]
 for index,value in [(37,power),(0,role),(127,low),(120,blitz),(103,0)]:call(0x82a907c,pp,index,value)
 call(symbols['player_hook'],db,0,pid)
 expected=min(127,power+7) if power>84 else power
 assert get(pp,37)==expected and get(pp,103)==int(4<=role<=12 and not(low or blitz))
 for repeat in range(20):call(symbols['player_hook'],db,0,pid)
 assert get(pp,37)==expected
# Native player detour is tested independently of direct hook calls.
import importlib.util
spec=importlib.util.spec_from_file_location('runtime',r/'select_team_runtime.py');runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
entry=0x823c8d4;cave=0x0b001000;u.mem_map(cave,4096);stolen=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(symbols['player_hook'])+b'\0'*16+stolen+runtime.jump(entry+4));call(symbols['configure_player'],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
assert call(entry,db,0,17592722922839)==players[17592722922839]
assert call(entry,db,0xdeadbeef00000000,17592722922839)==players[17592722922839] # typed key kind uses low32; upper padding is not an enum
assert call(symbols['ensure_team'],1222)==1
report=dict(status='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',device_tested=False,synthetic_database=True,native_roster_counts={k:len(v) for k,v in cfg['native_rosters'].items()},classic_profiles=len(cfg['classic_profiles']),checks=['original full64 player resolver / lower_bound / XOR decode; complete card IDs never truncated','all18 roster preflights, shirt getters and exact typed player entries','all12 classic formations4 variants through original role/coordinate getters; valid lineup order','all classic NPCs neutral OVR<=89 at every13 positions and no Marseille Turn','classic targets stable through repeated lookups, no progressive stat reduction','base, exact cards and all220 relative policies; global power boost/conditional Dipping Shot; original147 getter/setter','adjacent native bytes preserved including short-name +4e boundary','verified80-byte uniform block matches PSG/City/Liverpool donors','player hook via real atomic detour/trampoline including full64 Messi','missing player blocks roster writes'])
(r/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
