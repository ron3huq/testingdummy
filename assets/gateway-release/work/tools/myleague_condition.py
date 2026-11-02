"""Force final My League condition after native roster probability/capping.

Live Update, Form consistency, stamina and injury retain their native meanings.
The checked native setter also covers conditions restored from match records.
"""
from pathlib import Path
import ctypes as C
import functools
import json
import platform
import threading
import time

SCOPES=(122,128,473,518,566,549,125)
LEVELS=('Terrible','Bad','Normal','Good','Excellent')
ENTRY=0x7095740
PROLOGUE=bytes.fromhex('2808001209cc40f9090968b309cc00f9')
HERE=Path(__file__).parent
PATH=HERE/'myleague_condition.json'
DEFAULT={'schema':1,'enabled':True,'scope':'owned_players_in_myleague'}
_lock=threading.RLock()
_native=None
_installed=False
_module=None
KEY='full7_myleague_condition'

def config():
    d=json.loads(PATH.read_text()) if PATH.exists() else dict(DEFAULT)
    if _module is not None:
        row=_module._logic.conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone()
        if row is not None:
            d=json.loads(row[0])
    if not isinstance(d,dict) or d.get('schema')!=1 or type(d.get('enabled'))is not bool or d.get('scope')not in('owned_players_in_myleague','both_teams_in_myleague'):
        raise ValueError('Invalid My League condition policy')
    return d

def configure_native(hook,base):
    global _native
    with _lock:
        d=config()
        hook.myleague_condition_configure.argtypes=[C.c_size_t,C.c_uint,C.c_uint]
        hook.myleague_condition_configure.restype=C.c_uint
        hook.myleague_condition_status.argtypes=[C.c_uint]
        hook.myleague_condition_status.restype=C.c_uint64
        if hook.myleague_condition_configure(base,int(d['enabled']),int(d['scope']=='both_teams_in_myleague'))!=1:
            raise RuntimeError('My League condition engine identity mismatch')
        _native=hook

def ready():
    import select_team_runtime as team
    return _native is not None and team._ready.is_set() and any(entry==ENTRY for _,entry in team._installed_hooks)

def require_ready(timeout=15):
    if platform.machine().lower() not in('aarch64','arm64'):
        return
    deadline=time.monotonic()+timeout
    while not ready():
        if time.monotonic()>=deadline:
            raise RuntimeError('My League final-condition hook was not initialized')
        time.sleep(.05)

def status():
    d=config()
    out={'enabled':d['enabled'],'scope':d['scope'],'competitions':list(SCOPES),'condition_levels':dict(enumerate(LEVELS)),'forced_condition':4,'ready':ready(),'changes_Live_Update_or_Form':False,'preserves_stamina_and_injury':True,'applies_after_native_team_condition_cap':True}
    if _native is not None:
        out.update(active_competition=int(_native.myleague_condition_status(2)),condition_assignments_forced=int(_native.myleague_condition_status(3)))
    return out

def install(root,module):
    global _installed,_module
    if _installed:
        return
    _module=module
    config()
    old_manage=module.manage
    @functools.wraps(old_manage)
    def manage(action,payload=''):
        if action=='ui7_myleague_condition_get':
            return json.dumps(status())
        if action=='ui7_myleague_condition_apply':
            req=json.loads(payload or'{}')
            d=dict(DEFAULT,enabled=req.get('enabled'),scope=req.get('scope',config()['scope']))
            if type(d['enabled'])is not bool or d['scope']not in('owned_players_in_myleague','both_teams_in_myleague'):
                raise ValueError('Choose an enabled state and player scope')
            import body_dimensions
            if body_dimensions.engine_loaded():
                raise ValueError('Close and reopen the app; change My League condition before Enter Game')
            with _lock:
                conn=module._logic.conn
                if conn.in_transaction:
                    raise ValueError('Another save operation is active')
                try:
                    conn.execute('BEGIN IMMEDIATE')
                    conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(d,separators=(',',':'))))
                    conn.commit()
                except Exception:
                    conn.rollback()
                    raise
            return json.dumps({'saved':True,'enabled':d['enabled'],'scope':d['scope'],'applies':'next_game_launch'})
        return old_manage(action,payload)
    module.manage=manage
    _installed=True
