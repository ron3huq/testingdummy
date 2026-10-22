"""efootxi 1.3.2: persistent season draw, strength-based CPU scores, first-team events.
CPU simulations and native roster/player hooks are installed by separate modules.
Played results, accepted ranking receipts and real-match events are never rewritten.
"""
from __future__ import annotations
import copy
import functools
import hashlib
import json
import math
from pathlib import Path
import random
import secrets
import threading
from collections import Counter

_event_context=threading.local()

ROOT = Path(__file__).resolve().parents[2]
ATTRS = ROOT / 'outputs/reference/external-attrs'
VERSION = 'native-hotfix-v10'
META = 'realism_v1'
_installed = False
_league = _rankings = None
_last_audit = None


def _rng(*values):
    raw = json.dumps(values,sort_keys=True,separators=(',',':')).encode()
    return random.Random(int.from_bytes(hashlib.sha256(raw).digest(),'big'))


def _seed(season):
    return (season.get(META) or {}).get('seed') or 'legacy:%s:%s:%s' % (
        season['season'],season['competition_id'],season['team_id'])


@functools.lru_cache(maxsize=32768)
def _profile(pid):
    # Use standard base cards, never boosted legend/owned-card ratings or foreign club labels.
    try:
        from myleague_worlds import config
        classic=config().get('classic_profiles',{}).get(str(pid),{}).get('simulation')
        if classic:return dict(classic)
        source=config().get('club_alias_ids',{}).get(str(pid),pid)
        path=ATTRS / (str(pid)+'.json')
        if not path.is_file():path=ATTRS / (str(source)+'.json')
        data = json.loads(path.read_text(encoding='utf8'))['efhub']
        player, stats = data['player'],data['card']['baseStats']
        rating = float(player['overallRating'])
        if not 40 <= rating <= 99:
            raise ValueError('invalid overall')
        return dict(rating=rating,finishing=float(stats['finishing']),
                    awareness=float(stats['offensiveAwareness']),
                    passing=float(stats['lowPass']),name=player.get('name',str(pid)),known=True)
    except (OSError,ValueError,TypeError,KeyError):
        # Explicit neutral estimate when this roster contains an uncatalogued player.
        return dict(rating=70.,finishing=65.,awareness=65.,passing=65.,name=str(pid),known=False)


def _position(pid):
    canonical = _rankings._canonical_data()
    pos = (canonical or {}).get('positions',{}).get(str(pid))
    return pos if type(pos) is int and 0 <= pos <= 12 else None


@functools.lru_cache(maxsize=2048)
def _roster_goal_boosts(roster):
    from myleague_worlds import config
    cfg=config();boosts=dict(cfg['scorer_boosts']);members=set(roster)
    for tid,overrides in cfg.get('team_scorer_boosts',{}).items():
        if members==set(_rankings._rosters().get(tid,[])):boosts.update(overrides)
    return boosts


@functools.lru_cache(maxsize=2048)
def _lineup(roster):
    from myleague_worlds import config
    for tid in ['108','114','127']+list(config().get('classic_teams',{})):
        ids=config()['native_rosters'][tid]
        if set(roster)==set(ids):return frozenset(ids[:11])
    goals=_roster_goal_boosts(roster)
    boosts={pid:max(float(goals.get(str(pid),goals.get(str(config().get('club_alias_ids',{}).get(str(pid),pid)),1))),float(config().get('assist_boosts',{}).get(str(pid),1))) for pid in roster}
    ordered = sorted(roster,key=lambda pid:(-_profile(pid)['rating']-4*(float(boosts.get(pid,1))-1),pid))
    chosen = []
    for positions,quota in [({0},1),({1,2,3},4),({4,5,6,7,8},3),({9,10,11,12},3)]:
        chosen.extend([pid for pid in ordered if _position(pid) in positions][:quota])
    for pid in ordered:
        if len(chosen)>=min(11,len(roster)):
            break
        if pid not in chosen and _position(pid)!=0:
            chosen.append(pid)
    return frozenset(chosen)


@functools.lru_cache(maxsize=2048)
def _club(team):
    roster = tuple(sorted(set(_rankings._rosters().get(str(team),[]))))
    starters = _lineup(roster)
    if not starters:
        return 72.,72.
    def mean(ids):
        ids=list(ids)
        # Missing catalog coverage is uncertainty, not proof of a poor club.
        return sum(_profile(pid)['rating'] if _profile(pid)['known'] else 74. for pid in ids)/len(ids) if ids else 74.
    overall=mean(starters)
    attack=mean(pid for pid in starters if _position(pid) in {6,7,8,9,10,11,12})
    defence=mean(pid for pid in starters if _position(pid) in {0,1,2,3,4})
    return .7*attack+.3*overall,.7*defence+.3*overall


def _poisson(rng,rate):
    threshold=math.exp(-rate);product=1.;count=0
    while product>threshold:
        count+=1;product*=rng.random()
    return count-1


