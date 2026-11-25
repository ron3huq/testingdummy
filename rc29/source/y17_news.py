"""RC29.17: the Y17 Champions League newsroom.

Rebuilt every matchday from the stored results (deterministic per season seed + matchday):
  report     commentary-style match report of your match and of the headline match (scene, goals minute by minute, verdict)
  interview  post-match voices: players and managers speak in their own voice (Ronaldo's certainty, Messi's few words, Zlatan's ego,
             Mourinho's needles, Klopp's heart, Simeone's war...)
  mindgames  the press conference before the big one: two managers, two quotes, one needle
  form       on fire / goal drought / breakout player
  duel       Messi v Ronaldo
  race       Golden Boot, title race, crisis, unbeaten runs, records
  season     awards night (Golden Boot, Ballon d'Or, champion)
"""
import zlib, random

import ml_cups as C


def _Y():
    import y17_league
    return y17_league


def _r(*parts):
    return random.Random(zlib.crc32(':'.join(str(p) for p in parts).encode()))


def pick(r, seq):
    return seq[int(r.random() * len(seq)) % len(seq)]


def _fold(n):
    return C._fold(n or '')


def _owner():
    return _Y()._owner()


def _pname(pid):
    o = _owner().get(pid)
    return o[1] if o else C._name(pid)


def _last(pid):
    return _Y()._last(_pname(pid))


def _nick(t):
    return _Y()._nick(t)


def _boss(t):
    return _Y().MANAGERS.get(t, 'the manager')


def _boss_last(t):
    b = _boss(t)
    return b.split()[-1] if b else 'the manager'


# ------------------------------------------------------------------ voices
# player voice: key (folded name fragment) -> situation -> lines
PV = {
    'cristiano ronaldo': {
        'score': ['I work every day to be the best. Tonight you saw why.', 'Goals? It is what I do. I was born for nights like this.',
                  'People talk, I answer on the pitch. Always.', 'Siiii! The fans deserve this. And I deserve it too, I work for it.',
                  'Records follow me. I do not chase them - they chase me.', 'I said before the game I would score. I keep my promises.'],
        'loss': ['If everyone had my level, maybe we would be top. I say it with respect.', 'I am angry. Good. Angry players win titles.',
                 'One bad night does not change history. Look at the numbers at the end.'],
        'rival': ['Messi? He does his job, I do mine. At the end of the season we count.', 'Comparisons are for journalists. I compare myself with me.',
                  'The Golden Boot is not a gift. You take it.'],
        'drought': ['Strikers have moments. Mine will come back - and when it comes, be careful.', 'I am not worried. You are worried. I am calm.'],
    },
    'lionel messi': {
        'score': ['The important thing is the team won.', 'I am happy. We played well together.', 'Goals come from the work of everybody.',
                  'I try to enjoy it. When you enjoy, things come.', 'It was a nice goal, yes. But the three points are what count.'],
        'loss': ['We have to improve. There is a lot of season left.', 'It hurts. We did not play like us.', 'We stay calm and keep working.'],
        'rival': ['I do not look at Cristiano. I look at my team.', 'Prizes are nice but the league is what matters to me.', 'I just want to win titles with this shirt.'],
        'drought': ['Sometimes the ball does not want to go in. It will come.', 'I do not think about goals. I think about winning.'],
    },
    'zlatan ibrahimovic': {
        'score': ['Zlatan does not score goals. Goals happen to Zlatan.', 'They asked me for a goal. I gave them art.', 'I am like wine - every season more expensive.',
                  'Defenders tonight will dream of me. Nightmares.', 'I did not come here to be king. I came here to be legend.'],
        'loss': ['Without Zlatan in form, it is football. With Zlatan, it is a show. Tonight was football.', 'I lose sometimes. Rarely. Tonight, rarely.'],
        'rival': ['Messi, Ronaldo... good players. But there is only one Zlatan.', 'The Ballon d\'Or without Zlatan is not a Ballon d\'Or.'],
        'drought': ['Zlatan does not have a drought. The goal is resting.'],
    },
    'neymar': {
        'score': ['Joy! Football is joy. I dance because I am happy.', 'I play like in the street in Brazil, and tonight it worked.',
                  'The fans are my energy. This goal is for them.'],
        'loss': ['A bad night. We will be back smiling.', 'They kicked a lot. I will not complain. Too much.'],
        'rival': ['One day the prize will be mine too. I am patient - a little.'],
        'drought': ['I am creating, the goals will come. I am not worried.'],
    },
    'luis suarez': {
        'score': ['I fight for every ball. Tonight it paid.', 'The defenders know me. They know I never stop.', 'For my family and for this shirt.'],
        'loss': ['I am furious. We must bite... in football terms!', 'We lost the battle, not the war.'],
        'rival': ['I want Leo to win everything. If I win something too, better.'],
        'drought': ['A striker without goals is hungry. I am very hungry.'],
    },
    'robert lewandowski': {
        'score': ['I prepare like a professional - diet, sleep, focus. The goals are the result.', 'My job is simple: be in the right place. Tonight I was.',
                  'The team gives me chances, I must finish. It is a deal.'],
        'loss': ['We were not sharp. We will analyse and be better.', 'I did not get the service. But I do not blame anybody.'],
        'rival': ['Everybody talks about two players. Maybe this year there are three.', 'The Golden Boot is open. I am in it.'],
        'drought': ['I trust my routine. The goals will come back.'],
    },
    'harry kane': {
        'score': ['I am just pleased to help the team. Great team performance.', 'I keep working hard on my finishing and it is paying off.',
                  'A big three points for the lads.'],
        'loss': ['Disappointing. We go again.', 'We have to learn from it and move on.'],
        'rival': ['It is special to be mentioned with those two. I want to keep pushing them.'],
        'drought': ['Strikers go through spells. I will keep getting in the box.'],
    },
    'mohamed salah': {
        'score': ['Alhamdulillah. I am happy for the team and the fans.', 'The crowd gives me something special. I want to give it back.',
                  'I want to break records here. Step by step.'],
        'loss': ['We go home, we rest, we come back stronger.'],
        'rival': ['They are legends. I just want my own story.'],
        'drought': ['I am patient. My time will come again.'],
    },
    'antoine griezmann': {
        'score': ['I celebrate like in Fortnite because I am happy!', 'Simeone asked us to suffer. We suffered, then we scored.'],
        'loss': ['It was hard, they defended very well. We must be calmer in front of goal.'],
        'rival': ['I want to be in that conversation. With Atlético, why not?'],
        'drought': ['I play for the team first. The goals will come.'],
    },
    'francesco totti': {
        'score': ['I have lived this club for twenty-five years. Every goal is like the first.', 'Rome is my home. Tonight Rome was smiling.'],
        'loss': ['We suffer together. That is what it means to be Romanista.'],
        'rival': ['Ballon d\'Or? I won the love of a city. It is enough.'],
        'drought': ['At my age, every goal is a gift. I wait for the next one.'],
    },
    'eden hazard': {
        'score': ['I just play. When I enjoy, I am dangerous.', 'Dribble, dribble, goal. Simple!'],
        'loss': ['We were not good. I was not good. Next game.'],
        'rival': ['Real Madrid? I am happy here. Today.'],
        'drought': ['I am creating more. The goals will come, I promise.'],
    },
    'sergio aguero': {
        'score': ['Gracias! The boys gave me great balls, I just put them in.', 'Every goal is like the first. I love it.'],
        'loss': ['Bad day. We are a good team, we will recover.'],
        'rival': ['Leo is my brother, but on the pitch I want the Boot.'],
        'drought': ['Kun is coming back, do not worry!'],
    },
    'kevin de bruyne': {
        'score': ['We played the way we wanted to. That is the most important thing.'],
        'assist': ['A pass is like a goal for me. Maybe better.', 'I saw the run and the space. After that it is easy.'],
        'loss': ['Honestly we were bad. No excuses.'],
        'rival': ['Assists don\'t win you the Ballon d\'Or. I know that. I still love them.'],
        'drought': ['My job is to make goals, not only score them.'],
    },
    'sergio ramos': {
        'score': ['Minute 90? That is my time. Everyone knows.', 'A defender who scores is a happy defender. A captain who scores - even more.'],
        'loss': ['This shirt does not accept excuses. We will react.'],
        'rival': ['I do not talk about other clubs. I talk with my legs.'],
        'drought': [],
    },
    'gianluigi buffon': {
        'score': ['A clean sheet is a little poem. Tonight we wrote one.'],
        'loss': ['At forty you learn: defeat is a teacher. A strict one.'],
        'rival': [],
        'drought': [],
    },
}
GENERIC = {
    'score': ['It is a dream to score on this stage.', 'I just tried to stay calm and hit the target.', 'The ball fell to me and I did not think - I just hit it.',
              'For my family, watching at home.', 'We worked all week for this. I am so proud of the boys.', 'I have been waiting for this moment.'],
    'loss': ['We have to look at ourselves. No excuses.', 'It is a hard one to take. We wanted more.', 'We must stay together now.'],
    'rival': ['I do not think about prizes. I think about the next game.'],
    'drought': ['I keep working. It will turn.'],
    'assist': ['Seeing the ball go in after your pass - it is the same feeling as scoring.', 'I just looked up and he was there.'],
}

