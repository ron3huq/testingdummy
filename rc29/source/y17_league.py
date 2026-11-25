"""RC29.17: Y17 Champions League - a stand-alone league of the twelve 2017 super-clubs (RC26 Y17 squads + 2013-19 squad players).

Completely separate from the Master League, My League and the career: its own files (work/tools/rc29_y17/), its own save slots.
Format: triple round robin, 12 clubs, 33 matchdays (every pair meets three times; home games 16/17 each).
Every match: Poisson goals from club strength (home edge, season drift, momentum, a dark horse), scorers and assists from the
squad by position, star share, hot/cold streak and a breakout player of the season. Golden Boot, Playmaker, Golden Glove,
Ballon d'Or (Y17), Team of the Season. Newsroom: commentary-style reports, interviews by personality, mind games before
big matches, form stories, title race and the Messi-Ronaldo duel.

API (no Master League profile needed):
  GET  /api/rc29/y17                 state (null career -> {career: null, teams})
  POST /api/rc29/y17/new   {team}    new career (season 1)
  POST /api/rc29/y17/next  {hg, ag}  play the next matchday (optional: your own result, e.g. played in My League)
  POST /api/rc29/y17/sim   {}        play to the end of the season
  POST /api/rc29/y17/season          start the next season (history kept)
  GET  /api/rc29/y17/match/<r>/<i>   one match
  GET  /api/rc29/y17/saves           slots;  POST /api/rc29/y17/saves/<save|load|delete> {slot}
"""
import json, math, random, time, zlib
from pathlib import Path

import ml_cups as C

ROUNDS = 33
LINK_CID = 518          # My League's 'Y17 Champion League' (RC26): the real matches are played there
SLOTS = ('1', '2', '3', '4', '5')
POS = C.POS
GRP = C.GRP
SCORE_POS = {'CF': 10.0, 'SS': 7.5, 'LWF': 6.5, 'RWF': 6.5, 'AMF': 4.2, 'LMF': 3.0, 'RMF': 3.0, 'CMF': 1.6, 'DMF': 0.7,
             'CB': 0.75, 'LB': 0.45, 'RB': 0.45, 'GK': 0.0}
ASSIST_POS = {'CF': 3.5, 'SS': 4.6, 'LWF': 5.2, 'RWF': 5.2, 'AMF': 6.4, 'LMF': 4.6, 'RMF': 4.6, 'CMF': 3.8, 'DMF': 1.6,
              'CB': 0.5, 'LB': 2.6, 'RB': 2.6, 'GK': 0.05}

# 2013-19 squad players (cards that exist in the game data), one club each: team -> [(card, name, position)]
ADD = {
    1220: [(105566001282344, 'Achraf Hakimi', 'RB'), (103408, 'Lucas Vázquez', 'RWF'), (104710, 'Dani Ceballos', 'CMF'),
           (103008, 'Marcos Llorente', 'DMF'), (None, 'Theo Hernández', 'LB'), (17592186045268, 'Iker Casillas', 'GK'), (None, 'Jesús Vallejo', 'CB')],
    1222: [(45089, 'Lucas Digne', 'LB'), (None, 'Yerry Mina', 'CB'), (16878336, 'Malcom', 'RWF'), (None, 'Gerard Deulofeu', 'LWF'),
           (None, 'Munir El Haddadi', 'RWF'), (None, 'Sandro Ramírez', 'CF')],
    5317: [(43040, 'Mario Götze', 'AMF'), (None, 'Leon Goretzka', 'CMF'), (None, 'Serge Gnabry', 'RWF'), (None, 'Renato Sanches', 'CMF')],
    2365: [(None, 'Moise Kean', 'CF'), (None, 'Leonardo Spinazzola', 'LB'), (None, 'Marko Pjaca', 'LWF'), (None, 'Tomás Rincón', 'DMF')],
    1219: [(100967, 'Thomas Lemar', 'LWF'), (None, 'Gelson Martins', 'RWF')],
    1986: [(109010, 'Kevin Trapp', 'GK'), (108984, 'Christopher Nkunku', 'CMF'), (None, 'Gonçalo Guedes', 'LWF'), (None, 'Yuri Berchiche', 'LB'), (None, 'Thilo Kehrer', 'CB')],
    131: [(104226, 'Bernardo Silva', 'RWF'), (None, 'Riyad Mahrez', 'RWF'), (None, 'Aymeric Laporte', 'CB'), (88046292727298, 'Yaya Touré', 'CMF'),
          (None, 'Jesús Navas', 'RWF'), (None, 'Kelechi Iheanacho', 'CF'), (70375723534347, 'Joe Hart', 'GK'), (None, 'Brahim Díaz', 'AMF')],
    1987: [(47238, 'Nathaniel Clyne', 'RB'), (58843, 'Alberto Moreno', 'LB'), (None, 'Dominic Solanke', 'CF'), (None, 'Christian Benteke', 'CF')],
    1221: [(None, 'Olivier Giroud', 'CF'), (None, 'Jorginho', 'DMF'), (None, 'Andreas Christensen', 'CB'), (47242, 'Kepa Arrizabalaga', 'GK'),
           (None, 'Davide Zappacosta', 'RB'), (None, 'Ross Barkley', 'AMF')],
    1985: [(104612, 'Davinson Sánchez', 'CB'), (None, 'Kyle Walker-Peters', 'RB'), (None, 'Juan Foyth', 'CB'), (None, 'Paulo Gazzaniga', 'GK'),
           (None, 'Clinton N’Jie', 'RWF'), (None, 'Oliver Skipp', 'CMF')],
    2621: [(102719, 'Patrik Schick', 'CF'), (None, 'Nicolò Zaniolo', 'AMF'), (None, 'Bryan Cristante', 'DMF'), (None, 'Justin Kluivert', 'LWF'),
           (None, 'Robin Olsen', 'GK'), (None, 'Steven Nzonzi', 'DMF')],
    132: [(None, 'Romelu Lukaku', 'CF'), (None, 'Luke Shaw', 'LB'), (109123, 'Victor Lindelöf', 'CB'), (None, 'Alexis Sánchez', 'LWF'),
          (None, 'Marcos Rojo', 'CB'), (None, 'Radamel Falcao', 'CF')],
}

