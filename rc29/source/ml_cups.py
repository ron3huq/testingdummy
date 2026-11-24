"""RC29.4: two stand-alone cups inside the Master League app, fully separate from the leagues, My League and the career.

  UCL 2017   the twelve 2017 sides of RC26's Y17 league (RC26 rosters). League phase: every club plays 4 different opponents
             (2 home, 2 away) = 24 matches; 1-4 go straight to the quarter-finals, 5-12 play a two-legged play-off (5 v 12, 6 v 11,
             7 v 10, 8 v 9); quarter-finals and semi-finals over two legs like the Master League Champions League; one final on neutral ground.
             Barcelona always reach at least the semi-finals.
  AFC CL     24 Asian clubs with real squads in the game data, the Elite format: league stage of 8 matches each (4 home, 4 away),
             top 16 to a two-legged round of 16, then centralised single-match quarter-finals, semi-finals and final (Jeddah).

Every match: Poisson goals from club strength (home advantage, a seeded swing), scorers and assists from the squad by position
with the real share of the leading forwards, deterministic per (cup, run seed, match). Stats, player ratings, MVP top 3.
State: ML store meta `rc29_cup_<id>`.  API: GET /api/rc29/cups, GET /api/rc29/cups/<id>, POST /api/rc29/cups/<id>/start {team},
POST /api/rc29/cups/<id>/next, POST /api/rc29/cups/<id>/finish, POST /api/rc29/cups/<id>/reset, GET /api/rc29/cups/<id>/match/<mid>.
"""
import json, math, random, zlib, gzip
from pathlib import Path

POS = ('GK', 'CB', 'LB', 'RB', 'DMF', 'CMF', 'LMF', 'RMF', 'AMF', 'LWF', 'RWF', 'SS', 'CF')
GRP = {'GK': 'G', 'CB': 'D', 'LB': 'D', 'RB': 'D', 'DMF': 'M', 'CMF': 'M', 'LMF': 'M', 'RMF': 'M', 'AMF': 'M', 'LWF': 'F', 'RWF': 'F', 'SS': 'F', 'CF': 'F'}

# id, name, short, crest id (real club crest), colour, attack, defence
UCL17 = [
    (1220, 'Real Madrid', 'RMA', 109, '#f4f4f4', 2.35, 0.92), (1222, 'FC Barcelona', 'BAR', 108, '#a50044', 2.4, 0.96),
    (5317, 'Bayern München', 'FCB', 127, '#dc052d', 2.35, 0.92), (2365, 'Juventus', 'JUV', 120, '#111111', 1.85, 0.78),
    (1219, 'Atlético de Madrid', 'ATM', 172, '#cb3524', 1.65, 0.78), (1986, 'Paris Saint-Germain', 'PSG', 114, '#004170', 2.3, 1.0),
    (131, 'Manchester City', 'MCI', 173, '#6cabdd', 2.3, 1.05), (1987, 'Liverpool', 'LIV', 103, '#c8102e', 2.15, 1.12),
    (1221, 'Chelsea', 'CHE', 102, '#034694', 1.85, 0.95), (1985, 'Tottenham Hotspur', 'TOT', 179, '#132257', 1.95, 1.0),
    (2621, 'AS Roma', 'ROM', 125, '#8e1f2f', 1.7, 1.05), (132, 'Manchester United', 'MUN', 100, '#da291c', 1.65, 0.92),
]
AFC = [
    (17873, 'Al Hilal', 'HIL', 17873, '#1f3f99', 1.9, 0.98), (18961, 'Al Nassr', 'NAS', 18961, '#ffd100', 1.95, 1.02),
    (17733, 'Al Ahli', 'AHL', 17733, '#007a3d', 1.85, 1.0), (17734, 'Al Ittihad', 'ITT', 17734, '#f2c200', 1.82, 1.04),
    (163, 'Kawasaki Frontale', 'KAW', 163, '#00a0e9', 1.6, 1.12), (152, 'Yokohama F. Marinos', 'YFM', 152, '#0042a5', 1.55, 1.18),
    (158, 'Vissel Kobe', 'VIS', 158, '#a8002b', 1.62, 1.08), (159, 'Sanfrecce Hiroshima', 'SAN', 159, '#5c3e98', 1.55, 1.08),
    (2372, 'FC Machida Zelvia', 'MAC', 2372, '#0b318f', 1.5, 1.05), (147, 'Urawa Red Diamonds', 'URA', 147, '#e60012', 1.45, 1.12),
    (146, 'Kashima Antlers', 'KAS', 146, '#b5002d', 1.55, 1.08), (4174, 'Ulsan HD', 'ULS', 4174, '#1f4ea1', 1.5, 1.12),
    (279, 'Jeonbuk Hyundai Motors', 'JEO', 279, '#007a3e', 1.58, 1.08), (281, 'Pohang Steelers', 'POH', 281, '#c8102e', 1.4, 1.18),
    (282, 'FC Seoul', 'SEO', 282, '#b30d23', 1.38, 1.2), (5914, 'Gwangju FC', 'GWA', 5914, '#f5b800', 1.4, 1.18),
    (1493, 'Buriram United', 'BUR', 1493, '#004b98', 1.45, 1.18), (5394, 'Bangkok United', 'BKU', 5394, '#e30613', 1.3, 1.3),
    (5401, 'Port FC', 'POR', 5401, '#003b7a', 1.25, 1.35), (4948, 'Johor Darul Ta\'zim', 'JDT', 4948, '#0a2a6c', 1.45, 1.18),
    (20478, 'Shanghai Port', 'SHP', 20478, '#c8102e', 1.45, 1.2), (16679, 'Beijing Guoan', 'BGA', 16679, '#006b3f', 1.35, 1.28),
    (22498, 'Cong An Ha Noi', 'CAH', 22498, '#c8102e', 1.22, 1.35), (22428, 'Thep Xanh Nam Dinh', 'NDI', 22428, '#0f4c9c', 1.15, 1.4),
]
# extra leading scorers of these squads: name tokens -> (goal share, assist share)
CUP_STARS = {
    'ucl17': [(('lionel messi', 'messi'), 0.5, 0.22), (('cristiano ronaldo',), 0.42, 0.10), (('luis suarez', 'luis suárez'), 0.24, 0.12),
              (('neymar',), 0.18, 0.18), (('robert lewandowski', 'lewandowski'), 0.36, 0.06), (('gonzalo higuain', 'higuain'), 0.30, 0.05),
              (('paulo dybala', 'dybala'), 0.24, 0.10), (('douglas costa',), 0.12, 0.16), (('antoine griezmann', 'griezmann'), 0.32, 0.12), (('edinson cavani', 'cavani'), 0.32, 0.06),
              (('kylian mbappe',), 0.22, 0.12), (('sergio aguero', 'agüero'), 0.34, 0.06), (('mohamed salah',), 0.30, 0.12),
              (('roberto firmino',), 0.16, 0.12), (('harry kane',), 0.38, 0.06), (('edin dzeko', 'džeko'), 0.32, 0.06),
              (('romelu lukaku',), 0.30, 0.06), (('eden hazard',), 0.22, 0.14), (('alvaro morata', 'álvaro morata'), 0.22, 0.05),
              (('kevin de bruyne',), 0.10, 0.22), (('karim benzema',), 0.14, 0.12), (('gareth bale',), 0.14, 0.08), (('thomas muller', 'thomas müller'), 0.12, 0.16)],
    'afc': [(('cristiano ronaldo',), 0.40, 0.08), (('aleksandar mitrovic', 'mitrović'), 0.32, 0.05), (('karim benzema',), 0.30, 0.10),
            (('ivan toney',), 0.32, 0.05), (('riyad mahrez',), 0.16, 0.16), (('sadio mane', 'sadio mané'), 0.18, 0.12),
            (('malcom',), 0.16, 0.14), (('salem al dawsari', 'al dawsari'), 0.14, 0.14), (('steven bergwijn',), 0.14, 0.10),
            (('joao felix', 'joão félix'), 0.16, 0.12), (('kingsley coman',), 0.12, 0.12), (('marcos leonardo',), 0.24, 0.05),
            (('franck kessie', 'franck kessié'), 0.08, 0.06), (('roberto firmino',), 0.16, 0.14), (('oscar',), 0.10, 0.18),
            (('leo pele', 'leo pelé'), 0.10, 0.05)],
}
CUPS = {
    'ucl17': {'id': 'ucl17', 'name': 'UEFA Champions League 2017', 'short': 'UCL 2017', 'teams': UCL17, 'league_games': 4,
              'direct': 4, 'po': 8, 'ko_legs': {'po': 2, 'qf': 2, 'sf': 2, 'final': 1}, 'final_venue': 'Millennium Stadium, Cardiff'},
    'afc': {'id': 'afc', 'name': 'AFC Champions League Elite', 'short': 'AFC CL', 'teams': AFC, 'league_games': 8,
            'direct': 16, 'po': 0, 'ko_legs': {'r16': 2, 'qf': 1, 'sf': 1, 'final': 1}, 'final_venue': 'King Abdullah Sports City, Jeddah'},
}
# a cup-long target for a few legends (goals): the sheet is rebalanced inside his own club's goals when the cup ends
TARGETS = {'ucl17': {1222: ('lionel messi', 10, 13)}}
STAGE_NAME = {'league': 'League phase', 'po': 'Knockout play-off', 'r16': 'Round of 16', 'qf': 'Quarter-finals', 'sf': 'Semi-finals', 'final': 'Final', 'done': 'Finished'}
LG = 1.42


# ------------------------------------------------------------------ data
_cache = {}


def _tools():
    import embedded_gateway as eg
    for root in (getattr(eg, '_root', None), getattr(eg, 'ROOT', None)):
        if root:
            return Path(root) / 'work/tools'
    import myleague_73
    return Path(myleague_73.__file__).resolve().parent


