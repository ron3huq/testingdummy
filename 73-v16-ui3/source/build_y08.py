from pathlib import Path
import json,hashlib,copy,struct
P=Path('/workspace/ronaldo-work/73-ui3');T=P/'payload/work/tools';cfg=json.loads((T/'myleague_custom.json').read_text());catalog=json.loads((P/'catalog.json').read_text());names=json.loads((P/'fullnames.json').read_text());native=set(json.loads((P/'native-ids.json').read_text()));used=set(map(str,json.loads((P/'used-cards.json').read_text())));original_used=set(used)
roles={'GK':0,'CB':1,'LB':2,'RB':3,'DMF':4,'CMF':5,'LMF':6,'RMF':7,'AMF':8,'LWF':9,'RWF':10,'SS':11,'CF':12}
fixed={'Wayne Rooney':'88037702766648','Cristiano Ronaldo':'89135066911146','Ronaldo Nazário':'88046292734664','Zinedine Zidane':'89136418985301','Thierry Henry':'88046312750111','Lionel Messi':'89136409091415','Ronaldinho Gaúcho':'89067152870864','Adriano':'89066884435465'}
# Source identity is exact. No renamed substitutes, generated players or invented card IDs.
def pick(name):
 if name in fixed:cid=fixed[name];row=next(x for x in catalog if x['id']==cid)
 else:
  rows=[r for r in catalog if r['name_en']==name and r['id']in native and r['id']not in used]
  rows.sort(key=lambda r:(r['card_type']not in ['Epic','Legendary'],-r['overall'],int(r['id'])))
  if not rows:
   matches=[(cid,v)for cid,v in names.items()if v[1]==name and cid in native and cid not in used]
   if not matches:raise ValueError('No unused actual card: '+name)
   cid=sorted(matches,key=lambda x:int(x[0]))[0][0];row={'id':cid,'position':base_positions[cid],'overall':0}
  else:row=rows[0];cid=row['id']
 assert cid in native and cid not in used,(name,cid)
 used.add(cid);return cid,row
