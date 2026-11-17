"""Host checks for the merged V30 + RC26 gateway (no phone, no real save).
Usage: test_merged.py APP_DIR GATEWAY_ROOT
"""
import sys, types, json, os, time, traceback, copy
app, root = sys.argv[1], sys.argv[2]
opened = []
class _Panel:
    @staticmethod
    def openFromGateway(event): opened.append(event)
    def __getattr__(self, k): return lambda *a, **kw: None
j = types.ModuleType('java'); j.jclass = lambda name: _Panel(); j.cast = lambda *a: None; j.dynamic_proxy = lambda *a: object
sys.modules['java'] = j
sys.path.insert(0, app)
import _protected_runtime as pr
pr.install_root(root)
import embedded_gateway as eg
results = {}
def check(name, fn):
    t = time.time()
    try:
        out = fn(); results[name] = dict(ok=True, info=out, s=round(time.time() - t, 2))
    except Exception as e:
        results[name] = dict(ok=False, error=repr(e)[:400], trace=traceback.format_exc()[-1500:])
    print(('PASS ' if results[name]['ok'] else 'FAIL ') + name, json.dumps(results[name], ensure_ascii=False, default=str)[:600], flush=True)

check('initialize', lambda: eg.initialize(root, 311010201))
check('bridge_73 installed', lambda: bool(getattr(eg, '_v191_full_installed', False)) or (_ for _ in ()).throw(AssertionError('bridge not installed')))
def status():
    return json.loads(open(os.path.join(root, 'work/tools/myleague-73-status.json')).read())['state']
check('myleague_73 status', status)

# ---- V30 Master League (iml) ----
def iml(method, path, body=None):
    raw = eg.manage('iml_api', json.dumps(dict(method=method, path=path, body=body or {})))
    return json.loads(raw) if isinstance(raw, str) else raw
check('iml_status', lambda: str(eg.manage('iml_status', '{}'))[:300])
check('iml /api/health', lambda: str(iml('GET', '/api/health'))[:300])
check('iml /api/state', lambda: str(iml('GET', '/api/state'))[:300])
check('iml /api/careers', lambda: str(iml('GET', '/api/careers'))[:300])
check('iml /api/world/leagues', lambda: str(iml('GET', '/api/world/leagues'))[:300])

# ---- RC26 Transfer editor (public My League contexts 122/128) ----
def transfer():
    import transfer_editor as tr, rc24_registry
    c = eg._logic.conn
    out = {}
    for cid in (122, 128):
        teams = tr.manage(c, 'ui712_transfer_list', dict(competition=cid))['teams']
        ready = [t for t in teams if t.get('ready')]
        out[cid] = (len(teams), len(ready))
        if ready:
            got = tr.manage(c, 'ui712_transfer_get', dict(team_id=ready[0]['id'], competition=cid))
            assert got['ready'], got
    got = tr.manage(c, 'ui712_transfer_get', dict(team_id=108, competition=122))
    out['barcelona_ready'] = got.get('ready')
    return out
check('transfer editor 122/128', transfer)