def _custom():
    if 'custom' not in _cache:
        T = _tools()
        _cache['custom'] = json.loads((T / 'myleague_custom.json').read_text(encoding='utf-8'))
        try:
            _cache['base'] = json.loads(gzip.decompress((T / 'myleague_base_rosters.json.gz').read_bytes()))
        except Exception:
            _cache['base'] = {'positions': {}, 'rosters': {}}
    return _cache['custom']


def _names():
    if 'names' not in _cache:
        import my_league_opponents as mo
        _cache['names'] = mo._names()
    return _cache['names']


NAME_OVERRIDE = {88042803047215: 'Cristiano Ronaldo'}


def _name(pid):
    try:
        if int(pid) in NAME_OVERRIDE:
            return NAME_OVERRIDE[int(pid)]
    except Exception:
        pass
    v = _names().get(str(pid))
    return (v[0] if isinstance(v, list) else v) or str(pid)


def _pos(pid):
    cust = _custom()
    prof = (cust.get('classic_profiles') or {}).get(str(pid))
    if prof and prof.get('roles'):
        r = prof['roles'][0]
        return POS[r] if isinstance(r, int) and 0 <= r < 13 else str(r)
    b = (_cache.get('base') or {}).get('positions', {}).get(str(pid))
    if isinstance(b, int) and 0 <= b < 13:
        return POS[b]
    try:
        import my_league as ml
        code = ml.SIM_PLAYERS.get(int(pid), (None,))[0]
        if code is not None:
            return POS[code]
    except Exception:
        pass
    return 'CMF'


# UCL 2017: every player belongs to ONE club, all from his 2014-19 spell there (the RC26 Y17 squads borrow a few players
# from other clubs and eras; My League keeps them, this cup does not).  team -> [(remove name, add id, add position)]
U17_FIX = {
    1220: [('Cristiano Ronaldo', 88042803047215, 'LWF')],     # the user's own Ronaldo card (face-swapped Honda card)
    2365: [('Dani Alves', 105559290329771, 'RB'), ('Paul Pogba', 105804640335593, 'CMF'), ('Arturo Vidal', 105739158855570, 'LWF'), ('Lilian Thuram', 105642505376103, 'CB')],
    5317: [('Medhi Benatia', 128181, 'CB')],
    1219: [('Kieran Trippier', 44857, 'RB'), ('Diego Costa', 60235, 'CF'), ('Diego Forlán', 105566806576367, 'DMF')],
    1985: [('Gareth Bale', 105556069156811, 'RB'), ('Sergio Reguilón', 109045, 'CF')],
    1986: [('Lucas Moura', 105562243182718, 'RWF')],
    1221: [('Frank Lampard', 105631767959826, 'CMF'), ('Juan Mata', 105565464340566, 'CF')],
    2621: [('Alisson Becker', 105555532226537, 'GK'), ('Medhi Benatia', 52778974094781, 'CB'), ('Vincent Candela', 105649753077667, 'RB'), ('Aldair', 88040655558775, 'CB')],
    1222: [(None, 105565732771563, 'GK'), (None, 105705050843288, 'RB'), (None, 105748000511970, 'CB'), (None, 105811351222601, 'CMF'),
           (None, 105572712165410, 'RWF'), (None, 101065, 'AMF')],
}


def _fold(n):
    import unicodedata
    return unicodedata.normalize('NFKD', n or '').encode('ascii', 'ignore').decode().lower().strip()


def roster(cup, team):
    key = (cup, team)
    if key in _cache:
        return _cache[key]
    cust = _custom()
    ids = []
    if cup == 'ucl17':
        ids = list(cust.get('native_rosters', {}).get(str(team)) or [])
    else:
        ids = list(cust.get('native_rosters', {}).get(str(team)) or cust.get('simulation_rosters', {}).get(str(team)) or [])
        if not ids:
            try:
                import ziru_data
                ids = list(ziru_data.rosters().get(str(team)) or [])
            except Exception:
                ids = []
    rows = []
    seen = set()
    for pid in ids:
        if pid in seen:
            continue
        seen.add(pid)
        rows.append({'pid': int(pid), 'name': _name(pid), 'pos': _pos(pid)})
    slots = (cust.get('classic_teams') or {}).get(str(team), {}).get('slots') if cup == 'ucl17' else None
    if slots:
        # the RC26 Y17 squad sheet: real roles and the real starting eleven
        rows = [{'pid': int(x['player_id']), 'name': x.get('name') or _name(x['player_id']), 'pos': x.get('role') or _pos(x['player_id']), 'start': bool(x.get('starting'))} for x in slots]
    if cup == 'ucl17':
        for old, new, pos in U17_FIX.get(team, ()):
            at = next((i for i, r in enumerate(rows) if old and _fold(r['name']) == _fold(old)), None)
            row = {'pid': new, 'name': _name(new), 'pos': pos, 'start': False} if new else None
            if at is None:
                if row:
                    rows.append(row)
            elif row:
                row['start'] = rows[at].get('start', False)
                rows[at] = row
            else:
                rows.pop(at)
    if slots and sum(1 for r in rows if r.get('start')) == 11:
        xi = [r for r in rows if r.get('start')]
        bench = [r for r in rows if not r.get('start')]
        for r in xi:
            r['xi'] = True
        _cache[key] = (xi, bench)
        return _cache[key]
    # a match XI: 1 GK, 4 D, 3 M, 3 F in roster order (the roster lists the regular starters first)
    need = {'G': 1, 'D': 4, 'M': 3, 'F': 3}
    xi, bench = [], []
    for r in rows:
        g = GRP.get(r['pos'], 'M')
        if need.get(g, 0) > 0:
            need[g] -= 1
            xi.append(r)
        else:
            bench.append(r)
    while len(xi) < 11 and bench:
        xi.append(bench.pop(0))
    for r in xi:
        r['xi'] = True
    _cache[key] = (xi, bench)
    return _cache[key]


def team_row(cup, tid):
    for t in CUPS[cup]['teams']:
        if t[0] == tid:
            return t
    return None


def team_doc(cup, tid):
    t = team_row(cup, tid)
    return {'id': t[0], 'name': t[1], 'short': t[2], 'crest': t[3], 'c': t[4]}


# ------------------------------------------------------------------ model
def _rng(*parts):
    return random.Random(zlib.crc32(':'.join(str(p) for p in parts).encode()))


def _poisson(rng, lam):
    lam = max(0.05, min(5.0, lam))
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p < limit:
            return k
        k += 1


def strength(cup, seed, tid):
    t = team_row(cup, tid)
    r = _rng('cupform', cup, seed, tid)
    return t[5] * math.exp(r.gauss(0, 0.07)), t[6] / math.exp(r.gauss(0, 0.07))


def play(cup, seed, mid, home, away, neutral=False, scale=1.0):
    ah, dh = strength(cup, seed, home)
    aa, da = strength(cup, seed, away)
    hf, af = (1.0, 1.0) if neutral else (1.13, 0.9)
    r = _rng('cupmatch', cup, seed, mid)

    def damp(g):
        # elite knockout football rarely runs riot: every goal past the third survives only half the time
        return min(g, 3) + sum(1 for _ in range(max(0, g - 3)) if r.random() < 0.5)
    return (damp(_poisson(r, min(2.8, ah * da / (LG * 1.08) * hf) * scale)),
            damp(_poisson(r, min(2.8, aa * dh / (LG * 1.08) * af) * scale)))


def _star(cup, name):
    import ml_realism as M
    n = ' ' + M._norm(name) + ' '
    for keys, g, a in CUP_STARS.get(cup, []):
        if any(' ' + M._norm(k) + ' ' in n for k in keys):
            return g, a
    return M.star_of(name)


def _weights(cup, players, assist):
    import ml_realism as M
    table = M.ASSIST_POS if assist else M.SCORE_POS
    cands = [(p['pid'], p['name'], table.get(p['pos'], 2.0) * (1.0 if p.get('xi') else 0.25)) for p in players]
    shares = {}
    for pid, name, w in cands:
        st = _star(cup, name)
        if st and w > 0:
            shares[pid] = st[1] if assist else st[0]
    total = sum(shares.values())
    if total > 0.8:
        shares = {k: v * 0.8 / total for k, v in shares.items()}
        total = 0.8
    rest = sum(w for pid, n, w in cands if pid not in shares)
    out = {pid: w for pid, n, w in cands}
    if shares and rest > 0:
        for pid, s in shares.items():
            out[pid] = s / (1 - total) * rest
    return out


def sheet(cup, seed, mid, team, goals, index):
    """[(scorer pid, assist pid | None)] for `goals` goals of `team`; `index` = the team's goals before this match (low-discrepancy)."""
    import ml_realism as M
    xi, bench = roster(cup, team)
    players = xi + bench[:5]
    if not players:
        return []
    gw, aw = _weights(cup, players, False), _weights(cup, players, True)
    keys = [p['pid'] for p in players]
    r = _rng('cupsheet', cup, seed, mid, team)
    off = (zlib.crc32(('%s:%s:%s' % (cup, seed, team)).encode()) % 1000) / 1000.0
    out = []
    for k in range(int(goals)):
        n = index + k
        sc = M.spread_pick(keys, [gw[x] for x in keys], n * M.PHI + off)
        ast = None
        if r.random() < 0.8:
            opts = [x for x in keys if x != sc]
            ast = M.spread_pick(opts, [aw[x] for x in opts], n * M.PHI + off + 0.37)
        out.append((sc, ast))
    return out


def ratings(cup, seed, mid, team, gf, ga, goals):
    xi, bench = roster(cup, team)
    r = _rng('cuprate', cup, seed, mid, team)
    g, a = {}, {}
    for sc, ast in goals:
        g[sc] = g.get(sc, 0) + 1
        if ast:
            a[ast] = a.get(ast, 0) + 1
    rows = []
    for p in xi + [b for b in bench if b['pid'] in g or b['pid'] in a]:
        v = 6.4 + 0.95 * g.get(p['pid'], 0) + 0.55 * a.get(p['pid'], 0) + (0.35 if gf > ga else -0.3 if gf < ga else 0) + r.gauss(0, 0.3)
        if GRP.get(p['pos']) in ('G', 'D'):
            v += 0.35 if ga == 0 else -0.12 * ga
        rows.append({'pid': p['pid'], 'name': p['name'], 'pos': p['pos'], 'g': g.get(p['pid'], 0), 'a': a.get(p['pid'], 0), 'r': round(max(4.6, min(10.0, v)), 1)})
    rows.sort(key=lambda x: -x['r'])
    return rows


