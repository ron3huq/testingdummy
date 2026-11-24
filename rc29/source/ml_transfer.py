"""RC29.6 "Master League Transfer": the RC26 native Transfer screen (same Java UI, same controls) on the Master League world.

The launcher button opens TransferEditor.showForCup(activity, 999). Every Transfer command of competition 999 is answered here
from the V32 Master League world (iml_world for our league, iml_world_leagues for the other four):

  rc24_cup_transfer_list / ui712_transfer_list   clubs of the five leagues
  ui712_transfer_get                             a club: its eleven on a native formation + the bench, shirts, captain, kickers, kits
  ui712_transfer_save                            formation / order / shirts / captain / kickers  -> kept in meta rc29_ml_lineups,
                                                 shirts written to the world (the CPU side is served in this order)
  ui712_transfer_move                            "Transfer to Another Team": the player really changes club in the ML world
                                                 (any league; results, scorers, news and the dynamics follow)
  ui712_transfer_kits                            native kit choices
  ui712_transfer_player_get / _apply             Abilities · Celebrations · Accessories: the RC26 player editor in its GLOBAL
                                                 scope (the card plays with the edit in every mode); abilities also move the
                                                 player's ML ability (CA), so the simulation follows
Our own club is shown read-only (your squad is managed in the Master League itself).
"""
import copy, functools, hashlib, json, threading

ML_CID = 999
KEY = 'rc29_ml_lineups'
_lock = threading.RLock()
_state = {'installed': False}
ROLE = {'GK': 0, 'CB': 1, 'LB': 2, 'RB': 3, 'DMF': 4, 'CMF': 5, 'LMF': 6, 'RMF': 7, 'AMF': 8, 'LWF': 9, 'RWF': 10, 'SS': 11, 'CF': 12}
GRP_ROLE = {'G': 0, 'D': 1, 'M': 5, 'F': 12}


def _conn():
    import embedded_gateway as eg, iml_host as HO
    return HO._open_ml(HO._main_conn(eg._logic))


def _store():
    import iml_news_leagues as nl
    return nl.store


def _lineups(conn):
    try:
        raw = _store().get_meta(conn, KEY)
        d = json.loads(raw) if raw else {}
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _state_of(conn):
    import my_league
    return my_league.state(conn) or {}


def _clubs(conn, s):
    import ml_editor as E
    out = []
    for lg in E.leagues(conn, s)['leagues']:
        for c in lg['clubs']:
            out.append((lg['cid'], c, lg['name']))
    return out


def _where(conn, s, team):
    for cid, c, lname in _clubs(conn, s):
        if c['team'] == int(team):
            return cid, c, lname
    return None, None, None


def _formation(name=None):
    import transfer_editor as T
    fs = T.formation_choices()
    return next((f for f in fs if f['name'] == name), None) or next((f for f in fs if f['name'] == '4-3-3'), fs[0])


def _row(conn, s, team):
    """The club as a native Transfer team row."""
    import ml_editor as E
    cid, club, lname = _where(conn, s, team)
    if cid is None:
        raise ValueError('Unknown Master League club')
    sq = [p for p in E.club(conn, s, cid, team)['players'] if p.get('card')]
    saved = _lineups(conn).get(str(team)) or {}
    form = _formation(saved.get('formation'))
    by_id = {str(p['card']): p for p in sq}
    order = [x for x in saved.get('order') or [] if x in by_id]
    rest = sorted((p for p in sq if str(p['card']) not in order), key=lambda p: -float(p.get('ca') or 0))
    xi, bench, used = [], [], set(order)
    if len(order) >= 11:
        xi = order[:11]
        bench = order[11:] + [str(p['card']) for p in rest]
    else:
        pool = list(order) + [str(p['card']) for p in rest]
        for slot in form['slots']:
            want = slot['role']
            grp = 'G' if want == 0 else 'D' if want in (1, 2, 3) else 'F' if want in (9, 10, 11, 12) else 'M'
            near = {0: (0,), 1: (1,), 2: (2, 3), 3: (3, 2), 4: (4, 5), 5: (5, 4, 8), 6: (6, 9, 5), 7: (7, 10, 5), 8: (8, 5, 11), 9: (9, 6, 11), 10: (10, 7, 11), 11: (11, 12, 8), 12: (12, 11)}.get(want, (want,))
            pick = None
            for r_ in near:
                pick = next((c for c in pool if c not in xi and ROLE.get(by_id[c].get('pos') or '') == r_), None)
                if pick:
                    break
            pick = pick or next((c for c in pool if c not in xi and by_id[c].get('grp') == grp), None) or next((c for c in pool if c not in xi), None)
            if pick:
                xi.append(pick)
        bench = [c for c in pool if c not in xi]
    roster, shirts = [], set()
    for i, c in enumerate(xi + bench[:29]):
        p = by_id[c]
        sh = (saved.get('shirts') or {}).get(c) or p.get('shirt') or 0
        if not 1 <= int(sh) <= 99 or sh in shirts:
            sh = next(n for n in range(1, 100) if n not in shirts)
        shirts.add(sh)
        if i < 11:
            sl = form['slots'][i]
            roster.append({'id': c, 'shirt': int(sh), 'role': sl['role'], 'x': sl['x'], 'y': sl['y'], 'name': p['name']})
        else:
            roster.append({'id': c, 'shirt': int(sh), 'role': ROLE.get(p.get('pos') or '', GRP_ROLE.get(p.get('grp'), 5)), 'x': 0, 'y': 0, 'name': p['name']})
    ids = [r['id'] for r in roster]
    captain = saved.get('captain') if saved.get('captain') in ids else (ids[0] if ids else None)
    kickers = [k if k in ids else None for k in (saved.get('kickers') or [])][:6]
    kickers += [ids[10] if len(ids) > 10 else None] * (6 - len(kickers))
    row = {'team_id': int(team), 'competition': ML_CID, 'name': '%s · %s' % (E._team_name(team, club), lname), 'roster': roster,
           'captain': captain, 'kickers': kickers, 'formation': form['name'], 'source': 'RC29_MASTER_LEAGUE_WORLD', 'ml_league': cid}
    try:
        import transfer_editor as T
        row['kits'] = saved.get('kits') or T.kit_choices(int(team))
    except Exception:
        row['kits'] = saved.get('kits') or []
    return row


