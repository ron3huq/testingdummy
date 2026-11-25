"""RC29.3: Ballon d'Or and European Golden Shoe for the Master League.

At the end of a season (iml_rollover.advance, before the boundary) the season's numbers are frozen into meta `rc29_awards_v1`:
league goals / assists of the five leagues, Champions League / Europa League goals / assists, and team honours.
The vote is modelled on the real one: individual output first (goals, assists), the Champions League weighted most, team trophies
(league title, Champions League run, Europa League), and a little reputation for the established stars.
The calendar of the following season reveals it like the real award: the 30 nominees on 8 August, the ceremony on 22 September.
GET /api/rc29/awards -> {'latest': {...with 'phase'}, 'history': [...]}.
"""
import json, datetime, functools
KEY = 'rc29_awards_v1'
TOP5 = (113, 119, 116, 900307, 122)
NOMINEES_DAY = (8, 8)
CEREMONY_DAY = (9, 22)


def _store():
    import iml_news_leagues as nl
    return nl.store


def load(conn):
    try:
        return json.loads(_store().get_meta(conn, KEY, '') or '{}') or {}
    except Exception:
        return {}


def save(conn, doc):
    _store().set_meta(conn, KEY, json.dumps(doc, ensure_ascii=False))


def _team_name(t):
    try:
        import iml_leagues as L
        d = L._team(int(t)) or {}
        return d.get('latin') or d.get('name') or str(t)
    except Exception:
        return str(t)


def _league_rows(conn, s):
    """{name: {'team', 'lg', 'g', 'a'}} of every league, plus {cid: champion team}."""
    import iml_leagues as L
    import iml_news_leagues as nl
    import ml_realism as M
    players, champions, names = {}, {}, {}
    def add(name, team, cid, g=0, a=0, pid=None):
        if not name:
            return
        p = players.setdefault(name, {'team': team, 'lg': cid, 'g': 0, 'a': 0, 'ug': 0, 'ua': 0, 'eg': 0, 'ea': 0, 'pid': None})
        if pid and not p.get('pid'):
            p['pid'] = pid
        p['g'] += g
        p['a'] += a
    own = int(s.get('competition_id') or 0)
    snaps = {}
    try:
        snaps = (nl.load(conn, s) or {}).get('leagues') or {}
    except Exception:
        snaps = {}
    for cid in TOP5:
        lg = snaps.get(str(cid))
        if cid != own and lg:
            pn = lg.get('pn') or {}
            for r, v in (lg.get('played') or {}).items():
                for row in v.get('ps') or []:
                    team, pid, g, a = row[0], str(row[1]), int(row[2] or 0), int(row[3] or 0)
                    name = pn.get(pid) or (M._name(pid) if pid.isdigit() else '')
                    add(name, team, cid, g, a, int(pid) if pid.isdigit() else None)
        top_was = getattr(L, 'TOP', 10)
        try:
            L.TOP = 999          # the whole season, not just the page's top 10 (assists of a 23-goal winger outside the top 10 counted as 0)
            page = L.view(conn, s, cid)
        except Exception:
            page = {}
        finally:
            L.TOP = top_was
        tbl = page.get('table') or []
        if tbl:
            champions[cid] = tbl[0].get('team')
        if cid == own:
            for kind, key in (('scorers', 'g'), ('assisters', 'a')):
                for row in page.get(kind) or []:
                    add(row.get('name'), row.get('team'), cid, pid=row.get('pid') or None, **{key: int(row.get('n') or 0)})
    return players, champions


def _cups(conn, s, players):
    import iml_europe as E
    honours = {}
    try:
        d = E.view(conn, s) or {}
    except Exception:
        d = {}
    for c in d.get('comps') or []:
        cid = c.get('id')
        gk, ak = ('ug', 'ua') if cid == 'ucl' else ('eg', 'ea')
        for kind, key in (('scorers', gk), ('assists', ak)):
            for row in c.get(kind) or []:
                p = players.setdefault(row['name'], {'team': row.get('team'), 'lg': None, 'g': 0, 'a': 0, 'ug': 0, 'ua': 0, 'eg': 0, 'ea': 0, 'pid': None})
                p[key] += int(row.get('n') or 0)
        reached = {}
        for rnd in c.get('ko') or []:
            for tie in rnd.get('ties') or []:
                for t in (tie.get('a'), tie.get('b')):
                    if isinstance(t, int):
                        reached[t] = rnd.get('stage')
        if c.get('champion'):
            reached[c['champion']] = 'won'
        honours[cid] = reached
    return honours