# ------------------------------------------------------------------ fixtures
def league_rounds(cup, seed):
    """`league_games` rounds of pairings, no repeated pairing, every club home in half of its games."""
    teams = [t[0] for t in CUPS[cup]['teams']]
    n = CUPS[cup]['league_games']
    r = _rng('cupdraw', cup, seed)
    for attempt in range(400):
        used, rounds, ok = set(), [], True
        for k in range(n):
            pool = teams[:]
            r.shuffle(pool)
            pairs = []
            while pool:
                a = pool.pop()
                opts = [b for b in pool if frozenset((a, b)) not in used]
                if not opts:
                    ok = False
                    break
                b = opts[0]
                pool.remove(b)
                used.add(frozenset((a, b)))
                pairs.append([a, b])
            if not ok:
                break
            rounds.append(pairs)
        if ok:
            break
    # orient: every club plays half its games at home (greedy balance)
    homes = {t: 0 for t in teams}
    for rd in rounds:
        for p in rd:
            a, b = p
            if homes[a] > homes[b] or (homes[a] == homes[b] and r.random() < 0.5):
                p[0], p[1] = b, a
            homes[p[0]] += 1
    return rounds


# ------------------------------------------------------------------ state
def _key(cup):
    return 'rc29_cup_' + cup


def _store():
    import iml_news_leagues as nl
    return nl.store


def load(conn, cup):
    try:
        return json.loads(_store().get_meta(conn, _key(cup), '') or 'null')
    except Exception:
        return None


def save(conn, cup, st):
    _store().set_meta(conn, _key(cup), json.dumps(st))
    try:
        conn.commit()
    except Exception:
        pass


def start(conn, cup, team):
    if cup not in CUPS or team_row(cup, int(team)) is None:
        return {'error': 'bad-team'}
    seed = random.randrange(1, 10 ** 9)
    rounds = league_rounds(cup, seed)
    st = {'v': 1, 'cup': cup, 'team': int(team), 'seed': seed, 'stage': 'league',
          'league': [[{'id': 'L%d-%d' % (i + 1, j), 'h': h, 'a': a, 'hg': None, 'ag': None} for j, (h, a) in enumerate(rd)] for i, rd in enumerate(rounds)],
          'ko': [], 'sheets': {}, 'goals_index': {}, 'champion': None}
    save(conn, cup, st)
    return view(st)


def _settle(st, m, neutral=False, scale=1.0):
    cup, seed = st['cup'], st['seed']
    hg, ag = play(cup, seed, m['id'], m['h'], m['a'], neutral, scale)
    m['hg'], m['ag'] = hg, ag
    gi = st['goals_index']
    hs = sheet(cup, seed, m['id'], m['h'], hg, gi.get(str(m['h']), 0))
    as_ = sheet(cup, seed, m['id'], m['a'], ag, gi.get(str(m['a']), 0))
    gi[str(m['h'])] = gi.get(str(m['h']), 0) + hg
    gi[str(m['a'])] = gi.get(str(m['a']), 0) + ag
    st['sheets'][m['id']] = {'h': hs, 'a': as_}


def table(st):
    cup = st['cup']
    rows = {t[0]: {'team': t[0], 'p': 0, 'w': 0, 'd': 0, 'l': 0, 'gf': 0, 'ga': 0, 'pts': 0} for t in CUPS[cup]['teams']}
    for rd in st['league']:
        for m in rd:
            if m['hg'] is None:
                continue
            h, a = rows[m['h']], rows[m['a']]
            h['p'] += 1; a['p'] += 1
            h['gf'] += m['hg']; h['ga'] += m['ag']; a['gf'] += m['ag']; a['ga'] += m['hg']
            if m['hg'] > m['ag']:
                h['w'] += 1; a['l'] += 1; h['pts'] += 3
            elif m['hg'] < m['ag']:
                a['w'] += 1; h['l'] += 1; a['pts'] += 3
            else:
                h['d'] += 1; a['d'] += 1; h['pts'] += 1; a['pts'] += 1
    form = {t: [] for t in rows}
    for rd in st['league']:
        for m in rd:
            if m['hg'] is None:
                continue
            rh = 'W' if m['hg'] > m['ag'] else 'L' if m['hg'] < m['ag'] else 'D'
            form[m['h']].append(rh)
            form[m['a']].append({'W': 'L', 'L': 'W', 'D': 'D'}[rh])
    # tie-breakers: points, goal difference, goals scored, wins, then the club name A-Z (so an unplayed table reads alphabetically)
    out = sorted(rows.values(), key=lambda x: (-x['pts'], -(x['gf'] - x['ga']), -x['gf'], -x['w'], _sort_name(cup, x['team'])))
    for i, r in enumerate(out):
        r['pos'] = i + 1
        r['gd'] = r['gf'] - r['ga']
        r['form'] = form[r['team']][-5:]
    return out


def _sort_name(cup, tid):
    import unicodedata
    n = (team_row(cup, tid) or (0, str(tid)))[1]
    n = unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()
    return n


def _tie(st, stage, a, b, n):
    """a = the better-placed club (home in the last leg)."""
    legs = []
    if CUPS[st['cup']]['ko_legs'][stage] == 2:
        legs = [{'id': '%s-%d-1' % (stage, n), 'h': b, 'a': a, 'hg': None, 'ag': None},
                {'id': '%s-%d-2' % (stage, n), 'h': a, 'a': b, 'hg': None, 'ag': None}]
    else:
        legs = [{'id': '%s-%d' % (stage, n), 'h': a, 'a': b, 'hg': None, 'ag': None, 'neutral': stage in ('qf', 'sf', 'final') and st['cup'] == 'afc' or stage == 'final'}]
    return {'stage': stage, 'a': a, 'b': b, 'legs': legs, 'agg': None, 'et': None, 'pens': None, 'winner': None}


def _resolve(st, t):
    cup, seed = st['cup'], st['seed']
    ga = gb = 0
    for l in t['legs']:
        if l['h'] == t['a']:
            ga += l['hg']; gb += l['ag']
        else:
            ga += l['ag']; gb += l['hg']
    last = t['legs'][-1]
    if ga == gb:
        eh, ea = play(cup, seed, last['id'] + ':et', last['h'], last['a'], last.get('neutral', False), 1 / 3.0)
        last['et'] = [eh, ea]
        gi = st['goals_index']
        hs = sheet(cup, seed, last['id'] + ':et', last['h'], eh, gi.get(str(last['h']), 0))
        as_ = sheet(cup, seed, last['id'] + ':et', last['a'], ea, gi.get(str(last['a']), 0))
        gi[str(last['h'])] = gi.get(str(last['h']), 0) + eh
        gi[str(last['a'])] = gi.get(str(last['a']), 0) + ea
        st['sheets'][last['id']]['h'] += hs
        st['sheets'][last['id']]['a'] += as_
        if last['h'] == t['a']:
            ga += eh; gb += ea
        else:
            ga += ea; gb += eh
        t['et'] = True
    # Barcelona always reach the semi-finals of the 2017 cup: a late comeback in the last leg
    if cup == 'ucl17' and t['stage'] in ('po', 'qf') and 1222 in (t['a'], t['b']):
        barca_a = t['a'] == 1222
        if (ga <= gb) if barca_a else (gb <= ga):
            need = (gb - ga if barca_a else ga - gb) + 1
            side = 'h' if last['h'] == 1222 else 'a'
            last['hg' if side == 'h' else 'ag'] += need
            st['sheets'][last['id']][side] += sheet(cup, seed, last['id'] + ':late', 1222, need, st['goals_index'].get('1222', 0))
            st['goals_index']['1222'] = st['goals_index'].get('1222', 0) + need
            if barca_a:
                ga += need
            else:
                gb += need
    if ga == gb:
        r = _rng('cuppens', cup, seed, t['legs'][-1]['id'])
        sa = strength(cup, seed, t['a'])[0]
        sb = strength(cup, seed, t['b'])[0]
        pa = 0.5 + (sa - sb) * 0.08
        win_a = r.random() < pa
        x, y = (5, 4) if r.random() < 0.6 else (4, 3)
        t['pens'] = [x, y] if win_a else [y, x]
        t['winner'] = t['a'] if win_a else t['b']
    else:
        t['winner'] = t['a'] if ga > gb else t['b']
    t['agg'] = [ga, gb]


def _next_stage(st):
    cup = CUPS[st['cup']]
    order = ['league'] + [s for s in ('po', 'r16', 'qf', 'sf', 'final') if s in cup['ko_legs']]
    return order[order.index(st['stage']) + 1] if st['stage'] in order and order.index(st['stage']) + 1 < len(order) else 'done'