def cpu_score(season,fixture,home,away):
    """Stable for this saved season+fixture, with genuine upsets, home edge and score tails."""
    rng=_rng(VERSION,_seed(season),fixture,home,away)
    if int(season['competition_id']) in SIMULATED_COMPETITIONS:
        score=_new_score(season,int(fixture),home,away,rng,_history(season,int(fixture)))
        if score is not None:return score
    special=_hierarchy_score(season,home,away,rng)
    if special is not None:return special
    ha,hd=_club(home);aa,ad=_club(away)
    # Shared club form across a season + independent match-day variability.
    hf=_rng(VERSION,_seed(season),'form',home).gauss(0,.07)
    af=_rng(VERSION,_seed(season),'form',away).gauss(0,.07)
    hrate=1.38*math.exp((ha-ad)/11+hf-af+rng.gauss(0,.12))
    arate=1.12*math.exp((aa-hd)/11+af-hf+rng.gauss(0,.12))
    return (_poisson(rng,max(.2,min(4.,hrate))),
            _poisson(rng,max(.2,min(4.,arate))))


def _hierarchy_score(season,home,away,rng):
    if int(season['competition_id']) in SIMULATED_COMPETITIONS:
        fixture=int(season.get('fixture',1))
        return _new_score(season,fixture,home,away,rng,_history(season,fixture))
    from myleague_worlds import config
    cid=str(season['competition_id']);definition=config()['leagues'].get(cid)
    if not definition:return None
    tiers=definition['tiers']
    if str(home) not in tiers or str(away) not in tiers:return None
    if cid=='566':return _asian_score(season,home,away,rng)
    ht,at=tiers[str(home)],tiers[str(away)]
    strengths={'122':[2.15,1.9,1.1,.1,-1.15],
               '128':[2.1,1.55,.75,.4,-.5],
               
               '549':[2.1,1.1,.2]}
    values=strengths.get(cid)
    if not values:return None
    hs,as_=values[ht],values[at]
    # El Clasico is even before home advantage and season/match form.
    if cid=='122' and {home,away}=={108,109}:hs=as_=2.
    if cid=='128':
        hs+=.18 if home==7 else 0;as_+=.18 if away==7 else 0
    hs+=.18 # modest general home advantage
    hs+=_rng(VERSION,_seed(season),'form',home).gauss(0,.13)
    as_+=_rng(VERSION,_seed(season),'form',away).gauss(0,.13)
    if cid=='122':
        if home in {125,126}:hs+=.45
        if away in {125,126}:as_-=.25
        for tid,is_home in [(home,True),(away,False)]:
            noise=rng.gauss(0,.6 if tid in {130,327,179} else .18)
            if is_home:hs+=noise
            else:as_+=noise
        # Unstable outsiders occasionally produce an exceptional performance.
        if home in {130,327} and at<=1 and rng.random()<.09:hs+=2.
        if away in {130,327} and ht<=1 and rng.random()<.09:as_+=2.
    else:
        hs+=rng.gauss(0,.22);as_+=rng.gauss(0,.22)
    gap=abs(hs-as_)
    draw=max(.08,.25-.055*gap)
    home_win=(1-draw)/(1+math.exp(-1.45*(hs-as_)))
    # Explicit probability rules choose outcomes; score generation is separate.
    if cid=='122':
        policy=config()['club_outcome_policy'];fav=None;chosen=None
        if {home,away}=={108,109}:
            draw=.24;home_win=(1-draw)/(1+math.exp(-1.1*(hs-as_)))
        elif {ht,at}=={0,1}:
            fav=home if ht==0 else away;chosen=policy['top1_vs_top2']
        elif min(ht,at)<=1 and max(ht,at)>=2:
            fav=home if ht<=1 else away;weak=away if fav==home else home;ft=ht if fav==home else at;wt=at if fav==home else ht
            chosen=policy['vs_group3'] if wt==2 else policy['top1_vs_group4'] if ft==0 else policy['vs_group4']
        if chosen:
            win=chosen['win'];draw=chosen['draw']
            if max(ht,at)>=3 and weak in {125,126,130,327}:
                win+=.04 if fav==home else -.04;draw=(1-win)*chosen['draw']/(1-chosen['win'])
            roll=rng.random();winner=fav if roll<win else None if roll<win+draw else (away if fav==home else home)
        else:
            roll=rng.random();winner=home if roll<home_win else None if roll<home_win+draw else away
        return _club_scoreline(home,away,winner,ht,at,rng)
    roll=rng.random()
    if roll<home_win:winner=home
    elif roll<home_win+draw:winner=None
    else:winner=away
    mode=rng.random()
    if winner is None:
        # Goalless tactical draws and open 3-3 games are both possible.
        rate=.5 if mode<.50 else 1.5 if mode<.9 else 2.8
        g=min(5,_poisson(rng,rate));return g,g
    favorite=home if hs>=as_ else away
    if mode<.43:
        # Narrow wins: a low block can hold even the strongest attack down.
        loser=0 if rng.random()<.64 else 1
        win=loser+1
    elif mode<.78:
        loser=min(3,_poisson(rng,1.0));win=loser+1+min(2,_poisson(rng,.65))
    elif mode<.94 and winner==favorite:
        loser=0 if rng.random()<.72 else 1;win=4 if rng.random()<.60 else 5
    else:
        loser=min(4,_poisson(rng,1.8));win=loser+1+min(2,_poisson(rng,.8))
    if cid=='122' and 100 in (home,away) and winner!=100 and rng.random()<.45:
        win=min(7,win+1)
    return (win,loser) if winner==home else (loser,win)


