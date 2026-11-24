"""RC29.3: Master League realism layer (installed by rc26_hook after RC26 and ml_isolation; Master League only).

  * results    CPU v CPU scores (all leagues and the European cups) from real-world club strengths (ml_ratings) with a season
               swing per club and a 5-round form drift; Poisson goals, deterministic per (season, fixture, home, away).
  * scorers    the world's leading forwards take their real share of their club's goals (and assists); the rest by position.
  * structure  no second tiers, no promotion / relegation; no ageing, retirement, academy or youth intake.
  * form       both elevens at their best (form A); the default difficulty of a Master League match is LEGEND.
  * transfers  CPU deals are rare and plausible: few per window, no core player of a big club moving to a rival.
Every patch is a plain wrapper; My League (RC26) never reaches these functions (ml_isolation routes it elsewhere).
"""
import sys, math, random, zlib, unicodedata, functools, datetime
import ml_ratings as R

_state = {'installed': False, 'patched': [], 'errors': []}
TOP5 = (113, 119, 116, 900307, 122)


def in_ml():
    try:
        g = sys.modules.get('e307_profile_gate')
        if g is not None and g.active() == 'ml':
            return True
    except Exception:
        pass
    f = sys._getframe(2)
    n = 0
    while f is not None and n < 120:
        if f.f_globals.get('__name__', '').startswith('iml_'):
            return True
        f = f.f_back
        n += 1
    return False


_TRANS = str.maketrans({'ø': 'o', 'Ø': 'o', 'æ': 'ae', 'Æ': 'ae', 'ß': 'ss', 'ł': 'l', 'Ł': 'l', 'đ': 'd', 'Đ': 'd', 'ı': 'i', 'œ': 'oe'})


def _norm(s):
    s = unicodedata.normalize('NFKD', str(s or '').translate(_TRANS)).encode('ascii', 'ignore').decode().lower()
    return ' '.join(s.replace('-', ' ').replace('.', ' ').split())


_STAR_KEYS = [([_norm(k) for k in keys], g, a) for keys, g, a in R.STARS]
_star_cache = {}


def _name_match(k, n, words):
    """A star key names ONE person: a one-word key must be the surname (or the whole name / first name + Junior),
    never just any word of the name ('isak' is Alexander Isak, not Isak Hien; 'kane' is Harry Kane)."""
    if ' ' in k:
        return (' ' + k + ' ') in words
    toks = n.split()
    if not toks:
        return False
    if toks[-1] == k or n == k:
        return True
    return toks[0] == k and all(t in ('junior', 'jr', 'jnr', 'filho') for t in toks[1:])


def star_of(name):
    """(goal share, assist share) of a leading player, or None."""
    n = _norm(name)
    if n in _star_cache:
        return _star_cache[n]
    try:
        import ml_dynamics
        o = ml_dynamics.override(n)
        if o is not None:
            _star_cache[n] = o if (o[0] or o[1]) else None
            return _star_cache[n]
    except Exception:
        pass
    hit = None
    words = ' ' + n + ' '
    hit_key = None
    for keys, g, a in _STAR_KEYS:
        if any(_name_match(k, n, words) for k in keys):
            hit = (g, a)
            hit_key = keys[0]
            break
    try:
        import ml_dynamics
        hit = ml_dynamics.star_adjust(hit_key or n, hit)
    except Exception:
        pass
    _star_cache[n] = hit
    return hit


PHI = 0.6180339887498949


def spread_pick(keys, weights, u):
    total = sum(weights)
    if total <= 0:
        return keys[0]
    x = (u % 1.0) * total
    for k, w in zip(keys, weights):
        x -= w
        if x < 0:
            return k
    return keys[-1]


def season_u(tag, f, k):
    """A low-discrepancy draw for the k-th goal of match f: over a season the shares land close to their expectation."""
    off = (zlib.crc32(tag.encode()) % 100000) / 100000.0
    try:
        f = int(f)
    except Exception:
        f = zlib.crc32(str(f).encode()) % 997
    return (f * 7 + k) * PHI + off


SQRT2M1 = 0.41421356237309515


def season_v(tag, f, k):
    """Like season_u but on an independent low-discrepancy sequence (assists must not move in step with the goals:
    with the same stride the assist draw always fell on the scorer's slot and a 30-goal striker never got an assist)."""
    off = (zlib.crc32(tag.encode()) % 100000) / 100000.0
    try:
        f = int(f)
    except Exception:
        f = zlib.crc32(str(f).encode()) % 997
    return (f * 11 + k * 3) * SQRT2M1 + off


