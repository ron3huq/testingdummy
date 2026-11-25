"""RC29.23: Master League match diagnostics in the phone's "runtime diagnostics" paste.

The diagnostics screen (RuntimeDiagnostics) prints a fixed list of status files from work/tools; resource-presence-status.json is on
that list and nothing else writes it in this build, so the Master League writes its own report there:
  * every gateway command that raised (command id, exception, last frames) or answered with a non-NOERR result while the
    Master League profile was active - the source of a client "Network Error ... C_RTMC_9999"
  * the match start job (iml_host.status), the profile gate (server / client profile), own-squad / guard / Champions League 2017 state
  * the last 40 events of the Master League store (iml_season / iml_europe / health ... log_event rows)
No save data, no player records: ids and reasons only.
"""
import json, time, traceback, threading

FILE = 'resource-presence-status.json'
_err = []
_lock = threading.Lock()
_last = {'t': 0}


def _tools():
    import ml_cups as C
    return C._tools()


def _short(x, n=400):
    try:
        s = x if isinstance(x, str) else json.dumps(x, ensure_ascii=False, default=str)
    except Exception:
        s = repr(x)
    return s[:n]


def note(kind, mid, detail):
    with _lock:
        _err.append({'t': int(time.time()), 'kind': kind, 'mid': str(mid), 'detail': detail})
        del _err[:-30]
    write(force=True)


def write(force=False, logic=None):
    now = time.time()
    if not force and now - _last['t'] < 8:
        return
    _last['t'] = now
    out = {'version': 'RC29.23-ml-diag', 'written_unix': int(now), 'gateway_errors': list(_err)}
    try:
        import iml_host as HO
        out['start_job'] = HO.status()
    except Exception as exc:
        out['start_job'] = repr(exc)[:200]
    try:
        import embedded_gateway as eg, e307_profile_gate as pg
        lg = logic or eg._logic
        out['profile'] = {'server': pg.active(lg), 'client': pg.client_profile(lg)}
    except Exception as exc:
        out['profile'] = repr(exc)[:200]
    for mod in ('ml_own', 'ml_guard', 'ml_transfer'):
        try:
            out[mod] = getattr(__import__(mod), '_state', None)
        except Exception:
            pass
    try:
        import y17_league as Y
        out['cl2017'] = {k: v for k, v in Y._c.items() if k in ('kick_install', 'kick_pending', 'kick_um', 'schedule', 'sync_error')}
    except Exception:
        pass
    try:
        import embedded_gateway as eg, iml_host as HO
        c = HO._open_ml(HO._main_conn(logic or eg._logic))
        try:
            rows = c.execute('select at, kind, detail from events order by id desc limit 40').fetchall()
            out['ml_events'] = [{'at': r[0], 'kind': r[1], 'detail': _short(r[2], 300)} for r in rows]
            n = c.execute('select count(*) from gameplayers').fetchone()[0]
            out['ml_cards'] = n
        finally:
            c.close()
    except Exception as exc:
        out['ml_events'] = repr(exc)[:200]
    try:
        p = _tools() / FILE
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        tmp.replace(p)
    except Exception:
        pass


def install():
    import embedded_gateway as eg
    lg = getattr(eg, '_logic', None)
    if lg is None:
        return
    cls = type(lg)
    if getattr(cls.handle, '_rc29_diag', False):
        return
    orig = cls.handle

    def handle(self, mid, req, *a, **k):
        try:
            resp = orig(self, mid, req, *a, **k)
        except Exception as exc:
            try:
                note('exception', mid, {'error': repr(exc)[:300], 'trace': traceback.format_exc()[-1500:]})
            except Exception:
                pass
            raise
        try:
            r = resp.get('result') if isinstance(resp, dict) else None
            if r and r != 'NOERR':
                import e307_profile_gate as pg
                if pg.active(self) == 'ml':
                    note('result', mid, {'result': r, 'reply': _short(resp, 300)})
        except Exception:
            pass
        return resp
    handle._rc29_diag = True
    cls.handle = handle
    write(force=True)


def install_api():
    try:
        import iml_host as HO
        if getattr(HO.api, '_rc29_diag', False):
            return
        orig = HO.api

        def api(logic, method, path, body=''):
            out = orig(logic, method, path, body)
            try:
                if str(path).split('?')[0] in ('/api/state', '/api/start/status', '/api/rc29/y17'):
                    write(logic=logic)
            except Exception:
                pass
            return out
        api._rc29_diag = True
        HO.api = api
    except Exception:
        pass
