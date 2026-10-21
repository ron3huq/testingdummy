"""Gateway on disposable seed DB copies; native readiness is stubbed explicitly."""
from pathlib import Path
import argparse,sys,json,copy,sqlite3,tempfile,hashlib,random,collections
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;g=a.gateway.resolve()
sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_realism as model,myleague_worlds as worlds,my_league as league,season_rankings as ranks,club_store as store
class Bridge:
 status=1
 @classmethod
 def ensure_native_team(cls,team):return cls.status
worlds.NATIVE_BRIDGE=Bridge;model.ATTRS=g/'outputs/reference/external-attrs';model.install();cfg=worlds.config();checks=[]
assert cfg['leagues']['125']['teams']==cfg['leagues']['125']['original_teams']
assert cfg['leagues']['549']['name']=='Asia-Pacific League'
assert {m['player_id'] for m in cfg['transfers']}=={16906726}
assert 16906726 in cfg['native_rosters']['116'] and 16906726 not in cfg['native_rosters']['18961']
source=g/'outputs/efootball/local-club.sqlite3';source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
for cid,d in cfg['leagues'].items():
 s=dict(team_id=999999,competition_id=int(cid),season=1,fixture=1,played={},active=None,completed=False,cpu_level='NORMAL')
 rows=league.fixtures(s);pairs=collections.Counter((m['home_team_id'],m['away_team_id']) for fx in rows for m in fx['match_list'])
 assert len(rows)==d.get('legs',2)*(len(d['teams'])-1)
 if d.get('legs',2)==2:assert set(pairs.values())=={1} and len(pairs)==len(d['teams'])*(len(d['teams'])-1)
 else:
  unordered=collections.Counter(tuple(sorted(k)) for fx in rows for k in [(m['home_team_id'],m['away_team_id']) for m in fx['match_list']]);assert len(unordered)==28 and set(unordered.values())=={3}
checks.append('18/18/20/18/8 membership; double round-robin plus triple Danish schedule')
# Exact IDs, all numeric changes, skill additions/removals, no truncated Card IDs.
for collection in ['base_overrides','card_overrides']:
 for pid,rule in cfg[collection].items():
  player=dict(gameplayer_id=dict(id=int(pid),serial=7),parameters=[70]*70+[0]*77,additional_skill_id=[3,74],is_skill_added='YES')
  original=copy.deepcopy(player);out=worlds.edit_projection(player)
  assert out['gameplayer_id']==player['gameplayer_id'] and player==original
  for name,value in rule.get('stats',{}).items():assert out['parameters'][worlds.STAT_INDEX[name]]==value
  for flag in rule.get('skill_flags_add',[]):assert out['parameters'][flag]==1
  for flag in rule.get('skill_flags_remove',[]):assert out['parameters'][flag]==0
  if 3 in rule.get('skill_ids_remove',[]):assert out['additional_skill_id']==[74,74]
assert 125 in cfg['base_overrides']['132756']['skill_flags_add']
assert cfg['unresolved_skill_names']==['Power Tackle'] and cfg['base_overrides']['110815']['stats']['tackling']==94
checks.append('84 exact Base IDs and 19 exact Card IDs; requested stats/skills and Marseille removal; Long-Reach Tackle verified; Power Tackle pending')
# Exercise the shared projection used by both single-card detail and bulk LOGIN/list.
for pid,rule in cfg['card_overrides'].items():
 con=sqlite3.connect(source.resolve().as_uri()+'?mode=ro',uri=True)
 raw=con.execute('select payload from managed_cards where card_id=?',(pid,)).fetchone()
 con.close()
 assert raw is not None,pid
 card=json.loads(raw[0]);card['additional_skill_id']=[3,74]
 for shape in ['login','list','detail']:
  out=store.wire_player(card,shape)
  for key,value in rule['stats'].items():assert out['parameters'][worlds.STAT_INDEX[key]]==value
  if pid=='89138019825360':assert out['parameters'][72]==0 and 3 not in out.get('additional_skill_id',[])