# (name keys) -> goal share, assist share, prestige (Ballon d'Or voters' memory), free kicks / penalties
STARS = [
    (('lionel messi',), 0.52, 0.24, 9, 'fk'), (('cristiano ronaldo',), 0.42, 0.11, 9, 'fk'),
    (('neymar',), 0.17, 0.21, 5, 'fk'), (('luis suarez',), 0.24, 0.13, 4, ''), (('robert lewandowski',), 0.36, 0.07, 5, ''),
    (('harry kane',), 0.40, 0.06, 4, ''), (('edinson cavani',), 0.34, 0.05, 3, ''), (('zlatan ibrahimovic',), 0.30, 0.10, 4, 'fk'),
    (('kylian mbappe',), 0.18, 0.10, 3, ''), (('sergio aguero',), 0.35, 0.07, 4, ''), (('mohamed salah',), 0.33, 0.11, 4, ''),
    (('roberto firmino',), 0.15, 0.13, 2, ''), (('sadio mane',), 0.18, 0.08, 2, ''), (('antoine griezmann',), 0.33, 0.12, 5, 'fk'),
    (('paulo dybala',), 0.27, 0.12, 3, 'fk'), (('karim benzema',), 0.14, 0.12, 3, ''), (('gareth bale',), 0.14, 0.08, 3, 'fk'),
    (('eden hazard',), 0.22, 0.15, 4, ''), (('diego costa',), 0.30, 0.05, 2, ''), (('kevin de bruyne',), 0.10, 0.27, 4, 'fk'),
    (('edin dzeko',), 0.34, 0.07, 2, ''), (('francesco totti',), 0.10, 0.10, 3, 'fk'), (('thomas muller',), 0.14, 0.15, 3, ''),
    (('arjen robben', 'franck ribery'), 0.10, 0.12, 2, ''), (('wayne rooney',), 0.20, 0.10, 3, 'fk'), (('anthony martial',), 0.18, 0.07, 1, ''),
    (('romelu lukaku',), 0.24, 0.05, 2, ''), (('luka modric',), 0.03, 0.10, 4, ''), (('toni kroos',), 0.04, 0.12, 3, 'fk'),
    (('andres iniesta',), 0.04, 0.12, 4, ''), (('christian eriksen',), 0.10, 0.18, 2, 'fk'), (('philippe coutinho',), 0.12, 0.10, 2, 'fk'),
    (('james rodriguez',), 0.10, 0.14, 2, 'fk'), (('angel di maria',), 0.10, 0.18, 3, ''), (('son heung-min',), 0.18, 0.08, 2, ''),
    (('raheem sterling',), 0.20, 0.10, 2, ''), (('leroy sane',), 0.12, 0.12, 1, ''), (('david silva',), 0.06, 0.16, 3, ''),
    (('alvaro morata',), 0.18, 0.05, 1, ''), (('gonzalo higuain',), 0.30, 0.05, 2, ''), (('douglas costa',), 0.10, 0.14, 1, ''),
    (('marco verratti',), 0.01, 0.07, 2, ''), (('sergio ramos',), 0.05, 0.02, 4, ''), (('marcelo',), 0.03, 0.08, 3, ''),
    (('n golo kante',), 0.02, 0.03, 4, ''), (('willian',), 0.08, 0.10, 1, 'fk'), (('pedro',), 0.10, 0.06, 1, ''),
    (('stephan el shaarawy',), 0.12, 0.06, 1, ''), (('dele alli',), 0.14, 0.08, 2, ''), (('marcus rashford',), 0.12, 0.06, 1, ''),
]
PRESTIGE_GK = {'gianluigi buffon': 4, 'manuel neuer': 4, 'keylor navas': 2, 'david de gea': 3, 'jan oblak': 2, 'marc ter stegen': 2, 'thibaut courtois': 2}

MANAGERS = dict(C.MANAGERS)
NICK = {1220: 'Real Madrid', 1222: 'Barça', 5317: 'Bayern', 2365: 'Juve', 1219: 'Atlético', 1986: 'PSG', 131: 'City', 1987: 'Liverpool',
        1221: 'Chelsea', 1985: 'Spurs', 2621: 'Roma', 132: 'United'}
STADIUM = {1220: 'the Bernabéu', 1222: 'the Camp Nou', 5317: 'the Allianz Arena', 2365: 'the Allianz Stadium', 1219: 'the Wanda Metropolitano',
           1986: 'the Parc des Princes', 131: 'the Etihad', 1987: 'Anfield', 1221: 'Stamford Bridge', 1985: 'White Hart Lane',
           2621: 'the Stadio Olimpico', 132: 'Old Trafford'}
RIVALS = {frozenset(x): n for x, n in (((1220, 1222), 'El Clásico'), ((131, 132), 'the Manchester derby'), ((1220, 1219), 'the Madrid derby'),
                                         ((1987, 132), 'the North-West derby'), ((1221, 1985), 'the London derby'), ((2365, 2621), 'Juve v Roma'),
                                         ((1987, 131), 'Liverpool v City'), ((1221, 132), 'Mourinho\'s return'), ((1222, 1986), 'the Remontada rematch'),
                                         ((5317, 1220), 'Bayern v Real'), ((1222, 2365), 'the Cardiff ghosts'), ((1222, 5317), 'Pep\'s old flames'))}

# 2016-18 level (attack, defence): Barça and Real a class apart, Bayern / Juventus / Liverpool right behind
STR = {1222: (2.95, 0.80), 1220: (2.88, 0.82), 5317: (2.45, 0.88), 2365: (2.15, 0.78), 1987: (2.40, 0.94), 1986: (2.25, 1.00),
       131: (2.20, 1.02), 1219: (1.75, 0.84), 1221: (1.85, 1.00), 1985: (1.85, 1.05), 2621: (1.60, 1.10), 132: (1.60, 1.02)}

_c = {}


# ------------------------------------------------------------------ files
def _dir():
    d = C._tools() / 'rc29_y17'
    d.mkdir(parents=True, exist_ok=True)
    return d


def _read(name):
    p = _dir() / (name + '.json')
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def _write(name, obj):
    p = _dir() / (name + '.json')
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    tmp.replace(p)


def _drop(name):
    try:
        (_dir() / (name + '.json')).unlink()
    except Exception:
        pass


# ------------------------------------------------------------------ squads
def _card_for(name):
    if 'idx' not in _c:
        idx = {}
        for pid, v in C._names().items():
            n = v[0] if isinstance(v, list) else v
            if n:
                idx.setdefault(C._fold(n), []).append(pid)
        _c['idx'] = idx
    ids = sorted(_c['idx'].get(C._fold(name), []), key=lambda x: (len(x), x))
    return int(ids[0]) if ids else None


def squad(team):
    key = ('sq', team)
    if key in _c:
        return _c[key]
    xi, bench = C.roster('ucl17', team)
    rows = [dict(p, xi=True) for p in xi] + [dict(p, xi=False) for p in bench]
    seen = {C._fold(p['name']) for p in rows}
    for card, name, pos in ADD.get(team, ()):
        if C._fold(name) in seen:
            continue
        card = card or _card_for(name)
        if not card:
            continue
        rows.append({'pid': int(card), 'name': name, 'pos': pos, 'xi': False})
        seen.add(C._fold(name))
    _c[key] = rows
    return rows


def _owner():
    if 'owner' not in _c:
        own = {}
        for t in C.UCL17:
            for p in squad(t[0]):
                own[p['pid']] = (t[0], p['name'], p['pos'])
        _c['owner'] = own
    return _c['owner']


def _star(name):
    n = ' ' + C._fold(name).replace('-', ' ').replace('’', ' ').replace("'", ' ') + ' '
    for keys, g, a, pr, fk in STARS:
        if any(' ' + k + ' ' in n for k in keys):
            return g, a, pr, fk
    return None


def _team(tid):
    return C.team_row('ucl17', tid)


def _tname(tid):
    t = _team(tid)
    return t[1] if t else str(tid)


def _nick(tid):
    return NICK.get(tid) or _tname(tid)


def _short(name):
    return C._short(name)


def _last(name):
    parts = (name or '').split()
    if not parts:
        return name
    if len(parts) == 1 or parts[-1] in ('Jr', 'Júnior'):
        return parts[0]
    return parts[-1] if len(parts[-1]) > 2 else name


# ------------------------------------------------------------------ randomness
def _rng(*parts):
    return random.Random(zlib.crc32(':'.join(str(p) for p in parts).encode()))


def _poisson(r, lam):
    lam = max(0.05, min(5.5, lam))
    lim, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= r.random()
        if p < lim:
            return k
        k += 1


