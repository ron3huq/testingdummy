"""Experimental exact-card noodle hair; engine calls occur only in native callbacks."""
import ctypes as C
import hashlib,json,os,platform,struct,threading,time
from pathlib import Path
ENGINE_SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
HOOK_SHA='959c446b61bc7931401165ae655bb3a8eaf1e9e927d854e7581ea9c95dc2bc82'
GETTER=0x39cd71c
PROLOGUE=bytes.fromhex('ff0304d1fd7b0ca9f76b00f9f6570ea9')
HERE=Path(__file__).resolve().parent
_keep=[]
_digest_cache={}
_started=False
_ready=threading.Event()
_installed_hooks={}
def owned_entry(base,entry,expected):
 item=_installed_hooks.get((base,entry))
 if item is None:return False
 target,cave,hook=item
 return C.string_at(target,4)==struct.pack('<I',branch(target,cave))and C.string_at(target+4,len(expected)-4)==expected[4:]

_advertised=0
_handle=None
_payload_ok=False
_state='STARTING'
_error=None
_SESSION=time.time_ns()
_installed_entries=[]
_installing_entry=None
def branch(source, target):
    delta = target - source
    if delta % 4 or not -(1 << 27) <= delta < (1 << 27):
        raise ValueError('branch target outside ARM64 B range')
    return 0x14000000 | ((delta >> 2) & 0x3ffffff)

def jump(target):
    return struct.pack('<IIQ', 0x58000050, 0xd61f0200, target)

def maps():
    result = []
    for line in Path('/proc/self/maps').read_text().splitlines():
        parts = line.split(maxsplit=5)
        start, end = [int(x, 16) for x in parts[0].split('-')]
        result.append((start, end, parts[1], int(parts[2], 16), parts[5] if len(parts)>5 else ''))
    return result

from mod_integrity import digest


def trampoline_hints(entries,target,page):
    # A gap can start outside B range yet END beside the target mapping.
    # Intersect the whole free interval with the ARM64 branch interval.
    candidates=set()
    for left,right in zip(entries,entries[1:]):
        lo=max((left[1]+page-1)&~(page-1),(target-(1<<27)+page-1)&~(page-1))
        hi=min((right[0]-page)&~(page-1),(target+(1<<27)-4)&~(page-1))
        if lo>hi:continue
        closest=min(max(target&~(page-1),lo),hi)
        candidates.update([closest,lo,hi])
    return sorted(candidates,key=lambda p:(abs(p-target),p))

def install(base, path, entry=GETTER, prologue=PROLOGUE, hook_name='menu_hook', configure_name='configure'):
    import hook_arena
    global _handle,_installing_entry
    _installing_entry=hex(entry)
    _handle=hook_arena.install(globals(),base,path,entry,prologue,hook_name,configure_name)
    if configure_name=='configure_bake':
        import appearance_choices,hook_arena
        appearance_choices.configure_skin_chain(_handle,base,_installed_hooks[(base,entry)][1]+hook_arena.RETURN)
    return _handle


def configuration():
    # This build is an always-enabled mod. A stale/missing enable flag from an
    # older gateway release must not silently switch the working faces off.
    return True


def bundle():
    meta=json.loads((HERE/'noodle_bundle.json').read_text())
    if meta.get('target_card_ids')!=['88044950524330','89135066911146','106781745353130','106734785925546','105765448873424','88045755960841','88038776539586','105643042189511','106728863696709','105848932271764','105874433662542','88033139360669','106726716084650','106778792700170','105807861630781','176104','84062184','89138556572074','89136418985303','106754901843130','105647605587130','105804908868664','105873896755947','88042803047215','105634720685845','105565464400480','105625593957752','89138288266704','105797392639585','106654775417922','105756321970183','105568954067359','106781476920663','105794439855675'] or meta.get('container')!='pc9298_mobile_and':
        raise ValueError('unexpected noodle bundle identity')
    if digest(HERE/'myleague_editor_runtime.py')!=meta.get('appearance_overlay_sha256'):
        raise ValueError('appearance overlay checksum mismatch')

    for name,sha in meta['appearance_files'].items():
        if digest(HERE/name)!=sha:raise ValueError('appearance native/runtime checksum mismatch: '+name)
    root=HERE.parent.parent/'livedata'
    for ext in ['pak','utoc','ucas']:
        name='pc9298_mobile_and.'+ext;path=root/name;item=meta['files'][name]
        if path.stat().st_size!=item['size'] or digest(path)!=item['sha256']:
            raise ValueError('noodle asset checksum mismatch: '+name)
    if digest(HERE/'libnoodle_hair.so')!=HOOK_SHA:
        raise ValueError('noodle native module checksum mismatch')
    return meta


