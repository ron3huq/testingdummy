"""Native scopes/fallbacks plus native material lifecycle and exact test IDs.
The original engine body remains modeled at boundaries; no GPU claims.
"""
from pathlib import Path
exec((Path(__file__).resolve().parent/'native_harness.py').read_text())

# Exact generic-head fallback for base Yan; every body mesh and other card passes.
for base_path in ["SkeletalMesh'/Game/Assets/character/Body/SK_Base_Face.SK_Base_Face'","/Game/Assets/character/Body/SK_Base_Face.SK_Base_Face"]:
 full_mesh_path_override=base_path
 for card,enabled,wanted in [(176104,1,True),(84062184,1,True),(176104,0,False),(176104+(1<<32),1,False),(target,1,False)]:
  es=request(card,'176104',enabled)
  assert any(e[0]=='mesh'and 'SK_NWDY' in e[1]for e in es)==wanted
  assert string(actor+0x448)=='176104'
  checks.append('v21_Yan_generic_head_only_'+str((card,enabled,base_path)))
full_mesh_path_override='/Game/Assets/character/Body/SK_002d01.SK_002d01'
es=request(176104,'176104');assert any(e[0]=='mesh'and e[1]==full_mesh_path_override for e in es)
checks.append('v21_Yan_never_replaces_body_mesh')
full_mesh_path_override=None

black=[88044950524330,106734785925546,105765448873424,105643042189511]
for card,profile in [(105807861630781,'NW01'),(176104,'NWDY'),(84062184,'NWDY')]:
    for face_id in ['4522','176104','99123ep00v0313']:
        es=request(card,face_id)
        assert any(e[0]=='mesh' and f'SK_{profile}ep00v0313_Face' in e[1]for e in es)
        assert string(actor+0x448)==face_id
        checks.append(f'v21_exact_{card}_{face_id}')
    for collision in [card-1,card+1,card+(1<<32),card&0xffffffff]:
        # Base176104 is already32-bit; its identical low32 form is the exact ID.
        if collision==card:continue
        es=request(collision,'4522')
        assert not any(e[0]=='mesh'and f'SK_{profile}'in e[1]for e in es)
        checks.append(f'v21_collision_passthrough_{collision}')

for card in black+[105807861630781]:
    request(card,'4522ep00v0313')
    guard_before={ix:call(syms['noodle_stat'],ix)for ix in [28,37,38,63,64,81,82,83]}
    snapshot=bytes(u.mem_read(actor,0x2300));before=call(syms['noodle_stat'],92)
    at=len(events);call(bake,actor)
    assert ('bake',actor)in events[at:]
    assert bytes(u.mem_read(actor,0x2300))==snapshot
    assert call(syms['noodle_stat'],92)==before+1
    # No static material rebind, no CSMMask write, no hidden-common-body search.
    for ix,value in guard_before.items():assert call(syms['noodle_stat'],ix)==value
    u.mem_write(closure,struct.pack('<Q',actor));u.mem_write(result,struct.pack('<Q',0x30080000))
    before=call(syms['noodle_stat'],93);call(done,closure,result,detail)
    assert call(syms['noodle_stat'],93)==before+1
    checks.append(f'v21_native_bake_no_post_material_or_shadow_mutation_{card}')

call(syms['noodle_enable'],1)
path="Texture2D'/Game/Assets/character/Uniform/LowTextures/T_u0351p1_FontName_D.T_u0351p1_FontName_D'"
putstr(chars,path);before=call(syms['noodle_stat'],94);call(printf,holder,chars,len(path))
assert call(syms['noodle_stat'],94)==before+1
observed=''.join(chr(call(syms['noodle_font_char'],i))for i in range(192)).split('\0',1)[0]
assert observed==path and events[-1][1]==path
checks.append('v21_font_resource_observed_without_rewrite')
cfg=0x302a2000;fstring(cfg,'T_u0351p1_FontName_D',0x302a2100)
before=bytes(u.mem_read(cfg,80))+bytes(u.mem_read(0x302a2100,80));value=call(0x39c0420,actor,cfg)
assert value==123 and bytes(u.mem_read(cfg,80))+bytes(u.mem_read(0x302a2100,80))==before
checks.append('v21_native_font_key_return_config_dimensions_untouched')


