"""Exact per-fixture requirements for a future aggregate-aware engine binding.
Carry is private match setup data; never added to the saved played-leg score.
This is not an engine hook, and must not be advertised as one.
"""
from ucl_lp_mode import UclError,aggregate_before,needs_decision,number

def build(state,fixture):
    if fixture.get('leg')not in(1,2):raise UclError('invalid fixture leg')
    carry=aggregate_before(state,fixture)if fixture['leg']==2 else(0,0)
    return dict(fixture_id=fixture['id'],home=fixture['home'],away=fixture['away'],carry_home=carry[0],carry_away=carry[1],deciding=needs_decision(state,fixture),away_goals_rule=False)

def at_whistle(plan,home,away,period):
    if period not in('REGULATION','EXTRA_TIME'):raise UclError('unsupported match period')
    h,a=number(home),number(away)
    if period=='EXTRA_TIME'and not plan['deciding']:raise UclError('extra time not permitted')
    aggregate=(h+plan['carry_home'],a+plan['carry_away'])
    tied=aggregate[0]==aggregate[1]
    action='EXTRA_TIME'if plan['deciding']and tied and period=='REGULATION'else'PENALTIES'if plan['deciding']and tied else'FINISH'
    return dict(action=action,aggregate_home=aggregate[0],aggregate_away=aggregate[1],played_home=h,played_away=a)