def _abilities(conn, s):
    """{normalised name: current ability} over every league's world."""
    import ml_realism as M
    out = {}
    try:
        import iml_world as IW, iml_world_leagues as W
        worlds = [IW.load(conn)] + [W.load(conn, int(c)) for c in W.others(s)]
        for w in worlds:
            for p in ((w or {}).get('players') or {}).values():
                if p.get('status') == 'active' and p.get('ca'):
                    k = M._norm(p.get('name'))
                    out[k] = max(out.get(k, 0), float(p['ca']))
    except Exception:
        pass
    return out


def compute(conn, s):
    players, champions = _league_rows(conn, s)
    cups = _cups(conn, s, players)
    import ml_realism as M
    stage_pts = {'won': 55, 'final': 26, 'sf': 13, 'qf': 6, 'r16': 2}
    ability = _abilities(conn, s)
    import ml_ratings as R
    rows = []
    for name, p in players.items():
        team = p.get('team')
        trophies = []
        pts = 4.0 * p['g'] + 2.6 * p['a'] + 7.0 * p['ug'] + 3.6 * p['ua'] + 1.5 * p['eg'] + 0.8 * p['ea']
        if team is not None and team in champions.values():
            pts += 30
            trophies.append('League title')
        st = (cups.get('ucl') or {}).get(team)
        if st:
            pts += stage_pts.get(st, 0)
            if st == 'won':
                trophies.append('Champions League')
        if (cups.get('uel') or {}).get(team) == 'won':
            pts += 12
            trophies.append('Europa League')
        star = M.star_of(name)
        if star:
            pts += 55 * star[0] + 30 * star[1]
        # the jury votes for the world's best players at the biggest clubs, not just for a lucky season
        ca = ability.get(M._norm(name))
        if ca:
            pts += 3.2 * max(0.0, ca - 150) - 2.0 * max(0.0, 150 - ca)
        att = (R.CLUBS.get(int(team)) or (1.3,))[0] if team is not None else 1.3
        pts *= max(0.72, min(1.15, 0.62 + 0.2 * att))
        if pts <= 0 or (ca and ca < 145):
            continue
        if st and st != 'won':
            trophies.append({'final': 'UCL runner-up', 'sf': 'UCL semi-final', 'qf': 'UCL quarter-final', 'r16': 'UCL last 16'}.get(st, 'UCL'))
        rows.append({'name': name, 'pid': p.get('pid'), 'team': team, 'club': _team_name(team) if team is not None else '', 'goals': p['g'], 'assists': p['a'],
                     'ucl_goals': p['ug'], 'ucl_assists': p['ua'], 'trophies': trophies, 'points': round(pts, 1),
                     'ucl': (cups.get('ucl') or {}).get(team)})
    rows.sort(key=lambda r: (-r['points'], -r['goals']))
    top = rows[:30]
    total = sum(r['points'] for r in top) or 1
    for i, r in enumerate(top):
        r['rank'] = i + 1
        r['votes'] = int(round(r['points'] / total * 1200))   # a points tally like the jury's
    league_top = {}
    for n, p in players.items():
        if p.get('lg') and p['g'] > league_top.get(p['lg'], ('', 0))[1]:
            league_top[p['lg']] = (n, p['g'])
    tops = {n for n, g in league_top.values()}
    for r in rows:
        if r['name'] in tops:
            r['trophies'].append('League top scorer')
    boot = sorted(({'name': n, 'pid': p.get('pid'), 'team': p['team'], 'club': _team_name(p['team']) if p['team'] is not None else '', 'goals': p['g'],
                    'points': p['g'] * 2} for n, p in players.items() if p['g'] > 0), key=lambda r: (-r['goals'], r['name']))[:10]
    for i, r in enumerate(boot):
        r['rank'] = i + 1
    season = int(s.get('season') or 1)
    return {'season': season, 'label': '%d/%02d' % (2025 + season, (26 + season) % 100), 'ballon_dor': top, 'golden_boot': boot,
            'champions': {str(k): v for k, v in champions.items()}, 'ucl_winner': next((t for t, st in (cups.get('ucl') or {}).items() if st == 'won'), None)}


