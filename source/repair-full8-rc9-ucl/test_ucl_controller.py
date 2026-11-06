"""Check explicit mode selection and passthrough for unrelated saves/matches."""
import sqlite3,json,types,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_controller import Controller,PASS
from ucl_lp_mode import UclError,own_match

def run():
    conn=sqlite3.connect(':memory:');conn.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');conn.execute('INSERT INTO meta VALUES(?,?)',('my_league_state_v1','normal-sentinel'));conn.commit()
    calls=[]
    bridge=types.SimpleNamespace(aggregate_setup=None,league=types.SimpleNamespace(is_season=lambda r:r.get('match_category')=='MYLEAGUE'),info=lambda p,r:dict(result='NOERR',source='UCL'),finish=lambda r,p:calls.append(r)or dict(result='NOERR'))
    c=Controller(conn,lambda:bridge);team=c.draws['teams'][0]['team_id'];c.manage(dict(op='create',team_id=team));before=copy.deepcopy(c.store.get())
    try:c.manage(dict(op='activate'))
    except UclError:pass
    else:raise AssertionError('unfinished aggregate setup enabled')
    assert not c.enabled()and c.store.get()==before
    assert c.route('CMD_GET_SEASON_INFO',{}, {})is PASS
    bridge.aggregate_setup=lambda *a:None;c.manage(dict(op='activate'));assert c.enabled();assert c.route('CMD_GET_SEASON_INFO',{}, {})['source']=='UCL'
    assert c.route('CMD_GET_VSCOM_OPPONENT',dict(match_category='EXHIBITION'),{})is PASS
    assert c.route('CMD_START_GAME',dict(game_id=123),{})is PASS
    assert c.route('CMD_GET_VSCOM_GAME_RESULT',dict(match_result=dict(game_id=123)),{})is PASS
    bridge.home_references=lambda req:[{'id':123,'serial':1}];bridge.start=lambda resp,req,entries:dict(result='NOERR',entries=entries)
    c.home_entries=lambda refs,log_substitutes:[{'gameplayer_id':r}for r in refs]
    c.store.reserve(123,{});c.store.start(123);assert c.route('CMD_START_GAME',{'game_id':123},{})['entries']==[{'gameplayer_id':{'id':123,'serial':1}}];c.route('CMD_GET_VSCOM_GAME_RESULT',dict(match_result=dict(game_id=123)),{});assert len(calls)==1
    try:c.manage(dict(op='leave'))
    except UclError:pass
    else:raise AssertionError('pending match abandoned')
    assert c.enabled()
    c.store.finish(123,dict(home=1,away=0));c.manage(dict(op='leave'));assert not c.enabled()
    try:c.manage(dict(op='create',team_id=team))
    except UclError:pass
    else:raise AssertionError('season replaced without explicit confirmation')
    assert conn.execute('SELECT value FROM meta WHERE key=?',('my_league_state_v1',)).fetchone()[0]=='normal-sentinel'
    print(json.dumps(dict(passed=True,normal_season_untouched=True,unrelated_match_passthrough=True,aggregate_readiness_gate=True,explicit_season_replace=True,pending_match_leave_guard=True,installed_in_game=False),indent=2))
if __name__=='__main__':run()