def _draw(st, stage, prev_stage=None):
    cup = CUPS[st['cup']]
    tb = [r['team'] for r in table(st)]
    prev = [t for t in st['ko'] if t['stage'] == prev_stage]
    ties = []
    if stage == 'po':
        top, mid = tb[:cup['direct']], tb[cup['direct']:cup['direct'] + cup['po']]
        for i in range(len(mid) // 2):
            ties.append(_tie(st, 'po', mid[i], mid[-1 - i], i + 1))
    elif stage == 'r16':
        top = tb[:16]
        for i in range(8):
            ties.append(_tie(st, 'r16', top[i], top[15 - i], i + 1))
    elif stage == 'qf':
        if st['cup'] == 'ucl17':
            po = [t['winner'] for t in st['ko'] if t['stage'] == 'po']        # po ties: 5v12, 6v11, 7v10, 8v9
            pairs = [(tb[0], po[3]), (tb[1], po[2]), (tb[2], po[1]), (tb[3], po[0])]
        else:
            w = [t['winner'] for t in prev]
            pairs = [(w[0], w[7]), (w[3], w[4]), (w[1], w[6]), (w[2], w[5])]
        for i, (a, b) in enumerate(pairs):
            ties.append(_tie(st, 'qf', a, b, i + 1))
    elif stage == 'sf':
        w = [t['winner'] for t in prev]
        for i, (a, b) in enumerate([(w[0], w[1]), (w[2], w[3])]):
            ties.append(_tie(st, 'sf', a, b, i + 1))
    elif stage == 'final':
        w = [t['winner'] for t in prev]
        ties.append(_tie(st, 'final', w[0], w[1], 1))
        ties[0]['legs'][0]['neutral'] = True
    st['ko'].extend(ties)


def step(conn, cup):
    """Play the next match day (one league round, or one leg of every tie of the stage)."""
    st = load(conn, cup)
    if not st:
        return {'error': 'not-started'}
    if st['stage'] == 'done':
        return view(st)
    if st['stage'] == 'league':
        rd = next((rd for rd in st['league'] if rd[0]['hg'] is None), None)
        if rd:
            for m in rd:
                _settle(st, m)
        if all(m['hg'] is not None for rd in st['league'] for m in rd):
            nxt = _next_stage(st)
            st['stage'] = nxt
            _draw(st, nxt, 'league')
    else:
        ties = [t for t in st['ko'] if t['stage'] == st['stage']]
        leg_no = next((i for i in range(len(ties[0]['legs'])) if ties[0]['legs'][i]['hg'] is None), None)
        if leg_no is not None:
            for t in ties:
                _settle(st, t['legs'][leg_no], neutral=t['legs'][leg_no].get('neutral', False))
        if all(l['hg'] is not None for t in ties for l in t['legs']):
            for t in ties:
                _resolve(st, t)
            if st['stage'] == 'final':
                st['champion'] = ties[0]['winner']
                st['stage'] = 'done'
                _targets(st)
            else:
                prev_stage = st['stage']
                nxt = _next_stage(st)
                st['stage'] = nxt
                _draw(st, nxt, prev_stage)
    save(conn, cup, st)
    return view(st)


def _targets(st):
    import ml_realism as M
    for team, (who, lo, hi) in (TARGETS.get(st['cup']) or {}).items():
        xi, bench = roster(st['cup'], team)
        star = next((p['pid'] for p in xi + bench if M._norm(who) in M._norm(p['name'])), None)
        if star is None:
            continue
        slots = []      # (match id, side, index) of every goal of the club
        for mid in sorted(st['sheets']):
            sh = st['sheets'][mid]
            for side in ('h', 'a'):
                for i, (sc, ast) in enumerate(sh[side]):
                    if any(p['pid'] == sc for p in xi + bench):
                        slots.append((mid, side, i))
        mine = [x for x in slots if st['sheets'][x[0]][x[1]][x[2]][0] == star]
        other = [x for x in slots if st['sheets'][x[0]][x[1]][x[2]][0] != star]
        r = _rng('target', st['cup'], st['seed'], team)
        goal = r.randint(lo, hi)
        r.shuffle(other)
        r.shuffle(mine)
        while len(mine) < goal and other:
            mid, side, i = other.pop()
            sc, ast = st['sheets'][mid][side][i]
            st['sheets'][mid][side][i] = [star, sc if ast == star else ast]
            mine.append((mid, side, i))
        while len(mine) > goal:
            mid, side, i = mine.pop()
            sc, ast = st['sheets'][mid][side][i]
            mate = next((p['pid'] for p in xi if p['pid'] != star and GRP.get(p['pos']) == 'F'), None) or next(p['pid'] for p in xi if p['pid'] != star)
            st['sheets'][mid][side][i] = [mate, star if ast is None or ast == mate else ast]


def finish(conn, cup):
    for _ in range(40):
        st = load(conn, cup)
        if not st or st['stage'] == 'done':
            break
        step(conn, cup)
    return view(load(conn, cup))


def reset(conn, cup):
    _store().set_meta(conn, _key(cup), 'null')
    try:
        conn.commit()
    except Exception:
        pass
    return {'ok': True}


# ------------------------------------------------------------------ views
def stats(st):
    cup = st['cup']
    goals, assists, team_of = {}, {}, {}
    apps = {}
    for mid, sh in st['sheets'].items():
        for side in ('h', 'a'):
            for sc, ast in sh[side]:
                goals[sc] = goals.get(sc, 0) + 1
                if ast:
                    assists[ast] = assists.get(ast, 0) + 1
    for t in CUPS[cup]['teams']:
        xi, bench = roster(cup, t[0])
        for p in xi + bench:
            team_of[p['pid']] = (t[0], p['name'])
    def tb(d):
        rows = sorted(d.items(), key=lambda x: (-x[1], team_of.get(x[0], (0, ''))[1]))[:25]
        return [{'rank': i + 1, 'pid': pid, 'name': team_of.get(pid, (0, _name(pid)))[1], 'team': team_of.get(pid, (None,))[0], 'n': n} for i, (pid, n) in enumerate(rows)]
    return tb(goals), tb(assists), goals, assists, team_of


def mvp(st):
    if st['stage'] != 'done':
        return []
    g_tab, a_tab, goals, assists, team_of = stats(st)
    reach = {}
    for t in st['ko']:
        for x in (t['a'], t['b']):
            reach[x] = t['stage']
    stage_pts = {'final': 18, 'sf': 9, 'qf': 4, 'r16': 2, 'po': 1}
    rows = []
    for pid, (team, name) in team_of.items():
        g, a = goals.get(pid, 0), assists.get(pid, 0)
        if not g and not a:
            continue
        pts = 5 * g + 3.2 * a + (30 if team == st['champion'] else stage_pts.get(reach.get(team), 0))
        rows.append({'pid': pid, 'name': name, 'team': team, 'goals': g, 'assists': a, 'points': round(pts, 1)})
    rows.sort(key=lambda r: (-r['points'], -r['goals']))
    for i, r in enumerate(rows[:3]):
        r['rank'] = i + 1
    return rows[:3]


# ------------------------------------------------------------------ news desk (Football-Manager-style media feed, rebuilt from the stored cup each time)
OUTLETS = ('Cup Desk', 'Matchday Wire', 'The Touchline', 'Tactics Lab', 'Press Room', 'Fan Zone', 'Data Room', 'Pundit Panel')
MANAGERS = {1220: 'Zinedine Zidane', 1222: 'Luis Enrique', 5317: 'Carlo Ancelotti', 2365: 'Massimiliano Allegri', 1219: 'Diego Simeone',
            1986: 'Unai Emery', 131: 'Pep Guardiola', 1987: 'Jürgen Klopp', 1221: 'Antonio Conte', 1985: 'Mauricio Pochettino', 2621: 'Luciano Spalletti',
            132: 'José Mourinho', 17873: 'Simone Inzaghi', 18961: 'Jorge Jesus', 17733: 'Matthias Jaissle', 17734: 'Laurent Blanc'}
KO_LABEL = {'po': 'Play-off', 'r16': 'Round of 16', 'qf': 'Quarter-final', 'sf': 'Semi-final', 'final': 'Final'}


def _rating(cup, tid):
    t = team_row(cup, tid)
    return t[5] / t[6]


def _short_pl(name):
    parts = (name or '').split()
    return parts[-1] if parts else name


def _pick(r, *opts):
    return opts[r.randrange(len(opts))]


NICK = {1220: 'Real Madrid', 1222: 'Barça', 5317: 'Bayern', 2365: 'Juve', 1219: 'Atlético', 1986: 'PSG', 131: 'City', 1987: 'Liverpool',
        1221: 'Chelsea', 1985: 'Spurs', 2621: 'Roma', 132: 'United', 17873: 'Al Hilal', 18961: 'Al Nassr', 17733: 'Al Ahli', 17734: 'Al Ittihad',
        163: 'Frontale', 152: 'Marinos', 158: 'Vissel', 159: 'Sanfrecce', 147: 'Urawa', 146: 'Kashima', 4174: 'Ulsan', 279: 'Jeonbuk', 282: 'FC Seoul',
        1493: 'Buriram', 4948: 'JDT', 20478: 'Shanghai Port', 16679: 'Guoan', 22498: 'CAHN', 22428: 'Nam Định'}
HL = {
    'late': ('{w} snatch it at the death against {l}', 'Heartbreak for {l} as {p} strikes in the {m}\'', 'Last-gasp {p}! {w} steal the show',
             '{m}\' — and {p} breaks {l} hearts', 'Never in doubt? {w} leave it late to sink {l}', 'Stoppage-time stunner: {w} {s} {l}'),
    'comeback': ('From behind to brilliant: {w} roar back against {l}', '{w} rise from the canvas to floor {l}', 'Comeback kings! {w} turn {l} upside down',
                 '{l} let it slip as {w} fight back', 'Down but never out — {w} stun {l}'),
    'goalless': ('Chess, not football: {h} and {a} cancel out', 'Nothing to separate {h} and {a} in a tactical arm-wrestle', 'Keepers on top as {h} and {a} share a blank',
                 'Stalemate under the lights between {h} and {a}'),
    'draw': ('All square in a thriller: {h} {s} {a}', 'Spoils shared as {h} and {a} trade blows', '{h} and {a} can\'t be separated',
             'Point apiece — but who blinked first between {h} and {a}?', 'Honours even in a game of moments'),
    'upset': ('Giant-killers! {w} topple {l}', 'Nobody saw that coming: {w} beat {l}', '{w} rip up the script against {l}',
              'Shockwaves across Europe as {w} down {l}', 'Underdogs bite: {w} {s} {l}'),
    'thrash': ('{w} run riot: {s} against {l}', 'Statement made — {w} put {s} past {l}', 'Total football from {w} in {s} rout of {l}',
               '{p} leads the charge as {w} brush {l} aside'),
    'win': ('{p} the difference as {w} edge {l}', '{w} grind past {l}', '{w} do the job against {l}', 'Job done: {w} {s} {l}',
            '{p} decides it for {w}', 'Three more points for {w} at {l}\'s expense', '{w} keep marching with win over {l}'),
    'drought': ('Where have the goals gone, {p}?', '{p} hunts for answers as drought drags on', 'Fire fading? Pressure mounts on {p}',
                'Three games, zero goals: {p} under the microscope', '{b} backs {p} amid goal drought'),
    'potm': ('{p} lights up {when}', 'Unplayable: {p} owns {when}', 'The {when} belonged to {p}', 'Star of the show: {p}'),
    'table': ('{t} out in front after {when}', 'Top of the pile: {t}', '{t} set the pace', 'Eyes on {t} — leaders after {when}'),
    'war': ('{b1} fires back at {b2}', 'Temperature rising: {b1} vs {b2}', '"Not here to make friends" — {b1} turns up the heat',
            'Rivalry boils over as {b1} answers {b2}'),
    'ref': ('{b} fumes at the officials', '"Everybody saw it" — {b} blasts referee', 'VAR fury: {b} demands answers', 'Robbed? {b} sees red over key call'),
    'sulk': ('{p} storms off after being hooked', 'Trouble brewing? {p} furious at substitution', 'Tunnel tantrum from {p}'),
    'through': ('{w} march on — {l} go home', 'Into the hat! {w} book their place', '{w} survive the test of {l}', 'Curtains for {l} as {w} progress'),
    'champions': ('{w} are kings of {c}!', 'Glory night: {w} lift the {c} trophy', 'History made — {w} conquer {c}', 'Champions! {w} complete the job'),
    'race': ('{p} sets the pace in the Golden Boot race', '{p} out in front with {n}', 'Catch him if you can: {p} on {n}', 'Boot race heats up — {p} leads on {n}'),
    'boot': ('{p} claims the Golden Boot with {n}', 'Top of the scoring charts: {p} ({n})', '{n} and the crown for {p}'),
    'mvp': ('{p} crowned player of the tournament', 'The best of the best: {p}', '{p} walks away with the MVP award'),
    'preview': ('The draw is in — and {t} are the team to beat', 'Bookies install {t} as favourites', 'Let the games begin: all eyes on {t}'),
    'next': ('{h} vs {a}: the tie everyone wants to see', 'Showdown! {h} take on {a}', 'Clear your diary: {h} – {a}', '{h} vs {a} — a night for the history books?'),
    'loser': ('{p} breaks the silence after defeat', '"No excuses" — {p} faces the music', '{p}: "The dressing room is silent"'),
}


def _nick(cup, tid):
    return NICK.get(tid) or team_row(cup, tid)[1]


def _hl(r, kind, **kw):
    return _pick(r, *HL[kind]).format(**kw)


def _boss(tid):
    return MANAGERS.get(tid) or 'the head coach'


RIVALS = {frozenset(x) for x in ((1220, 1222), (131, 132), (1987, 132), (1221, 1985), (1220, 1219), (2365, 2621), (17873, 18961), (17733, 17734),
                                 (17873, 17734), (279, 4174), (22498, 22428), (163, 152))}
WIN_Q = ('We controlled the game from the first minute. The players deserve all the credit.', 'This is the mentality I want - hungry, brave, together.',
         'We suffered at times, but great teams know how to win these nights.', 'I am proud, but we have won nothing yet. Next game.',
         'Tactically we were perfect in the first half. In the second we had to defend, and we did it as a family.')
LOSS_Q = ('We were not at our level tonight. I take responsibility.', 'Football can be cruel. We created enough to win but we were not clinical.',
          'It hurts, but there is still everything to play for. We will react.', 'Small details decide this competition, and tonight they went against us.',
          'I will not hide behind excuses. We were second best in every duel.')
DRAW_Q = ('A fair result. Both teams had their moments.', 'We wanted the three points, but this keeps us alive.', 'Not perfect, not a disaster. We move on.',
          'When you cannot win, you must not lose. That is maturity.')
SCORER_Q = ('The ball fell to me and I just had to stay calm.', 'I saw the keeper off his line and tried my luck. Sometimes it goes in.',
            'Credit to {a} - that pass was perfect, I only had to finish it.', 'Nights like this are why you play football.',
            'I dedicate this goal to my family and to the fans who travelled.', 'Every goal matters in this competition. I want more.',
            'We worked on that move all week in training. Beautiful when it comes off.')
HAT_Q = ('A hat-trick on this stage... I am keeping the ball, and everyone is signing it.', 'I did not even know it was three until the lads told me!',
         'Three goals, but the most important thing is the result.')
LOSER_Q = ('We have to look at ourselves in the mirror. No excuses.', 'It is on us, the players. The coach gave us a plan and we did not follow it.',
           'The dressing room is silent. That says everything.')


# real voices: how each star / coach actually talks (used for the scorer interview and the press conference)
PERSONA = {
    'cristiano ronaldo': ('I work every day to be the best. The numbers speak for themselves.', 'Siuuu! When the team needs me, I am there. Always.',
                          'People doubt me every year. Every year I answer.', 'Goals are my job. Trophies are my obsession.'),
    'lionel messi': ('The important thing is that the team won. The goal is for all of us.', 'I am happy, but we must keep going. It is a long way.',
                     'I just try to enjoy it, like when I was a kid in Rosario.'),
    'zlatan ibrahimovic': ('Zlatan does not need luck. Zlatan needs the ball.', 'They wanted a show. I gave them a show. You are welcome.',
                           'I came, I scored. Like a lion. Next question.'),
    'neymar': ('Joga bonito! I play with joy, that is my football.', 'I dedicate this to my son and my family. Tamo junto!', 'If they kick me, I get up and dribble again.'),
    'luis suarez': ('I live for these nights. I give everything, every ball.', 'A striker must be hungry. Today I was hungry.', 'The fans of Barcelona deserve this.'),
    'antoine griezmann': ('Happy, happy! I did my little dance, the dressing room loves it.', 'I always work for the team first, the goals come after.'),
    'harry kane': ('Pleased to get on the scoresheet, but it is all about the team.', 'Proud of the lads. We stuck to the game plan.', 'Just doing my job - I want to keep improving.'),
    'mohamed salah': ('Alhamdulillah. I am grateful, and the team was amazing.', 'I want to win trophies with this club, nothing else.', 'The fans give us energy. This is for them.'),
    'robert lewandowski': ('A professional performance. We prepared well and executed it.', 'Hard work, good diet, good sleep - and then goals.', 'For a striker the next goal is always the most important.'),
    'kylian mbappe': ('I want to write history. Tonight was a step.', 'Speed, confidence - I felt that I could make the difference.', 'I am young, but I am not afraid of these nights.'),
    'eden hazard': ('Honestly? I just enjoy it. When you enjoy, you play well.', 'I take the ball and I go. Football is simple for me.'),
    'gareth bale': ('Great result for the club. I felt good and fit tonight.', 'Big games need big moments. Happy to have helped.'),
    'paul pogba': ('Pogba is back, baby! Seriously - the team was fantastic.', 'I play with a smile. When I smile, I play my best football.'),
    'sergio aguero': ('Ha! It was a good one, no? I am very happy, very happy.', 'I just wanted to score for Pep and the lads. Vamos!'),
    'edinson cavani': ('Thanks to God and to my teammates. We fight together.', 'Sacrifice, always sacrifice. That is my football.'),
    'karim benzema': ('Simple. I play for the team.', 'I do not speak much. I prefer the pitch.'),
    'diego costa': ('They kicked me, I kicked the ball into the net. Fair.', 'This is football for men. I love these battles.'),
    'francesco totti': ('For Roma, always for Roma. One shirt, one city, one love.', 'At my age, these nights still give me goosebumps.'),
    'thomas muller': ('I am the Raumdeuter - I find the space, and today the space found the ball!', 'Not the prettiest goal, but they all count, ja?'),
    'kevin de bruyne': ('I just try to make the right pass at the right moment.', 'Good performance from everybody. We keep going.'),
    'wayne rooney': ('Get in! That is what this club is about.', 'Big game, big goal. We needed that.'),
    'sergio ramos': ('We are Real Madrid. We never give up, never.', 'Ninety minutes in this stadium are very long - ask our opponents.'),
    'paulo dybala': ('I made the mask for the fans. They know what it means.', 'I am happy for the goal, but more for the win.'),
    'edin dzeko': ('In Italy they said I was finished. I keep scoring.', 'Simple finish, good assist. Roma deserved it.'),
    'aleksandar mitrovic': ('I score goals, that is what I do. In Saudi, in England, everywhere.',), 'riyad mahrez': ('A bit of magic tonight, inshallah more to come.',),
    'sadio mane': ('For my village, for Senegal. I am very proud.',), 'ivan toney': ('Penalties? I don\'t even look at the keeper. Never have.',),
}
BOSS_VOICE = {
    'José Mourinho': {'W': ('I am not going to speak about my team. You saw it. Special.', 'They wanted to park the bus? We parked a plane.'),
                      'L': ('I prefer not to speak. If I speak, I am in big trouble.', 'Respect. Respect. Respect.'), 'D': ('A point. Some people will cry, I will not.',)},
    'Pep Guardiola': {'W': ('The way we control the space, the positional play - I am so proud.', 'Amazing, amazing, amazing. The players were incredible.'),
                      'L': ('We were not good enough with the ball. I take the blame.',), 'D': ('We created a lot, but football is about the boxes.',)},
    'Jürgen Klopp': {'W': ('Boom! What a night. Heavy metal football!', 'The boys were absolutely outstanding. I am so happy.'),
                     'L': ('It is not nice, but we will be ready again. Mentality monsters.',), 'D': ('We had the chances. Next time, they go in.',)},
    'Diego Simeone': {'W': ('Partido a partido. Match by match. Nothing more.', 'Effort is not negotiable. Tonight we were warriors.'),
                      'L': ('We continue. Partido a partido.',), 'D': ('Hard match, hard team. We compete, always.',)},
    'Antonio Conte': {'W': ('We worked like dogs this week. This is the result.', 'Intensity, intensity, intensity. I want this every game.'),
                      'L': ('I am angry. Very angry. We must change things.',), 'D': ('Not enough. With me, a draw is not enough.',)},
    'Zinedine Zidane': {'W': ('I am content with my players. They did everything well.',), 'L': ('It happens. We stay calm and continue working.',), 'D': ('A normal match. We continue.',)},
    'Carlo Ancelotti': {'W': ('Calm, calm. We played with balance and quality.',), 'L': ('We will analyse calmly. No drama.',), 'D': ('A fair result. Football is like this.',)},
    'Massimiliano Allegri': {'W': ('Football is simple. Defend well, take your chances. We did.',), 'L': ('Sometimes you win, sometimes you learn. Calma.',), 'D': ('Corto muso - in Italy a draw away is not bad.',)},
    'Luis Enrique': {'W': ('The players executed what we trained. That is all.', 'We were the better team. Clear.'),
                     'L': ('I will not look for excuses. We will improve.',), 'D': ('Not the result we wanted. Next.',)},
    'Mauricio Pochettino': {'W': ('Dream, believe - and work very hard. Tonight we did.',), 'L': ('Pain is part of the process. We grow from this.',), 'D': ('We keep building. Step by step.',)},
    'Luciano Spalletti': {'W': ('Roma played like an orchestra tonight.',), 'L': ('Football is a strange animal. Tomorrow we work.',), 'D': ('A draw that tastes of both sweet and bitter.',)},
    'Unai Emery': {'W': ('Good ebening. Very good match, very good players!',), 'L': ('We need to analyse with calm, with our idea.',), 'D': ('Our idea was good. The result, okay.',)},
    'Jorge Jesus': {'W': ('With me, teams win. It is simple.',), 'L': ('The referee... I do not want to speak about the referee.',), 'D': ('We were superior, the result does not show it.',)},
}


def _voice(name, r, default_bank):
    try:
        import ml_realism as M
        n = ' ' + M._norm(name) + ' '
    except Exception:
        n = ' ' + (name or '').lower() + ' '
    for k, bank in PERSONA.items():
        if ' ' + k + ' ' in n:
            return _pick(r, *bank)
    return _pick(r, *default_bank)


def _boss_voice(boss, res, r, default_bank):
    v = BOSS_VOICE.get(boss)
    if v and v.get(res):
        return _pick(r, *v[res])
    return _pick(r, *default_bank)


def _minutes(st, m, n_h, n_a):
    r = _rng('cupmin', st['cup'], st['seed'], m['id'])
    total = n_h + n_a
    mins = sorted(r.sample(range(3, 91), total)) if total <= 80 else list(range(total))
    sides = ['h'] * n_h + ['a'] * n_a
    r.shuffle(sides)
    return list(zip(mins, sides))


def _story(st, m):
    """How the match went: goal-by-goal timeline and the shape of the game."""
    cup = st['cup']
    sh = st['sheets'].get(m['id'], {'h': [], 'a': []})
    tl = _minutes(st, m, len(sh['h']), len(sh['a']))
    it = {'h': iter(sh['h']), 'a': iter(sh['a'])}
    goals, sh_, sa_, lead_changes, led = [], 0, 0, 0, None
    for mn, side in tl:
        sc, ast = next(it[side])
        if side == 'h':
            sh_ += 1
        else:
            sa_ += 1
        now = 'h' if sh_ > sa_ else 'a' if sa_ > sh_ else None
        if now and led and now != led:
            lead_changes += 1
        led = now or led
        goals.append({'min': mn, 'side': side, 'team': m[side], 'pid': sc, 'name': _name(sc), 'assist': _name(ast) if ast else None})
    return goals, lead_changes


def _cut(q, n=62):
    first = q.split('. ')[0].split(' - ')[0].rstrip('.!?')
    if len(first) <= n:
        return first
    return first[:n].rsplit(' ', 1)[0] + '…'


def _goal_line(g):
    how = ('after a one-two with %s' % g['assist'], 'from %s\'s cross' % g['assist'], 'tapping in %s\'s cut-back' % g['assist'],
           'on the end of a through ball from %s' % g['assist']) if g['assist'] else ('with a curling effort from the edge of the box', 'from the penalty spot',
           'with a header at the near post', 'after a solo run past two defenders', 'from a rebound')
    return '%s (%d\') %s' % (g['name'], g['min'], how[(g['min'] + len(g['name'])) % len(how)])


def _match_news(st, m, label, sort_key, ko=None, focus=False):
    """Stories about one match. focus=True for our club's matches and the matchday's headline match."""
    cup = st['cup']
    r = _rng('cupnews', cup, st['seed'], m['id'])
    nm = lambda t: team_row(cup, t)[1]
    hg = m['hg'] + ((m.get('et') or [0, 0])[0])
    ag = m['ag'] + ((m.get('et') or [0, 0])[1])
    goals, changes = _story(st, m)
    items = []
    win, lose = (m['h'], m['a']) if hg > ag else (m['a'], m['h']) if ag > hg else (None, None)
    gap = _rating(cup, m['h']) - _rating(cup, m['a'])
    rivals = frozenset((m['h'], m['a'])) in RIVALS
    late = [g for g in goals if g['min'] >= 85]
    if focus or rivals or changes or late or (win and ((win == m['a'] and gap > 0.35) or (win == m['h'] and gap < -0.35))):
        if not goals:
            shape = 'A cagey, tactical night: neither keeper was beaten and both coaches seemed content with a point.'
        elif changes:
            shape = ('A breathless match in which the lead changed hands.' if changes == 1 else 'A breathless match: the lead changed hands %d times.' % changes)
        elif late and win and late[-1]['team'] == win:
            shape = 'Settled at the death: %s struck in the %d\' to break hearts.' % (late[-1]['name'], late[-1]['min'])
        elif win and goals[0]['team'] != win:
            shape = '%s came from behind after %s had opened the scoring.' % (nm(win), nm(goals[0]['team']))
        elif win and abs(hg - ag) >= 3:
            shape = '%s were in control from the first whistle and never let the tempo drop.' % nm(win)
        else:
            shape = 'Tight in midfield, decided by the finer details in both boxes.'
        lines = '; '.join(_goal_line(g) for g in goals[:5])
        nk = lambda t: _nick(cup, t)
        top_sc = max(goals, key=lambda g: sum(1 for x in goals if x['pid'] == g['pid']))['name'] if goals else ''
        wsc = [g for g in goals if g['team'] == win]
        key = ('late' if late and win and late[-1]['team'] == win else 'comeback' if win and goals and goals[0]['team'] != win else
               'goalless' if not win and not goals else 'draw' if not win else
               'upset' if (win == m['a'] and gap > 0.35) or (win == m['h'] and gap < -0.35) else 'thrash' if abs(hg - ag) >= 3 else 'win')
        title = _hl(r, key, w=nk(win) if win else '', l=nk(lose) if lose else '', h=nk(m['h']), a=nk(m['a']),
                    s='%d-%d' % (max(hg, ag), min(hg, ag)), m=(late[-1]['min'] if late else 90),
                    p=late[-1]['name'] if key == 'late' else (wsc[-1] if wsc else {'name': top_sc})['name'] if goals else '')
        items.append({'k': sort_key + 0.2, 'tag': 'Match report', 'tone': 'blue', 'team': win or m['h'], 'when': label, 'h': title,
                      'b': shape + (' Goals: ' + lines + '.' if lines else ''), 'src': 'Matchday Wire'})
    # the scorer speaks
    if goals and (focus or rivals):
        tally = {}
        for g in goals:
            tally.setdefault(g['pid'], []).append(g)
        pid, gs = max(tally.items(), key=lambda kv: (len(kv[1]), kv[1][-1]['team'] == win))
        q = (_pick(r, *HAT_Q) if len(gs) >= 3 and r.random() < 0.5 else _voice(gs[0]['name'], r, HAT_Q if len(gs) >= 3 else SCORER_Q)).replace('{a}', gs[0]['assist'] or 'my teammates')
        items.append({'k': sort_key + 0.35, 'tag': 'Hat-trick' if len(gs) >= 3 else 'Interview', 'tone': 'gold', 'team': gs[0]['team'], 'pid': pid, 'when': label,
                      'h': '%s: "%s"' % (gs[0]['name'], _cut(q)), 'q': q, 'by': gs[0]['name'],
                      'b': '', 'src': 'Mixed zone'})
    me = st['team']
    if me in (m['h'], m['a']):
        opp = m['a'] if m['h'] == me else m['h']
        gf, ga = (hg, ag) if m['h'] == me else (ag, hg)
        res = 'W' if gf > ga else 'L' if gf < ga else 'D'
        q = _boss_voice(_boss(me), res, r, WIN_Q if res == 'W' else LOSS_Q if res == 'L' else DRAW_Q)
        items.append({'k': sort_key + 0.6, 'tag': 'Press conference', 'tone': 'green' if res == 'W' else 'red' if res == 'L' else 'blue', 'team': me, 'when': label,
                      'h': '%s: "%s"' % (_boss(me) if MANAGERS.get(me) else _nick(cup, me) + ' boss', _cut(q, 66)),
                      'q': q, 'by': (_boss(me) if MANAGERS.get(me) else _nick(cup, me) + ' head coach') + ' after %d-%d vs %s' % (gf, ga, nm(opp)), 'b': '', 'src': 'Press Room'})
        if MANAGERS.get(opp):
            ores = {'W': 'L', 'L': 'W', 'D': 'D'}[res]
            oq = _boss_voice(_boss(opp), ores, _rng('oppq', st['seed'], m['id']), WIN_Q if ores == 'W' else LOSS_Q if ores == 'L' else DRAW_Q)
            items.append({'k': sort_key + 0.58, 'tag': 'Reaction', 'tone': 'green' if ores == 'W' else 'red' if ores == 'L' else 'blue', 'team': opp, 'when': label,
                          'h': '%s: "%s"' % (_boss(opp), _cut(oq, 66)), 'q': oq, 'by': _boss(opp), 'b': '', 'src': 'Press Room'})
        if res == 'L' and r.random() < 0.55:
            capt = next((p['name'] for p in roster(cup, me)[0] if GRP.get(p['pos']) == 'D'), None)
            if capt:
                items.append({'k': sort_key + 0.55, 'tag': 'Dressing room', 'tone': 'red', 'team': me, 'when': label,
                              'h': _hl(r, 'loser', p=capt), 'q': _pick(r, *LOSER_Q), 'by': capt, 'b': '', 'src': 'The Touchline'})
    # drama
    if rivals and r.random() < 0.8:
        a, b = (win, lose) if win else (m['h'], m['a'])
        r = _rng('wow', st['seed'], m['id'], b)
        items.append({'k': sort_key + 0.45, 'tag': 'War of words', 'tone': 'red', 'team': b, 'when': label,
                      'h': _hl(r, 'war', b1=_boss(b) if MANAGERS.get(b) else _nick(cup, b) + ' coach', b2=_boss(a) if MANAGERS.get(a) else _nick(cup, a)),
                      'q': _pick(r, 'They talk a lot before these games. We prefer to answer on the pitch - and the tie is not over.',
                                 'Some people should look at their own team before giving lessons to everybody else.',
                                 'They had one good half. If they think it is over, they do not know my players.',
                                 'I will not comment on what was said in the tunnel. What happens there stays there.',
                                 'Respect? I respect them. But I do not like how they celebrated in front of our bench.',
                                 'Every rivalry needs a bit of fire. I am not here to make friends.'),
                      'by': _boss(b) if MANAGERS.get(b) else nm(b) + ' coach', 'b': '', 'src': 'The Touchline'})
    if win and abs(hg - ag) == 1 and r.random() < 0.3:
        items.append({'k': sort_key + 0.4, 'tag': 'Controversy', 'tone': 'red', 'team': lose, 'when': label,
                      'h': _hl(r, 'ref', b=_boss(lose) if MANAGERS.get(lose) else _nick(cup, lose) + ' boss'),
                      'q': _pick(r, 'Everybody saw it. That was never a penalty and VAR stayed silent.', 'One decision changed the whole match. I will not say more or I get banned.',
                                 'We asked for a clear handball. Nothing. In this competition you need the small decisions.'),
                      'by': _boss(lose) if MANAGERS.get(lose) else nm(lose) + ' coach', 'b': '', 'src': 'Pundit Panel'})
    if win and r.random() < 0.12:
        star = next((p for p in roster(cup, win)[0] if GRP.get(p['pos']) == 'F' and not any(g['pid'] == p['pid'] for g in goals)), None)
        if star:
            items.append({'k': sort_key + 0.3, 'tag': 'Drama', 'tone': 'red', 'team': win, 'pid': star['pid'], 'when': label,
                          'h': _hl(r, 'sulk', p=star['name']), 'b': '',
                          'q': _pick(r, 'He wants to play every minute. That is normal for a champion. We will talk tomorrow.',
                                     'I made the decision for the team. Nobody is bigger than the club.'),
                          'by': _boss(win), 'src': 'Fan Zone'})
    if ko and ko.get('winner') and m is ko['legs'][-1]:
        w, l = ko['winner'], ko['b'] if ko['winner'] == ko['a'] else ko['a']
        how = ' on penalties' if ko.get('pens') else ' after extra time' if ko.get('et') else ''
        agg = ko['agg']
        if ko['stage'] == 'final':
            items.append({'k': sort_key + 0.9, 'tag': 'Champions', 'tone': 'gold', 'team': w, 'when': label,
                          'h': _hl(r, 'champions', w=_nick(cup, w), c=CUPS[cup]['short']),
                          'b': '%s beat %s%s at %s. Confetti, tears and a captain lifting the trophy into the night sky.' % (nm(w), nm(l), how, CUPS[cup]['final_venue']),
                          'q': _pick(r, 'This is for every person who believed in us when nobody else did.', 'I have dreamed about this night since I was a kid.'),
                          'by': _boss(w), 'src': 'Cup Desk'})
        else:
            items.append({'k': sort_key + 0.5, 'tag': 'Through', 'tone': 'green', 'team': w, 'when': label,
                          'h': _hl(r, 'through', w=_nick(cup, w), l=_nick(cup, l)),
                          'b': '%s go through%s%s. The journey ends here for %s.' % (nm(w), (' %d-%d on aggregate' % (max(agg), min(agg))) if len(ko['legs']) > 1 else '', how, nm(l)),
                          'src': 'Cup Desk'})
    return items


def _droughts(st, upto_round):
    """Stars of a club who have gone the last three of their club's matches without a goal."""
    cup = st['cup']
    out = []
    names = {t: [p for p in roster(cup, t)[0] if ((_star(cup, p['name']) or (0, 0))[0] or 0) >= 0.2] for t in (x[0] for x in CUPS[cup]['teams'])}
    for t, stars in names.items():
        ms = [m for rd in st['league'][:upto_round] for m in rd if t in (m['h'], m['a'])][-3:]
        if len(ms) < 3:
            continue
        for p in stars:
            if not any(sc == p['pid'] for m in ms for side in ('h', 'a') for sc, _ in st['sheets'].get(m['id'], {}).get(side, [])):
                out.append((t, p))
    return out


def _potm(st, matches):
    best = None
    for m in matches:
        sh = st['sheets'].get(m['id'])
        if not sh:
            continue
        for side, team in (('h', m['h']), ('a', m['a'])):
            tally = {}
            for sc, ast in sh[side]:
                tally.setdefault(sc, [0, 0])[0] += 1
                if ast:
                    tally.setdefault(ast, [0, 0])[1] += 1
            for pid, (g, a) in tally.items():
                score = g * 3 + a * 2
                if best is None or score > best[0]:
                    best = (score, pid, team, g, a, m)
    return best[1:] if best and best[0] >= 5 else None


def news(st):
    if not st:
        return []
    cup = st['cup']
    nm = lambda t: team_row(cup, t)[1]
    me = st['team']
    items = []
    drought_seen = set()
    r0 = _rng('cupnews0', cup, st['seed'])
    fav = sorted((t[0] for t in CUPS[cup]['teams']), key=lambda t: -_rating(cup, t))[:3]
    items.append({'k': 0, 'tag': 'Preview', 'tone': 'blue', 'team': fav[0], 'when': 'Draw',
                  'h': _hl(r0, 'preview', t=_nick(cup, fav[0])),
                  'b': 'The draw is done. %s head the betting, ahead of %s and %s. %s' % (nm(fav[0]), nm(fav[1]), nm(fav[2]),
                       'Our tactics desk says %s have the squad to go all the way.' % nm(me) if me in fav else 'Few expect %s to challenge the elite - can they prove the doubters wrong?' % nm(me)),
                  'src': 'Press Room'})
    for i, rd in enumerate(st['league']):
        if rd[0]['hg'] is None:
            break
        label = 'Matchday %d' % (i + 1)
        head = max(rd, key=lambda m: (frozenset((m['h'], m['a'])) in RIVALS, m['hg'] + m['ag']))
        for m in rd:
            items += _match_news(st, m, label, 10 + i, focus=(st['team'] in (m['h'], m['a']) or m is head))
        for t, p in _droughts(st, i + 1):
            key = (t, p['pid'])
            if key in drought_seen:
                continue
            drought_seen.add(key)
            items.append({'k': 10 + i + 0.15, 'tag': 'Under pressure', 'tone': 'red', 'team': t, 'pid': p['pid'], 'when': label,
                          'h': _hl(_rng('dh', st['seed'], p['pid'], i), 'drought', p=p['name'], b=_boss(t)),
                          'q': _pick(_rng('drought', st['seed'], p['pid']), 'He is the best in the world at what he does. The goals will come, I have zero doubts.',
                                     'Strikers go through moments like this. My job is to protect him, and I will.',
                                     'Ask me again in two weeks. He will answer you on the pitch.'),
                          'by': _boss(t), 'b': '', 'src': 'Pundit Panel'})
        potm = _potm(st, rd)
        if potm:
            pid, team, g, a, m = potm
            hg, ag = m['hg'], m['ag']
            items.append({'k': 10 + i + 0.4, 'tag': 'Player of the matchday', 'tone': 'gold', 'team': team, 'pid': pid, 'when': label,
                          'h': _hl(_rng('ph', st['seed'], i), 'potm', p=_name(pid), when=label.lower()),
                          'b': '%s%s in %s %d-%d %s. %s' % ('%d goal%s' % (g, 's' if g > 1 else '') if g else '', (' and ' if g else '') + '%d assist%s' % (a, 's' if a > 1 else '') if a else '',
                                                          nm(m['h']), hg, ag, nm(m['a']), _pick(_rng('potm', st['seed'], m['id']), 'Our panel gave him a 9.1.', 'Nobody touched the ball more in the final third.', 'A complete performance.')),
                          'src': 'Data Room'})
        tb = table(dict(st, league=st['league'][:i + 1]))
        lead = tb[0]
        items.append({'k': 10 + i + 0.1, 'tag': 'Table', 'tone': 'blue', 'team': lead['team'], 'when': label,
                      'h': _hl(_rng('th', st['seed'], i), 'table', t=_nick(cup, lead['team']), when=label.lower()),
                      'b': '%s have %d points and a goal difference of %+d. %s' % (nm(lead['team']), lead['pts'], lead['gd'],
                           'One more matchday to go - every goal counts now.' if i == len(st['league']) - 2 else 'Plenty still to play for.'), 'src': 'Data Room'})
    if all(m['hg'] is not None for rd in st['league'] for m in rd):
        tb = table(st)
        cut = CUPS[cup]['direct']
        top = [nm(x['team']) for x in tb[:cut]]
        items.append({'k': 30, 'tag': 'Qualified', 'tone': 'green', 'team': tb[0]['team'], 'when': 'League phase',
                      'h': _pick(_rng('lp', st['seed']), 'The dust settles: %s top the league phase' % top[0], 'Group of death? %s finish on top' % top[0], 'Pole position for %s heading into the knockouts' % top[0]),
                      'b': ('%s go straight into the quarter-finals; the rest fight it out in the play-off.' % ', '.join(top)) if CUPS[cup]['po'] else
                           ('The top 16 advance to the round of 16. %s miss out.' % ', '.join(nm(x['team']) for x in tb[16:])),
                      'src': 'Cup Desk'})
        mine = next(x for x in tb if x['team'] == me)
        items.append({'k': 30.1, 'tag': 'Your club', 'tone': 'gold' if mine['pos'] <= cut else 'red', 'team': me, 'when': 'League phase',
                      'h': ('Boardroom beaming: %s chiefs delighted' % _nick(cup, me) if mine['pos'] <= max(2, cut // 4) else 'Mission accomplished for %s — for now' % _nick(cup, me) if mine['pos'] <= cut else 'Alarm bells at %s: the board wants answers' % _nick(cup, me)),
                      'b': '%s finished %d%s with %d points.' % (nm(me), mine['pos'], {1: 'st', 2: 'nd', 3: 'rd'}.get(mine['pos'] if mine['pos'] < 20 else 0, 'th'), mine['pts']),
                      'src': 'Press Room'})
    order = ['po', 'r16', 'qf', 'sf', 'final']
    for t in st['ko']:
        base = 40 + order.index(t['stage']) * 10
        for j, l in enumerate(t['legs']):
            if l['hg'] is None:
                continue
            label = KO_LABEL[t['stage']] + ((' · leg %d' % (j + 1)) if len(t['legs']) > 1 else '')
            items += _match_news(st, l, label, base + j * 2, ko=t, focus=True)
    # top scorer race
    g_tab, a_tab, goals, assists, team_of = stats(st)
    if g_tab:
        g = g_tab[0]
        played = sum(1 for rd in st['league'] for m in rd if m['hg'] is not None) + sum(1 for t in st['ko'] for l in t['legs'] if l['hg'] is not None)
        items.append({'k': 95 if st['stage'] == 'done' else 9 + played / 1000.0 + len(st['league']) + len([t for t in st['ko'] if t['winner']]) * 3,
                      'tag': 'Golden Boot' if st['stage'] == 'done' else 'Scoring race', 'tone': 'gold', 'team': g['team'], 'pid': g['pid'], 'when': 'Stats',
                      'h': _hl(_rng('rh', st['seed'], g['n'], g['pid']), 'boot' if st['stage'] == 'done' else 'race', p=g['name'], n='%d goal%s' % (g['n'], '' if g['n'] == 1 else 's')),
                      'b': '%s%s' % ('%s (%d) and %s (%d) are chasing. ' % (g_tab[1]['name'], g_tab[1]['n'], g_tab[2]['name'], g_tab[2]['n']) if len(g_tab) > 2 else '',
                                     ('Top assist provider: %s with %d.' % (a_tab[0]['name'], a_tab[0]['n'])) if a_tab else ''),
                      'src': 'Data Room'})
    if st['stage'] == 'done':
        mv = mvp(st)
        if mv:
            items.append({'k': 96, 'tag': 'MVP', 'tone': 'gold', 'team': mv[0]['team'], 'pid': mv[0]['pid'], 'when': 'Awards',
                          'h': _hl(r0, 'mvp', p=mv[0]['name']),
                          'b': '%d goals and %d assists. %s' % (mv[0]['goals'], mv[0]['assists'], 'Runner-up: %s, third: %s.' % (mv[1]['name'], mv[2]['name']) if len(mv) > 2 else ''),
                          'src': 'Cup Desk'})
    else:
        nxt = None
        for t in st['ko']:
            for l in t['legs']:
                if l['hg'] is None and me in (l['h'], l['a']):
                    nxt = (t, l)
                    break
            if nxt:
                break
        if nxt:
            t, l = nxt
            opp = l['a'] if l['h'] == me else l['h']
            items.append({'k': 99, 'tag': 'Next up', 'tone': 'blue', 'team': opp, 'when': KO_LABEL[t['stage']],
                          'h': _hl(_rng('nx', st['seed'], l['id']), 'next', h=_nick(cup, l['h']), a=_nick(cup, l['a'])),
                          'b': 'Our analysts rate %s as %s.' % (nm(me), 'favourites' if _rating(cup, me) > _rating(cup, opp) + 0.08 else 'underdogs' if _rating(cup, me) < _rating(cup, opp) - 0.08 else 'evenly matched with their opponents'),
                          'src': 'Tactics Lab'})
    items.sort(key=lambda x: -x['k'])
    for x in items:
        x.pop('k', None)
    return items[:60]


def _short(name):
    parts = (name or '').split()
    if len(parts) < 2 or parts[-1].rstrip('.') in ('Jr', 'Júnior', 'Junior') or parts[0][-1] == '.':
        return name
    return parts[0][0] + '. ' + ' '.join(parts[1:])


def view(st):
    if not st:
        return None
    cup = CUPS[st['cup']]
    g_tab, a_tab, *_ = stats(st)
    def _with_sc(m):
        sh = st['sheets'].get(m['id'])
        if not sh:
            return m
        out = {}
        for side in ('h', 'a'):
            cnt, order = {}, []
            for sc, _ in sh[side]:
                if sc not in cnt:
                    order.append(sc)
                cnt[sc] = cnt.get(sc, 0) + 1
            out[side] = [[_short(_name(pid)), cnt[pid]] for pid in order]
        return dict(m, sc=out)
    rounds = [{'round': i + 1, 'matches': [_with_sc(m) for m in rd]} for i, rd in enumerate(st['league'])]
    st = dict(st, ko=[dict(t, legs=[_with_sc(l) for l in t['legs']]) for t in st['ko']])
    ko = {}
    for t in st['ko']:
        ko.setdefault(t['stage'], []).append(t)
    played_league = sum(1 for rd in st['league'] if rd[0]['hg'] is not None)
    return {'cup': cup['id'], 'name': cup['name'], 'short': cup['short'], 'team': st['team'], 'stage': st['stage'],
            'stage_name': STAGE_NAME.get(st['stage'], st['stage']), 'champion': st['champion'], 'final_venue': cup['final_venue'],
            'teams': {str(t[0]): team_doc(cup['id'], t[0]) for t in cup['teams']}, 'table': table(st), 'rounds': rounds,
            'played_rounds': played_league, 'ko': [{'stage': k, 'name': STAGE_NAME[k], 'ties': v} for k, v in ko.items()],
            'scorers': g_tab, 'assists': a_tab, 'mvp': mvp(st), 'direct': cup['direct'], 'po': cup['po'], 'news': news(st),
            'squads': {str(t[0]): [dict(r, xi=bool(r.get('xi'))) for r in sum(roster(cup['id'], t[0]), [])] for t in cup['teams']}}


def match(conn, cup, mid):
    st = load(conn, cup)
    if not st:
        return {'error': 'not-started'}
    m = None
    for rd in st['league']:
        for x in rd:
            if x['id'] == mid:
                m = x
    for t in st['ko']:
        for x in t['legs']:
            if x['id'] == mid:
                m = x
    if not m or m['hg'] is None:
        return {'error': 'no-match'}
    sh = st['sheets'].get(mid, {'h': [], 'a': []})
    hg = m['hg'] + ((m.get('et') or [0, 0])[0])
    ag = m['ag'] + ((m.get('et') or [0, 0])[1])
    goals = [{'team': m['h'], 'name': _name(sc), 'assist': _name(ast) if ast else None} for sc, ast in sh['h']] + \
            [{'team': m['a'], 'name': _name(sc), 'assist': _name(ast) if ast else None} for sc, ast in sh['a']]
    out = {'id': mid, 'cup': CUPS[cup]['name'], 'home': {'team': m['h'], 'goals': hg, 'ratings': ratings(cup, st['seed'], mid, m['h'], hg, ag, sh['h'])},
           'away': {'team': m['a'], 'goals': ag, 'ratings': ratings(cup, st['seed'], mid, m['a'], ag, hg, sh['a'])}, 'goals': goals, 'et': m.get('et'),
           'teams': {str(t[0]): team_doc(cup, t[0]) for t in CUPS[cup]['teams']}}
    best = max(out['home']['ratings'] + out['away']['ratings'], key=lambda r: r['r'], default=None)
    if best:
        out['motm'] = best
    return out


def api(conn, method, path, body):
    parts = [p for p in path.split('/') if p][3:]        # after api/rc29/cups
    if not parts:
        out = []
        for cid, c in CUPS.items():
            st = load(conn, cid)
            out.append({'id': cid, 'name': c['name'], 'short': c['short'], 'started': bool(st), 'stage': st and st['stage'],
                        'team': st and st['team'], 'champion': st and st['champion'],
                        'teams': [dict(team_doc(cid, t[0]), rating=round((t[5] / t[6]) * 50)) for t in c['teams']]})
        return {'cups': out}
    cup = parts[0]
    if cup not in CUPS:
        return {'error': 'unknown-cup'}
    act = parts[1] if len(parts) > 1 else ''
    if method == 'POST' and act == 'start':
        try:
            team = int(json.loads(body or '{}').get('team'))
        except Exception:
            return {'error': 'bad-team'}
        return start(conn, cup, team)
    if method == 'POST' and act == 'next':
        return step(conn, cup)
    if method == 'POST' and act == 'finish':
        return finish(conn, cup)
    if method == 'POST' and act == 'reset':
        return reset(conn, cup)
    if act == 'match' and len(parts) > 2:
        return match(conn, cup, parts[2])
    st = load(conn, cup)
    return view(st) if st else {'started': False, 'cup': cup}
