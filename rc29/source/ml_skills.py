"""RC29.5 Master League skills: real special skills for the big clubs' players, and crossing / low lofted pass for every
winger and midfielder.  Only ever ADDS skill flags (an existing skill is never removed) and only inside Master League
(ml_isolation.in_ml); My League / RC26 cards are untouched.

Hooked on the two ways a player reaches a Master League match:
  * club_store._wire_project  - our own squad (every served card)
  * opponent_squad.build      - the CPU side (V32 original, as routed by ml_isolation)
"""
import functools, sys, unicodedata

# skill label id (innate_skill_labels.json) -> parameter flag: myleague_editor_runtime.FLAGS[id]
FLAGS = [70, 107, 71, 72, 73, 108, 74, 75, 135, 136, 102, 116, 124, 130, 140, 76, 121, 77, 120, 101, 78, 103, 104, 109, 127, 143, 134, 79, 80, 81, 114, 128,
         82, 110, 83, 84, 119, 85, 86, 98, 117, 118, 122, 141, 87, 88, 105, 89, 90, 99, 100, 138, 139, 126, 129, 91, 92, 93, 106, 111, 112, 113, 125, 137, 115, 94,
         123, 132, 142, 95, 131, 96, 97, 133]
ID = {'scissors': 0, 'double touch': 1, 'flip flap': 2, 'marseille': 3, 'sombrero': 4, 'chop turn': 5, 'cut behind': 6, 'scotch': 7, 'tap trick': 8,
      'sole control': 10, 'momentum': 11, 'accel': 12, 'magnetic': 13, 'heading': 15, 'bullet header': 16, 'curler': 17, 'blitz curler': 18, 'chip': 19,
      'knuckle': 20, 'dipping': 21, 'rising': 22, 'long shot': 23, 'low screamer': 24, 'snap': 26, 'acrobatic finish': 27, 'heel trick': 28, 'first time': 29,
      'phenomenal finish': 30, 'willpower': 31, 'one touch': 32, 'through': 33, 'weighted': 34, 'pinpoint': 35, 'edge cross': 36, 'outside curler': 37,
      'rabona': 38, 'no look': 39, 'game changing': 40, 'visionary': 41, 'phenomenal pass': 42, 'low loft': 44, 'long throw': 47, 'penalty': 49,
      'gk saver': 50, 'gk directing': 53, 'gk roar': 54, 'man marking': 56, 'track back': 57, 'interception': 58, 'blocker': 59, 'aerial': 60, 'sliding': 61,
      'long reach': 62, 'fortress': 64, 'acrobatic clear': 65, 'aerial fort': 66, 'captaincy': 69, 'super sub': 71, 'fighting spirit': 72,
      'gk low punt': 45, 'gk high punt': 46, 'gk long throw': 48}
WIDE_MID = {4, 5, 6, 7, 8, 9, 10}           # DMF CMF LMF RMF AMF LWF RWF  -> edge crossing + low lofted pass
BASE = (ID['edge cross'], ID['low loft'])

