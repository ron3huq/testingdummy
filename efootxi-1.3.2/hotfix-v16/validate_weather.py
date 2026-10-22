from pathlib import Path
import sys,json,struct,collections
from elftools.elf.elffile import ELFFile
from unicorn import *
from unicorn.arm64_const import *
r=Path(__file__).parent;sys.path[:0]=[str(r),str(r.parent/'android/user-gateway/work/tools')];import select_team_runtime as runtime
raw=(r.parent/'android/official-apk/lib/arm64-v8a/libUE4.so').read_bytes();stadiums=(r.parent/'kit-research/Stadium.bin').read_bytes();u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
u.mem_map(0x82b0000,0x2000);u.mem_write(0x82b0a14,raw[0x82b0a14-0x4000:0x82b0ac8-0x4000]);u.mem_map(0xcd6000,0x1000);u.mem_write(0xcd6e04,raw[0xcd6e04:0xcd6e04+13]);u.mem_map(0x30000000,0x10000);base=0x35000000
with(r/'libselect_team.so').open('rb')as f:
 e=ELFFile(f)
 for s in e.iter_segments():
  if s['p_type']=='PT_LOAD':
   lo=(base+s['p_vaddr'])&~4095;hi=(base+s['p_vaddr']+s['p_memsz']+4095)&~4095;u.mem_map(lo,hi-lo);u.mem_write(base+s['p_vaddr'],s.data())
 for s in e.iter_sections():
  if s.name.startswith('.rela'):
   for rel in s.iter_relocations():assert rel['r_info_type']==1027;u.mem_write(base+rel['r_offset'],struct.pack('<Q',base+rel['r_addend']))
 syms={s.name:base+s['st_value']for s in e.get_section_by_name('.dynsym').iter_symbols()}
def call(a,*args):
 for reg,value in zip([UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2],args):u.reg_write(reg,value)
 u.reg_write(UC_ARM64_REG_SP,0x3000f000);u.reg_write(UC_ARM64_REG_LR,0x3000ff00);u.emu_start(a,0x3000ff00,count=100000);assert u.reg_read(UC_ARM64_REG_PC)==0x3000ff00;return u.reg_read(UC_ARM64_REG_X0)
def param(i):
 call(0x82b0a14,0x30000000,i,0x30001000);return struct.unpack('<I',u.mem_read(0x30001000,4))[0]
baselines={}
for i in range(0,len(stadiums),1096):
 u.mem_write(0x30000000,stadiums[i:i+1096]);values=[param(j)for j in range(13)];baselines[values[0]]=values
entry=0x82b0a14;cave=0x0b040000;u.mem_map(cave,4096);first=bytes(u.mem_read(entry,4));u.mem_write(cave,runtime.jump(syms['stadium_parameter_hook'])+b'\0'*16+first+runtime.jump(entry+4));call(syms['configure_stadium_parameter'],0,cave+32);call(syms['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
cases=0
for cid in [0,518,122,566,128,549,125]:
 call(syms['activate_context'],cid)
 for i in range(0,len(stadiums),1096):
  record=stadiums[i:i+1096];u.mem_write(0x30000000,record);sid=param(0)
  for index,wanted in enumerate(baselines[sid]):
   if cid in [518,122,566,128,549]and sid in [1,7,30,51,52,85]and index in [9,10]:wanted=1
   assert param(index)==wanted,(cid,sid,index,param(index),wanted);cases+=1
  assert bytes(u.mem_read(0x30000000,1096))==record
 u.mem_write(0x30001000,struct.pack('<I',0xdeadbeef));assert call(entry,0x30000000,13,0x30001000)==0 and struct.unpack('<I',u.mem_read(0x30001000,4))[0]==0xdeadbeef
# Gateway requests four distinct states in every four consecutive rounds;
# reads/retries do not reroll the weather or the home stadium.
import myleague_worlds as w,myleague_realism as m
class Bridge:
 @staticmethod
 def activate_context(cid):pass
 @staticmethod
 def set_environment(cid,stadium,snow):assert stadium in [1,7,30,51,52,85]and not snow;return 1
 @staticmethod
 def ensure_native_team(t):return 1
w.NATIVE_BRIDGE=Bridge;m.ATTRS=r.parent/'android/user-gateway/outputs/reference/external-attrs';m.install();c=w.config();conditions={}
for cid in [518,122,566,128,549]:
 samples=[]
 for fixture in range(1,61):
  state=dict(realism_v1={'seed':'weather-v9-fixed-season'},team_id=c['leagues'][str(cid)]['teams'][0],competition_id=cid,season=1,fixture=fixture,played={},active=None,completed=False,cpu_level='NORMAL')
  env=w._prepare_environment(state);assert env==w._prepare_environment(state)
  if fixture<=7:assert env['season_type']=='SEASON_TYPE_SUMMER'
  if 8<=fixture<=14:assert env['season_type']=='SEASON_TYPE_WINTER'
  assert not env['snow_applied'];samples.append((env['weather'],env['time_zone']))
 assert set(samples)=={(a,b)for a in ['WEATHER_TYPE_FINE','WEATHER_TYPE_RAIN']for b in ['TIME_ZONE_TYPE_DAY','TIME_ZONE_TYPE_NIGHT']}
 conditions[str(cid)]=dict(collections.Counter('|'.join(s)for s in samples))
report=dict(status='WEATHER_CAPABILITY_AND_PROTOCOL_PASS',phone_verified=False,native_parameter_cases=cases,source_stadiums=len(baselines),source_records_unchanged=True,conditions=conditions,checks=['real ARM64 stadium getter through actual detour; only9/10 changed for six allowed IDs in five competitions','other stadiums, other parameters including snow11, context0 and Eredivisie125 preserved','invalid parameter does not write output','gateway seeded weather stable across reloads; summer1..7, winter8..14 and allfour day/night/rain/fine combinations observed','winter8..14 retained, no snow request'],limits='Rain/time/season enums and native capability acceptance validated; visual rain and resource loading require actual Android test')
(r/'weather-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
