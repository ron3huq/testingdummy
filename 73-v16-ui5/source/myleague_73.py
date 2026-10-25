"""Adapt the retained six-world configuration to 73 V16's native My League API.
No replacement of the 73 save/result implementation and no historical score edits.
"""
import copy,functools,hashlib,json,types,gzip
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
_installed=False

def report(state,**values):
    p=HERE/'myleague-73-status.json'
    try:
        temp=p.with_suffix('.tmp');temp.write_text(json.dumps(dict(state=state,version='v25-73-full1',phone_verified=False,**values),indent=2));temp.replace(p)
    except OSError:pass

def scoped(s,cfg):
    if not isinstance(s,dict) or str(s.get('competition_id')) not in cfg['leagues']:return False
    expected=set(cfg['leagues'][str(s['competition_id'])]['teams'])
    members=s.get('competition_teams')
    if isinstance(members,list) and set(members)!=expected:return False
    if s.get('schedule_v2'):
        members={m[side+'_team_id'] for fx in s['schedule_v2'] for m in fx['match_list'] for side in ('home','away')}
        if members!=expected:return False
    return int(s.get('team_id',0)) in expected

def info_fixture(s,rows):
    idx=min(int(s['fixture']),len(rows))-1
    def own(fx):return next((m for m in fx['match_list'] if s['team_id'] in (m['home_team_id'],m['away_team_id'])),None)
    m=own(rows[idx])
    if m:return idx,rows[idx],m
    if not s.get('completed'):
        for k in range(idx+1,len(rows)):
            m=own(rows[k])
            if m:return k,rows[k],m
    for fx in reversed(rows[:idx+1]):
        m=own(fx)
        if m:return idx,rows[idx],m
    raise ValueError('selected team missing from season')

def project_registry(ziru,cfg):
    names=copy.deepcopy(ziru.team_names());names.update(cfg.get('team_names',{}))
    registry=copy.deepcopy(ziru.competition_registry())
    for cid,row in cfg['leagues'].items():
        comp=registry['competitions'][cid]
        for tid in comp['team_ids']:
            if registry['team_to_competition'].get(str(tid))==int(cid):registry['team_to_competition'].pop(str(tid))
        ids=list(row['teams']);comp.update(name=row['name'],team_count=len(ids),team_ids=ids,teams=[dict(team_id=t,name=names.get(str(t),{}).get('name',str(t)),short=names.get(str(t),{}).get('short','')) for t in ids])
        for tid in ids:registry['team_to_competition'][str(tid)]=int(cid)
        if not row.get('preserve_original_schedule'):
            from myleague_worlds import schedule
            ziru._cache['schedules/ml_schedule_'+cid+'.json']={'schedule_list':schedule(ids,row.get('legs',2))}
    rosters=copy.deepcopy(ziru.rosters())
    fallback=json.loads(gzip.decompress((HERE/'myleague_base_rosters.json.gz').read_bytes()))
    for tid,ids in fallback['rosters'].items():
        if not rosters.get(str(tid)):rosters[str(tid)]=list(ids)
    rosters.update({str(k):list(v) for k,v in cfg.get('simulation_rosters',{}).items()})
    rosters.update({str(k):list(v) for k,v in cfg['native_rosters'].items()})
    ziru._cache.update({'team_names.json':names,'ml_competition_registry.json':registry,'ml_rosters.json':rosters})
    return rosters

