import argparse,collections,copy,hashlib,json,sqlite3,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--gateway',required=True,type=Path);p.add_argument('--seasons',type=int,default=200);a=p.parse_args();gateway=a.gateway.resolve();r=Path(__file__).parent
sys.path[:0]=[str(r),str(gateway/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,my_league as league,season_rankings as rankings,club_store as store
model.ATTRS=gateway/'outputs/reference/external-attrs';model.install();cfg=worlds.config();checks=[]
def season(cid,index=1,team=999999):return dict(team_id=team,competition_id=int(cid),fixture=1,played={},completed=False,active=None,cpu_level='NORMAL',season=index,realism_v1=dict(seed='test-'+str(index),version=model.VERSION))
for cid,d in cfg['leagues'].items():
 s=season(cid);rows=league.fixtures(s);pairs=collections.Counter((m['home_team_id'],m['away_team_id']) for fx in rows for m in fx['match_list']);ids=d['teams']
 assert len(ids)==len(set(ids)) and len(rows)==2*(len(ids)-1)
 assert set(pairs)=={(h,aw) for h in ids for aw in ids if h!=aw} and set(pairs.values())=={1}
 for fx in rows:
  played=[m[side+'_team_id'] for m in fx['match_list'] for side in ['home','away']];assert len(played)==len(set(played))==len(ids)
 for tid in ids:assert store is not None and rankings._rosters().get(str(tid))
checks.append('all requested league memberships, double round robins, native national rosters and Bayern overlay complete')
source=gateway/'outputs/efootball/local-club.sqlite3';source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory() as tmp:
 for cid,team in [('566',5763),('128',7),('122',101)]:
  conn=sqlite3.connect(Path(tmp)/(cid+'.db'));conn.row_factory=sqlite3.Row;src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);src.backup(conn);src.close()
  count=conn.execute('select count(*) from gameplayers').fetchone()[0]
  out=league.select(conn,{},dict(rqid='select-'+cid,select_team_id=team,select_compe_unit_id=int(cid)),session_token='world-tests');assert out['result']=='NOERR'
  s=league.state(conn);assert set(row['team_id'] for row in league.ranking(s))==set(cfg['leagues'][cid]['teams'])
  if cid in ['122','128']:
   cpu_team=127 if cid=='122' else 45
   rows=league.fixtures(s);fx=next(fx for fx in rows if any({m['home_team_id'],m['away_team_id']}=={team,cpu_team} for m in fx['match_list']))
   s['fixture']=fx['fixture'];league.save(conn,s);conn.commit()
  req=dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='prepare-'+cid,cpu_level='NORMAL',match_category='SEASON')
  opponent=league.prepare(conn,req,session_token='world-tests');assert opponent['result']=='NOERR'
  if cid in ['122','128']:
   target=cfg['custom_rosters'][str(cpu_team)]
   assert opponent['team_data']['base_team_id']==cpu_team and len(opponent['player_list'])==len(target)
   ids=[x['gameplayer_id']['id'] for x in opponent['player_list']];assert set(ids)==set(target)
   assert set(x['gameplayer_id']['id'] for x in opponent['squad_data']['player_list'])==set(ids)
   assert all(len(x['parameters'])==149 for x in opponent['player_list'])
   assert max(opponent['squad_data']['squad_gameplan']['match_plan_settings']['order'])<len(target)
   if cpu_team==127:
    import player_skills
    before_card=conn.execute('select payload from managed_cards where card_id=?',('47287',)).fetchone()[0]
    cfg['player_overrides']['47287']={'stats':{'finishing':99},'skills_add':[18]}
    edited=worlds._custom_squad(conn,127)
    kane=next(x for x in edited['player_list'] if x['gameplayer_id']['id']==47287)
    assert kane['parameters'][20]==99 and kane['parameters'][player_skills.PARAMETER_BY_SKILL[18]]==1
    assert conn.execute('select payload from managed_cards where card_id=?',('47287',)).fetchone()[0]==before_card
    cfg['player_overrides'].clear()
   entries=[store.wire_player(store.player_by_key(conn,x['gameplayer_id']['id'],x['gameplayer_id']['serial']),'list') for x in league.start_refs(conn,{})]
   start=league.start(conn,{},dict(msgid='CMD_START_GAME',rqid='start-bayern',game_id=opponent['game_id'],match_category='SEASON',user_id=1),entries)
   assert start['result']=='NOERR',start
   saved=league.state(conn);cpu='away' if saved['active']['side']=='HOME' else 'home'
   assert start['squad_data_'+cpu]['team_id']==cpu_team
   assert set(x['gameplayer_id']['id'] for x in start['squad_data_'+cpu]['player_list'])==set(target)
  else:assert opponent['player_list'] is None # Keep built-in national roster path.
  assert conn.execute('select count(*) from gameplayers').fetchone()[0]==count
  assert conn.execute('pragma quick_check').fetchone()[0]=='ok';conn.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