checks.append('real managed-card payloads pass shared single/bulk projection for LOGIN/list/detail with exact 19 full IDs')
with tempfile.TemporaryDirectory() as tmp:
 for side in ['HOME','AWAY']:
  conn=sqlite3.connect(Path(tmp)/(side+'.db'));conn.row_factory=sqlite3.Row;src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True);src.backup(conn);src.close()
  inv=conn.execute('select * from gameplayers order by rowid').fetchall();inv=[tuple(x) for x in inv]
  out=league.select(conn,{},dict(rqid='v3-select',select_team_id=101,select_compe_unit_id=122),session_token='v3-tests');assert out['result']=='NOERR'
  s=league.state(conn);rows=league.fixtures(s)
  fx=next(fx for fx in rows if any(m['home_team_id']==(101 if side=='HOME' else 127) and m['away_team_id']==(127 if side=='HOME' else 101) for m in fx['match_list']))
  s['fixture']=fx['fixture'];league.save(conn,s);conn.commit()
  req=dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='prepare',cpu_level='NORMAL',match_category='SEASON')
  Bridge.status=13;assert league.prepare(conn,req,session_token='v3-tests')['result']!='NOERR'
  assert not (league.state(conn).get('active')or{}).get('started')
  Bridge.status=1;out=league.prepare(conn,req,session_token='v3-tests');assert out['result']=='NOERR'
  assert out['team_data']['base_team_id']==127 and all(out.get(k) is None for k in ['player_list','squad_data','coach_data'])
  # Reproduce a saved v2 crash receipt. V3 should quarantine it, keep fixture and regenerate native-only.
  s=league.state(conn);s['active']['opponent']['player_list']=[{'unsafe_v2':True}];s['active']['started']=True;gid=s['active']['game_id'];played=copy.deepcopy(s['played']);league.save(conn,s);conn.commit()
  out=league.prepare(conn,dict(req,rqid='recover'),session_token='v3-tests');assert out['result']=='NOERR' and out.get('player_list') is None
  s=league.state(conn);assert s['fixture']==fx['fixture'] and s['played']==played
  assert store.get_meta(conn,'v3_quarantined_inline_'+str(gid),'')
  entries=[store.wire_player(store.player_by_key(conn,x['gameplayer_id']['id'],x['gameplayer_id']['serial']),'list') for x in league.start_refs(conn,{})]
  request=dict(msgid='CMD_START_GAME',rqid='start',game_id=out['game_id'],match_category='SEASON',user_id=1)
  Bridge.status=13;assert league.start(conn,{},request,entries)['result']!='NOERR'
  Bridge.status=1;start=league.start(conn,{},request,entries);assert start['result']=='NOERR',start
  cpu='away' if side=='HOME' else 'home';assert start['squad_data_'+cpu] is None,start['squad_data_'+cpu]
  assert [tuple(x) for x in conn.execute('select * from gameplayers order by rowid')]==inv
  assert conn.execute('pragma quick_check').fetchone()[0]=='ok';conn.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
checks.append('real gateway prepare/START HOME and AWAY with native-readiness stub; unsafe saved v2 receipt quarantined; no CPU inline squad; unavailable native roster blocks launch; seed DB unchanged')
# Verify pair probabilities independently of Poisson goal totals; includes both fixture directions.
def distribution(cid,h,aw,n=15000):
 rng=random.Random(197);wins=draws=losses=0
 for i in range(n):
  hg,ag=model._hierarchy_score(dict(competition_id=cid,season=1,team_id=999999),h,aw,rng)
  wins+=hg>ag;draws+=hg==ag;losses+=hg<ag
 return dict(win=wins/n,draw=draws/n,loss=losses/n)
pairs={}
for h,aw in [(5763,52),(52,5763),(5763,54),(54,5763),(5763,5750),(52,53),(7,8),(8,7),(8,5),(7,1174),(45,1174),(6,1174)]:
 cid=566 if h>1000 or h==52 else 128
 if aw==5763:cid=566
 d=distribution(cid,h,aw);pairs[f'{cid}:{h}-{aw}']=d
 if cid==566 and h==5763 and aw==52:assert .68<d['loss']<.72
 if cid==566 and h==5763 and aw==54:assert .68<d['win']<.72 and d['loss']==0
 if cid==566 and h==54 and aw==5763:assert .68<d['loss']<.72 and d['win']==0
 if (cid,h,aw)==(566,5763,5750):assert abs(d['win']-d['loss'])<.025
 if cid==128 and aw==1174:assert d['win']>(.85 if h==7 else .75) and d['draw']>.03 and d['loss']>0
 if (cid,h,aw)==(128,7,8):assert .4<d['win']<.62 and d['loss']>.2
checks.append('15000 draws per selected pair: Asian 70% rules, equal middle peers, Japan strongest, competitive world Top4 and dominance over bottom teams')
result=dict(status='SERVER_AND_SIMULATION_PASS_DEVICE_UNTESTED',device_tested=False,native_readiness_stubbed=True,checks=checks,pair_distributions=pairs)
(r/'worlds-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
