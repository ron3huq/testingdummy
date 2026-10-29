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

ENGINE_SHA = 'efd257d9e41b622d6ecb8f51f7b0a8ee8820113fd427c5572025df1c8eecc7b8'
HOOK_SHA='5b305abde16e2984e52a85a67de28e92f7090689ef1c7933c8b105f62bbd0e30'
GETTER = 0x737e05c
PROLOGUE = bytes.fromhex('fd7bbaa9fb0b00f9fa6702a9f85f03a9')
HERE = Path(__file__).resolve().parent
_started = False
_ready=threading.Event()
_installed_hooks={}
def owned_entry(base,entry,expected):
 item=_installed_hooks.get((base,entry))
 if item is None:return False
 target,cave,hook=item
 return C.string_at(target,4)==struct.pack('<I',branch(target,cave))and C.string_at(target+4,len(expected)-4)==expected[4:]

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
        tmp.write_text(json.dumps({'state': state, 'version':'v25-73-full1', 'device_verified': False, **kwargs}, indent=2))
        tmp.replace(p)
    except Exception:
        pass


_digest_cache = {}

from mod_integrity import digest


def relocated_first(prologue, target):
    word=struct.unpack('<I',prologue[:4])[0]
    if (word & 0x7e000000) in (0x34000000,0x36000000) or (word & 0xff000010)==0x54000000:
        bits,shift=(14,5) if (word & 0x7e000000)==0x36000000 else (19,5)
        mask=(1<<bits)-1;imm=(word>>shift)&mask
        if imm & (1<<(bits-1)):imm-=1<<bits
        destination=target+imm*4
        local=(word & ~(mask<<shift)) | (5<<shift)
        return struct.pack('<I',local)+jump(target+4)+jump(destination)
    return prologue[:4]+jump(target+4)

def install(base, path, entry=GETTER, prologue=PROLOGUE, hook_name='menu_hook', configure_name='configure'):
    import hook_arena
    return hook_arena.install(globals(),base,path,entry,prologue,hook_name,configure_name)


_native_handle = None

def ensure_native_team(team):
    return int(_native_handle.ensure_team(int(team))) if _native_handle is not None else 10

_owned_cards=()

def configure_owned_players(ids):
 global _owned_cards
 values=tuple(sorted(set(int(i)for i in ids)))
 if values==_owned_cards:return
 if len(values)>8192 or any(i<=0 or i>=2**63 for i in values):raise ValueError('Invalid owned-card list')
 _owned_cards=values
 if _native_handle is not None:_install_owned(_native_handle)

def _install_owned(hook):
 array=(C.c_uint64*len(_owned_cards))(*_owned_cards);hook.configure_owned_cards.argtypes=[C.POINTER(C.c_uint64),C.c_uint];hook.configure_owned_cards.restype=C.c_uint
 if hook.configure_owned_cards(array,len(_owned_cards))!=1:raise RuntimeError('Owned-card protection rejected')

_pending_context=0
def activate_context(cid):
    global _pending_context
    _pending_context=int(cid)
    if _native_handle is not None:_native_handle.activate_context(_pending_context)

def stadium_mask(snow=False):
    return int(_native_handle.stadium_mask(int(bool(snow)))) if _native_handle is not None else 0

def set_environment(cid,stadium,snow=False):
    return int(_native_handle.set_environment(int(cid),int(stadium),int(bool(snow)))) if _native_handle is not None else 10