def shared_weights(cands, assist=False):
    """cands: [(key, name, base weight)] -> {key: weight} where a leading player gets his real share of the team's total."""
    shares = {}
    for key, name, w in cands:
        st = star_of(name)
        if st and w > 0:
            shares[key] = st[1] if assist else st[0]
    total = sum(shares.values())
    if total > 0.85:
        shares = {k: v * 0.85 / total for k, v in shares.items()}
        total = 0.85
    rest = sum(w for key, name, w in cands if key not in shares)
    out = {key: w for key, name, w in cands}
    if shares and rest > 0:
        for key, s in shares.items():
            out[key] = s / (1.0 - total) * rest
    return cap_shares(out, set(shares), NONSTAR_CAP_A if assist else NONSTAR_CAP_G)


NONSTAR_CAP_G = 0.14     # a player who is not a proven scorer takes at most ~17% of his team's goals (about 12-13 a season)
NONSTAR_CAP_A = 0.15


def cap_shares(weights, stars, cap):
    """Water-filling: no non-star keeps more than `cap` of the total; what they lose goes to everybody else in proportion."""
    w = {k: max(0.0, float(v)) for k, v in weights.items()}
    capped = set()
    for _ in range(10):
        total = sum(w.values())
        if total <= 0:
            return w
        over = {k for k, v in w.items() if k not in stars and k not in capped and v / total > cap + 1e-9}
        if not over:
            return w
        capped |= over
        rest = [k for k in w if k not in capped]
        rest_sum = sum(w[k] for k in rest)
        if rest_sum <= 0 or cap * len(capped) >= 1.0:
            return w
        # capped players hold exactly `cap` of the total, the others keep their proportions
        unit = rest_sum / (1.0 - cap * len(capped))
        for k in capped:
            w[k] = cap * unit
    return w


# ---------------------------------------------------------------- results
def _club(team):
    return R.CLUBS.get(int(team), R.DEFAULT)


def _coef(team):
    team = int(team)
    if team in R.GUEST_COEF:
        return R.GUEST_COEF[team]
    return R.LEAGUE_COEF.get(R.LEAGUE_OF.get(str(team)), 0.75)


def _gauss(key, sd):
    return random.Random(zlib.crc32(key.encode())).gauss(0.0, sd)


def team_strength(team, season, rnd):
    a, d, v = _club(team)
    sa = math.exp(_gauss('rc29-sa:%s:%s' % (season, team), v))
    sd = math.exp(_gauss('rc29-sd:%s:%s' % (season, team), v))
    blk = int(rnd or 0) // 5
    fa = math.exp(_gauss('rc29-fa:%s:%s:%s' % (season, team, blk), v * 0.55))
    fd = math.exp(_gauss('rc29-fd:%s:%s:%s' % (season, team, blk), v * 0.55))
    try:
        import ml_dynamics
        xa, xd = ml_dynamics.club_factor(team, season)
    except Exception:
        xa, xd = 1.0, 1.0
    return a * sa * fa * xa, d / (sd * fd) * xd


def _poisson(rng, lam):
    lam = max(0.05, min(5.0, lam))
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p < limit:
            return k
        k += 1


LEAGUE_GOAL_FACTOR = {116: 1.20, 122: 1.12, 119: 1.08, 900307: 1.08, 113: 1.02}


def realistic_score(season, rnd, home, away, neutral=False):
    ah, dh = team_strength(home, season, rnd)
    aa, da = team_strength(away, season, rnd)
    ch, ca = _coef(home), _coef(away)
    if abs(ch - ca) > 1e-9:
        ah, dh = ah * (ch / ca) ** 0.9, dh / (ch / ca) ** 0.45
        aa, da = aa * (ca / ch) ** 0.9, da / (ca / ch) ** 0.45
    hf, af = (1.0, 1.0) if neutral else (R.HOME, R.AWAY)
    # each league's real scoring level (goals a game): Serie A ~2.6, La Liga ~2.65, Ligue 1 ~2.85, Bundesliga ~3.15, Premier League ~2.9
    lgh, lga = R.LEAGUE_OF.get(str(home)), R.LEAGUE_OF.get(str(away))
    gfac = LEAGUE_GOAL_FACTOR.get(int(lgh), 1.0) if lgh is not None and lgh == lga else 0.9   # Europe: tighter games (~3 goals a match)
    lh = ah * da / R.LEAGUE_GOALS * hf * gfac
    la = aa * dh / R.LEAGUE_GOALS * af * gfac
    rng = random.Random(zlib.crc32(('rc29-cpu:%s:%s:%s:%s' % (season, rnd, home, away)).encode()))
    return _poisson(rng, lh), _poisson(rng, la)


