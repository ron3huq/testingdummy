"""Atomic native-attribution contract tests; no claim of game/UI integration."""
from pathlib import Path
import sys,json,sqlite3,tempfile,copy
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import Store,own_match,UclError
from ucl_lp_stats import record,leaderboard,StatsError,player_key

def run():
    doc=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text())
    with tempfile.TemporaryDirectory()as folder:
        path=Path(folder)/'season.sqlite';conn=sqlite3.connect(path);store=Store(conn);state=store.create(doc['teams'],doc['draws'][0]['rounds'],doc['teams'][0]['team_id'],0);fixture=own_match(state);home,away=fixture['home'],fixture['away'];p='9007199254740993';q='9007199254740995';r='9007199254740997';rosters={str(home):[p,q],str(away):[r]}
        store.reserve('9007199254740999',{'ucl_rosters':rosters});store.start('9007199254740999');before=conn.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]
        bad=[dict(team_id=home,scorer=p,assist=r)]
        try:store.finish('9007199254740999',dict(home=1,away=0),player_events=bad)
        except StatsError:pass
        else:raise AssertionError('opponent assist accepted')
        assert conn.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]==before
        assert conn.execute('SELECT receipt FROM ucl_lp_sessions').fetchone()[0]is None
        # An own goal counts toward the opponent's match score but is not a scorer award.
        events=[dict(team_id=home,scorer=p,assist=q),dict(team_id=away,scorer=r,own_goal=True)]
        receipt=store.finish('9007199254740999',dict(home=2,away=0),player_events=events);state=store.get();board=leaderboard(state);assert board['rows'][0]['player_id']==p and board['rows'][0]['goals']==1;assert leaderboard(state,'assists')['rows'][0]['player_id']==q;assert board['attributed_matches']==1 and board['completed_matches']==18 and not board['coverage_complete'];snapshot=json.dumps(state,sort_keys=True);conn.close()
        conn=sqlite3.connect(path);store=Store(conn);assert store.finish('9007199254740999',dict(home=99,away=0),player_events=[])==receipt;assert json.dumps(store.get(),sort_keys=True)==snapshot;conn.close()
    # Reject malformed or conflicting events before mutating leaderboard state.
    s=dict(matches=[dict(fixture,result=dict(home=2,away=0))]);record(s,fixture,dict(home=2,away=0),rosters,events);before=copy.deepcopy(s);assert record(s,fixture,dict(home=2,away=0),rosters,events)is False;assert s==before
    for event_list in [[],[dict(team_id=home,scorer='999')],[dict(team_id=home,scorer=p,assist=p)]]:
        try:record(s,fixture,dict(home=2,away=0),rosters,event_list)
        except StatsError:pass
        else:raise AssertionError('invalid events accepted')
        assert s==before
    for value in [True,1.0,'01','9e3',0,2**63]:
        try:player_key(value)
        except StatsError:pass
        else:raise AssertionError('lossy player ID accepted')
    print(json.dumps(dict(passed=True,atomic_result_stats_receipt=True,restart_duplicate_no_double_count=True,own_goal_attribution=True,reserved_roster_validation=True,exact_large_player_ids=True,partial_coverage_explicit=True,native_adapter_integrated=False),indent=2))
if __name__=='__main__':run()
