"""RC29.12: the V32 Home -> News feed, rewritten in English with varied headlines and real-sounding quotes.

V32 generates every story in Chinese from a small set of topics (big_win, heavy_loss, narrow, draw, goalless, shootout, shutout,
match_home, round_summary, round_shutouts, xfer_buy ...). The facts (teams, score, round, fee, player) are kept; only the words change.
"""
import re, zlib, random

COACH = {101: 'Mikel Arteta', 173: 'Pep Guardiola', 103: 'Arne Slot', 102: 'Enzo Maresca', 179: 'Thomas Frank', 100: 'Ruben Amorim',
         106: 'Eddie Howe', 107: 'Unai Emery', 108: 'Hansi Flick', 109: 'Xabi Alonso', 172: 'Diego Simeone', 258: 'Ernesto Valverde',
         127: 'Vincent Kompany', 126: 'Niko Kovac', 128: 'Kasper Hjulmand', 114: 'Luis Enrique', 113: 'Roberto De Zerbi', 119: 'Cristian Chivu',
         120: 'Luciano Spalletti', 121: 'Massimiliano Allegri', 327: 'Antonio Conte', 125: 'Gian Piero Gasperini', 234: 'Ivan Juric',
         191: 'Jose Mourinho', 130: 'Okan Buruk', 197: 'Domenico Tedesco', 193: 'Rui Borges', 192: 'Francesco Farioli'}

H = {
    'big_win': ['{w} run riot against {l}', '{s}! {w} tear {l} apart', 'Statement made: {w} {s} {l}', '{w} put on a show at {l}\'s expense'],
    'heavy_loss': ['Nightmare for {l}: hammered {s} by {w}', '{l} humbled in {s} thrashing', 'Questions for {l} after {s} collapse', 'Rock bottom? {l} crushed by {w}'],
    'narrow': ['{w} edge a thriller against {l}', 'Nerves of steel: {w} {s} {l}', '{w} hang on to beat {l}', 'Fine margins go {w}\'s way'],
    'draw': ['All square: {a} {s} {b}', 'Honours even between {a} and {b}', '{a} and {b} trade blows in {s} draw', 'Nothing to separate {a} and {b}'],
    'goalless': ['Stalemate: {a} and {b} cancel each other out', 'Chess, not football: {a} 0-0 {b}', 'Keepers on top as {a} and {b} draw a blank'],
    'shootout': ['Goal fest! {a} {s} {b}', '{n} goals and pure chaos: {a} v {b}', 'Defences on holiday as {a} and {b} share {n} goals'],
    'shutout': ['{w} win and keep it tight', 'Clean sheet, three points: {w}', '{w} shut out {l}', 'Wall at the back: {w} blank {l}'],
    'match_home': ['Fortress! {w} too strong for {l} at home', '{w} make home advantage count against {l}', 'Home crowd roars as {w} beat {l}'],
    'round_summary': ['{lg}: {n} goals in round {r}', 'Round {r} in {lg}: the numbers', '{lg} round {r} wrap: {n} goals'],
    'round_shutouts': ['{lg} round {r}: {n} clean sheets', 'Defences rule in {lg} round {r}'],
    'xfer_buy': ['DONE DEAL: {p} joins {w}', 'Here we go! {p} signs for {w}', '{w} land {p}', 'Transfer: {p} completes move to {w}'],
}
QW = ['We controlled the game and the players executed the plan perfectly.', 'This is the mentality I want. Hungry, brave, together.',
      'Three points, but we can still play better. Next game.', 'The fans pushed us all night. This one is for them.']
QL = ['We were not at our level. I take full responsibility.', 'It hurts. We have to look at ourselves and react quickly.',
      'Football can be cruel, but there are no excuses tonight.']
QD = ['A fair result. Both teams had their moments.', 'We wanted the win, but a point away from home is not bad.', 'Not perfect, not a disaster. We move on.']
LG = {113: 'Premier League', 119: 'La Liga', 116: 'Serie A', 122: 'Ligue 1', 900307: 'Bundesliga'}
_names = {}


_zh = {}


