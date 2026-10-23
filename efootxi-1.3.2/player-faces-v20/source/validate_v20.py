"""All v19 regressions plus exact-card Ozil, positional proficiency and v18
editor offensive overrides; actual ARM64 detours, engine API boundaries modeled.
"""
exec((__import__('pathlib').Path(__file__).parent/'validate_v19.py').read_text())
# Independent source-corpus evidence for native proficiency parameter order.
# It differs from the primary-role enum! Every source player's own position
# must be level2 at its correct parameter; GK at13 and CF at1 are sentinels.
catalog=json.loads((r.parents[1]/'editor-v16/source/catalog.json').read_text());role_parameter=[13,10,11,12,6,7,8,9,5,3,4,2,1];corpus=[]
for role,parameter in enumerate(role_parameter):
 values=[p[3][parameter]for p in catalog['players']if p[3]and p[3][0]==role];assert values and set(values)=={2};corpus.append({'role':catalog['roles'][role],'parameter':parameter,'rows':len(values),'all_primary_mastery':2})
(r.parent/'position-parameter-evidence.json').write_text(json.dumps(corpus,indent=2));checks.append('v20_independent_full_source_corpus_position_parameter_mapping')
# Fourteen card redirects, full64 ID collision rejects, original FaceID invariant.
for face_id in ['79120','79120ep00v0313','4522ep00v0313']:
 es=request(106778792700170,face_id);assert any(e[0]=='mesh' and 'SK_NWOZep00v0313_Face' in e[1] for e in es);assert string(actor+0x448)==face_id;redirected=''.join(chr(call(syms['noodle_redirect_char'],i))for i in range(160)).split('\0')[0];assert 'SK_NWOZep00v0313_Face' in redirected;checks.append('v20_ozil_foreign_'+face_id)
es=request(106778792700170+(1<<32),'79120');assert all('NWOZ' not in str(e) for e in es);checks.append('v20_ozil_high32_collision_passthrough')
# Real hook invokes typed native parameter API only after decoded record ID match.
rec=0x30290000;values={i:40+(i%45) for i in range(147)};values[0]=12;values[47]=187;updates=[]
def parameters_boundary(uc,addr,size,data):
 if addr not in [0x82a84d4,0x82a907c]:return
 x0=uc.reg_read(UC_ARM64_REG_X0);ix=uc.reg_read(UC_ARM64_REG_X1);x2=uc.reg_read(UC_ARM64_REG_X2);assert x0==rec
 if addr==0x82a84d4:uc.mem_write(x2,struct.pack('<I',values[ix]))
 else:updates.append((ix,x2));values[ix]=x2
 uc.reg_write(UC_ARM64_REG_X0,1);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
u.hook_add(UC_HOOK_CODE,parameters_boundary)
for pid,kind,stored,enabled in [(target,0,target,1),(89135066911146,0,89135066911146,1),(106726716084650,0,106726716084650,1),(106734785925546,0,106734785925546,1),(target,0,target+1,1),(target,1,target,1),(target,0,target,0),(target+(1<<32),0,target+(1<<32),1)]:
 call(syms['noodle_enable'],enabled);values={i:40+(i%45) for i in range(147)};values[0]=12;values[47]=187;before=dict(values);updates.clear();u.mem_write(rec+0x38,struct.pack('<QQ',kind,stored));call(syms['noodle_record_lookup_hook'],0,0,pid)
 wanted=pid in [target,89135066911146,106726716084650] and kind==0 and stored==pid and enabled
 if wanted:
  assert values[0]==(9 if pid==target else 10)
  for ix in range(1,14):assert values[ix]==(2 if (ix==3 if pid==target else ix in [9,4]) else 0)
  for ix in range(14,147):assert values[ix]==before[ix]
 else:assert not updates and values==before
 checks.append('v20_exact_position_'+str((pid,kind,stored,enabled)))
call(syms['noodle_enable'],1)
# Ozil names must not enter the six-card Vietnam-only affiliation branch.
u.mem_write(rec+0x38,struct.pack('<QQ',0,106778792700170));u.mem_write(rec+0x4c,b'\0'*244);u.mem_write(rec+0x140,struct.pack('<I',77));u.mem_write(rec+0x198,struct.pack('<H',99));call(syms['noodle_record_lookup_hook'],0,0,106778792700170)
assert bytes(u.mem_read(rec+0x4c,61)).split(b'\0')[0]==b'Mesut Ozil';assert struct.unpack('<I',u.mem_read(rec+0x140,4))[0]==77 and struct.unpack('<H',u.mem_read(rec+0x198,2))[0]==210;checks.append('v20_ozil_rename_not_Vietnam')
# The existing supported v18 editor layer applies these AFTER competition rating.
import importlib.util,copy
spec=importlib.util.spec_from_file_location('v20_editor',r/'myleague_editor_runtime.py');overlay=importlib.util.module_from_spec(spec);spec.loader.exec_module(overlay)
orig=copy.deepcopy(overlay.DEFAULT);orig['players']=[{'id':str(target),'competition':122,'sleeve':'none','parameters':{'15':61}},{'id':'999','competition':0,'sleeve':'none','parameters':{'20':55}}];data=overlay.requested_long_sleeves(orig);assert orig['players'][0]['parameters']=={'15':61}
fields={14,17,18,19,20,21,22,23,27,28,34,35,36,37,38,39,40};targets={str(x)for x in [target,89135066911146,106726716084650,106734785925546]}
for row in data['players']:
 if row['id']in targets:
  assert fields<={int(k)for k in row['parameters']}
  assert all(92<=row['parameters'][str(k)]<=96 for k in fields)
  assert set(map(int,row['parameters']))<=fields|({15}if row['competition']==122 else set())
 else:assert row.get('parameters',{})==({'20':55}if row['id']=='999'else {})
