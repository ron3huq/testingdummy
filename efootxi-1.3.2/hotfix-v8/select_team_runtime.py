"""Experimental efootxi 1.3.2 ARM64 menu hook, loaded by its embedded Python.
No root, Frida server, CPK replacement, APK signing, or save modification.
Device integration is UNVERIFIED. Failure before installation records a diagnostic.
"""
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import threading
import time

ENGINE_SHA = '3da06a36fb5c434a75c5739af65f16664347477bd653659eb354376410d52f98'
HOOK_SHA = '20d3026ab442d03c1305beedfa260c71ebee52ab927e30a1ac4b6e98bf3ed566'
GETTER = 0x737e05c
PROLOGUE = bytes.fromhex('fd7bbaa9fb0b00f9fa6702a9f85f03a9')
HERE = Path(__file__).resolve().parent
_started = False
_keep = []  # Never unload code or free trampolines while native threads may use them.


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


def diagnostic(state, **kwargs):
    try:
        p = HERE / 'select-team-status.json'
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps({'state': state, 'version':'native-hotfix-v8', 'device_verified': False, **kwargs}, indent=2))
        tmp.replace(p)
    except Exception:
        pass


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def install(base, path, entry=GETTER, prologue=PROLOGUE, hook_name='menu_hook', configure_name='configure'):
    if digest(path) != ENGINE_SHA:
        raise RuntimeError('unsupported libUE4.so SHA-256; no patch installed')
    libpath = HERE / 'libselect_team.so'
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
    hook.status.argtypes = [C.c_uint]
    hook.status.restype = C.c_uint
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


_native_handle = None

def ensure_native_team(team):
    return int(_native_handle.ensure_team(int(team))) if _native_handle is not None else 10

def activate_context(cid):
    if _native_handle is not None:_native_handle.activate_context(int(cid))

def stadium_mask(snow=False):
    return int(_native_handle.stadium_mask(int(bool(snow)))) if _native_handle is not None else 0

def set_environment(cid,stadium,snow=False):
    return int(_native_handle.set_environment(int(cid),int(stadium),int(bool(snow)))) if _native_handle is not None else 10