def _team_names(conn, s):
    if _names:
        return _names
    try:
        import iml_world_leagues as W
        for t in list(_names_world(conn, s)):
            try:
                z = W._zh(t)
                if z:
                    _zh[z] = t
            except Exception:
                pass
    except Exception:
        pass
    return _names


def _names_world(conn, s):
    try:
        import ml_editor as E
        for cid in E._leagues(s):
            w = E._load(conn, s, cid) or {}
            for tid, c in (w.get('clubs') or {}).items():
                _names[int(tid)] = E._team_name(tid, c)
    except Exception:
        pass
    return _names


def _pick(seed, arr):
    return arr[zlib.crc32(str(seed).encode()) % len(arr)]


def rewrite(conn, s, d):
    if not isinstance(d, dict) or not isinstance(d.get('items'), list):
        return d
    nm = _team_names(conn, s)
    name = lambda t: nm.get(int(t), '') if t is not None else ''
    for it in d['items']:
        try:
            _one(it, name)
        except Exception:
            pass
    for l in d.get('leagues') or []:
        l['name'] = LG.get(int(l.get('id') or 0), l.get('name'))
    d['language'] = 'en'
    add_articles(conn, s, d)
    return d


def _one(it, name):
    tp = it.get('topic')
    teams = [int(t) for t in it.get('teams') or []]
    body = it.get('body') or ''
    sc = re.search(r'(\d+)\s*[:：-]\s*(\d+)', body)
    x, y = (int(sc.group(1)), int(sc.group(2))) if sc else (None, None)
    lg = LG.get(int(it.get('league_id') or 0), it.get('league') or '')
    rnd = it.get('fixture') or ''
    seed = it.get('id') or it.get('title')
    if tp not in H:
        return
    # who is who: the Chinese club names in V32's own sentence (title first, then body), in the order they appear
    text = (it.get('title') or '') + '|' + body
    found = sorted(((text.find(z), t) for z, t in _zh.items() if z and z in text), key=lambda x: x[0])
    order = []
    for _, t in found:
        if t not in order:
            order.append(t)
    for t in teams:
        if t not in order:
            order.append(t)
    t1 = order[0] if order else None
    t2 = order[1] if len(order) > 1 else None
    hi, lo = (max(x, y), min(x, y)) if x is not None else (0, 0)
    f = dict(s='%d-%d' % (hi, lo) if x is not None else '', n=(x + y) if x is not None else '', lg=lg, r=rnd)
    if tp in ('big_win', 'narrow', 'shutout', 'match_home'):
        f.update(w=name(t1), l=name(t2) or 'their opponents')
    elif tp == 'heavy_loss':
        f.update(l=name(t1), w=name(t2) or 'their opponents')
    elif tp in ('draw', 'goalless', 'shootout'):
        f.update(a=name(t1), b=name(t2), s='%d-%d' % (x, y) if x is not None else '')
    elif tp in ('round_summary', 'round_shutouts'):
        m = re.search(r'(\d+)', it.get('title') or '')
        f['n'] = m.group(1) if m else ''
    elif tp == 'xfer_buy':
        p = re.search(r'签下(.+?)。?$', body)
        fee = re.search(r'€[\d.]+M', body)
        f.update(w=name(t1), p=(p.group(1).strip() if p else 'a new signing'), fee=fee.group(0) if fee else '', l=name(t2))
    if any(v == '' for k, v in f.items() if k in ('w', 'a', 'l', 'b')):
        return
    it['title'] = _pick(seed, H[tp]).format(**f)
    q, by = None, None
    if tp in ('big_win', 'narrow', 'shutout', 'match_home'):
        b = f'{f["w"]} beat {f["l"]} {f["s"]} in {lg} round {rnd}.' if f['s'] else f'{f["w"]} beat {f["l"]}.'
        q, by = _pick(seed + 'q', QW), COACH.get(t1, f['w'] + ' head coach')
    elif tp == 'heavy_loss':
        b = f'{f["l"]} lost {f["s"]} to {f["w"]} in {lg} round {rnd}.'
        q, by = _pick(seed + 'q', QL), COACH.get(t1, f['l'] + ' head coach')
    elif tp in ('draw', 'goalless'):
        b = f'{f["a"]} and {f["b"]} drew {f["s"]} in {lg} round {rnd}.'
        q, by = _pick(seed + 'q', QD), COACH.get(t1, f['a'] + ' head coach')
    elif tp == 'shootout':
        b = f'{f["a"]} {f["s"]} {f["b"]}: {f["n"]} goals in {lg} round {rnd}.'
    elif tp == 'round_summary':
        b = f'Round {rnd} of {lg} is in the books with {f["n"]} goals.'
    elif tp == 'round_shutouts':
        b = f'{f["n"]} teams kept a clean sheet in round {rnd} of {lg}.'
    else:
        b = f'{f["w"]} sign {f["p"]}' + (f' from {f["l"]}' if f['l'] else '') + (f' for {f["fee"]}' if f['fee'] else '') + '.'
        q, by = _pick(seed + 'q', ['A player of his quality makes us stronger. We are very happy.', 'He was our first choice. The project convinced him.',
                                   'We have followed him for a long time. Welcome!']), COACH.get(t1, f['w'] + ' head coach')
    it['body'] = b + (f'\n“{q}” — {by}' if q else '')
    it['league'] = lg