def _cpu_score(orig):
    @functools.wraps(orig)
    def cpu_score(s, home, away):
        if not in_ml():
            return orig(s, home, away)
        try:
            s = s if isinstance(s, dict) else {}
            rnd = s.get('fixture', 0)
            neutral = False
            if not isinstance(rnd, int):
                text = str(rnd)
                neutral = 'final' in text and ':et' not in text
                rnd = zlib.crc32(text.encode()) % 997 + 100
            return realistic_score(s.get('season', 1), rnd, int(home), int(away), neutral)
        except Exception as exc:
            _state['errors'].append('cpu_score %r' % (exc,))
            return orig(s, home, away)
    cpu_score._rc29_realism = True
    return cpu_score


# ---------------------------------------------------------------- scorers
POS_GOAL = {1: 1, 2: 1.5, 3: 1.5, 4: 2, 5: 3, 6: 4, 7: 4, 8: 6, 9: 8, 10: 8, 11: 9, 12: 12}
POS_ASSIST = {1: 0.7, 2: 3, 3: 3, 4: 1.6, 5: 4, 6: 5, 7: 5, 8: 7, 9: 7, 10: 7, 11: 5, 12: 3}
_names = None


def _name(pid):
    global _names
    if _names is None:
        try:
            import my_league_opponents as mo
            _names = mo._names()
        except Exception:
            _names = {}
    v = _names.get(str(pid))
    return (v[0] if isinstance(v, list) else v) or ''


def _sim_scorer(orig, ml):
    @functools.wraps(orig)
    def pick(players, rng):
        if not in_ml():
            return orig(players, rng)
        sp = ml.SIM_PLAYERS
        cands = [(p, _name(p), POS_GOAL.get(sp[p][0], 0)) for p in players if p in sp and sp[p][0] in POS_GOAL]
        if not cands:
            return None
        w = shared_weights(cands)
        keys = [c[0] for c in cands]
        return rng.choices(keys, weights=[w[k] for k in keys], k=1)[0]
    pick._rc29_realism = True
    return pick


def _world_grp(pid):
    return None


def _round_stats(orig, ml):
    @functools.wraps(orig)
    def stats(s, matches, fixture, req=None):
        rows = orig(s, matches, fixture, req)
        if not in_ml():
            return rows
        try:
            own = int((s or {}).get('team_id') or 0)
            skip = set()
            for m in matches:
                if own in (int(m['home_team_id']), int(m['away_team_id'])):
                    skip.update((int(m['home_team_id']), int(m['away_team_id'])))
            import ziru_data
            rosters = ziru_data.rosters()
            sp = ml.SIM_PLAYERS
            by_team = {}
            for r in rows:
                by_team.setdefault(int(r['team_id']), []).append(r)
            for team, trs in by_team.items():
                if team in skip:
                    continue
                total = sum(int(r.get('assist') or 0) for r in trs)
                if not total:
                    continue
                # the players really in this match first (the living squad: transfers, the editor), then the club's regulars
                players = list(dict.fromkeys([r['player_id'] for r in trs] + list(rosters.get(str(team)) or [])[:16]))
                cands = []
                for p in players:
                    code = sp[p][0] if p in sp else None
                    if code is None:
                        try:
                            code = {'G': 0, 'D': 1, 'M': 5, 'F': 12}.get(_world_grp(p), 8)
                        except Exception:
                            code = 8
                    if code in POS_ASSIST:
                        cands.append((p, _name(p), POS_ASSIST.get(code, 0)))
                if not cands:
                    continue
                w = shared_weights(cands, assist=True)
                rng = random.Random(zlib.crc32(('rc29-ast:%s:%s:%s' % ((s or {}).get('season', 1), fixture, team)).encode()))
                keys = [c[0] for c in cands]
                for r in trs:
                    r['assist'] = 0
                index = {r['player_id']: r for r in trs}
                for _ in range(total):
                    p = rng.choices(keys, weights=[w[k] for k in keys], k=1)[0]
                    r = index.get(p)
                    if r is None:
                        r = dict(team_id=team, player_id=p, goal=0, assist=0)
                        rows.append(r)
                        index[p] = r
                    r['assist'] += 1
            # a team never has more scorers' goals than it scored in the match (and no more assists than goals)
            scored = {}
            for m in matches:
                scored[int(m['home_team_id'])] = scored.get(int(m['home_team_id']), 0) + int(m.get('home_goals') or 0)
                scored[int(m['away_team_id'])] = scored.get(int(m['away_team_id']), 0) + int(m.get('away_goals') or 0)
            for team, trs in by_team.items():
                cap = scored.get(team)
                if cap is None:
                    continue
                for key in ('goal', 'assist'):
                    total = sum(int(r.get(key) or 0) for r in trs)
                    limit = cap
                    if total > limit:
                        excess = total - limit
                        for r in sorted(trs, key=lambda r: int(r.get(key) or 0)):
                            take = min(excess, int(r.get(key) or 0))
                            r[key] = int(r.get(key) or 0) - take
                            excess -= take
                            if not excess:
                                break
            rows[:] = [r for r in rows if r.get('goal') or r.get('assist')]
        except Exception as exc:
            _state['errors'].append('round_stats %r' % (exc,))
        return rows
    stats._rc29_realism = True
    return stats