# the big clubs' players: real special skills (2025-26)
SPECIAL = {
    # Arsenal
    'bukayo saka': 'edge cross,pinpoint,curler,first time,momentum,one touch,through', 'martin odegaard': 'visionary,through,weighted,game changing,one touch,outside curler,captaincy',
    'declan rice': 'interception,man marking,blocker,track back,long reach,fighting spirit,captaincy', 'william saliba': 'interception,blocker,aerial fort,fortress,long reach',
    'gabriel magalhaes': 'aerial,bullet header,fortress,blocker,heading', 'viktor gyokeres': 'phenomenal finish,first time,low screamer,accel,willpower',
    'eberechi eze': 'curler,double touch,marseille,momentum,dipping', 'david raya': 'gk directing,gk low punt,gk saver', 'jurrien timber': 'interception,track back,man marking',
    'martin zubimendi': 'one touch,through,interception,weighted', 'gabriel martinelli': 'accel,momentum,first time', 'kai havertz': 'heading,first time,one touch',
    'noni madueke': 'double touch,scissors,curler', 'riccardo calafiori': 'interception,low loft,fighting spirit', 'leandro trossard': 'curler,first time,super sub',
    # Real Madrid
    'kylian mbappe': 'phenomenal finish,accel,momentum,first time,chip,low screamer,snap', 'vinicius': 'scissors,double touch,momentum,accel,flip flap,cut behind,chip',
    'jude bellingham': 'willpower,fighting spirit,first time,heading,marseille,through', 'federico valverde': 'long shot,low screamer,track back,willpower,interception',
    'arda guler': 'curler,through,visionary,outside curler,dipping', 'thibaut courtois': 'gk directing,gk saver,gk high punt', 'eder militao': 'aerial,interception,blocker',
    'antonio rudiger': 'fortress,aerial fort,fighting spirit,blocker', 'trent alexander arnold': 'pinpoint,visionary,weighted,game changing,dipping,curler',
    'aurelien tchouameni': 'interception,man marking,blocker,long reach', 'rodrygo': 'curler,double touch,first time', 'dean huijsen': 'aerial,interception,weighted',
    'eduardo camavinga': 'interception,sliding,track back',
    # Barcelona
    'lamine yamal': 'outside curler,curler,double touch,scissors,visionary,through,rabona,momentum', 'raphinha': 'curler,knuckle,first time,accel,edge cross,willpower',
    'pedri': 'one touch,through,visionary,weighted,marseille,sole control', 'robert lewandowski': 'phenomenal finish,first time,heading,acrobatic finish,chip,penalty',
    'frenkie de jong': 'marseille,sole control,one touch,through', 'gavi': 'fighting spirit,interception,one touch,track back', 'dani olmo': 'curler,first time,one touch',
    'pau cubarsi': 'interception,weighted,low loft,blocker', 'jules kounde': 'interception,man marking,track back', 'alejandro balde': 'accel,track back,edge cross',
    'marc andre ter stegen': 'gk directing,gk low punt', 'joan garcia': 'gk saver,gk low punt', 'ferran torres': 'first time,heading', 'marcus rashford': 'knuckle,accel,curler',
    'fermin lopez': 'first time,long shot,track back', 'ronald araujo': 'aerial,fortress,blocker',
    # Bayern
    'harry kane': 'phenomenal finish,first time,visionary,weighted,low screamer,penalty,heading', 'michael olise': 'curler,outside curler,double touch,scissors,visionary,through',
    'jamal musiala': 'double touch,scissors,marseille,sole control,momentum,cut behind,first time', 'joshua kimmich': 'pinpoint,weighted,through,interception,captaincy,game changing',
    'luis diaz': 'accel,double touch,momentum,cut behind', 'dayot upamecano': 'interception,blocker,long reach', 'jonathan tah': 'aerial,fortress,blocker',
    'manuel neuer': 'gk directing,gk low punt,gk high punt', 'serge gnabry': 'first time,curler', 'leroy sane': 'accel,curler,double touch', 'alphonso davies': 'accel,track back,edge cross',
    'aleksandar pavlovic': 'one touch,interception,weighted', 'konrad laimer': 'track back,interception,fighting spirit', 'thomas muller': 'first time,one touch,willpower,heading',
    # Man City
    'erling haaland': 'phenomenal finish,first time,acrobatic finish,heading,bullet header,accel,low screamer', 'phil foden': 'curler,double touch,first time,through,one touch',
    'rodri': 'interception,through,weighted,long shot,man marking,blocker', 'ruben dias': 'interception,fortress,blocker,aerial,captaincy', 'jeremy doku': 'scissors,double touch,flip flap,accel,momentum',
    'tijjani reijnders': 'through,one touch,long shot', 'rayan cherki': 'curler,rabona,no look,double touch,outside curler', 'bernardo silva': 'marseille,sole control,one touch,track back,willpower',
    'josko gvardiol': 'interception,aerial,long reach', 'omar marmoush': 'curler,knuckle,first time', 'gianluigi donnarumma': 'gk saver,gk high punt', 'savinho': 'double touch,scissors,curler',
    'rayan ait nouri': 'edge cross,accel', 'nico gonzalez': 'interception,long shot',
    # Liverpool
    'mohamed salah': 'phenomenal finish,curler,first time,outside curler,chip,momentum,penalty', 'virgil van dijk': 'aerial fort,fortress,interception,blocker,captaincy,heading,long loft',
    'florian wirtz': 'visionary,through,one touch,no look,double touch,game changing', 'alexis mac allister': 'one touch,through,interception,low screamer',
    'dominik szoboszlai': 'knuckle,long shot,low screamer,dipping,track back', 'alexander isak': 'first time,chip,double touch,acrobatic finish', 'hugo ekitike': 'first time,double touch,chip',
    'ryan gravenberch': 'marseille,interception,one touch', 'cody gakpo': 'curler,first time,dipping', 'alisson': 'gk directing,gk low punt,gk saver', 'ibrahima konate': 'aerial,blocker,long reach',
    'milos kerkez': 'edge cross,accel,track back', 'jeremie frimpong': 'accel,edge cross,momentum', 'federico chiesa': 'curler,first time,super sub',
    # Chelsea
    'cole palmer': 'curler,outside curler,first time,visionary,through,penalty,no look', 'enzo fernandez': 'through,weighted,long shot,dipping,low loft', 'moises caicedo': 'interception,man marking,track back,blocker,sliding',
    'joao pedro': 'first time,double touch,heading', 'pedro neto': 'accel,edge cross,curler', 'reece james': 'pinpoint,edge cross,knuckle,interception', 'marc cucurella': 'interception,track back,fighting spirit',
    'robert sanchez': 'gk low punt', 'levi colwill': 'interception,weighted', 'wesley fofana': 'interception,blocker', 'estevao': 'double touch,curler,scissors', 'liam delap': 'heading,first time',
    'jamie gittens': 'accel,double touch,scissors', 'garnacho': 'accel,curler,scissors',
    # Atletico
    'julian alvarez': 'first time,phenomenal finish,track back,knuckle,chip', 'antoine griezmann': 'curler,first time,visionary,through,one touch,acrobatic finish', 'jan oblak': 'gk saver,gk directing',
    'koke': 'through,weighted,captaincy,one touch', 'pablo barrios': 'one touch,interception', 'alex baena': 'curler,through,dipping', 'giuliano simeone': 'track back,fighting spirit,accel',
    'jose maria gimenez': 'aerial,fortress,fighting spirit', 'robin le normand': 'aerial,blocker', 'marcos llorente': 'accel,track back,long shot', 'alexander sorloth': 'heading,bullet header,first time',
    'nico gonzalez atletico': 'curler,edge cross', 'thiago almada': 'curler,double touch', 'conor gallagher': 'track back,fighting spirit,interception',
    # PSG
    'ousmane dembele': 'phenomenal finish,double touch,curler,first time,outside curler,accel,chip', 'khvicha kvaratskhelia': 'double touch,scissors,curler,marseille,momentum',
    'vitinha': 'one touch,through,weighted,long shot,marseille', 'achraf hakimi': 'accel,edge cross,pinpoint,knuckle', 'marquinhos': 'interception,captaincy,aerial,blocker', 'joao neves': 'interception,one touch,track back',
    'desire doue': 'double touch,curler,first time', 'nuno mendes': 'accel,edge cross,track back', 'fabian ruiz': 'through,long shot,low loft', 'willian pacho': 'interception,fortress,blocker',
    'bradley barcola': 'accel,first time,double touch', 'goncalo ramos': 'first time,heading', 'lucas chevalier': 'gk saver,gk low punt', 'warren zaire emery': 'interception,track back',
}