def _weighted_score(rng,rows):
    roll=rng.random()*sum(w for h,a,w in rows)
    for h,a,w in rows:
        roll-=w
        if roll<0:return h,a
    return rows[-1][:2]

def _club_scoreline(home,away,winner,ht,at,rng):
    top_clash=max(ht,at)<=1
    if winner is None:
        rows=[(0,0,35),(1,1,65)] if top_clash or min(ht,at)<=1 else [(0,0,30),(1,1,65),(2,2,5)]
        return _weighted_score(rng,rows)
    loser_team=away if winner==home else home
    upset=(ht<=1 and winner==away and at>=2) or (at<=1 and winner==home and ht>=2)
    if top_clash:rows=[(1,0,30),(2,1,25),(2,0,23),(3,1,22)]
    elif upset:rows=[(1,0,30),(2,1,70)]
    elif loser_team==100:rows=[(1,0,15),(2,0,25),(2,1,10),(3,0,25),(3,1,10),(4,0,15)]
    elif min(ht,at)<=1:rows=[(1,0,26),(2,0,28),(2,1,18),(3,0,15),(3,1,8),(4,0,5)]
    else:rows=[(1,0,30),(2,1,30),(2,0,20),(3,1,15),(3,0,5)]
    # Reweight the legal score support by match style; the result winner was
    # already chosen independently. No score outside the requested envelope.
    style=rng.random();pressure=rng.uniform(.7,1.3)
    if style<.38:rows=[(w,l,weight*(1.8 if w<=2 and l==0 else .55)) for w,l,weight in rows]
    elif style<.70:rows=[(w,l,weight*(1.65 if l==1 else .7)) for w,l,weight in rows]
    else:rows=[(w,l,weight*(pressure*1.65 if w-l>=2 else .65)) for w,l,weight in rows]
    w,l=_weighted_score(rng,rows)
    return (w,l) if winner==home else (l,w)



def _asian_score(season,home,away,rng):
    from myleague_worlds import config
    cid=str(season['competition_id']);definition=config()['leagues'].get(cid)
    if not definition:return None
    tiers=definition['tiers']
    if str(home) not in tiers or str(away) not in tiers:return None
    ht,at=tiers[str(home)],tiers[str(away)]
    if cid=='566':
        middle={5763,5750,1031,5752,1011,1012}
        if home in middle and away in middle:strong=True;win,draw=.40,.20
        elif (home in middle)!=(away in middle):
            medium=home if home in middle else away;other=away if home in middle else home
            if tiers[str(other)]<2:strong=other==home;win,draw=.70,.20
            else:strong=medium==home;win,draw=.70,.30
        elif 52 in (home,away):strong=home==52;win,draw=(.90,.07) if max(ht,at)<=1 else (.98,.02)
        elif ht!=at:strong=ht<at;win,draw=(.78,.15) if max(ht,at)<=1 else (.95,.04)
        else:strong=True;win,draw=.40,.20
    elif cid=='128' and ht==at==0:
        if 7 in (home,away):strong=home==7;win,draw=.58,.18
        else:strong=True;win,draw=.40,.20
    elif cid=='128' and ((ht==0)!=(at==0)):
        strong=ht==0;win,draw=(.88,.08) if max(ht,at)==1 else (.96,.04)
    elif cid=='122' and ((ht<=1)!=(at<=1)):
        # User's top five remain unbeaten against the lower groups in CPU simulation.
        strong=ht<=1;win,draw=.97,.03
    elif cid=='122' and 100 in (home,away):
        strong=home!=100;win,draw=.88,.095 # United wins only 2.5% against non-top-five.
    elif ht!=at:
        strong=ht<at;gap=abs(ht-at)
        if cid=='122' and max(ht,at)==1:win,draw=.72,.18
        else:win,draw=min(.97,.83+.035*(gap-1)),max(.02,.12-.025*(gap-1))
    else:
        strong=True;win,draw=.44,.23 # Home edge within the same tier.
    roll=rng.random();winner=(home if strong else away) if roll<win else None if roll<win+draw else (away if strong else home)
    if winner is None:
        score=_poisson(rng,1.35 if min(ht,at)<=1 else 1.)
        return score,score
    gap=abs(ht-at);favored=(winner==home if strong else winner==away)
    winner_goals=_poisson(rng,min(4.2,2.6+.25*gap) if favored else 1.5)
    loser_goals=_poisson(rng,.65 if gap>=2 and favored else 1.)
    if winner_goals<=loser_goals:winner_goals=loser_goals+1+(_poisson(rng,.7) if favored else 0)
    return (winner_goals,loser_goals) if winner==home else (loser_goals,winner_goals)