SCORE_POS = {'GK': 0.0, 'CB': 1.0, 'LB': 1.4, 'RB': 1.4, 'DMF': 1.4, 'CMF': 3.0, 'LMF': 5.0, 'RMF': 5.0, 'AMF': 6.0,
             'LWF': 8.0, 'RWF': 8.0, 'SS': 9.5, 'CF': 13.0}
ASSIST_POS = {'GK': 0.05, 'CB': 0.7, 'LB': 3.0, 'RB': 3.0, 'DMF': 2.0, 'CMF': 4.5, 'LMF': 5.5, 'RMF': 5.5, 'AMF': 7.5,
              'LWF': 7.0, 'RWF': 7.0, 'SS': 5.0, 'CF': 3.0}
SCORE_GRP = {'G': 0.0, 'D': 1.2, 'M': 3.0, 'F': 10.0}
ASSIST_GRP = {'G': 0.05, 'D': 2.0, 'M': 5.5, 'F': 5.0}


def _league_scorers(orig, wl):
    @functools.wraps(orig)
    def scorers(self, season, f, home, away, hg, ag):
        try:
            out = {}
            rng = random.Random(zlib.crc32(('rc29-lw:%s:%s:%s:%s:%s' % (self.cid, season, f, home, away)).encode()))
            for team, goals in ((home, hg), (away, ag)):
                if not goals:
                    continue
                sq = self.squad(team) or []
                gc, ac = [], []
                for row, share in sq:
                    pid = str(row.get('id'))
                    ca = float(row.get('ca') or 120) / 150.0
                    pos = row.get('pos')
                    pos_w = SCORE_POS.get(pos, SCORE_GRP.get(row.get('grp'), 1.0))
                    gc.append((pid, row.get('name'), pos_w * share * ca ** 3))
                    ac.append((pid, row.get('name'), ASSIST_POS.get(pos, ASSIST_GRP.get(row.get('grp'), 1.0)) * share * ca ** 3))
                if not gc:
                    continue
                gw, aw = shared_weights(gc), shared_weights(ac, assist=True)
                gk, ak = [c[0] for c in gc], [c[0] for c in ac]
                for k in range(int(goals)):
                    sc = spread_pick(gk, [gw[x] for x in gk], season_u('g:%s:%s:%s' % (self.cid, season, team), f, k))
                    out.setdefault((team, sc), [0, 0])[0] += 1
                    if rng.random() < 0.78:
                        opts = [x for x in ak if x != sc]
                        if opts:
                            hp = spread_pick(opts, [aw[x] for x in opts], season_v('a:%s:%s:%s' % (self.cid, season, team), f, k))
                            out.setdefault((team, hp), [0, 0])[1] += 1
            return [[t, p, g, a] for (t, p), (g, a) in out.items()]
        except Exception as exc:
            _state['errors'].append('league_scorers %r' % (exc,))
            return orig(self, season, f, home, away, hg, ag)
    scorers._rc29_realism = True
    return scorers


def _sim_weight(orig, assist):
    @functools.wraps(orig)
    def weight(r):
        w = orig(r)
        try:
            st = star_of(r.get('name') or _name(r.get('pid') or r.get('player_id') or ''))
            if st:
                share = st[1] if assist else st[0]
                w *= max(0.5, 1.0 + 9.0 * (share - (0.16 if not assist else 0.10)))
            elif not assist:
                pos = str(r.get('pos') or r.get('position') or '')
                if pos in ('CF', 'SS', '11', '12') or r.get('grp') == 'F':
                    w *= 0.6      # a forward who is not a proven scorer does not take 25+ goals a season
        except Exception:
            pass
        return w
    weight._rc29_realism = True
    return weight


