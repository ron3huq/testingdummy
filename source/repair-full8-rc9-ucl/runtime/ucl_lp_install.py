"""Gateway entry wiring. Deliberately not invoked by the RC7 release bootstrap.
A launcher operation mapping and a verified aggregate provider are prerequisites.
"""
import copy,functools,json,types
from ucl_lp_controller import Controller,PASS,MODE_KEY
from ucl_lp_bridge import Bridge
from ucl_lp_mode import UclError
COMMANDS=frozenset({'CMD_SET_SEASON_ENTER','CMD_SET_MYCLUB_SPECIAL_DREAM_SQUAD_INFO','CMD_GET_SEASON_INFO','CMD_GET_SEASON_SCHEDULE','CMD_GET_VSCOM_OPPONENT','CMD_START_GAME','CMD_GET_VSCOM_GAME_RESULT'})

def install(module,aggregate_setup=None,bridge_factory=None):
    if getattr(module,'_ucl_lp_entry_installed',False):return False
    def factory(logic):
        if bridge_factory is not None:return bridge_factory(logic)
        import my_league,club_store,select_team_runtime as native
        def ready(team):
            native.configure_owned_players([r[0]for r in logic.conn.execute('SELECT DISTINCT id FROM gameplayers')]);native.activate_context(122);return native.ensure_native_team(team)
        return Bridge(logic.conn,my_league,ready,club_store.default_uniforms,aggregate_setup)
    def controller(logic):return Controller(logic.conn,lambda:factory(logic),home_entries=getattr(logic,'_home_entries',None))
    cls=type(module._logic);original_handle=cls.handle
    @functools.wraps(original_handle)
    def handle(logic,command,request):
        if logic is not module._logic or command not in COMMANDS:return original_handle(logic,command,request)
        selected=logic.conn.execute('SELECT value FROM meta WHERE key=?',(MODE_KEY,)).fetchone()
        if not selected:
            if command!='CMD_GET_VSCOM_GAME_RESULT':return original_handle(logic,command,request)
            exists=logic.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='ucl_lp_sessions'").fetchone()
            if not exists:return original_handle(logic,command,request)
        response=copy.deepcopy(getattr(logic,'responses',{}).get(command)or getattr(logic,'templates',{}).get(command)or{})
        try:reply=controller(logic).route(command,request,response)
        except UclError:
            # Native error response, not an exception/crash or fallback that writes
            # the normal season. No incomplete match is marked as finished.
            import my_league
            return my_league.fail(command,request)
        return original_handle(logic,command,request)if reply is PASS else reply
    original_manage=module.manage
    @functools.wraps(original_manage)
    def manage(action,payload=''):
        if action!='ui73_ucl':return original_manage(action,payload)
        request=json.loads(payload or'{}')
        if not isinstance(request,dict):raise UclError('invalid UCL request')
        return json.dumps(controller(module._logic).manage(request),ensure_ascii=False)
    cls.handle=handle;module.manage=manage;module._ucl_lp_entry_installed=True
    return True
