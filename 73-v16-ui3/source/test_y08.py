from pathlib import Path
import json,sys,types,collections,random,statistics
P=Path('/workspace/ronaldo-work/73-ui3');sys.path.insert(0,str(P/'payload/work/tools'));import myleague_worlds as worlds,myleague_realism as sim
cfg=worlds.config();old=json.loads(Path('/workspace/ronaldo-work/73-ui2/payload/work/tools/myleague_custom.json').read_text());reg=json.loads((P/'registry.json').read_text());ros=json.loads((P/'rosters.json').read_text());can=json.loads(Path('/workspace/ronaldo-work/73-v25-full/android/user-gateway/outputs/reference/canonical_rosters.json').read_text());teams={str(t)for c,r in reg['competitions'].items()if c!='473'for t in r['team_ids']};existing={str(i)for t in teams for i in old['native_rosters'].get(t,old['simulation_rosters'].get(t,can['rosters'].get(t,ros.get(t,[]))))};new={str(i)for t in cfg['leagues']['473']['teams']for i in cfg['native_rosters'][str(t)]};native=set(json.loads((P/'native-ids.json').read_text()));assert len(new)==110 and not new&existing and new<=native
for cid,league in old['leagues'].items():assert cfg['leagues'][cid]==league
for key in ['native_rosters','classic_teams','classic_profiles','team_names','shirt_overrides','visual_aliases']:
 for k,v in old[key].items():assert cfg[key][k]==v,(key,k)
positions=dict(can['positions']);positions.update({pid:p.get('formation_role',p['roles'][0])for pid,p in cfg['classic_profiles'].items()});sim._rankings=types.SimpleNamespace(_canonical_data=lambda:{'positions':positions},_rosters=lambda:cfg['native_rosters']);definition=cfg['leagues']['473'];s={'competition_id':473,'season':1,'team_id':1706,'fixture':1,'realism_v1':{'seed':'public-ui3-validation'},'played':{},'active':None};topwin=[];milan=[];other=[]
for fixture in range(1,401):
 for home in definition['teams']:
  for away in definition['teams']:
   if home==away:continue
   hg,ag=sim._new_score(s,fixture,home,away,random.Random(fixture*100000+home+away*30),())
   ht,at=definition['tiers'][str(home)],definition['tiers'][str(away)]
   if ht!=at:topwin.append(hg>ag if ht<at else ag>hg)
   for tid,conceded in [(home,ag),(away,hg)]:
    (milan if tid==1956 else other).append(conceded)
assert statistics.mean(topwin)>.5
assert statistics.mean(milan)<statistics.mean(other)*.75
shares={}
for tid,star in [(4937,88046292734664),(1957,89136409091415)]:
 roster=tuple(cfg['native_rosters'][str(tid)]);pool=sim._event_pool(roster,False);counts=collections.Counter(pool);assert counts[star]==max(counts.values())and counts[star]/len(pool)>.35,(tid,counts[star]/len(pool));shares[str(star)]=round(counts[star]/len(pool),3)
report={'passed':True,'clubs_checked_in_other_leagues':len(teams),'existing_exact_card_ids':len(existing),'Y08_cards':110,'native_table_ids_verified':True,'duplicate_cards':0,'overlap_other_MyLeague_leagues':[],'existing_six_leagues_unchanged':True,'tier0_win_rate_over_tier1':round(statistics.mean(topwin),3),'milan_mean_AI_conceded':round(statistics.mean(milan),3),'others_mean_AI_conceded':round(statistics.mean(other),3),'R9_Messi_own_club_goal_event_shares':shares,'simulation_games':len(milan)*5,'scorer_ranking_guaranteed':False,'phone_tested':False};(P/'y08-validation.json').write_text(json.dumps(report,indent=2));print('Y08_PASS',report)