# ---------------------------------------------------------------- install
def _sim_events(orig, S):
    @functools.wraps(orig)
    def events(rows, goals, rng, *a, **k):
        try:
            rows = list(rows)
            sw, aw = S._score_weight, S._assist_weight
            gc = [(i, r.get('name') or _name(r.get('pid') or r.get('player_id') or ''), sw(r)) for i, r in enumerate(rows)]
            ac = [(i, n, aw(r)) for (i, n, _), r in zip(gc, rows)]
            gw, aww = shared_weights(gc), shared_weights(ac, assist=True)
            ids = {id(r): i for i, r in enumerate(rows)}
            S._score_weight = lambda r: gw.get(ids.get(id(r)), sw(r))
            S._assist_weight = lambda r: aww.get(ids.get(id(r)), aw(r))
            try:
                return orig(rows, goals, rng, *a, **k)
            finally:
                S._score_weight, S._assist_weight = sw, aw
        except Exception as exc:
            _state['errors'].append('sim_events %r' % (exc,))
            return orig(rows, goals, rng, *a, **k)
    events._rc29_realism = True
    return events


def _sim_process(orig):
    """Our simulated matches (V32 chances-v1): keep every shot, minute and the score, but the goals and assists go to players by
    their real share of the team's goals (stars by their known share, everybody else by position x ability, nobody but a
    proven scorer above ~14%)."""
    @functools.wraps(orig)
    def process(*a, **k):
        out = orig(*a, **k)
        try:
            rng = a[6] if len(a) > 6 else k.get('rng') or random.Random()
            teams, goals, tl = out.get('teams') or [], out.get('goals') or [], out.get('timeline') or []
            for side in (0, 1):
                if side >= len(goals) or not goals[side]:
                    continue
                rows = teams[side]
                evs = [t for t in tl if t.get('outcome') == 'goal' and t.get('side') == side]
                new_goals = []
                for gi, g in enumerate(goals[side]):
                    ev = evs[gi] if gi < len(evs) else None
                    m = float(ev['minute']) if ev else 45.0
                    on = [r for r in rows if r.get('group') != 'GK' and float(r.get('start', 0)) <= m <= float(r.get('end', 90))] or [r for r in rows if r.get('group') != 'GK']
                    if not on:
                        new_goals.append(g)
                        continue
                    ca = lambda r: (float(r.get('ca') or 120) / 150.0) ** 3
                    gc = [(i, r.get('name'), SCORE_POS.get(r.get('position'), 1.0) * ca(r)) for i, r in enumerate(on)]
                    gw = shared_weights(gc)
                    sc = on[spread_pick([c[0] for c in gc], [gw[c[0]] for c in gc], rng.random())]
                    ast = None
                    if g[1] is not None or rng.random() < 0.75:
                        others = [(i, r.get('name'), ASSIST_POS.get(r.get('position'), 1.0) * ca(r)) for i, r in enumerate(on) if r is not sc]
                        if others:
                            aw = shared_weights(others, assist=True)
                            idx = spread_pick([c[0] for c in others], [aw[c[0]] for c in others], rng.random())
                            ast = on[idx]
                    for row, key in ((g[0], 'goals'), (g[1], 'assists')):
                        st = (row or {}).get('stats') if isinstance(row, dict) else None
                        if isinstance(st, dict) and isinstance(st.get(key), (int, float)) and st[key] > 0:
                            st[key] -= 1
                    for row, key in ((sc, 'goals'), (ast, 'assists')):
                        st = (row or {}).get('stats') if isinstance(row, dict) else None
                        if isinstance(st, dict) and isinstance(st.get(key), (int, float)):
                            st[key] += 1
                    if ev is not None:
                        ev['player'] = sc.get('key')
                        ev['assist'] = ast.get('key') if ast else None
                    new_goals.append((sc, ast))
                goals[side] = new_goals
        except Exception as exc:
            _state['errors'].append('sim_process %r' % (exc,))
        return out
    process._rc29_realism = True
    return process


def _patch(mod, name, new):
    setattr(mod, name, new)
    _state['patched'].append('%s.%s' % (getattr(mod, '__name__', mod), name))