# ------------------------------------------------------------------ fixtures
def fixtures(seed):
    r = _rng('y17fix', seed)
    teams = [t[0] for t in C.UCL17]
    r.shuffle(teams)

    def cycle(order):
        n = len(order)
        arr = order[:]
        out = []
        for k in range(n - 1):
            rd = []
            for i in range(n // 2):
                a, b = arr[i], arr[n - 1 - i]
                rd.append([a, b] if (k + i) % 2 == 0 else [b, a])
            out.append(rd)
            arr = [arr[0]] + [arr[-1]] + arr[1:-1]
        return out
    c1 = cycle(teams)
    c2 = [[[b, a] for a, b in rd] for rd in c1]
    r.shuffle(c2)
    # keep the same pair out of consecutive rounds at the joint of cycle 1 and 2
    for _ in range(30):
        last = {frozenset(m) for m in c1[-1]}
        if not any(frozenset(m) in last for m in c2[0]):
            break
        r.shuffle(c2)
    t3 = teams[:]
    r.shuffle(t3)
    c3 = cycle(t3)
    r.shuffle(c3)
    homes = {t: 0 for t in teams}
    for rd in c1 + c2:
        for h, a in rd:
            homes[h] += 1
    for rd in c3:
        for m in rd:
            a, b = m
            if homes[a] > homes[b] or (homes[a] == homes[b] and r.random() < 0.5):
                m[0], m[1] = b, a
            homes[m[0]] += 1
    return c1 + c2 + c3


# ------------------------------------------------------------------ season set-up
def _new_season(team, season, history, seed=None):
    seed = seed or random.randrange(1, 10 ** 9)
    r = _rng('y17season', seed)
    drift = {str(t[0]): round(r.gauss(0, 0.035), 3) for t in C.UCL17}
    # a dark horse: one of the weaker six has the season of its life
    weak = sorted(C.UCL17, key=lambda t: STR[t[0]][0] / STR[t[0]][1])[:6]
    horse = r.choice(weak)[0]
    drift[str(horse)] = round(drift[str(horse)] + 0.07, 3)
    # breakout players: squad men nobody talks about who catch fire
    pool = []
    for t in C.UCL17:
        for p in squad(t[0]):
            if _star(p['name']) or p['pos'] not in ('CF', 'SS', 'LWF', 'RWF', 'AMF', 'LMF', 'RMF'):
                continue
            pool.append(p['pid'])
    r.shuffle(pool)
    breakout = pool[:1 + (r.random() < 0.45)]
    fx = fixtures(seed)
    return {'v': 1, 'season': season, 'team': int(team), 'seed': seed, 'round': 0, 'drift': drift, 'horse': horse, 'breakout': breakout,
            'fx': [[{'h': h, 'a': a, 'hg': None, 'ag': None} for h, a in rd] for rd in fx], 'pform': {}, 'news': [], 'history': history or [],
            'awards': None, 'started': int(time.time()), 'saved': int(time.time())}


# ------------------------------------------------------------------ tables & stats
def table(st, upto=None):
    rows = {t[0]: {'team': t[0], 'p': 0, 'w': 0, 'd': 0, 'l': 0, 'gf': 0, 'ga': 0, 'pts': 0, 'form': [], 'cs': 0} for t in C.UCL17}
    for i, rd in enumerate(st['fx']):
        if upto is not None and i >= upto:
            break
        for m in rd:
            if m['hg'] is None:
                continue
            h, a = rows[m['h']], rows[m['a']]
            for x, gf, ga in ((h, m['hg'], m['ag']), (a, m['ag'], m['hg'])):
                x['p'] += 1
                x['gf'] += gf
                x['ga'] += ga
                x['cs'] += ga == 0
                if gf > ga:
                    x['w'] += 1; x['pts'] += 3; x['form'].append('W')
                elif gf < ga:
                    x['l'] += 1; x['form'].append('L')
                else:
                    x['d'] += 1; x['pts'] += 1; x['form'].append('D')
    out = sorted(rows.values(), key=lambda x: (-x['pts'], -(x['gf'] - x['ga']), -x['gf'], -x['w'], C._fold(_tname(x['team']))))
    for i, x in enumerate(out):
        x['pos'] = i + 1
        x['gd'] = x['gf'] - x['ga']
        x['form'] = x['form'][-5:]
    return out


def player_stats(st):
    g, a, motm, apps_team, big, hat, pens = {}, {}, {}, {}, {}, {}, {}
    top4 = set()
    tb = table(st)
    for x in tb[:4]:
        top4.add(x['team'])
    for rd in st['fx']:
        for m in rd:
            if m['hg'] is None:
                continue
            cnt = {}
            for ev in m.get('ev', []):
                _, side, sc, ast, kind = ev
                g[sc] = g.get(sc, 0) + 1
                cnt[sc] = cnt.get(sc, 0) + 1
                if kind == 'pen':
                    pens[sc] = pens.get(sc, 0) + 1
                if ast:
                    a[ast] = a.get(ast, 0) + 1
                opp = m['a'] if side == 0 else m['h']
                if opp in top4:
                    big[sc] = big.get(sc, 0) + 1
            for pid, n in cnt.items():
                if n >= 3:
                    hat[pid] = hat.get(pid, 0) + 1
            if m.get('motm'):
                motm[m['motm']] = motm.get(m['motm'], 0) + 1
    return {'g': g, 'a': a, 'motm': motm, 'big': big, 'hat': hat, 'pens': pens}


def _rank(d, n=30):
    own = _owner()
    rows = sorted(d.items(), key=lambda x: (-x[1], C._fold(own.get(x[0], (0, ''))[1])))[:n]
    out, prev, rank = [], None, 0
    for i, (pid, v) in enumerate(rows):
        if v != prev:
            rank = i + 1
            prev = v
        o = own.get(pid, (None, C._name(pid), ''))
        out.append({'rank': rank, 'pid': pid, 'name': o[1], 'team': o[0], 'pos': o[2], 'n': v})
    return out


# ------------------------------------------------------------------ match engine
def _strength(st, tid, rd):
    att, dfn = STR[tid]
    k = math.exp(st['drift'].get(str(tid), 0))
    tb = table(st, upto=rd)
    row = next(x for x in tb if x['team'] == tid)
    f = row['form']
    mom = 1.0
    if f:
        ppg = sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in f) / len(f)
        mom = math.exp((ppg - 1.5) * 0.035)
    return att * k * mom, dfn / (k ** 0.6) / mom ** 0.5


def _score(st, rd, i, m):
    r = _rng('y17m', st['seed'], rd, i)
    ah, dh = _strength(st, m['h'], rd)
    aa, da = _strength(st, m['a'], rd)
    swing = r.gauss(0, 0.12)
    big = frozenset((m['h'], m['a'])) in RIVALS
    tense = 0.9 if big else 1.0
    lh = ah * da / 1.22 * 1.10 * math.exp(swing) * tense
    la = aa * dh / 1.22 * 0.92 * math.exp(-swing) * tense

    def damp(g):
        return min(g, 4) + sum(1 for _ in range(max(0, g - 4)) if r.random() < 0.45)
    return damp(_poisson(r, lh)), damp(_poisson(r, la))


def _pf(st, pid):
    return st['pform'].get(str(pid), 0.0)


def _weights(st, team, assist):
    rows = []
    for p in squad(team):
        base = (ASSIST_POS if assist else SCORE_POS).get(p['pos'], 1.0) * (1.0 if p['xi'] else 0.22)
        rows.append([p['pid'], p['name'], base])
    total_base = sum(w for _, _, w in rows) or 1.0
    shares = {}
    for pid, name, w in rows:
        s = _star(name)
        if s and w > 0:
            shares[pid] = s[1] if assist else s[0]
    tot = sum(shares.values())
    if tot > 0.85:
        shares = {k: v * 0.85 / tot for k, v in shares.items()}
        tot = 0.85
    rest = sum(w for pid, _, w in rows if pid not in shares) or 1.0
    out = {}
    for pid, name, w in rows:
        v = shares[pid] / (1 - tot) * rest if pid in shares else w
        v *= math.exp(_pf(st, pid))
        if pid in st.get('breakout', ()):
            v *= 2.8 if not assist else 1.7
        out[pid] = max(v, 0.0)
    return out


