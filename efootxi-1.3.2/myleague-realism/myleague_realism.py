"""efootxi 1.3.2: persistent season draw, strength-based CPU scores, first-team events.
Only replaces three existing Python extension points; native menu hook is unchanged.
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
VERSION = 'realism-v1'
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
        data = json.loads((ATTRS / (str(pid)+'.json')).read_text(encoding='utf8'))['efhub']
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
def _lineup(roster):
    ordered = sorted(roster,key=lambda pid:(-_profile(pid)['rating'],pid))
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
    ha,hd=_club(home);aa,ad=_club(away)
    # Shared club form across a season + independent match-day variability.
    hf=_rng(VERSION,_seed(season),'form',home).gauss(0,.07)
    af=_rng(VERSION,_seed(season),'form',away).gauss(0,.07)
    hrate=1.38*math.exp((ha-ad)/11+hf-af+rng.gauss(0,.12))
    arate=1.12*math.exp((aa-hd)/11+af-hf+rng.gauss(0,.12))
    return (_poisson(rng,max(.2,min(4.,hrate))),
            _poisson(rng,max(.2,min(4.,arate))))


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
        weight=round(12*role*minutes*quality*skill)
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
            native_select_team_changed=False,new_season_draw='random_persisted',
            cpu_model='base-card strength + home edge + Poisson',
            scorer_model='canonical roster + role + quality + first-team minutes'),indent=2))
    except OSError:
        pass
    return True
