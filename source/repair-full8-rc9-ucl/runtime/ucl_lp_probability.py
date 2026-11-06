"""User document's CPU-only probability model. Never chooses a played result.
Raw score weights are preserved; normalize only at the weighted draw.
"""
import math
from fractions import Fraction

MODEL='user-ucl-probability-v1'
WDL={0:((40,27,33),(33,27,40)),1:((55,24,21),(42,27,31)),2:((68,20,12),(55,24,21)),3:((78,14,8),(66,20,14)),4:((85,10,5),(74,17,9))}
CLOSE=[(1,0,22),(2,1,18),(2,0,17),(3,0,9),(3,1,9),(3,2,5),(4,0,5),(4,1,4),(5,0,3),(4,2,4),(5,1,4),(6,0,4),(4,3,4),(5,2,4),(6,1,4),(6,2,4)]
BIG=[(3,0,17),(2,0,14),(4,0,7),(4,2,7),(5,0,Fraction(8,3)),(5,1,Fraction(8,3)),(5,2,Fraction(8,3)),(3,1,10),(4,1,9),(1,0,8),(5,1,6),(6,0,6),(6,1,3),(7,0,3),(8,2,3),(6,2,3),(7,1,3),(7,2,3),(9,1,3)]
DRAWS=[(1,1,42),(0,0,24),(2,2,24),(3,3,8),(4,4,2)]
UPSET={(1,0),(2,1),(2,0),(3,1),(3,2)}

def normalize(weights):
    values=[float(v)for v in weights]
    if not values or any(not math.isfinite(v)or v<0 for v in values)or sum(values)<=0:raise ValueError('invalid probability weights')
    total=sum(values);return tuple(v/total for v in values)

def shift(probabilities,index,points):
    p=list(probabilities);before=p[index];after=max(0.,min(1.,before+points));others=[i for i in range(3)if i!=index];rest=1-before;p[index]=after
    for i in others:p[i]=(1-after)*p[i]/rest if rest>1e-15 else(1-after)/2
    return normalize(p)

def probabilities(home_group,away_group,home_streak=0,away_streak=0,derby=False,neutral=False):
    if type(home_group)is not int or type(away_group)is not int or not 1<=home_group<=5 or not 1<=away_group<=5:raise ValueError('group must be1..5')
    gap=abs(home_group-away_group)
    if gap==0:p=(.365,.27,.365)if neutral else(.40,.27,.33)
    else:
        strong_home=home_group<away_group;columns=WDL[gap]
        strong=tuple((a+b)/200 for a,b in zip(*columns))if neutral else normalize(columns[0 if strong_home else 1]);p=strong if strong_home else strong[::-1]
    # Explicit deterministic order where both clubs have a qualifying streak.
    for index,streak in [(0,home_streak),(2,away_streak)]:
        if streak>=3:p=shift(p,index,.04)
        elif streak<=-2:p=shift(p,index,-.04)
    if derby:p=shift(p,1,.05)
    return p

def choose(rows,rng):
    weights=normalize([row[2]for row in rows]);roll=rng.random();cumulative=0.
    for row,weight in zip(rows,weights):
        cumulative+=weight
        if roll<cumulative:return(row[0],row[1])
    return(rows[-1][0],rows[-1][1])

def regulation(rng,home_group,away_group,home_streak=0,away_streak=0,derby=False,neutral=False,prolific=(False,False)):
    p=probabilities(home_group,away_group,home_streak,away_streak,derby,neutral);roll=rng.random();winner=0 if roll<p[0]else None if roll<p[0]+p[1]else 1
    if winner is None:return _draw_result(rng,p)
    groups=(home_group,away_group);loser=1-winner;gap=abs(home_group-away_group);weaker=groups[winner]>groups[loser]
    # The3% shock is inside, never added to, the existing weak-win probability.
    weak_probability=p[0 if winner==0 else 2];shock=weaker and groups[loser]==1 and gap>=3 and rng.random()<min(1.,.03/weak_probability)
    if shock:w,l=choose([(3,0,1),(4,1,1)],rng)
    else:
        rows=CLOSE if gap<=2 or weaker else BIG
        if weaker:rows=[r for r in rows if r[:2]in UPSET]
        if prolific[winner]:rows=[(w,l,float(weight)*1.25**max(w-2,0))for w,l,weight in rows]
        w,l=choose(rows,rng)
    home,away=(w,l)if winner==0 else(l,w)
    return dict(home=home,away=away,shock=shock,probabilities=p)

def _draw_result(rng,p):
    home,away=choose(DRAWS,rng);return dict(home=home,away=away,shock=False,probabilities=p)

def extra_time(rng,home_group,away_group):
    # Conditional55/45 applies only to the70% decisive extra-time branch.
    if rng.random()<.30:return(0,0)
    if home_group==away_group:home_probability=.5
    else:home_probability=.55 if home_group<away_group else .45
    return(1,0)if rng.random()<home_probability else(0,1)

def shootout(rng):
    # Real five-kick series + paired sudden death; independent50/50 teams.
    home=away=0;hs=aws=0
    for kick in range(10):
        if kick%2==0:hs+=1;home+=int(rng.random()<.75)
        else:aws+=1;away+=int(rng.random()<.75)
        if home>away+5-aws or away>home+5-hs:return(home,away)
    for _ in range(64):
        home+=int(rng.random()<.75);away+=int(rng.random()<.75)
        if home!=away:return(home,away)
    # Computational bound on a CPU-only random series; still symmetric.
    return(home+1,away)if rng.random()<.5 else(home,away+1)

def streak(state,team,fixture_id):
    value=0
    for match in state['matches']:
        if match['id']==fixture_id:break
        result=match.get('result')
        if result is None or team not in(match['home'],match['away']):continue
        simulated=result.get('simulation',{});home=simulated.get('regulation_home',result['home']);away=simulated.get('regulation_away',result['away']);ours,theirs=(home,away)if team==match['home']else(away,home)
        if ours==theirs:value=0
        elif ours>theirs:value=value+1 if value>0 else 1
        else:value=value-1 if value<0 else-1
    return value

def fixture_result(state,match,rng,before=(0,0)):
    policy=state['cpu_policy'];groups=policy['groups'];home_group=groups[str(match['home'])];away_group=groups[str(match['away'])];teams={t['team_id']:t for t in state['teams']}
    regular=regulation(rng,home_group,away_group,streak(state,match['home'],match['id']),streak(state,match['away'],match['id']),teams[match['home']]['association']==teams[match['away']]['association'],match['stage']=='FINAL',tuple(t in policy['prolific_teams']for t in(match['home'],match['away'])))
    h,a=regular['home'],regular['away'];eh=ea=0;ph=pa=None;deciding=match['stage']=='FINAL'or(match['stage']in('PLAYOFFS','R16','QF','SF')and match['leg']==2)
    if deciding and h+before[0]==a+before[1]:
        eh,ea=extra_time(rng,home_group,away_group)
        if h+eh+before[0]==a+ea+before[1]:ph,pa=shootout(rng)
    return dict(home=h+eh,away=a+ea,pk_home=ph,pk_away=pa,simulation=dict(model=MODEL,regulation_home=h,regulation_away=a,extra_home=eh,extra_away=ea,shock=regular['shock'],home_draw_away_probabilities=regular['probabilities']))