# ---- Event cups via the real V30 gateway logic + RC24/RC25 layers ----
def cup_cycle(spec_key):
    import club_store, rc22_v25_events
    L = eg._logic; c = L.conn
    m = rc22_v25_events._modules
    s = m['cup_spec'].SPECS[spec_key]
    entries = L.handle('CMD_GET_EVENT_LIST_AND_LOG', dict(rqid=1))
    listed = {e['event_id'] for e in entries.get('event_list', [])}
    assert s.group_event_id in listed, sorted(listed)[:20]
    r = L.handle('CMD_GET_EVENT_COMPE_INFO', dict(event_id=s.group_event_id, match_category='EVENT_COM', rqid=2))
    assert r['result'] == 'NOERR', r
    snap = json.loads(eg.manage('ucl_ui_snapshot', json.dumps(dict(eventId=s.group_event_id))))
    own = [dict(gameplayer_id=p['gameplayer_id']) for p in club_store.players(c)][:11]
    first = own[0]['gameplayer_id']
    played = 0
    for i in range(3):
        event = s.group_event_id
        L.handle('CMD_GET_EVENT_LIST_AND_LOG', dict(rqid=10 + i))
        e = L.handle('CMD_SET_EVENT_ENTER', dict(event_id=event, select_team_id=club_store.club_team_id(c), rqid=20 + i)); assert e['result'] == 'NOERR', e
        f = L.handle('CMD_GET_EVENT_COMPE_GROUP_STAGE_DRAW', dict(event_id=event, compe_unit_id=s.group_compe_unit_id, rqid=25 + i)); assert f['result'] == 'NOERR', f
        p = L.handle('CMD_GET_VSCOM_OPPONENT', dict(event_id=event, match_category='EVENT_COM', rqid=30 + i)); assert p['result'] == 'NOERR', p
        gid = p['game_id']
        st = L.handle('CMD_START_GAME', dict(event_id=event, game_id=gid, side='HOME', coach=club_store.coaches(c)[0], player_list_home=own, match_category='EVENT_COM', rqid=40 + i)); assert st['result'] == 'NOERR', st
        detail = dict(game_id=gid, pk_flag='NO', abnormalend_reason='NOERR', goal_player_list=[first, first], assist_player_list=[], myteam_player_list=[dict(gameplayer_id=first, is_man_of_the_match='YES', is_join_game='YES')])
        score = [dict(score_1st=2, score_2nd=0, score_pk=0), dict(score_1st=0, score_2nd=0, score_pk=0)]
        res = L.handle('CMD_GET_VSCOM_GAME_RESULT', dict(event_id=event, match_result=detail, score=score, rqid=50 + i)); assert res['result'] == 'NOERR', res
        played += 1
    awards = json.loads(eg.manage('ucl_ui_snapshot', json.dumps(dict(eventId=s.group_event_id)))).get('awards')
    assert awards and awards['games'] == 3, awards
    goals = next(p for p in awards['boards']['goals'] if p['id'] == first['id'])
    return dict(played=played, own_goals=goals['goals'], snapshot_keys=sorted(snap)[:12], cpu_level=p.get('cpu_level'))
check('UCL event cycle + awards', lambda: cup_cycle('ucl'))
check('WC event cycle + awards', lambda: cup_cycle('wc'))

# ---- login resources (livedata manifest) via RC26 v191_live + kits_runtime ----
def login_resources():
    import json as J
    tpl = J.loads(open(os.path.join(root, 'work/templates/CMD_LOGIN_LIVEDATA.json')).read())
    out = eg._local_urls(copy.deepcopy(tpl))
    ver = J.loads(out['version_file'])
    dt = [r for r in out['livedata_list'] if r.get('name') == 'dt870_mobile_and.cpk']
    return dict(dt870Hash=ver.get('dt870Hash'), dt870Size=ver.get('dt870FileSize'), dt870_url=dt[0]['url'] if dt else None, containers=len(ver.get('dt880', [])))
check('login livedata manifest', login_resources)

print(json.dumps({k: v['ok'] for k, v in results.items()}, indent=1))

# ---- ML profile creation + world/career listing ----
check('iml /api/entry (auto-create ML profile)', lambda: str(iml('GET', '/api/entry'))[:300])
check('iml /api/state after entry', lambda: str(iml('GET', '/api/state'))[:400])
check('iml /api/careers after entry', lambda: str(iml('GET', '/api/careers'))[:300])
check('iml /api/world/leagues after entry', lambda: str(iml('GET', '/api/world/leagues'))[:300])
print(json.dumps({k: v['ok'] for k, v in results.items()}, indent=1))

def ml_career():
    opts = iml('GET', '/api/season/options')
    teams = iml('GET', '/api/teams?q=')
    rows = teams if isinstance(teams, list) else (teams.get('teams') or teams.get('items') or [])
    ids = [r.get('id') or r.get('team_id') for r in rows][:20]
    st = iml('POST', '/api/career/new', dict(league_name='Test League', teams=ids, user_team=ids[0], reborn_world=False, variants=False, cup=True, lower=False))
    s2 = iml('GET', '/api/state')
    return dict(options=str(opts)[:200], nteams=len(rows), new=str(st)[:300], state=str(s2)[:300])
check('iml career/new', ml_career)
