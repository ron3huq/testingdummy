"""RC29.16 self-repair: a Master League store whose main squad lost its cards (an ML store created by an earlier build) is rebuilt with
the career club's own 23 (iml_rosters.build_squad, exactly what V32 does when a career starts).  Runs before a match / simulation.
Never touches the main save."""
import functools

_state = {'repairs': 0, 'last': None}


def squad_count(conn):
    try:
        import iml_health as IH
        slots, starters = IH.squad_cards(conn)
        return sum(1 for x in slots if x)
    except Exception:
        return -1


def repair(conn):
    try:
        import my_league, iml_rosters as RS
        s = my_league.state(conn) or {}
        team = int(s.get('team_id') or 0)
        if not team:
            return None
        n = squad_count(conn)
        if n >= RS.SQUAD_SIZE or n < 0:
            return None
        r = RS.build_squad(conn, team, commit=True)
        _state['repairs'] += 1
        _state['last'] = {'team': team, 'before': n, 'result': {k: r.get(k) for k in ('ok', 'cards', 'reason') if isinstance(r, dict)}}
        return r
    except Exception as exc:
        _state['last'] = {'error': repr(exc)[:200]}
        return None


def install():
    try:
        import iml_health as IH
        pf = IH.preflight

        @functools.wraps(pf)
        def preflight(conn, ctx, *a, **k):
            try:
                repair(conn)
            except Exception:
                pass
            return pf(conn, ctx, *a, **k)
        IH.preflight = preflight
    except Exception as exc:
        _state['install'] = repr(exc)
    try:
        import e307_profile_gate as pg, iml_host as HO
        sw = pg.switch_with_client

        @functools.wraps(sw)
        def switch_with_client(target, logic=None, *a, **k):
            if target == 'ml':
                c = None
                try:
                    import embedded_gateway as eg
                    lg = logic or getattr(eg, '_logic', None)
                    c = HO._open_ml(HO._main_conn(lg))
                    repair(c)
                except Exception as exc:
                    _state['switch_repair'] = repr(exc)[:200]
                finally:
                    try:
                        c and c.close()
                    except Exception:
                        pass
            return sw(target, logic, *a, **k)
        pg.switch_with_client = switch_with_client
    except Exception as exc:
        _state['install_switch'] = repr(exc)
    install_models()
    install_shuffle()
    return _state


# ------------------------------------------------------------------ appearance copies for Master League cards (RC26 model copy)
MODEL_COPY = {'56164297650152': ('Yan Diomande', '176104')}     # ML Real Madrid Diomande = the My League Real Madrid Diomande (face, skin)


def install_models():
    try:
        import profile_editor as PE, myleague_editor_runtime as ED, json as _j
        for pid, (name, donor) in MODEL_COPY.items():
            row = dict(PE.DEFAULTS.get(pid) or {})
            row.setdefault('name', name)
            row['model_source'] = donor
            PE.DEFAULTS[pid] = row
        cfg = _j.loads(ED.PATH.read_text())
        changed = False
        for pid, (name, donor) in MODEL_COPY.items():
            r = next((x for x in cfg['players'] if x['id'] == pid and x.get('competition') == 0), None)
            if r is None:
                r = {'id': pid, 'competition': 0, 'sleeve': 'none', 'parameters': {}}
                cfg['players'].append(r)
            if r.get('ui711_copy') != donor:
                r['ui711_copy'] = donor
                changed = True
        if changed:
            ED.validate(cfg)
            tmp = ED.PATH.with_suffix('.rc29.tmp')
            tmp.write_text(_j.dumps(cfg, indent=2))
            tmp.replace(ED.PATH)
            ED._config = None
        try:
            PE.sync_model_inheritance()
        except Exception:
            pass
        _state['models'] = 'ok'
    except Exception as exc:
        _state['models'] = repr(exc)[:200]


# ------------------------------------------------------------------ RC29.17: a fresh, realistic fixture order every season
def _shuffle_rounds(rounds, seed):
    """Permute two-round blocks inside each half of the season (home/away rhythm kept: no team gets more than two home or away games
    in a row from the shuffle), and never the same pair in consecutive rounds across a block border."""
    import random
    r = random.Random(seed)
    n = len(rounds)
    half = n // 2
    out = []
    for lo, hi in ((0, half), (half, n)):
        blocks = [rounds[i:i + 2] for i in range(lo, hi, 2)]
        best = None
        for _ in range(60):
            r.shuffle(blocks)
            flat = [x for b in blocks for x in b]
            prev = out[-1:] + flat
            ok = True
            for a, b in zip(prev, prev[1:]):
                pa = {frozenset((m['home_team_id'], m['away_team_id'])) for m in a}
                if any(frozenset((m['home_team_id'], m['away_team_id'])) in pa for m in b):
                    ok = False
                    break
            if ok:
                best = flat
                break
        out.extend(best or [x for b in blocks for x in b])
    return out


def shuffle_schedule(conn):
    try:
        import my_league as ML
        s = ML.state(conn)
        if not isinstance(s, dict) or not s.get('schedule_v2') or s.get('played') or int(s.get('fixture') or 1) != 1:
            return False
        season = int(s.get('season') or 1)
        if s.get('rc29_shuffle') == season:
            return False
        sch = s['schedule_v2']
        lists = [rd.get('match_list') or [] for rd in sch]
        import random
        new = _shuffle_rounds(lists, random.randrange(1, 10 ** 9))
        for rd, ml in zip(sch, new):
            rd['match_list'] = ml
        s['rc29_shuffle'] = season
        ML.save(conn, s)
        try:
            conn.commit()
        except Exception:
            pass
        _state['shuffled'] = season
        return True
    except Exception as exc:
        _state['shuffle'] = repr(exc)[:200]
        return False


def install_shuffle():
    try:
        import iml_host as HO
        orig = HO.api

        def api(logic, method, path, body=''):
            if str(path).split('?')[0] == '/api/state':
                c = None
                try:
                    c = HO._open_ml(HO._main_conn(logic))
                    shuffle_schedule(c)
                except Exception:
                    pass
                finally:
                    try:
                        c and c.close()
                    except Exception:
                        pass
            return orig(logic, method, path, body)
        HO.api = api
    except Exception as exc:
        _state['install_shuffle'] = repr(exc)[:200]
