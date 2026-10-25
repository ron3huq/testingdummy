"""Custom finite agents using the shipped gateway's existing grant/receipt path.
Only named existing managed_cards are used. No player definitions or owned
instances are imported, replaced or granted during installation.
"""
import copy,functools,hashlib,json,threading
from pathlib import Path
ROOT=Path(__file__).parent
_lock=threading.RLock()

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def validate(rows):
 if not isinstance(rows,list) or len(rows)>32:raise ValueError('maximum32 packs')
 seen=set()
 for p in rows:
  aid=p.get('agent_id');title=p.get('title');ids=p.get('player_ids')
  if type(aid)is not int or not 200000<=aid<=299999 or aid in seen:raise ValueError('invalid/duplicate pack ID')
  seen.add(aid)
  if not isinstance(title,str)or not title.strip()or len(title)>80 or any(ord(c)<32 for c in title):raise ValueError('invalid pack title')
  if not isinstance(ids,list)or not 1<=len(ids)<=300 or any(not isinstance(x,str)or not x.isascii()or not x.isdecimal()or str(int(x))!=x or not 0<int(x)<2**63 for x in ids)or len(set(ids))!=len(ids):raise ValueError('invalid pack members')
 return rows

def apply(conn,rows):
 import club_store as store
 validate(rows)
 if conn.in_transaction:raise ValueError('pack installation requires a clean transaction')
 exists=conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='studio_packs'").fetchone()
 if not rows and not exists:return {'packs':0,'changed':False}
 if not conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='managed_cards'").fetchone():raise ValueError('managed card registry unavailable')
 document_hash=hashlib.sha256(canonical(rows).encode()).hexdigest()
 if store.get_meta(conn,'studio_packs_revision','')==document_hash:return {'packs':len(rows),'changed':False}
 conn.execute('BEGIN IMMEDIATE')
 try:
  # Preflight every card and every ID before any definition is changed.
  prior=dict(conn.execute('SELECT agent_id,members FROM studio_packs')) if exists else {}
  prepared=[]
  for p in rows:
   aid=p['agent_id'];members=canonical(sorted(p['player_ids'],key=int));old=conn.execute('SELECT json FROM agents WHERE agent_id=?',(aid,)).fetchone()
   if old and aid not in prior:raise ValueError('pack ID already belongs to another agent: '+str(aid))
   if aid in prior and prior[aid]!=members:raise ValueError('published membership is immutable; create a NEW pack ID: '+str(aid))
   counts=[0]*5
   for pid in p['player_ids']:
    row=conn.execute('SELECT payload FROM managed_cards WHERE card_id=?',(pid,)).fetchone()
    if not row:raise ValueError('card not registered on this device: '+pid)
    card=json.loads(row[0]);rarity=card.get('default_rarity',1)
    if str((card.get('gameplayer_id')or{}).get('id'))!=pid or type(rarity)is not int or not 1<=rarity<=5:raise ValueError('invalid registered card: '+pid)
    counts[rarity-1]+=1
   if aid in prior:
    actual=canonical(sorted((r[0] for r in conn.execute('SELECT card_id FROM managed_members WHERE agent_id=? AND weight>0',(aid,))),key=int))
    if actual!=members:raise ValueError('published membership changed outside Studio: '+str(aid))
   prepared.append((p,members,old,counts))
  template=conn.execute('SELECT json FROM agents WHERE agent_id=7000').fetchone() or conn.execute('SELECT json FROM agents ORDER BY agent_id LIMIT1'.replace('LIMIT1','LIMIT 1')).fetchone()
  if rows and not template:raise ValueError('native agent template missing')
  conn.execute('CREATE TABLE IF NOT EXISTS studio_packs(agent_id INTEGER PRIMARY KEY,members TEXT NOT NULL)')
  owned=set(prior);wanted={p['agent_id']for p in rows}
  for aid in owned-wanted:conn.execute('UPDATE managed_agents SET enabled=0 WHERE agent_id=?',(aid,))
  for p,members,old,counts in prepared:
   aid=p['agent_id'];native=json.loads(old[0]if old else template[0])
   native.update(agent_id=aid,title=p['title'].strip())
   if not old:
    native.update(agent_type='BOX_AGENT',acquired_list=[],use_count=0,player_list_total=sum(counts),base_player_count=counts,remaining_player_count=counts,can_reset='YES',pickup_list=[],banner_a_pickup_list=[],banner_c_pickup_list=[],pickup_cardtype_list=[],start_date=0,expiration_date=2147483647)
    conn.execute('INSERT INTO agents VALUES(?,?)',(aid,canonical(native)))
    conn.execute('INSERT INTO managed_agents VALUES(?,?,1,0,?)',(aid,p['title'].strip(),'LEAGUE_POSITION'))
    conn.executemany('INSERT INTO managed_members VALUES(?,?,1)',[(aid,pid)for pid in p['player_ids']])
    conn.execute('INSERT INTO studio_packs VALUES(?,?)',(aid,members))
   else:
    conn.execute('UPDATE agents SET json=? WHERE agent_id=?',(canonical(native),aid))
    conn.execute('UPDATE managed_agents SET enabled=1,name=? WHERE agent_id=?',(p['title'].strip(),aid))
  active=json.loads(store.get_meta(conn,'league_position_agent_ids','[]'))
  if not active:active=[r[0]for r in conn.execute('SELECT agent_id FROM agents ORDER BY agent_id')if r[0]not in owned|wanted]
  active=[aid for aid in active if aid not in owned|wanted]+[p['agent_id']for p in rows]
  prices=json.loads(store.get_meta(conn,'agent_price_list','[]'))
  prices=[p for p in prices if p.get('agent_id')not in owned|wanted]
  for p in rows:
   entries=[{'multiple_count':n,'price':{'can_use_coin':'YES','can_use_gp':'NO','coin_price':c,'coin_price_base':c,'gp_price':0,'gp_price_base':0}}for n,c in [(1,100),(10,900)]]
   prices.append({'agent_id':p['agent_id'],'discount_limit_count':0,'discount_use_count':0,'price_list':entries})
  store.set_meta(conn,'league_position_agent_ids',canonical(active));store.set_meta(conn,'agent_price_list',canonical(prices));store.set_meta(conn,'studio_packs_revision',document_hash)
  conn.commit();return {'packs':len(rows),'changed':True}
 except Exception:conn.rollback();raise

def status(**row):
 try:(ROOT/'myleague-packs-status.json').write_text(json.dumps(row,ensure_ascii=False,indent=2))
 except OSError:pass

def install():
 import gate_logic
 original=gate_logic.GateLogic.handle
 if getattr(original,'_studio_packs',False):return False
 @functools.wraps(original)
 def handle(self,mid,req):
  if mid in ('CMD_GET_MYCLUB_AGENTLIST','CMD_USE_MYCLUB_AGENT','CMD_GET_MYCLUB_AGENT_BOX_INFO','CMD_RESET_MYCLUB_AGENT'):
   with _lock:
    try:
     import myleague_editor_runtime as editor
     result=apply(self.conn,editor.config().get('packs',[]));status(state='READY',device_verified=False,error=None,**result)
    except Exception as exc:status(state='ERROR',device_verified=False,error=str(exc))
  return original(self,mid,req)
 handle._studio_packs=True;gate_logic.GateLogic.handle=handle
 return True
