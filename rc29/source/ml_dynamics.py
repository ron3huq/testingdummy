"""RC29.5 long-term Master League: the football world moves on from season to season.

Season 1 is the hand-tuned picture of today (ml_ratings: Arsenal dominant, Kane / Haaland / Mbappe goal shares...).
From season 2 on, every rollover writes one more page into meta `rc29_dyn_v1`:

  * club strength  = hand-tuned rating x drift x squad
      drift  - a mean-reverting random walk per club (clubs have good and bad eras: x prev^0.6 x e^N(0, 0.07))
      squad  - the club's living squad in the V32 world (transfers, CPU deals, the Master League editor) against the squad it
               started the career with: attack from the best forwards / midfielders, defence from the back line and keeper
  * star scorers   - each leading player's goal / assist share drifts too (x prev^0.65 x e^N(0, 0.16), 0.55..1.35), so
                     the Golden Boot race changes hands; a star who moves club takes his share with him (shares follow the player)
  * emerging stars - every summer up to six high-ability forwards / attacking midfielders who are not yet stars break out
                     with a real share of their club's goals; they keep developing or fade like everybody else
  * player ability - the scorer sheets weight every player by his current ability (CA^3), so an edited or improved player
                     scores more at once, a weakened one less.

Everything is seeded from the career, the season and the club / player: the same save always tells the same story.
"""
import json, math, random, zlib

KEY = 'rc29_dyn_v1'
FORWARD = {'CF', 'SS', 'LWF', 'RWF', 'AMF'}
_cache = {'season': None, 'doc': None, 'loaded': False}
_live = {'t': 0.0, 'players': {}, 'lines': {}}
GRP_OF = {'GK': 'G', 'CB': 'D', 'LB': 'D', 'RB': 'D', 'DMF': 'M', 'CMF': 'M', 'LMF': 'M', 'RMF': 'M', 'AMF': 'M', 'LWF': 'F', 'RWF': 'F', 'SS': 'F', 'CF': 'F'}
SCORER_POS = {'CF', 'SS', 'LWF', 'RWF', 'AMF', 'LMF', 'RMF'}


# ------------------------------------------------------------------ the living world, right now (edits and transfers count at once)
def _world_rows(conn):
    """{team: [(name, pos, ca)]} from the current Master League world files (our league + the four others)."""
    out = {}
    try:
        import iml_world as IW, iml_world_leagues as W, my_league
        s = my_league.state(conn) or {}
        worlds = [IW.load(conn)] + [W.load(conn, int(c)) for c in W.others(s)]
        for w in worlds:
            for p in ((w or {}).get('players') or {}).values():
                if p.get('status') != 'active' or p.get('club') is None:
                    continue
                pos = p.get('pos') or {'G': 'GK', 'D': 'CB', 'M': 'CMF', 'F': 'CF'}.get(p.get('grp'), 'CMF')
                out.setdefault(int(p['club']), []).append((p.get('name') or '', pos, float(p.get('ca') or 110)))
    except Exception:
        pass
    return out


def refresh(conn, force=False):
    """Re-read every club's squad and every player's ability (at most every 90 s, or at once after an edit)."""
    import time
    if not force and time.time() - _live['t'] < 90:
        return _live
    rows = _world_rows(conn)
    if not rows:
        return _live
    import ml_realism as M
    players = {}
    for team, rs in rows.items():
        for name, pos, ca in rs:
            k = M._norm(name)
            if k not in players or ca > players[k][0]:
                players[k] = (ca, pos, team)
    _live.update(t=time.time(), players=players, lines={t: _lines(sorted(rs, key=lambda r: -r[2])[:20]) for t, rs in rows.items()})
    _clear_star_cache()
    return _live


def live_ability(norm_name):
    return _live['players'].get(norm_name)


def _store():
    import iml_news_leagues as nl
    return nl.store


def load(conn):
    try:
        raw = _store().get_meta(conn, KEY)
        doc = json.loads(raw) if raw else {}
    except Exception:
        doc = {}
    _cache['doc'] = doc if isinstance(doc, dict) else {}
    _cache['loaded'] = True
    _clear_star_cache()
    return _cache['doc']


def save(conn, doc):
    _store().set_meta(conn, KEY, json.dumps(doc, separators=(',', ':')))
    try:
        conn.commit()
    except Exception:
        pass
    _cache['doc'] = doc
    _clear_star_cache()


def _clear_star_cache():
    try:
        import ml_realism
        ml_realism._star_cache.clear()
    except Exception:
        pass


def _page(season):
    doc = _cache['doc'] or {}
    return (doc.get('seasons') or {}).get(str(int(season))) if season is not None else None


def current_page():
    doc = _cache['doc'] or {}
    seasons = doc.get('seasons') or {}
    if not seasons:
        return None
    return seasons[max(seasons, key=int)]