def _pick(r, w, exclude=None):
    items = [(k, v) for k, v in w.items() if k != exclude and v > 0]
    tot = sum(v for _, v in items)
    x = r.random() * tot
    for k, v in items:
        x -= v
        if x <= 0:
            return k
    return items[-1][0] if items else None


def _events(st, rd, i, m):
    r = _rng('y17ev', st['seed'], rd, i)
    ev = []
    for side, team, n in ((0, m['h'], m['hg']), (1, m['a'], m['ag'])):
        gw, aw = _weights(st, team, False), _weights(st, team, True)
        for _ in range(n):
            sc = _pick(r, gw)
            kind = 'open'
            x = r.random()
            st_ = _star(_owner().get(sc, (0, ''))[1])
            if x < 0.085:
                kind = 'pen'
            elif x < 0.115 + (0.03 if st_ and st_[3] == 'fk' else 0):
                kind = 'fk'
            elif x < 0.30 and GRP.get(_owner().get(sc, (0, '', 'CF'))[2]) in ('D', 'F'):
                kind = 'header'
            elif x < 0.40:
                kind = 'long'
            ast = None
            if kind not in ('pen', 'fk') and r.random() < 0.8:
                ast = _pick(r, aw, exclude=sc)
            ev.append([0, side, sc, ast, kind])
    mins = sorted(r.sample(range(2, 94), len(ev))) if ev else []
    r.shuffle(ev)
    for k, e in enumerate(ev):
        e[0] = mins[k]
    ev.sort(key=lambda e: e[0])
    return ev


def _motm(st, rd, i, m):
    r = _rng('y17motm', st['seed'], rd, i)
    pts = {}
    for _, side, sc, ast, kind in m['ev']:
        pts[sc] = pts.get(sc, 0) + 3
        if ast:
            pts[ast] = pts.get(ast, 0) + 1.6
    win = 0 if m['hg'] > m['ag'] else 1 if m['ag'] > m['hg'] else None
    best, bv = None, -1
    for side, team in ((0, m['h']), (1, m['a'])):
        bonus = 1.3 if win == side else 0.5 if win is None else 0
        conceded = m['ag'] if side == 0 else m['hg']
        for p in squad(team):
            if not p['xi'] and p['pid'] not in pts:
                continue
            v = pts.get(p['pid'], 0) + bonus + r.random() * 0.9
            if conceded == 0 and p['pos'] == 'GK':
                v += 1.6 + r.random()
            elif conceded == 0 and GRP.get(p['pos']) == 'D':
                v += 0.8
            if v > bv:
                best, bv = p['pid'], v
    return best


def _update_form(st, rd):
    r = _rng('y17pf', st['seed'], rd)
    scored = {}
    for m in st['fx'][rd]:
        for _, side, sc, ast, kind in m.get('ev', []):
            scored[sc] = scored.get(sc, 0) + 1
            if ast:
                scored[ast] = scored.get(ast, 0) + 0.5
    pf = st['pform']
    for t in C.UCL17:
        for p in squad(t[0]):
            if not p['xi'] and p['pid'] not in st.get('breakout', ()):
                continue
            k = str(p['pid'])
            v = pf.get(k, 0.0) * 0.72 + r.gauss(0, 0.18) + 0.09 * min(scored.get(p['pid'], 0), 3)
            if not scored.get(p['pid']) and _star(p['name']):
                v -= 0.04
            pf[k] = round(max(-0.55, min(0.75, v)), 3)
    # the duel: the man behind keeps chasing
    stats = player_stats(st)
    ids = {n: next((p['pid'] for t in C.UCL17 for p in squad(t[0]) if C._fold(p['name']) == n), None) for n in ('lionel messi', 'cristiano ronaldo')}
    m_, r_ = ids['lionel messi'], ids['cristiano ronaldo']
    if m_ and r_ and rd >= 8:
        gm, gr = stats['g'].get(m_, 0), stats['g'].get(r_, 0)
        if gm - gr >= 4:
            pf[str(r_)] = round(min(0.75, pf.get(str(r_), 0) + 0.08), 3)
        elif gr - gm >= 4:
            pf[str(m_)] = round(min(0.75, pf.get(str(m_), 0) + 0.08), 3)


def _play_round(st, mine=None, um=None):
    rd = st['round']
    if rd >= len(st['fx']):
        return False
    before = table(st, upto=rd)
    for i, m in enumerate(st['fx'][rd]):
        ev = None
        if mine and st['team'] in (m['h'], m['a']):
            m['hg'], m['ag'] = int(mine[0]), int(mine[1])
            m['you'] = True
            if um:
                ev = _user_events(st, m, {'user_match': um}, {'team_id': st['team']})
        else:
            m['hg'], m['ag'] = _score(st, rd, i, m)
        m['ev'] = ev if ev is not None else _events(st, rd, i, m)
        m['motm'] = _motm(st, rd, i, m)
    st['round'] = rd + 1
    _update_form(st, rd)
    try:
        import y17_news
        y17_news.round_news(st, rd, before)
    except Exception as exc:
        st.setdefault('errors', []).append(repr(exc)[:160])
    if st['round'] >= len(st['fx']):
        _finish(st)
    return True


# ------------------------------------------------------------------ awards
CLASICO = frozenset((1220, 1222))


def impact(st, upto=None):
    """Per player: what his goals and assists were WORTH - match winners, equalisers that saved a point, goals in El Clasico and
    against the top four, man-of-the-match awards in those games, and how much of his team's attack he carried."""
    tb = table(st)
    top4 = {x['team'] for x in tb[:4]}
    team_goals = {x['team']: x['gf'] for x in tb}
    out = {}

    def row(pid):
        return out.setdefault(pid, {'win': 0, 'eq': 0, 'cg': 0, 'ca': 0, 'cm': 0, 'cw': 0, 'bg': 0, 'ba': 0, 'pts': 0.0})
    for rd_i, rd in enumerate(st['fx']):
        if upto is not None and rd_i >= upto:
            break
        for m in rd:
            if m.get('hg') is None:
                continue
            ev = sorted(m.get('ev') or [], key=lambda e: e[0])
            clas = frozenset((m['h'], m['a'])) == CLASICO
            big = m['h'] in top4 or m['a'] in top4
            win = 0 if m['hg'] > m['ag'] else 1 if m['ag'] > m['hg'] else None
            gh = ga = 0
            decisive = None          # (scorer) of the goal that put the winner ahead for good
            last_eq = {0: None, 1: None}
            for mn, side, sc, ast, kind in ev:
                if side == 0:
                    gh += 1
                else:
                    ga += 1
                mine, theirs = (gh, ga) if side == 0 else (ga, gh)
                if win == side and mine == (m['ag'] if side == 0 else m['hg']) + 1 and decisive is None:
                    decisive = (sc, ast)
                if mine == theirs:
                    last_eq[side] = (sc, ast)
                r = row(sc)
                if clas:
                    r['cg'] += 1
                if big and not clas:
                    r['bg'] += 1
                if ast:
                    ra = row(ast)
                    if clas:
                        ra['ca'] += 1
                    if big and not clas:
                        ra['ba'] += 1
            if decisive:
                row(decisive[0])['win'] += 1
                row(decisive[0])['pts'] += 2.0
                if decisive[1]:
                    row(decisive[1])['pts'] += 0.8
            if win is None and (m['hg'] or m['ag']):
                for side in (0, 1):
                    if last_eq[side]:
                        row(last_eq[side][0])['eq'] += 1
                        row(last_eq[side][0])['pts'] += 1.0
            if clas and m.get('motm'):
                row(m['motm'])['cm'] += 1
                own = _owner().get(m['motm'])
                if own and win is not None and own[0] == (m['h'] if win == 0 else m['a']):
                    row(m['motm'])['cw'] += 1
    stats = player_stats(st)
    for pid, r in out.items():
        t = _owner().get(pid, (None,))[0]
        tg = team_goals.get(t) or 1
        r['carry'] = round((stats['g'].get(pid, 0) + 0.5 * stats['a'].get(pid, 0)) / tg, 3)
    return out