def install():
    if _state['installed']:
        return _state
    import importlib
    def mod(n):
        try:
            return importlib.import_module(n)
        except Exception as exc:
            _state['errors'].append('import %s %r' % (n, exc))
            return None
    ml = mod('my_league')
    if ml is not None:
        _patch(ml, 'cpu_score', _cpu_score(ml.cpu_score))
        _patch(ml, '_sim_scorer', _sim_scorer(ml._sim_scorer, ml))
        _patch(ml, '_cpu_round_stats', _round_stats(ml._cpu_round_stats, ml))
    wl = mod('iml_world_leagues')
    if wl is not None:
        _patch(wl.LeagueWorld, 'scorers', _league_scorers(wl.LeagueWorld.scorers, wl))
    sim = mod('iml_sim')
    if sim is not None:
        _patch(sim, '_score_weight', _sim_weight(sim._score_weight, False))
        if hasattr(sim, 'match_process') and not getattr(sim.match_process, '_rc29_realism', False):
            _patch(sim, 'match_process', _sim_process(sim.match_process))
        if not getattr(sim.events, '_rc29_realism', False):
            _patch(sim, 'events', _sim_events(sim.events, sim))
        _patch(sim, '_assist_weight', _sim_weight(sim._assist_weight, True))
        try:
            sim.SCORE_W.update({'LWF': 6.0, 'RWF': 6.0, 'AMF': 5.0, 'SS': 9.0, 'CF': 14.0, 'LMF': 3.5, 'RMF': 3.5, 'CMF': 2.5, 'DMF': 1.0})
        except Exception:
            pass
        _patch(sim, 'form_offset', lambda results: 2.0 * float(getattr(sim, 'OPP_FORM_CA', 2.0)) / 2.0)
    # ---- structure: five top divisions only
    st = mod('iml_second_tier')
    if st is not None:
        st.LEAGUES = {}
        st.TEAMS = {}
        _patch(st, 'competitions', lambda: {})
    nl = mod('iml_news_leagues')
    if nl is not None:
        nl.LEAGUES = {k: v for k, v in nl.LEAGUES.items() if k in TOP5}
        nl.SECOND_TIERS = {}
    pr = mod('iml_promotion')
    if pr is not None:
        pr.PAIRS = ()
        _patch(pr, 'plan', lambda conn, s, final_only=True: {'season': (s or {}).get('season'), 'moves': [], 'skipped': [], 'mine': None, 'pairs': []})
        _patch(pr, 'settle', lambda conn, s: {'ok': True, 'season': (s or {}).get('season'), 'moves': [], 'disabled': True})
        _patch(pr, 'zones', lambda cid: {'up': [], 'down': [], 'up_to': None, 'down_to': None})
    ui = mod('iml_ui')
    if ui is not None:
        ui.PICKER_LEAGUES = tuple(c for c in ui.PICKER_LEAGUES if c in TOP5)
    # ---- no ageing, retirement or academy
    yo = mod('iml_youth')
    if yo is not None:
        _patch(yo, 'youth_days', lambda season: [])
        _patch(yo, 'intake', lambda conn, s, day, window=None: {'news': [], 'drawn': [], 'disabled': True})
        _patch(yo, 'cpu_intake', lambda conn, s, window, day: {})
        _patch(yo, 'retirement_plan', lambda conn, s: [])
    w = mod('iml_world')
    if w is not None:
        w.RETIRE_P = {}
        w.FREE_RETIRE_P = 0.0
        w.P_RESIGN_CORE = w.P_RESIGN_REST = w.P_RESIGN_YOUNG = 1.0
        w.ARRIVALS_PER_RETIREE = 0.0
        _patch(w, '_add_youth', lambda *a, **k: None)
        age_of = w.age_of
        _patch(w, 'age_of', lambda p, on: age_of(p, datetime.date(2026, 7, 1)))
        # transfers: rare and plausible
        w.DAY_P, w.LATE_P, w.SECOND_P = 0.05, 0.12, 0.0
        w.CLUB_WINDOW_LIMIT = 1
        w.CORE_RANK = 16
        seller_ok = w._seller_ok
        def _seller(world, p, season, buyer, seller, r):
            if not seller_ok(world, p, season, buyer, seller, r):
                return False
            try:
                value = float(p.get('value') or 0)
                sid, bid = int(seller.get('id') or p.get('club') or 0), int(buyer.get('id') or 0)
                if value >= 60 and r.random() > 0.08:
                    return False
                if sid in R.CLUBS and bid in R.CLUBS and R.CLUBS[sid][0] >= 1.6 and R.CLUBS[bid][0] >= 1.6 and value >= 35:
                    return False
            except Exception:
                pass
            return True
        _patch(w, '_seller_ok', _seller)
    ab = mod('iml_ability')
    if ab is not None:
        _patch(ab, 'grow_ca', lambda key, season, ca, pa, age: ca)
        _patch(ab, 'grow_youth', lambda key, season, ca, pa: ca)
    ro = mod('iml_rollover')
    if ro is not None:
        _patch(ro, '_age_squad', lambda conn: 0)
    gr = mod('iml_growth')
    if gr is not None:
        _patch(gr, 'age', lambda doc: 26)
    if wl is not None:
        wl.XL_DAY_P, wl.XL_LATE_P, wl.XL_SECOND_P = 0.02, 0.05, 0.0
        wl.XL_CLUB_LIMIT = 1
    # ---- form and difficulty
    fm = mod('iml_form')
    if fm is not None:
        _patch(fm, 'grade_of', lambda x: 4)
    se = mod('iml_season')
    if se is not None:
        chosen = se.chosen_level
        def chosen_level(conn):
            v = chosen(conn)
            return v if v not in (None, 'AUTO') else 'LEGEND'
        _patch(se, 'chosen_level', chosen_level)
    _install_europe()
    _state['installed'] = True
    return _state


