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
HOOK_SHA = '16a02639588f6901418e0c425d8f24cdaa6b62dbabb52504e57a0681dbea49cb'
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
        tmp.write_text(json.dumps({'state': state, 'device_verified': False, **kwargs}, indent=2))
        tmp.replace(p)
    except Exception:
        pass


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def install(base, path):
    if digest(path) != ENGINE_SHA:
        raise RuntimeError('unsupported libUE4.so SHA-256; no patch installed')
    libpath = HERE / 'libselect_team.so'
    if digest(libpath) != HOOK_SHA:
        raise RuntimeError('hook binary SHA-256 mismatch')
    target = base + GETTER
    entries = maps()
    region = next((r for r in entries if r[0] <= target and target+16 <= r[1] and 'x' in r[2] and 'r' in r[2]), None)
    if region is None or C.string_at(target, 16) != PROLOGUE:
        raise RuntimeError('native prologue mismatch; no patch installed')
    hook = C.CDLL(str(libpath))
    hook.configure.argtypes = [C.c_size_t, C.c_size_t]
    hook.configure.restype = None
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
        hookaddr = C.cast(hook.menu_hook,C.c_void_p).value
        code = jump(hookaddr) + b'\0'*16 + PROLOGUE[:4] + jump(target+4)
        C.memmove(cave,code,len(code))
        hook.flush(cave,len(code))
        if libc.mprotect(cave,page,5) != 0:
            raise OSError(C.get_errno(),'Android denied executable trampoline')
        hook.configure(base,cave+32)
        target_page = target&~(page-1)
        oldprot = (1 if 'r' in region[2] else 0)|(2 if 'w' in region[2] else 0)|(4 if 'x' in region[2] else 0)
        if libc.mprotect(target_page,page,oldprot|2) != 0:
            raise OSError(C.get_errno(),'Android denied native code modification')
        # One aligned atomic instruction store; no partially written 16-byte jump.
        try:
            if C.string_at(target,16) != PROLOGUE:
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


def worker():
    try:
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        diagnostic('WAITING_FOR_LIBUE4')
        for _ in range(300):
            matches = [r for r in maps() if r[4].endswith('/libUE4.so') and r[3]==0]
            if matches:
                base = matches[0][0]
                hook = install(base,matches[0][4])
                diagnostic('HOOK_INSTALLED_MENU_NOT_YET_VERIFIED')
                previous = None
                while True:
                    stats = tuple(hook.status(i) for i in range(3))
                    if stats != previous:
                        diagnostic('HOOK_ACTIVE',result=stats[0],patched_contexts=stats[1],menu_calls=stats[2])
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