def _norm(s):
    s = unicodedata.normalize('NFKD', str(s or '').replace('ø', 'o').replace('Ø', 'O').replace('ł', 'l')).encode('ascii', 'ignore').decode().lower()
    return ' '.join(s.replace('-', ' ').replace('.', ' ').split())


_KEYS = [(' ' + k + ' ', [ID[x.strip()] for x in v.split(',') if x.strip() in ID]) for k, v in SPECIAL.items()]
_state = {'installed': False, 'added': 0}


def skills_for(name, pos_code):
    ids = set()
    nn = _norm(name)
    try:
        import ml_realism as M
        match = lambda k: M._name_match(k.strip(), nn, ' ' + nn + ' ')
    except Exception:
        match = lambda k: k in ' ' + nn + ' '
    for k, sk in _KEYS:
        if match(k):
            ids.update(sk)
            break
    if pos_code in WIDE_MID:
        ids.update(BASE)
    return ids


def enhance(params, name):
    """Turn on the player's extra skill flags in a canonical parameter list (in place). Never turns a flag off."""
    if not isinstance(params, list) or len(params) < 144:
        return params
    try:
        pos = int(params[0])
    except Exception:
        pos = -1
    for sid in skills_for(name, pos):
        f = FLAGS[sid]
        if f < len(params) and not params[f]:
            params[f] = 1
            _state['added'] += 1
    return params