def advertise(value,port):
    """Copy only CMD_LOGIN_LIVEDATA-shaped objects; preserve the rest of login."""
    global _advertised
    if not isinstance(value,dict) or not isinstance(value.get('version_file'),str) or not isinstance(value.get('livedata_list'),list):
        return value
    # Keep the mounted bundle/version stable when only visual redirection is disabled.
    try:
        meta=bundle();version=json.loads(value['version_file'])
        if not isinstance(version.get('dt880'),list) or type(version.get('version')) is not int:
            raise ValueError('unrecognized live-data version schema')
        if type(port) is not int or not 1<=port<=65535:
            raise ValueError('invalid gateway listener')
        stem='pc9298_mobile_and';rows={ext:meta['files'][stem+'.'+ext] for ext in ['pak','utoc','ucas']}
        item={'name':'pc9298','hash':rows['pak']['sha256'],'hashFileSize':rows['pak']['size'],'ucas':rows['ucas']['sha256'],'ucasFileSize':rows['ucas']['size'],'utoc':rows['utoc']['sha256'],'utocFileSize':rows['utoc']['size']}
        # Idempotent if another wrapper calls us again on the already rewritten object.
        previous=next((row for row in version['dt880'] if isinstance(row,dict) and row.get('name')=='pc9298'),None)
        if previous!=item:
            version['version']+=43
            if version['version']>=2**31:raise ValueError('live-data version overflow')
        version['dt880']=[row for row in version['dt880'] if not isinstance(row,dict) or row.get('name')!='pc9298']+[item]
        result=dict(value);result['version_file']=json.dumps(version,separators=(',',':'))
        names={stem+'.'+ext for ext in ['pak','utoc','ucas']}
        result['livedata_list']=[row for row in value['livedata_list'] if not isinstance(row,dict) or row.get('name') not in names]
        result['livedata_list'] += [{'name':stem+'.'+ext,'size':rows[ext]['size'],'url':'http://127.0.0.1:'+str(port)+'/livedata/'+stem+'.'+ext} for ext in ['pak','utoc','ucas']]
        _advertised+=1
        return result
    except Exception as exc:
        try:(HERE/'noodle-advertise-error.txt').write_text(str(exc))
        except Exception:pass
        raise RuntimeError('Mod resource verification failed: '+str(exc))from exc


