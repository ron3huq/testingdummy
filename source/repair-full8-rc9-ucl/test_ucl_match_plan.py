"""Football boundary cases independent of a particular native hook offset."""
import json,sys,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import *
from ucl_lp_match_plan import build,at_whistle

def run():
    doc=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text());c=sqlite3.connect(':memory:');state=Store(c).create(doc['teams'],doc['draws'][0]['rounds'],4219,17)
    assert state['knockout_legs']==2
    add_ties(state,'QF',[(4219,114)],True);first,second=state['matches'][-2:]
    # First leg is PSG-Como, return leg Como-PSG. Carry must reverse home/away.
    first['result']=score(state,first,1,0);plan=build(state,second)
    assert(plan['carry_home'],plan['carry_away'])==(0,1)
    assert at_whistle(plan,1,0,'REGULATION')['action']=='EXTRA_TIME'
    assert at_whistle(plan,0,0,'REGULATION')['action']=='FINISH'
    assert at_whistle(plan,1,0,'EXTRA_TIME')['action']=='PENALTIES'
    assert at_whistle(plan,2,0,'EXTRA_TIME')['action']=='FINISH'
    # Equal match score can still have a non-tied aggregate; no ET in that case.
    first['result']=score(state,first,0,2);plan=build(state,second)
    assert at_whistle(plan,1,1,'REGULATION')['action']=='FINISH'
    # Different away-goal totals do not break an aggregate tie.
    first['result']=score(state,first,2,1);plan=build(state,second)
    assert at_whistle(plan,3,2,'REGULATION')['action']=='EXTRA_TIME'
    assert at_whistle(build(state,first),0,0,'REGULATION')['action']=='FINISH'
    assert at_whistle(plan,3,2,'REGULATION')['played_home']==3
    print(json.dumps(dict(passed=True,new_seasons_two_legs=True,carry_reverses_home_away=True,leg_win_aggregate_draw_requires_et=True,leg_draw_aggregate_win_no_et=True,no_away_goals_rule=True,played_scores_not_inflated=True,native_hook_integrated=False),indent=2))
if __name__=='__main__':run()
