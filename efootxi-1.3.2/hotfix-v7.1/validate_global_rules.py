from pathlib import Path
import sys,json,argparse,copy
p=argparse.ArgumentParser();p.add_argument('--gateway',type=Path,required=True);a=p.parse_args();r=Path(__file__).parent;sys.path[:0]=[str(r),str(a.gateway/'work/tools')]
import myleague_worlds as w
checks=0
for role in range(13):
 for power in [83,84,85,94,120,127]:
  for low,blitz,learned in [(0,0,[]),(1,0,[]),(0,1,[]),(0,0,[18]),(0,0,[24])]:
   params=[0]*147;params[0]=role;params[37]=power;params[127]=low;params[120]=blitz
   player=dict(gameplayer_id=dict(id=1234567890123,serial=9),parameters=params,additional_skill_id=learned);original=copy.deepcopy(player)
   out=w.edit_projection(player);assert player==original;expected=min(127,power+7) if power>84 else power
   assert out['parameters'][37]==expected
   expected_dip=int(4<=role<=12 and not(low or blitz or set(learned)&{18,24}));assert out['parameters'][103]==expected_dip
   assert all(out['parameters'][i]==params[i] for i in range(147) if i not in [37,103])
   for repeat in range(3):assert w.edit_projection(player)==out
   checks+=1
# Same card can have different trained serials and current/detail base parameters.
p=[0]*147;p[0]=12;p[37]=85
one=dict(gameplayer_id=dict(id=1234567890123,serial=1),parameters=list(p));p[37]=97;two=dict(gameplayer_id=dict(id=1234567890123,serial=2),parameters=list(p))
assert w.edit_projection(one)['parameters'][37]==92 and w.edit_projection(two)['parameters'][37]==104
# Current training changes for an existing serial are seen; no stale PID cache.
two['parameters'][37]=100;assert w.edit_projection(two)['parameters'][37]==107
assert w.edit_projection(dict(gameplayer_id={'id':999},parameters=[0]*145))['parameters']==[0]*145
report=dict(status='GLOBAL_RULES_PASS',cases=checks,checks=['strict power>84, +7, packed-field cap127','all13 primary roles; conditional Dipping absent only when neither Low Screamer nor Blitz Curler innate/learned','unrelated147 fields and source objects preserved','repeated raw-source projections stable; serials and later training remain distinct','unsupported unselected legacy layouts passed through'])
(r/'global-rules-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