# V10 CPU-only simulation. No match packets or native engine pointers are touched.
SIMULATED_COMPETITIONS = {122,518,566,128}
_DERBIES = {frozenset(x) for x in [(100,173),(101,179),(101,102),(102,179),
    (109,172),(108,109),(121,119),(120,119),(125,327),(126,127),(103,100),(103,173)]}
# Style identifiers use exact team IDs; classic aliases are resolved by donor ID.
_ATTACK = {108,114,126,179,50,45}
_DEFENCE = {101,172,119,120,5,12,24,49}
_HOME_SPECIAL = {103,127,125,126,130,327,14,44,40,32,38,39}
_RARE = {(4,4),(6,2),(2,6),(7,1),(1,7)}


def _sim_definition(season):
    from myleague_worlds import config
    cid=int(season['competition_id'])
    return config()['leagues'].get(str(cid),{}) if cid in SIMULATED_COMPETITIONS else {}


def _identity(cid,team):
    if cid==518:
        from myleague_worlds import config
        return int(config()['classic_teams'].get(str(team),{}).get('visual_team',team))
    return team


class _MatchHistory(list):
    def __init__(self,rows):
        super().__init__(rows)
        self.by_team={};self.pairs={}
        for rnd,m in rows:
            h,a=m['home_team_id'],m['away_team_id'];x,y=m['home_goals'],m['away_goals']
            self.by_team.setdefault(h,[]).append((x,y))
            self.by_team.setdefault(a,[]).append((y,x))
            self.pairs.setdefault((h,a),[]).append((x,y))
            self.pairs.setdefault((a,h),[]).append((y,x))


def _history(season,before):
    rows=[]
    for key,record in season.get('played',{}).items():
        try:round_no=int(key)
        except (ValueError,TypeError):continue
        if round_no<before:
            rows.extend((round_no,m) for m in record.get('matches',[]))
    return _MatchHistory(sorted(rows,key=lambda x:x[0]))