def install():
    global _installed
    if _installed:return False
    import my_league as league,ziru_data as ziru,club_store as store
    import league_sim_data,ml_super_league
    import myleague_worlds as worlds,myleague_realism as realism
    import myleague_editor_runtime as editor,select_team_runtime as native
    cfg=worlds.config()
    needed=['fixtures','cpu_score','_cpu_round_stats','prepare','start','info','_opponent_squad','current','state']
    if not all(callable(getattr(league,n,None)) for n in needed):raise RuntimeError('unsupported 73 My League API')
    original_schedules={}
    for cid in cfg['leagues']:
        rel='schedules/ml_schedule_'+cid+'.json'
        original_schedules[rel]=copy.deepcopy(ziru.payload(rel))
    # Original 73 fixture code with a read-only view of original schedules for
    # pre-existing seasons whose membership differs from the custom leagues.
    old_fixtures=league.fixtures
    snapshot_globals=dict(old_fixtures.__globals__)
    snapshot_globals['ziru_data']=types.SimpleNamespace(payload=lambda rel:original_schedules[rel] if rel in original_schedules else ziru.payload(rel))
    legacy_fixtures=types.FunctionType(old_fixtures.__code__,snapshot_globals,old_fixtures.__name__,old_fixtures.__defaults__,old_fixtures.__closure__)
    rosters=project_registry(ziru,cfg)
    for row in editor.config().get('teams',[]):rosters[str(row['team_id'])]=[int(p['id']) for p in row['roster']]
    fallback=json.loads(gzip.decompress((HERE/'myleague_base_rosters.json.gz').read_bytes()))
    positions=dict(fallback['positions'])
    positions.update({str(pid):data[0] for pid,data in league_sim_data.PLAYERS.items()})
    positions.update({str(pid):row.get('formation_role',row['roles'][0]) for pid,row in cfg.get('classic_profiles',{}).items()})
    canonical={'rosters':rosters,'positions':positions}
    realism._league=league
    realism._rankings=types.SimpleNamespace(_canonical_data=lambda:canonical,_rosters=lambda:rosters)
    worlds.NATIVE_BRIDGE=native
    # This helper was removed in 73, but the retained stadium policy uses it.
    league._info_fixture=info_fixture
    old_fixtures=league.fixtures
    @functools.wraps(old_fixtures)
    def fixtures(s):
        return realism._fixtures(old_fixtures,s) if scoped(s,cfg) else legacy_fixtures(s)
    league.fixtures=fixtures
    original_super=ml_super_league.start_season
    @functools.wraps(original_super)
    def custom_season(s):
        if isinstance(s,dict) and str(s.get('competition_id')) in cfg['leagues']:
            # This is called at creation/season boundary. Never rewrite an active draw.
            if s.get('played') or s.get('active'):return None
            cid=str(s['competition_id']);s['competition_teams']=list(cfg['leagues'][cid]['teams'])
            s.pop('schedule_v2',None)
            s['schedule_v2']=fixtures(s)
            return None
        return original_super(s)
    ml_super_league.start_season=custom_season
    old_score=league.cpu_score
    @functools.wraps(old_score)
    def score(s,home,away):
        if not scoped(s,cfg):return old_score(s,home,away)
        fx=league.fixtures(s)[int(s['fixture'])-1]
        rows=realism.fixture_matches(s,fx)
        found=next((r for r in rows if r['home_team_id']==home and r['away_team_id']==away),None)
        if found is None:return old_score(s,home,away)
        return found['home_goals'],found['away_goals']
    league.cpu_score=score
    old_round=league._cpu_round_stats
    @functools.wraps(old_round)
    def round_stats(s,matches,fixture,req):
        original=old_round(s,matches,fixture,req)
        if not scoped(s,cfg):return original
        own=int(s['team_id']);result=[r for r in original if int(r['team_id'])==own]
        for match in matches:
            for side in ('home','away'):
                team=int(match[side+'_team_id'])
                if team==own:continue
                roster=tuple(dict.fromkeys(rosters.get(str(team),[])))
                if not roster:result.extend(r for r in original if int(r['team_id'])==team);continue
                rng=realism._rng('73-events',realism._seed(s),fixture,team)
                goals=max(0,int(match.get(side+'_goals',0)))
                assists=min(goals,sum(int(r.get('assist',0)) for r in original if int(r['team_id'])==team))
                rows={}
                for kind,count in [('goal',goals),('assist',assists)]:
                    pool=realism._event_pool(roster,kind=='assist')
                    if not pool:continue
                    for _ in range(count):
                        pid=rng.choice(pool)
                        row=rows.setdefault(pid,dict(team_id=team,player_id=pid,goal=0,assist=0));row[kind]+=1
                result.extend(rows[p] for p in sorted(rows))
        return result
    league._cpu_round_stats=round_stats
    old_opponent=league._opponent_squad
    @functools.wraps(old_opponent)
    def opponent(conn,team):
        s=league.state(conn)
        if scoped(s,cfg):return None  # Native rosters, never 73's substitute-card inline squad.
        return old_opponent(conn,team)
    league._opponent_squad=opponent
    owned_stamp=None
    def context(conn):
        nonlocal owned_stamp
        stamp=(id(conn),conn.total_changes)
        if stamp!=owned_stamp:
            native.configure_owned_players([r[0]for r in conn.execute("SELECT DISTINCT id FROM gameplayers")]);owned_stamp=stamp
        s=league.state(conn);cid=int(s['competition_id']) if scoped(s,cfg) else 0
        native.activate_context(cid);return s,cid
    old_prepare=league.prepare
    @functools.wraps(old_prepare)
    def prepare(conn,req):
        s,cid=context(conn)
        if cid and not s.get('completed'):
            _,match,_=league.current(s);tid=match['away_team_id'] if match['home_team_id']==s['team_id'] else match['home_team_id']
            if str(tid) in cfg['native_rosters'] and native.ensure_native_team(tid)!=1:
                report('WAITING_FOR_NATIVE_ROSTER',team=tid);return league.fail('CMD_GET_VSCOM_OPPONENT',req)
        return old_prepare(conn,req)
    league.prepare=prepare
    old_info=league.info
    @functools.wraps(old_info)
    def info(conn,resp,req):
        s,cid=context(conn);out=old_info(conn,resp,req)
        if cid:
            view=dict(s,fixture=out.get('fixture',s['fixture']))
            try:env=worlds._prepare_environment(view)
            except ValueError as exc:
                report('WAITING_FOR_ENVIRONMENT_HOOK',error=str(exc));return out
            for key in ('weather','season_type','time_zone'):out[key]=env[key]
        return out
    league.info=info
    # Projection only: the 73 result handler/database schema stays in charge.
    old_start=league.start
    @functools.wraps(old_start)
    def start(conn,resp,req,home_entries):
        s,cid=context(conn)
        entries=home_entries
        if cid:
            from myleague_balance import project
            entries=([editor.project(worlds.edit_projection(p),cid)for p in home_entries]if cid in(518,473)else[editor.project(project(worlds.edit_projection(p),cid,worlds._messi((p.get('gameplayer_id')or{}).get('id'))),cid)for p in home_entries])
            try:worlds._prepare_environment(s)
            except ValueError as exc:report('WAITING_FOR_ENVIRONMENT_HOOK',error=str(exc));return league.fail('CMD_START_GAME',req)
        out=old_start(conn,resp,req,entries)
        if cid and out.get('result')=='NOERR':
            if cid==473:
                #73's response may use base_team_id=0, or the owned club rather
                #than the selected My League club. Route by fixture identity.
                import team_kits
                current=league.state(conn);active=current.get('active')or{}
                _,fixture,_=league.current(current)
                own=int(current['team_id']);opponent=fixture['away_team_id']if fixture['home_team_id']==own else fixture['home_team_id']
                own_side='away'if active.get('side')=='AWAY'else'home'
                selected={own_side:own,('home'if own_side=='away'else'away'):opponent}
                for side,team in selected.items():
                    row=out.get('uniform_list_'+side);donor=cfg['kit_aliases'].get(str(team))
                    if isinstance(row,dict)and donor:
                        row.update(base_team_id=donor,uniform_list=team_kits.uniform_ids(donor))
            else:
                import team_kits
                for side in ('home','away'):
                    row=out.get('uniform_list_'+side)
                    if isinstance(row,dict):
                        donor=cfg['kit_aliases'].get(str(row.get('base_team_id')))
                        if donor:row.update(base_team_id=donor,uniform_list=team_kits.uniform_ids(donor))
        return out
    league.start=start
    # 73 removed _wire_project. Preserve each native reply shape and apply
    # the retained exact-ID/base-ID projection to the already normalized result.
    old_wire=store.wire_player
    @functools.wraps(old_wire)
    def wire_player(player,*args,**kwargs):
        out=old_wire(player,*args,**kwargs)
        return editor.project(worlds.edit_projection(out),native.editor_context())
    store.wire_player=wire_player
    if editor.config().get('packs'):
        import myleague_packs
        myleague_packs.install()
    # Reset native league scope when a non-My-League opponent is requested.
    import gate_logic
    original_opponent=gate_logic.GateLogic._vscom_opponent
    @functools.wraps(original_opponent)
    def gate_opponent(self,mid,resp,req):
        if not league.is_season(req):native.activate_context(0)
        return original_opponent(self,mid,resp,req)
    gate_logic.GateLogic._vscom_opponent=gate_opponent
    original_gate_start=gate_logic.GateLogic._start_game
    @functools.wraps(original_gate_start)
    def gate_start(self,resp,req):
        if not league.is_season(req):native.activate_context(0)
        return original_gate_start(self,resp,req)
    gate_logic.GateLogic._start_game=gate_start
    _installed=True
    report('INSTALLED',leagues={k:r['name'] for k,r in cfg['leagues'].items()},native_rosters=len(cfg['native_rosters']),saved_history_rewritten=False,kits={'351':'Real Madrid 2017','352':'Manchester United 2007','242':'Real Madrid 2011','245':'Barcelona 2017'},native_status_file='select-team-status.json')
    return True
