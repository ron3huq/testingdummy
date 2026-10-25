"""Original ARM64 accessors + compiled v6 on synthetic DB records, NOT a device test."""
from pathlib import Path
import json,struct,hashlib
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
r=Path('/workspace/ronaldo-work/73-ui6/native-test')
engine=Path('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so')
assert hashlib.sha256(engine.read_bytes()).hexdigest()=='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
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
load(engine);symbols=load(Path('/workspace/ronaldo-work/73-ui6/payload/work/tools/libselect_team.so'),0x35000000)
u.mem_map(0x30000000,0x4000000)
u.reg_write(UC_ARM64_REG_TPIDR_EL0,0x33001000)
def call(addr,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x31fff000);u.reg_write(UC_ARM64_REG_LR,0x33000010)
 u.emu_start(addr,0x33000010,count=20000000)
 assert u.reg_read(UC_ARM64_REG_PC)==0x33000010
 return u.reg_read(UC_ARM64_REG_X0)
def get(p,index):
 call(0x82a84d4,p,index,0x33200000)
 return struct.unpack('<I',u.mem_read(0x33200000,4))[0]

import sys,sqlite3
sys.path.insert(0,"/workspace/ronaldo-work/73-ui6/payload/work/tools")
sys.path[:0]=[str(r),str(r.parent/'android/user-gateway/work/tools')]
sys.path.insert(0,'/workspace/ronaldo-work/73-v25-full/test-gateway/work/tools')
import native_overall
cfg=json.loads((r/'myleague_custom.json').read_text());can=json.loads((Path('/workspace/ronaldo-work/73-v25-full/android/user-gateway/outputs/reference/canonical_rosters.json')).read_text())
players={};teams={};heap=0x30000000;db=heap;XOR_KEY=0x1a2b3c4d5e6f7a8b;w(0xa52e030,'Q',XOR_KEY)
ids=set(sum(cfg['native_rosters'].values(),[]))|set(map(int,cfg['base_overrides']))|set(map(int,cfg['card_overrides']))|set(map(int,cfg['base_adjustments']))|{52776558193083}
source=(Path('/workspace/ronaldo-work/73-ui3/Player-decoded.bin')).read_bytes();spare=[]
for off in range(0,len(source),400):
 candidate=struct.unpack_from('<Q',source,off+8)[0]
 if candidate and candidate not in ids and candidate not in spare:spare.append(candidate)
 if len(spare)==6:break
ids.update(spare);ids.update([89136418985303,89136418985302])
for pid in sorted(ids):
 p=heap;heap+=0x1d0;players[pid]=p;w(p+0x38,'I',0);w(p+0x40,'Q',pid^XOR_KEY)
 role=can['positions'].get(str(pid),6);classic=cfg['classic_profiles'].get(str(pid));role=classic['roles'][0] if classic else role
 for index,value in [(0,role),(47,185)]+[(i,96 if classic else 70) for i in range(14,41) if i!=33]+[(33,2),(72,1)]:call(0x82a907c,p,index,value)
 for i in range(1,14):call(0x82a907c,p,i,(i+pid)%3)
 # Vary unmodified thresholds and ceiling without relying on any copied implementation.
 if pid not in map(int,cfg['base_overrides']) and not classic:
  for row in cfg['base_adjustments'].get(str(pid),[]):call(0x82a907c,p,{'defensive_awareness':15,'defensive_engagement':26,'tackling':24,'aggression':25,'low_pass':21,'lofted_pass':22}[row['stat']],[70,83,84,98,99][pid%5])
source_position_fields={pid:[get(p,i)for i in range(14)]for pid,p in players.items()}
# The 73 build patches the backing DB search (0x823e0c8) for extended
# records. Model that initialized-DB boundary; execute the actual 73
# accessors and the unchanged My League native hooks on returned records.
def initialized_lookup(uc,addr,size,data):
 if addr!=0x823c8d8:return
 kind=uc.reg_read(UC_ARM64_REG_W1);pid=uc.reg_read(UC_ARM64_REG_X2)
 value=players.get(pid,0) if kind==0 else 0
 uc.reg_write(UC_ARM64_REG_X0,value)
 uc.reg_write(UC_ARM64_REG_SP,uc.reg_read(UC_ARM64_REG_SP)+0x40)
 uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,initialized_lookup)
