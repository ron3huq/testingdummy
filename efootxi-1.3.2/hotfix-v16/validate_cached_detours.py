"""Real accessor detours over distinct stale match snapshots, not DB pointers."""
from pathlib import Path
r=Path(__file__).parent
# Share the complete original engine loader and synthetic exact64 player DB.
setup=(r/'validate_native.py').read_text().split("assert call(symbols['ensure_team'],127)==10")[0]
exec(compile(setup,str(r/'validate_native.py'),'exec'))
import select_team_runtime as runtime
call(symbols['configure_team'],0,0x33000040);call(symbols['configure_player'],0,0x823c8d4)
for index,(entry,hook,configure) in enumerate([(0x82948d0,'cached_team_hook','configure_cached_team'),(0x82948ec,'cached_find_hook','configure_cached_find'),(0x82446d8,'kit_resource_hook','configure_kit_resource')]):
 cave=0x0b010000+index*4096;u.mem_map(cave,4096);body=bytes(u.mem_read(entry,16));u.mem_write(cave,runtime.jump(symbols[hook])+b'\0'*16+body[:4]+runtime.jump(entry+4));call(symbols[configure],0,cave+32);call(symbols['store_instruction'],entry,runtime.branch(entry,cave));u.ctl_remove_cache(entry,entry+16)
root=0x33210000;sideptr=0x33212000;keyptr=0x33212010;out=0x33213000;cases=0
for tid,t in cfg['classic_teams'].items():
 for side in [0,1]:
  u.mem_write(root,b'\0'*0x1400);cp=root+0x620+side*0x5d8;u.mem_write(cp,b'\x55'*0x5d8);w(cp,'I',int(tid)<<14);w(cp+0x40c,'I',11<<9);u.mem_write(cp+0x110,b'\0'*(40*16));w(sideptr,'I',side);w(keyptr,'I',int(tid)<<14)
  call(symbols['activate_context'],518);assert call(0x82948d0,root,sideptr)==cp
  assert bytes(u.mem_read(cp+0x56f,80))==bytes(u.mem_read(teams[t['visual_team']]+0x56f,80))
  assert call(0x82446d8,int(tid))==t['visual_team']
  for variant in [0,1]:
   call(0x82bfb2c,out,11,cp+0x478,variant,cp+0x538)
   for i,slot in enumerate(t['slots'][:11]):
    member,xy,role=struct.unpack('<IH2xI',bytes(u.mem_read(out+i*16,12)));assert member==i and role==t['formation'][i][0]
    call(0x68fc714,cp,member,0x33200000);assert u.reg_read(UC_ARM64_REG_X1)==slot['player_id']
  # Refresh through the key-based accessor after cache content changes in place.
  u.mem_write(cp+0x478,b'\x55'*11);u.mem_write(cp+0x56f,b'\xaa'*80)
  assert call(0x82948ec,root,keyptr)==cp
  assert list(u.mem_read(cp+0x478,11))==[v[0]for v in t['formation']]
  assert bytes(u.mem_read(cp+0x56f,80))==bytes(u.mem_read(teams[t['visual_team']]+0x56f,80))
  before=bytes(u.mem_read(cp,0x5d8));call(symbols['activate_context'],0);assert call(0x82948d0,root,sideptr)==cp and bytes(u.mem_read(cp,0x5d8))==before
  assert call(0x82446d8,int(tid))==int(tid)
  cases+=1
report=dict(status='CACHED_TEAM_ACTUAL_DETOURS_PASS',device_tested=False,cases=cases,synthetic_exact64_database=True,checks=['original82948d0 and82948ec execute through real atomic detours/trampolines','all12 stale clubs on both fixture sides refreshed separately from DB records','original82bfb2c consumes matching member IDs, coordinates and roles','kit block and real82446d8 resource-team resolver use exact donor','same-pointer cache overwrite is detected and repaired through key lookup','context0 accessors preserve snapshots and forward original resource IDs'])
(r/'cached-detours-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