def club_factor(team, season):
    """(attack x, defence x): the club's era (season drift, from season 2) x its squad NOW against the squad it started the career with."""
    p = _page(season)
    da, dd = 1.0, 1.0
    if p:
        f = (p.get('drift') or {}).get(str(int(team))) or (p.get('club') or {}).get(str(int(team)))
        if f:
            da, dd = f[0], f[1]
    sa = sd = 1.0
    base = ((_cache['doc'] or {}).get('base') or {}).get(str(int(team)))
    now = _live['lines'].get(int(team))
    if base and now and ((_cache['doc'] or {}).get('base_v') == 2):
        sa = max(0.75, min(1.3, math.exp((now[0] - base[0]) / 32.0)))
        sd = max(0.75, min(1.3, math.exp(-(now[1] - base[1]) / 32.0)))
    ov = ((_cache['doc'] or {}).get('club_ovr') or {}).get(str(int(team)))
    if ov:
        k = max(0.6, min(1.5, float(ov) / 100.0))
        return da * sa * k, dd * sd / k
    return da * sa, dd * sd


def _ability_factor(norm_name):
    """How much better / worse the player is now than when the career started: (CA now / CA then)^3, 0.45..1.35."""
    now = _live['players'].get(norm_name)
    then = ((_cache['doc'] or {}).get('base_ca') or {}).get(norm_name)
    if not now or not then:
        return 1.0
    return max(0.45, min(1.35, (now[0] / then) ** 3))


def implied_share(norm_name):
    """A player nobody listed as a scorer, who IS one by ability now (an edit, a breakout): his share by CA and position."""
    now = _live['players'].get(norm_name)
    if not now:
        return None
    ca, pos, team = now
    if pos not in SCORER_POS or ca < 168:
        return None
    g = min(0.30, 0.10 + (ca - 168) * 0.0085) * (1.0 if pos in ('CF', 'SS') else 0.7)
    a = min(0.18, 0.06 + (ca - 168) * 0.004) * (1.4 if pos in ('AMF', 'LWF', 'RWF', 'LMF', 'RMF') else 0.8)
    return (round(g, 4), round(a, 4))


def override(norm_name):
    """The user's own scoring role for a player (Editor -> Scoring role): (goal share, assist share) or None."""
    o = ((_cache['doc'] or {}).get('overrides') or {}).get(norm_name)
    return (float(o[0]), float(o[1])) if o else None


def set_club(conn, team, pct):
    doc = dict(_cache['doc'] if _cache['loaded'] else load(conn))
    co = dict(doc.get('club_ovr') or {})
    if pct is None or int(pct) == 100:
        co.pop(str(int(team)), None)
    else:
        co[str(int(team))] = max(60, min(150, int(pct)))
    doc['club_ovr'] = co
    save(conn, doc)
    return co.get(str(int(team)), 100)


def club_pct(team):
    return ((_cache['doc'] or {}).get('club_ovr') or {}).get(str(int(team)), 100)


def set_override(conn, norm_name, g, a):
    doc = dict(_cache['doc'] if _cache['loaded'] else load(conn))
    ov = dict(doc.get('overrides') or {})
    if g is None and a is None:
        ov.pop(norm_name, None)
    else:
        ov[norm_name] = [max(0.0, min(0.45, float(g or 0))), max(0.0, min(0.35, float(a or 0)))]
    doc['overrides'] = ov
    save(conn, doc)
    return ov.get(norm_name)


def star_adjust(norm_name, base):
    """(goal share, assist share) of a player now: his known share x his season form x how his ability changed (edits count at once);
    a player who became a scorer by ability gets an implied share; nobody passes 36% of his team's goals."""
    p = current_page()
    abil = _ability_factor(norm_name)
    if base:
        m = (p.get('star') or {}).get(norm_name) if p else None
        m = max(0.85, min(1.15, m)) if m else 1.0
        return (min(0.36, base[0] * m * abil), min(0.24, base[1] * m * abil))
    e = (p.get('new') or {}).get(norm_name) if p else None
    if e:
        return (min(0.36, e[0] * abil), min(0.24, e[1] * abil))
    return implied_share(norm_name)


# ------------------------------------------------------------------ the summer: write next season's page
def _squads(conn):
    """{team: [(name, pos, ca)]} from the living world of every league."""
    out = {}
    try:
        import iml_world_leagues as wl, ml_ratings as R
        for cid in sorted({int(v) for v in R.LEAGUE_OF.values()} | {113, 119, 116, 122, 900307}):
            try:
                lw = wl.open_league(conn, cid)
            except Exception:
                lw = None
            if lw is None:
                continue
            for t in [int(k) for k, v in R.LEAGUE_OF.items() if int(v) == cid]:
                if t in out:
                    continue
                try:
                    sq = lw.squad(t) or []
                except Exception:
                    sq = []
                if sq:
                    out[t] = [(r.get('name') or '', r.get('pos') or 'CMF', float(r.get('ca') or 110)) for r, share in sq]
    except Exception:
        pass
    return out