def _revision(row):
    core = {k: v for k, v in row.items() if k not in ('revision',)}
    core['roster'] = [{k: v for k, v in p.items() if k != 'name'} for p in row['roster']]
    return hashlib.sha256(json.dumps(core, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _list(conn, s, req):
    q = str(req.get('query') or '').strip().lower()
    me = int(s.get('team_id') or 0)
    saved = _lineups(conn)
    teams = []
    for cid, c, lname in _clubs(conn, s):
        name = '%s · %s' % (c['name'], lname)
        if q and q not in name.lower() and q != str(c['team']):
            continue
        teams.append({'id': c['team'], 'name': name + (' (your club)' if c['team'] == me else ''), 'edited': str(c['team']) in saved, 'ready': True})
    return {'teams': teams, 'leagues': [{'id': ML_CID, 'name': 'Master League'}]}


def _get(conn, s, req):
    import transfer_editor as T
    row = _row(conn, s, req.get('team_id'))
    out = copy.deepcopy(row)
    out['revision'] = _revision(row)
    return {'ready': True, 'team': out, 'formation_choices': T.formation_choices(), 'roles': T.catalog()['roles'],
            'kit_teams': [{'id': c['team'], 'name': c['name']} for cid, c, l in _clubs(conn, s)]}


def _save(conn, s, req):
    team = int(req.get('team_id'))
    if team == int(s.get('team_id') or 0):
        raise ValueError('Your own club is managed inside the Master League (squad, tactics, transfer market).')
    t = req.get('team') or {}
    roster = t.get('roster') or []
    if len(roster) < 11:
        raise ValueError('Keep at least 11 players')
    form = _formation()
    for f in __import__('transfer_editor').formation_choices():
        if [(x['role'], x['x'], x['y']) for x in f['slots']] == [(p.get('role'), p.get('x'), p.get('y')) for p in roster[:11]]:
            form = f
            break
    doc = _lineups(conn)
    doc[str(team)] = {'order': [str(p['id']) for p in roster], 'shirts': {str(p['id']): int(p.get('shirt') or 0) for p in roster},
                      'captain': t.get('captain'), 'kickers': t.get('kickers') or [], 'formation': form['name'], 'kits': t.get('kits') or []}
    _store().set_meta(conn, KEY, json.dumps(doc, separators=(',', ':')))
    # shirts into the world (the CPU side is served with them)
    import ml_editor as E
    cid, club, _ = _where(conn, s, team)
    w = E._load(conn, s, cid)
    for p in (w.get('players') or {}).values():
        if str(p.get('card')) in doc[str(team)]['shirts'] and str(p.get('club')) == str(team):
            p['shirt'] = doc[str(team)]['shirts'][str(p.get('card'))]
    E._save(conn, s, cid, w)
    return {'saved': True, 'teams': 1}


def _move(conn, s, req):
    import ml_editor as E
    src_team, dst_team, card = int(req.get('team_id')), int(req.get('target_team')), str(req.get('player_id'))
    scid, _, _ = _where(conn, s, src_team)
    dcid, _, _ = _where(conn, s, dst_team)
    if scid is None or dcid is None:
        raise ValueError('Choose two Master League clubs')
    w = E._load(conn, s, scid)
    p = next((x for x in (w.get('players') or {}).values() if str(x.get('card')) == card and str(x.get('club')) == str(src_team)), None)
    if p is None:
        raise ValueError('Reload the team and select a current member')
    r = E.move(conn, s, {'pid': p['id'], 'from_cid': scid, 'to_cid': dcid, 'to_team': dst_team})
    if r.get('error'):
        raise ValueError(r.get('reason') or r['error'])
    doc = _lineups(conn)
    for t in (str(src_team), str(dst_team)):
        if t in doc:
            doc[t]['order'] = [x for x in doc[t].get('order') or [] if x != card]
    _store().set_meta(conn, KEY, json.dumps(doc, separators=(',', ':')))
    return {'saved': True, 'teams': 2}


def _player(conn, s, action, req, game_conn):
    """The RC26 player editor in its global scope for this card."""
    import transfer_editor as T, transfer_player_editor as PE
    team = int(req.get('team_id'))
    row = _row(conn, s, team)
    pid = str(req.get('player_id'))
    if not any(p['id'] == pid for p in row['roster']):
        raise ValueError('Reload the team and select a current member')
    ident, src = T.identity, T.source
    T.identity = lambda r: (team, 0)
    T.source = lambda tid, cid: copy.deepcopy(row)
    try:
        out = PE.manage(game_conn, action, dict(req, competition=0))
    finally:
        T.identity, T.source = ident, src
    if action.endswith('_apply') and isinstance((req.get('values') or {}).get('parameters'), dict):
        try:     # the ML simulation follows: overall-ish change moves the CA
            import ml_editor as E
            vals = [int(v) for v in req['values']['parameters'].values() if str(v).lstrip('-').isdigit()]
            if vals:
                cid, _, _ = _where(conn, s, team)
                w = E._load(conn, s, cid)
                p = next((x for x in (w.get('players') or {}).values() if str(x.get('card')) == pid), None)
                if p is not None:
                    mean = sum(vals) / len(vals)
                    p['ca'] = max(60, min(199, int(round(mean * 2.05))))
                    p['pa'] = max(p.get('pa') or 0, p['ca'])
                    E._save(conn, s, cid, w)
        except Exception:
            pass
    return out


def handle(action, req, game_conn):
    conn = _conn()
    try:
        s = _state_of(conn)
        if not s:
            raise ValueError('Start a Master League career first')
        if action in ('rc24_cup_transfer_list', 'ui712_transfer_list'):
            return _list(conn, s, req)
        if action == 'ui712_transfer_get':
            return _get(conn, s, req)
        if action == 'ui712_transfer_save':
            return _save(conn, s, req)
        if action == 'ui712_transfer_move':
            return _move(conn, s, req)
        if action == 'ui712_transfer_kits':
            import transfer_editor as T
            donor = int(req.get('donor'))
            names = {c['team']: c['name'] for cid, c, l in _clubs(conn, s)}
            return {'kits': [{'id': uid, 'label': names.get(donor, 'Team') + ' · ' + ('Home' if i == 0 else 'Away' if i == 1 else 'Slot ' + str(i + 1))}
                             for i, uid in enumerate(T.kit_choices(donor)) if uid is not None]}
        if action in ('ui712_transfer_player_get', 'ui712_transfer_player_apply', 'ui712_transfer_traits_get', 'ui712_transfer_traits_apply'):
            return _player(conn, s, action.replace('traits', 'player') if 'traits' in action else action, req, game_conn)
        if action == 'ui712_transfer_player_search':
            import transfer_editor as T
            return T.search_players(game_conn, req)
        raise ValueError('Unknown transfer action')
    finally:
        try:
            conn.close()
        except Exception:
            pass


def install():
    if _state['installed']:
        return _state
    import embedded_gateway as eg
    old = eg.manage

    @functools.wraps(old)
    def manage(action, payload=''):
        if action == 'rc24_cup_transfer_list' or str(action).startswith('ui712_transfer_') or action == 'ui712_motion_search':
            try:
                req = json.loads(payload or '{}')
            except Exception:
                req = {}
            if int(req.get('competition') or 0) == ML_CID:
                with _lock:
                    return json.dumps(handle(action, req, eg._logic.conn), ensure_ascii=False)
        return old(action, payload)
    eg.manage = manage
    _state['installed'] = True
    return _state