def report():
    fields=['load_calls','target_calls','redirects','nonnull_callbacks','null_callbacks','skipped_face_id','busy_skips','unscoped_or_disabled_calls','restore_requests','reserved','last_target_id','reserved11','face_profile_reads','target_texture_callbacks','texture_nonnull_callbacks','texture_null_callbacks','outer_calls','texture_path_redirects','scoped_path_calls','mesh_path_redirects','face_texture_path_redirects','last_actor_type','reserved22','reserved23','face_bake_calls','private_texture_confirmed','face_texture_reapplied','face_texture_guard_skips','mesh_texture_inspections','mesh_texture_name_mismatches','mesh_texture_missing','mesh_material_invalid','mesh_texture_confirmed','body_skin_changes','body_skin_last_card','body_skin_index','mesh_texture_wrong_class','head_material_checks','head_material_rebinds','head_material_confirmed','head_material_rebind_failed','head_component_mismatch','bake_owner_missing','bake_texture_missing','bake_material_missing','xuan_son_name_changes','mesh_callback_component_matches','head_binding_state_bits','last_material_card_id','face_mid_created','face_mid_binding_checks','face_mid_failures','face_mid_source_channels_invalid','face_mid_channels_confirmed','face_mid_cache_hits','face_mid_last_card_id','shirt_name_changes','shirt_name_failures','shirt_name_last_card','native_ui_name_changes','native_ui_name_last_card','mq_shader_parent_confirmed','mq_shader_parent_mismatch','head_csm_receive_disabled','head_shadow_checks','duplicate_private_head_candidates','duplicate_private_head_mainpass_disabled','head_shadow_last_card','native_shirt_setter_intercepts','record_name_fields_updated','record_name_field_rejections','shirt_render_text_replaced','nationality_changes','nationality_last_card','nationality_internal_code','four_face_comparison_mode','vietnam_club_removed','vietnam_club_last_card','card_ui_affiliation_changes','icon_ui_affiliation_changes','card_ui_affiliation_last_card','common_head_checks','common_head_candidates','common_head_render_disabled','common_head_other_mesh','common_head_fname','common_head_restored','position_card_changes','position_last_card','position_record_rejections','extended_card_builder_calls','extended_card_last_id','standard_head_bake_calls','standard_head_mesh_callbacks','font_name_resource_paths','shirt_resource_key_calls']
    result={'session_id':_SESSION,'reported_at_unix':time.time(),'pid':os.getpid(),'runtime_path':str(Path(__file__).resolve()),'runtime_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'expected_native_sha256':HOOK_SHA,'state':_state,'installed_hook_entries':list(_installed_entries),'installing_hook_entry':_installing_entry,'version':'73-ui7.15-body-motion','device_verified':False,'face_bake_guard':True,'four_heads_use_native_material_lifecycle':True,'legacy_material_guard_card_ids':['106726716084650'],'error':_error,'enabled':configuration(),'payload_verified':_payload_ok,'manifest_advertised':_advertised,'target_card_ids':['88044950524330','89135066911146','106781745353130','106734785925546','105765448873424','88045755960841','88038776539586','105643042189511','106728863696709','105848932271764','105874433662542','88033139360669','106726716084650','106778792700170','105807861630781','176104','84062184','89138556572074','89136418985303','106754901843130','105647605587130','105804908868664','105873896755947','88042803047215','105634720685845','105565464400480','105625593957752','89138288266704','105797392639585','106654775417922','105756321970183','105568954067359','106781476920663','105794439855675']}
    if _handle is not None:
        result.update({name:((int(_handle.noodle_stat_word(i,1))&0xffffffff)<<32)|(int(_handle.noodle_stat_word(i,0))&0xffffffff) for i,name in enumerate(fields)})
        _handle.noodle_background_status.argtypes=[C.c_uint];_handle.noodle_background_status.restype=C.c_uint64
        result['skin_mode']='NATIVE_GAME_PALETTES_ONLY'
        _handle.noodle_identity_status.argtypes=[C.c_uint];_handle.noodle_identity_status.restype=C.c_uint64
        result['identity_profiles']={k:int(_handle.noodle_identity_status(i))for i,k in enumerate(['ready','profiles','applies'])}
        result['card_backgrounds']={k:int(_handle.noodle_background_status(i))for i,k in enumerate(['applies','photo_key_restores'])}
        _handle.noodle_cr2008_char.argtypes=[C.c_uint];_handle.noodle_cr2008_char.restype=C.c_uint
        _handle.noodle_cr2008_seen.argtypes=[];_handle.noodle_cr2008_seen.restype=C.c_uint
        result['ronaldo_89136418985302_original_head']={'calls':int(_handle.noodle_cr2008_seen()),'path':''.join(chr(_handle.noodle_cr2008_char(i))for i in range(192)).split('\0',1)[0],'redirected':False}
        result['last_font_name_resource_path']=''.join(chr(_handle.noodle_font_char(i)) for i in range(192)).split('\0',1)[0]
        result['last_asset_path']=''.join(chr(_handle.noodle_path_char(i)) for i in range(160)).split('\0',1)[0]
        result['last_redirected_asset_path']=''.join(chr(_handle.noodle_redirect_char(i)) for i in range(160)).split('\0',1)[0]
        result['last_face_id']=''.join(chr(_handle.noodle_face_char(i)) for i in range(64)).split('\0',1)[0]
        result['last_common_head_mesh']=''.join(chr(_handle.noodle_common_char(i)) for i in range(96)).split('\0',1)[0]
        result['last_face_profile']=''.join(chr(_handle.noodle_profile_char(i)) for i in range(64)).split('\0',1)[0]
    try:
        for filename in ['player-faces-v25-status.json','noodle-hair-status.json']:
            path=HERE/filename;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));tmp.replace(path)
    except Exception:pass