assert next(x for x in data['players']if x['id']==str(target)and x['competition']==122)['parameters']['15']==61
assert {x['id']for x in data['players']if x['sleeve']=='long'}>={'88044950524330','89135066911146','106781745353130','106726716084650','17592722922839'};checks.append('v20_editor_four_only_17_offensive_fields_92_to_96_defence_untouched')
# Alternate card builder forwards all eight registers and BOTH stack arguments.
ext_stub=0x33018040;u.mem_write(ext_stub,struct.pack('<I',0xd65f03c0));ext_seen=[]
def ext_boundary(uc,addr,size,data):
 if addr==ext_stub:
  regs=tuple(uc.reg_read(x)for x in [UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3,UC_ARM64_REG_X4,UC_ARM64_REG_X5,UC_ARM64_REG_X6,UC_ARM64_REG_X7]);stack=struct.unpack('<QQ',uc.mem_read(uc.reg_read(UC_ARM64_REG_SP),16));ext_seen.append(regs+stack)
u.hook_add(UC_HOOK_CODE,ext_boundary);call(syms['configure_card_data_ext'],0,ext_stub)
for pid in vn+[speed,106778792700170,target,vn[0]+(1<<32)]:
 for enabled in [0,1]:
  raw=bytearray(rng.randbytes(0x140));struct.pack_into('<Q',raw,0x20,pid);u.mem_write(ui-16,b'\xa5'*16+raw+b'\x5a'*16);want=bytearray(raw);args=(ui,0x30600000,0x30600020,3,4,5,6,7,0x1122334455667788,0x30600080);call(syms['noodle_enable'],enabled);call(syms['noodle_card_data_ext_hook'],*args);assert ext_seen[-1]==args
  if enabled and (pid in vn or pid==speed):
   for off in [0x28,0x2c,0x10c]:struct.pack_into('<I',want,off,0x3ffff if pid in vn else 18961)
   want[0x30]=0;struct.pack_into('<II',want,0x34,0,38 if pid in vn else 228)
  if enabled and pid==106778792700170:struct.pack_into('<I',want,0x38,210)
  assert bytes(u.mem_read(ui-16,0x160))==b'\xa5'*16+want+b'\x5a'*16
  checks.append('v20_extended_builder_all10_args_exact_UI_'+str((pid,enabled)))
# Germany comes from the actual native getter and the localized country table.
country=__import__('pathlib').Path('/workspace/ronaldo-work/v17-research/tables/Country-decoded.bin').read_bytes()
germany=next(country[off:off+1488]for off in range(0,len(country),1488)if (int.from_bytes(country[off:off+8],'little')>>10)&511==210);assert germany[148:218].split(b'\0')[0]==b'Alemania'and int.from_bytes(germany[:8],'little')&1023==23
player_source=__import__('pathlib').Path('/workspace/ronaldo-work/v17-research/tables/Player-decoded.bin').read_bytes();neuer=next(player_source[off:off+400]for off in range(0,len(player_source),400)if int.from_bytes(player_source[off+8:off+16],'little')==33185);u.mem_write(0x303f0000,neuer);assert call(0x8257850,0x303f0000,0)==210;checks.append('v20_native_Germany_country_getter_and_country_table')
(r.parent/'ozil-country-evidence.json').write_text(json.dumps({'country_internal':210,'flag_resource':23,'country_table_name':'Alemania','native_getter_executed_on_Neuer_source':True,'club_and_league_not_changed_for_Ozil':True},indent=2))
# API JSON mirrors the same policy, rather than only changing native match data.
overlay._config=copy.deepcopy(overlay.DEFAULT)
for pid in targets:
 source={'gameplayer_id':{'id':int(pid)},'parameters':[55]*147};projected=overlay.project(source,122);assert source['parameters']==[55]*147
 for ix in fields:assert 92<=projected['parameters'][ix]<=96
 for ix in [15,16,24,25,26,29,30,31,32,47,48]:assert projected['parameters'][ix]==55
 if pid!='106734785925546':assert projected['parameters'][0]==(9 if pid==str(target)else 10)
 checks.append('v20_API_parameter_mirror_'+pid)
report.update(status='V20_NATIVE_SCOPE_POSITIONS_OZIL_EDITOR_PASS',checks=checks,full_card_ids=14,offensive_stats_editor_after_native_rating=True,position_primary_and_proficiency_only_three_exact_ids=True,black_face_renderer_verified=False,phone_tested=False);(r/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
