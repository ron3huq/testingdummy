"""RC29.6 Master League editor (the RC26 "Edit Transfer" idea for the V32 Master League world).

/api/rc29/editor                         -> leagues (own league + the four other top leagues) with their clubs
/api/rc29/editor/club/<cid>/<team>       -> one club's squad (name, position, ability CA, potential, value, card)
/api/rc29/editor/search/<text>           -> players of every league whose name matches
POST /api/rc29/editor/move   {pid, from_cid, to_cid, to_team}   -> move a player to another club (same or another league), no fee
POST /api/rc29/editor/ca     {pid, cid, ca}                    -> set a player's current ability (60..199)

Our own club is locked (your squad is your cards: buy / sell through the normal transfer market). Everything goes through the
V32 world files (iml_world for our league, iml_world_leagues for the others), so results, scorers, the table and the RC29
long-term dynamics all follow the edit at once.
"""
import json, datetime, random

NAMES = {113: 'Premier League', 119: 'La Liga', 116: 'Serie A', 122: 'Ligue 1', 900307: 'Bundesliga'}


def _own(s):
    return int(s.get('competition_id') or 113)


def _load(conn, s, cid):
    import iml_world as IW, iml_world_leagues as W
    return IW.load(conn) if int(cid) == _own(s) else W.load(conn, int(cid))


def _save(conn, s, cid, world):
    import iml_world as IW, iml_world_leagues as W
    if int(cid) == _own(s):
        IW.save(conn, world)
    else:
        W.save(conn, int(cid), world)
    try:
        conn.commit()
    except Exception:
        pass


def _leagues(s):
    import iml_world_leagues as W
    return [_own(s)] + [int(c) for c in W.others(s) if int(c) != _own(s)]


def _team_name(tid, club):
    try:
        import ml_isolation as I
        if int(tid) in I.REAL_CLUB:
            return I.REAL_CLUB[int(tid)]
    except Exception:
        pass
    return (club or {}).get('name') or str(tid)


def _row(p):
    return {'pid': p.get('id'), 'name': p.get('name'), 'pos': p.get('pos') or {'G': 'GK', 'D': 'CB', 'M': 'CMF', 'F': 'CF'}.get(p.get('grp'), ''),
            'grp': p.get('grp'), 'ca': p.get('ca'), 'pa': p.get('pa'), 'value': p.get('value'), 'card': p.get('card'), 'nat': p.get('nat'),
            'shirt': p.get('shirt'), 'club': p.get('club')}


def leagues(conn, s):
    me = int(s.get('team_id') or 0)
    out = []
    for cid in _leagues(s):
        w = _load(conn, s, cid) or {}
        clubs = w.get('clubs') or {}
        ps = [p for p in (w.get('players') or {}).values() if p.get('status') == 'active']
        rows = []
        for tid, c in clubs.items():
            sq = [p for p in ps if str(p.get('club')) == str(tid)]
            top = sorted((float(p.get('ca') or 0) for p in sq), reverse=True)[:11]
            rows.append({'team': int(tid), 'name': _team_name(tid, c), 'n': len(sq), 'level': round(sum(top) / max(1, len(top)), 1), 'mine': int(tid) == me})
        rows.sort(key=lambda r: -r['level'])
        out.append({'cid': cid, 'name': NAMES.get(cid, str(cid)), 'own': cid == _own(s), 'clubs': rows})
    return {'leagues': out, 'team': me}


def club(conn, s, cid, team):
    w = _load(conn, s, cid) or {}
    ps = [p for p in (w.get('players') or {}).values() if p.get('status') == 'active' and str(p.get('club')) == str(team)]
    order = {'G': 0, 'D': 1, 'M': 2, 'F': 3}
    ps.sort(key=lambda p: (order.get(p.get('grp'), 4), -float(p.get('ca') or 0)))
    return {'cid': int(cid), 'team': int(team), 'name': _team_name(team, (w.get('clubs') or {}).get(str(team))),
            'locked': int(team) == int(s.get('team_id') or 0), 'players': [_row(p) for p in ps]}


