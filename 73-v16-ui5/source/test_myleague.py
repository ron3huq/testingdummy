from pathlib import Path
import zipfile,shutil,sys,types,marshal,json,copy,tempfile
base=Path('/workspace/ronaldo-work/73-v25-full');root=base/'test-gateway';tools=root/'work/tools';tools.mkdir(parents=True,exist_ok=True)
for d in [Path('/workspace/ronaldo-work/73-v25-port/package/payload/work/tools'),base/'payload/work/tools',Path('/workspace/ronaldo-work/73-ui5/payload/work/tools')]:
 for p in d.iterdir():
  if p.is_file():shutil.copy2(p,tools/p.name)
z=zipfile.ZipFile('/workspace/ronaldo-work/73-v25-port/package/output/73-V16-V25-unsigned.apk')
for n in z.namelist():
 if n.startswith('assets/gateway-release/outputs/reference/'):
  p=root/n[len('assets/gateway-release/'):];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
sys.path.insert(0,str(tools));app=zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy');pr=types.ModuleType('_protected_runtime');pr.__file__=str(tools/'_protected_runtime.py');sys.modules['_protected_runtime']=pr;exec(marshal.loads(app.read('_protected_runtime.pyc')[16:]),pr.__dict__);pr.install_root(root)
native=types.ModuleType('select_team_runtime');native.cid=0;native.activate_context=lambda cid:setattr(native,'cid',cid);native.ensure_native_team=lambda tid:1;native.set_environment=lambda *args:1;native.editor_context=lambda:native.cid
native.configure_owned_players=lambda ids:setattr(native,'owned',tuple(ids))
sys.modules['select_team_runtime']=native
sys.path.insert(0,'/workspace/ronaldo-work/73-ui5/payload/work/tools')
import myleague_73 as mod,myleague_worlds as worlds,myleague_realism as realism,my_league as league,ziru_data,club_store,gate_logic
old_finish=league.finish;old_begin=league.begin;old_save=league.save;old_result=league.result_key
assert mod.install();assert mod.install()==False
assert (league.finish,league.begin,league.save,league.result_key)==(old_finish,old_begin,old_save,old_result)
checks=['actual_73_protected_modules_imported','all_seven_leagues_adapter_installs','73_finish_and_save_and_receipts_bytecode_untouched','adapter_idempotent']
cfg=worlds.config();registry=ziru_data.competition_registry()
for cid,row in cfg['leagues'].items():
 assert registry['competitions'][cid]['team_ids']==row['teams']
 assert registry['competitions'][cid]['name']==row['name']
 for tid,ids in cfg['native_rosters'].items():assert ziru_data.rosters()[tid]==ids
 s=dict(competition_id=int(cid),team_id=row['teams'][0],season=1,fixture=1,played={},active=None,completed=False)
 rows=league.fixtures(s);counts={}
 for fx in rows:
  teams=[]
  for m in fx['match_list']:
   h,a=m['home_team_id'],m['away_team_id'];assert h!=a;teams.extend([h,a]);counts[(h,a)]=counts.get((h,a),0)+1
  assert len(teams)==len(set(teams))
 assert set(t for pair in counts for t in pair)==set(row['teams'])
 s['schedule_v2']=copy.deepcopy(rows)
 before=copy.deepcopy(s)
 for m in rows[0]['match_list']:
  if s['team_id'] not in (m['home_team_id'],m['away_team_id']):
   score=league.cpu_score(s,m['home_team_id'],m['away_team_id']);assert len(score)==2 and all(isinstance(x,int) and 0<=x<=9 for x in score)
 assert s==before
 # Persisted results pass through the retained fixtures helper without recalculation.
 s['played']={'1':{'matches':copy.deepcopy(rows[0]['match_list'])}}
 for r in s['played']['1']['matches']:r.update(home_goals=3,away_goals=2)
 saved=copy.deepcopy(s['played']);assert realism.fixture_matches(s,rows[0])==saved['1']['matches'];assert s['played']==saved
checks+=['seven_league_memberships_and_names','all_custom_native_rosters','round_robin_unique_teams_per_round','deterministic_cpu_scores_in_native_schema','saved_results_not_recalculated']
# Verify 73-native prepare/START are retained as wrapped call targets (no legacy START implementation imported).
assert league.start.__wrapped__.__code__.co_filename.endswith('my_league.py')
assert league.prepare.__wrapped__.__code__.co_filename.endswith('my_league.py')
checks+=['original_73_prepare_and_start_wrapped_not_replaced','all_reference_sources_load_without_Android_or_network']
# Exercise the actual 73 SQLite/state/info and scorer APIs on an isolated DB.
conn=club_store.connect(root/'outputs/efootball/port-test.sqlite3')
import editor_names,card_rules
editor_names.install();card_rules.install()
cid='122';definition=cfg['leagues'][cid]
s=dict(competition_id=int(cid),team_id=definition['teams'][0],season=1,fixture=1,played={},active=None,completed=False)
s['schedule_v2']=league.fixtures(s)
league.save(conn,s);conn.commit()
wire=league.info(conn,{},dict(rqid=987))
assert wire['result']=='NOERR' and league.state(conn)['competition_id']==122
assert native.cid==122
rows=copy.deepcopy(s['schedule_v2'][0]['match_list'])
for row in rows:row.update(home_goals=2,away_goals=1)
counts=league._cpu_round_stats(s,rows,1,{})
for row in counts:
 if row['team_id']!=s['team_id']:
  assert row['player_id'] in ziru_data.rosters()[str(row['team_id'])]
  assert realism._position(row['player_id'])!=0