def record(conn, s):
    doc = load(conn)
    seasons = doc.setdefault('seasons', {})
    key = str(int(s.get('season') or 1))
    if key in seasons:
        return seasons[key]
    seasons[key] = compute(conn, s)
    save(conn, doc)
    return seasons[key]


def phase_of(award, today):
    if today is None:
        return 'pending'
    y = 2026 + int(award['season'])
    if today >= datetime.date(y, *CEREMONY_DAY):
        return 'ceremony'
    if today >= datetime.date(y, *NOMINEES_DAY):
        return 'nominees'
    return 'pending'


def api(conn, s):
    import iml_calendar as C
    doc = load(conn)
    seasons = doc.get('seasons') or {}
    try:
        today = C.today(conn, s)
    except Exception:
        today = None
    out = []
    for k in sorted(seasons, key=int):
        a = dict(seasons[k])
        a['phase'] = phase_of(a, today)
        a['nominees_date'] = '%d-%02d-%02d' % (2026 + a['season'], *NOMINEES_DAY)
        a['ceremony_date'] = '%d-%02d-%02d' % (2026 + a['season'], *CEREMONY_DAY)
        if a['phase'] != 'ceremony':
            # before the ceremony nobody knows the order: nominees alphabetically, no points
            a['ballon_dor'] = sorted(({'name': r['name'], 'pid': r.get('pid'), 'team': r['team'], 'club': r['club'], 'goals': r['goals'], 'assists': r['assists'],
                                       'ucl_goals': r['ucl_goals'], 'trophies': r['trophies']} for r in a['ballon_dor']), key=lambda r: r['name'])
        if a['phase'] == 'pending':
            a['ballon_dor'] = []
        out.append(a)
    visible = [a for a in out if a['phase'] != 'pending']
    teams = {}
    try:
        import iml_leagues as L
        for a in visible:
            for r in (a.get('ballon_dor') or []) + (a.get('golden_boot') or []):
                t = r.get('team')
                if t is not None and str(t) not in teams:
                    teams[str(t)] = L._team(int(t))
    except Exception:
        pass
    return {'teams': teams, 'latest': visible[-1] if visible else None, 'history': [a for a in visible if a['phase'] == 'ceremony'][::-1],
            'today': today.isoformat() if today else None}


def _goals_of(rows, home, away, nm):
    goals = []
    for team in (home, away):
        tr = [r for r in rows if int(r[0]) == team]
        scorers = [(nm(r[1]), r[1]) for r in tr for _ in range(int(r[2] or 0))]
        helpers = [(nm(r[1]), r[1]) for r in tr for _ in range(int(r[3] or 0))]
        for sc, sp in scorers:
            hp = next((h for h in helpers if h[0] != sc), None)
            if hp:
                helpers.remove(hp)
            goals.append({'team': team, 'name': sc, 'pid': sp, 'assist': hp[0] if hp else None})
    return goals


def _match_ratings(lg, rnd, m, rows, lw, nm, sqcache):
    """Ratings of both elevens of one simulated match (same model as the report)."""
    import random, zlib
    home, away = int(m['home_team_id']), int(m['away_team_id'])
    hg, ag = int(m['home_goals']), int(m['away_goals'])
    goals = _goals_of(rows, home, away, nm)
    gcount, acount = {}, {}
    for g in goals:
        gcount[(g['team'], g['name'])] = gcount.get((g['team'], g['name']), 0) + 1
        if g['assist']:
            acount[(g['team'], g['assist'])] = acount.get((g['team'], g['assist']), 0) + 1
    sides = {}
    for side, team, gf, ga in (('home', home, hg, ag), ('away', away, ag, hg)):
        if team not in sqcache:
            sq = (lw.squad(team) if lw is not None else None) or []
            sqcache[team] = sq
        sq = sqcache[team]
        info = {}
        for r, sh in sq:
            info.setdefault(r.get('name'), (r.get('grp'), r.get('card') or r.get('id')))
        names = [r.get('name') for r, sh in sq if sh >= 1.0][:11]
        extra = {g['name']: g.get('pid') for g in goals if g['team'] == team}
        extra.update({g['assist']: None for g in goals if g['team'] == team and g['assist']})
        for n in extra:
            if n not in names:
                names.append(n)
        players = []
        for n in names:
            rng = random.Random(zlib.crc32(('rc29-rt:%s:%s:%s:%s' % (lg, rnd, team, n)).encode()))
            g, a = gcount.get((team, n), 0), acount.get((team, n), 0)
            r = 6.4 + 0.95 * g + 0.55 * a + (0.35 if gf > ga else -0.3 if gf < ga else 0.0) + rng.gauss(0, 0.32)
            grp, pid = info.get(n, (None, extra.get(n)))
            if grp in ('G', 'D'):
                r += 0.35 if ga == 0 else -0.12 * ga
            r = max(4.6, min(10.0, r))
            players.append({'name': n, 'pid': pid, 'g': g, 'a': a, 'r': round(r, 1)})
        players.sort(key=lambda x: -x['r'])
        sides[side] = (team, players)
    return goals, sides