namecases=[(88045755960841, 'Nguyen Xuan Son', 'XUAN SON'), (88038776539586, 'Nguyen Dinh Bac', 'DINH BAC'), (105643042189511, 'Nguyen Hoang Duc', 'HOANG DUC'), (106728863696709, 'Do Hoang Hen', 'HOANG HEN'), (105848932271764, 'Cao Pendant Quang Vinh', 'QUANG VINH'), (105874433662542, 'Nguyen Tai Loc', 'TAI LOC'), (88033139360669, 'IShowSpeed', 'ISHOWSPEED'), (105765448873424, 'Ronaldo Jr', 'RONALDO JR'),(106778792700170,'Mesut Ozil','OZIL')]
record=0x30290000;vtable=0x302c0000;resource=0x302d0000;u.mem_write(actor,struct.pack('<Q',vtable));u.mem_write(vtable+0x838,struct.pack('<Q',0x302b0000));u.mem_write(0x302a0000,b'Original\0');u.mem_write(actor+0x1a70,b'\0'*8);u.mem_write(actor+0x228,b'\0'*8);u.mem_write(actor+0x1aa0,b'\0'*8);u.mem_write(actor+0x1ab8,b'\0'*8)
track_names=True
for card,display,shirt in namecases:
 for key in [card,card+(1<<32),card&0xffffffff]:
  for enabled in [0,1]:
   for kind in [0,1]:
    call(syms['noodle_enable'],enabled);u.mem_write(record+0x38,struct.pack('<QQ',kind,key));start=len(events);ptr=call(0x82a1e48,record)
    actual=bytes(u.mem_read(ptr,64)).split(b'\0',1)[0].decode();assert actual==(display if enabled and key==card and kind==0 else 'Original')
    checks.append('native_record_name_'+str(card)+'_'+str(key)+'_'+str(enabled)+'_'+str(kind))
 for enabled in [0,1]:
  for actual_id in [card,card+(1<<32),88044950524330]:
   call(syms['noodle_enable'],enabled);u.mem_write(actor+0x10b0,struct.pack('<Q',actual_id));src=0x302a1000;u.mem_write(src,b'ADRIANO\0');start=len(events);call(0x39bc570,actor,src)
   assert events[start:]==[('native_shirt_char',actor,shirt if enabled and actual_id==card else 'ADRIANO')]
   start=len(events);call(0x39bc5ac,actor,0x302a3000)
   assert events[start:]==([('native_shirt_char',actor,shirt)] if enabled and actual_id==card else [('native_shirt_string',actor)])
   cfg=0x302a2000;fstring(cfg,'T_Real_FontAtlas_001',0x302a2100);before_cfg=bytes(u.mem_read(cfg,80));before_chars=bytes(u.mem_read(0x302a2100,80));start=len(events);call(0x39c0420,actor,cfg)
   assert events[start:]==[('shirt_key_text','T_Real_FontAtlas_001')]
   assert bytes(u.mem_read(cfg,80))==before_cfg and bytes(u.mem_read(0x302a2100,80))==before_chars
   checks.append('native_char_string_and_glyph_config_before_cache_'+str(card)+'_'+str(actual_id)+'_'+str(enabled))
 # Full-ID record fields are updated before lookup returns, identity/stats untouched.
 for enabled in [0,1]:
  for record_id in [card,card+(1<<32)]:
   original=bytearray([0x55]*0x1d0);struct.pack_into('<QQ',original,0x38,0,record_id)
   for off in [0x4c,0x89,0xc6,0x103]:original[off:off+61]=b'Original\0'+b'\0'*52
   u.mem_write(record,bytes(original));call(syms['noodle_enable'],enabled);call(0x823be04,0,0,card);actual=bytes(u.mem_read(record,0x1d0));expected=bytearray(original)
   if enabled and record_id==card:
    for off in [0x4c,0x89,0xc6,0x103]:expected[off:off+61]=display.encode()+b'\0'*(61-len(display))
    struct.pack_into('<H',expected,0x198,210 if card==106778792700170 else (228 if card in [88033139360669,105765448873424] else 38))
    if card not in [88033139360669,105765448873424,106778792700170]:struct.pack_into('<I',expected,0x140,0xffffffff)
   assert actual==expected
   checks.append('four_native_name_fields_only_exact64_'+str(card)+'_'+str(record_id)+'_'+str(enabled))
