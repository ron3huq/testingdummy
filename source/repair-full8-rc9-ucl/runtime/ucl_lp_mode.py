"""Versioned 36-club UCL season. Pure stdlib; no game imports or personal save files.
2024/25 bracket and home-leg policy, native club pool/game-strength pots.
"""
import copy,hashlib,json,random,sqlite3,uuid
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
RULESET='ucl-2024-25-format-game-pots-v1'
TWO_LEGS={'PLAYOFFS','R16','QF','SF'}
class UclError(ValueError):pass

def number(v,hi=99):
 if type(v)is not int or not 0<=v<=hi:raise UclError('invalid score')
 return v

def session_key(value):
 if type(value)is int:value=str(value)
 if not isinstance(value,str)or not value.isascii()or not value.isdecimal()or not 0<int(value)<2**63 or str(int(value))!=value:raise UclError('invalid native session ID')
 return value

def rng(*parts):return random.Random(hashlib.sha256('|'.join(map(str,parts)).encode()).digest())
def validate_draw(teams,rounds):
 ids={t['team_id']for t in teams};by={t['team_id']:t for t in teams}
 if len(teams)!=36 or len(ids)!=36 or len(rounds)!=8:raise UclError('36 clubs and eight rounds required')
 pairs=set();seen={t:[]for t in ids}
 for games in rounds:
  if len(games)!=18 or Counter(x for g in games for x in g)!=Counter({t:1 for t in ids}):raise UclError('invalid matchday')
  for h,a in games:
   pair=frozenset((h,a))
   if len(pair)!=2 or pair in pairs or by[h]['association']==by[a]['association']:raise UclError('duplicate or same-association opponent')
   pairs.add(pair);seen[h].append((a,'H'));seen[a].append((h,'A'))
 for t,op in seen.items():
  if Counter((by[o]['pot'],side)for o,side in op)!=Counter({(p,s):1 for p in range(1,5)for s in ('H','A')}):raise UclError('pot/home/away imbalance')
  if max(Counter(by[o]['association']for o,s in op).values())>2:raise UclError('association limit exceeded')
 return True

def table(s):
 rows={t['team_id']:dict(team_id=t['team_id'],played=0,points=0,gf=0,ga=0,away_goals=0,wins=0,away_wins=0,discipline=0,opponents=[])for t in s['teams']}
 for m in s['matches']:
  if m['stage']!='LEAGUE_PHASE':continue
  h,a=rows[m['home']],rows[m['away']];h['opponents'].append(m['away']);a['opponents'].append(m['home'])
  if m.get('result')is None:continue
  r=m['result'];hg,ag=r['home'],r['away']
  for row,gf,ga,d in [(h,hg,ag,r.get('discipline_home',0)),(a,ag,hg,r.get('discipline_away',0))]:
   row['played']+=1;row['gf']+=gf;row['ga']+=ga;row['discipline']+=d;row['points']+=3 if gf>ga else int(gf==ga);row['wins']+=int(gf>ga)
  a['away_goals']+=ag;a['away_wins']+=int(ag>hg)
 for row in rows.values():
  op=[rows[t]for t in row['opponents']];row['gd']=row['gf']-row['ga'];row['opponent_points']=sum(r['points']for r in op);row['opponent_gd']=sum(r['gf']-r['ga']for r in op);row['opponent_goals']=sum(r['gf']for r in op)
 # Missing official coefficients are explicit game-strength proxies, not team IDs.
 strength={t['team_id']:t['strength']for t in s['teams']};lots={t['team_id']:rng(s['seed'],'ranking-lot',t['team_id']).random()for t in s['teams']}
 def key(r):return(-r['points'],-r['gd'],-r['gf'],-r['away_goals'],-r['wins'],-r['away_wins'],-r['opponent_points'],-r['opponent_gd'],-r['opponent_goals'],r['discipline'],-strength[r['team_id']],lots[r['team_id']])
 ranked=sorted(rows.values(),key=key)
 for i,row in enumerate(ranked):row['rank']=i+1
 return ranked

def new(teams,rounds,own,seed,level='NORMAL'):
 validate_draw(teams,rounds)
 if own not in {t['team_id']for t in teams}:raise UclError('selected club is outside the validated UCL field')
 if level not in {'VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND'}:raise UclError('invalid difficulty')
 s=dict(schema_version=1,ruleset=RULESET,mode='UCL_LP',season_uuid=uuid.uuid4().hex,seed=seed,own=own,cpu_level=level,stage='LEAGUE_PHASE',round=1,teams=copy.deepcopy(teams),matches=[],ties=[],stats={},active=None,champion=None,eliminated=False)
 for day,games in enumerate(rounds,1):
  for h,a in games:s['matches'].append(dict(id='LP-%d-%d-%d'%(day,h,a),stage='LEAGUE_PHASE',round=day,leg=1,home=h,away=a,result=None))
 return s

