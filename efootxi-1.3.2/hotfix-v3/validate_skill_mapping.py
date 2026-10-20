"""Compare requested names with flag occurrences in uploaded managed-card corpus."""
from pathlib import Path
import json,sqlite3,collections,argparse
p=argparse.ArgumentParser();p.add_argument('--database',type=Path,required=True);a=p.parse_args()
con=sqlite3.connect(a.database.resolve().as_uri()+'?mode=ro',uri=True)
requested={'snapStrike':136,'accelerationBurst':124,'tapTrick':135,'lowScreamer':127,'bulletHeader':121,'phenomenalFinishing':114,'blitzCurler':120,'momentumDribbling':116,'edgedCrossing':119,'magneticFeet':130,'dippingShot':103,'visionaryPass':118,'shadowHunt':132}
names=collections.Counter();flags=collections.Counter();overlaps=collections.Counter();cards=0
for raw, in con.execute('select payload from managed_cards'):
 row=json.loads(raw);params=row.get('parameters',[])
 if len(params)!=147:continue
 cards+=1;skills=set(row.get('_skills',[]))
 for name,flag in requested.items():
  names[name]+=name in skills;flags[name]+=params[flag]==1;overlaps[name]+=name in skills and params[flag]==1
report={}
for name,flag in requested.items():
 assert names[name]>0 and names[name]==overlaps[name],(name,names[name],overlaps[name])
 if name!='visionaryPass':assert flags[name]==names[name],(name,flags[name],names[name])
 report[name]=dict(parameter=flag,named_cards=names[name],flagged_cards=flags[name],overlap=overlaps[name])
out=dict(status='CORPUS_CO_OCCURRENCE_VALIDATED',cards=cards,mapping=report,limits='Corpus evidence and native parameter accessors validated; not proof of skill gameplay activation on device. visionaryPass shares flag with an alternate external label.')
Path(__file__).with_name('skill-mapping-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
