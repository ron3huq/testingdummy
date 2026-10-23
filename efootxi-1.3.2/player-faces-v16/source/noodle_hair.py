"""Experimental exact-card noodle hair; engine calls occur only in native callbacks."""
import ctypes as C
import hashlib,json,os,platform,struct,threading,time
from pathlib import Path
ENGINE_SHA='3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98'
HOOK_SHA='7f60dc0cdffd14a1d3613da560b1b02fa597952725f90d291ee870c378ea1e45'
GETTER=0x39cd71c
PROLOGUE=bytes.fromhex('ff0304d1fd7b0ca9f76b00f9f6570ea9')
HERE=Path(__file__).resolve().parent
_keep=[]
_digest_cache={}
_started=False
_advertised=0
_handle=None
_payload_ok=False
_state='STARTING'
_error=None
_SESSION=time.time_ns()
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

def digest(path):
    stat = os.stat(path)
    key = (os.fspath(path), stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
    if key in _digest_cache:
        return _digest_cache[key]
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    result = h.hexdigest()
    if len(_digest_cache) >= 16:
        _digest_cache.clear()
    _digest_cache[key] = result
    return result

def install(base, path, entry=GETTER, prologue=PROLOGUE, hook_name='menu_hook', configure_name='configure'):
    if digest(path) != ENGINE_SHA:
        raise RuntimeError('unsupported libUE4.so SHA-256; no patch installed')
    libpath = HERE / 'libnoodle_hair.so'
    if digest(libpath) != HOOK_SHA:
        raise RuntimeError('hook binary SHA-256 mismatch')
    target = base + entry
    entries = maps()
    region = next((r for r in entries if r[0] <= target and target+16 <= r[1] and 'x' in r[2] and 'r' in r[2]), None)
    if region is None or C.string_at(target, 16) != prologue:
        raise RuntimeError('native prologue mismatch; no patch installed')
    hook = C.CDLL(str(libpath))
    configure = getattr(hook,configure_name)
    configure.argtypes = [C.c_size_t, C.c_size_t]
    configure.restype = None
    hook.flush.argtypes = [C.c_void_p, C.c_size_t]
    hook.flush.restype = None
    hook.store_instruction.argtypes = [C.c_void_p, C.c_uint32]
    hook.store_instruction.restype = None
    libc = C.CDLL('libc.so', use_errno=True)
    libc.mmap.argtypes = [C.c_void_p,C.c_size_t,C.c_int,C.c_int,C.c_int,C.c_long]
    libc.mmap.restype = C.c_void_p
    libc.munmap.argtypes = [C.c_void_p,C.c_size_t]
    libc.mprotect.argtypes = [C.c_void_p,C.c_size_t,C.c_int]
    page = os.sysconf('SC_PAGE_SIZE')
    # Non-fixed hints only: never replace an existing mapping. Need one free page within B range.
    candidates = []
    for left,right in zip(entries, entries[1:]):
        hint = (left[1]+page-1)&~(page-1)
        if hint+page <= right[0] and abs(hint-target) < (1<<27)-page:
            candidates.append(hint)
    candidates.sort(key=lambda p: abs(p-target))
    cave = None
    for hint in candidates:
        allocated = libc.mmap(hint,page,3,0x22,-1,0)  # RW, MAP_PRIVATE|MAP_ANONYMOUS, no MAP_FIXED
        if allocated in (None,C.c_void_p(-1).value):
            continue
        try:
            branch(target,allocated)
        except ValueError:
            libc.munmap(allocated,page)
            continue
        cave = allocated
        break
    if cave is None:
        raise RuntimeError('no nearby executable trampoline page; no patch installed')
    installed = False
    try:
        hookaddr = C.cast(getattr(hook,hook_name),C.c_void_p).value
        code = jump(hookaddr) + b'\0'*16 + prologue[:4] + jump(target+4)
        C.memmove(cave,code,len(code))
        hook.flush(cave,len(code))
        if libc.mprotect(cave,page,5) != 0:
            raise OSError(C.get_errno(),'Android denied executable trampoline')
        configure(base,cave+32)
        target_page = target&~(page-1)
        oldprot = (1 if 'r' in region[2] else 0)|(2 if 'w' in region[2] else 0)|(4 if 'x' in region[2] else 0)
        if libc.mprotect(target_page,page,oldprot|2) != 0:
            raise OSError(C.get_errno(),'Android denied native code modification')
        # One aligned atomic instruction store; no partially written 16-byte jump.
        try:
            if C.string_at(target,16) != prologue:
                raise RuntimeError('native entry changed during installation')
            _keep.extend([hook,libc,cave])
            hook.store_instruction(target,branch(target,cave))
            installed = True
            hook.flush(target,4)
        finally:
            if libc.mprotect(target_page,page,oldprot) != 0:
                raise OSError(C.get_errno(),'native hook installed but page permissions could not be restored; restart game')
        return hook
    finally:
        if not installed:
            libc.munmap(cave,page)

def configuration():
    try:
        data=json.loads((HERE/'noodle_hair.json').read_text())
        return data.get('enabled') is True
    except Exception:
        return False


def bundle():
    meta=json.loads((HERE/'noodle_bundle.json').read_text())
    if meta.get('target_card_ids')!=['88044950524330','89135066911146','106781745353130','106734785925546','105765448873424','88045755960841','88038776539586','105643042189511','106728863696709','105848932271764','105874433662542','88033139360669','106726716084650'] or meta.get('container')!='pc9298_mobile_and':
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
            version['version']+=34
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
        return value


def report():
    fields=['load_calls','target_calls','redirects','nonnull_callbacks','null_callbacks','skipped_face_id','busy_skips','unscoped_or_disabled_calls','restore_requests','reserved','last_target_id','reserved11','face_profile_reads','target_texture_callbacks','texture_nonnull_callbacks','texture_null_callbacks','outer_calls','texture_path_redirects','scoped_path_calls','mesh_path_redirects','face_texture_path_redirects','last_actor_type','reserved22','reserved23','face_bake_calls','private_texture_confirmed','face_texture_reapplied','face_texture_guard_skips','mesh_texture_inspections','mesh_texture_name_mismatches','mesh_texture_missing','mesh_material_invalid','mesh_texture_confirmed','body_skin_changes','body_skin_last_card','body_skin_index','mesh_texture_wrong_class','head_material_checks','head_material_rebinds','head_material_confirmed','head_material_rebind_failed','head_component_mismatch','bake_owner_missing','bake_texture_missing','bake_material_missing','xuan_son_name_changes','mesh_callback_component_matches','head_binding_state_bits','last_material_card_id','face_mid_created','face_mid_binding_checks','face_mid_failures','face_mid_source_channels_invalid','face_mid_channels_confirmed','face_mid_cache_hits','face_mid_last_card_id','shirt_name_changes','shirt_name_failures','shirt_name_last_card','native_ui_name_changes','native_ui_name_last_card','mq_shader_parent_confirmed','mq_shader_parent_mismatch','head_csm_receive_disabled','head_shadow_checks','duplicate_private_head_candidates','duplicate_private_head_mainpass_disabled','head_shadow_last_card','native_shirt_setter_intercepts','record_name_fields_updated','record_name_field_rejections','shirt_render_text_replaced']
    result={'session_id':_SESSION,'reported_at_unix':time.time(),'pid':os.getpid(),'runtime_path':str(Path(__file__).resolve()),'runtime_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'expected_native_sha256':HOOK_SHA,'state':_state,'version':'player-faces-v16-head-shadow-names','device_verified':False,'face_bake_guard':True,'error':_error,'enabled':configuration(),'payload_verified':_payload_ok,'manifest_advertised':_advertised,'target_card_ids':['88044950524330','89135066911146','106781745353130','106734785925546','105765448873424','88045755960841','88038776539586','105643042189511','106728863696709','105848932271764','105874433662542','88033139360669','106726716084650']}
    if _handle is not None:
        result.update({name:int(_handle.noodle_stat(i)) for i,name in enumerate(fields)})
        result['last_asset_path']=''.join(chr(_handle.noodle_path_char(i)) for i in range(160)).split('\0',1)[0]
        result['last_face_id']=''.join(chr(_handle.noodle_face_char(i)) for i in range(64)).split('\0',1)[0]
        result['last_face_profile']=''.join(chr(_handle.noodle_profile_char(i)) for i in range(64)).split('\0',1)[0]
    try:
        for filename in ['player-faces-v16-status.json','noodle-hair-status.json']:
            path=HERE/filename;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));tmp.replace(path)
    except Exception:pass