# manager voice: surname -> situation -> lines
BV = {
    'Zidane': {'win': ['I am happy, the players were fantastic. Always calm, always together.', 'We suffered a bit, but this is football. Three points.'],
               'loss': ['It is not a drama. We lost a match, not the league.', 'I take responsibility. Tomorrow we work.'],
               'draw': ['A point is a point. We continue.'],
               'preview': ['I respect every opponent. But we play to win - always.', 'My players know these matches. They do not need speeches.'],
               'jab': ['I do not answer that. I smile and I work.']},
    'Enrique': {'win': ['Good. Very good. Next question.', 'We were brave and we were superior. That is all.'],
                'loss': ['I am not going to give you a headline. We lost. We were worse.', 'You want drama. I give you analysis: we were not good enough.'],
                'draw': ['Not enough for this club. Never enough.'],
                'preview': ['We will go to attack. If you want a defensive coach, ask someone else.', 'Pressure? Pressure is for other jobs. We play football.'],
                'jab': ['I do not read what others say. I prefer cycling.']},
    'Ancelotti': {'win': ['The team was compact, balanced. I am very satisfied.', 'Quiet night, good result. I like quiet nights.'],
                  'loss': ['Calm. We were not at our level. We will be.', 'A small problem. We will fix it, piano piano.'],
                  'draw': ['A draw away is not a bad result. A draw at home - we must do better.'],
                  'preview': ['Big match, big players. I trust my players.', 'I raise my eyebrow only when it is necessary. Saturday, maybe.'],
                  'jab': ['I have too much experience to answer this. *raises eyebrow*']},
    'Allegri': {'win': ['Corto muso - we won by a nose. The nose is enough.', 'Football is simple. People make it complicated.'],
                'loss': ['We made mistakes we do not normally make. It happens.', 'The league is not won in one night, and not lost.'],
                'draw': ['A balanced game. At this level a point has value.'],
                'preview': ['You win championships with balance, not with poetry.', 'They play beautiful. We play to win. Let us see.'],
                'jab': ['Some coaches love philosophy. I love the table.']},
    'Simeone': {'win': ['Partido a partido. Tonight the partido was ours.', 'My players left their soul on the pitch. That is Atlético.'],
                'loss': ['We will rise. This club always rises.', 'When you lose, you look at the mirror. Tomorrow we look at it together.'],
                'draw': ['We competed. Always we compete.'],
                'preview': ['We go there like warriors. Eleven warriors and forty thousand behind.', 'Nobody believes in us? Perfect. We prefer it.'],
                'jab': ['They have the money. We have the heart.']},
    'Emery': {'win': ['Fantastic, the players did all the work we prepared. Very good.', 'Intensity, intensity, intensity! This is the way.'],
              'loss': ['We need to analyse, the details, every detail.', 'I am sad for the supporters. We will improve.'],
              'draw': ['Positive in some moments, not in others. Balance.'],
              'preview': ['I watched every video of them. Every one. Three times.'],
              'jab': ['Respect for everybody. But we are ready.']},
    'Guardiola': {'win': ['The way we played with the ball - incredible. Incredible.', 'We controlled the spaces. When we control the spaces, we are a team.'],
                  'loss': ['They were better in the transitions. Congratulations to them.', 'I am not a genius. Tonight it is clear.'],
                  'draw': ['We created a lot. Sometimes football does not reward you.'],
                  'preview': ['They are one of the best teams in the world. In the world!', 'We will try to have the ball. If we don\'t have it, we suffer.'],
                  'jab': ['Everybody has an opinion. I respect all the opinions. Even the wrong ones.']},
    'Klopp': {'win': ['Boom! What a night. The boys were absolutely outstanding.', 'Heavy metal football tonight. I loved every second.'],
              'loss': ['It hurts, and it should hurt. That is the deal in football.', 'I will not lie, we were not good. We will be.'],
              'draw': ['A point, a fight, a story. I take it.'],
              'preview': ['Anfield on a night like this - you cannot describe it, you have to feel it.', 'We are not here to be nice. We are here to be annoying to play against.'],
              'jab': ['If he wants to talk, he can talk. I prefer my players talking on the pitch.']},
    'Conte': {'win': ['Great desire, great will. I want this desire in every game!', 'We worked like animals this week. This is the result.'],
              'loss': ['I am very angry. Very angry. We must work more.', 'This is not acceptable for this club.'],
              'draw': ['We have to be more clinical. More clinical!'],
              'preview': ['In my career I have learned one thing: you must suffer to win.', 'We go to fight. To fight!'],
              'jab': ['I prefer to work in silence. Other people prefer to talk.']},
    'Pochettino': {'win': ['I am so proud. The project is growing - you can see it.', 'Young players, big character. Very pleased.'],
                   'loss': ['We need to keep believing. The process continues.', 'Today was a lesson. Good teams learn.'],
                   'draw': ['A fair result. We showed our identity.'],
                   'preview': ['We do not fear anybody. We respect, but we do not fear.', 'We are dreamers. But dreams need work.'],
                   'jab': ['We do not have their budget. We have our ideas.']},
    'Spalletti': {'win': ['The team had brains and legs tonight. Both!', 'When Roma plays like this, the city sings.'],
                  'loss': ['I am the first one responsible. And the last.', 'We gave away too much. A gift, a gift!'],
                  'draw': ['We had the match in our hand. Then we opened the hand.'],
                  'preview': ['They are a great team. We are Roma. It is enough to fight.'],
                  'jab': ['I do not do politics. I do football.']},
    'Mourinho': {'win': ['I am not going to speak much. The result speaks.', 'Some people were trying to write my obituary. Write something else.',
                         'Three points. Three titles in my career here at this stadium? No - three points. Respect.'],
                 'loss': ['If I speak, I am in big trouble. I prefer not to be in big trouble.', 'The referee... no. I say nothing. Nothing.',
                          'Football heritage - some people do not understand what it means.'],
                 'draw': ['We parked the bus? We parked two buses. And we nearly won.'],
                 'preview': ['I respect him, but I have more titles than him. That is not arrogance - it is a fact.', 'Pressure? I am the Special One, I eat pressure for breakfast.'],
                 'jab': ['He is a specialist in failure. I am not. Next question.', 'Some coaches want to be philosophers. I want to win.']},
}
DEFAULT_BV = {'win': ['A deserved win. The players were excellent.'], 'loss': ['Not our night. We go again.'], 'draw': ['A fair result.'],
              'preview': ['A big game. We are ready.'], 'jab': ['No comment.']}


