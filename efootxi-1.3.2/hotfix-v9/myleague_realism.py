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

ROOT = Path(__file__).resolve().parents[2]
ATTRS = ROOT / 'outputs/reference/external-attrs'
VERSION = 'native-hotfix-v9'
META = 'realism_v1'
_installed = False
_league = _rankings = None


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


def fixture_matches(season,fixture):
    saved=season.get('played',{}).get(str(fixture['fixture']))
    if saved:
        return copy.deepcopy(saved['matches'])
    matches=copy.deepcopy(fixture['match_list'])
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
    return list(_event_pool(tuple(sorted(set(roster))),bool(assists)))


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
    _installed=True
    try:
        Path(__file__).with_name('myleague-realism-status.json').write_text(json.dumps(dict(
            state='INSTALLED',version=VERSION,previous_results_rewritten=False,
            native_select_team_changed=True,new_season_draw='random_persisted',
            cpu_model='tier strengths, persisted form, home advantage, narrow/open/rout score regimes; upsets enabled',
            scorer_model='canonical roster + role + quality + first-team minutes + requested priority'),indent=2))
    except OSError:
        pass
    return True