def fixture(conn, s, q):
    """GET /api/rc29/fixture/<lg>/<round>/<home>/<away>: a report for a match of a league the career does not play in."""
    import iml_news_leagues as nl, iml_world_leagues as wl, ml_realism as M
    lg, rnd, home, away = str(q.get('lg')), str(q.get('round')), int(q.get('home')), int(q.get('away'))
    snap = ((nl.load(conn, s) or {}).get('leagues') or {}).get(lg) or {}
    day = (snap.get('played') or {}).get(rnd) or {}
    m = next((x for x in day.get('matches') or [] if int(x['home_team_id']) == home and int(x['away_team_id']) == away), None)
    if m is None:
        return {'error': 'no-fixture'}
    pn = snap.get('pn') or {}
    nm = lambda pid: pn.get(str(pid)) or (M._name(pid) if str(pid).isdigit() else str(pid))
    try:
        lw = wl.open_league(conn, int(lg))
    except Exception:
        lw = None
    rows = [r for r in day.get('ps') or [] if int(r[0]) in (home, away)]
    goals, sides = _match_ratings(lg, rnd, m, rows, lw, nm, {})
    out = {'league': {'113': 'Premier League', '119': 'La Liga', '116': 'Serie A', '122': 'Ligue 1', '900307': 'Bundesliga'}.get(lg, lg),
           'round': int(rnd), 'home': {'team': home, 'goals': int(m['home_goals'])}, 'away': {'team': away, 'goals': int(m['away_goals'])}, 'goals': goals}
    best = None
    for side in ('home', 'away'):
        team, players = sides[side]
        out[side]['ratings'] = players
        for p in players:
            if best is None or p['r'] > best['r']:
                best = dict(p, team=team)
    if best:
        out['motm'] = best
        for side in ('home', 'away'):
            for p in out[side]['ratings']:
                p['motm'] = p['name'] == best['name'] and best['team'] == out[side]['team']
    return out


_season_cache = {}


def league_season(conn, s, lg):
    """GET /api/rc29/lgstats/<lg>: every player's season line in another league: apps, goals, assists, average rating."""
    import iml_news_leagues as nl, iml_world_leagues as wl, ml_realism as M
    lg = str(lg)
    snap = ((nl.load(conn, s) or {}).get('leagues') or {}).get(lg) or {}
    played = snap.get('played') or {}
    key = (lg, s.get('season'), len(played))
    if key in _season_cache:
        return _season_cache[key]
    pn = snap.get('pn') or {}
    nm = lambda pid: pn.get(str(pid)) or (M._name(pid) if str(pid).isdigit() else str(pid))
    try:
        lw = wl.open_league(conn, int(lg))
    except Exception:
        lw = None
    agg, sqcache = {}, {}
    for rnd, day in played.items():
        for m in day.get('matches') or []:
            home, away = int(m['home_team_id']), int(m['away_team_id'])
            rows = [r for r in day.get('ps') or [] if int(r[0]) in (home, away)]
            goals, sides = _match_ratings(lg, rnd, m, rows, lw, nm, sqcache)
            for side in ('home', 'away'):
                team, players = sides[side]
                for p in players:
                    k = (team, p['name'])
                    a = agg.setdefault(k, {'name': p['name'], 'team': team, 'pid': p.get('pid'), 'apps': 0, 'g': 0, 'a': 0, 'sum': 0.0, 'motm': 0})
                    a['apps'] += 1; a['g'] += p['g']; a['a'] += p['a']; a['sum'] += p['r']
                    if not a.get('pid') and p.get('pid'):
                        a['pid'] = p['pid']
            cands = [(p['r'], sides[sd][0], p['name']) for sd in ('home', 'away') for p in sides[sd][1]]
            if cands:
                r_, t_, n_ = max(cands)
                if (t_, n_) in agg:
                    agg[(t_, n_)]['motm'] += 1
    rows = []
    for a in agg.values():
        if a['apps']:
            rows.append({'name': a['name'], 'team': a['team'], 'pid': a['pid'], 'apps': a['apps'], 'g': a['g'], 'a': a['a'],
                         'avg': round(a['sum'] / a['apps'], 2), 'motm': a['motm']})
    rows.sort(key=lambda r: (-(r['g'] + r['a']), -r['avg']))
    out = {'lg': lg, 'rounds': len(played), 'players': rows[:200]}
    _season_cache.clear()
    _season_cache[key] = out
    return out


