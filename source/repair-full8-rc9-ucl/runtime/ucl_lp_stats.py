"""Season-local scorer/assist records from adapter-resolved events.

Not a native packet decoder: the future native adapter must resolve player and
team identity against the original reserved roster before calling this module.
CPU goals without attributed events remain explicitly unattributed.
"""
from collections import Counter

class StatsError(ValueError):pass

def player_key(value):
    # Keep card/instance identifiers exact through JSON/WebView (>2**53).
    if type(value)is int:value=str(value)
    if not isinstance(value,str)or not value.isascii()or not value.isdecimal()or not 0<int(value)<2**63 or str(int(value))!=value:raise StatsError('invalid player identity')
    return value

def record(state,fixture,result,rosters,events):
    if not isinstance(events,list):raise StatsError('goal events must be a list')
    teams=(fixture['home'],fixture['away']);eligible={}
    if set(rosters)!={str(t)for t in teams}:raise StatsError('rosters must identify both fixture teams')
    for team in teams:
        rows=rosters[str(team)]
        if not isinstance(rows,list)or not rows:raise StatsError('missing reserved roster')
        keys=[player_key(v)for v in rows]
        if len(keys)!=len(set(keys)):raise StatsError('duplicate roster identity')
        eligible[team]=set(keys)
    if eligible[teams[0]]&eligible[teams[1]]:raise StatsError('ambiguous player identity across teams')
    goals=Counter();changes=Counter();normalized=[]
    for event in events:
        if not isinstance(event,dict)or set(event)-{'team_id','scorer','assist','own_goal'}:raise StatsError('invalid goal event')
        team=event.get('team_id');own=event.get('own_goal',False)
        if type(team)is not int or team not in teams or type(own)is not bool:raise StatsError('invalid event team or own-goal flag')
        scorer=player_key(event.get('scorer'));assist=event.get('assist')
        scoring_team=teams[1]if own and team==teams[0]else teams[0]if own else team
        if scorer not in eligible[team]:raise StatsError('scorer not in original reserved roster')
        if assist is not None:
            assist=player_key(assist)
            if own or assist==scorer or assist not in eligible[team]:raise StatsError('invalid assist attribution')
        goals[scoring_team]+=1
        if not own:changes[(team,scorer,'goals')]+=1
        if assist is not None:changes[(team,assist,'assists')]+=1
        normalized.append(dict(team_id=team,scorer=scorer,assist=assist,own_goal=own))
    if goals[teams[0]]!=result['home']or goals[teams[1]]!=result['away']:raise StatsError('event goals disagree with native regulation/extra-time score')
    # Caller includes this in the SAME transaction as the match receipt.
    stats=state.setdefault('stats',{});receipts=stats.setdefault('attributed_fixtures',{})
    old=receipts.get(fixture['id'])
    if old is not None:
        if old!=normalized:raise StatsError('conflicting event replay')
        return False
    players=stats.setdefault('players',{})
    for (team,player,kind),count in changes.items():
        key=str(team)+':'+player;row=players.setdefault(key,dict(team_id=team,player_id=player,goals=0,assists=0));row[kind]+=count
    receipts[fixture['id']]=normalized
    return True

def leaderboard(state,kind='goals',limit=100):
    if kind not in('goals','assists')or type(limit)is not int or not 1<=limit<=1000:raise StatsError('invalid leaderboard query')
    stats=state.get('stats',{});players=stats.get('players',{});rows=[dict(r)for r in players.values()if r[kind]>0]
    # Ties share rank: no fabricated minutes-played or UEFA tie-breaking claim.
    rows.sort(key=lambda r:(-r[kind],r['team_id'],int(r['player_id'])))
    previous=None;rank=0
    for i,row in enumerate(rows,1):
        if row[kind]!=previous:rank=i;previous=row[kind]
        row['rank']=rank
    completed=[m for m in state['matches']if m.get('result')is not None];attributed=stats.get('attributed_fixtures',{})
    return dict(kind=kind,rows=rows[:limit],completed_matches=len(completed),attributed_matches=sum(m['id']in attributed for m in completed),coverage_complete=all(m['id']in attributed for m in completed),native_adapter_integrated=False)