def _form(season,fixture,team,history):
    if not isinstance(history,_MatchHistory):history=_MatchHistory(history)
    recent=[1 if x>y else 0 if x==y else -1 for x,y in history.by_team.get(team,[])[-5:]]
    inertia=sum((i+1)*v for i,v in enumerate(recent))/max(1,sum(range(1,len(recent)+1)))
    phase=_rng('form-phase-v10',_seed(season),team,(fixture-1)//4).uniform(-.18,.18)
    return .24*inertia+phase


def _outcome_probabilities(season,fixture,home,away,history=()):
    definition=_sim_definition(season);tiers=definition.get('tiers',{})
    if str(home) not in tiers or str(away) not in tiers:return None
    cid=int(season['competition_id']);ht,at=tiers[str(home)],tiers[str(away)]
    # Japan's explicit probabilities take precedence over generic venue/form weights.
    if cid==566 and 52 in (home,away):
        tier=at if home==52 else ht
        win,draw={1:(.65,.22),2:(.70,.15),3:(.85,.15),4:(.94,.06)}[tier]
        return (win,draw,1-win-draw) if home==52 else (1-win-draw,draw,win)
    if cid==122 and {ht,at}=={0,1} and {home,away}!={108,109}:
        win=.65 if ht==0 else .45;draw=.28
        hw=win if ht==0 else 1-win-draw
    elif cid==122 and ht==at==0:hw,draw=.365,.35
    elif cid==122 and ht==at==1:hw,draw=.40,.30
    else:
        gap=at-ht
        # The equal Clasico exception survives the regrouping.
        if cid==122 and {home,away}=={108,109}:gap=0
        if cid==518 and {home,away}=={1220,1222}:gap=0
        if cid==566 and {home,away} <= {5763,1031,5750}:gap=0
        gap=max(-5,min(5,gap))
        draw=max(.10,.30-.035*abs(gap))
        if cid==122 and min(ht,at)==0 and max(ht,at)>=5:draw=.13
        advantage=.20+.58*gap
        hw=(1-draw)/(1+math.exp(-advantage))
    if cid==122 and min(ht,at)<=1 and max(ht,at)>=2:
        strong=home if ht<at else away;top=min(ht,at);weak=max(ht,at)
        win=({2:.84,3:.89,4:.91,5:.93,6:.94} if top==0 else {2:.74,3:.82,4:.86,5:.89,6:.91})[weak]
        win+=.02 if strong==home else -.02
        draw=(1-win)*.72
        hw=win if strong==home else 1-win-draw
    elif cid==122 and 100 in (home,away):
        other=away if home==100 else home;ot=tiers[str(other)]
        win={2:.60,3:.40,4:.35,5:.32}.get(ot,.54)
        win+=.05 if other==home else -.05
        draw=.28;hw=win if other==home else 1-win-draw
    ih,ia=_identity(cid,home),_identity(cid,away)
    venue=(.045 if ih in _HOME_SPECIAL else 0)+(.02 if ia in _HOME_SPECIAL else 0)
    delta=.075*(_form(season,fixture,home,history)-_form(season,fixture,away,history))+venue
    hw=max(.015,min(1-draw-.015,hw+delta))
    if cid==122 and frozenset((home,away)) in _DERBIES:
        # Narrow derby disparity rather than pretending cards or comeback events exist.
        draw=min(.38,draw+.035);hw=.78*hw+.22*(1-draw)/2
    return hw,draw,max(0.,1-hw-draw)


def _large_upset(definition,m):
    tiers=definition['tiers'];h,a=m['home_team_id'],m['away_team_id']
    if str(h) not in tiers or str(a) not in tiers:return False
    hg,ag=m['home_goals'],m['away_goals']
    if hg==ag:return False
    winner,loser=(h,a) if hg>ag else (a,h)
    return tiers[str(winner)]-tiers[str(loser)]>=3


def _new_score(season,fixture,home,away,rng,history=()):
    definition=_sim_definition(season);prob=_outcome_probabilities(season,fixture,home,away,history)
    if prob is None:return None
    cid=int(season['competition_id']);tiers=definition['tiers'];ht,at=tiers[str(home)],tiers[str(away)]
    hw,draw,aw=prob;roll=rng.random();winner=home if roll<hw else None if roll<hw+draw else away
    shock_count=sum(_large_upset(definition,m) for rnd,m in history if rnd>=fixture-9)
    if winner is not None and shock_count>=2:
        loser=away if winner==home else home
        if tiers[str(winner)]-tiers[str(loser)]>=3:winner=None
    ih,ia=_identity(cid,home),_identity(cid,away)
    attack=sum(t in _ATTACK for t in (ih,ia));defence=sum(t in _DEFENCE for t in (ih,ia))
    if winner is None:
        rows=[(0,0,32),(1,1,55),(2,2,11),(3,3,2)]
        if attack:rows=[(h,a,w*(1+attack*.8 if h>=2 else 1)) for h,a,w in rows]
        if defence:rows=[(h,a,w*(1+defence*.4 if h<=1 else .6)) for h,a,w in rows]
    else:
        # Unconditional margin targets36/24/11/7 conditional on a decisive result.
        margin_weights=[36,24,11,7]
        top_clash=max(ht,at)<=1
        if top_clash:margin_weights=[67,28,4,1]
        if winner==(away if ht<at else home) and ht!=at:margin_weights=[72,24,3,1]
        if cid==566:margin_weights=[51,31,15,3]
        rows=[]
        for margin,weight in enumerate(margin_weights,1):
            for loser,lw in [(0,65),(1,29),(2,5),(3,1)]:
                win=loser+margin
                if win>5:continue
                factor=1.
                if attack and loser>=1:factor*=1+attack*.65
                if defence and loser==0:factor*=1+defence*.35
                if winner==home and ih in _HOME_SPECIAL and margin>=2:factor*=1.3
                if winner==away and ia in _HOME_SPECIAL and margin>=3:factor*=.65
                if min(ht,at)==0 and max(ht,at)>=5 and margin>=3:factor*=1.5
                rows.append((win,loser,weight*lw*factor))
        # Six goals only in modern Ligue1, with a large, correctly directed gap.
        if cid==122 and abs(ht-at)>=3 and tiers[str(winner)]<tiers[str(away if winner==home else home)]:
            rows.extend([(6,0,15),(6,1,8)])
    # Remove exact reverse-leg repeats and a third identical team score.
    if not isinstance(history,_MatchHistory):history=_MatchHistory(history)
    legal=[]
    rare_used=sum((m['home_goals'],m['away_goals']) in _RARE for _,m in history)
    if cid==122 and rare_used<2 and rng.random()<.004:
        rows=rows+([(4,4,30)] if winner is None else [(6,2,15),(7,1,5)])
    for x,y,w in rows:
        hg,ag=(x,y) if winner in (None,home) else (y,x)
        rejected=(hg,ag) in history.pairs.get((home,away),[])
        for team,score in [(home,(hg,ag)),(away,(ag,hg))]:
            past=history.by_team.get(team,[])
            if len(past)>=2 and past[-2:]==[score,score]:rejected=True
        if not rejected:legal.append((hg,ag,w))
    if max(ht,at)<=1:
        prior=history.pairs.get((home,away),[])
        if prior and not any(x+y>=4 or x==y==0 for x,y in prior):
            varied=[row for row in legal if row[0]+row[1]>=4 or row[0]==row[1]==0]
            if varied:legal=varied
    if not legal:
        legal=[((x if winner in (None,home) else y),(y if winner in (None,home) else x),w) for x,y,w in rows]
    return _weighted_score(rng,legal)


def _round_cost(season,fixture,matches,history):
    from collections import Counter
    definition=_sim_definition(season);tiers=definition['tiers'];n=len(matches)
    scores=[(m['home_goals'],m['away_goals']) for m in matches]
    draws=sum(x==y for x,y in scores)
    # Scottish has6 fixtures, World10 and modern/Asian9; scale draw quota accordingly.
    low=1 if n<=6 else 2;high=2 if n<=6 else 3
    penalty=25*(max(0,low-draws)+max(0,draws-high))
    penalty+=15*int(not any(sorted((x,y))==[0,1] for x,y in scores))
    penalty+=12*int(not any(x+y>=4 for x,y in scores))
    penalty+=15*int(not any(x<y for x,y in scores))
    penalty+=12*int(not any(min(x,y)>=2 for x,y in scores))
    penalty+=20*sum(max(0,v-2) for v in Counter(scores).values())
    penalty+=18*sum(max(0,v-3) for v in Counter(abs(x-y) for x,y in scores).values())
    top_results=[]
    shocks=sum(_large_upset(definition,m) for rnd,m in history if rnd>=fixture-9)
    shocks+=sum(_large_upset(definition,m) for m in matches)
    penalty+=100*max(0,shocks-2)
    rare=sum((m['home_goals'],m['away_goals']) in _RARE for _,m in history)
    rare+=sum(s in _RARE for s in scores);penalty+=100*max(0,rare-2)
    for m in matches:
        for team,other,x,y in [(m['home_team_id'],m['away_team_id'],m['home_goals'],m['away_goals']),(m['away_team_id'],m['home_team_id'],m['away_goals'],m['home_goals'])]:
            if tiers.get(str(team),9)<=1:top_results.append(x>y)
    penalty+=8*int(bool(top_results) and all(top_results))
    # Avoid the same complete score multiset on consecutive rounds.
    previous=[m for rnd,m in history if rnd==fixture-1]
    if previous and sorted(scores)==sorted((m['home_goals'],m['away_goals']) for m in previous):penalty+=12
    # Five-round rolling feedback: a soft target, never editing completed games.
    recent=[m for rnd,m in history if rnd>=fixture-4]+matches
    if recent:
        total=len(recent);nd=sum(m['home_goals']==m['away_goals'] for m in recent)
        goals=sum(m['home_goals']+m['away_goals'] for m in recent)
        penalty+=abs(nd/total-.22)*12+abs(goals/total-2.8)*1.5
        for margin,target in [(1,.36),(2,.24),(3,.11),(4,.07)]:
            frequency=sum(min(4,abs(m['home_goals']-m['away_goals']))==margin for m in recent)/total
            penalty+=abs(frequency-target)*3
        penalty+=abs(sum(m['home_goals']>m['away_goals'] for m in recent)/total-.45)*2
    return penalty


def _round_scores(season,fixture,matches):
    number=int(fixture);history=_history(season,number)
    # User match is not simulated and is not counted as a fictional0-0 for quotas.
    indices=[i for i,m in enumerate(matches) if season['team_id'] not in (m['home_team_id'],m['away_team_id'])]
    result=copy.deepcopy(matches)
    rng=_rng('round-v10',_seed(season),number)
    for i in indices:
        m=result[i];score=_new_score(season,number,m['home_team_id'],m['away_team_id'],rng,history)
        if score is None:score=cpu_score(season,number,m['home_team_id'],m['away_team_id'])
        m.update(home_goals=score[0],away_goals=score[1])
    cpu=lambda rows:[rows[i] for i in indices]
    best=_round_cost(season,number,cpu(result),history)
    # Bounded coordinate search; alternatives retain team probabilities/style.
    # At most320 candidates, ~milliseconds for a round without deep history.
    for attempt in range(320):
        if not indices or best<.4:break
        i=rng.choice(indices);m=result[i];old=(m['home_goals'],m['away_goals'])
        score=_new_score(season,number,m['home_team_id'],m['away_team_id'],rng,history)
        if score is None:continue
        m.update(home_goals=score[0],away_goals=score[1])
        cost=_round_cost(season,number,cpu(result),history)
        if cost<best or (abs(cost-best)<1e-9 and rng.random()<.03):best=cost
        else:m.update(home_goals=old[0],away_goals=old[1])
    # Enforce budgets even if the bounded quota search cannot find a full fit.
    definition=_sim_definition(season)
    shocks=sum(_large_upset(definition,m) for rnd,m in history if rnd>=number-9)
    rare=sum((m['home_goals'],m['away_goals']) in _RARE for _,m in history)
    for i in indices:
        m=result[i]
        if _large_upset(definition,m):
            if shocks>=2:
                goals=0 if rng.random()<.32 else 1
                m.update(home_goals=goals,away_goals=goals)
            else:shocks+=1
        score=(m['home_goals'],m['away_goals'])
        if score in _RARE:
            if rare>=2:
                replacement={(4,4):(2,2),(6,2):(4,2),(2,6):(2,4),(7,1):(5,1),(1,7):(1,5)}[score]
                m.update(home_goals=replacement[0],away_goals=replacement[1])
            else:rare+=1
    for i,m in enumerate(result):
        if i not in indices:m.update(home_goals=0,away_goals=0)
    return result


def simulation_summary(season):
    """Read-only audit of completed rounds; no fictional minute/card commentary."""
    history=_history(season,10**9);matches=[m for _,m in history];n=len(matches)
    return dict(version=VERSION,completed_rounds=len({rnd for rnd,_ in history}),matches=n,
        draw_rate=sum(m['home_goals']==m['away_goals'] for m in matches)/max(1,n),
        home_win_rate=sum(m['home_goals']>m['away_goals'] for m in matches)/max(1,n),
        goals_per_game=sum(m['home_goals']+m['away_goals'] for m in matches)/max(1,n),
        score_counts={str(x):sum((m['home_goals'],m['away_goals'])==x for m in matches) for x in sorted({(m['home_goals'],m['away_goals']) for m in matches})},
        real_match_results_included=True,guaranteed_season_totals=False)



def fixture_matches(season,fixture):
    global _last_audit
    completed=len(season.get('played',{}))
    audit_key=(_seed(season),season['competition_id'],season['team_id'],completed)
    if int(season['competition_id']) in SIMULATED_COMPETITIONS and completed and completed%5==0 and audit_key!=_last_audit:
        try:
            Path(__file__).with_name('myleague-simulation-status.json').write_text(json.dumps(simulation_summary(season),indent=2))
            _last_audit=audit_key
        except OSError:pass
    saved=season.get('played',{}).get(str(fixture['fixture']))
    if saved:
        return copy.deepcopy(saved['matches'])
    matches=copy.deepcopy(fixture['match_list'])
    if int(season['competition_id']) in SIMULATED_COMPETITIONS:
        result=_round_scores(season,fixture['fixture'],matches)
        return result
    for match in matches:
        home,away=match['home_team_id'],match['away_team_id']
        # Actual user fixture is handled by the original native match/receipt path.
        hg,ag=(0,0) if season['team_id'] in (home,away) else cpu_score(season,fixture['fixture'],home,away)
        match.update(home_goals=hg,away_goals=ag)
    return matches


def _fixtures(original,season):
    # Existing snapshots, historical seasons and prepared opponents keep their exact draw.
    rows=original(season)
    if 'schedule_v2' in season or season.get('played') or season.get('active'):
        return rows
    metadata=season.get(META)
    if not isinstance(metadata,dict) or not metadata.get('seed'):
        season[META]=dict(version=VERSION,seed=secrets.token_hex(16))
    rng=_rng(VERSION,_seed(season),'draw')
    teams=sorted({m[side+'_team_id'] for fx in rows for m in fx['match_list'] for side in ('home','away')})
    shuffled=teams.copy();rng.shuffle(shuffled)
    relabel=dict(zip(teams,shuffled))
    # Relabel the existing validated double round-robin graph. Keeps round numbers,
    # byes, mirrored home/away legs and venue-run quality without fixed opponents.
    for fx in rows:
        for match in fx['match_list']:
            for side in ('home','away'):
                match[side+'_team_id']=relabel[match[side+'_team_id']]
            match.update(home_goals=0,away_goals=0)
        rng.shuffle(fx['match_list'])
    return rows


@functools.lru_cache(maxsize=4096)
def _event_pool(roster,assists):
    starters=_lineup(roster)
    goal_roles=(0,.25,.35,.35,.5,1.1,2.,2.,2.4,4.5,4.5,5.5,7.)
    assist_roles=(0,.4,1.5,1.5,1.3,2.8,3.5,3.5,5.,4.,4.,3.,1.8)
    roles=assist_roles if assists else goal_roles
    pool=[]
    for pid in roster:
        pos=_position(pid);profile=_profile(pid)
        role=roles[pos] if pos is not None else 1.
        minutes=1. if pid in starters else .12
        quality=math.exp((profile['rating']-75)/7)
        skill=(profile['passing']/70)**2 if assists else ((profile['finishing']+profile['awareness'])/140)**2
        from myleague_worlds import config
        alias=str(config().get('club_alias_ids',{}).get(str(pid),pid))
        boost=float(_roster_goal_boosts(roster).get(str(pid),_roster_goal_boosts(roster).get(alias,1)))
        if assists:boost=float(config().get('assist_boosts',{}).get(str(pid),config().get('assist_boosts',{}).get(alias,math.sqrt(boost))))
        weight=round(12*role*minutes*quality*skill*boost)
        # A known GK cannot become a scorer through rounding/minimum-weight fallback.
        if role>0:
            pool.extend([pid]*max(1,min(2000,weight)))
    return tuple(pool)


def weighted_roster(conn,roster,assists=False):
    base=_event_pool(tuple(sorted(set(roster))),bool(assists))
    context=getattr(_event_context,'current',None)
    if not context or int(context[0]['competition_id']) not in SIMULATED_COMPETITIONS:return list(base)
    season,fixture=context;weights=Counter(base)
    # Stable4-round player form gives bursts/dry spells without inventing injuries.
    for pid in weights:
        phase=_rng('player-form-v10',_seed(season),pid,(fixture-1)//4,assists).uniform(.65,1.4)
        weights[pid]=max(1,round(weights[pid]*phase))
    from myleague_worlds import config
    cfg=config();boosts=cfg['assist_boosts'] if assists else _roster_goal_boosts(tuple(sorted(set(roster))))
    def priority(pid):
        alias=str(cfg.get('club_alias_ids',{}).get(str(pid),pid))
        return float(boosts.get(str(pid),boosts.get(alias,1)))
    leaders=sorted(weights,key=lambda p:(priority(p),weights[p]),reverse=True)
    if leaders and priority(leaders[0])>=5:
        leader=leaders[0];others=sum(weights.values())-weights[leader]
        # Main finishers40-53% of own-team goals; creator35-45% of assists.
        share=_rng('leader-share-v10',_seed(season),leader,(fixture-1)//4,assists).uniform(.35,.45) if assists else _rng('leader-share-v10',_seed(season),leader,(fixture-1)//4).uniform(.40,.53)
        if not assists and int(season['competition_id'])==518 and cfg['classic_profiles'].get(str(leader),{}).get('name') in ['Cristiano Ronaldo','Lionel Messi']:
            share=_rng('retro-duo-share',_seed(season),leader,(fixture-1)//4).uniform(.66,.74)
        if not assists and int(season['competition_id'])==128 and leader==133543:
            share=_rng('norway-striker-share',_seed(season),(fixture-1)//4).uniform(.58,.68)
        if others:weights[leader]=max(1,round(others*share/(1-share)))
    if weights:
        # Messi/Ronaldo retro remain the main duo; no forced external player IDs.
        retro=int(season['competition_id'])==518
        special=[pid for pid in weights if priority(pid)>=5 and (not retro or cfg['classic_profiles'].get(str(pid),{}).get('name') in ['Cristiano Ronaldo','Lionel Messi'])]
        cap=(.38 if max((priority(pid) for pid in weights),default=0)>=8 else .23) if assists else (.72 if retro and special else .65 if int(season['competition_id'])==128 and 133543 in weights else .48 if special else .34)
        for _ in range(5):
            total=sum(weights.values());changed=False
            for pid,value in list(weights.items()):
                if value>total*cap:
                    others=total-value;weights[pid]=max(1,round(others*cap/(1-cap)));changed=True
            if not changed:break
    # Bounded memory independent of full64 ID size; identity remains exact.
    total=sum(weights.values())
    return [pid for pid,w in weights.items() for _ in range(max(1,round(4096*w/max(1,total))))]


def install():
    global _installed,_league,_rankings
    if _installed:
        return False
    import my_league
    import season_rankings
    expected={'my_league.py': '06ef47e1700e408044543ebc227729bff8904b63a68891c825a70e2a9d047f0b', 'season_rankings.py': '22d58b6396ea655c419d5e9a665ea280554c3a3138acff791cc190147831903f'}
    for name,digest in expected.items():
        source=Path(my_league.__file__).parent/name
        if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
            raise RuntimeError("Unsupported gateway source: "+name)
    import myleague_worlds
    myleague_worlds.install()
    original=my_league.fixtures
    _league,_rankings=my_league,season_rankings
    @functools.wraps(original)
    def fixtures(season):
        return _fixtures(original,season)
    my_league.fixtures=fixtures
    my_league.fixture_matches=fixture_matches
    season_rankings._weighted_roster=weighted_roster
    original_simulate=season_rankings._simulate_matches
    @functools.wraps(original_simulate)
    def simulate(conn,season,fixture,matches,only_teams=None):
        previous=getattr(_event_context,'current',None)
        _event_context.current=(season,int(fixture))
        try:return original_simulate(conn,season,fixture,matches,only_teams)
        finally:_event_context.current=previous
    season_rankings._simulate_matches=simulate
    _installed=True
    try:
        Path(__file__).with_name('myleague-realism-status.json').write_text(json.dumps(dict(
            state='INSTALLED',version=VERSION,previous_results_rewritten=False,
            native_select_team_changed=True,new_season_draw='random_persisted',
            cpu_model='seven-group scoped styles, rolling played form, bounded CPU round diversity and ten-round upset budget',
            scorer_model='canonical roster + role + quality + first-team minutes + requested priority'),indent=2))
    except OSError:
        pass
    return True