def preflight(base,path):
    if digest(path)!=ENGINE_SHA:raise RuntimeError("unsupported 73 V16 engine")
    for entry,expected in [(121102428, 'fd7bbaa9fb0b00f9fa6702a9f85f03a9'), (136563156, 'ffc300d1fd7b01a9f44f02a9fd430091'), (136562900, 'ff0301d1fd7b02a9f44f03a9fd830091'), (136923344, '280040b909bb80520a8018910929a99b'), (136923372, 'ff0301d1fd7b01a9f65702a9f44f03a9'), (136595160, 'ff0301d1fd7b02a9f31b00f9fd830091'), (54665332, 'ff4301d1fd7b02a9f51b00f9f44f04a9'), (54664760, 'ff4301d1fd7b02a9f51b00f9f44f04a9'), (59357124, 'ff4306d1fd7b14a9fc6715a9f85f16a9'), (59358164, 'ff4306d1fd7b14a9fc6715a9f85f16a9'), (59358684, 'ff4306d1fd7b14a9fc6715a9f85f16a9'), (136564688, 'fd7bbea9f44f01a9fd030091f30300aa'), (136564940, 'fd7bbea9f30b00f9fd030091f30300aa'), (137038356, 'e8031f2a3f30007128050054e903012a'), (109906024, 'fd7bbfa9fd03009102600091e00301aa'), (109898564, 'fd7bbaa9fc6f01a9fa6702a9f85f03a9'), (109949264, '800000b4080040f9032d40f960001fd6'), (60863116, 'fd7bbaa9fc6f01a9fa6702a9f85f03a9'), (61173224, 'ff0306d1fd7b12a9fc6f13a9fa6714a9'), (137054844, '00280191c0035fd60850218b3f0c0071'), (61167724, 'fd7bbca9f85f01a9f65702a9f44f03a9'), (61167676, 'fd7bbea9f44f01a9fd030091f303002a'), (61184292, 'ff4305d1fd7b10a9fc8b00f9f85f12a9')]:
        if not owned_entry(base,entry,bytes.fromhex(expected))and C.string_at(base+entry,16)!=bytes.fromhex(expected):
            raise RuntimeError("My League hook conflict at "+hex(entry)+"; no My League hook installed")