w(db+0x2686098,'I',len(players))
for pid,p in players.items():assert call(0x823c8d4,db,0,pid)==p
heap=0x33300000
for tid in dict.fromkeys(list(cfg['native_rosters'])+list(cfg['team_names'])+list(map(str,cfg['visual_aliases'].values()))+['103','351','352','242','245','100','108','109']):
 p=heap;heap+=0x1000;teams[int(tid)]=p;u.mem_write(p,b'\x55'*0x700);w(p,'I',int(tid)<<14)
 if tid=='116':u.mem_write(p+4,b'Ajax\0\0')
 u.mem_write(p+0x56f,bytes((int(tid)+i)%256 for i in range(80)))
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
 call(symbols['activate_context'],cfg['classic_teams'][tid].get('competition',518) if tid in cfg['classic_teams'] else 0)
 p=teams[int(tid)];before=bytes(u.mem_read(p,0x700));assert call(symbols['ensure_team'],int(tid))==1
 assert call(0x68fd47c,p)==len(ids)
 for i,pid in enumerate(ids):
  call(0x68fc714,p,i,0x33200000);assert u.reg_read(UC_ARM64_REG_X0)==0 and u.reg_read(UC_ARM64_REG_X1)==pid
  wanted=cfg['shirt_overrides'].get(tid,{}).get(str(pid))
  if wanted:assert struct.unpack('<H',u.mem_read(0x33200000,2))[0]==wanted
 after=bytes(u.mem_read(p,0x700));allowed=set(range(0x110,0x110+len(ids)*16))|set(range(0x3a2,0x3a2+len(ids)*2))|set(range(0x40c,0x410))
 if tid in cfg['match_environment']['home_stadiums']:allowed|=set(range(0x3f4,0x3f8))
 if tid in cfg['team_names']:allowed |=set(range(4,74))|set(range(0x4a,0x4e))
 if tid in cfg['classic_teams']:allowed |=set(range(0x478,0x478+34))|set(range(0x49a,0x49a+34))|set(range(0x4d8,0x4d8+34))|set(range(0x4fa,0x4fa+34))|set(range(0x538,0x56a))
 if tid in cfg['visual_aliases']:allowed |=set(range(0x56f,0x5bf))
 assert all(before[i]==after[i] for i in range(0x700) if i not in allowed),tid
 assert call(symbols['ensure_team'],int(tid))==1 and bytes(u.mem_read(p,0x700))==after
 if tid in cfg['classic_teams']:
  plan=cfg['classic_teams'][tid]['formation']
  for off in [0x478,0x49a,0x4d8,0x4fa]:
   for i,(role,x,y) in enumerate(plan):
    assert call(0x82b5f10,p+off,i)==role
    ptr=call(0x82b5f30,p+off,i);assert bytes(u.mem_read(ptr,2))==bytes([x,y])
  assert list(u.mem_read(p+0x538,len(ids)))==list(range(len(ids)))
  assert list(u.mem_read(p+0x560,6))==cfg['classic_teams'][tid]['set_piece_taker']
  assert u.mem_read(p+0x569,1)[0]==cfg['classic_teams'][tid]['responsibilities']['captain']
  for pid in ids:
   pp=players[pid];params=[get(pp,i) for i in range(147)];assert params[72]==0
   assert native_overall.rating(params,params[0])==cfg['classic_profiles'][str(pid)]['target_ovr'] and params[108]==0
   expected=list(source_position_fields[pid]);profile=cfg['classic_profiles'][str(pid)]
   if profile.get('competition')==473:expected[0]=profile['formation_role']
   expected[1:14]=[2]*13
   assert params[:14]==expected,(pid,params[:14],expected)
   before_params=list(params)
   for repeat in range(4):call(symbols['player_hook'],db,0,pid)
   assert [get(pp,i) for i in range(147)]==before_params