def _ballon(st, stats, tb):
    """Ballon d'Or 2017 - a jury's logic, not a goal count:
      output       goals x3, assists x2, man of the match x2.5, hat-tricks x3
      decisive     match winners x4, point-saving equalisers x2 (points he won for his club)
      El Clasico   goals x6, assists x4, man of the match x6 (+4 when his side won it) - the season's defining nights
      big games    goals / assists against the top four x1
      carried      share of his team's attack (goals + half the assists) x45
      trophies     champion +42, runner-up +18, third +9, fourth +4 - weighted by how much he drove it
      reputation   a small tie-breaker (prestige x0.8)"""
    pos_bonus = {1: 42, 2: 18, 3: 9, 4: 4}
    place = {x['team']: x['pos'] for x in tb}
    imp = impact(st)
    rows = []
    for pid, (team, name, pos) in _owner().items():
        if team is None or team not in place:
            continue
        g, a = stats['g'].get(pid, 0), stats['a'].get(pid, 0)
        mo = stats['motm'].get(pid, 0)
        s_ = _star(name)
        pr = s_[2] if s_ else PRESTIGE_GK.get(C._fold(name), 0)
        cs = next(x['cs'] for x in tb if x['team'] == team)
        im = imp.get(pid) or {'win': 0, 'eq': 0, 'cg': 0, 'ca': 0, 'cm': 0, 'cw': 0, 'bg': 0, 'ba': 0, 'carry': 0}
        drive = min(1.0, 0.25 + im.get('carry', 0) * 2.2 + mo * 0.03)
        parts = {
            'output': 3.0 * g + 2.0 * a + 2.5 * mo + 3 * stats['hat'].get(pid, 0),
            'decisive': 4.0 * im['win'] + 2.0 * im['eq'],
            'clasico': 6.0 * im['cg'] + 4.0 * im['ca'] + 6.0 * im['cm'] + 4.0 * im['cw'],
            'big': 1.0 * (im['bg'] + im['ba']),
            'carry': 45.0 * im.get('carry', 0),
            'trophy': pos_bonus.get(place[team], 0) * drive,
            'name': pr * 0.8,
        }
        if pos == 'GK':
            parts['output'] += cs * 1.6
        elif GRP.get(pos) == 'D':
            parts['output'] += cs * 0.7
        score = sum(parts.values())
        why = []
        if place[team] == 1:
            why.append('Champion')
        if im['win']:
            why.append('%d match winner%s' % (im['win'], 's' if im['win'] > 1 else ''))
        if im['cg'] or im['ca']:
            why.append('Clásico %dG %dA' % (im['cg'], im['ca']))
        if im.get('carry', 0) >= 0.3:
            why.append('%d%% of team attack' % round(im['carry'] * 100))
        if stats['hat'].get(pid):
            why.append('%d hat-trick%s' % (stats['hat'][pid], 's' if stats['hat'][pid] > 1 else ''))
        rows.append({'pid': pid, 'name': name, 'team': team, 'pos': pos, 'g': g, 'a': a, 'motm': mo, 'score': round(score, 1),
                     'win': im['win'], 'cg': im['cg'], 'ca': im['ca'], 'cm': im['cm'], 'carry': im.get('carry', 0), 'why': why[:3],
                     'parts': {k: round(v, 1) for k, v in parts.items()}})
    rows.sort(key=lambda x: -x['score'])
    for i, x in enumerate(rows[:30]):
        x['rank'] = i + 1
    return rows[:30]


def _tots(st, stats, tb, ballon):
    by = {}
    score = {x['pid']: x['score'] for x in _ballon(st, stats, tb)} if ballon is None else {x['pid']: x['score'] for x in ballon}
    own = _owner()
    shape = [('GK', 1), ('D', 4), ('M', 3), ('F', 3)]
    out = []
    for g, n in shape:
        cands = [(pid, o) for pid, o in own.items() if (o[2] == 'GK' if g == 'GK' else GRP.get(o[2]) == g and o[2] != 'GK')]
        cands.sort(key=lambda x: -(score.get(x[0], 0) + stats['motm'].get(x[0], 0) * 2 + stats['g'].get(x[0], 0) * 0.5))
        for pid, o in cands[:n]:
            out.append({'pid': pid, 'name': o[1], 'team': o[0], 'pos': o[2], 'line': g})
    return out


def _finish(st):
    stats = player_stats(st)
    tb = table(st)
    ballon = _ballon(st, stats, tb)
    boot = _rank(stats['g'], 5)
    play = _rank(stats['a'], 5)
    gk = max((x for x in tb), key=lambda x: (x['cs'], -x['ga']))
    keeper = next((p for p in squad(gk['team']) if p['pos'] == 'GK' and p['xi']), None)
    br = None
    for pid in st.get('breakout', []):
        o = _owner().get(pid)
        if o and stats['g'].get(pid, 0) + stats['a'].get(pid, 0) >= 8:
            br = {'pid': pid, 'name': o[1], 'team': o[0], 'g': stats['g'].get(pid, 0), 'a': stats['a'].get(pid, 0)}
    st['awards'] = {'champion': tb[0]['team'], 'runner': tb[1]['team'], 'third': tb[2]['team'], 'points': tb[0]['pts'],
                    'boot': boot, 'playmaker': play, 'glove': {'pid': keeper and keeper['pid'], 'name': keeper and keeper['name'], 'team': gk['team'], 'cs': gk['cs']},
                    'ballon': ballon[:10], 'tots': _tots(st, stats, tb, ballon), 'breakout': br, 'shown': False}
    st['history'] = [h for h in st['history'] if h.get('season') != st['season']] + [{
        'season': st['season'], 'champion': tb[0]['team'], 'runner': tb[1]['team'], 'pts': tb[0]['pts'], 'you': next(x['pos'] for x in tb if x['team'] == st['team']),
        'team': st['team'], 'boot': boot[0] if boot else None, 'ballon': ballon[0] if ballon else None, 'podium': ballon[:3]}]
    try:
        import y17_news
        y17_news.season_news(st)
    except Exception as exc:
        st.setdefault('errors', []).append(repr(exc)[:160])


# ------------------------------------------------------------------ views
def _team_doc(tid):
    t = _team(tid)
    return {'id': t[0], 'name': t[1], 'short': t[2], 'crest': t[3], 'c': t[4], 'nick': _nick(tid), 'boss': MANAGERS.get(tid, ''), 'ground': STADIUM.get(tid, '')}


def _scorers_line(m):
    out = {0: [], 1: []}
    for mn, side, sc, ast, kind in m.get('ev', []):
        out[side].append([_short(_owner().get(sc, (0, C._name(sc)))[1]), mn, kind])
    return out