u.mem_write(actor+0x18d0,b'\0'*8)
# Reject a non-string buffer and a different typed record family, without any writes.
call(syms['noodle_enable'],1);card=namecases[0][0];bad=bytearray([0x41]*0x1d0);struct.pack_into('<QQ',bad,0x38,0,card);u.mem_write(record,bytes(bad));call(0x823be04,0,0,card);assert bytes(u.mem_read(record,0x1d0))==bytes(bad)
checks.append('record_name_schema_no_terminator_rejects_before_any_write')
struct.pack_into('<QQ',bad,0x38,1,card);u.mem_write(record,bytes(bad));call(0x823be04,0,1,card);assert bytes(u.mem_read(record,0x1d0))==bytes(bad)
checks.append('record_name_other_typed_family_untouched')
# Native wire source country checks.
# runtime record layouts are different, verified by the actual importer calls.
raw=Path('/workspace/ronaldo-work/v17-research/tables/Player-decoded.bin').read_bytes()
rawchecks=[]
for off in range(0,len(raw),400):
 row=raw[off:off+400];pid=struct.unpack_from('<Q',row,8)[0];name=row[332:].split(b'\0',1)[0].decode('utf8','replace')
 if pid in [4522,7511,110718,47287] or name in ['Nguyen Quang Hai','Nguyen Thanh Binh']:
  u.mem_write(0x303f0000,row);code=call(0x8257850,0x303f0000,0)
  expected={'Cristiano Ronaldo':228,'Lionel Messi':144,'Kylian Mbappé':208,'Harry Kane':204,'Nguyen Quang Hai':38,'Nguyen Thanh Binh':38}.get(name)
  if expected is None:continue
  assert code==expected,(pid,name,code,expected)
  rawchecks.append({'id':pid,'name':name,'wire_country':code});checks.append('actual_country_wire_getter_'+str(pid))
assert len(rawchecks)>=6
# Original font glyph table: uppercase full shirt names have visible glyphs;
# font resource, font family, size and render config remain native.
for card,display,shirt in namecases:
 for char in shirt.replace(' ',''):
  pointers=[0x303f1000+i*8 for i in range(5)]
  for ptr in pointers:u.mem_write(ptr,b'\0'*8)
  call(0x39259c8,*pointers,ord(char))
  width=struct.unpack('<f',u.mem_read(pointers[3],4))[0];height=struct.unpack('<f',u.mem_read(pointers[4],4))[0]
  assert width>0 and height>0,(shirt,char,width,height)
 checks.append('original_glyph_table_all_shirt_letters_visible_'+str(card))

report={'status':'V21_SCOPE_FALLBACK_NATIVE_HEAD_LIFECYCLE_PASS','checks':checks,'four_original_failing_cards':black,'additional_R2017_test_card':105807861630781,'exact_base_Yan_Diomande_ids':[176104,84062184],'no_head_material_or_shadow_override_for_five_tested_cards':True,'original_engine_bodies_modeled':True,'black_face_renderer_verified':False,'phone_tested':False}
(r.parent/'native-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],len(checks),'checks')