def _pvoice(r, pid, situation):
    n = _fold(_pname(pid)).replace('-', ' ')
    for k, d in PV.items():
        if k in n and d.get(situation):
            return pick(r, d[situation])
    return pick(r, GENERIC.get(situation) or GENERIC['score'])


def _bvoice(r, team, situation):
    d = BV.get(_boss_last(team), DEFAULT_BV)
    return pick(r, d.get(situation) or DEFAULT_BV[situation])


# ------------------------------------------------------------------ commentary
VERB = {
    'open': ['slots it home', 'finishes coolly', 'fires low into the corner', 'drills it past the keeper', 'side-foots it in', 'smashes it into the roof of the net',
             'dinks it over the keeper', 'rolls it into the empty net', 'lashes it in at the near post', 'bends it into the far corner'],
    'header': ['rises highest and heads it in', 'thumps a header past the keeper', 'glances a header into the corner', 'meets the cross with a bullet header'],
    'pen': ['converts from the spot', 'sends the keeper the wrong way from twelve yards', 'buries the penalty', 'rolls the penalty in, ice in the veins'],
    'fk': ['curls a free kick over the wall and in', 'whips the free kick into the top corner', 'bends a sublime free kick beyond everybody'],
    'long': ['unleashes a thunderbolt from 25 yards', 'tries his luck from distance - and it flies in', 'hits a screamer from outside the box', 'curls one in from the edge of the area'],
}
SHOUT = {
    'lionel messi': ['Messi! Again! What else can you say about this man?', 'Leo Messi - from another planet!', 'Of course it is Messi. It is always Messi!'],
    'cristiano ronaldo': ['Ronaldo! And there\'s the celebration - SIIII!', 'Cristiano! The machine never stops!', 'Ronaldo, the man for the big moments!'],
    'zlatan ibrahimovic': ['Zlatan! Absurd! Only he tries that!'],
    'neymar': ['Neymar! Samba magic!'],
    'luis suarez': ['Suárez! The pistolero strikes!'],
    'sergio ramos': ['Ramos! Of course it\'s Ramos, late on!'],
    'harry kane': ['Kane! He just doesn\'t miss!'],
    'mohamed salah': ['Salah! The Egyptian King!'],
    'francesco totti': ['Totti! The eternal captain!'],
    'robert lewandowski': ['Lewandowski! Clinical. Ruthless.'],
}
ASSIST = ['after a lovely ball from {a}', 'set up by {a}', 'from {a}\'s pass', 'on the end of {a}\'s cross', 'after {a} picked him out',
          'from a wonderful through ball by {a}', 'after {a} did all the hard work']