def view(st):
    if not st:
        return {'career': None, 'teams': {str(t[0]): _team_doc(t[0]) for t in C.UCL17},
                'pick': [dict(_team_doc(t[0]), rating=round(STR[t[0]][0] / STR[t[0]][1] * 33)) for t in C.UCL17], 'saves': saves_list()['slots']}
    stats = player_stats(st)
    tb = table(st)
    rd = st['round']
    nxt = None
    if rd < len(st['fx']):
        m = next(m for m in st['fx'][rd] if st['team'] in (m['h'], m['a']))
        nxt = {'round': rd + 1, 'h': m['h'], 'a': m['a'], 'derby': RIVALS.get(frozenset((m['h'], m['a'])))}
    rounds = []
    for i, r_ in enumerate(st['fx']):
        rounds.append([{'h': m['h'], 'a': m['a'], 'hg': m['hg'], 'ag': m['ag'], 'you': bool(m.get('you')), 'sc': _scorers_line(m) if m['hg'] is not None else None,
                        'motm': m.get('motm'), 'i': j} for j, m in enumerate(r_)])
    own = _owner()
    # the Golden Boot race over the season (top 6 at the moment): cumulative goals per round
    top = [x['pid'] for x in _rank(stats['g'], 6)]
    race = {pid: [] for pid in top}
    tot = {pid: 0 for pid in top}
    for r_ in st['fx'][:rd]:
        for m in r_:
            for _, side, sc, ast, kind in m.get('ev', []):
                if sc in tot:
                    tot[sc] += 1
        for pid in top:
            race[pid].append(tot[pid])
    ga = {}
    for pid in set(stats['g']) | set(stats['a']):
        ga[pid] = stats['g'].get(pid, 0) + stats['a'].get(pid, 0)
    hot = sorted(((pid, v) for pid, v in st['pform'].items() if int(pid) in own), key=lambda x: -x[1])
    form = [{'pid': int(pid), 'name': own[int(pid)][1], 'team': own[int(pid)][0], 'v': v, 'g': stats['g'].get(int(pid), 0)} for pid, v in hot[:6]]
    cold = [{'pid': int(pid), 'name': own[int(pid)][1], 'team': own[int(pid)][0], 'v': v, 'g': stats['g'].get(int(pid), 0)}
            for pid, v in sorted(hot, key=lambda x: x[1])[:6] if _star(own[int(pid)][1])][:4]
    _bal_all = _ballon(st, stats, tb) if rd else []
    live_ballon = _bal_all[:10]
    _imp = impact(st) if rd else {}
    clas = []
    for i_, r_ in enumerate(st['fx']):
        for m in r_:
            if frozenset((m['h'], m['a'])) == CLASICO:
                clas.append({'round': i_ + 1, 'i': r_.index(m), 'h': m['h'], 'a': m['a'], 'hg': m['hg'], 'ag': m['ag']})
    duel = {}
    for key in ('lionel messi', 'cristiano ronaldo'):
        pid = next((p for p, o in own.items() if C._fold(o[1]) == key), None)
        if pid:
            im = _imp.get(pid) or {}
            bl = next((x for x in _bal_all if x['pid'] == pid), None)
            duel[key.split()[1]] = {'pid': pid, 'name': own[pid][1], 'team': own[pid][0], 'g': stats['g'].get(pid, 0), 'a': stats['a'].get(pid, 0),
                                    'win': im.get('win', 0), 'cg': im.get('cg', 0), 'ca': im.get('ca', 0), 'cm': im.get('cm', 0), 'carry': im.get('carry', 0),
                                    'big': im.get('bg', 0) + im.get('ba', 0) + im.get('cg', 0) + im.get('ca', 0),
                                    'bscore': bl['score'] if bl else 0, 'brank': bl['rank'] if bl else None,
                                    'motm': stats['motm'].get(pid, 0), 'hat': stats['hat'].get(pid, 0), 'form': st['pform'].get(str(pid), 0),
                                    'ballons': sum(1 for h in st['history'] if h.get('ballon') and h['ballon']['pid'] == pid),
                                    'boots': sum(1 for h in st['history'] if h.get('boot') and h['boot']['pid'] == pid)}
    squads = {str(t[0]): [{'pid': p['pid'], 'name': p['name'], 'pos': p['pos'], 'xi': p['xi'], 'g': stats['g'].get(p['pid'], 0),
                           'a': stats['a'].get(p['pid'], 0), 'motm': stats['motm'].get(p['pid'], 0), 'f': st['pform'].get(str(p['pid']), 0)} for p in squad(t[0])]
              for t in C.UCL17}
    return {'career': {'season': st['season'], 'team': st['team'], 'round': rd, 'rounds': len(st['fx']), 'done': rd >= len(st['fx']), 'horse': st.get('horse'), 'linked': bool(st.get('link'))},
            'teams': {str(t[0]): _team_doc(t[0]) for t in C.UCL17}, 'table': tb, 'next': nxt, 'rounds': rounds,
            'scorers': _rank(stats['g']), 'assists': _rank(stats['a']), 'ga': _rank(ga), 'motm': _rank(stats['motm'], 15),
            'race': [{'pid': pid, 'name': own.get(pid, (0, ''))[1], 'team': own.get(pid, (0,))[0], 'pts': race[pid]} for pid in top],
            'form': form, 'cold': cold, 'ballon': live_ballon, 'duel': duel, 'clasicos': clas, 'news': st['news'][:60], 'awards': st.get('awards'),
            'history': st['history'], 'squads': squads}


def match(st, rd, i):
    try:
        m = st['fx'][rd][i]
    except Exception:
        return {'error': 'no-match'}
    if m['hg'] is None:
        return {'error': 'not-played'}
    own = _owner()
    goals = [{'min': mn, 'side': side, 'name': own.get(sc, (0, C._name(sc)))[1], 'pid': sc, 'assist': ast and own.get(ast, (0, C._name(ast)))[1], 'kind': kind}
             for mn, side, sc, ast, kind in m['ev']]
    rep = None
    try:
        import y17_news
        rep = y17_news.report(st, rd, i)
    except Exception as exc:
        rep = {'paras': ['Report unavailable: %s' % repr(exc)[:80]]}
    lineups = {}
    for side, team in (('h', m['h']), ('a', m['a'])):
        lineups[side] = [{'pid': p['pid'], 'name': p['name'], 'pos': p['pos']} for p in squad(team) if p['xi']]
    mo = own.get(m.get('motm'), (0, '', ''))
    return {'round': rd + 1, 'h': m['h'], 'a': m['a'], 'hg': m['hg'], 'ag': m['ag'], 'goals': goals, 'derby': RIVALS.get(frozenset((m['h'], m['a']))),
            'motm': m.get('motm') and {'pid': m['motm'], 'name': mo[1], 'team': mo[0]}, 'report': rep, 'lineups': lineups,
            'venue': STADIUM.get(m['h'], ''), 'teams': {str(t): _team_doc(t) for t in (m['h'], m['a'])}}


# ------------------------------------------------------------------ saves
def _summary(st):
    if not st:
        return None
    tb = table(st)
    me = next(x for x in tb if x['team'] == st['team'])
    return {'team': st['team'], 'team_name': _tname(st['team']), 'crest': _team(st['team'])[3], 'season': st['season'], 'round': st['round'],
            'rounds': len(st['fx']), 'rank': me['pos'], 'points': me['pts'], 'won': me['w'], 'drawn': me['d'], 'lost': me['l'],
            'titles': sum(1 for h in st['history'] if h['champion'] == st['team'])}


def saves_list():
    out = []
    for s in SLOTS:
        st = _read('slot' + s)
        out.append({'slot': s, 'empty': st is None, 'time': st and st.get('saved'), 'summary': _summary(st)})
    cur = _read('current')
    return {'slots': out, 'current': _summary(cur)}


