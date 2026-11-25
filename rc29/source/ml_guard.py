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
