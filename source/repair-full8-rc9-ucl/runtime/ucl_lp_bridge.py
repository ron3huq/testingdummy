"""Isolated adapter to the installed APK73 native My League prepare/start API.

No process-wide monkey patch of state/save; use private function globals and one
SQLite transaction for packet construction + season/session writes. UI routing
and native aggregate setup still require installation by the entry adapter.
"""
import copy,types,inspect
from ucl_lp_mode import Store,UclError,own_match,session_key,needs_decision,apply

class NativeAbort(UclError):pass

class ConnectionView:
    """Existing native helpers can query/write; only the outer UCL layer commits."""
    def __init__(self,conn):self._conn=conn
    def __getattr__(self,name):return getattr(self._conn,name)
    def execute(self,*args,**kwargs):
        # Native functions use begin/commit methods. Reject raw transaction SQL.
        if args and args[0].lstrip().split(None,1)[0].upper()in{'BEGIN','COMMIT','ROLLBACK','SAVEPOINT','RELEASE','END'}:raise NativeAbort('unexpected nested native transaction SQL')
        return self._conn.execute(*args,**kwargs)
    def commit(self):pass
    def rollback(self):raise NativeAbort('native preparation rejected the request')
    def close(self):raise NativeAbort('native helper attempted to close the save')

class MetaView:
    def __init__(self,source):self._source=source
    def __getattr__(self,name):return getattr(self._source,name)
    def set_season_points(self,conn,value):pass  # UCL does not alter normal My League balance.
    @staticmethod
    def key(key):
        if key.startswith('my_league_'):return 'ucl_lp_native_'+key[len('my_league_'):]
        raise NativeAbort('unsupported native metadata access: '+str(key))
    def get_meta(self,conn,key,*args):return self._source.get_meta(conn,self.key(key)if key.startswith('my_league_')else key,*args)
    def set_meta(self,conn,key,*args):return self._source.set_meta(conn,self.key(key),*args)