def search(conn, s, text):
    import ml_realism as M
    q = M._norm(text)
    out = []
    if len(q) < 2:
        return {'players': []}
    for cid in _leagues(s):
        w = _load(conn, s, cid) or {}
        clubs = w.get('clubs') or {}
        for p in (w.get('players') or {}).values():
            if p.get('status') == 'active' and q in M._norm(p.get('name')):
                r = _row(p)
                r.update(cid=cid, league=NAMES.get(cid, ''), club_name=_team_name(p.get('club'), clubs.get(str(p.get('club')))))
                out.append(r)
    out.sort(key=lambda r: -float(r.get('ca') or 0))
    return {'players': out[:40]}


def move(conn, s, body):
    import iml_world_leagues as W
    me = int(s.get('team_id') or 0)
    pid, src, dst, to = str(body.get('pid')), int(body.get('from_cid')), int(body.get('to_cid')), int(body.get('to_team'))
    sw = _load(conn, s, src)
    p = ((sw or {}).get('players') or {}).get(pid)
    if not p:
        return {'error': 'no-player'}
    if int(p.get('club') or 0) == me or to == me:
        return {'error': 'locked', 'reason': 'Your own squad changes through the transfer market.'}
    if src == dst:
        if str(to) not in (sw.get('clubs') or {}):
            return {'error': 'no-club'}
        p['club'] = to
        _save(conn, s, src, sw)
    else:
        dw = _load(conn, s, dst)
        if not dw or str(to) not in (dw.get('clubs') or {}):
            return {'error': 'no-club'}
        season = int(s.get('season') or 1)
        try:
            W._xl_move(sw, dw, src, dst, p, to, 0.0, datetime.date.today(), season, random.Random(7))
        except Exception:
            dw.setdefault('players', {})[pid] = dict(p, club=to)
            sw['players'].pop(pid, None)
        moved = dw.get('players', {}).get(pid) or next((x for x in dw.get('players', {}).values() if x.get('name') == p.get('name') and str(x.get('club')) == str(to)), None)
        if moved is not None:
            moved['club'] = to
        _save(conn, s, src, sw)
        _save(conn, s, dst, dw)
    _refresh(conn)
    return {'ok': True, 'player': p.get('name'), 'to': to}


def set_ca(conn, s, body):
    cid, pid = int(body.get('cid')), str(body.get('pid'))
    w = _load(conn, s, cid)
    p = ((w or {}).get('players') or {}).get(pid)
    if not p:
        return {'error': 'no-player'}
    if int(p.get('club') or 0) == int(s.get('team_id') or 0):
        return {'error': 'locked', 'reason': 'Your own players grow through training.'}
    ca = max(60, min(199, int(body.get('ca'))))
    p['ca'] = ca
    if float(p.get('pa') or 0) < ca:
        p['pa'] = ca
    _save(conn, s, cid, w)
    _refresh(conn)
    return {'ok': True, 'ca': ca}


def _refresh(conn=None):
    """An edit counts at once: club strength, scorer shares and the Ballon d'Or read the edited world from the next match."""
    try:
        import ml_realism
        ml_realism._star_cache.clear()
        if conn is not None:
            import ml_dynamics
            ml_dynamics.refresh(conn, force=True)
    except Exception:
        pass


def api(conn, s, method, path, body):
    parts = [x for x in path.split('/') if x][3:]          # after api/rc29/editor
    try:
        data = json.loads(body or '{}') if method == 'POST' else {}
    except Exception:
        data = {}
    if not parts:
        return leagues(conn, s)
    if parts[0] == 'club' and len(parts) >= 3:
        return club(conn, s, int(parts[1]), int(parts[2]))
    if parts[0] == 'search' and len(parts) >= 2:
        from urllib.parse import unquote
        return search(conn, s, unquote(parts[1]))
    if method == 'POST' and parts[0] == 'move':
        return move(conn, s, data)
    if method == 'POST' and parts[0] == 'ca':
        return set_ca(conn, s, data)
    return {'error': 'unknown'}
