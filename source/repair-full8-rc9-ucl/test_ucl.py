import copy,json,sqlite3,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import *
def fails(fn):
 try:fn()
 except UclError:return
 raise AssertionError('invalid operation accepted')
def run():
 doc=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text());teams=doc['teams'];draws=doc['draws']
 for d in draws:
  validate_draw(teams,d['rounds'])
  bad=copy.deepcopy(d['rounds']);bad[0][0]=bad[0][1];fails(lambda:validate_draw(teams,bad))
 for cutoff in [0,8]:
  s=new(teams,draws[0]['rounds'],teams[0]['team_id'],0)
  for day in range(1,9):
   for m in current_matches(s):m['result']=simulate(s,m)
   if day==8:s['own']=table(s)[cutoff]['team_id']
   transition(s)
  advance_cpu(s);own=s['own']
  while s['stage']not in ['CHAMPION','ELIMINATED']:
   m=own_match(s);assert m is not None
   # Player wins each leg; no penalty goals invented or required here.
   result=dict(home=5 if m['home']==own else 0,away=5 if m['away']==own else 0)
   apply(s,m['id'],result)
  assert s['champion']==own and len(s['matches'])==189
  assert sum(own in(m['home'],m['away'])for m in s['matches'])==(15 if cutoff==0 else 17)
  assert all(m['result']is not None for m in s['matches'])
 s=new(teams,draws[0]['rounds'],teams[0]['team_id'],0);a,b=teams[0]['team_id'],teams[1]['team_id'];add_ties(s,'PLAYOFFS',[(a,b)],True);one,two=s['matches'][-2:]
 one['result']=score(s,one,0,1);fails(lambda:score(s,two,0,1));valid=score(s,two,0,1,5,4);assert valid['pk_home']==5
 fails(lambda:score(s,two,1,0,5,4));fails(lambda:score(s,one,0,0,5,4));fails(lambda:score(s,two,0,1,0,0))
 one['result']=score(s,one,2,1);fails(lambda:score(s,two,3,2));assert score(s,two,3,2,5,4)['pk_home']==5
 # SQLite resume and a durable receipt, not a RAM-only duplicate guard.
 with tempfile.TemporaryDirectory()as d:
  p=Path(d)/'test.sqlite3';c=sqlite3.connect(p);st=Store(c);s=st.create(teams,draws[0]['rounds'],a,0);m=own_match(s);st.reserve('123456',{'test':True});fails(lambda:st.finish('123456',dict(home=1,away=0)));st.start('123456');receipt=st.finish('123456',dict(home=1,away=0));snapshot=c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0];c.close();c=sqlite3.connect(p);st=Store(c);assert st.finish('123456',dict(home=99,away=99))==receipt;assert c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]==snapshot;fails(lambda:st.finish('999',dict(home=0,away=0)));c.close()

 # Session replay must preserve its original roster snapshot and reject ID reuse.
 c=sqlite3.connect(':memory:');st=Store(c);fails(lambda:st.reserve('1',{}))
 st.create(teams,draws[0]['rounds'],a,0);first=st.reserve(9007199254740993,{'roster':'original'})
 assert first['game_id']=='9007199254740993'
 assert st.reserve('9007199254740993',{'roster':'changed'})==first
 st.start('9007199254740993');st.finish('9007199254740993',dict(home=2,away=0))
 snapshot=c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]
 fails(lambda:st.reserve('9007199254740993',{'roster':'wrong fixture'}))
 assert c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]==snapshot
 for invalid in [True,1.5,'1.5','01','0',str(2**63)]:fails(lambda:st.reserve(invalid,{}))
 # Failed aggregate settlement rolls back and keeps a resumable pending session.
 state=st.get();field=[a,b]+[t['team_id']for t in teams if t['team_id']not in(a,b)][:6];add_ties(state,'QF',list(zip(field[::2],field[1::2])),True)
 for game in current_matches(state):game['result']=score(state,game,2,1)if a in(game['home'],game['away'])else simulate(state,game)
 transition(state)
 with st.transaction():st.save(state)
 st.reserve('987654321',{});st.start('987654321');before=c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]
 fails(lambda:st.finish('987654321',dict(home=3,away=2)))
 assert c.execute('SELECT state FROM ucl_lp_seasons').fetchone()[0]==before
 assert c.execute('SELECT receipt FROM ucl_lp_sessions WHERE game=?',('987654321',)).fetchone()[0]is None
 st.finish('987654321',dict(home=3,away=2,pk_home=5,pk_away=4));c.close()
 return dict(passed=True,draws=len(draws),league_matches=144,total_matches=189,champion_routes=[15,17],two_leg_aggregate_shootout_checks=True,sqlite_restart_idempotency=True,session_collision_and_roster_replay=True,invalid_aggregate_result_rolls_back=True,phone_verified=False)
if __name__=='__main__':print(json.dumps(run(),indent=2))