checks.append('actual gateway select and native-national opponent prepare in all 3 leagues on copied DB; source/inventory preserved')
checks.append('optional CPU base stat/skill override appears in custom squad wire payload; library/owned data unchanged')
checks.append('Bayern ID127 and Brazil ID45 explicit prepare/START squads contain exact configured players and valid references/parameters; Vinicius included, no Monaco identity')
reports={}
for cid in ['566','128','122']:
 totals=collections.defaultdict(lambda:dict(wins=0,draws=0,losses=0,goals=0,points=0));scorers=collections.Counter();stars=[47287,110718,133543,110644,7511,4522,117047,162114];top_undefeated=0;top_games=0
 for index in range(a.seasons):
  s=season(cid,index);rows=league.fixtures(s)
  for fx in rows:
   matches=league.fixture_matches(s,fx)
   for m in matches:
    h,aw=m['home_team_id'],m['away_team_id'];hg,ag=m['home_goals'],m['away_goals']
    for tid,gf,ga in [(h,hg,ag),(aw,ag,hg)]:
     t=totals[tid];t['wins']+=gf>ga;t['draws']+=gf==ga;t['losses']+=gf<ga;t['goals']+=gf;t['points']+=3 if gf>ga else 1 if gf==ga else 0
    if cid=='122':
     top={101,108,114,109,173}
     if (h in top)!=(aw in top):top_games+=1;top_undefeated+=(hg>=ag if h in top else ag>=hg)
   if cid in ['128','122']:
    events,missing=rankings._simulate_matches(None,s,fx['fixture'],matches);assert not missing
    for event in events:scorers[event['player_id']]+=event['goal']
 games=2*(len(cfg['leagues'][cid]['teams'])-1)*a.seasons
 report={str(t):dict(win_rate=round(v['wins']/games,4),mean_points=round(v['points']/a.seasons,2),mean_goals=round(v['goals']/a.seasons,2)) for t,v in totals.items()}
 if cid=='566':assert .88<report['52']['win_rate']<.92
 if cid=='122':assert top_undefeated==top_games and report['100']['win_rate']<.05
 if cid=='122':
  report['club_star_goals_per_season']={str(pid):round(scorers[pid]/a.seasons,2) for pid in [110718,133543,110644]}
  assert all(scorers[pid]/a.seasons>35 for pid in [110718,133543,110644])
 if cid=='128':
  assert report['7']['win_rate']>report['1174']['win_rate']+.5
  report['star_goals_per_season']={str(pid):round(scorers[pid]/a.seasons,2) for pid in stars}
  assert min(scorers[pid]/a.seasons for pid in stars)>12
 reports[cid]=report
checks.append('multi-season hierarchy: Japan ~90% wins, club Top5 unbeaten against lower groups, United <5% wins, world stars score')
result={'status':'SERVER_AND_SIMULATION_PASS_DEVICE_UNTESTED','device_tested':False,'seasons_each_league':a.seasons,'checks':checks,'benchmark':reports,'limits':['Bayern inline squad requires actual Android match/render test','new league menus require device check','old season snapshots and observed scores are retained; start a new season for new membership']}
(r/'worlds-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