def current_matches(s):return[m for m in s['matches']if m['stage']==s['stage']and m['round']==s['round']]
def own_match(s):return next((m for m in current_matches(s)if s['own']in(m['home'],m['away'])),None)
def tie_for(s,m):return next((t for t in s['ties']if t['id']==m.get('tie')),None)
def needs_decision(s,m):
 if m['stage']=='FINAL':return True
 if m['stage']not in TWO_LEGS or m['leg']!=2:return False
 return True

def first_leg(s,m):
 t=tie_for(s,m)
 return next(x for x in s['matches']if x['id']==t['matches'][0])if t else None

def aggregate_before(s,m):
 first=first_leg(s,m)
 if not first:return(0,0)
 if first.get('result')is None:raise UclError('first leg has no valid result')
 r=first['result'];return(r['away'],r['home'])

def valid_shootout(home,away):
 # Reachable terminal scores under five kicks each then paired sudden death.
 # Low scores such as1-0/2-0 are legal;5-2 would have stopped earlier.
 if type(home)is not int or type(away)is not int or min(home,away)<0 or home==away:return False
 if max(home,away)>5:return abs(home-away)==1
 pending={(0,0,0,0)};terminal=set()
 for kick in range(10):
  following=set()
  for hs,aws,h,a in pending:
   for goal in(0,1):
    nhs,naws,nh,na=(hs+1,aws,h+goal,a)if kick%2==0 else(hs,aws+1,h,a+goal)
    if nh>na+5-naws or na>nh+5-nhs:terminal.add((nh,na))
    else:following.add((nhs,naws,nh,na))
  pending=following
 # A tied initial series can be any0..5; a sudden-death pair can finish1-0.
 for tied in range(6):terminal.update([(tied+1,tied),(tied,tied+1)])
 return(home,away)in terminal or(away,home)in terminal

def score(s,m,home,away,pk_home=None,pk_away=None,discipline_home=0,discipline_away=0):
 h,a=number(home),number(away);dh,da=number(discipline_home,999),number(discipline_away,999)
 bh,ba=aggregate_before(s,m)if m['leg']==2 else(0,0)
 level=needs_decision(s,m)and h+bh==a+ba
 if level:
  ph,pa=number(pk_home),number(pk_away)
  # Reject impossible/unresolved shootout receipts; no invented penalties.
  if not valid_shootout(ph,pa):raise UclError('valid deciding shootout required')
 elif pk_home is not None or pk_away is not None:raise UclError('shootout is not permitted for this fixture')
 else:ph=pa=None
 return dict(home=h,away=a,pk_home=ph,pk_away=pa,discipline_home=dh,discipline_away=da)

def simulate(s,m):
 r=rng(s['season_uuid'],s['seed'],m['id']);strength={t['team_id']:t['strength']for t in s['teams']};gap=max(-15,min(15,strength[m['home']]-strength[m['away']]));h=sum(r.random()<(.22+gap*.006)for _ in range(6));a=sum(r.random()<(.18-gap*.006)for _ in range(6));bh,ba=aggregate_before(s,m)if m['leg']==2 else(0,0);ph=pa=None
 if needs_decision(s,m)and h+bh==a+ba:
  # CPU extra time and shootout; persisted once in the same transaction as the round.
  h+=int(r.random()<.25);a+=int(r.random()<.23)
  if h+bh==a+ba:ph,pa=(5,4)if r.random()<.5 else(4,5)
 return score(s,m,h,a,ph,pa)

def add_ties(s,stage,pairs,seeded=False):
 s['stage']=stage;s['round']=1
 for k,(a,b)in enumerate(pairs):
  tid=stage+'-'+str(k);two=stage in TWO_LEGS
  # Seeded club a hosts leg two. QF/SF order was drawn once, not drawn after results.
  if not seeded and rng(s['seed'],stage,k,'home-order').random()<.5:a,b=b,a
  games=[(b,a),(a,b)]if two else[(a,b)]
  tie=dict(id=tid,stage=stage,teams=[a,b],matches=[],winner=None)
  for leg,(h,a)in enumerate(games,1):
   mid=tid+'-'+str(leg);tie['matches'].append(mid);s['matches'].append(dict(id=mid,tie=tid,stage=stage,round=leg,leg=leg,home=h,away=a,result=None))
  s['ties'].append(tie)