def api(method, path, body, logic=None):
    parts = [p for p in path.split('/') if p][3:]       # after api/rc29/y17
    try:
        data = json.loads(body or '{}') if body else {}
    except Exception:
        data = {}
    act = parts[0] if parts else ''
    linked = False
    if logic is not None and act in ('', 'match', 'seen'):
        try:
            st, linked = sync(logic)
        except Exception as exc:
            st = _read('current')
            _c['sync_error'] = repr(exc)[:200]
    else:
        st = _read('current')
    if st:
        _extras(st)
    if act == 'saves':
        sub = parts[1] if len(parts) > 1 else ''
        slot = str(data.get('slot') or '')
        if method == 'GET' or not sub:
            return saves_list()
        if slot not in SLOTS:
            return {'error': 'bad-slot'}
        if sub == 'save':
            if not st:
                return {'error': 'no-career'}
            st['saved'] = int(time.time())
            _write('slot' + slot, st)
            return dict(saves_list(), ok=True)
        if sub == 'load':
            sv = _read('slot' + slot)
            if not sv:
                return {'error': 'empty-slot'}
            if st:
                _write('backup', st)
            _write('current', sv)
            return dict(view(sv), ok=True)
        if sub == 'delete':
            _drop('slot' + slot)
            return dict(saves_list(), ok=True)
        return {'error': 'unknown'}
    if method == 'POST' and act == 'kick' and logic is not None:
        return kick_arm(logic)
    if method == 'POST' and act == 'unkick' and logic is not None:
        return kick_clear(logic)
    if method == 'POST' and act == 'new':
        try:
            team = int(data.get('team'))
        except Exception:
            return {'error': 'bad-team'}
        if not _team(team):
            return {'error': 'bad-team'}
        keep = (st or {}).get('history', []) if data.get('keep_history') else []
        st = _new_season(team, 1 if not keep else max(h['season'] for h in keep) + 1, keep)
        try:
            import y17_news
            y17_news.preseason(st)
        except Exception:
            pass
        _write('current', st)
        return view(st)
    if method == 'POST' and act == 'quit':
        if st:
            _write('backup', st)
        _drop('current')
        return view(None)
    if not st:
        return view(None)
    if method == 'POST' and act == 'next':
        mine = None
        if data.get('hg') is not None and data.get('ag') is not None:
            try:
                mine = (max(0, min(15, int(data['hg']))), max(0, min(15, int(data['ag']))))
            except Exception:
                mine = None
        _play_round(st, mine)
        st['saved'] = int(time.time())
        _write('current', st)
        return view(st)
    if method == 'POST' and act == 'sim':
        n = 0
        while st['round'] < len(st['fx']) and n < 40:
            _play_round(st)
            n += 1
        st['saved'] = int(time.time())
        _write('current', st)
        return view(st)
    if method == 'POST' and act == 'seen':
        if st.get('awards'):
            st['awards']['shown'] = True
            _write('current', st)
        return {'ok': True}
    if method == 'POST' and act == 'season':
        if st['round'] < len(st['fx']):
            return {'error': 'season-active'}
        team = int(data.get('team') or st['team'])
        if not _team(team):
            team = st['team']
        ns = _new_season(team, st['season'] + 1, st['history'])
        try:
            import y17_news
            y17_news.preseason(ns)
        except Exception:
            pass
        _write('current', ns)
        return view(ns)
    if act == 'match' and len(parts) >= 3:
        try:
            return match(st, int(parts[1]) - 1, int(parts[2]))
        except Exception:
            return {'error': 'no-match'}
    out = view(st)
    out['link_active'] = linked
    if _c.get('sync_error'):
        out['sync_error'] = _c['sync_error']
    return out


# ------------------------------------------------------------------ RC29.18: linked to My League's Y17 Champion League (real matches)
def _extras(st):
    own = _owner()
    for k, v in (st.get('extra') or {}).items():
        own.setdefault(int(k), tuple(v))


def _ml_state(logic):
    try:
        import iml_host as HO, my_league as ML
        main = HO._main_conn(logic)
        s = ML.state(main)
        if isinstance(s, dict) and int(s.get('competition_id') or 0) == LINK_CID and s.get('schedule_v2'):
            return s
    except Exception:
        pass
    return None


def _link_id(s):
    sig = zlib.crc32(json.dumps([[(m['home_team_id'], m['away_team_id']) for m in fx['match_list']] for fx in s['schedule_v2']]).encode())
    return '%s:%s:%s' % (s.get('team_id'), s.get('season') or 1, sig)


def _new_linked(s, history, season):
    st = _new_season(int(s['team_id']), season, history, seed=zlib.crc32(_link_id(s).encode()) or 1)
    st['fx'] = [[{'h': int(m['home_team_id']), 'a': int(m['away_team_id']), 'hg': None, 'ag': None} for m in fx['match_list']] for fx in s['schedule_v2']]
    st['link'] = _link_id(s)
    st['news'] = []
    try:
        import y17_news
        y17_news.preseason(st)
    except Exception:
        pass
    return st


def _user_events(st, m, entry, s):
    """Real scorers / assists of your match (My League's own record of the game you played)."""
    u = entry.get('user_match') or {}
    goals, assists = u.get('goals') or [], u.get('assists') or []
    me = int(s['team_id'])
    my_side = 0 if m['h'] == me else 1
    ev = []
    st.setdefault('extra', {})
    for i, g in enumerate(goals):
        try:
            cid, serial = int(g[0]), int(g[1])
        except Exception:
            continue
        side = my_side if serial else 1 - my_side
        if side == my_side and cid not in _owner():
            st['extra'][str(cid)] = [me, C._name(cid), C._pos(cid)]
        ast = None
        if i < len(assists):
            try:
                a0, a1 = int(assists[i][0]), int(assists[i][1])
                if a0 and a0 != cid and bool(a1) == bool(serial):
                    ast = a0
                    if side == my_side and a0 not in _owner():
                        st['extra'][str(a0)] = [me, C._name(a0), C._pos(a0)]
            except Exception:
                ast = None
        ev.append([0, side, cid, ast, 'open'])
    _extras(st)
    if [e[1] for e in ev].count(0) != m['hg'] or [e[1] for e in ev].count(1) != m['ag']:
        return None
    r = _rng('y17real', st['seed'], m['h'], m['a'], st['round'])
    mins = sorted(r.sample(range(2, 94), len(ev))) if ev else []
    for k, e in enumerate(ev):
        e[0] = mins[k]
    return ev


def _apply_played(st, entry, s):
    rd = st['round']
    before = table(st, upto=rd)
    res = {(int(x['home_team_id']), int(x['away_team_id'])): (int(x['home_goals']), int(x['away_goals'])) for x in entry.get('matches') or []}
    me = int(s['team_id'])
    for i, m in enumerate(st['fx'][rd]):
        sc = res.get((m['h'], m['a']))
        if sc is None:
            sc = _score(st, rd, i, m)
        m['hg'], m['ag'] = sc
        ev = None
        if me in (m['h'], m['a']):
            m['you'] = True
            ev = _user_events(st, m, entry, s)
        m['ev'] = ev if ev is not None else _events(st, rd, i, m)
        m['motm'] = _motm(st, rd, i, m)
    st['round'] = rd + 1
    _update_form(st, rd)
    try:
        import y17_news
        y17_news.round_news(st, rd, before)
    except Exception as exc:
        st.setdefault('errors', []).append(repr(exc)[:160])
    if st['round'] >= len(st['fx']):
        _finish(st)