def status():
    return dict(_state, patched=list(_state['patched']), errors=list(_state['errors'][-20:]))


# ---------------------------------------------------------------- European cups
FORCE_UCL = (130, 197, 191, 193)   # Galatasaray, Fenerbahçe, Benfica, Sporting always play the Champions League


def _qualify(orig):
    @functools.wraps(orig)
    def qualify(s, prev, offs, rng):
        out = orig(s, prev, offs, rng)
        try:
            ucl, uel = list(out.get('ucl') or []), list(out.get('uel') or [])
            in_ucl = {int(e[0]) for e in ucl}
            for team in FORCE_UCL:
                if team in in_ucl:
                    continue
                entry = next((e for e in uel if int(e[0]) == team), None)
                if entry is not None:
                    uel.remove(entry)
                    entry = (team, entry[1], 'UCL')
                else:
                    entry = (team, R.LEAGUE_OF.get(str(team), 900307), 'UCL')
                # the weakest club placed from outside the five leagues (else the last entry) makes room
                cand = [e for e in ucl if int(e[0]) not in FORCE_UCL and int(e[1] if not isinstance(e[1], str) else 0) not in TOP5]
                drop = cand[-1] if cand else next(e for e in reversed(ucl) if int(e[0]) not in FORCE_UCL)
                ucl.remove(drop)
                ucl.append(entry)
                uel.append(drop)
                in_ucl.add(team)
            while len(uel) > 36:
                uel.pop()
            out['ucl'], out['uel'] = ucl, uel
        except Exception as exc:
            _state['errors'].append('qualify %r' % (exc,))
        return out
    qualify._rc29_realism = True
    return qualify


def cup_squad(conn, team, cache):
    """[(key, name, pos, weight)] of a club's living Master League squad (transfers, the editor, ability) for the European sheets."""
    team = int(team)
    if team in cache:
        return cache[team]
    rows = []
    try:
        import iml_world as IW, iml_world_leagues as W, my_league
        s = my_league.state(conn) or {}
        own = int(s.get('competition_id') or 113)
        lg = R.LEAGUE_OF.get(str(team))
        ps = []
        if lg is not None and int(lg) == own:
            w = IW.load(conn) or {}
            ps = [p for p in (w.get('players') or {}).values() if p.get('status') == 'active' and str(p.get('club')) == str(team)]
        else:
            for cid in ([int(lg)] if lg is not None else []) + [900307, 119, 116, 122]:
                w = W.load(conn, cid) or {}
                ps = [p for p in (w.get('players') or {}).values() if p.get('status') == 'active' and str(p.get('club')) == str(team)]
                if ps:
                    break
        ps.sort(key=lambda p: -float(p.get('ca') or 0))
        grp_pos = {'G': 'GK', 'D': 'CB', 'M': 'CMF', 'F': 'CF'}
        for i, p in enumerate(ps[:18]):
            ca = float(p.get('ca') or 120) / 150.0
            rows.append(('w%s' % p.get('id'), p.get('name'), p.get('pos') or grp_pos.get(p.get('grp'), 'CMF'), (1.0 if i < 11 else 0.3) * ca ** 3))
    except Exception:
        rows = []
    if not rows:
        try:
            import ziru_data, my_league as ml
            ids = list(dict.fromkeys(ziru_data.rosters().get(str(team)) or []))
            pos_names = ('GK', 'CB', 'LB', 'RB', 'DMF', 'CMF', 'LMF', 'RMF', 'AMF', 'LWF', 'RWF', 'SS', 'CF')
            for i, p in enumerate(ids[:16]):
                code = ml.SIM_PLAYERS.get(p, (None,))[0]
                if code is None:
                    continue
                rows.append(('n%s' % p, _name(p), pos_names[code] if 0 <= code < 13 else 'CMF', 1.0 if i < 11 else 0.3))
        except Exception:
            rows = []
    cache[team] = rows
    return rows


UCL_STAR_BOOST = 1.3      # the elite finishers carry their side in Europe even more (Kane / Haaland / Mbappe: 10-14 a campaign)