def _worker_once():
    global _native_handle
    try:
        if platform.machine().lower() not in ('aarch64','arm64') or C.sizeof(C.c_void_p)!=8:
            raise RuntimeError('only Android ARM64 supported')
        diagnostic('WAITING_FOR_LIBUE4')
        while True:  # Keep waiting while the user stays in the pre-game editors.
            matches = [r for r in maps() if r[4].endswith('/libUE4.so') and r[3]==0]
            if matches:
                base = matches[0][0]
                preflight(base,matches[0][4])
                codec_errors={}
                hook = install(base,matches[0][4])
                install(base,matches[0][4],entry=0x823c9d4,prologue=bytes.fromhex('ffc300d1fd7b01a9f44f02a9fd430091'),hook_name='team_hook',configure_name='configure_team')
                install(base,matches[0][4],entry=0x823c8d4,prologue=bytes.fromhex('ff0301d1fd7b02a9f44f03a9fd830091'),hook_name='player_hook',configure_name='configure_player')
                install(base,matches[0][4],entry=0x82948d0,prologue=bytes.fromhex('280040b909bb80520a8018910929a99b'),hook_name='cached_team_hook',configure_name='configure_cached_team')
                install(base,matches[0][4],entry=0x82948ec,prologue=bytes.fromhex('ff0301d1fd7b01a9f65702a9f44f03a9'),hook_name='cached_find_hook',configure_name='configure_cached_find')
                install(base,matches[0][4],entry=0x82446d8,prologue=bytes.fromhex('ff0301d1fd7b02a9f31b00f9fd830091'),hook_name='kit_resource_hook',configure_name='configure_kit_resource')
                hook.cached_status.argtypes=[];hook.cached_status.restype=C.c_uint
                install(base,matches[0][4],entry=0x3422074,prologue=bytes.fromhex('ff4301d1fd7b02a9f51b00f9f44f04a9'),hook_name='stage_default_hook',configure_name='configure_stage_default')
                install(base,matches[0][4],entry=0x3421e38,prologue=bytes.fromhex('ff4301d1fd7b02a9f51b00f9f44f04a9'),hook_name='stage_home_hook',configure_name='configure_stage_home')
                install(base,matches[0][4],entry=0x389b7c4,prologue=bytes.fromhex('ff4306d1fd7b14a9fc6715a9f85f16a9'),hook_name='name_caps_hook',configure_name='configure_name_caps')
                install(base,matches[0][4],entry=0x389bbd4,prologue=bytes.fromhex('ff4306d1fd7b14a9fc6715a9f85f16a9'),hook_name='name_knockout_hook',configure_name='configure_name_knockout')
                install(base,matches[0][4],entry=0x389bddc,prologue=bytes.fromhex('ff4306d1fd7b14a9fc6715a9f85f16a9'),hook_name='name_all_hook',configure_name='configure_name_all')
                install(base,matches[0][4],entry=0x823cfd0,prologue=bytes.fromhex('fd7bbea9f44f01a9fd030091f30300aa'),hook_name='compe_record_hook',configure_name='configure_compe_record')
                install(base,matches[0][4],entry=0x823d0cc,prologue=bytes.fromhex('fd7bbea9f30b00f9fd030091f30300aa'),hook_name='compe_unit_hook',configure_name='configure_compe_unit')
                install(base,matches[0][4],entry=0x82b0a14,prologue=bytes.fromhex('e8031f2a3f30007128050054e903012a'),hook_name='stadium_parameter_hook',configure_name='configure_stadium_parameter')
                hook.name_status.argtypes=[];hook.name_status.restype=C.c_uint
                hook.ensure_team.argtypes=[C.c_uint];hook.ensure_team.restype=C.c_uint
                hook.native_status.argtypes=[C.c_uint];hook.native_status.restype=C.c_uint
                hook.last_player_id.argtypes=[];hook.last_player_id.restype=C.c_uint64
                hook.activate_context.argtypes=[C.c_uint];hook.activate_context.restype=None
                hook.stadium_mask.argtypes=[C.c_uint];hook.stadium_mask.restype=C.c_uint
                hook.set_environment.argtypes=[C.c_uint,C.c_uint,C.c_uint];hook.set_environment.restype=C.c_uint
                hook.environment_status.argtypes=[C.c_uint];hook.environment_status.restype=C.c_uint
                _install_owned(hook)
                _native_handle=hook
                hook.activate_context(_pending_context)
                face_lib=C.CDLL(str(HERE/'libnoodle_hair.so'));hook.configure_classic_notify.argtypes=[C.c_size_t];hook.configure_classic_notify(C.cast(face_lib.noodle_set_league_scope,C.c_void_p).value)

                hook.codec_status.argtypes=[C.c_uint];hook.codec_status.restype=C.c_uint
                skill_text_error=None
                try:
                    install(base,matches[0][4],entry=0x2f47358,prologue=bytes.fromhex('ff8301d1fd7b03a9f52300f9f44f05a9'),hook_name='skill_text_hook',configure_name='configure_skill_text')
                except Exception as exc:skill_text_error=str(exc)
                try:
                    install(base,matches[0][4],entry=0x2f44e4c,prologue=bytes.fromhex('fd7bbaa9fc6f01a9fa6702a9f85f03a9'),hook_name='skill_page_hook',configure_name='configure_skill_page')
                except Exception as exc:skill_text_error=(skill_text_error+'; 'if skill_text_error else'')+str(exc)
                hook.skill_text_status.argtypes=[];hook.skill_text_status.restype=C.c_uint
                hook.set_appearance_trial.argtypes=[C.c_uint];hook.set_appearance_trial.restype=None
                trial_error=None
                try:
                    settings=json.loads((HERE/'myleague_custom.json').read_text())
                    trial=settings.get('requested_appearance',{}).get('sleeve_copy',{}).get('rolled_trial',{}).get('enabled',False)
                    hook.set_appearance_trial(int(trial is True))
                except Exception as exc:
                    hook.set_appearance_trial(0);trial_error=str(exc)
                editor_error=None
                editor_team_ids=[]
                try:
                    import myleague_editor_runtime as editor
                    editor.install_native(hook)
                    import player_model
                    hook.editor_copy_status.argtypes=[C.c_uint];hook.editor_copy_status.restype=C.c_uint64
                    hook.editor_motion_status.argtypes=[C.c_uint];hook.editor_motion_status.restype=C.c_uint64
                    hook.editor_gear_status.argtypes=[C.c_uint];hook.editor_gear_status.restype=C.c_uint64
                    hook.editor_gear_detail_status.argtypes=[C.c_uint];hook.editor_gear_detail_status.restype=C.c_uint64
                    hook.editor_socks_status.argtypes=[C.c_uint];hook.editor_socks_status.restype=C.c_uint64
                    import profile_editor
                    profile_editor.configure_select(hook)
                    import motion_editor
                    motion_editor.configure(hook)
                    import transfer_editor
                    transfer_editor.configure(hook)
                    import appearance_gear
                    appearance_gear.configure_select(hook)
                    player_model.configure_native(hook)
                    editor_team_ids=[row['team_id'] for row in editor.config().get('teams',[])]
                except Exception as exc:
                    editor_error=str(exc)
                hook.editor_team_status.argtypes=[C.c_uint];hook.editor_team_status.restype=C.c_uint
                hook.skin_status.argtypes=[C.c_uint];hook.skin_status.restype=C.c_uint64
                hook.editor_status.argtypes=[C.c_uint];hook.editor_status.restype=C.c_uint64
                import noodle_hair
                face_hook=noodle_hair.wait_ready(15)and noodle_hair._handle
                hook.configure_cut_scope.argtypes=[C.c_uint64,C.c_uint64];hook.configure_cut_scope.restype=None
                hook.configure_cut_scope(C.cast(face_hook.noodle_body_begin,C.c_void_p).value,C.cast(face_hook.noodle_body_end,C.c_void_p).value)
                for address,prologue,name in [(0x39ce7d8,'ffc306d1fd7b15a9fc6f16a9fa6717a9','detail'),(0x39cefe4,'ffc301d1fd7b03a9f72300f9f65705a9','common')]:
                    install(base,matches[0][4],entry=address,prologue=bytes.fromhex(prologue),hook_name='cut_'+name+'_hook',configure_name='configure_cut_'+name)
                hook.editor_cut_status.argtypes=[C.c_uint];hook.editor_cut_status.restype=C.c_uint64
                rolled_error=None;rolled_hooks=[]
                hook.rolled_enable.argtypes=[C.c_uint];hook.rolled_enable(0)
                appearance_error=None
                hook.rolled_status.argtypes=[C.c_uint];hook.rolled_status.restype=C.c_uint64
                appearance_hooks={}
                try:
                    install(base,matches[0][4],entry=0x68d0868,prologue=bytes.fromhex('fd7bbfa9fd03009102600091e00301aa'),hook_name='appearance_serialize_hook',configure_name='configure_appearance_serialize')
                    appearance_hooks['serialize']='INSTALLED'
                except Exception as exc:
                    appearance_hooks['serialize']=str(exc)
                    appearance_error=(appearance_error+'; ' if appearance_error else '')+'serialize: '+str(exc)
                try:
                    install(base,matches[0][4],entry=0x68ceb44,prologue=bytes.fromhex('fd7bbaa9fc6f01a9fa6702a9f85f03a9'),hook_name='appearance_build_hook',configure_name='configure_appearance_build')
                    appearance_hooks['build']='INSTALLED'
                except Exception as exc:
                    appearance_hooks['build']=str(exc)
                    appearance_error=(appearance_error+'; ' if appearance_error else '')+'build: '+str(exc)
                try:
                    install(base,matches[0][4],entry=0x68db150,prologue=bytes.fromhex('800000b4080040f9032d40f960001fd6'),hook_name='appearance_entity_hook',configure_name='configure_appearance_entity')
                    appearance_hooks['entity']='INSTALLED'
                except Exception as exc:
                    appearance_hooks['entity']=str(exc)
                    appearance_error=(appearance_error+'; ' if appearance_error else '')+'entity: '+str(exc)
                try:
                    install(base,matches[0][4],entry=0x3a0b28c,prologue=bytes.fromhex('fd7bbaa9fc6f01a9fa6702a9f85f03a9'),hook_name='appearance_shirt_hook',configure_name='configure_appearance_shirt')
                    appearance_hooks['shirt']='INSTALLED'
                except Exception as exc:
                    appearance_hooks['shirt']=str(exc)
                    appearance_error=(appearance_error+'; ' if appearance_error else '')+'shirt: '+str(exc)
                hook.appearance_card_status.argtypes=[C.c_uint];hook.appearance_card_status.restype=C.c_uint64
                hook.appearance_shirt_status.argtypes=[C.c_uint];hook.appearance_shirt_status.restype=C.c_uint64
                hook.appearance_seen.argtypes=[C.c_uint,C.c_uint];hook.appearance_seen.restype=C.c_uint64
                shirt_fields=['appearance_shirt_calls','appearance_shirt_matches','appearance_shirt_alias_matches','appearance_shirt_applies','appearance_last_shirt_id','appearance_shirt_before','appearance_shirt_after']
                hook.appearance_status.argtypes=[];hook.appearance_status.restype=C.c_uint
                hook.appearance_diagnostic.argtypes=[C.c_uint];hook.appearance_diagnostic.restype=C.c_uint64
                appearance_fields=['appearance_serialize_calls','appearance_build_calls','appearance_build_matches','appearance_entity_calls','appearance_entity_matches','appearance_last_build_id','appearance_last_entity_id','appearance_build_before','appearance_entity_before']
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
                if appearance_error or editor_error or skill_text_error or presentation_error:raise RuntimeError('Mod initialization incomplete: '+str(appearance_error or editor_error or skill_text_error or presentation_error))
                _ready.set()
                diagnostic('HOOK_INSTALLED_MENU_NOT_YET_VERIFIED' ,presentation_error=presentation_error,appearance_error=appearance_error)
                rules=list(settings['leagues']);rule_ids=['122','566','128','125','549','473'];native_ids=list(settings['native_rosters']);rule_count=len(rule_ids);native_count=len(native_ids)
                previous = None
                while True:
                    stats = tuple(hook.status(i) for i in range(3+2*rule_count))+tuple(hook.native_status(i) for i in range(native_count+4))+tuple(hook.environment_status(i) for i in range(3))+(hook.cached_status(),hook.name_status(),hook.appearance_status())+tuple(hook.appearance_diagnostic(i) for i in range(9))+tuple(hook.appearance_shirt_status(i) for i in range(7))+tuple(hook.appearance_card_status(i) for i in range(8))+tuple(hook.editor_status(i) for i in range(5))+tuple(hook.codec_status(i)for i in range(3))
                    if stats != previous:
                        diagnostic('HOOK_ACTIVE',cut_sleeve_status={k:hook.editor_cut_status(i)for i,k in enumerate(['ready','profiles','applies','unsupported','last_card'])},motion_status={k:hook.editor_motion_status(i)for i,k in enumerate(['ready','profiles','applies','failures','last_card','last_source'])},accessory_vector_status={k:hook.editor_gear_detail_status(i)for i,k in enumerate(['calls','rejected','appended','last_count','left_enabled','right_enabled'])},accessory_packed_status={k:hook.editor_gear_status(i)for i,k in enumerate(['applies','last_card'])},copy_model_status={k:hook.editor_copy_status(i)for i,k in enumerate(['ready','profiles','applies','failures'])},socks_status={k:hook.editor_socks_status(i)for i,k in enumerate(['ready','profiles','applies'])},skin_palette_status={k:hook.skin_status(i)for i,k in enumerate(['ready','profiles','applies','last_card_id','last_palette'])},player_model_status={k:hook.model_status(i)for i,k in enumerate(['ready','profiles','applies','scope_failures','final_float_applies','last_card_id','arm_before_float_bits','arm_after_float_bits'])},codec_errors=codec_errors,skill_text_error=skill_text_error,skill_text_fallbacks=hook.skill_text_status(),codec_status={name:hook.codec_status(i)for i,name in enumerate(['uniform_layouts','coach_resources','coach_native_views'])},rolled_hooks=rolled_hooks,rolled_error=rolled_error,rolled_state={name:hook.rolled_status(i) for i,name in enumerate(['enabled','detail_applies','common_applies','last_card_id','last_kit','last_source_model','last_variant'])},editor_team_results={str(tid):hook.editor_team_status(tid) for tid in editor_team_ids},editor_error=editor_error,editor_status={'ready':hook.editor_status(0),'player_applies':hook.editor_status(1),'team_applies':hook.editor_status(2),'failures':hook.editor_status(3),'last_error_id':hook.editor_status(4)},appearance_trial_error=trial_error,appearance_trial_enabled=bool(hook.appearance_card_status(7)),appearance_policy_matches={'Y17':hook.appearance_card_status(4),'UEFA':hook.appearance_card_status(5),'rolled_trial':hook.appearance_card_status(6)},appearance_build_matches_by_id={'89138556572074':hook.appearance_card_status(0),'88044950524330':hook.appearance_card_status(1)},appearance_last_applied_id=hook.appearance_card_status(2),appearance_build_after=hook.appearance_card_status(3),appearance_build_ids=sorted({hook.appearance_seen(0,i) for i in range(64)}-{0}),appearance_shirt_ids=sorted({hook.appearance_seen(1,i) for i in range(64)}-{0}),**{name:hook.appearance_shirt_status(i) for i,name in enumerate(shirt_fields)},appearance_hooks=appearance_hooks,**{name:hook.appearance_diagnostic(i) for i,name in enumerate(appearance_fields)},appearance_error=appearance_error,appearance_sleeve_applies=hook.appearance_status(),environment_error=environment_error,active_competition=hook.environment_status(0),selected_stadium=hook.environment_status(1),ovr_balance_failures=hook.environment_status(2),presentation_error=presentation_error,result=stats[0],patched_contexts=stats[1],menu_calls=stats[2],league_results={cid:hook.status(3+i)for i,cid in enumerate(rule_ids)},patched_leagues={cid:hook.status(3+rule_count+i)for i,cid in enumerate(rule_ids)},native_team_results={tid:hook.native_status(i)for i,tid in enumerate(native_ids)},native_player_applies=hook.native_status(native_count),native_last_player_error=hook.native_status(native_count+1),native_last_team_error=hook.native_status(native_count+2),native_last_player_reason=hook.native_status(native_count+3),native_last_player_full_id=hook.last_player_id(),cached_team_applies=hook.cached_status(),competition_name_applies=hook.name_status())
                        previous = stats
                    try:
                        import myleague_team_snapshot
                        import transfer_editor
                        transfer_editor.preload(hook)
                        myleague_team_snapshot.export(hook)
                    except Exception as exc:
                        (HERE/'myleague-snapshot-error.txt').write_text(str(exc))
                    time.sleep(10)
            time.sleep(2)
        raise RuntimeError('libUE4.so not loaded in this Python process')
    except Exception as exc:
        _ready.clear()
        diagnostic('INSTALL_FAILED',error=str(exc))
        try:
            import mod_startup
            mod_startup.record_error('league-worker',exc)
        except Exception:pass


def start():
    global _started
    if not _started:
        _started = True
        threading.Thread(target=worker,name='MyLeagueMenuFix',daemon=True).start()

def editor_context():
    return int(_native_handle.environment_status(0)) if _native_handle is not None else 0


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
