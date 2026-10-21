"""Independent expected slot layouts from the user's live UI observations."""
from pathlib import Path
import json,hashlib,tempfile,sys
r=Path(__file__).parent;c=json.loads((r/'myleague_custom.json').read_text());role_names=['GK','CB','LB','RB','DMF','CMF','LMF','RMF','AMF','LWF','RWF','SS','CF']
# These are the slot labels seen on the device, independent of generated JSON.
contracts={'1220':['GK','CB','CB','RB','LB','DMF','CMF','CMF','RWF','LWF','CF'],'1222':['GK','CB','CB','RB','LB','DMF','CMF','CMF','RWF','LWF','CF'],'5317':['GK','CB','CB','RB','LB','DMF','CMF','AMF','RWF','LWF','CF'],'131':['GK','CB','CB','RB','LB','DMF','CMF','RMF','LWF','AMF','CF'],'1987':['GK','CB','CB','RB','LB','DMF','CMF','CF','LMF','AMF','RMF'],'1986':['GK','CB','CB','RB','LB','CMF','CMF','AMF','RWF','LWF','CF'],'1985':['GK','CB','CB','CB','LMF','DMF','CMF','RMF','LWF','AMF','CF']}
expected={'1220':{'Cristiano Ronaldo':'LWF','Karim Benzema':'CF','Gareth Bale':'RWF','Daniel Carvajal':'RB','Raphaël Varane':'CB'},'1222':{'Neymar Jr':'LWF','Luis Suárez':'CF','Sergi Roberto':'RB','Samuel Umtiti':'CB'},'5317':{'Joshua Kimmich':'RB','Mats Hummels':'CB'},'131':{'Sergio Agüero':'CF','David Silva':'AMF','Leroy Sané':'RMF','Vincent Kompany':'CB','Kyle Walker':'RB','Ederson Moraes':'GK'},'1987':{'Philippe Coutinho':'AMF','Roberto Firmino':'CF','Virgil van Dijk':'CB','T. Alexander-Arnold':'RB'},'1986':{'Zlatan Ibrahimović':'CF','Edinson Cavani':'LWF','Julian Draxler':'AMF','Ángel Di María':'RWF','Dani Alves':'RB','Marquinhos':'CB'},'1985':{'Harry Kane':'CF','Lucas Moura':'RMF','Christian Eriksen':'AMF'}}
for tid,layout in contracts.items():
 t=c['classic_teams'][tid];actual={s['name']:layout[i]for i,s in enumerate(t['slots'][:11])}
 for name,wanted in expected[tid].items():assert actual[name]==wanted,(tid,name,actual[name],wanted)
 assert [role_names[row[0]]for row in t['formation']]==layout
captains=['Antoine Griezmann','Sergio Ramos','Francesco Totti','Giorgio Chiellini','Manuel Neuer','Eden Hazard','Lionel Messi','Vincent Kompany','Wayne Rooney','Virgil van Dijk','Marquinhos','Harry Kane']
penalties=['Antoine Griezmann','Cristiano Ronaldo','Francesco Totti','Paulo Dybala','Robert Lewandowski','Eden Hazard','Lionel Messi','Sergio Agüero','Wayne Rooney','Mohamed Salah','Zlatan Ibrahimović','Harry Kane']
rows=[]
for tid,cap,pk in zip(['1219','1220','2621','2365','5317','1221','1222','131','132','1987','1986','1985'],captains,penalties):
 t=c['classic_teams'][tid];assert t['slots'][t['responsibilities']['captain']]['name']==cap and t['slots'][t['responsibilities']['penalty']]['name']==pk
 assert t['set_piece_taker'][5]==t['responsibilities']['penalty'];assert len({s['shirt']for s in t['slots']})==len(t['slots'])
 rows.append(dict(team=t['name'],captain=cap,penalty=pk))
assert next(s for s in c['classic_teams']['131']['slots']if s['name']=='Claudio Bravo')['starting']is False
assert all(p['all_outfield_positions']is False for p in c['classic_profiles'].values())
# Loader verifies the same exact file, but rechecks metadata after a replacement.
sys.path.insert(0,str(r));import select_team_runtime as rt
with tempfile.TemporaryDirectory()as d:
 p=Path(d)/'engine';p.write_bytes(b'original');assert rt.digest(p)==hashlib.sha256(b'original').hexdigest();assert rt.digest(p)==rt.digest(p)
 p.write_bytes(b'replaced-longer');assert rt.digest(p)==hashlib.sha256(b'replaced-longer').hexdigest()
report=dict(status='LIVE_SLOT_AND_ROLE_CONTRACT_PASS',phone_verified=False,observed_slot_layouts=contracts,roles=rows,shirt_numbers_unique_per_team=True,ederson_starts=True,all_position_proficiency_disabled=True,checks=['configured roster order now matches reported native slot layout; identity/formation references changed together','captain and penalty identity checks independent of generated index values','keeper Ederson starts, Bravo remains bench','source position/proficiency retained; no global all-position flag','hash verification cache invalidates when file metadata changes'],limits='Live observed layout is used as the contract; final Android formation UI and any later automatic substitutions still need device verification')
(r/'live-contract-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
