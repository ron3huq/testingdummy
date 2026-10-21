from pathlib import Path
import json,sys,sqlite3,tempfile,hashlib,copy
r=Path(__file__).parent;g=r.parent/'android/user-gateway';sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_worlds as w,myleague_realism as model,my_league as league,club_store as store,ziru_data,gate_logic,native_overall
class Bridge:
 mask=63;snow=63;status=1;context=0;last=None
 @classmethod
 def activate_context(cls,cid):cls.context=cid
 @classmethod
 def stadium_mask(cls,snow=False):return cls.snow if snow else cls.mask
 @classmethod
 def set_environment(cls,cid,stadium,snow=False):cls.context=cid;cls.last=(cid,stadium,snow);return 2 if not stadium else cls.status
 @staticmethod
 def ensure_native_team(t):return 1
w.NATIVE_BRIDGE=Bridge;model.ATTRS=g/'outputs/reference/external-attrs';model.install();c=w.config();src=g/'outputs/efootball/local-club.sqlite3';digest=hashlib.sha256(src.read_bytes()).hexdigest();cases=[]
for season in range(1,31):
 for fx in range(1,35):
  s=dict(season=season,fixture=fx,competition_id=518,team_id=1220)
  a=w.environment_for(s);assert a==w.environment_for(copy.deepcopy(s));assert a['stadium_id'] in [1,7,30,51,52,85] and a['stadium_id']!=100
  if 8<=fx<=14:assert a['weather']=='WEATHER_TYPE_SNOW' and a['season_type']=='SEASON_TYPE_WINTER'
with tempfile.TemporaryDirectory() as tmp:
 conn=sqlite3.connect(Path(tmp)/'test.db');conn.row_factory=sqlite3.Row;ro=sqlite3.connect(src.as_uri()+'?mode=ro',uri=True);ro.backup(conn);ro.close();original=[tuple(x) for x in conn.execute('select * from gameplayers order by rowid')]
 for cid,tid in [(518,1220),(566,52),(122,108)]:
  out=league.select(conn,{},dict(rqid='env-'+str(cid),select_team_id=tid,select_compe_unit_id=cid),session_token='environment');assert out['result']=='NOERR'
  for fixture in [1,7,8,14,15]:
   for available,snow,expected in [(63,63,'snow-capable'),(63,0,'snow-unavailable'),(1,1,'single-installed'),(0,0,'none-installed')]:
    Bridge.mask=available;Bridge.snow=snow;Bridge.status=1
    s=league.state(conn);s.update(fixture=fixture,active=None);league.save(conn,s);conn.commit()
    preview=league.info(conn,ziru_data.season_info(),dict(msgid='CMD_GET_SEASON_INFO',rqid='info'))
    prep=league.prepare(conn,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid=f'{cid}-{fixture}-{expected}',cpu_level='NORMAL',match_category='SEASON'),session_token='environment');assert prep['result']=='NOERR',(cid,fixture,expected,prep)
    s=league.state(conn);env=s['active']['environment'];assert (env['weather'],env['season_type'],env['time_zone'])==tuple(preview[k] for k in ['weather','season_type','time_zone'])
    if 8<=fixture<=14:
     assert env['season_type']=='SEASON_TYPE_WINTER'
     if snow:assert env['weather']=='WEATHER_TYPE_SNOW' and env['snow_applied']
     else:assert env['requested_weather']=='WEATHER_TYPE_SNOW' and env['weather']=='WEATHER_TYPE_FINE' and not env['snow_applied']
    if available:
     assert env['stadium_id'] in [1,7,30,51,52,85] and env['stadium_id']!=100
     if available==1:assert env['stadium_id']==1
    else:assert env['stadium_id']==0 and not env['stadium_applied']
    entries=gate_logic.GateLogic({},conn=conn)._home_entries(league.start_refs(conn,{}));req=dict(msgid='CMD_START_GAME',rqid='start-env',game_id=prep['game_id'],match_category='SEASON',user_id=1)
    start=league.start(conn,{},req,entries);assert start['result']=='NOERR'
    ownside='home' if s['active']['side']=='HOME' else 'away';wire=start['squad_data_'+ownside]['player_list'];lo,hi=(80,86) if cid==566 else (87,95)
    assert all(lo<=native_overall.rating(p['parameters'],p['parameters'][0])<=hi for p in wire)
    if str(tid) in c['visual_aliases']:
     assert start['uniform_list_'+ownside]['base_team_id']==c['visual_aliases'][str(tid)]
    before=copy.deepcopy(league.state(conn)['active']['environment']);again=league.info(conn,ziru_data.season_info(),dict(msgid='CMD_GET_SEASON_INFO',rqid='info2'));assert league.state(conn)['active']['environment']==before
    assert tuple(again[k] for k in ['weather','season_type','time_zone'])==tuple(before[k] for k in ['weather','season_type','time_zone'])
    cases.append((cid,fixture,expected))
 # Optional hook failure is reported without turning an otherwise valid match into C_RTMC_9999.
 Bridge.mask=63;Bridge.snow=63;Bridge.status=20;s=league.state(conn);s.update(active=None,fixture=15);league.save(conn,s);conn.commit();prep=league.prepare(conn,dict(msgid='CMD_GET_VSCOM_OPPONENT',rqid='hook-absent',match_category='SEASON'),session_token='environment');assert prep['result']=='NOERR';assert league.state(conn)['active']['environment']['native_environment_error']==20
 assert [tuple(x) for x in conn.execute('select * from gameplayers order by rowid')]==original
 assert conn.execute('pragma quick_check').fetchone()[0]=='ok'
assert hashlib.sha256(src.read_bytes()).hexdigest()==digest
report=dict(status='ENVIRONMENT_GATEWAY_PASS',device_tested=False,native_assets_and_hooks_stubbed=True,deterministic_draws=30*34,actual_gateway_cases=len(cases),checks=['info/prepare/START share weather/season/time; saved active draw stable','8–14 request winter/snow when supported; unsupported snow explicitly falls back to fine, no fake enable','six permitted stage IDs only; unsupported/missing assets and hook failures preserve baseline launch with diagnostics','own START neutral OVR in requested general/Belgium range; original inventory and DB unchanged','classic controlled-kit IDs refer to original donor club, not Scottish kit ID'],limits='Does not render rain/snow/stadiums; unavailable assets are not created. In supplied source all six snow capability flags are zero.')
(r/'environment-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