for match in rows:
 for side in ('home','away'):
  team=match[side+'_team_id']
  if team!=s['team_id']:
   assert sum(r['goal'] for r in counts if r['team_id']==team)==match[side+'_goals'],(team,match,[(r['player_id'],r['goal']) for r in counts if r['team_id']==team],len(ziru_data.rosters().get(str(team),[])))
assert league.state(conn)['played']=={}

checks+=['actual_73_SQLite_info_route','scorers_are_current_club_roster_members','known_goalkeepers_never_selected_as_scorers','AI_goal_events_match_actual_simulated_scores','menu_reads_do_not_add_played_rounds']
# The working face loader must still accept the mixed old/new payload hashes.
live=root/'livedata'
if not live.exists():live.symlink_to('/workspace/ronaldo-work/73-v25-port/package/payload/livedata',target_is_directory=True)
import importlib.util
spec=importlib.util.spec_from_file_location('noodle_hair',tools/'noodle_hair.py');noodle_hair=importlib.util.module_from_spec(spec);spec.loader.exec_module(noodle_hair)
assert noodle_hair.bundle()['myleague_port']=='v25-73-full1'
checks.append('working_face_bundle_accepts_updated_MyLeague_runtime_hashes')
# New10-club Y08 round-robin and native state/info/scorer replies.
for tid in cfg['leagues']['473']['teams']:
 s=dict(competition_id=473,team_id=tid,season=1,fixture=1,played={},active=None,completed=False);s['schedule_v2']=league.fixtures(s)
 assert len(s['schedule_v2'])==18 and all(len(fx['match_list'])==5 for fx in s['schedule_v2'])
 league.save(conn,s);conn.commit();reply=league.info(conn,{},dict(rqid=901));assert reply['result']=='NOERR'and native.cid==473
 assert set(ziru_data.competition_registry()['competitions']['473']['team_ids'])==set(cfg['leagues']['473']['teams'])
 for fx in s['schedule_v2'][:2]:
  counts=league._cpu_round_stats(s,fx['match_list'],fx['fixture'],{})
  assert all(row['player_id']in ziru_data.rosters()[str(row['team_id'])] for row in counts)
checks+=['Y08 ten starting clubs actual73 state/info;18 rounds, five matches per round, valid in-roster scorers']
# Exercise the real 73 wire-player serializer with a recorded source player;
# projections retain command-specific key sets and never mutate that source.
import msgpack
login_path=next((root/'outputs/reference/decrypted').glob('*CMD_LOGIN_resp.txt'))
login=msgpack.unpackb(login_path.read_bytes(),raw=False,strict_map_key=False)
player=copy.deepcopy(login['entry_info']['gameplayer_list'][0]);original_player=copy.deepcopy(player)
for shape in ['login','warehouse']:
 expected=club_store.wire_player.__wrapped__(copy.deepcopy(player),shape)
 actual=club_store.wire_player(player,shape)
 assert set(actual)==set(expected) and len(actual['parameters'])==147
 assert player==original_player
checks+=['actual_73_login_and_warehouse_wire_shapes_preserved','player_source_not_mutated_by_projection']
# Exercise the installed START closure with the genuine73 state and fixture APIs,
# a deterministic response substitute, and deliberately misleading wire IDs.
import team_kits
cells=dict(zip(league.start.__code__.co_freevars,league.start.__closure__))
original_start=cells['old_start'].cell_contents
seen=[]
def start_fixture(conn,resp,req,entries):
 seen.append(copy.deepcopy(entries))
 return {'result':'NOERR','uniform_list_home':{'base_team_id':0,'uniform_list':[]},'uniform_list_away':{'base_team_id':999,'uniform_list':[]}}
cells['old_start'].cell_contents=start_fixture
old_env=worlds._prepare_environment;worlds._prepare_environment=lambda state:None
try:
 for cid in (473,518):
  for tid in cfg['leagues'][str(cid)]['teams']:
   for side in ('HOME','AWAY'):
    s=dict(competition_id=cid,team_id=tid,season=1,fixture=1,played={},active=None,completed=False);s['schedule_v2']=league.fixtures(s);s['active']={'side':side,'fixture':1}
    league.save(conn,s);conn.commit()
    actual=league.start(conn,{},dict(rqid=902),[copy.deepcopy(original_player)])
    assert actual['result']=='NOERR'
    # Compare with the uncapped editor projection; owned game cards must
    # never pass through opponent rating balancing during START.
    import myleague_editor_runtime as editor
    assert seen[-1]==[editor.project(worlds.edit_projection(copy.deepcopy(original_player)),cid)]
    if cid==473:
     _,fx,_=league.current(s);opponent=fx['away_team_id'] if fx['home_team_id']==tid else fx['home_team_id']
     expected={'home':tid,'away':opponent} if side=='HOME' else {'away':tid,'home':opponent}
     for key,logical in expected.items():
      donor=cfg['kit_aliases'][str(logical)]
      assert actual['uniform_list_'+key]=={'base_team_id':donor,'uniform_list':team_kits.uniform_ids(donor)},(tid,side,key)
    else:
     assert actual['uniform_list_home']['base_team_id']==0 and actual['uniform_list_away']['base_team_id']==999
 checks+=['START fixture routing: all10Y08 teams and both user sides; ignores zero/default wire team IDs','Y17 previous kit behavior preserved; owned START entries bypass opponent rating caps in Y08/Y17']
finally:
 cells['old_start'].cell_contents=original_start;worlds._prepare_environment=old_env
conn.close()
(Path('/workspace/ronaldo-work/73-ui5')/'myleague-api-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'phone_tested':False},indent=2));print('API_TESTS_PASS',len(checks))