def _goal_line(r, ev, h, a, sc_before, team_names):
    mn, side, sc, ast, kind = ev
    who = _pname(sc)
    verb = pick(r, VERB.get(kind, VERB['open']))
    ctx = ''
    gh, ga = sc_before
    nh, na = (gh + 1, ga) if side == 0 else (gh, ga + 1)
    mine, theirs = (nh, na) if side == 0 else (na, nh)
    if gh == ga == 0:
        ctx = pick(r, ['The deadlock is broken', 'First blood', 'The opener', 'And the breakthrough'])
    elif mine == theirs:
        ctx = pick(r, ['Level!', 'Back on terms!', 'The equaliser!', 'All square again!'])
    elif mine == theirs + 1 and mn >= 80:
        ctx = pick(r, ['Late drama!', 'Is that the winner?', 'Heartbreak for one side, delirium for the other!'])
    elif mine - theirs >= 3:
        ctx = pick(r, ['It is a rout.', 'This is becoming a procession.', 'Total control now.'])
    elif mine > theirs:
        ctx = pick(r, ['', 'Breathing space.', 'Momentum swings.', ''])
    else:
        ctx = pick(r, ['A lifeline!', 'Game on!', 'Hope!'])
    tail = ' ' + pick(r, ASSIST).format(a=_pname(ast)) if ast else ''
    shout = ''
    fold = _fold(who).replace('-', ' ')
    for k, lines in SHOUT.items():
        if k in fold and r.random() < 0.7:
            shout = ' "' + pick(r, lines) + '"'
    lead = ''
    if ctx:
        lead = ctx + ('' if ctx[-1] in '!.?' else ':') + ' '
    return "%d' - %s%s %s%s (%d-%d).%s" % (mn, lead, who, verb, tail, nh, na, shout), (nh, na)


def _scene(r, st, rd, m, tb_before):
    Y = _Y()
    h, a = m['h'], m['a']
    pos = {x['team']: x for x in tb_before}
    derby = Y.RIVALS.get(frozenset((h, a)))
    venue = Y.STADIUM.get(h, 'a packed stadium')
    opens = [
        'Under the lights of %s, %s welcomed %s.' % (venue, _nick(h), _nick(a)),
        'A wall of noise greeted the teams at %s.' % venue,
        'Matchday %d, and %s was sold out long before kick-off.' % (rd + 1, venue),
        'Everything about the build-up said this one would matter.',
        'The rain fell, the flags waved and %s held its breath.' % venue,
    ]
    s = pick(r, opens)
    if derby:
        s += ' ' + pick(r, ['This was %s - no friendly words before, none expected after.' % derby,
                            '%s: the kind of fixture that stops a city.' % (derby[0].upper() + derby[1:]),
                            'It was %s, and nobody needed reminding.' % derby])
    if rd > 0:
        ph, pa = pos[h]['pos'], pos[a]['pos']
        if ph <= 3 and pa <= 3:
            s += ' Top-three clash: %s %s, %s %s.' % (_nick(h), _ord(ph), _nick(a), _ord(pa))
        elif ph >= 10 or pa >= 10:
            low = h if ph >= pa else a
            s += ' For %s, down in %s, the pressure on %s was impossible to ignore.' % (_nick(low), _ord(pos[low]['pos']), _boss(low))
    return s