def preflight(base,path):
    if digest(path)!=ENGINE_SHA:raise RuntimeError("unsupported 73 V16 engine; no patch installed")
    for entry,expected in [(0x39ca65c,'e80f19fcfd7b01a9fc6f02a9fa6703a9'),(0x388180c,'fd7bbaa9fc6f01a9fa6702a9f85f03a9'),(59257416, 'ff0307d1fd7b16a9fc6f17a9fa6718a9'), (59247036, 'fd7bbaa9fc6f01a9fa6702a9f85f03a9'), (53522004, 'ff4307d1fd7b17a9fc6f18a9fa6719a9'), (60556320, 'fd7bbba9f90b00f9f85f02a9f65703a9'), (60540272, 'fd7bbea9f44f01a9fd030091f40300aa'), (60540332, '08dc82522aa440a90000088b28004039'), (136560132, 'ff8301d1fd7b03a9f52300f9f44f05a9'), (136977992, 'fd7bbea9f30b00f9fd030091f30300aa'), (61409440, 'ff4306d1fd7b14a9fcab00f9f85f16a9'), (60602204, 'ffc306d1fd7b17a9fc5f18a9f65719a9'), (73095344, 'ff8301d1fd7b03a9f52300f9f44f05a9'), (60634628, 'ff0301d1fd7b01a9f65702a9f44f03a9'), (60636700, 'ff4302d1fd7b03a9fc6f04a9fa6705a9'), (60610332, 'ff0304d1fd7b0ca9f76b00f9f6570ea9'), (60611344, 'ff4307d1fd7b17a9fcc300f9fa6719a9')]:
        prologue=bytes.fromhex(expected)
        if not owned_entry(base,entry,prologue)and C.string_at(base+entry,len(prologue))!=prologue:
            raise RuntimeError("73 native hook conflict at "+hex(entry)+"; no V25 patch installed")

