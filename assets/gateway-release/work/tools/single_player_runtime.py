"""Persistent choices for native single-player control. Staged until hooks validate."""
from pathlib import Path
import functools,json,threading,ctypes as C,platform,time
KEY='full7_single_player'
DEFAULT={'schema':1,'enabled':False,'player_id':None}
HERE=Path(__file__).parent
_module=None
_lock=threading.RLock()
_native=None
_ready=threading.Event()
_error=None
_started=False
_engine_base=0


def validate(data):
    if not isinstance(data,dict)or data.get('schema')!=1 or type(data.get('enabled'))is not bool:
        raise ValueError('Invalid single-player settings')
    pid=data.get('player_id')
    if pid is not None:
        import body_dimensions
        body_dimensions.identity(pid)
    if data['enabled'] and pid is None:
        raise ValueError('Choose a player first')
    return data


def config():
    if _module is None:
        return dict(DEFAULT)
    row=_module._logic.conn.execute('SELECT value FROM meta WHERE key=?',(KEY,)).fetchone()
    return validate(json.loads(row[0])if row else dict(DEFAULT))


_index_conn=None
_index_stamp=-1
_index_rows=()

def player_index():
    global _index_conn,_index_stamp,_index_rows
    import editor_names,motion_editor
    c=_module._logic.conn
    if _index_conn is c and _index_stamp==c.total_changes:
        return _index_rows
    # Only exact owned records currently assigned to the active squad.
    selected=c.execute('SELECT value FROM meta WHERE key=?',('main_squad_id',)).fetchone()
    squad_id=int(selected[0])if selected else 1
    saved=c.execute('SELECT json FROM squads WHERE squad_id=?',(squad_id,)).fetchone()
    squad=json.loads(saved[0])if saved else {}
    slots=(squad.get('squad_data')or{}).get('player_list')or[]
    if not isinstance(slots,list)or len(slots)>40:raise ValueError('Invalid current squad')
    rows={}
    for slot,entry in enumerate(slots):
        key=entry.get('gameplayer_id')or{}
        pid=str(key.get('id',0));serial=key.get('serial',0)
        if not pid.isdecimal()or not 0<int(pid)<2**63:continue
        record=c.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(int(pid),serial)).fetchone()
        if not record:continue
        if pid not in rows:rows[pid]={'id':pid,'name':editor_names.NAMES.get(pid,pid),'owned':True,'slot':slot,'serial':serial}
    for row in rows.values():row['search']=motion_editor.fold(row['name'])+' '+row['id']
    _index_rows=tuple(rows.values())
    _index_conn=c;_index_stamp=c.total_changes
    return _index_rows


def status():
    d=config()
    out=dict(d,ready=ready(),AI_off_behavior='selected_player_manual_when_enabled',AI_on_behavior='selected_player_manual_with_AI_teammates',manual_single_player_supported=True,changes_match_speed=False)
    if d['player_id'] is not None:
        row=next((r for r in player_index()if r['id']==d['player_id']),None)
        out['player_name']=row['name']if row else d['player_id']
        out['known']=row is not None
        out['owned']=bool(row and row['owned'])
    if _native is not None:
        keys={2:'requested_AI',3:'active',4:'generation',5:'side',6:'controller',7:'live_player',8:'reason_code'}
        out['runtime']={name:int(_native.single_player_status(i))for i,name in keys.items()}
    return out


def manage(action,req):
    if action=='ui7_single_player_get':
        return status()
    if action=='ui7_single_player_search':
        import motion_editor
        query=motion_editor.fold(str(req.get('query',''))[:80]);page=req.get('page',0)
        if type(page)is not int or not 0<=page<=2048:
            raise ValueError('Invalid player search page')
        rows=[{k:r[k]for k in('id','name')}for r in player_index()if not query or query in r['search']]
        return {'players':rows[page*40:(page+1)*40],'page':page,'total':len(rows)}
    import body_dimensions
    d=validate({'schema':1,'enabled':req.get('enabled'),'player_id':req.get('player_id')})
    c=_module._logic.conn
    if d['enabled']and not any(row['id']==d['player_id']for row in player_index()):
        raise ValueError('Choose a player from your current squad')
    live=action=='ui7_single_player_live'
    if body_dimensions.engine_loaded()and not live:
        raise ValueError('Use the in-match 1P button to change live control')
    if live:
        if _native is None or not _ready.is_set():raise ValueError('Single Player is still initializing')
        previous=config()
    with _lock:
        if c.in_transaction:
            raise ValueError('Another save is active')
        try:
            c.execute('BEGIN IMMEDIATE');c.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(KEY,json.dumps(d,separators=(',',':'))))
            if live and _native.single_player_configure(_engine_base,int(d['enabled']),int(d['player_id']or 0))!=1:raise ValueError('Live single-player control was rejected')
            c.commit()
        except Exception:
            c.rollback()
            if live:_native.single_player_configure(_engine_base,int(previous['enabled']),int(previous['player_id']or 0))
            raise
    start()
    return dict(d,saved=True,applies='live'if live else'next_game_launch')