def _ord(n):
    return '%d%s' % (n, 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def _verdict(r, m):
    h, a, hg, ag = m['h'], m['a'], m['hg'], m['ag']
    w = h if hg > ag else a if ag > hg else None
    l = a if w == h else h if w == a else None
    diff = abs(hg - ag)
    if w is None and hg == 0:
        return pick(r, ['A tactical chess match with no checkmate. Two defences, one point each, plenty of respect.',
                        'Goalless, but never dull: every duel was a small war.'])
    if w is None:
        return pick(r, ['A point apiece, and the feeling that both could have had all three.', 'Honours even after a game that swung like a pendulum.',
                        'Neither side would blink. A draw that felt like a story with the last page torn out.'])
    if diff >= 3:
        return pick(r, ['%s were ruthless. %s will want to forget this one quickly.' % (_nick(w), _nick(l)),
                        'A statement win. The rest of the league will have noticed.', 'One-way traffic: %s at their imperious best.' % _nick(w)])
    if diff == 1:
        return pick(r, ['Fine margins - and %s were on the right side of them.' % _nick(w), 'Won on the edge of a knife. %s will not care how.' % _nick(w),
                        '%s survived the storm and took the points.' % _nick(w)])
    return pick(r, ['Comfortable in the end for %s.' % _nick(w), '%s did what big teams do: they found a way.' % _nick(w)])


def report(st, rd, i, tb_before=None):
    """Full commentary report for match (rd, i)."""
    Y = _Y()
    m = st['fx'][rd][i]
    r = _r('y17rep', st['seed'], rd, i)
    if tb_before is None:
        tb_before = Y.table(st, upto=rd)
    paras = [_scene(r, st, rd, m, tb_before)]
    lines, score = [], (0, 0)
    for ev in m.get('ev', []):
        line, score = _goal_line(r, ev, m['h'], m['a'], score, None)
        lines.append(line)
    if not lines:
        paras.append(pick(r, ['Chances came and went. The woodwork rattled, the keepers were heroes, and the net stayed untouched.',
                              'Both keepers produced saves worthy of a highlights reel. Nobody could find the final touch.']))
    paras.append(_verdict(r, m))
    mo = m.get('motm')
    voices = []
    if mo:
        team = _owner().get(mo, (None,))[0]
        won = (team == m['h'] and m['hg'] > m['ag']) or (team == m['a'] and m['ag'] > m['hg'])
        g = sum(1 for e in m.get('ev', []) if e[2] == mo)
        voices.append({'who': _pname(mo), 'pid': mo, 'role': 'Player of the match', 'text': _pvoice(r, mo, 'score' if (g or won) else 'loss')})
    w = m['h'] if m['hg'] > m['ag'] else m['a'] if m['ag'] > m['hg'] else None
    for t in (m['h'], m['a']):
        sit = 'draw' if w is None else 'win' if t == w else 'loss'
        voices.append({'who': _boss(t), 'team': t, 'role': _nick(t) + ' manager', 'text': _bvoice(r, t, sit)})
    return {'paras': paras, 'timeline': lines, 'voices': voices}


# ------------------------------------------------------------------ helpers over the season
def _streaks(st, upto):
    """pid -> (consecutive matchdays scoring, consecutive matchdays without a goal) up to matchday `upto` (inclusive)."""
    own = _owner()
    on, off = {}, {}
    for rd in range(upto + 1):
        scored = set()
        for m in st['fx'][rd]:
            for e in m.get('ev', []):
                scored.add(e[2])
        for pid in own:
            if pid in scored:
                on[pid] = on.get(pid, 0) + 1
                off[pid] = 0
            else:
                on[pid] = 0
                off[pid] = off.get(pid, 0) + 1
    return on, off


def _team_run(st, team, upto):
    res = []
    for rd in range(upto + 1):
        for m in st['fx'][rd]:
            if team in (m['h'], m['a']) and m['hg'] is not None:
                gf, ga = (m['hg'], m['ag']) if m['h'] == team else (m['ag'], m['hg'])
                res.append('W' if gf > ga else 'L' if gf < ga else 'D')
    return res


def _add(st, item):
    st['nid'] = st.get('nid', 0) + 1
    item.setdefault('id', '%d-%d-%s-%d' % (st['season'], item.get('round', 0), item.get('kind', 'x'), st['nid']))
    st['news'].insert(0, item)
    del st['news'][80:]


# ------------------------------------------------------------------ preseason
def preseason(st):
    Y = _Y()
    r = _r('y17pre', st['seed'])
    me = st['team']
    horse = st.get('horse')
    br = st.get('breakout', [])
    _add(st, {'round': 0, 'kind': 'season', 'tag': 'Season preview', 'team': me,
              'title': pick(r, ['Twelve giants, thirty-three matchdays, one crown', 'The greatest league never played begins now',
                                'Season %d: the gods of 2017 return' % st['season']]),
              'lead': 'Barcelona and Real Madrid start as favourites. Bayern, Juventus and Liverpool lurk. Every pair meets three times.',
              'paras': ['%s take charge of %s with one aim: finish above eleven of the best sides of their generation.' % ('You', Y._tname(me)),
                        pick(r, ['The bookmakers have it as a two-horse race. The bookmakers have been wrong before.',
                                 'Messi or Ronaldo? Barça or Madrid? Or does someone crash the party?']),
                        'Dark horse tip from the press box: %s. "Nobody is talking about them," one scout said. "That is exactly why they are dangerous."' % Y._tname(horse) if horse else ''],
              'quote': {'who': _boss(me), 'team': me, 'text': _bvoice(r, me, 'preview')}})
    if br:
        pid = br[0]
        _add(st, {'round': 0, 'kind': 'form', 'tag': 'One to watch', 'pid': pid, 'team': _owner()[pid][0],
                  'title': '%s: "This is my year"' % _pname(pid),
                  'lead': 'Overshadowed for too long, the %s man insists he is ready to step into the light.' % _nick(_owner()[pid][0]),
                  'paras': ['Training ground whispers say he has never looked sharper.', 'Pre-season: goals in every friendly. Coincidence, or a warning?'],
                  'quote': {'who': _pname(pid), 'pid': pid, 'text': pick(r, ['I am tired of waiting. This season, people will know my name.',
                                                                             'Everybody talks about the stars. Fine. Let them talk. I will play.'])}})


# ------------------------------------------------------------------ matchday
def round_news(st, rd, tb_before):
    Y = _Y()
    r = _r('y17news', st['seed'], rd)
    me = st['team']
    tb = Y.table(st)
    pos = {x['team']: x for x in tb}
    stats = Y.player_stats(st)
    matches = st['fx'][rd]

    # 1) your match - full report
    mi = next(i for i, m in enumerate(matches) if me in (m['h'], m['a']))
    m = matches[mi]
    rep = report(st, rd, mi, tb_before)
    gf, ga = (m['hg'], m['ag']) if m['h'] == me else (m['ag'], m['hg'])
    opp = m['a'] if m['h'] == me else m['h']
    res = 'win' if gf > ga else 'loss' if gf < ga else 'draw'
    title = {
        'win': [ '%s %d-%d %s: %s' % (_nick(m['h']), m['hg'], m['ag'], _nick(m['a']), pick(r, ['statement made', 'job done', 'the march goes on', 'what a night'])),
                 '%s too strong for %s' % (_nick(me), _nick(opp)), '%s light up %s' % (_nick(me), Y.STADIUM.get(m['h'], 'the stadium'))],
        'loss': ['%s stun %s' % (_nick(opp), _nick(me)), 'Night to forget for %s' % _nick(me), '%s %d-%d %s: alarm bells' % (_nick(m['h']), m['hg'], m['ag'], _nick(m['a']))],
        'draw': ['Stalemate: %s %d-%d %s' % (_nick(m['h']), m['hg'], m['ag'], _nick(m['a'])), 'Spoils shared between %s and %s' % (_nick(m['h']), _nick(m['a']))],
    }[res]
    _add(st, {'round': rd + 1, 'kind': 'report', 'tag': 'Your match', 'teams': [m['h'], m['a']], 'score': [m['hg'], m['ag']], 'ref': [rd + 1, mi],
              'title': pick(r, title), 'lead': rep['paras'][-1], 'paras': rep['paras'][:-1] + rep['timeline'], 'voices': rep['voices'],
              'pid': m.get('motm'), 'team': me})

    # 2) the headline match elsewhere
    def weight(i, x):
        if i == mi:
            return -1
        w = 0
        if frozenset((x['h'], x['a'])) in Y.RIVALS:
            w += 3
        w += max(0, 7 - pos[x['h']]['pos'] - pos[x['a']]['pos'] // 2) * 0.4
        w += abs(x['hg'] - x['ag']) * 0.6 + (x['hg'] + x['ag']) * 0.3
        return w
    hi = max(range(len(matches)), key=lambda i: weight(i, matches[i]))
    hm = matches[hi]
    hrep = report(st, rd, hi, tb_before)
    derby = Y.RIVALS.get(frozenset((hm['h'], hm['a'])))
    _add(st, {'round': rd + 1, 'kind': 'report', 'tag': derby or 'Match of the day', 'teams': [hm['h'], hm['a']], 'score': [hm['hg'], hm['ag']], 'ref': [rd + 1, hi],
              'title': '%s %d-%d %s%s' % (_nick(hm['h']), hm['hg'], hm['ag'], _nick(hm['a']), (' - ' + pick(r, ['drama', 'chaos', 'a classic', 'what a game'])) if hm['hg'] + hm['ag'] >= 4 else ''),
              'lead': hrep['paras'][-1], 'paras': hrep['paras'][:-1] + hrep['timeline'], 'voices': hrep['voices'], 'pid': hm.get('motm'), 'team': hm['h']})

    # 3) hat-tricks
    for i, x in enumerate(matches):
        cnt = {}
        for e in x.get('ev', []):
            cnt[e[2]] = cnt.get(e[2], 0) + 1
        for pid, n in cnt.items():
            if n >= 3:
                t = _owner().get(pid, (None,))[0]
                word = {3: 'hat-trick', 4: 'four-goal show', 5: 'five-goal masterpiece'}.get(n, '%d-goal night' % n)
                _add(st, {'round': rd + 1, 'kind': 'form', 'tag': 'Hat-trick hero', 'pid': pid, 'team': t,
                          'title': pick(r, ['%s %s sinks %s' % (_pname(pid), word, _nick(x['a'] if t == x['h'] else x['h'])),
                                            'Match ball for %s' % _pname(pid), '%s: the %s nobody saw coming' % (_last(pid), word) if not Y._star(_pname(pid)) else '%s does it again: %s' % (_last(pid), word)]),
                          'lead': '%s now has %d league goals this season.' % (_pname(pid), stats['g'].get(pid, 0)),
                          'paras': [pick(r, ['He walked off clutching the match ball, the crowd chanting his name.', 'Three goals, three different ways. A complete striker\'s performance.',
                                             'Defenders will be seeing him in their sleep.'])],
                          'quote': {'who': _pname(pid), 'pid': pid, 'text': _pvoice(r, pid, 'score')}})

    # 4) Golden Boot / Messi-Ronaldo duel
    boot_now = Y._rank(stats['g'], 3)
    prev_stats = None
    if boot_now:
        lead = boot_now[0]
        st_prev = dict(st)
        prev = {}
        for x in st['fx'][:rd]:
            for mm in x:
                for e in mm.get('ev', []):
                    prev[e[2]] = prev.get(e[2], 0) + 1
        prev_lead = max(prev.items(), key=lambda kv: kv[1])[0] if prev else None
        if prev_lead and lead['pid'] != prev_lead and lead['n'] > prev.get(prev_lead, 0):
            _add(st, {'round': rd + 1, 'kind': 'race', 'tag': 'Golden Boot', 'pid': lead['pid'], 'team': lead['team'],
                      'title': '%s seizes the Golden Boot lead' % lead['name'],
                      'lead': '%d goals - one clear of %s.' % (lead['n'], _pname(prev_lead)) if lead['n'] - prev.get(prev_lead, 0) == 1 else '%d goals and counting.' % lead['n'],
                      'paras': [pick(r, ['The race has a new leader, and the old one will not like it.', 'A new name at the top of the scoring charts. The chase is on.'])],
                      'quote': {'who': lead['name'], 'pid': lead['pid'], 'text': _pvoice(r, lead['pid'], 'rival')}})
        for x in boot_now:
            for mark in (10, 20, 30, 40, 50):
                if x['n'] >= mark > prev.get(x['pid'], 0):
                    _add(st, {'round': rd + 1, 'kind': 'race', 'tag': 'Milestone', 'pid': x['pid'], 'team': x['team'],
                              'title': '%d up for %s' % (mark, x['name']), 'lead': 'Matchday %d of %d and %s already has %d league goals.' % (rd + 1, len(st['fx']), _last(x['pid']), x['n']),
                              'paras': [pick(r, ['At this rate, the record books are in danger.', 'The numbers are almost absurd.', 'Some players dream of this tally in a career.'])]})
    own = _owner()
    ids = {k: next((p for p, o in own.items() if _fold(o[1]) == k), None) for k in ('lionel messi', 'cristiano ronaldo')}
    mpid, rpid = ids['lionel messi'], ids['cristiano ronaldo']
    if mpid and rpid and (rd % 4 == 3 or rd == len(st['fx']) - 1):
        gm, gr = stats['g'].get(mpid, 0), stats['g'].get(rpid, 0)
        am, ar = stats['a'].get(mpid, 0), stats['a'].get(rpid, 0)
        lead_pid = mpid if gm > gr else rpid if gr > gm else None
        if lead_pid:
            title = pick(r, ['%s edges ahead in the eternal duel' % _last(lead_pid), 'Messi %d, Ronaldo %d: the war of numbers' % (gm, gr),
                             'Two kings, one crown: %s leads' % _last(lead_pid)])
        else:
            title = pick(r, ['Messi %d, Ronaldo %d: dead heat' % (gm, gr), 'Neck and neck: the duel that never ends'])
        _add(st, {'round': rd + 1, 'kind': 'duel', 'tag': 'Messi v Ronaldo', 'pid': lead_pid or mpid, 'pids': [mpid, rpid],
                  'title': title, 'lead': 'Goals %d-%d, assists %d-%d after %d matchdays.' % (gm, gr, am, ar, rd + 1),
                  'paras': [pick(r, ['One plays like water, the other like fire. Both burn the league down.',
                                     'Every Messi goal is answered by a Ronaldo goal. It is a conversation conducted in the back of the net.',
                                     'Pundits split down the middle. Bars split down the middle. Families, too.']),
                            pick(r, ['Messi has the touch of a poet; Ronaldo, the will of a machine.', 'Ronaldo counts the goals. Messi counts the passes. The league counts both.'])],
                  'voices': [{'who': own[mpid][1], 'pid': mpid, 'role': _nick(own[mpid][0]), 'text': _pvoice(r, mpid, 'rival')},
                             {'who': own[rpid][1], 'pid': rpid, 'role': _nick(own[rpid][0]), 'text': _pvoice(r, rpid, 'rival')}]})

    # 5) form: on fire / drought / breakout
    on, off = _streaks(st, rd)
    hot = [(pid, n) for pid, n in on.items() if n in (4, 6, 8, 10)]
    if hot:
        pid, n = max(hot, key=lambda x: (x[1], stats['g'].get(x[0], 0)))
        _add(st, {'round': rd + 1, 'kind': 'form', 'tag': 'On fire', 'pid': pid, 'team': own[pid][0],
                  'title': pick(r, ['%s cannot stop scoring' % _pname(pid), '%d matchdays, %d in a row: %s is on fire' % (n, n, _last(pid)), 'Unstoppable %s' % _last(pid)]),
                  'lead': 'Scored in each of his last %d matches - %d league goals in total.' % (n, stats['g'].get(pid, 0)),
                  'paras': [pick(r, ['Confidence is a strange drug. Right now he is high on it.', 'Every touch turns to gold.', 'Defenders have tried everything. Nothing works.'])],
                  'quote': {'who': _pname(pid), 'pid': pid, 'text': _pvoice(r, pid, 'score')}})
    cold = [(pid, n) for pid, n in off.items() if n in (5, 7, 9) and Y._star(own[pid][1]) and Y._star(own[pid][1])[0] >= 0.2]
    if cold:
        pid, n = max(cold, key=lambda x: Y._star(own[x[0]][1])[0])
        t = own[pid][0]
        _add(st, {'round': rd + 1, 'kind': 'form', 'tag': 'Drought', 'pid': pid, 'team': t,
                  'title': pick(r, ['Where have the goals gone, %s?' % _last(pid), '%s: %d games without a goal' % (_pname(pid), n), 'Crisis of confidence for %s?' % _last(pid)]),
                  'lead': '%d matchdays and counting without a league goal.' % n,
                  'paras': [pick(r, ['The whistles have started. Quietly, for now.', 'He snatched at one chance, blazed another over. The shoulders dropped.']),
                            '%s defended him: "%s"' % (_boss(t), pick(r, ['He is our best player. Goals are a matter of time.', 'I would play him tomorrow, and the day after.', 'I do not worry. He will explode.']))],
                  'quote': {'who': _pname(pid), 'pid': pid, 'text': _pvoice(r, pid, 'drought')}})
    for pid in st.get('breakout', []):
        g = stats['g'].get(pid, 0)
        prevg = g - sum(1 for mm in matches for e in mm.get('ev', []) if e[2] == pid)
        for mark in (5, 10, 15, 20):
            if g >= mark > prevg:
                _add(st, {'round': rd + 1, 'kind': 'form', 'tag': 'Breakout', 'pid': pid, 'team': own[pid][0],
                          'title': pick(r, ['%s: the surprise of the season' % _pname(pid), 'Nobody saw %s coming' % _last(pid), '%d goals - who is %s?' % (g, _last(pid))]),
                          'lead': '%d league goals from a man most expected to watch from the bench.' % g,
                          'paras': [pick(r, ['Stars get the headlines. He gets the goals.', 'A season ago he was a name on a team sheet. Now he is the name.'])],
                          'quote': {'who': _pname(pid), 'pid': pid, 'text': pick(r, ['I always believed. Now everyone believes.', 'I do not care about the big names. I care about the next goal.'])}})

    # 6) crisis / runs / title race
    for t in [x['team'] for x in tb]:
        run = _team_run(st, t, rd)
        if len(run) >= 3 and run[-3:] == ['L', 'L', 'L'] and (len(run) < 4 or run[-4] != 'L'):
            _add(st, {'round': rd + 1, 'kind': 'drama', 'tag': 'Crisis', 'team': t,
                      'title': pick(r, ['Crisis at %s: three defeats in a row' % _nick(t), '%s under fire' % _boss(t), 'Dressing-room unrest at %s?' % _nick(t)]),
                      'lead': '%s, %s, and %d points from the top.' % (_nick(t), _ord(pos[t]['pos']), tb[0]['pts'] - pos[t]['pts']),
                      'paras': [pick(r, ['Sources describe a tense training session, with raised voices.', 'The board has not commented. The fans have - loudly.',
                                         'Body language tells its own story: heads down, arms folded.'])],
                      'quote': {'who': _boss(t), 'team': t, 'text': _bvoice(r, t, 'loss')}})
        unbeaten = 0
        for x in reversed(run):
            if x == 'L':
                break
            unbeaten += 1
        if unbeaten in (8, 12, 16, 20) and len(run) == rd + 1:
            _add(st, {'round': rd + 1, 'kind': 'race', 'tag': 'Unbeaten', 'team': t,
                      'title': '%s: %d without defeat' % (_nick(t), unbeaten), 'lead': 'The run goes on - can anybody stop them?',
                      'paras': [pick(r, ['Momentum is the most dangerous weapon in football.', 'Every week a new hero, the same result.'])],
                      'quote': {'who': _boss(t), 'team': t, 'text': _bvoice(r, t, 'win')}})
    if rd >= len(st['fx']) * 2 // 3 and len(tb) > 1:
        gap = tb[0]['pts'] - tb[1]['pts']
        left = len(st['fx']) - (rd + 1)
        if gap > left * 3:
            if not any(n.get('kind') == 'champion' for n in st['news']):
                c = tb[0]['team']
                _add(st, {'round': rd + 1, 'kind': 'champion', 'tag': 'Champions', 'team': c,
                          'title': '%s are champions!' % Y._tname(c), 'lead': 'Crowned with %d matchday%s to spare.' % (left, '' if left == 1 else 's'),
                          'paras': [pick(r, ['The party started on the pitch and spilled into the streets.', 'Champagne, tears and a trophy lifted to the sky.'])],
                          'quote': {'who': _boss(c), 'team': c, 'text': pick(r, ['This is for the fans who suffered with us. Today we celebrate together!',
                                                                                 'I am so proud of these players. They are champions - forever.'])}})
        elif rd % 3 == 0 or rd >= 29:
            a_, b_ = tb[0]['team'], tb[1]['team']
            _add(st, {'round': rd + 1, 'kind': 'race', 'tag': 'Title race', 'teams': [a_, b_], 'team': a_,
                      'title': pick(r, ['%s v %s: %d point%s in it' % (_nick(a_), _nick(b_), gap, '' if gap == 1 else 's'), 'The run-in: nerves of steel required',
                                        '%d to play, %d between them' % (left, gap)]),
                      'lead': '%s %d pts, %s %d pts. %d matchdays left.' % (_nick(a_), tb[0]['pts'], _nick(b_), tb[1]['pts'], left),
                      'paras': [pick(r, ['Every slip now is fatal.', 'The title will be decided by nerve as much as talent.', 'One bad afternoon could undo a season.'])],
                      'voices': [{'who': _boss(a_), 'team': a_, 'role': _nick(a_), 'text': _bvoice(r, a_, 'preview')},
                                 {'who': _boss(b_), 'team': b_, 'role': _nick(b_), 'text': _bvoice(r, b_, 'jab')}]})

    # 7) mind games before the next big match
    if rd + 1 < len(st['fx']):
        nxt = st['fx'][rd + 1]

        def bigness(x):
            w = 4 if frozenset((x['h'], x['a'])) in Y.RIVALS else 0
            return w + max(0, 8 - pos[x['h']]['pos'] - pos[x['a']]['pos']) * 0.5
        bx = max(nxt, key=bigness)
        if bigness(bx) >= 3:
            h, a = bx['h'], bx['a']
            derby = Y.RIVALS.get(frozenset((h, a)))
            _add(st, {'round': rd + 1, 'kind': 'mindgames', 'tag': 'Press conference', 'teams': [h, a], 'team': h,
                      'title': pick(r, ['%s fires the first shot before %s' % (_boss(a), derby or 'the big one'), 'War of words before %s v %s' % (_nick(h), _nick(a)),
                                        '%s: "%s"' % (_boss_last(h), _bvoice(r, h, 'preview')[:60].rstrip('.') + ('...' if len(_bvoice(r, h, 'preview')) > 60 else ''))]),
                      'lead': 'Next up: %s v %s at %s. The talking has already started.' % (_nick(h), _nick(a), Y.STADIUM.get(h, 'home')),
                      'paras': [pick(r, ['Tickets: gone in eleven minutes. Tension: rising by the hour.', 'Both camps say all the right things. Neither believes a word of the other.'])],
                      'voices': [{'who': _boss(h), 'team': h, 'role': _nick(h) + ' manager', 'text': _bvoice(r, h, 'preview')},
                                 {'who': _boss(a), 'team': a, 'role': _nick(a) + ' manager', 'text': _bvoice(r, a, 'jab')}]})


# ------------------------------------------------------------------ awards night
def season_news(st):
    Y = _Y()
    r = _r('y17end', st['seed'])
    aw = st.get('awards') or {}
    if not aw:
        return
    c = aw['champion']
    if not any(n.get('kind') == 'champion' for n in st['news']):
        _add(st, {'round': len(st['fx']), 'kind': 'champion', 'tag': 'Champions', 'team': c, 'title': '%s are champions!' % Y._tname(c),
                  'lead': '%d points from %d matchdays.' % (aw['points'], len(st['fx'])),
                  'paras': ['It went down to the wire, and %s held their nerve.' % _nick(c)],
                  'quote': {'who': _boss(c), 'team': c, 'text': 'We deserved it. Thirty-three battles, and we are still standing at the top.'}})
    if aw.get('boot'):
        b = aw['boot'][0]
        _add(st, {'round': len(st['fx']), 'kind': 'award', 'tag': 'Golden Boot', 'pid': b['pid'], 'team': b['team'],
                  'title': 'Golden Boot: %s (%d goals)' % (b['name'], b['n']), 'lead': 'The top scorer of the Y17 Champions League, season %d.' % st['season'],
                  'paras': ['Runner-up: %s (%d).' % (aw['boot'][1]['name'], aw['boot'][1]['n'])] if len(aw['boot']) > 1 else [],
                  'quote': {'who': b['name'], 'pid': b['pid'], 'text': _pvoice(r, b['pid'], 'score')}})
    if aw.get('ballon'):
        w = aw['ballon'][0]
        _add(st, {'round': len(st['fx']), 'kind': 'award', 'tag': "Ballon d'Or", 'pid': w['pid'], 'team': w['team'],
                  'title': "%s wins the Y17 Ballon d'Or" % w['name'],
                  'lead': '%d goals, %d assists, %d player-of-the-match awards.' % (w['g'], w['a'], w['motm']),
                  'paras': ['The podium: ' + ', '.join('%d. %s' % (x['rank'], x['name']) for x in aw['ballon'][:3]) + '.'],
                  'quote': {'who': w['name'], 'pid': w['pid'], 'text': pick(r, ['I dedicate this to my team-mates. Without them, nothing.',
                                                                              'It is a dream. I hope it is not the last one.', 'I worked my whole life for nights like this.'])}})