def _worker_once():
    global _handle,_payload_ok,_state,_error,_installing_entry
    try:
        bundle();_payload_ok=True
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        _state='WAITING_FOR_LIBUE4';report()
        while True:  # Keep waiting while the user stays in the pre-game editors.
            matches=[row for row in maps() if row[4].endswith('/libUE4.so') and row[3]==0]
            if matches:
                base=matches[0][0];path=matches[0][4]
                preflight(base,path)
                install(base,path,entry=0x3883248,prologue=bytes.fromhex('ff0307d1fd7b16a9fc6f17a9fa6718a9'),hook_name='noodle_card_data_ext_hook',configure_name='configure_card_data_ext')
                install(base,path,entry=0x38809bc,prologue=bytes.fromhex('fd7bbaa9fc6f01a9fa6702a9f85f03a9'),hook_name='noodle_card_data_hook',configure_name='configure_card_data')
                install(base,path,entry=0x330ae54,prologue=bytes.fromhex('ff4307d1fd7b17a9fc6f18a9fa6719a9'),hook_name='noodle_icon_data_hook',configure_name='configure_icon_data')
                install(base,path,entry=0x39c0420,prologue=bytes.fromhex('fd7bbba9f90b00f9f85f02a9f65703a9'),hook_name='noodle_shirt_key_hook',configure_name='configure_shirt_key')
                install(base,path,entry=0x39bc570,prologue=bytes.fromhex('fd7bbea9f44f01a9fd030091f40300aa'),hook_name='noodle_shirt_char_hook',configure_name='configure_shirt_char')
                install(base,path,entry=0x39bc5ac,prologue=bytes.fromhex('08dc82522aa440a90000088b28004039'),hook_name='noodle_shirt_string_hook',configure_name='configure_shirt_string')
                install(base,path,entry=0x823be04,prologue=bytes.fromhex('ff8301d1fd7b03a9f52300f9f44f05a9'),hook_name='noodle_record_lookup_hook',configure_name='configure_record_lookup')
                install(base,path,entry=0x82a1e48,prologue=bytes.fromhex('fd7bbea9f30b00f9fd030091f30300aa'),hook_name='noodle_record_name_hook',configure_name='configure_record_name')
                install(base,path,entry=0x3a908a0,prologue=bytes.fromhex('ff4306d1fd7b14a9fcab00f9f85f16a9'),hook_name='noodle_player_name_hook',configure_name='configure_player_name')
                import appearance_choices
                # RGB was retired; no custom body texture profiles are published.
                import profile_editor
                profile_editor.configure_noodle(_handle)
                import appearance_gear
                appearance_gear.configure_native(_handle)
                import photo_editor
                photo_editor.configure(_handle)
                install(base,path,entry=0x388180c,prologue=bytes.fromhex('fd7bbaa9fc6f01a9fa6702a9f85f03a9'),hook_name='noodle_background_hook',configure_name='configure_background')
                install(base,path,entry=0x39cb75c,prologue=bytes.fromhex('ffc306d1fd7b17a9fc5f18a9f65719a9'),hook_name='noodle_bake_hook',configure_name='configure_bake')
                install(base,path,entry=0x45b58b0,prologue=bytes.fromhex('ff8301d1fd7b03a9f52300f9f44f05a9'),hook_name='noodle_path_hook',configure_name='configure_path')
                install(base,path,entry=0x39d3604,prologue=bytes.fromhex('ff0301d1fd7b01a9f65702a9f44f03a9'),hook_name='noodle_texture_done_hook',configure_name='configure_texture_done')
                handle=install(base,path,entry=0x39d3e1c,prologue=bytes.fromhex('ff4302d1fd7b03a9fc6f04a9fa6705a9'),hook_name='noodle_done_hook',configure_name='configure_done')
                _handle=handle
                handle.noodle_enable.argtypes=[C.c_uint32];handle.noodle_enable.restype=None
                handle.noodle_stat.argtypes=[C.c_uint32];handle.noodle_stat.restype=C.c_uint64
                handle.noodle_stat_word.argtypes=[C.c_uint32,C.c_uint32];handle.noodle_stat_word.restype=C.c_uint32
                handle.noodle_font_char.argtypes=[C.c_uint32];handle.noodle_font_char.restype=C.c_uint32
                handle.noodle_face_char.argtypes=[C.c_uint32];handle.noodle_face_char.restype=C.c_uint32
                handle.noodle_path_char.argtypes=[C.c_uint32];handle.noodle_path_char.restype=C.c_uint32
                handle.noodle_redirect_char.argtypes=[C.c_uint32];handle.noodle_redirect_char.restype=C.c_uint32
                handle.noodle_common_char.argtypes=[C.c_uint32];handle.noodle_common_char.restype=C.c_uint32
                handle.noodle_profile_char.argtypes=[C.c_uint32];handle.noodle_profile_char.restype=C.c_uint32
                install(base,path,entry=0x39cd71c,prologue=bytes.fromhex('ff0304d1fd7b0ca9f76b00f9f6570ea9'),hook_name='noodle_load_hook',configure_name='configure_load')
                install(base,path,entry=0x39cdb10,prologue=bytes.fromhex('ff4307d1fd7b17a9fcc300f9fa6719a9'),hook_name='noodle_outer_hook',configure_name='configure_outer')
                _installing_entry=None
                _state='HOOK_ACTIVE';_ready.set()
                while True:
                    handle.noodle_enable(int(configuration()));report();time.sleep(10)
            time.sleep(2)
        raise RuntimeError('libUE4.so did not become available')
    except Exception as exc:
        _ready.clear();_state='ERROR';_error=str(exc)
        try:
            import mod_startup
            mod_startup.record_error('face-worker',exc)
        except Exception:pass
        if _handle is not None:
            try:_handle.noodle_enable(0)
            except Exception:pass
        report()


def start():
    global _started
    if _started:return
    _started=True;report();threading.Thread(target=worker,name='noodle-hair',daemon=True).start()


def worker():
    # Retain and recognize already installed branches after a partial attempt.
    # Never overwrite another component's hook or silently accept original play.
    for attempt in range(5):
        _worker_once()
        if _ready.is_set():return
        if attempt<4:time.sleep(min(2,0.25*(attempt+1)))

def wait_ready(timeout=15):
    start()
    if not _ready.wait(timeout):raise RuntimeError('Mod initialization incomplete; close and reopen game. See startup diagnostics.')
    return True