base_positions=json.loads(Path('/workspace/ronaldo-work/73-v25-full/android/user-gateway/outputs/reference/canonical_rosters.json').read_text())['positions']
# Entries are name, role, shirt, era target OVR, X, Y. Defensive side/order and
# all formations are explicit, rather than inferred from a sorted roster.
teams={
1706:('Manchester United','MUN',100,0,[
('Edwin van der Sar','GK',1,97,3,52),('Rio Ferdinand','CB',5,98,11,70),('Jaap Stam','CB',6,97,11,34),("John O'Shea",'RB',22,93,13,88),('Denis Irwin','LB',3,95,13,16),('Darren Fletcher','DMF',24,94,23,60),('Paul Scholes','CMF',18,97,27,42),('Cristiano Ronaldo','RMF',7,98,34,85),('Ryan Giggs','LMF',11,97,34,18),('Wayne Rooney','SS',10,97,42,35),('Carlos Tévez','CF',32,96,46,65)],8,[7,7,6,8,7,7],['Brown/Vidić/Evra/Hargreaves/Carrick absent; O’Shea/Stam/Irwin/Fletcher selected from actual MU 2000s players.']),
4937:('Real Madrid CF','RMA',109,0,[
('Iker Casillas','GK',1,98,3,52),('Fabio Cannavaro','CB',13,97,11,70),('Pepe','CB',2,96,11,34),('Sergio Ramos','RB',4,97,13,88),('Roberto Carlos','LB',3,98,13,16),('Guti','CMF',14,95,25,35),('David Beckham','CMF',23,96,25,69),('Zinedine Zidane','AMF',5,98,35,52),('Luís Figo','RWF',10,97,41,87),('Raúl','SS',7,97,42,20),('Ronaldo Nazário','CF',9,98,47,52)],0,[6,4,7,6,5,10],['Fernando Hierro absent; Pepe (joined2007) selected. R9 ID corrected with user approval. Cross-era number collision: Cannavaro uses Italy13 and Pepe Portugal2, leaving Zidane5 and Roberto Carlos3.']),
1957:('Barcelona FC','BAR',108,0,[
('Marc ter Stegen','GK',1,96,3,52),('Carles Puyol','CB',5,98,11,70),('Gerard Piqué','CB',3,96,11,34),('Dani Alves','RB',2,97,13,88),('G. van Bronckhorst','LB',12,94,13,16),('Sergio Busquets','DMF',16,96,23,52),('Xavi','CMF',6,98,29,70),('Andrés Iniesta','CMF',8,98,29,34),('Lionel Messi','RWF',19,98,43,85),('Ronaldinho Gaúcho','LWF',10,98,43,18),('Samuel Eto\'o','CF',9,97,47,52)],1,[8,9,6,6,7,8],['Valdés/Pinto and Abidal absent; ter Stegen is a 2010s goalkeeper fallback, van Bronckhorst is the2003–07 left-back. Messi wears his actual2006–08 number19 and Ronaldinho10.']),
1956:('AC Milan','MIL',121,0,[
('Dida','GK',1,97,3,52),('Alessandro Nesta','CB',13,98,11,70),('Paolo Maldini','CB',3,98,11,34),('Cafu','RB',2,97,13,88),('A. Costacurta','LB',5,96,13,16),('Gennaro Gattuso','DMF',8,96,25,72),('Andrea Pirlo','DMF',21,98,24,52),('Clarence Seedorf','CMF',20,97,28,31),('Kaká','AMF',22,98,35,52),('Andriy Shevchenko','CF',7,98,45,32),('Filippo Inzaghi','CF',9,97,46,70)],2,[6,6,8,6,7,9],['Kaladze absent; Costacurta (Milan through2007, played LB/CB/RB) selected.']),
4962:('Juventus','JUV',120,1,[
('Gianluigi Buffon','GK',1,98,3,52),('Fabio Cannavaro','CB',28,97,11,70),('Giorgio Chiellini','CB',3,96,11,34),('Lilian Thuram','RB',21,97,13,88),('Gianluca Zambrotta','LB',19,96,13,16),('Edgar Davids','DMF',26,96,24,59),('Patrick Vieira','CMF',4,96,26,40),('Hasan Salihamidžić','RMF',7,93,33,87),('Pavel Nedvěd','LMF',11,97,33,17),('Alessandro Del Piero','SS',10,98,42,34),('Zlatan Ibrahimović','CF',9,96,46,65)],9,[9,9,8,8,9,9],['Montero/Camoranesi/Emerson/Tacchinardi/Trezeguet absent; Chiellini/Salihamidžić/Davids/Vieira/Ibrahimović are actual Juventus2000s replacements.']),
4964:('Chelsea FC','CHE',102,1,[
('Petr Čech','GK',1,98,3,52),('Marcel Desailly','CB',6,97,11,70),('Antonio Rüdiger','CB',2,95,11,34),('Belletti','RB',35,93,13,88),('Marcos Alonso','LB',3,93,13,16),('Claude Makélélé','DMF',4,97,22,52),('Emmanuel Petit','CMF',17,94,28,72),('Deco','CMF',20,95,28,31),('Frank Lampard','AMF',8,98,35,52),('Gianfranco Zola','SS',25,96,43,33),('Didier Drogba','CF',11,98,47,65)],8,[8,9,7,8,7,10],['Ferreira/Terry/Carvalho/Cole/Essien/Ballack absent; Belletti/Desailly/Petit/Deco are2000s Chelsea players. Rüdiger/Marcos Alonso fill missing CB/LB with user-approved2010s exceptions.']),
4938:('Liverpool FC','LIV',103,1,[
('Pepe Reina','GK',25,95,3,52),('Virgil van Dijk','CB',4,97,11,70),('Joël Matip','CB',32,94,11,34),('T. Alexander-Arnold','RB',66,95,13,88),('Andrew Robertson','LB',26,95,13,16),('Xabi Alonso','DMF',14,97,24,37),('James Milner','CMF',7,93,26,69),('Steven Gerrard','AMF',8,98,35,52),('Dirk Kuyt','RWF',18,95,41,87),('Luis García','LWF',10,94,41,18),('Fernando Torres','CF',9,98,47,52)],7,[7,7,5,5,7,7],['Requested back four and Mascherano/Riera absent; van Dijk/Matip/Trent/Robertson/Milner are approved2010s positional fallbacks. Luis García played Liverpool2004–07.']),
1950:('Inter Milan','INT',119,1,[
('Júlio César','GK',12,97,3,52),('Iván Córdoba','CB',2,96,11,70),('Marco Materazzi','CB',23,95,11,34),('Maicon','RB',13,97,13,88),('Javier Zanetti','LB',4,97,13,16),('Esteban Cambiasso','DMF',19,97,24,38),('Juan Sebastián Verón','CMF',14,95,27,69),('Wesley Sneijder','AMF',10,98,35,52),('Samuel Eto\'o','RWF',9,97,42,87),('Zlatan Ibrahimović','SS',8,97,42,20),('Adriano','CF',29,98,47,52)],4,[7,7,6,7,6,10],['Lúcio/Samuel/Chivu absent; Córdoba/Materazzi used at CB, Zanetti at LB; Verón fills CMF. All replacements played Inter2000s.']),
1228:('Arsenal FC','ARS',101,1,[
('David Seaman','GK',1,96,3,52),('Sol Campbell','CB',23,97,11,70),('Tony Adams','CB',6,97,11,34),('Lee Dixon','RB',2,94,13,88),('Mikaël Silvestre','LB',18,93,13,16),('Patrick Vieira','DMF',4,98,24,60),('Gilberto Silva','DMF',19,96,24,40),('Freddie Ljungberg','RMF',8,96,34,86),('Robert Pirès','LMF',7,97,34,18),('Dennis Bergkamp','SS',10,98,42,34),('Thierry Henry','CF',14,98,47,65)],2,[10,10,9,8,9,10],['Lehmann/Lauren/Kolo Touré/Ashley Cole absent; Seaman/Dixon/Adams/Silvestre are actual Arsenal2000s replacements.']),
1955:('Bayern Munchen','BAY',127,1,[
('Oliver Kahn','GK',1,98,3,52),('Martín Demichelis','CB',6,95,11,70),('Daniel Van Buyten','CB',5,95,11,34),('Philipp Lahm','RB',21,98,13,88),('Bixente Lizarazu','LB',3,96,13,16),('Mark van Bommel','DMF',17,95,24,59),('B. Schweinsteiger','CMF',31,97,27,39),('Lothar Matthäus','CMF',10,97,33,72),('Zé Roberto','LMF',11,95,33,18),('Gerd Müller','CF',9,98,46,34),('Miroslav Klose','CF',18,96,46,70)],0,[7,7,6,8,6,9],['Sagnol/Lúcio/Ballack absent; Lahm/Demichelis/Matthäus used. Gerd Müller retained exactly as requested despite his earlier era.'])}
for tid,(name,short,donor,tier,entries,captain,kickers,notes)in teams.items():
 slots=[];formation=[];roster=[]
 for namep,role,shirt,ovr,x,y in entries:
  cid,row=pick(namep);roster.append(int(cid));formation.append([roles[role],x,y]);primary=row['position'];slot={'name':namep,'source_name':namep,'player_id':int(cid),'role':role,'shirt':shirt,'starting':True,'source_primary_role':primary,'target_ovr':ovr};slots.append(slot)
  flags=cfg['classic_profiles'].get(cid,{}).get('skill_flags_add',[])
  if not flags:
   flags=[88,90,100,105]if primary==0 else [106,111,113,115]if role in ['CB','RB','LB','DMF']else[78,82,116,118]if role in ['CMF','AMF','LMF','RMF']else[103,114,116,128,136]
  cfg['classic_profiles'][cid]={'name':namep,'roles':list(dict.fromkeys([primary,roles[role]])),'skill_flags_add':flags,'skill_flags_remove':[72,108],'target_ovr':ovr,'competition':473,'formation_role':roles[role],'simulation':{'rating':ovr,'finishing':98 if role in ['CF','SS','LWF','RWF']else 88 if role in ['AMF','CMF','LMF','RMF']else 65,'awareness':98 if role in ['CF','SS','LWF','RWF']else 90 if role in ['AMF','CMF','LMF','RMF']else 65,'passing':97 if role in ['AMF','CMF','DMF']else 88,'name':namep,'known':True}}
  if tid==1956 and role in ['CB','RB','LB','GK']:
   cfg['classic_profiles'][cid]['minimum_stats']={'defensive_awareness':97,'tackling':97,'defensive_engagement':97}if primary!=0 else{}
  cfg['scorer_boosts'][cid]=8 if namep in ['Lionel Messi','Ronaldo Nazário']else 3 if role in ['CF','SS','LWF','RWF']else 1
  cfg['assist_boosts'][cid]=3 if role in ['AMF','CMF','LMF','RMF']else 1
 cfg['native_rosters'][str(tid)]=roster;cfg['visual_aliases'][str(tid)]=donor;cfg['team_names'][str(tid)]={'name':name,'short':short};cfg['shirt_overrides'][str(tid)]={str(s['player_id']):s['shirt']for s in slots}
 cfg['classic_teams'][str(tid)]={'name':name,'short':short,'visual_team':donor,'competition':473,'slots':slots,'formation':formation,'responsibilities':{'captain':captain,'long_free_kick':kickers[0],'short_free_kick':kickers[1],'second_free_kick':kickers[2],'left_corner':kickers[3],'right_corner':kickers[4],'penalty':kickers[5]},'set_piece_taker':kickers,'era_notes':notes}
 assert len(roster)==11 and len({s['shirt']for s in slots})==11
 cfg['team_scorer_boosts'][str(tid)]={str(s['player_id']):cfg['scorer_boosts'][str(s['player_id'])]for s in slots}
 cfg['match_environment']['home_stadiums'][str(tid)]={100:7,109:1,108:30,121:85,120:85,102:52,103:7,119:85,101:52,127:51}[donor]
