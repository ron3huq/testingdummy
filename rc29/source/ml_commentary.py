"""RC29.17: commentator-style match writing for Master League news articles (V32 news topics), shared phrase banks with y17_news.

  lines(timeline, home, away, name, seed)  -> ["23' - The opener: Kane rises highest and heads it in after Olise's cross (1-0). \"Kane! He just doesn't miss!\"", ...]
  scene / verdict / voices                 -> opening paragraph, the final word, both managers and the man of the match in their own voice
"""
import random, zlib

import y17_news as N

SHOUT_ML = {
    'kylian mbappe': ['Mbappé! Lightning in boots!', 'Kylian Mbappé - unplayable!'], 'erling haaland': ['Haaland! The cyborg strikes again!', 'Who else? Erling Haaland!'],
    'harry kane': ['Kane! He just doesn\'t miss!', 'Harry Kane, cold as ice!'], 'lamine yamal': ['Lamine Yamal! A teenager doing impossible things!', 'Yamal! Pure magic!'],
    'mohamed salah': ['Salah! The Egyptian King!'], 'vinicius': ['Vinícius! Samba on the wing!'], 'raphinha': ['Raphinha! What a strike!'],
    'robert lewandowski': ['Lewandowski! Ageless!'], 'lautaro martinez': ['Lautaro! El Toro!'], 'bukayo saka': ['Saka! Starboy!'],
    'jude bellingham': ['Bellingham! Hey Jude!'], 'ousmane dembele': ['Dembélé! Both feet, no fear!'], 'viktor gyokeres': ['Gyökeres! The masked man strikes!'],
    'cole palmer': ['Palmer! Cold Palmer!'], 'michael olise': ['Olise! Silk!'], 'florian wirtz': ['Wirtz! Genius!'], 'khvicha kvaratskhelia': ['Kvaradona!'],
    'serhou guirassy': ['Guirassy! Again!'], 'alexander isak': ['Isak! Elegance itself!'], 'pedri': ['Pedri! The conductor finishes the symphony!'],
}
BOSS = {
    'Arteta': {'win': ['We showed the character this group has. Relentless.', 'Big night. The way we defended as a team - that\'s the standard.'],
               'loss': ['Painful. We have to learn quickly and react.', 'Fine margins decided it. We were not ruthless enough.'],
               'draw': ['We wanted more. We dominated big phases, but the last action was missing.']},
    'Slot': {'win': ['Good performance, good result. Let\'s keep it calm.', 'I liked our control today. The players deserve it.'],
             'loss': ['We were not good enough in both boxes. Simple as that.', 'It\'s football - sometimes you don\'t get what you deserve.'],
             'draw': ['A point. Not more, not less.']},
    'Flick': {'win': ['Intensity and courage. That is our football.', 'We pressed high and we were brave. I am very happy.'],
              'loss': ['We made mistakes in transition. We must analyse.', 'Not our day. We stay calm.'],
              'draw': ['We had the chances. Next time they go in.']},
    'Alonso': {'win': ['The structure was perfect today. Very proud.', 'We managed the moments well. That is maturity.'],
               'loss': ['We need to be more consistent in the details.', 'A lesson. We take it and grow.'],
               'draw': ['Balanced game. We accept it.']},
    'Kompany': {'win': ['Dominant. That\'s the identity of this club.', 'Every player gave everything. Outstanding.'],
                'loss': ['We set high standards. Today we fell below them.'], 'draw': ['We wanted three points. We\'ll come back stronger.']},
    'Amorim': {'win': ['Step by step. Today was a good step.', 'The players believed in the idea. You can see it.'],
               'loss': ['I am not going to hide - we were bad. I am the first responsible.', 'It\'s hard. But we will keep going with our idea.'],
               'draw': ['It\'s not enough for this club. We know that.']},
    'Maresca': {'win': ['We controlled the ball and the game. That\'s what we want.'], 'loss': ['We lost our structure in key moments.'],
                'draw': ['We created enough to win it.']},
    'Howe': {'win': ['The supporters were magnificent tonight. What a performance.'], 'loss': ['Disappointing. We regroup.'], 'draw': ['A hard-fought point.']},
    'Frank': {'win': ['Brave, aggressive, smart. Exactly what we trained.'], 'loss': ['We have to be better with and without the ball.'], 'draw': ['Fair result.']},
    'Enrique': {'win': ['Good. Very good. Next question.', 'We attacked like a team and defended like a team.'], 'loss': ['We were worse. I will not invent excuses.'],
                'draw': ['Not enough for us. Never enough.']},
    'Chivu': {'win': ['The lads played with heart. Great night.'], 'loss': ['We must be more clinical.'], 'draw': ['A point we take.']},
    'Gasperini': {'win': ['Our intensity broke them. Fantastic.'], 'loss': ['We paid for the details.'], 'draw': ['Open game, fair result.']},
}
for k, v in N.BV.items():
    BOSS.setdefault(k, v)


