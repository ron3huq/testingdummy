"""RC29: keep the V32 Master League exactly as shipped while RC26 customises My League.

RC26 (bridge_73 -> myleague_73 / myleague_worlds / rc24 cups ...) replaces a few V32 functions and the shared ziru_data cache
(competition registry, team names, rosters, schedules) so that competition 122 is its UCL, 128 its World Nation League, etc.
The V32 Master League uses the same ids for real leagues (122 = Ligue 1, 125/128/476/518/566/473/549 feed the European cups).

Rule: while the Master League is in play - the ML profile is active (e307_profile_gate.active() == 'ml') or the call comes from a
Master League module (a frame of an iml_* module on the stack) - every RC26 replacement listed below answers with the original V32
function and the original V32 data.  Otherwise (My League, events, everything else) RC26 answers exactly as before.
Nothing is written to disk, no save is touched.
"""
import sys, json, functools, threading

TARGETS = {
    'my_league': ('fixtures', 'cpu_score', '_cpu_round_stats', 'info', '_opponent_squad', 'prepare', 'start'),
    'ml_super_league': ('start_season',),
    'opponent_squad': ('preset', 'build'),
    ('gate_logic', 'GateLogic'): ('handle', '_vscom_opponent', '_start_game'),
}
NATIVE_RESET = {('my_league', 'prepare'), ('my_league', 'start'), ('gate_logic', '_vscom_opponent'), ('gate_logic', '_start_game')}
_state = {'installed': False, 'wrapped': [], 'ml_calls': 0, 'errors': []}
_before = {}
_ziru_cache = None
_ml_data = {}
_lock = threading.Lock()
# RC26 renamed these clubs to their real names; the Master League keeps those (same club, real name).
# Clubs RC26 re-used for other teams (Scottish / Swiss clubs as My League youth sides, 116 'AjaxE', ...) keep the V32 name.
REAL_CLUB = {
    102: 'Chelsea', 103: 'Liverpool', 104: 'Leeds United', 106: 'Newcastle United', 107: 'Aston Villa', 1589: 'Hull City', 173: 'Manchester City',
    177: 'Everton', 178: 'Fulham', 179: 'Tottenham Hotspur', 377: 'Brighton & Hove Albion', 382: 'Crystal Palace', 386: 'Ipswich Town',
    389: 'Nottingham Forest', 396: 'Sunderland', 4071: 'AFC Bournemouth', 4180: 'Brentford', 4183: 'Coventry City', 101: 'Arsenal',
    109: 'Real Madrid', 110: 'Valencia CF', 111: 'Deportivo La Coruña', 172: 'Atlético de Madrid', 194: 'Real Betis', 195: 'Celta de Vigo',
    196: 'Real Sociedad', 258: 'Athletic Club', 259: 'RCD Espanyol', 260: 'Málaga CF', 263: 'CA Osasuna', 264: 'Racing Santander',
    265: 'Sevilla FC', 267: 'Villarreal CF', 361: 'Elche CF', 362: 'Getafe CF', 366: 'Levante UD', 370: 'Rayo Vallecano', 4145: 'Deportivo Alavés',
    120: 'Juventus', 124: 'ACF Fiorentina', 125: 'AS Roma', 186: 'Bologna FC 1909', 1919: 'US Sassuolo', 320: 'Cagliari Calcio', 323: 'Genoa CFC',
    327: 'SSC Napoli', 4229: 'Venezia FC', 4234: 'Frosinone Calcio', 4237: 'US Lecce', 4914: 'AC Monza',
    127: 'FC Bayern München',
    1195: 'KRC Genk', 1196: 'KAA Gent', 1197: 'Standard Liège', 1200: 'KV Mechelen', 174: 'RSC Anderlecht', 2009: 'Cercle Brugge', 269: 'Club Brugge',
    2010: 'Sporting Charleroi', 2013: 'KV Kortrijk', 2019: 'Zulte Waregem', 5191: 'Royal Antwerp', 5194: 'Sint-Truidense VV', 5195: 'SK Beveren',
    5217: 'OH Leuven', 5220: 'Union Saint-Gilloise', 5221: 'KVC Westerlo', 5422: 'Lommel SK', 6067: 'RAAL La Louvière',
    1228: 'Grasshopper Club Zürich', 1957: 'FC Zürich', 1706: 'FC Basel', 1950: 'BSC Young Boys', 1955: 'FC Sion', 1956: 'FC Vaduz', 1958: 'Servette FC',
    4937: 'FC St. Gallen', 4938: 'FC Thun', 4962: 'FC Luzern', 4964: 'FC Lausanne-Sport', 4965: 'FC Lugano',
    1207: 'FC København', 1208: 'FC Nordsjælland', 1832: 'Brøndby IF', 2066: 'AC Horsens', 2067: 'AGF Aarhus', 2069: 'FC Midtjylland', 2070: 'OB Odense',
    2071: 'Randers FC', 5224: 'Lyngby BK', 5225: 'Silkeborg IF', 5226: 'SønderjyskE', 5237: 'Viborg FF',
}
REAL_NAMES = (101, 102, 108, 109, 120, 127, 172, 173, 179, 279, 1248, 1254, 4155, 5738, 5741, 17873, 18961)


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
        name = f.f_globals.get('__name__', '')
        if name.startswith('iml_'):
            return True
        f = f.f_back
        n += 1
    return False