league={'teams':list(teams),'original_teams':[1706,4937,1228,1957,1956,4962,1950,4938,4964,1955,1958,4965],'name':'Y08 Champion League','tiers':{str(k):v[3]for k,v in teams.items()},'legs':2,'strength_model':'same engine as Premier/Uefa league; four tier0 and six tier1 clubs','milan_defence_team':1956}
cfg['leagues']['473']=league;cfg['league_names']['473']='Y08 Champion League';cfg['ovr_policy']['473']={'default':93,'range':[93,98],'target_by_id':{str(s['player_id']):s['target_ovr']for tid in teams for s in cfg['classic_teams'][str(tid)]['slots']}}
cfg['match_environment']['home_assignment_scope'].append('473') if '473' not in cfg['match_environment']['home_assignment_scope'] else None
# No exact card can be reused across old leagues or within Y08.
chosen=[str(i)for t in teams for i in cfg['native_rosters'][str(t)]];assert len(chosen)==len(set(chosen))and not set(chosen)&original_used
(T/'myleague_custom.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2));(P/'y08-roster-audit.json').write_text(json.dumps({'passed':True,'native_table_decoded_records':46623,'teams':{str(k):cfg['classic_teams'][str(k)]for k in teams},'new_cards':len(chosen),'duplicate_cards_in_Y08':0,'overlap_with_existing_leagues':[],'fixed_ids':fixed,'removed_teams':[1958,4965],'phone_tested':False},ensure_ascii=False,indent=2))
print('Y08_BUILT',len(teams),len(chosen), 'old-overlap',set(chosen)&original_used)
