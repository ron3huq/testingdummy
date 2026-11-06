"""Execute ONLY selected installed native function code under controlled bindings.
Usage: python test_ucl_bridge_native_api.py /path/to/verified/my_league.pyc
No application module top-level code is executed/copied into the UCL runtime.
Fixtures emulate native data services, not the engine. Phone test still required.
"""
import marshal,types,sys,sqlite3,copy,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import Store,UclError,own_match,add_ties
from ucl_lp_bridge import Bridge,NativeAbort

def run(path):
    data=Path(path).read_bytes();module_code=marshal.loads(data[16:]);codes={v.co_name:v for v in module_code.co_consts if isinstance(v,types.CodeType)}
    assert {'prepare','start','valid_kit_binding'}<=set(codes)
    conn=sqlite3.connect(':memory:');conn.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');conn.executemany('INSERT INTO meta VALUES(?,?)',[('my_league_state_v1','NORMAL-LEAGUE-SENTINEL'),('my_league_sequence','777'),('my_league_special_squad_v1','{"squad_data":{"squad_gameplan":"NORMAL-SPECIAL"}}')]);conn.commit()
    class Meta:
        UNIFORM_STRIDE=16384
        @staticmethod
        def get_meta(c,k,default=''):
            r=c.execute('SELECT value FROM meta WHERE key=?',(k,)).fetchone();return r[0]if r else default
        @staticmethod
        def set_meta(c,k,v):c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',(k,v))
        @staticmethod
        def log_event(*args,**kwargs):pass
        @staticmethod
        def default_uniforms(team):return[(team<<14),(team<<14)|1]
    namespace=dict(copy=copy,json=json,SQUAD_KEY='my_league_special_squad_v1',NATIVE_LEVELS=['NORMAL'],match_club=lambda c,r:{'squad_data':{'squad_gameplan':'UCL-OWNED-PLAN'}},time=types.SimpleNamespace(time=lambda:1000),store=Meta,LEVELS={'NORMAL'},fail=lambda cmd,req:dict(result='ERROR',msgid=cmd),match_squad=lambda c,r:{},owned_coaches=types.SimpleNamespace(resolve=lambda *a:None),player_match_stats=types.SimpleNamespace(remember_lineup=lambda *a:(_ for _ in()).throw(AssertionError('normal lineup write leaked'))))
    namespace['ziru_data']=types.SimpleNamespace(ml_get_vscom_opponent=lambda:dict(team_data={},player_list=[],squad_data={}),team_label=lambda team:'Team '+str(team),team_names=lambda:{},ml_game_result=lambda:dict(game_end_result=dict(match_result={},extra_match_result=dict(season_match_result={}))),season_enter=lambda:{},ml_start_game=lambda:dict(squad_data_home={},squad_data_away={},uniform_list_home={},uniform_list_away={},commentary_info={'first_match_player_list':[]}))
    Meta.season_points=staticmethod(lambda c:73)
    Meta.entry_roster=staticmethod(lambda c:[dict(gameplayer_id=dict(id=123,serial=1))])
    namespace['match_squad']=types.FunctionType(codes['match_squad'],namespace)
    namespace['result_key']=types.FunctionType(codes['result_key'],namespace)
    for helper in ['_season_events','_translate_opponent_events']:namespace[helper]=types.FunctionType(codes[helper],namespace)
    namespace['vscom_result']=types.SimpleNamespace(gave_up=lambda req:False,outcome=lambda req,side,h,a:'DRAW'if h==a else'WIN'if(h>a)==(side!='AWAY')else'LOSE',result_fields=lambda req,h,a,result:dict(game_res=result,gameend_reason='NORMAL_END',abnormalend_reason='NOERR',score_data=dict(home_score=h,away_score=a)))
    namespace['valid_kit_binding']=types.FunctionType(codes['valid_kit_binding'],namespace)
    league=types.SimpleNamespace(**{name:types.FunctionType(codes[name],namespace)for name in ['prepare','start','info','finish','enter_view','get_schedule','match_squad']})
    doc=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text());store=Store(conn);season=store.create(doc['teams'],doc['draws'][0]['rounds'],doc['teams'][0]['team_id'],0,knockout_legs=2);match=own_match(season);bridge=Bridge(conn,league,lambda team:1,Meta.default_uniforms)
    info=bridge.info(dict(msgid='CMD_GET_LEAGUE_SEASON_INFO'),dict(rqid=0));assert len(info['ranking'])==36 and len(info['auto_match_list'])==18;assert info['team_id']==season['own']
    prepared=bridge.prepare(dict(rqid=1));assert prepared['result']=='NOERR';gid=prepared['game_id'];assert store.get()['active']['game_id']==str(gid);assert prepared['side']==('AWAY'if match['home']==season['own']else'HOME')
    frozen=copy.deepcopy(store.get());assert bridge.prepare(dict(rqid=2))['game_id']==gid;assert store.get()==frozen
    try:bridge.prepare(dict(rqid=2,cpu_level='HARD'))
    except UclError:pass
    else:raise AssertionError('pending difficulty changed')
    assert store.get()==frozen
    # Native rollback must undo both native sequence allocation and UCL state.
    try:bridge.start({},dict(game_id=gid,rqid=3),[])
    except NativeAbort:pass
    else:raise AssertionError('empty native playing lineup accepted')
    assert store.get()==frozen;assert conn.execute('SELECT started FROM ucl_lp_sessions').fetchone()[0]==0
    assert bridge.home_references({})==[dict(id=123,serial=1)]
    entries=[dict(gameplayer_id=dict(id=123,serial=1))];started=bridge.start({},dict(game_id=gid,rqid=4),entries);assert started['squad_data_home']['player_list']==entries;assert started['squad_data_home']['team_id']==season['own'];assert started['squad_data_home']['squad_gameplan']=='UCL-OWNED-PLAN';assert conn.execute('SELECT started FROM ucl_lp_sessions').fetchone()[0]==1
    # Durable start reply ignores changed retry lineups/kit data except rqid.
    snapshot=copy.deepcopy(store.get());repeat=bridge.start({},dict(game_id=gid,rqid=5),[dict(gameplayer_id=dict(id=999,serial=2))]);assert repeat['squad_data_home']['player_list']==entries and repeat['rqid']==5;assert store.get()==snapshot
    assert Meta.get_meta(conn,'my_league_state_v1')=='NORMAL-LEAGUE-SENTINEL'and Meta.get_meta(conn,'my_league_sequence')=='777';assert Meta.get_meta(conn,'ucl_lp_native_sequence')==str(gid)
    # No global replacement of the installed module's original globals.
    assert namespace.get('state')is None and namespace.get('begin')is None
    request=dict(match_result=dict(game_id=gid,pk_flag='NO'),score=[dict(score_1st=99 if match['home']==season['own']else 0,score_2nd=0),dict(score_1st=99 if match['away']==season['own']else 0,score_2nd=0)]);bridge.finish(request);assert store.get()['active']is None;assert Meta.get_meta(conn,'my_league_state_v1')=='NORMAL-LEAGUE-SENTINEL'
    for day in range(2,9):
        current=store.get();fixture=own_match(current);prepared=bridge.prepare(dict(rqid=day*10));bridge.start({},dict(game_id=prepared['game_id']),entries)
        request=dict(match_result=dict(game_id=prepared['game_id'],pk_flag='NO'),score=[dict(score_1st=99 if fixture['home']==current['own']else 0,score_2nd=0),dict(score_1st=99 if fixture['away']==current['own']else 0,score_2nd=0)])
        reply=bridge.finish(request);assert reply['game_end_result']['extra_match_result']['season_match_result']['is_end_season']=='NO'
        assert bridge.finish(dict(match_result=dict(game_id=prepared['game_id']),rqid=day*10+1))['rqid']==day*10+1
    current=store.get();assert current['stage']=='R16'and len(current['matches'])>144
    view=bridge.info({},{});assert len(view['ranking'])==36 and view['fixture']==11 and view['is_end_season']=='NO'
    schedule=bridge.schedule({},{});assert len(schedule['schedule_list'])==12
    assert bridge.enter({})['league_compe_unit_id']==122
    # A missing aggregate setup blocks a return leg/final, never fakes a result.
    state=store.get();a,b=doc['teams'][0]['team_id'],doc['teams'][1]['team_id'];state['own']=a;state['active']=None;add_ties(state,'PLAYOFFS',[(a,b)],True);state['matches'][-2]['result']=dict(home=1,away=0);state['round']=2
    with store.transaction():store.save(state)
    prepared=bridge.prepare(dict(rqid=6));before=copy.deepcopy(store.get())
    try:bridge.start({},dict(game_id=prepared['game_id']),entries)
    except UclError as e:assert 'aggregate'in str(e)
    else:raise AssertionError('unverified aggregate setup bypassed')
    assert store.get()==before
    print(json.dumps(dict(passed=True,actual_prepare_start_info_finish_schedule_enter_executed=True,eight_native_result_rounds_to_R16=True,end_season_not_sent_after_league_phase=True,native_36_row_ranking_response=True,normal_special_squad_not_read=True,native_input_sha256=hashlib.sha256(data).hexdigest(),normal_league_save_unchanged=True,rollback_atomic=True,resume_start_packet_frozen=True,global_functions_unchanged=True,missing_aggregate_provider_blocks_return_leg=True,game_ui_hooks_installed=False,phone_verified=False),indent=2))
if __name__=='__main__':run(sys.argv[1])
