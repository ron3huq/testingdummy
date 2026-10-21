from pathlib import Path
import json,sqlite3,collections
r=Path(__file__).parent;ref=Path('/workspace/analysis/my-league/android/user-gateway/outputs/reference');conn=sqlite3.connect((ref.parent/'efootball/local-club.sqlite3').as_uri()+'?mode=ro',uri=True)
indexes={'speed':34,'acceleration':38,'physicalContact':35,'balance':36,'kickingPower':37,'jump':39,'aggression':25}
counts=collections.Counter();rows=0;skills=collections.Counter();overlap=collections.Counter();labels=collections.defaultdict(collections.Counter)
for pid,raw in conn.execute('select card_id,payload from managed_cards'):
 d=json.loads(raw);p=d.get('parameters',[])
 if len(p)!=147:continue
 for flag in [70,72,84,93,106,107,108,117,118,119,124,125,135]:
  if p[flag]==1:
   for name in d.get('_skills',[]):labels[flag][name]+=1
 for name,flag in [('scissorsFeint',70),('marseilleTurn',72),('pinpointCrossing',84),('doubleTouch',107),('crossOverTurn',108),('edgedCrossing',119),('accelerationBurst',124),('tapTrick',135),('trackBack',93),('interception',106),('gameChangingPass',117),('visionaryPass',118),('longReachTackle',125),('fortress',115),('knuckleShot',78),('phenomenalPassing',122),('attackTrigger',128)]:
  skills[name]+=name in d.get('_skills',[]);overlap[name]+=name in d.get('_skills',[]) and p[flag]==1
 if rows<200:
  try:data=json.loads((ref/'external-attrs'/f'{pid}.json').read_text())['efhub']['card']['baseStats']
  except (OSError,KeyError):continue
  for name,index in indexes.items():counts[name]+=data[name]==p[index]
  rows+=1
assert rows==200 and all(counts[k]==200 for k in indexes)
assert not any('powerTackle' in ns or 'steamroller' in ns for ns in labels.values())
for name in skills:
 assert skills[name]>0 and skills[name]==overlap[name],(name,skills[name],overlap[name])
report=dict(status='CORPUS_PASS',stat_cards=rows,stat_parameter_indexes=indexes,stat_matches=dict(counts),skill_cards=dict(skills),skill_matching_flags=dict(overlap),limits='Confirms data mapping, not Android skill animation/effect.')
(r/'corpus-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
