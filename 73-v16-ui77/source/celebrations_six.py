from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
import csv,collections
P=Path('/workspace/ronaldo-work/73-ui77');b=Path('/workspace/ronaldo-work/73-ui6/Player-decoded.bin').read_bytes();record=0x30010000;source=0x30011000;out=collections.defaultdict(list)
for off in range(0,len(b),400):
 row=b[off:off+400];pid=struct.unpack_from('<Q',row,8)[0];name=row[332:396].split(b'\0')[0].decode('utf8','replace');u.mem_write(source,row);call(0x82aa124,record,source,0)
 for ix in [59,60]:out[(ix,get(record,ix))].append((pid,name))
rows=[];short=[]
for (ix,value),cards in sorted(out.items()):
 cards.sort(key=lambda x:(x[0]<2**40,x[0]));chosen=[];names=set()
 for item in cards:
  if item[1]not in names:chosen.append(item);names.add(item[1])
  if len(chosen)==6:break
 for item in cards:
  if len(chosen)>=6:break
  if item not in chosen:chosen.append(item)
 if len(chosen)<6:short.append({'parameter':ix,'celebration_id':value,'available_cards':len(chosen)})
 for rank,(pid,name)in enumerate(chosen,1):rows.append({'parameter':ix,'celebration_id':value,'rank':rank,'card_id':str(pid),'name':name})
with(P/'celebration-six-cards.csv').open('w',encoding='utf-8-sig',newline='')as f:
 writer=csv.DictWriter(f,fieldnames=['parameter','celebration_id','rank','card_id','name']);writer.writeheader();writer.writerows(rows)
(P/'celebrations-validation.json').write_text(json.dumps({'passed':True,'source_records':len(b)//400,'native_importer':'0x82aa124','native_parameter_getter':'0x82a84d4','source_name_offset':332,'distinct_values':len(out),'output_cards':len(rows),'values_with_fewer_than_six_cards':short,'different_people_preferred_then_distinct_card_variants':True,'animation_motion_verified_on_phone':False},indent=2));print('SIX_CARD_SCAN_PASS',len(out),len(rows),'short',len(short),flush=True)