def _r(*p):
    return random.Random(zlib.crc32(':'.join(str(x) for x in p).encode()))


def _fold(n):
    import unicodedata
    return unicodedata.normalize('NFKD', n or '').encode('ascii', 'ignore').decode().lower().replace('-', ' ')


def _shout(r, who):
    f = _fold(who)
    for bank in (SHOUT_ML, N.SHOUT):
        for k, lines in bank.items():
            if k in f and r.random() < 0.75:
                return ' "' + N.pick(r, lines) + '"'
    return ''


def _kind(r, i):
    x = r.random()
    return 'pen' if x < 0.08 else 'fk' if x < 0.11 else 'header' if x < 0.27 else 'long' if x < 0.37 else 'open'


def lines(timeline, home, away, seed):
    r = _r('mlcm', seed)
    gh = ga = 0
    out = []
    for i, g in enumerate(timeline):
        side_home = g['team'] == home
        nh, na = (gh + 1, ga) if side_home else (gh, ga + 1)
        mine, theirs = (nh, na) if side_home else (na, nh)
        if gh == ga == 0:
            ctx = N.pick(r, ['The opener', 'First blood', 'The breakthrough', 'And the deadlock is broken'])
        elif mine == theirs:
            ctx = N.pick(r, ['Level!', 'Back on terms!', 'The equaliser!', 'All square again!'])
        elif mine == theirs + 1 and g['min'] >= 80:
            ctx = N.pick(r, ['Late drama!', 'Is that the winner?', 'Pandemonium!'])
        elif mine - theirs >= 3:
            ctx = N.pick(r, ['It\'s a rout.', 'Total control now.', 'This is a procession.'])
        elif mine < theirs:
            ctx = N.pick(r, ['A lifeline!', 'Game on!', 'Hope!'])
        else:
            ctx = N.pick(r, ['', 'Breathing space.', 'Momentum swings.'])
        kind = _kind(r, i)
        verb = N.pick(r, N.VERB[kind])
        tail = (' ' + N.pick(r, N.ASSIST).format(a=g['assist'])) if g.get('assist') and kind not in ('pen', 'fk') else ''
        lead = (ctx + ('' if ctx[-1] in '!.?' else ':') + ' ') if ctx else ''
        out.append("%d' - %s%s %s%s (%d-%d).%s" % (g['min'], lead, g['name'], verb, tail, nh, na, _shout(r, g['name'])))
        gh, ga = nh, na
    return out


def scene(home, away, name, seed, round_no=None):
    r = _r('mlsc', seed)
    return N.pick(r, ['Under the lights, %s welcomed %s with the stands already shaking.' % (name(home), name(away)),
                      'A wall of noise greeted the teams as %s and %s walked out.' % (name(home), name(away)),
                      'Sold out, flags everywhere: %s v %s had the feel of a big night from the first whistle.' % (name(home), name(away)),
                      'The rain fell, the flags waved and %s held its breath.' % name(home),
                      '%s against %s%s - and nobody needed reminding what was at stake.' % (name(home), name(away), (' in round %s' % round_no) if round_no else '')])


def verdict(home, away, hg, ag, name, seed):
    r = _r('mlvd', seed)
    w = home if hg > ag else away if ag > hg else None
    l = (away if w == home else home) if w else None
    d = abs(hg - ag)
    if w is None:
        return N.pick(r, ['Goalless, but never dull: every duel was a small war.', 'A tactical chess match with no checkmate.']) if hg == 0 else \
            N.pick(r, ['Honours even after a game that swung like a pendulum.', 'Neither side would blink. A point apiece.', 'A draw that felt like a story with the last page torn out.'])
    if d >= 3:
        return N.pick(r, ['%s were ruthless. %s will want to forget this one quickly.' % (name(w), name(l)), 'One-way traffic: %s at their imperious best.' % name(w),
                          'A statement win. The rest of the league will have noticed.'])
    if d == 1:
        return N.pick(r, ['Fine margins - and %s were on the right side of them.' % name(w), '%s survived the storm and took the points.' % name(w),
                          'Won on the edge of a knife. %s will not care how.' % name(w)])
    return N.pick(r, ['Comfortable in the end for %s.' % name(w), '%s did what big teams do: they found a way.' % name(w)])


def boss_line(coach, situation, seed):
    r = _r('mlbv', seed, coach, situation)
    last = (coach or '').split()[-1] if coach else ''
    bank = BOSS.get(last) or N.DEFAULT_BV
    return N.pick(r, bank.get(situation) or N.DEFAULT_BV[situation])


def player_line(name, situation, seed):
    r = _r('mlpv', seed, name)
    f = _fold(name)
    for k, d in N.PV.items():
        if k in f and d.get(situation):
            return N.pick(r, d[situation])
    return N.pick(r, N.GENERIC.get(situation) or N.GENERIC['score'])
