"""RC29.18: "My own squad" for the Master League (like My League: you play with the 23 cards of your main squad).

How (no new native work): the Master League store's squad and cards become an exact copy of the main squad, so the client's
cached lineup already IS the ML lineup.  The profile switch before a match then only moves the server to the ML store
(e307_profile_gate.switch) and marks the client in sync - the client-side roster refresh (the native job that fails on
some installs: "switch-failed" / 0 players) is not needed at all.  Your club in the ML world, fixtures, opponents, table,
stats and news all stay the Master League's; only the players you field are your own.

State (ML store meta):
  rc29_own_squad      "1" when on
  rc29_club_backup    the club squad + cards before the first switch to own mode (restored when you turn it off)
API: GET /api/rc29/own  ->  {on, main: n cards, ml: n cards}
     POST /api/rc29/own {on: true|false}
"""
import json

KEY = 'rc29_own_squad'
BACKUP = 'rc29_club_backup'
_state = {}


def _meta(conn, key, default=None):
    r = conn.execute('select value from meta where key=?', (key,)).fetchone()
    return r[0] if r else default


def _set_meta(conn, key, value):
    conn.execute('delete from meta where key=?', (key,))
    conn.execute('insert into meta(key, value) values(?, ?)', (key, value))


def is_on(ml):
    try:
        return str(_meta(ml, KEY, '0')) == '1'
    except Exception:
        return False


def _rows(conn, table):
    cols = [r[1] for r in conn.execute('pragma table_info("%s")' % table)]
    return cols, [list(r) for r in conn.execute('select %s from "%s"' % (','.join('"%s"' % c for c in cols), table))]


def _put(conn, table, cols, rows):
    conn.execute('delete from "%s"' % table)
    if rows:
        conn.executemany('insert into "%s"(%s) values(%s)' % (table, ','.join('"%s"' % c for c in cols), ','.join('?' * len(cols))), rows)


def copy_main(main, ml):
    """Main squad + every owned card of the main store -> ML store (cards the client can field, nothing else)."""
    gcols, grows = _rows(main, 'gameplayers')
    scols, srows = _rows(main, 'squads')
    if not srows:
        raise ValueError('no main squad')
    mcols = [r[1] for r in ml.execute('pragma table_info("gameplayers")')]
    if mcols != gcols:
        raise ValueError('store schema differs')
    _put(ml, 'gameplayers', gcols, grows)
    _put(ml, 'squads', scols, srows)
    try:
        wcols, wrows = _rows(main, 'warehouse')
        _put(ml, 'warehouse', wcols, wrows)
    except Exception:
        pass
    return len(grows)


def enable(main, ml):
    if not _meta(ml, BACKUP):
        gcols, grows = _rows(ml, 'gameplayers')
        scols, srows = _rows(ml, 'squads')
        _set_meta(ml, BACKUP, json.dumps({'g': [gcols, grows], 's': [scols, srows]}))
    n = copy_main(main, ml)
    _set_meta(ml, KEY, '1')
    ml.commit()
    return n


def disable(ml):
    raw = _meta(ml, BACKUP)
    if raw:
        b = json.loads(raw)
        _put(ml, 'gameplayers', *b['g'])
        _put(ml, 'squads', *b['s'])
        ml.execute('delete from meta where key=?', (BACKUP,))
    _set_meta(ml, KEY, '0')
    ml.commit()


def _conns(logic):
    import iml_host as HO
    main = HO._main_conn(logic)
    return main, HO._open_ml(main)


def api(logic, method, body):
    main, ml = _conns(logic)
    try:
        if method == 'POST':
            try:
                on = bool(json.loads(body or '{}').get('on'))
            except Exception:
                on = False
            try:
                if on:
                    enable(main, ml)
                else:
                    disable(ml)
            except Exception as exc:
                return {'error': 'own-squad', 'reason': str(exc)[:160]}
            try:
                import iml_host as HO
                HO.invalidate_client(logic)
            except Exception:
                pass
        n_main = main.execute('select count(*) from gameplayers').fetchone()[0]
        n_ml = ml.execute('select count(*) from gameplayers').fetchone()[0]
        return {'on': is_on(ml), 'main': n_main, 'ml': n_ml, 'state': _state}
    finally:
        ml.close()


def install():
    import e307_profile_gate as pg
    if getattr(pg.switch_with_client, '_rc29_own', False):
        return
    orig = pg.switch_with_client

    def switch_with_client(target, logic=None, *a, **k):
        lg = logic
        try:
            import embedded_gateway as eg
            lg = logic or eg._logic
            main, ml = _conns(lg)
            try:
                own = is_on(ml)
                if own and target == 'ml' and pg.active(lg) == 'main':
                    copy_main(main, ml)          # the latest main lineup (changed in the game) is the one we play
                    ml.commit()
            finally:
                ml.close()
        except Exception as exc:
            own = False
            _state['own_check'] = repr(exc)[:200]
        if not own:
            return orig(target, logic, *a, **k)
        r = pg.switch(target, lg)
        if (r or {}).get('result') != 'NOERR':
            _state['own_switch'] = r
            return orig(target, logic, *a, **k)
        lg.__dict__['client_profile'] = target
        _state['own_switches'] = _state.get('own_switches', 0) + 1
        return {'result': 'NOERR', 'ok': True, 'active': target, 'client': {'ok': True, 'own_squad': True}}
    switch_with_client._rc29_own = True
    pg.switch_with_client = switch_with_client
    # a new career builds the club's official 23: with own squad on, put your squad back right after
    try:
        import iml_rosters as RS
        b = RS.build_squad

        def build_squad(conn, team_id, *a, **k):
            out = b(conn, team_id, *a, **k)
            try:
                if is_on(conn):
                    conn.execute('delete from meta where key=?', (BACKUP,))
                    import embedded_gateway as eg, iml_host as HO
                    main = HO._main_conn(eg._logic)
                    enable(main, conn)
            except Exception as exc:
                _state['own_build'] = repr(exc)[:200]
            return out
        RS.build_squad = build_squad
    except Exception:
        pass