def sync(logic):
    """Follow My League's Y17 season: every matchday played there is taken over here (scores of all six matches, your real
    scorers).  Returns the stored league (None when My League is not on the Y17 Champion League)."""
    st = _read('current')
    s = _ml_state(logic)
    if s is None:
        if st:
            _extras(st)
        return st, False
    if st and not st.get('link'):
        _extras(st)
        return st, False            # a league played from this page: My League does not take it over
    link = _link_id(s)
    if not st or st.get('link') != link:
        hist = (st or {}).get('history', [])
        season = (max([h['season'] for h in hist]) + 1) if hist else 1
        if st and st.get('link') and st.get('round', 0) < len(st.get('fx') or []) and not any(h.get('season') == st.get('season') for h in hist):
            season = st['season'] + 1
        st = _new_linked(s, hist, season)
    _extras(st)
    played = s.get('played') or {}
    changed = False
    while st['round'] < len(st['fx']) and str(st['round'] + 1) in played:
        _apply_played(st, played[str(st['round'] + 1)], s)
        changed = True
    if changed or not _read('current') or _read('current').get('link') != st.get('link'):
        st['saved'] = int(time.time())
        _write('current', st)
    return st, True


def install_schedule():
    """My League's Y17 Champion League (518) as a triple round robin: 33 matchdays, every pair meets three times.  The checked
    native config stays untouched - only the schedule document the league reads for a NEW season is replaced (myleague_worlds'
    own legs=3 generator, the one the Asia-Pacific League already uses).  A season in progress keeps its stored draw."""
    try:
        import ziru_data as Z, myleague_worlds as W
        teams = list(W.config()['leagues'][str(LINK_CID)]['teams'])
        Z._cache['schedules/ml_schedule_%d.json' % LINK_CID] = {'schedule_list': W.schedule(teams, 3)}
        _c['schedule'] = 'legs3'
    except Exception as exc:
        _c['schedule'] = repr(exc)[:200]


# ------------------------------------------------------------------ RC29.18: Play - your match through the Master League's match flow
KICK = 'rc29_y17_kick'
EXT = 'rc29_y17_ext'
KICK_TTL = 1800
POST_BASE = 5000


def _ml_conn(logic):
    import iml_host as HO
    return HO._open_ml(HO._main_conn(logic))


def _m_get(conn, key):
    r = conn.execute('select value from meta where key=?', (key,)).fetchone()
    try:
        return json.loads(r[0]) if r and r[0] else None
    except Exception:
        return None


def _m_set(conn, key, value):
    conn.execute('delete from meta where key=?', (key,))
    if value is not None:
        conn.execute('insert into meta(key, value) values(?, ?)', (key, json.dumps(value)))
    conn.commit()


def kick_arm(logic):
    st = _read('current')
    if not st or st['round'] >= len(st['fx']):
        return {'error': 'no-match', 'reason': 'No match to play'}
    if st.get('link'):
        return {'error': 'linked', 'reason': 'This season follows My League'}
    rd = st['round']
    m = next(m for m in st['fx'][rd] if st['team'] in (m['h'], m['a']))
    home = m['h'] == st['team']
    opp = m['a'] if home else m['h']
    c = _ml_conn(logic)
    try:
        import my_league as ML
        s = ML.state(c)
        if not isinstance(s, dict) or not s.get('schedule_v2'):
            return {'error': 'no-career', 'reason': 'Start a Master League career first: the match runs through its match flow'}
        if s.get('completed'):
            return {'error': 'no-career', 'reason': 'Your Master League season is over: start the next season first'}
        _m_set(c, KICK, {'season': st['season'], 'round': rd, 'opponent': opp, 'home': home, 'team': st['team'], 't': int(time.time())})
    finally:
        c.close()
    return {'ok': True, 'round': rd + 1, 'home': home, 'opponent': opp, 'team': st['team'],
            'label': 'Champions League 2017 · Matchday %d' % (rd + 1), 'derby': RIVALS.get(frozenset((m['h'], m['a'])))}


def kick_clear(logic):
    c = _ml_conn(logic)
    try:
        _m_set(c, KICK, None)
    finally:
        c.close()
    return {'ok': True}


def _kick(conn):
    k = _m_get(conn, KICK)
    if not k or int(time.time()) - int(k.get('t') or 0) > KICK_TTL:
        return None
    return k


def install_kick():
    try:
        import iml_europe as E
    except Exception as exc:
        _c['kick_install'] = repr(exc)[:200]
        return
    if getattr(E.pending_kick, '_rc29_y17', False):
        return
    o_pending, o_arm, o_ext, o_venue, o_settle = E.pending_kick, E.arm_kick, E.kick_external, E.kick_venue, E.settle_kick

    def pending_kick(conn, s):
        try:
            k = _kick(conn)
            if k:
                return {'id': 'y17-%d-%d' % (k['season'], k['round']), 'date': None, 'comp': 'y17', 'stage': 'league',
                        'label': 'Champions League 2017 · Matchday %d' % (k['round'] + 1), 'home': bool(k['home']), 'neutral': False, 'opponent': int(k['opponent'])}
        except Exception as exc:
            _c['kick_pending'] = repr(exc)[:200]
        return o_pending(conn, s)

    def arm_kick(conn, s, gid, mapping):
        k = _kick(conn)
        if not k:
            return o_arm(conn, s, gid, mapping)
        ext = {'game_id': gid, 'leg': 'y17-%d-%d' % (k['season'], k['round']), 'side': 'HOME' if k['home'] else 'AWAY',
               'opponent': int(k['opponent']), 'mapping': mapping, 'y17': k}
        _m_set(conn, EXT, ext)
        return ext

    def kick_external(conn, gid):
        ext = _m_get(conn, EXT)
        if ext and ext.get('game_id') == gid:
            return ext
        return o_ext(conn, gid)

    def kick_venue(conn, s, gid):
        ext = _m_get(conn, EXT)
        if ext and ext.get('game_id') == gid:
            try:
                import iml_venue as V
                k = ext['y17']
                return V.plan(k['team'], k['opponent'], 'HOME') if k['home'] else V.plan(k['opponent'], k['team'], 'AWAY')
            except Exception:
                return None
        return o_venue(conn, s, gid)

    def settle_kick(conn, gid, uside, req):
        ext = _m_get(conn, EXT)
        if not ext or ext.get('game_id') != gid:
            return o_settle(conn, gid, uside, req)
        import my_league as ML
        k = ext['y17']
        h, w = ML._scores(req)
        ours, theirs = (h, w) if uside == 'HOME' else (w, h)
        try:
            import vscom_result
            if vscom_result.gave_up(req):
                ours, theirs = 0, 3
        except Exception:
            pass
        um = None
        try:
            settle_req = ML._translate_opponent_events(req, ext.get('mapping'))
            um = ML._user_match(conn, settle_req, uside, gid)
        except Exception as exc:
            _c['kick_um'] = repr(exc)[:200]
        st = _read('current')
        if st and st['season'] == k['season'] and st['round'] == k['round']:
            hg, ag = (ours, theirs) if k['home'] else (theirs, ours)
            _play_round(st, mine=(hg, ag), um=um)
            st['saved'] = int(time.time())
            st['just'] = k['round'] + 1
            _write('current', st)
        _m_set(conn, EXT, None)
        _m_set(conn, KICK, None)
        res = 'WIN' if ours > theirs else 'LOSE' if ours < theirs else 'DRAW'
        return {'game_id': gid, 'fixture': POST_BASE + k['round'] + 1, 'cup': 'y17', 'leg': ext['leg'], 'result': res, 'score': [ours, theirs], 'detail': {}}
    pending_kick._rc29_y17 = True
    E.pending_kick, E.arm_kick, E.kick_external, E.kick_venue, E.settle_kick = pending_kick, arm_kick, kick_external, kick_venue, settle_kick
    _c['kick_install'] = 'ok'