def worker():
    global _handle,_payload_ok,_state,_error
    try:
        bundle();_payload_ok=True
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        _state='WAITING_FOR_LIBUE4';report()
        for _ in range(300):
            matches=[row for row in maps() if row[4].endswith('/libUE4.so') and row[3]==0]
            if matches:
                base=matches[0][0];path=matches[0][4]
                install(base,path,entry=0x39c0420,prologue=bytes.fromhex('fd7bbba9f90b00f9f85f02a9f65703a9'),hook_name='noodle_shirt_key_hook',configure_name='configure_shirt_key')
                install(base,path,entry=0x39bc570,prologue=bytes.fromhex('fd7bbea9f44f01a9fd030091f40300aa'),hook_name='noodle_shirt_char_hook',configure_name='configure_shirt_char')
                install(base,path,entry=0x39bc5ac,prologue=bytes.fromhex('08dc82522aa440a90000088b28004039'),hook_name='noodle_shirt_string_hook',configure_name='configure_shirt_string')
                install(base,path,entry=0x823be04,prologue=bytes.fromhex('ff8301d1fd7b03a9f52300f9f44f05a9'),hook_name='noodle_record_lookup_hook',configure_name='configure_record_lookup')
                install(base,path,entry=0x82a1e48,prologue=bytes.fromhex('fd7bbea9f30b00f9fd030091f30300aa'),hook_name='noodle_record_name_hook',configure_name='configure_record_name')
                install(base,path,entry=0x3a908a0,prologue=bytes.fromhex('ff4306d1fd7b14a9fcab00f9f85f16a9'),hook_name='noodle_player_name_hook',configure_name='configure_player_name')
                install(base,path,entry=0x39cb75c,prologue=bytes.fromhex('ffc306d1fd7b17a9fc5f18a9f65719a9'),hook_name='noodle_bake_hook',configure_name='configure_bake')
                install(base,path,entry=0x45b58b0,prologue=bytes.fromhex('ff8301d1fd7b03a9f52300f9f44f05a9'),hook_name='noodle_path_hook',configure_name='configure_path')
                install(base,path,entry=0x39d3604,prologue=bytes.fromhex('ff0301d1fd7b01a9f65702a9f44f03a9'),hook_name='noodle_texture_done_hook',configure_name='configure_texture_done')
                handle=install(base,path,entry=0x39d3e1c,prologue=bytes.fromhex('ff4302d1fd7b03a9fc6f04a9fa6705a9'),hook_name='noodle_done_hook',configure_name='configure_done')
                _handle=handle
                handle.noodle_enable.argtypes=[C.c_uint32];handle.noodle_enable.restype=None
                handle.noodle_stat.argtypes=[C.c_uint32];handle.noodle_stat.restype=C.c_uint64
                handle.noodle_face_char.argtypes=[C.c_uint32];handle.noodle_face_char.restype=C.c_uint32
                handle.noodle_path_char.argtypes=[C.c_uint32];handle.noodle_path_char.restype=C.c_uint32
                handle.noodle_profile_char.argtypes=[C.c_uint32];handle.noodle_profile_char.restype=C.c_uint32
                install(base,path,entry=0x39cd71c,prologue=bytes.fromhex('ff0304d1fd7b0ca9f76b00f9f6570ea9'),hook_name='noodle_load_hook',configure_name='configure_load')
                install(base,path,entry=0x39cdb10,prologue=bytes.fromhex('ff4307d1fd7b17a9fcc300f9fa6719a9'),hook_name='noodle_outer_hook',configure_name='configure_outer')
                _state='HOOK_ACTIVE'
                while True:
                    handle.noodle_enable(int(configuration()));report();time.sleep(1)
            time.sleep(1)
        raise RuntimeError('libUE4.so did not become available')
    except Exception as exc:
        _state='ERROR';_error=str(exc)
        if _handle is not None:
            try:_handle.noodle_enable(0)
            except Exception:pass
        report()


def start():
    global _started
    if _started:return
    _started=True;report();threading.Thread(target=worker,name='noodle-hair',daemon=True).start()