def settle_ties(s):
 for t in s['ties']:
  if t['stage']!=s['stage']:continue
  games=[next(m for m in s['matches']if m['id']==mid)for mid in t['matches']]
  if any(m['result']is None for m in games):raise UclError('unfinished tie')
  goals=Counter()
  for m in games:goals[m['home']]+=m['result']['home'];goals[m['away']]+=m['result']['away']
  a,b=t['teams'];last=games[-1];r=last['result']
  t['winner']=a if goals[a]>goals[b]else b if goals[b]>goals[a]else last['home']if r['pk_home']>r['pk_away']else last['away']

def transition(s):
 if any(m['result']is None for m in current_matches(s)):raise UclError('unfinished round')
 if s['stage']=='LEAGUE_PHASE':
  if s['round']<8:s['round']+=1;return
  ranks=[r['team_id']for r in table(s)];s['league_ranks']=ranks;s['eliminated']=s['own']not in ranks[:24];s['draw_rank_pairs']={}
  # Paired ranks are drawn into opposite halves once.
  for start in [1,3,5,7,9,11,13,15,17,19,21,23]:
   pair=ranks[start-1:start+1];rng(s['seed'],'rank-pair',start).shuffle(pair);s['draw_rank_pairs'][str(start)]=pair
  p=s['draw_rank_pairs'];pairs=[]
  for high,low in [(9,23),(11,21),(13,19),(15,17)]:pairs.extend(zip(p[str(high)],p[str(low)]))
  add_ties(s,'PLAYOFFS',pairs,True);return
 if s['stage']in TWO_LEGS and s['round']==1:s['round']=2;return
 settle_ties(s);ties=[t for t in s['ties']if t['stage']==s['stage']];winners=[t['winner']for t in ties]
 if s['stage']=='FINAL':s['champion']=winners[0];s['stage']='CHAMPION'if s['own']==winners[0]else'ELIMINATED';s['eliminated']=s['own']!=winners[0];return
 if s['stage']=='PLAYOFFS':
  p=s['draw_rank_pairs'];pwin={high:winners[j*2:j*2+2]for j,high in enumerate([9,11,13,15])};slot={}
  for high,playoff in [(1,15),(3,13),(5,11),(7,9)]:
   for i in range(2):slot[high+i]=(p[str(high)][i],pwin[playoff][i])
  pairs=[slot[r]for r in [1,8,4,5,2,7,3,6]];add_ties(s,'R16',pairs,True)
 else:add_ties(s,{'R16':'QF','QF':'SF','SF':'FINAL'}[s['stage']],list(zip(winners[::2],winners[1::2])))
 if s['own']not in {t for m in current_matches(s)for t in(m['home'],m['away'])}:s['eliminated']=True

def advance_cpu(s):
 # Bypass playoffs for a top-eight club. Continue the bracket after elimination.
 while s['stage']not in('CHAMPION','ELIMINATED')and own_match(s)is None:
  for m in current_matches(s):
   if m['result']is None:m['result']=simulate(s,m)
  transition(s)

def apply(s,fixture,result):
 if s['active']and s['active'].get('fixture')!=fixture:raise UclError('fixture does not match pending native session')
 m=own_match(s)
 if m is None or m['id']!=fixture or m['result']is not None:raise UclError('fixture is not playable')
 m['result']=score(s,m,**result)
 for game in current_matches(s):
  if game['result']is None:game['result']=simulate(s,game)
 s['active']=None;transition(s);advance_cpu(s)