def cup_weights(cands, assist=False):
    """shared_weights for a European cup: a leading scorer (league share >= 25%) gets 30% more of his side's European goals."""
    if assist:
        return shared_weights(cands, assist=True)
    boosted = []
    for key, name, w in cands:
        st = star_of(name)
        boosted.append((key, name, w))
    out = shared_weights(boosted)
    total = sum(out.values()) or 1.0
    for key, name, w in cands:
        st = star_of(name)
        if st and st[0] >= 0.25:
            share = min(0.42, st[0] * UCL_STAR_BOOST)
            cur = out[key] / total
            if cur < share:
                out[key] = share / max(1e-6, 1 - share) * (total - out[key])
    return out


def cup_stats(conn, comp, own=None):
    """Scorer / assist tables of one European cup from every played leg (ours: the real sheet; the rest: a seeded sheet)."""
    goals, assists, teams_of = {}, {}, {}
    cache = {}
    seen = {}
    legs = []
    for md in comp.get('matchdays') or []:
        legs.extend(md.get('matches') or [])
    for rnd in comp.get('ko') or []:
        for tie in rnd.get('ties') or []:
            legs.extend(tie.get('legs') or [])
    for leg in legs:
        hg, ag = leg.get('hg'), leg.get('ag')
        if hg is None or ag is None:
            continue
        if leg.get('mine') and leg.get('scorers'):
            for g in leg['scorers']:
                n = g.get('name') or ''
                if not n:
                    continue
                side = g.get('team')
                if side is None:
                    side = own if own is not None and not g.get('opp') else (leg.get('away') if leg.get('home') == own else leg.get('home'))
                goals[n] = goals.get(n, 0) + 1
                teams_of[n] = side
                if g.get('assist'):
                    assists[g['assist']] = assists.get(g['assist'], 0) + 1
                    teams_of[g['assist']] = side
            continue
        key = 'rc29-cup:%s:%s:%s:%s:%s' % (comp.get('id'), leg.get('id') or leg.get('date'), leg.get('home'), leg.get('away'), hg)
        rng = random.Random(zlib.crc32(key.encode()))
        for team, n in ((leg.get('home'), hg), (leg.get('away'), ag)):
            if not n or team is None:
                continue
            sq = cup_squad(conn, team, cache)
            if not sq:
                continue
            gc = [(k, nm, SCORE_POS.get(pos, 2.0) * sh) for k, nm, pos, sh in sq]
            ac = [(k, nm, ASSIST_POS.get(pos, 2.0) * sh) for k, nm, pos, sh in sq]
            gw, aw = cup_weights(gc), cup_weights(ac, assist=True)
            name_of = {k: nm for k, nm, pos, sh in sq}
            gk = [c[0] for c in gc]
            seen[team] = seen.get(team, 0) + 1
            for gi in range(int(n)):
                sc = spread_pick(gk, [gw[k] for k in gk], season_u('ucl:%s:%s' % (comp.get('id'), team), seen[team], gi))
                nm = name_of[sc]
                goals[nm] = goals.get(nm, 0) + 1
                teams_of.setdefault(nm, team)
                if rng.random() < 0.78:
                    opts = [k for k in gk if k != sc]
                    if opts:
                        hp = rng.choices(opts, weights=[aw[k] for k in opts], k=1)[0]
                        an = name_of[hp]
                        assists[an] = assists.get(an, 0) + 1
                        teams_of.setdefault(an, team)
    def table(d):
        rows = sorted(d.items(), key=lambda x: (-x[1], x[0]))[:30]
        return [{'rank': i + 1, 'name': n, 'team': teams_of.get(n), 'n': v} for i, (n, v) in enumerate(rows)]
    return table(goals), table(assists)


def _europe_view(orig):
    @functools.wraps(orig)
    def view(conn, s=None):
        out = orig(conn, s)
        try:
            for c in (out or {}).get('comps') or []:
                c['scorers'], c['assists'] = cup_stats(conn, c, (out or {}).get('team'))
        except Exception as exc:
            _state['errors'].append('europe_view %r' % (exc,))
        return out
    view._rc29_realism = True
    return view


def _install_europe():
    import importlib
    try:
        E = importlib.import_module('iml_europe')
    except Exception as exc:
        _state['errors'].append('import iml_europe %r' % (exc,))
        return
    _patch(E, 'qualify', _qualify(E.qualify))
    _patch(E, 'view', _europe_view(E.view))
    try:
        E.NOT_IN_EUROPE = set(E.NOT_IN_EUROPE)
    except Exception:
        pass