class Bridge:
    def __init__(self,conn,league,team_ready,uniforms,aggregate_setup=None):
        self.store=Store(conn);self.league=league;self.team_ready=team_ready;self.uniforms=uniforms;self.aggregate_setup=aggregate_setup
    def projection(self,state):
        match=own_match(state)
        if match is None:raise UclError('no playable UCL fixture')
        old=state.get('active')
        if old:
            if old['fixture']!=match['id']:raise UclError('pending native fixture mismatch')
            return copy.deepcopy(old['native']['projection'])
        from ucl_lp_view import projection
        return projection(state)
    def function(self,name,projection):
        original=inspect.unwrap(getattr(self.league,name))
        if not isinstance(original,types.FunctionType)or not original.__code__.co_filename.replace('\\','/').endswith('/my_league.py'):raise UclError('unsupported native My League function: '+name)
        namespace=dict(original.__globals__);namespace['store']=MetaView(namespace['store']);namespace['begin']=lambda conn:None;namespace['state']=lambda conn:projection
        def save(conn,value):
            if value is not projection:raise NativeAbort('native helper replaced isolated season projection')
        namespace['save']=save
        def current(value):
            fixture=value['schedule_v2'][value['fixture']-1];match=next(m for m in fixture['match_list']if value['team_id']in(m['home_team_id'],m['away_team_id']))
            return fixture,match,'HOME'if match['home_team_id']==value['team_id']else'AWAY'
        namespace['current']=current
        namespace['fixtures']=lambda value:value['schedule_v2']
        namespace['ranking']=lambda value:copy.deepcopy(value['_ucl_view']['ranking'])
        namespace['player_ranking']=lambda value,kind:copy.deepcopy(value['_ucl_view'][kind])
        # Match the verified RC7 native-roster path, not substitute-card squads.
        namespace['_opponent_squad']=lambda conn,team:None
        namespace['match_club_team']=lambda conn,req:projection['team_id']
        namespace['my_league_home_uniforms']=lambda conn,req:self.uniforms(projection['team_id'])
        saved=namespace.get('player_match_stats')
        if saved is not None:
            class LineupView:
                def __getattr__(self,key):return getattr(saved,key)
                def remember_lineup(self,conn,game,players):projection['ucl_lineup']=copy.deepcopy(players)
                def record(self,*args,**kwargs):return dict(games=0,goal=0,assist=0)
            namespace['player_match_stats']=LineupView()
        if name in('start','finish'):
            helper=inspect.unwrap(namespace['match_squad'])
            if not isinstance(helper,types.FunctionType)or not helper.__code__.co_filename.replace('\\','/').endswith('/my_league.py'):raise UclError('unsupported native squad binding')
            namespace['match_squad']=types.FunctionType(helper.__code__,namespace,helper.__name__,helper.__defaults__,helper.__closure__)
        if name=='enter_view':namespace['own_special']=lambda conn,template,team:copy.deepcopy(template)
        if name=='save_special':
            helper=inspect.unwrap(namespace['own_special'])
            namespace['own_special']=types.FunctionType(helper.__code__,namespace,helper.__name__,helper.__defaults__,helper.__closure__)
        if name=='finish':
            namespace['_cpu_round_stats']=lambda *args,**kwargs:[]
            predicted=projection['_ucl_predicted']
            def cpu_score(value,home,away):
                match=next(m for m in predicted['matches']if m['home']==home and m['away']==away and m['stage']==projection['_ucl_stage']and m['round']==projection['_ucl_round'])
                return match['result']['home'],match['result']['away']
            namespace['cpu_score']=cpu_score
            result=projection['_ucl_result'];native_result=namespace['vscom_result'];namespace['_scores']=lambda request:(result['home'],result['away'])
            class ResultView:
                def __getattr__(self,key):return getattr(native_result,key)
                def outcome(self,request,side,home,away):
                    if result.get('pk_home')is None:return native_result.outcome(request,side,home,away)
                    ours,theirs=(result['pk_away'],result['pk_home'])if side=='AWAY'else(result['pk_home'],result['pk_away'])
                    return 'WIN'if ours>theirs else'LOSE'
            namespace['vscom_result']=ResultView()
            for helper_name in ('_season_events','_translate_opponent_events'):
                helper=inspect.unwrap(namespace[helper_name])
                namespace[helper_name]=types.FunctionType(helper.__code__,namespace,helper.__name__,helper.__defaults__,helper.__closure__)
        cloned=types.FunctionType(original.__code__,namespace,original.__name__,original.__defaults__,original.__closure__);cloned.__kwdefaults__=original.__kwdefaults__
        return cloned
    @staticmethod
    def check(reply):
        if not isinstance(reply,dict)or reply.get('result')!='NOERR':raise NativeAbort('native My League API did not return a valid packet')
        return reply
    def prepare(self,request):
        with self.store.transaction():
            state=self.store.get()
            if state is None:raise UclError('no UCL season selected')
            match=own_match(state)
            if match is None:raise UclError('no playable fixture')
            opponent=match['away']if match['home']==state['own']else match['home']
            pending=state.get('active')
            if pending:
                if pending['fixture']!=match['id']:raise UclError('pending native fixture mismatch')
                frozen=pending['native']['projection']['active']['opponent']
                if request.get('cpu_level')not in(None,frozen.get('cpu_level')):raise UclError('pending fixture difficulty is frozen')
                reply=copy.deepcopy(frozen);reply.update(rqid=request.get('rqid'),msgid=request.get('msgid','CMD_GET_VSCOM_OPPONENT'),result='NOERR');return reply
            if self.team_ready(opponent)!=1:raise UclError('native opponent roster is not ready')
            projection=self.projection(state);view=ConnectionView(self.store.conn);reply=self.check(self.function('prepare',projection)(view,request))
            active=projection.get('active')
            if not isinstance(active,dict)or session_key(reply.get('game_id'))!=session_key(active.get('game_id')):raise NativeAbort('native packet/session mismatch')
            actual=(active.get('opponent')or{}).get('team_data',{}).get('base_team_id')
            if actual!=opponent:raise NativeAbort('native opponent identity mismatch')
            from ucl_lp_match_plan import build
            self.store._reserve_locked(session_key(active['game_id']),dict(projection=projection,match_plan=build(state,match)))
            return reply
    def home_references(self,request):
        state=self.store.get()
        if state is None:raise UclError('no UCL season selected')
        saved=self.function('match_squad',self.projection(state))(ConnectionView(self.store.conn),request)
        refs=request.get('player_list_home')or saved.get('player_list')
        if refs:return copy.deepcopy(refs)
        source=inspect.unwrap(self.league.start).__globals__['store']
        return[copy.deepcopy(p['gameplayer_id'])for p in source.entry_roster(self.store.conn)[:23]]
    def start(self,response,request,home_entries):
        with self.store.transaction():
            state=self.store.get();active=state.get('active')if state else None
            if not active or session_key(request.get('game_id'))!=session_key(active['game_id']):raise UclError('native start does not match reserved UCL session')
            cache=active['native'].get('start_packet')
            if cache is not None:
                reply=self.check(copy.deepcopy(cache))
                if session_key(reply.get('game_id'))!=session_key(active['game_id']):raise NativeAbort('cached start packet/session mismatch')
                reply['rqid']=request.get('rqid');return reply
            match=own_match(state)
            from ucl_lp_match_plan import build
            frozen=active['native'].get('match_plan')
            if frozen is not None and frozen!=build(state,match):raise UclError('reserved aggregate match plan changed')
            # A two-leg return match MUST have a verified aggregate-aware setup.
            # No silent downgrade to isolated-leg extra time or simulated PK.
            if needs_decision(state,match) and self.aggregate_setup is None:raise UclError('native aggregate setup is not installed')
            projection=self.projection(state);reply=self.check(self.function('start',projection)(ConnectionView(self.store.conn),response,request,home_entries))
            if self.aggregate_setup is not None:self.aggregate_setup(state,match,reply)
            if session_key(reply.get('game_id'))!=session_key(active['game_id']):raise NativeAbort('native start packet/session mismatch')
            active['native']['projection']=projection;active['native']['start_packet']=copy.deepcopy(reply);self.store.save(state);self.store._start_locked(session_key(active['game_id']));return reply
    def info(self,response,request):
        from ucl_lp_view import projection
        state=self.store.get()
        if state is None:raise UclError('no UCL season selected')
        return self.check(self.function('info',projection(state))(ConnectionView(self.store.conn),response,request))
    def enter(self,request):
        from ucl_lp_view import projection
        state=self.store.get()
        if state is None:raise UclError('no UCL season selected')
        value=projection(state)
        return self.check(self.function('enter_view',value)(ConnectionView(self.store.conn),value,request))
    def special(self,request):
        with self.store.transaction():
            state=self.store.get()
            if state is None:raise UclError('no UCL season selected')
            return self.check(self.function('save_special',self.projection(state))(ConnectionView(self.store.conn),request))
    def schedule(self,response,request):
        from ucl_lp_view import projection
        state=self.store.get()
        if state is None:raise UclError('no UCL season selected')
        return self.function('get_schedule',projection(state))(ConnectionView(self.store.conn),response,request)
    def finish(self,request,response=None,player_events=None):
        from ucl_lp_result import game_id,decode
        from ucl_lp_view import rankings
        game=game_id(request)
        with self.store.transaction():
            row=self.store.conn.execute('SELECT season,fixture,started,receipt FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
            if not row or not row[2]:raise UclError('native match was not started')
            if row[3]is not None:
                import json
                reply=self.check(copy.deepcopy(json.loads(row[3])['reply']));reply['rqid']=request.get('rqid');return reply
            state=self.store.get(row[0]);match=own_match(state)
            if not match or match['id']!=row[1]:raise UclError('native finish fixture mismatch')
            result=decode(state,match,request);projection=self.projection(state);predicted=copy.deepcopy(state);apply(predicted,match['id'],result)
            projection['_ucl_result']=result;projection['_ucl_predicted']=predicted;projection['_ucl_stage']=match['stage'];projection['_ucl_round']=match['round'];projection['_ucl_view']['ranking']=rankings(predicted)
            reply=self.check(self.function('finish',projection)(ConnectionView(self.store.conn),response or{},request))
            end=reply.get('game_end_result',{}).get('extra_match_result',{}).get('season_match_result')
            if isinstance(end,dict):end.update(is_end_season='YES'if predicted.get('champion')or predicted.get('eliminated')else'NO',is_champion='YES'if predicted.get('champion')==state['own']else'NO',is_promote='NO',is_relegate='NO',next_compe_unit_id=122)
            self.store._finish_locked(game,result,reply,player_events)
            return reply
