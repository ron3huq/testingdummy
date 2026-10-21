"""Entry/prepare/START must not call any native stadium API, including legacy state."""
from pathlib import Path
import sys,json,sqlite3,tempfile,hashlib,copy
r=Path(__file__).parent;g=r.parent/'android/user-gateway';sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_worlds as w,myleague_realism as model,my_league as league,club_store as store,gate_logic,ziru_data
class Bridge:
 contexts=[]
 @classmethod
 def activate_context(cls,cid):cls.contexts.append(cid)
 @staticmethod
 def ensure_native_team(t):return 1
 @staticmethod
 def stadium_mask(*args):raise AssertionError('stage probe reached on gateway thread')
 @staticmethod
 def set_environment(cid,stadium,snow):
  assert cid in [518,122,566,128,549] and stadium in [1,7,30,51,52,85] and not snow
  return 1
w.NATIVE_BRIDGE=Bridge;model.ATTRS=g/'outputs/reference/external-attrs';model.install();c=w.config();src=g/'outputs/efootball/local-club.sqlite3';sha=hashlib.sha256(src.read_bytes()).hexdigest();cases=[]
with tempfile.TemporaryDirectory() as tmp:
 con=sqlite3.connect(Path(tmp)/'test.db');con.row_factory=sqlite3.Row;ro=sqlite3.connect(src.as_uri()+'?mode=ro',uri=True);ro.backup(con);ro.close();inventory=[tuple(x) for x in con.execute('select * from gameplayers order by rowid')]
 logic=gate_logic.GateLogic({'CMD_GET_SEASON_INFO':ziru_data.season_info()},conn=con)
 for cid,tid in [(122,108),(566,52)]+[(518,int(t)) for t in c['classic_teams']]:
  out=league.select(con,{},dict(rqid=f'entry-{cid}-{tid}',select_team_id=tid,select_compe_unit_id=cid),session_token='entry-fix');assert out['result']=='NOERR'
  for fixture in [1,8,14,15]:
   s=league.state(con);s.update(active=None,fixture=fixture);league.save(con,s);con.commit()
   # Exercise the real command dispatcher used when tapping My League.
   for retry in range(3):
    out=logic.handle('CMD_GET_SEASON_INFO',dict(msgid='CMD_GET_SEASON_INFO',rqid=f'info-{tid}-{fixture}-{retry}'))
    assert out['result']=='NOERR' and out['weather'] in ['WEATHER_TYPE_FINE','WEATHER_TYPE_RAIN'] and out['season_type'] in ['SEASON_TYPE_SUMMER','SEASON_TYPE_WINTER'] and out['time_zone'] in ['TIME_ZONE_TYPE_DAY','TIME_ZONE_TYPE_NIGHT']
   expected=w._prepare_environment(league.state(con));assert expected['stadium_id'] in [1,7,30,51,52,85] and expected==w._prepare_environment(league.state(con))
   if 8<=fixture<=14:assert expected['season_type']=='SEASON_TYPE_WINTER' and not expected['snow_applied']
   prepared=league.prepare(con,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid=f'prep-{tid}-{fixture}',cpu_level='NORMAL',match_category='SEASON'),session_token='entry-fix');assert prepared['result']=='NOERR'
   s=league.state(con);active=s['active'];old_gid=active['game_id']
   # A persisted v7 snow/stadium preview must not reactivate the removed path.
   active['environment']=dict(weather='WEATHER_TYPE_SNOW',season_type='SEASON_TYPE_WINTER',time_zone='TIME_ZONE_TYPE_NIGHT',stadium_id=85,snow_applied=True,stadium_applied=True,version='native-hotfix-v7',fixture=fixture)
   league.save(con,s);con.commit()
   out=logic.handle('CMD_GET_SEASON_INFO',dict(msgid='CMD_GET_SEASON_INFO',rqid='legacy-info'));assert out['weather'] in ['WEATHER_TYPE_FINE','WEATHER_TYPE_RAIN'] and league.state(con)['active']['game_id']==old_gid
   entries=logic._home_entries(league.start_refs(con,{}));start=league.start(con,{},dict(msgid='CMD_START_GAME',rqid='entry-start',game_id=old_gid,match_category='SEASON',user_id=1),entries);assert start['result']=='NOERR'
   assert league.state(con)['active']['game_id']==old_gid
   cases.append((cid,tid,fixture))
 # Completed seasons must remain readable: current() intentionally rejects them.
 s=league.state(con);s.update(active=None,completed=True,fixture=len(league.fixtures(s)));league.save(con,s);con.commit()
 completed=logic.handle('CMD_GET_SEASON_INFO',dict(msgid='CMD_GET_SEASON_INFO',rqid='completed-v8'));assert completed['result']=='NOERR'
 assert [tuple(x) for x in con.execute('select * from gameplayers order by rowid')]==inventory
 assert con.execute('pragma quick_check').fetchone()[0]=='ok'
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
report=dict(status='MY_LEAGUE_ENTRY_GATEWAY_PASS',version='native-hotfix-v10',phone_verified=False,native_roster_readiness_stubbed=True,command_entry_cases=len(cases)*4,prepare_start_cases=len(cases),stage_queries_fail_if_called=True,checks=['real GateLogic CMD_GET_SEASON_INFO dispatch, repeated My League entry across14 club/league selections','rounds1/8/14/15 use stable home stadiums and four weather/time combinations; original gateway entry/prepare/start do not query engine stage objects','persisted v7 snow/stadium metadata cannot reenable native queries; game IDs preserved','all tested prepare/START replies succeed, no inline CPU squad changes','source DB and owned inventory unchanged'])
(r/'environment-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