call(symbols['activate_context'],0)
for target,donor in [(int(k),v) for k,v in cfg['visual_aliases'].items()]:assert bytes(u.mem_read(teams[target]+0x56f,80))==bytes(u.mem_read(teams[donor]+0x56f,80))
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
# OVR transitions are absolute, reversible and identical to Python policy.
from myleague_balance import balance
for pid in spare:
 pp=players[pid];call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid);baseline=[get(pp,i) for i in range(147)]
 for cid in [518,566,122,518,566,0]:
  call(symbols['activate_context'],cid);call(symbols['player_hook'],db,0,pid);actual=[get(pp,i) for i in range(147)]
  target=balance(baseline,cid,target=92 if cid==518 else None) if cid else baseline
  if cid==122 and baseline[0] in (1,2,3):
   for flag in [106,111,113,115]:target[flag]=1
  assert actual==target,(pid,cid,[(i,actual[i],target[i]) for i in range(147) if actual[i]!=target[i]])
  for repeat in range(5):call(symbols['player_hook'],db,0,pid)
  assert [get(pp,i) for i in range(147)]==target
call(symbols['activate_context'],0)
# Disabled compatibility API must not access any engine stage helper.
def forbidden_stadium_call(uc,addr,size,data):
 if addr in (0x3033e64,0x73f46a4,0x3422074,0x3421e38):raise AssertionError('disabled stage path reached native engine')
u.hook_add(UC_HOOK_CODE,forbidden_stadium_call)
for snow in (0,1):
 assert call(symbols['stadium_mask'],snow)==0
 for cid in (0,122,518,566):assert call(symbols['set_environment'],cid,85,snow)==1
assert 'stage_default_hook' in symbols and 'stage_home_hook' in symbols
call(symbols['activate_context'],0)
assert call(symbols['environment_status'],2)==0
# Execute actual cached-Team accessors and runtime plan consumer. Seed each
# snapshot with wrong formation, takers, shirt numbers and old Arsenal colors.
call(symbols['configure_cached_team'],0,0x82948d0)
call(symbols['configure_cached_find'],0,0x82948ec)
call(symbols['configure_kit_resource'],0,0x82446d8)
call(symbols['activate_context'],518)
root=0x33210000;sideptr=0x33212000;output=0x33213000
for tid,definition in cfg['classic_teams'].items():
 call(symbols['activate_context'],definition.get('competition',518))
 for side in [0,1]:
  cp=root+0x620+side*0x5d8;u.mem_write(cp,b'\x55'*0x5d8);w(cp,'I',int(tid)<<14);w(cp+0x40c,'I',11<<9);u.mem_write(cp+0x110,b'\0'*(40*16));w(sideptr,'I',side)
  assert call(symbols['cached_team_hook'],root,sideptr)==cp
  # This is the same field consumed by the original stadium getter73f34b4.
  assert (struct.unpack('<I',u.mem_read(cp+0x3f4,4))[0]>>17)&255==cfg['match_environment']['home_stadiums'][tid]
  before=bytes(u.mem_read(cp,0x5d8));count=call(symbols['cached_status'])
  assert call(symbols['cached_team_hook'],root,sideptr)==cp and call(symbols['cached_status'])==count
  for block in [0x478,0x4d8]:
   for variant in [0,1]:
    # Original82bfb2c emits member index, coordinates and assigned role
    # for all11 runtime formation slots, not merely a raw memory assertion.
    call(0x82bfb2c,output,11,cp+block,variant,cp+0x538)
    for i,slot in enumerate(definition['slots'][:11]):
     member,xy,role=struct.unpack('<IH2xI',bytes(u.mem_read(output+i*16,12)))
     assert member==i and role==definition['formation'][i][0],(tid,i,member,role,[call(symbols['native_status'],j) for j in range(22)],list(u.mem_read(cp+0x478,11)),call(symbols['cached_status']),call(symbols['environment_status'],0))
     call(0x68fc714,cp,member,0x33200000)
     assert u.reg_read(UC_ARM64_REG_X1)==slot['player_id'] and struct.unpack('<H',u.mem_read(0x33200000,2))[0]==slot['shirt']
  assert bytes(u.mem_read(cp+0x56f,80))==bytes(u.mem_read(teams[definition['visual_team']]+0x56f,80))
  assert list(u.mem_read(cp+0x560,6))==definition['set_piece_taker'] and u.mem_read(cp+0x569,1)[0]==definition['responsibilities']['captain']
  assert call(symbols['kit_resource_hook'],int(tid))==cfg['kit_aliases'][str(tid)]
  # Simulate the game replacing its cached Team while keeping the same pointer.
  u.mem_write(cp+0x538,b'\xff'*40);assert call(symbols['cached_team_hook'],root,sideptr)==cp
  assert list(u.mem_read(cp+0x538,11))==list(range(11))