def install(root,module):
    global _module
    if _module is not None:
        return
    _module=module
    config()
    original=module.manage
    @functools.wraps(original)
    def wrapped(action,payload=''):
        if action in('ui7_single_player_get','ui7_single_player_search','ui7_single_player_apply','ui7_single_player_live'):
            return json.dumps(manage(action,json.loads(payload or'{}')))
        return original(action,payload)
    module.manage=wrapped


def ready():
    return _ready.is_set()


def require_ready(timeout=15):
    if platform.machine().lower()not in('aarch64','arm64'):
        return
    start()
    deadline=time.monotonic()+timeout
    while not _ready.is_set():
        if _error:
            raise RuntimeError('Single-player control initialization failed: '+str(_error))
        if time.monotonic()>=deadline:
            raise RuntimeError('Single-player control hooks are not ready')
        time.sleep(.05)

ENGINE_SHA='efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
HOOK_SHA='db7235a3debbd52a04976523ee1d2d144d5d906ce35a8568c74eff05e9771c78'
HOOKS=(
    (0x6b53180,bytes.fromhex('ffc304d1e86300fdfd7b0da9fc6f0ea9'),'single_update','configure_single_update'),
    (0x6b52b0c,bytes.fromhex('fd7bbea9f44f01a9fd030091f40300aa'),'single_ctor','configure_single_ctor'),
    (0x6b52f2c,bytes.fromhex('ff0301d1fd7b01a9f51300f9f44f03a9'),'single_dtor','configure_single_dtor'),
    (0x72dfe40,bytes.fromhex('ff0307d1fd7b16a9fc6f17a9fa6718a9'),'single_restore','configure_single_restore'),
    (0x72df7f4,bytes.fromhex('0824835201682838c0035fd6fd7bbea9'),'single_pause','configure_single_pause'),
    (0x72defe4,bytes.fromhex('fd7bbda9f50b00f9f44f02a9fd030091'),'single_transition','configure_single_transition'),
    (0x6a9d2e0,bytes.fromhex('e101805226b6fb17000840bdc0035fd6'),'single_getter','configure_single_getter'),
)

# Checked native bootstrap. Hooks remain passive while disabled, ready for the in-match toggle.
from mod_integrity import digest
from select_team_runtime import maps,branch
_installed_hooks={}
_keep=[]

def owned_entry(base,entry,expected):
    item=_installed_hooks.get((base,entry))
    if item is None:
        return False
    target,cave,_=item
    return C.string_at(target,4)==__import__('struct').pack('<I',branch(target,cave)) and C.string_at(target+4,len(expected)-4)==expected[4:]

def _worker():
    global _native,_error,_started,_engine_base
    try:
        while True:
            matches=[r for r in maps()if r[4].endswith('/libUE4.so')and r[3]==0]
            if matches:
                break
            time.sleep(.25)
        d=config()
        base=matches[0][0];path=matches[0][4];_engine_base=base
        if digest(path)!=ENGINE_SHA or digest(HERE/'libsingle_player.so')!=HOOK_SHA:
            raise RuntimeError('Unsupported engine or single-player native checksum mismatch')
        for entry,prologue,_,_ in HOOKS:
            if C.string_at(base+entry,16)!=prologue:
                raise RuntimeError('Single-player native hook conflict at '+hex(entry))
        hook=C.CDLL(str(HERE/'libsingle_player.so'))
        hook.single_player_configure.argtypes=[C.c_size_t,C.c_uint,C.c_size_t]
        hook.single_player_configure.restype=C.c_uint
        hook.single_player_status.argtypes=[C.c_uint]
        hook.single_player_status.restype=C.c_uint64
        if hook.single_player_configure(base,int(d['enabled']),int(d['player_id']or 0))!=1:
            raise RuntimeError('Single-player native configuration rejected')
        import hook_arena
        for entry,prologue,name,configure in HOOKS:
            hook_arena.install(globals(),base,path,entry,prologue,name,configure)
        if int(hook.single_player_status(9))!=127 or len(_installed_hooks)!=7:
            raise RuntimeError('Incomplete single-player native hook installation')
        import single_player_lookup_runtime
        single_player_lookup_runtime.install(base,path,hook)
        _native=hook
        _ready.set()
    except Exception as exc:
        _error=str(exc)
        _ready.clear()
        import mod_startup
        mod_startup.record_error('single-player-startup',exc)
    finally:
        if not _ready.is_set():
            _started=False

def start():
    global _started,_error
    if platform.machine().lower()not in('aarch64','arm64'):
        return
    with _lock:
        if _started:
            return
        _error=None
        _started=True
        threading.Thread(target=_worker,name='SinglePlayerNative',daemon=True).start()
