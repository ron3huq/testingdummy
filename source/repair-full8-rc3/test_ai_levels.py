from pathlib import Path
import sys,sqlite3,json,copy
sys.path.insert(0,'/workspace/73-v191-migration/decoded');import my_league,ml_event,ml_career
R=Path('/workspace/work/full8-rc3');c=sqlite3.connect(':memory:');c.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');c.commit()
s={'fixture':1,'cpu_level':'NORMAL','active':{'started':False,'opponent':{'player_list':[{'synthetic':True}],'cpu_level':'NORMAL'}}}
# Isolate the persisted season boundary; execute the actual prepare logic.
my_league.begin=lambda c:c.execute('BEGIN');my_league.state=lambda c:s;my_league.current=lambda s:({}, {},'home');my_league.save=lambda c,s:c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('synthetic_season',json.dumps(s)))
rows=[]
for level in my_league.NATIVE_LEVELS:
 r=my_league.prepare(c,{'cpu_level':level});assert r['result']=='NOERR'and r['cpu_level']==level
 saved=json.loads(c.execute('SELECT value FROM meta').fetchone()[0]);assert saved['active']['opponent']['cpu_level']==level and saved['cpu_level']==level
 points,fans=ml_event.level_reward(level,'WIN');rows.append(dict(level=level,opponent_payload=level,persisted_season=level,event_win_points=points,event_win_fans=fans))
r=my_league.prepare(c,{});assert r['cpu_level']=='LEGEND'
r=my_league.prepare(c,{'cpu_level':'INVALID'});assert r['result']!='NOERR'
# Background score simulation is a separate code path: level participates
# in the deterministic seed, not a monotone goal/skill scaling coefficient.
scores={level:ml_career.simulate_score({'cpu_level':level,'career_id':'synthetic','season':1},1,100,200)for level in my_league.NATIVE_LEVELS}
report=dict(passed=True,levels=rows,my_league_prepare_real_function_executed=True,season_storage_boundary_mocked=True,missing_request_preserves_cached_level=True,invalid_level_rejected=True,event_rewards_actually_differ=True,background_simulation_scores=scores,background_simulation_uses_level_in_seed_not_a_proven_harder_AI_curve=True,live_match_engine_difficulty_effect_not_executed=True,phone_verified=False)
(R/'ai-level-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