# Every configured club (including national teams) gets a permitted home stadium.
for tid,stadium in cfg['match_environment']['home_stadiums'].items():
 cp=root+0x620;u.mem_write(cp,b'\x55'*0x5d8);w(cp,'I',int(tid)<<14);w(cp+0x40c,'I',11<<9);u.mem_write(cp+0x110,b'\0'*(40*16));w(sideptr,'I',0)
 call(symbols['cached_team_hook'],root,sideptr)
 assert (struct.unpack('<I',u.mem_read(cp+0x3f4,4))[0]>>17)&255==stadium
assert call(symbols['environment_status'],2)==0
call(symbols['activate_context'],0)
# Exercise the exact four-kit resource selection in the new library.
def kit_fallback(uc,addr,size,data):
 if addr==0x33000080:
  uc.reg_write(UC_ARM64_REG_X0,100000+uc.reg_read(UC_ARM64_REG_W0))
  uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,kit_fallback);call(symbols['configure_kit_resource'],0,0x33000080)
for cid in [0,125,518,473]:
 call(symbols['activate_context'],cid)
 for team in [351,352,242,245]:
  for key in [team,team<<14,(team<<14)+1]:assert call(symbols['kit_resource_hook'],key)==team
  assert call(symbols['kit_resource_hook'],(team<<14)+2)==100000+(team<<14)+2
 for key in [0,101,350,353,243,246,65535]:assert call(symbols['kit_resource_hook'],key)==100000+key
 if cid==518:assert call(symbols['kit_resource_hook'],5317)==127
report=dict(status='ARM64_COMPONENT_VALIDATED_DEVICE_UNTESTED',device_tested=False,synthetic_database=True,native_roster_counts={k:len(v) for k,v in cfg['native_rosters'].items()},classic_profiles=len(cfg['classic_profiles']),checks=['73 initialized backing lookup modeled; full64 identity and actual native record accessors exercised','all28 roster preflights, shirt getters and exact typed player entries','all22 classic formations4 variants through original role/coordinate getters; valid lineup order','all classic NPCs configured neutral OVR; all13 position proficiencies scoped to Y17/Y08; no Marseille/Chop Turn; configured captain and six taker slots','classic targets stable through repeated lookups, no progressive stat reduction','base, exact cards and all220 relative policies; global power boost/conditional Dipping Shot; original147 getter/setter','adjacent native bytes preserved including short-name +4e boundary','all22 stale cached Team snapshots refreshed on both fixture sides; original82bfb2c runtime slot consumer verifies full64 identity, role and shirt; six takers/captain verified','cached kit blocks and actual3D resource team-ID resolver use exact donors','all86 club home stadium fields use allowed IDs; no100 writes; native UI resource fallback remains unverified','player hook via real atomic detour/trampoline including full64 Messi','missing player blocks roster writes','OVR scope518/566/0 changes match Python and restore baseline, repeated reads idempotent','gateway stage setters use atomics only; game-called stage selector hooks never return100 in active context; explicit this argument preserved outside My League'])
report['checks'].append('four requested kits: team keys and both uniform slots in contexts0/125/518; third slots and unrelated teams retain fallback; Y17 donors retained')
report['backing_DB_lookup_modeled']=True

# Real 73 canonical147 accessors, exact custom IDs and preservation checks.
call(symbols['activate_context'],0)
for team,donor in [(351,109),(352,100),(242,109),(245,108)]:
 p=teams[team];before=bytes(u.mem_read(p,0x700));call(symbols['team_hook'],db,team<<14)
 after=bytes(u.mem_read(p,0x700));assert after[0x56f:0x5bf]==bytes(u.mem_read(teams[donor]+0x56f,80))
 assert after[:0x56f]==before[:0x56f] and after[0x5bf:]==before[0x5bf:]
 cp=root+0x620;u.mem_write(cp,before[:0x5d8]);w(sideptr,'I',0)
 call(symbols['cached_team_hook'],root,sideptr)
 assert bytes(u.mem_read(cp+0x56f,80))==after[0x56f:0x5bf]
