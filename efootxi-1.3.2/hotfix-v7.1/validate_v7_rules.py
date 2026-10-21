"""Real source-card range and additive skills, era identities and role contracts."""
from pathlib import Path
import json,sys,sqlite3,copy,collections,struct
r=Path(__file__).parent;g=r.parent/'android/user-gateway';sys.path[:0]=[str(r),str(g/'work/tools')]
import myleague_balance as b,native_overall as o,myleague_worlds as w
c=w.config();con=sqlite3.connect((g/'outputs/efootball/local-club.sqlite3').as_uri()+'?mode=ro',uri=True);count=0;seen=collections.Counter();extremes={cid:[100,0] for cid in [518,566]}
for pid,raw in con.execute('select card_id,payload from managed_cards'):
 d=json.loads(raw);p=d.get('parameters')
 if len(p or[])!=147:continue
 original=copy.deepcopy(d)
 for cid in [518,566]:
  v=b.project(d,cid,pid in c['messi_ids']);q=v['parameters'];rating=o.rating(q,q[0]);lo,hi=(80,86) if cid==566 else (87,95);assert lo<=rating<=hi,(pid,cid,rating)
  extremes[cid]=[min(extremes[cid][0],rating),max(extremes[cid][1],rating)]
  assert q[0:14]==p[0:14] and q[47]==p[47] and q[43]==p[43] and q[33]==p[33]
  # Every original skill is retained, except the exact two classic replacements.
  assert all(q[i]>=p[i] for i in range(70,144) if cid!=518 or i not in (72,108))
  if cid==518:
   assert q[72]==q[108]==0
   if p[72]:assert q[116]
   if p[108]:assert q[135]
  if pid in c['messi_ids']:assert q[17]==q[28]==94 and q[120] and q[116]
 assert d==original;seen[p[0]]+=1;count+=1
# Every role, including full147 boundary patterns, retains all four existing skills.
for role in range(13):
 p=[0]*147;p[0]=role;p[47]=185;p[33]=2
 for i in range(14,41):
  if i!=33:p[i]=70
 for f in [70,72,73,84,107,108,120,124,132]:p[f]=1
 d={'parameters':p,'additional_skill_id':[3,5,18,24,57],'additional_skill':[3,5,18,24,57],'is_skill_added':'YES'}
 q=b.project(d,122)['parameters'];assert all(q[i]>=p[i] for i in range(70,144))
 if role in (1,2,3):assert all(q[i] for i in [106,111,113,115])
 else:assert all(q[i]==p[i] for i in [106,111,113,115])
 q=b.project(d,518);assert q['additional_skill_id']==[74,74,18,24,57] and q['parameters'][116] and q['parameters'][135]
# Requested formation constraints use source exact IDs and real per-slot role data.
assert c['native_rosters']['1220'][8]==70373039149482 and c['native_rosters']['1220'][10]==88045755861672
lr={s['name']:s['role'] for s in c['classic_teams']['1987']['slots']}
for name,role in {'Sadio Mané':'LMF','Roberto Firmino':'CF','Mohamed Salah':'RMF','Philippe Coutinho':'AMF','Fabinho':'CMF'}.items():assert lr[name]==role
ar={s['name']:s['role'] for s in c['classic_teams']['1219']['slots']};assert ar['Jan Oblak']=='GK' and ar['Koke']=='CMF' and ar['Fernando Torres']==ar['Antoine Griezmann']=='CF'
for tid,t in c['classic_teams'].items():
 assert len(t['slots'])>=11 and sum(s['starting'] for s in t['slots'])==11
 assert sum(s['role']=='GK' for s in t['slots'][:11])==1
 assert len(set(s['shirt'] for s in t['slots']))==len(t['slots'])
 assert len(set(tuple(v[1:]) for v in t['formation']))==11
 assert all(0<=i<11 for i in t['set_piece_taker']+[t['responsibilities']['captain']])
 forbidden={'Désiré Doué','Cole Palmer','Joško Gvardiol','Enzo Fernández','Manu Koné','Wesley','Matthijs de Ligt','Aaron Wan-Bissaka','Kenan Yıldız','Weston McKennie','Douglas Luiz','Matheus Nunes','Ronald Araújo','Jeremie Frimpong','Alexis Mac Allister','Ibrahima Konaté'}
 assert not forbidden.intersection(s['source_name'] for s in t['slots'])
report=dict(status='V7_REAL_CARD_AND_ROLE_RULES_PASS',real_cards=count,position_coverage=dict(seen),neutral_ovr_ranges=extremes,classic_teams=12,classic_slots=190,skill_additions_preserve_other_flags=True,source_objects_unchanged=True,limits='Neutral source primary-position OVR, no manager/conditional boosts; football-role exceptions are documented, roster years may mix where records absent.')
(r/'v7-rules-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