# ------------------------------------------------------------------ full match articles (tap a story)
OPEN = {
    'win': ['Under the lights, {w} delivered exactly the performance their supporters had demanded.',
            'It was a night that will be replayed for weeks in {wcity}: {w} were sharper, braver and more clinical.',
            'From the first whistle the tempo belonged to {w}, and {l} spent long spells chasing shadows.'],
    'draw': ['Neither side blinked in a contest that swung like a pendulum.', 'Two teams, two plans, and in the end nothing to separate them.',
             'A game of chess played at full sprint finished with the points shared.'],
}
GOAL_V = ['{p} struck in the {m}th minute', '{p} found the net on {m} minutes', 'on {m} minutes {p} made it count', '{p} pounced in the {m}th minute']
ASSIST_V = ['after {a} had carved the defence open', 'from a perfectly weighted ball by {a}', 'following clever work from {a}', 'converting {a}\'s cross']
STAR_V = ['{p} was the heartbeat of the side, finishing with a rating of {r}.', 'Nobody on the pitch matched {p}, who earned a {r} from our analysts.',
          '{p} turned in a display of real authority ({r}): every big moment seemed to go through him.']
PLAYER_Q = ['The team worked so hard for this. I just tried to help.', 'We knew this game was important. We showed character.',
            'I feel good, I feel confident. More to come.', 'The fans were incredible today. That one was for them.']