def install():
    import iml_rollover as RO, iml_host as HO
    try:
        import iml_leagues
        iml_leagues.TOP = 30          # league pages list 30 scorers / assisters (the full-table view)
    except Exception:
        pass
    advance = RO.advance
    @functools.wraps(advance)
    def advance_with_awards(conn):
        try:
            import my_league
            s = my_league.state(conn)
            if isinstance(s, dict) and s.get('completed'):
                record(conn, s)
                try:
                    import ml_dynamics
                    ml_dynamics.rollover(conn, int(s.get('season') or 1))
                except Exception:
                    pass
        except Exception:
            pass
        return advance(conn)
    RO.advance = advance_with_awards
    api_orig = HO.api
    @functools.wraps(api_orig)
    def api_with_awards(logic, method, path, body=''):
        if str(path).startswith('/api/rc29/own'):
            try:
                import ml_own
                return ml_own.api(logic, str(method).upper(), body)
            except Exception as exc:
                return {'error': 'own', 'reason': repr(exc)[:200]}
        if str(path).startswith('/api/rc29/y17'):
            # RC29.17: the stand-alone Y17 Champions League - its own files, no Master League profile involved
            try:
                import y17_league
                from urllib.parse import urlsplit
                return y17_league.api(str(method).upper(), urlsplit(str(path)).path, body, logic)
            except Exception as exc:
                return {'error': 'y17', 'reason': repr(exc)[:200]}
        try:
            import ml_dynamics
            import time as _t
            if not ml_dynamics._cache['loaded'] or not ml_dynamics._live['t']:
                c0 = HO._open_ml(HO._main_conn(logic))
                try:
                    if not ml_dynamics._cache['loaded']:
                        ml_dynamics.load(c0)
                    import my_league
                    if my_league.state(c0):
                        ml_dynamics.ensure_base(c0)
                        ml_dynamics.refresh(c0, force=True)
                finally:
                    c0.close()
        except Exception:
            pass
        if str(path).startswith('/api/rc29/'):
            conn = None
            try:
                conn = HO._open_ml(HO._main_conn(logic))
                import my_league
                from urllib.parse import urlsplit, parse_qsl
                parts = urlsplit(str(path))
                st = my_league.state(conn)
                if parts.path.startswith('/api/rc29/editor'):
                    import ml_editor
                    return ml_editor.api(conn, st, str(method).upper(), parts.path, body)
                if parts.path.startswith('/api/rc29/cups'):
                    import ml_cups
                    return ml_cups.api(conn, str(method).upper(), parts.path, body)
                if parts.path.startswith('/api/rc29/lgstats/'):
                    return league_season(conn, st, parts.path.split('/')[4])
                if parts.path.startswith('/api/rc29/fixture'):
                    seg = parts.path.split('/')[4:]
                    q = dict(zip(('lg', 'round', 'home', 'away'), seg)) if len(seg) >= 4 else dict(parse_qsl(parts.query))
                    return fixture(conn, st, q)
                return api(conn, st)
            except Exception as exc:
                return {'error': 'awards', 'reason': repr(exc)[:200]}
            finally:
                try:
                    conn and conn.close()
                except Exception:
                    pass
        out = api_orig(logic, method, path, body)
        if str(path).split('?')[0] == '/api/biz/news':
            c1 = None
            try:
                import ml_news, my_league
                c1 = HO._open_ml(HO._main_conn(logic))
                d = json.loads(out) if isinstance(out, str) else out
                d = ml_news.rewrite(c1, my_league.state(c1) or {}, d)
                out = json.dumps(d, ensure_ascii=False) if isinstance(out, str) else d
            except Exception:
                pass
            finally:
                try:
                    c1 and c1.close()
                except Exception:
                    pass
        return out
    HO.api = api_with_awards
    return True
