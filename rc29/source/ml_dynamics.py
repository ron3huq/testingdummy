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
    """(attack x, defence x) of a club in a season; (1, 1) in season 1 or before any rollover."""
    p = _page(season)
    if not p:
        return 1.0, 1.0
    f = (p.get('club') or {}).get(str(int(team)))
    return (f[0], f[1]) if f else (1.0, 1.0)


def star_adjust(norm_name, base):
    """Season-adjusted (goal share, assist share) for a player; base = the hand-tuned share or None."""
    p = current_page()
    if not p:
        return base
    if base:
        m = (p.get('star') or {}).get(norm_name)
        return (base[0] * m, base[1] * m) if m else base
    e = (p.get('new') or {}).get(norm_name)
    return (e[0], e[1]) if e else None


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
    if doc.get('base'):
        return doc
    sq = _squads(conn)
    if not sq:
        return doc
    doc = dict(doc, base={str(t): list(_lines(rows)) for t, rows in sq.items()}, seasons=doc.get('seasons') or {})
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
    sq = _squads(conn)
    base = doc.get('base') or {}
    club, drift = {}, {}
    for t in set(R.CLUBS) | {int(x) for x in sq}:
        pa, pd = ((prev.get('drift') or {}).get(str(t)) or [1.0, 1.0])
        r = rnd('club', new, t)
        da = max(0.78, min(1.25, pa ** 0.6 * math.exp(r.gauss(0, 0.07))))
        dd = max(0.78, min(1.25, pd ** 0.6 * math.exp(r.gauss(0, 0.07))))
        sa = sd = 1.0
        if str(t) in base and t in sq:
            a0, d0 = base[str(t)]
            a1, d1 = _lines(sq[t])
            sa = max(0.75, min(1.3, math.exp((a1 - a0) / 25.0)))
            sd = max(0.75, min(1.3, math.exp(-(d1 - d0) / 25.0)))
        club[str(t)] = [round(da * sa, 4), round(dd * sd, 4)]
        drift[str(t)] = [round(da, 4), round(dd, 4)]
    star = {}
    for keys, g, a in M._STAR_KEYS:
        k = keys[0]
        pm = (prev.get('star') or {}).get(k, 1.0)
        star[k] = round(max(0.55, min(1.35, pm ** 0.65 * math.exp(rnd('star', new, k).gauss(0, 0.16)))), 4)
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