def _article(it, f, tp, t1, t2, snap_day, lg_id, rnd, name, sqcache, pn=None):
    import ml_awards as A, iml_world_leagues as W, ml_realism as M
    m = None
    for x in (snap_day or {}).get('matches') or []:
        if {int(x['home_team_id']), int(x['away_team_id'])} == {t1, t2}:
            m = x
            break
    if m is None:
        return None
    home, away = int(m['home_team_id']), int(m['away_team_id'])
    hg, ag = int(m['home_goals']), int(m['away_goals'])
    rows = [r for r in snap_day.get('ps') or [] if int(r[0]) in (home, away)]
    pn = pn or {}
    nm = lambda pid: pn.get(str(pid)) or (M._name(pid) if str(pid).isdigit() else str(pid))
    try:
        lw = W.open_league(_conn_ref['c'], int(lg_id))
    except Exception:
        lw = None
    goals, sides = A._match_ratings(str(lg_id), str(rnd), m, rows, lw, nm, sqcache)
    rng = random.Random(zlib.crc32(('art:%s' % it.get('id')).encode()))
    mins = sorted(rng.sample(range(4, 91), len(goals))) if goals and len(goals) < 80 else []
    rng.shuffle(goals)
    timeline = []
    for g, mi in zip(goals, mins):
        timeline.append({'min': mi, 'team': g['team'], 'name': g['name'], 'assist': g.get('assist')})
    timeline.sort(key=lambda x: x['min'])
    win = home if hg > ag else away if ag > hg else None
    lose = (away if win == home else home) if win else None
    paras = []
    if win:
        paras.append(rng.choice(OPEN['win']).format(w=name(win), l=name(lose), wcity=name(win)))
    else:
        paras.append(rng.choice(OPEN['draw']))
    if timeline:
        bits = []
        for g in timeline:
            s = rng.choice(GOAL_V).format(p=g['name'], m=g['min'])
            if g['assist']:
                s += ', ' + rng.choice(ASSIST_V).format(a=g['assist'])
            bits.append(s + ('' if len({x['team'] for x in timeline}) == 1 else ' (' + name(g['team']) + ')'))
        paras.append(bits[0][0].upper() + bits[0][1:] + '. ' + ' '.join(b[0].upper() + b[1:] + '.' for b in bits[1:]))
        late = [g for g in timeline if g['min'] >= 85]
        if late and abs(hg - ag) <= 1 and win and late[-1]['team'] == win:
            paras.append('The drama was saved for the death: %s settled the nerves in the %dth minute and the stadium erupted.' % (late[-1]['name'], late[-1]['min']))
    else:
        paras.append('Chances were few and far between; both goalkeepers handled everything that came their way.')
    allp = [(p, sides[sd][0]) for sd in ('home', 'away') for p in sides[sd][1]]
    best = max(allp, key=lambda x: x[0]['r']) if allp else None
    if best:
        paras.append(rng.choice(STAR_V).format(p=best[0]['name'], r='%.1f' % best[0]['r']))
    hs, as_ = 0.5 + (hg - ag) * 0.03 + rng.uniform(-0.06, 0.06), None
    poss = max(32, min(68, int(round(hs * 100))))
    sh_h = max(hg + 2, int(rng.gauss(11 + 2 * (hg - ag), 3))); sh_a = max(ag + 2, int(rng.gauss(11 + 2 * (ag - hg), 3)))
    stats = [['Possession', '%d%%' % poss, '%d%%' % (100 - poss)], ['Shots', sh_h, sh_a],
             ['On target', max(hg, min(sh_h, hg + rng.randint(1, 4))), max(ag, min(sh_a, ag + rng.randint(1, 4)))],
             ['Corners', rng.randint(2, 9), rng.randint(2, 9)]]
    ratings = {sd: [{'name': p['name'], 'pid': p.get('pid'), 'r': p['r'], 'g': p['g'], 'a': p['a']} for p in sides[sd][1][:5]] for sd in ('home', 'away')}
    pq = None
    if best and best[0]['g'] + best[0]['a'] > 0:
        pq = {'q': rng.choice(PLAYER_Q), 'by': best[0]['name']}
    return {'paras': paras, 'timeline': timeline, 'stats': stats, 'home': home, 'away': away, 'score': [hg, ag], 'ratings': ratings,
            'motm': {'name': best[0]['name'], 'pid': best[0].get('pid'), 'r': best[0]['r'], 'team': best[1]} if best else None, 'player_quote': pq}


_conn_ref = {'c': None}


def add_articles(conn, s, d):
    try:
        import iml_news_leagues as nl
        snaps = (nl.load(conn, s) or {}).get('leagues') or {}
    except Exception:
        return d
    _conn_ref['c'] = conn
    nm = _team_names(conn, s)
    name = lambda t: nm.get(int(t), '') if t is not None else ''
    sqcache = {}
    for it in d.get('items') or []:
        try:
            tp = it.get('topic')
            if tp not in ('big_win', 'heavy_loss', 'narrow', 'draw', 'goalless', 'shootout', 'shutout', 'match_home'):
                continue
            teams = [int(t) for t in it.get('teams') or []]
            lg = str(it.get('league_id') or '')
            snap = snaps.get(lg) or {}
            day = (snap.get('played') or {}).get(str(it.get('fixture')))
            if not day:
                continue
            t1 = teams[0] if teams else None
            t2 = teams[1] if len(teams) > 1 else None
            if t2 is None:
                for x in day.get('matches') or []:
                    if t1 in (int(x['home_team_id']), int(x['away_team_id'])):
                        t2 = int(x['away_team_id']) if int(x['home_team_id']) == t1 else int(x['home_team_id'])
            art = _article(it, None, tp, t1, t2, day, lg, it.get('fixture'), name, sqcache.setdefault(lg, {}), snap.get('pn') or {})
            if art:
                it['article'] = art
        except Exception:
            pass
    return d