def _lines(rows):
    by = {'G': [], 'D': [], 'M': [], 'F': []}
    grp = {'GK': 'G', 'CB': 'D', 'LB': 'D', 'RB': 'D', 'DMF': 'M', 'CMF': 'M', 'LMF': 'M', 'RMF': 'M', 'AMF': 'M', 'LWF': 'F', 'RWF': 'F', 'SS': 'F', 'CF': 'F'}
    for name, pos, ca in rows:
        by[grp.get(pos, 'M')].append(ca)
    top = lambda xs, n, d: (sum(sorted(xs, reverse=True)[:n]) + d * max(0, n - len(xs))) / n
    f, m, d, g = top(by['F'], 3, 105), top(by['M'], 3, 105), top(by['D'], 4, 105), top(by['G'], 1, 105)
    return 0.7 * f + 0.3 * m, 0.55 * d + 0.25 * g + 0.2 * m


def ensure_base(conn):
    doc = _cache['doc'] if _cache['loaded'] else load(conn)
    if doc.get('base') and doc.get('base_v') == 2:
        return doc
    live = refresh(conn, force=True)
    if not live['lines']:
        return doc
    doc = dict(doc, base={str(t): list(v) for t, v in live['lines'].items()}, base_ca={k: v[0] for k, v in live['players'].items()},
               base_v=2, seasons=doc.get('seasons') or {})
    save(conn, doc)
    return doc


def rollover(conn, old_season):
    """Called when season `old_season` ends: write the page of season old_season + 1."""
    import ml_realism as M, ml_ratings as R
    doc = ensure_base(conn)
    new = str(int(old_season) + 1)
    seasons = doc.setdefault('seasons', {})
    if new in seasons:
        return seasons[new]
    prev = seasons.get(str(int(old_season))) or {}
    seed = doc.setdefault('seed', random.randrange(1, 10 ** 9))
    rnd = lambda *k: random.Random(zlib.crc32(':'.join(map(str, (seed,) + k)).encode()))
    sq = _world_rows(conn)
    base = doc.get('base') or {}
    club, drift = {}, {}
    for t in set(R.CLUBS) | {int(x) for x in sq}:
        pa, pd = ((prev.get('drift') or {}).get(str(t)) or [1.0, 1.0])
        r = rnd('club', new, t)
        da = max(0.78, min(1.25, pa ** 0.6 * math.exp(r.gauss(0, 0.07))))
        dd = max(0.78, min(1.25, pd ** 0.6 * math.exp(r.gauss(0, 0.07))))
        club[str(t)] = [round(da, 4), round(dd, 4)]      # the squad part is read live (club_factor)
        drift[str(t)] = [round(da, 4), round(dd, 4)]
    star = {}
    for keys, g, a in M._STAR_KEYS:
        k = keys[0]
        pm = (prev.get('star') or {}).get(k, 1.0)
        star[k] = round(max(0.85, min(1.15, pm ** 0.5 * math.exp(rnd('star', new, k).gauss(0, 0.07)))), 4)
    # emerging stars: keep last year's (with drift), then add new ones up to six
    newer = {}
    for k, (g, a) in (prev.get('new') or {}).items():
        rr = rnd('new', new, k)
        m = math.exp(rr.gauss(0.0, 0.2))
        if g * m >= 0.09 and rr.random() < 0.72:
            newer[k] = [round(min(0.34, g * m), 4), round(min(0.2, a * m), 4)]
    pool = []
    for t, rows in sq.items():
        for name, pos, ca in rows:
            n = M._norm(name)
            if pos in FORWARD and ca >= 128 and n not in newer and not any(any((' ' + x + ' ') in (' ' + n + ' ') for x in keys) for keys, _, _ in M._STAR_KEYS):
                pool.append((ca, n))
    pool.sort(reverse=True)
    r = rnd('break', new)
    added = 0
    for ca, n in pool[:60]:
        if len(newer) >= 10 or added >= 3:
            break
        if (prev.get('gone') or {}).get(n):
            continue
        if r.random() < 0.12 + (ca - 128) / 80.0:
            newer[n] = [round(0.14 + r.random() * 0.1, 4), round(0.05 + r.random() * 0.07, 4)]
            added += 1
    seasons[new] = {'club': club, 'drift': drift, 'star': star, 'new': newer}
    save(conn, doc)
    return seasons[new]


def summary():
    """For the UI / news: who rose, who fell, who broke out this season."""
    p = current_page()
    if not p:
        return {}
    st = sorted((p.get('star') or {}).items(), key=lambda kv: kv[1])
    return {'risers': st[-3:][::-1], 'fallers': st[:3], 'breakouts': list((p.get('new') or {}).items())[:6]}
