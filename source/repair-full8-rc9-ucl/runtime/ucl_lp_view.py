"""Project isolated UCL season into APK73 My League's native response schema.
No original-season DB keys are read or written. Native client rendering untested.
"""
from collections import OrderedDict
from ucl_lp_mode import table,UclError
from ucl_lp_stats import leaderboard

def rankings(state):
    rows=[]
    for row in table(state):
        draws=row['points']-3*row['wins']
        rows.append(dict(rank=row['rank'],pre_rank=row['rank'],team_id=row['team_id'],winning_points=row['points'],wins=row['wins'],losses=row['played']-row['wins']-draws,draws=draws,goals=row['gf'],goals_against=row['ga'],diff=row['gd']))
    return rows

def player_rankings(state,kind):
    field={'goal':'goals','assist':'assists'}[kind]
    return[dict(rank=r['rank'],player_id=int(r['player_id']),team_id=r['team_id'],value=r[field],is_com='NO'if r['team_id']==state['own']else'YES')for r in leaderboard(state,field,20)['rows']]

def projection(state):
    rounds=OrderedDict()
    for m in state['matches']:rounds.setdefault((m['stage'],m['round']),[]).append(m)
    rows=[];played={};selected=None;last_own=None
    for index,((stage,day),matches)in enumerate(rounds.items(),1):
        row=dict(fixture=index,match_list=[dict(home_team_id=m['home'],away_team_id=m['away'])for m in matches]);rows.append(row)
        own=next((m for m in matches if state['own']in(m['home'],m['away'])),None)
        if own:last_own=index
        if(stage,day)==(state['stage'],state['round'])and own:selected=index
        if own and all(m.get('result')is not None for m in matches):
            r=own['result'];ours,theirs=(r['home'],r['away'])if own['home']==state['own']else(r['away'],r['home'])
            decision_ours,decision_theirs=(r.get('pk_home'),r.get('pk_away'))if own['home']==state['own']else(r.get('pk_away'),r.get('pk_home'))
            outcome='WIN'if ours>theirs else'LOSE'if ours<theirs else('WIN'if decision_ours>decision_theirs else'LOSE')if decision_ours is not None else'DRAW'
            played[str(index)]=dict(result=outcome,matches=[dict(home_team_id=m['home'],away_team_id=m['away'],home_goals=m['result']['home'],away_goals=m['result']['away'])for m in matches])
    if not last_own:raise UclError('selected club is missing from UCL fixtures')
    return dict(team_id=state['own'],competition_id=122,fixture=selected or last_own,completed=bool(state.get('eliminated')or state.get('champion')),cpu_level=state['cpu_level'],active=None,played=played,schedule_v2=rows,_ucl_view=dict(ranking=rankings(state),goal=player_rankings(state,'goal'),assist=player_rankings(state,'assist')))