editor=json.loads(Path('/workspace/ronaldo-work/73-ui6/payload/work/tools/myleague_editor.json').read_text())
assert call(symbols['editor_status'],0)==0
newrows=[]
for cid in [89136418985303,89136418985302]:
 row=next(r for r in editor['players'] if r['id']==str(cid) and r['competition']==0)
 n=call(symbols['editor_add_player'],cid,0,3);assert n
 for ix,v in row['parameters'].items():assert call(symbols['editor_parameter'],n,int(ix),v)==1
 for ix,v in [(43,1),(47,193),(48,91),(60,90)]:assert call(symbols['editor_parameter'],n,ix,v)==1
 for ix,v in [(43,2),(47,139),(48,131),(60,128),(49,5)]:assert call(symbols['editor_parameter'],n,ix,v)==0
 for typ,mode in [(4,2),(5,1),(6,0),(7,2)]:assert call(symbols['editor_accessory'],n,typ,mode)==1
 assert call(symbols['editor_accessory'],n,3,2)==0
 newrows.append((cid,row))
assert call(symbols['editor_commit'])==1
for cid,row in newrows:
 p=players[cid];before=[get(p,i) for i in range(147)]
 call(symbols['player_hook'],db,0,cid)
 after=[get(p,i) for i in range(147)]
 expected=dict(row['parameters']);expected.update({'43':1,'47':193,'48':91,'60':90})
 for ix,v in expected.items():assert after[int(ix)]==v,(cid,ix,v,after[int(ix)])
 # Global power/conditional Dipping Shot rules may also run, as in the retained full build.
 for ix in range(147):
  if str(ix)not in expected and ix not in [37,103]:assert after[ix]==before[ix],(cid,ix)
 call(symbols['player_hook'],db,0,cid);assert after==[get(p,i) for i in range(147)]
# Populate the accessory vector through the ORIGINAL native append routine.
config=0x33230000;vector=0x33231000;u.mem_write(config,b'\0'*0x230);w(config+0x210,'QQQ',vector,vector,vector+18*12)
for typ in range(18):call(0x68cff80,config,typ,0xaabbccdd,1)
before=bytes(u.mem_read(vector,18*12));call(symbols['editor_apply_accessories'],config,89136418985303);after=bytes(u.mem_read(vector,18*12))
expected=bytearray(before);expected[5*12+8]=0;struct.pack_into('<I',expected,4*12+4,0xffffffff)
assert after==expected
# Unrelated card IDs, malformed vectors and goalkeeper entries stay unchanged.
u.mem_write(vector,before);call(symbols['editor_apply_accessories'],config,123);assert bytes(u.mem_read(vector,18*12))==before
w(config+0x218,'Q',vector+17*12);call(symbols['editor_apply_accessories'],config,89136418985303);assert bytes(u.mem_read(vector,18*12))==before

for cid in [88044950524330,89135066911146,89136418985303,89136418985302,88033139394625,106781745353130,89136418985303+(1<<32),123]:
 w(config+0x218,'Q',vector+18*12);u.mem_write(vector,before);call(symbols['editor_apply_accessories'],config,cid)
 actual=bytes(u.mem_read(vector,18*12));wanted=bytearray(before)
 if cid in [88044950524330,89135066911146,89136418985303,89136418985302]:
  struct.pack_into('<I',wanted,4*12+4,0xffffffff);wanted[4*12+8]=1;wanted[5*12+8]=0
 assert actual==wanted,(cid,'wrist scope')
# Body load/cross-library paths exercised in test_regressions.py.
# Original FString constructors remain native tailcalls. Only donor IDs change;
# hidden result pointer X8 must be preserved for the caller's FString.
alias_stub=0x33000160
u.mem_write(alias_stub,bytes.fromhex('c0035fd6'))
call(symbols['configure_emblem'],0,alias_stub);call(symbols['configure_kit'],0,alias_stub)
for name in ['emblem_hook','kit_hook']:
 for tid in cfg['leagues']['473']['teams']+[1958,4965,100,109,42]:
  u.reg_write(UC_ARM64_REG_X8,0x33270000);expected=cfg['kit_aliases'if name=='kit_hook'else'visual_aliases'].get(str(tid),tid)
  assert call(symbols[name],tid)==expected,(name,tid)
  assert u.reg_read(UC_ARM64_REG_X8)==0x33270000