class Store:
 def __init__(self,conn):
  self.conn=conn
  if conn.in_transaction:raise UclError('save transaction already active')
  conn.executescript('CREATE TABLE IF NOT EXISTS ucl_lp_seasons(id TEXT PRIMARY KEY,state TEXT NOT NULL);CREATE TABLE IF NOT EXISTS ucl_lp_sessions(game TEXT PRIMARY KEY,season TEXT NOT NULL,fixture TEXT NOT NULL,started INTEGER NOT NULL DEFAULT 0,receipt TEXT,UNIQUE(season,fixture));CREATE TABLE IF NOT EXISTS ucl_lp_selection(singleton INTEGER PRIMARY KEY CHECK(singleton=1),season TEXT);')
 @contextmanager
 def transaction(self):
  if self.conn.in_transaction:raise UclError('another save transaction is active')
  self.conn.execute('BEGIN IMMEDIATE')
  try:yield;self.conn.commit()
  except Exception:self.conn.rollback();raise
 def get(self,sid=None):
  if sid is None:
   row=self.conn.execute('SELECT season FROM ucl_lp_selection WHERE singleton=1').fetchone();sid=row[0]if row else None
  row=self.conn.execute('SELECT state FROM ucl_lp_seasons WHERE id=?',(sid,)).fetchone()
  return json.loads(row[0])if row else None
 def save(self,s):self.conn.execute('INSERT OR REPLACE INTO ucl_lp_seasons VALUES(?,?)',(s['season_uuid'],json.dumps(s,separators=(',',':'))))
 def create(self,teams,rounds,own,seed,level='NORMAL'):
  s=new(teams,rounds,own,seed,level)
  with self.transaction():
   old=self.get()
   if old and old.get('active'):raise UclError('finish or explicitly abandon the pending match before creating a season')
   self.save(s);self.conn.execute('INSERT OR REPLACE INTO ucl_lp_selection VALUES(1,?)',(s['season_uuid'],))
  return s
 def reserve(self,game,native):
  game=session_key(game)
  if not isinstance(native,dict):raise UclError('invalid native session payload')
  with self.transaction():
   s=self.get()
   if not s:raise UclError('no selected UCL season')
   m=own_match(s)
   if m is None:raise UclError('no playable fixture')
   active=s.get('active')
   if active and session_key(active['game_id'])!=game:raise UclError('pending fixture already reserved')
   previous=self.conn.execute('SELECT season,fixture,receipt FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
   if previous:
    if previous[0]!=s['season_uuid']or previous[1]!=m['id']or previous[2]is not None:raise UclError('native session ID already belongs to another fixture')
    if not active or active.get('fixture')!=m['id']:raise UclError('pending session state is inconsistent')
    return copy.deepcopy(active)
   try:self.conn.execute('INSERT INTO ucl_lp_sessions(game,season,fixture)VALUES(?,?,?)',(game,s['season_uuid'],m['id']))
   except sqlite3.IntegrityError as error:raise UclError('fixture already has a native session')from error
   s['active']=dict(game_id=game,fixture=m['id'],native=copy.deepcopy(native));self.save(s);return copy.deepcopy(s['active'])
 def finish(self,game,result,reply=None,player_events=None):
  game=session_key(game)
  with self.transaction():
   row=self.conn.execute('SELECT season,fixture,started,receipt FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
   if not row or not row[2]:raise UclError('native match was not started')
   if row[3]is not None:return json.loads(row[3])
   s=self.get(row[0]);active=s.get('active')if s else None
   if not active or session_key(active['game_id'])!=game or active.get('fixture')!=row[1]:raise UclError('result does not belong to the pending native session')
   if player_events is not None:
    from ucl_lp_stats import record
    fixture=own_match(s);checked=score(s,fixture,**result);record(s,fixture,checked,active['native'].get('ucl_rosters',{}),player_events)
   apply(s,row[1],result);self.save(s);receipt=dict(season=s['season_uuid'],fixture=row[1],reply=reply);self.conn.execute('UPDATE ucl_lp_sessions SET receipt=? WHERE game=?',(json.dumps(receipt),game));return receipt
 def finish_native(self,request,reply=None,player_events=None):
  from ucl_lp_result import game_id,decode
  game=game_id(request)
  row=self.conn.execute('SELECT season,fixture,started,receipt FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
  if not row or not row[2]:raise UclError('native match was not started')
  if row[3]is not None:return json.loads(row[3])
  state=self.get(row[0]);fixture=own_match(state)if state else None
  if fixture is None or fixture['id']!=row[1]:raise UclError('native fixture mismatch')
  result=decode(state,fixture,request)
  return self.finish(game,result,reply,player_events)
 def start(self,game):
  game=session_key(game)
  with self.transaction():
   row=self.conn.execute('SELECT season,fixture,receipt FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
   if not row or row[2]is not None:raise UclError('session is not pending')
   s=self.get(row[0]);active=s.get('active')if s else None
   if not active or session_key(active['game_id'])!=game or active.get('fixture')!=row[1]:raise UclError('session mismatch')
   self.conn.execute('UPDATE ucl_lp_sessions SET started=1 WHERE game=?',(game,))