def _player_name(p):
    for k in ('name', 'player_name', 'name_en'):
        if p.get(k):
            return p[k]
    try:
        import ml_realism
        pid = (p.get('gameplayer_id') or {}).get('id') or p.get('player_id') or p.get('id')
        return ml_realism._name(pid) if pid else ''
    except Exception:
        return ''


def _in_ml():
    try:
        import ml_isolation
        return ml_isolation.in_ml()
    except Exception:
        return False


def install():
    if _state['installed']:
        return _state
    try:
        import club_store as store
        attr = '_wire_project' if hasattr(store, '_wire_project') else 'wire_player'
        proj = getattr(store, attr)

        @functools.wraps(proj)
        def wire_project(player, *a, **k):
            out = proj(player, *a, **k)
            try:
                if isinstance(out, dict) and _in_ml():
                    enhance(out.get('parameters'), _player_name(out) or _player_name(player if isinstance(player, dict) else {}))
            except Exception:
                pass
            return out
        setattr(store, attr, wire_project)
    except Exception as exc:
        _state['error_store'] = repr(exc)
    try:
        import opponent_squad as o
        build = o.build

        @functools.wraps(build)
        def built(*a, **k):
            out = build(*a, **k)
            try:
                if isinstance(out, dict) and _in_ml():
                    for p in out.get('player_list') or []:
                        if isinstance(p, dict):
                            enhance(p.get('parameters'), _player_name(p))
            except Exception:
                pass
            return out
        for attr in ('_rc29_ml_isolation', '_rc29_original', '_rc29_rc26'):
            if hasattr(build, attr):
                setattr(built, attr, getattr(build, attr))
        o.build = built
    except Exception as exc:
        _state['error_opp'] = repr(exc)
    install_stadium()
    _state['installed'] = True
    return _state


# ------------------------------------------------------------------ stadiums (RC26 policy: licensed stadiums only, never the default one)
def _stadium_pool():
    try:
        import myleague_worlds as w
        cfg = w.config()['match_environment']
        bad = set(cfg.get('exclude_stadium_ids') or [100])
        pool = [int(x) for x in cfg.get('stadium_ids') or [] if int(x) not in bad]
        if pool:
            return pool
    except Exception:
        pass
    return [1, 7, 30, 51, 52, 85]


def _set_stadium(obj, sid, depth=0):
    n = 0
    if depth > 6:
        return 0
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == 'stadium_id' and isinstance(v, int) and not (101 <= v <= 103):
                obj[k] = sid
                n += 1
            elif isinstance(v, (dict, list)) and k not in ('custom_stadium', 'custom_stadium_list', 'stadium_list'):
                n += _set_stadium(v, sid, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            n += _set_stadium(v, sid, depth + 1)
    return n


def install_stadium():
    try:
        import gate_logic, random, time
        G = gate_logic.GateLogic
        orig = G._start_game

        @functools.wraps(orig)
        def start_game(self, *a, **k):
            out = orig(self, *a, **k)
            try:
                if _in_ml():
                    sid = random.Random(time.time_ns()).choice(_stadium_pool())
                    _state['stadium'] = (sid, _set_stadium(out, sid))
            except Exception as exc:
                _state['stadium_error'] = repr(exc)
            return out
        for attr in ('_rc29_ml_isolation', '_rc29_original', '_rc29_rc26'):
            if hasattr(orig, attr):
                setattr(start_game, attr, getattr(orig, attr))
        G._start_game = start_game
    except Exception as exc:
        _state['stadium_install'] = repr(exc)