def worker():
    global _native_handle
    try:
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        diagnostic('WAITING_FOR_LIBUE4')
        for _ in range(300):
            matches = [r for r in maps() if r[4].endswith('/libUE4.so') and r[3]==0]
            if matches:
                base = matches[0][0]
                hook = install(base,matches[0][4])
                install(base,matches[0][4],entry=0x823c9d4,prologue=bytes.fromhex('ffc300d1fd7b01a9f44f02a9fd430091'),hook_name='team_hook',configure_name='configure_team')
                install(base,matches[0][4],entry=0x823c8d4,prologue=bytes.fromhex('ff0301d1fd7b02a9f44f03a9fd830091'),hook_name='player_hook',configure_name='configure_player')
                install(base,matches[0][4],entry=0x82948d0,prologue=bytes.fromhex('280040b909bb80520a8018910929a99b'),hook_name='cached_team_hook',configure_name='configure_cached_team')
                install(base,matches[0][4],entry=0x82948ec,prologue=bytes.fromhex('ff0301d1fd7b01a9f65702a9f44f03a9'),hook_name='cached_find_hook',configure_name='configure_cached_find')
                install(base,matches[0][4],entry=0x82446d8,prologue=bytes.fromhex('ff0301d1fd7b02a9f31b00f9fd830091'),hook_name='kit_resource_hook',configure_name='configure_kit_resource')
                hook.cached_status.argtypes=[];hook.cached_status.restype=C.c_uint
                install(base,matches[0][4],entry=0x3422074,prologue=bytes.fromhex('ff4301d1fd7b02a9f51b00f9f44f04a9'),hook_name='stage_default_hook',configure_name='configure_stage_default')
                install(base,matches[0][4],entry=0x3421e38,prologue=bytes.fromhex('ff4301d1fd7b02a9f51b00f9f44f04a9'),hook_name='stage_home_hook',configure_name='configure_stage_home')
                hook.ensure_team.argtypes=[C.c_uint];hook.ensure_team.restype=C.c_uint
                hook.native_status.argtypes=[C.c_uint];hook.native_status.restype=C.c_uint
                hook.last_player_id.argtypes=[];hook.last_player_id.restype=C.c_uint64
                hook.activate_context.argtypes=[C.c_uint];hook.activate_context.restype=None
                hook.stadium_mask.argtypes=[C.c_uint];hook.stadium_mask.restype=C.c_uint
                hook.set_environment.argtypes=[C.c_uint,C.c_uint,C.c_uint];hook.set_environment.restype=C.c_uint
                hook.environment_status.argtypes=[C.c_uint];hook.environment_status.restype=C.c_uint
                _native_handle=hook
                presentation_error=None
                try:
                    install(base,matches[0][4],entry=0x3a56de8,prologue=bytes.fromhex('ff0306d1fd7b12a9fc6f13a9fa6714a9'),hook_name='emblem_hook',configure_name='configure_emblem')
                except Exception as exc:
                    presentation_error=str(exc)
                for address,hook_name,configure_name in [(0x82b4a7c,'short_hook','configure_short'),(0x3a5586c,'kit_hook','configure_kit'),(0x3a5583c,'competition_name_hook','configure_competition_name'),(0x3a59924,'competition_logo_hook','configure_competition_logo')]:
                    try:
                        prologues={0x82b4a7c:'00280191c0035fd60850218b3f0c0071',0x3a5586c:'fd7bbca9f85f01a9f65702a9f44f03a9',0x3a5583c:'fd7bbea9f44f01a9fd030091f303002a',0x3a59924:'ff4305d1fd7b10a9fc8b00f9f85f12a9'}
                        install(base,matches[0][4],entry=address,prologue=bytes.fromhex(prologues[address]),hook_name=hook_name,configure_name=configure_name)
                    except Exception as exc:
                        presentation_error=(presentation_error+'; ' if presentation_error else '')+hook_name+': '+str(exc)
                environment_error=None
                # Stage selectors are game-called member hooks; the gateway only writes atomics.
                diagnostic('HOOK_INSTALLED_MENU_NOT_YET_VERIFIED' ,presentation_error=presentation_error)
                previous = None
                while True:
                    stats = tuple(hook.status(i) for i in range(13))+tuple(hook.native_status(i) for i in range(22))+tuple(hook.environment_status(i) for i in range(3))+(hook.cached_status(),)
                    if stats != previous:
                        diagnostic('HOOK_ACTIVE',environment_error=environment_error,active_competition=stats[35],selected_stadium=stats[36],ovr_balance_failures=stats[37],presentation_error=presentation_error,result=stats[0],patched_contexts=stats[1],menu_calls=stats[2],league_results={cid:stats[3+i] for i,cid in enumerate(['122','566','128','125','549'])},patched_leagues={cid:stats[8+i] for i,cid in enumerate(['122','566','128','125','549'])},native_team_results={tid:stats[13+i] for i,tid in enumerate(['108', '114', '127', '45', '116', '18961', '5317', '1222', '1220', '1986', '1219', '132', '131', '2365', '1987', '1221', '2621', '1985'])},native_player_applies=stats[31],native_last_player_error=stats[32],native_last_team_error=stats[33],native_last_player_reason=stats[34],native_last_player_full_id=hook.last_player_id(),cached_team_applies=hook.cached_status())
                        previous = stats
                    time.sleep(1)
            time.sleep(1)
        raise RuntimeError('libUE4.so not loaded in this Python process')
    except Exception as exc:
        diagnostic('INSTALL_FAILED',error=str(exc))


def start():
    global _started
    if not _started:
        _started = True
        threading.Thread(target=worker,name='MyLeagueMenuFix',daemon=True).start()