# Swiss menu vector shrinks12 ->10, preserves packed IDs and removes exactly two.
root_menu=0x332a0000;regions=root_menu+0x1000;leagues=root_menu+0x2000;words=root_menu+0x3000
u.mem_write(root_menu,b'\0'*0x120);w(root_menu,'Q',0x98c3ff0);w(root_menu+0x90,'3Q',regions,regions+32,regions+32)
u.mem_write(regions,b'\0'*32);w(regions+8,'3Q',leagues,leagues+40,leagues+40);u.mem_write(leagues,b'\0'*40)
old=cfg['leagues']['473']['original_teams'];new=cfg['leagues']['473']['teams'];w(leagues+16,'3Q',words,words+len(old)*4,words+len(old)*4);w(words,str(len(old))+'I',*[t<<14 for t in old])
assert call(symbols['fix'],root_menu,0)==1
assert struct.unpack('<Q',u.mem_read(leagues+24,8))[0]==words+len(new)*4
assert list(struct.unpack('<10I',u.mem_read(words,40)))==[t<<14 for t in new]
assert call(symbols['fix'],root_menu,0)==2
# Both ordinary and encoded kit lookups route exactly to the original club kit.
call(symbols['activate_context'],473)
for tid in new:
 donor=cfg['kit_aliases'][str(tid)]
 for key in [tid]+[(kind<<28)|(tid<<14)|slot for kind in range(6)for slot in range(2)]:assert call(symbols['kit_resource_hook'],key)==donor,(tid,key)
# Y08's primary/proficiency edits and OVR are restored on leaving its context.
for tid in new:
 for pid in cfg['native_rosters'][str(tid)]:
  pp=players[pid];call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid);outside=[get(pp,i)for i in range(147)];assert outside[:14]==source_position_fields[pid]
  for _ in range(2):
   call(symbols['activate_context'],473);call(symbols['player_hook'],db,0,pid);inside=[get(pp,i)for i in range(147)];profile=cfg['classic_profiles'][str(pid)];assert inside[0]==profile['formation_role']and native_overall.rating(inside,inside[0])==profile['target_ovr']
   call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid);assert[get(pp,i)for i in range(147)]==outside
report['checks']+=['Y08 emblem/kit donor tailcalls preserve FString hidden pointer; Swiss native menu12-to10 membership; source-packed IDs retained; second call idempotent','Y08 exact card IDs, native formation role, shirt, takers, captain, cached sides, kit resource aliases and92–100OVR','Y08 primary/proficiency edits restore outside473; repeated context changes preserve original card data']
report['checks']+=['exact four-card left-white-wrist policy; right tape disabled; Suarez and other cards/gear unchanged','Body/soft-path/common-loader regression is recorded separately; no full-model ID or LOD substitution']
report['checks']+=['native accessory vector built by original68cff80: per-card wrist/ankle/outfield-glove modes preserve color, adjacent entries and GK gear; invalid vectors untouched','four licensed kit visual blocks copied in direct and cached lookups outside My League; adjacent bytes untouched','both custom64 Ronaldo IDs: actual native skill flags and body fields43/47/48/60 read back through original engine accessors; invalid fields rejected; repeated lookups stable']
# Ownership can change after the native profiles are already cached.
protected=sorted([spare[0],int(next(iter(cfg['classic_profiles'])))])
for pid in protected:
 call(symbols['activate_context'],0);call(symbols['player_hook'],db,0,pid)
base={pid:[get(players[pid],i)for i in range(147)]for pid in protected}
owned_ids=0x332f0000;w(owned_ids,'2Q',*protected);assert call(symbols['configure_owned_cards'],owned_ids,2)==1
for cid in [518,473,518,0,473]:
 call(symbols['activate_context'],cid)
 for pid in protected:
  call(symbols['player_hook'],db,0,pid);p=[get(players[pid],i)for i in range(147)]
  assert p[14:41]==base[pid][14:41],(pid,cid,p[14:41],base[pid][14:41])
assert call(symbols['configure_owned_cards'],0,0)==1
pid=protected[1]if str(protected[1])in cfg['classic_profiles']else protected[0];profile=cfg['classic_profiles'][str(pid)];call(symbols['activate_context'],profile['competition']);call(symbols['player_hook'],db,0,pid);assert native_overall.rating([get(players[pid],i)for i in range(147)],get(players[pid],0))==profile['target_ovr']
report['checks'].append('Owned full64 IDs remain at original attributes in both Y17/Y08, even after cached NPC scaling; repeated contexts restore; removing protection retains NPC target')
Path('/workspace/ronaldo-work/73-ui6/native-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