def _holder(key):
    if isinstance(key, tuple):
        mod = sys.modules.get(key[0])
        return getattr(mod, key[1], None) if mod is not None else None
    return sys.modules.get(key)


def _get(holder, name):
    return holder.__dict__.get(name) if isinstance(holder, type) else getattr(holder, name, None)


def snapshot():
    """Call before RC26 installs: remember the V32 originals."""
    global _ziru_cache
    import importlib
    for mod in ('my_league', 'ml_super_league', 'opponent_squad', 'gate_logic', 'ziru_data'):
        try:
            importlib.import_module(mod)
        except Exception as exc:
            _state['errors'].append('import %s: %r' % (mod, exc))
    for key, names in TARGETS.items():
        h = _holder(key)
        if h is None:
            continue
        for n in names:
            v = _get(h, n)
            if v is not None:
                _before[(key, n)] = v
    z = sys.modules.get('ziru_data')
    if z is not None:
        _ziru_cache = dict(z._cache)


def _reset_native():
    st = sys.modules.get('select_team_runtime')
    if st is not None:
        try:
            st.activate_context(0)
        except Exception:
            pass


def _dispatch(orig, rc, key, reset):
    @functools.wraps(rc)
    def call(*a, **k):
        if in_ml():
            _state['ml_calls'] += 1
            if reset:
                _reset_native()
            return orig(*a, **k)
        return rc(*a, **k)
    call._rc29_ml_isolation = True
    call._rc29_original = orig
    call._rc29_rc26 = rc
    return call


def _ziru_json(original_json, z):
    @functools.wraps(original_json)
    def _json(rel):
        if not in_ml():
            return original_json(rel)
        with _lock:
            if rel in _ml_data:
                return _ml_data[rel]
            if _ziru_cache is not None and rel in _ziru_cache:
                value = _ziru_cache[rel]
            else:
                p = z.DATA / rel
                if not p.is_file():
                    raise z.NotPorted(f'{rel} not ported; run work/tools/port_ziru_data.py')
                value = json.loads(p.read_text(encoding='utf-8'))
            if rel == 'team_names.json':
                try:
                    current = original_json(rel)
                    value = dict(value)
                    for tid in REAL_NAMES:
                        if str(tid) in current:
                            value[str(tid)] = current[str(tid)]
                    for tid, nm in REAL_CLUB.items():
                        row = value.get(str(tid))
                        value[str(tid)] = dict(row, name=nm) if isinstance(row, dict) else {'name': nm, 'short': nm[:3].upper()}
                except Exception as exc:
                    _state['errors'].append('names: %r' % (exc,))
            _ml_data[rel] = value
            return value
    _json._rc29_ml_isolation = True
    return _json


def install():
    """Call after RC26 installed: route Master League calls to the V32 originals."""
    if _state['installed']:
        return _state
    for key, names in TARGETS.items():
        h = _holder(key)
        if h is None:
            continue
        for n in names:
            orig = _before.get((key, n))
            rc = _get(h, n)
            if orig is None or rc is None or rc is orig or getattr(rc, '_rc29_ml_isolation', False):
                continue
            modname = key[0] if isinstance(key, tuple) else key
            setattr(h, n, _dispatch(orig, rc, key, (modname, n) in NATIVE_RESET))
            _state['wrapped'].append('%s.%s' % (key if isinstance(key, str) else '.'.join(key), n))
    z = sys.modules.get('ziru_data')
    if z is not None and not getattr(z._json, '_rc29_ml_isolation', False):
        z._json = _ziru_json(z._json, z)
        _state['wrapped'].append('ziru_data._json')
    _state['installed'] = True
    return _state


def status():
    return dict(_state, wrapped=list(_state['wrapped']), errors=list(_state['errors']))
