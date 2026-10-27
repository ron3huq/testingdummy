from pathlib import Path
import json,sys,struct
P=Path('/tmp/73-ui711');T=P/'build/payload/work/tools';sys.path.insert(0,str(T));import player_model
names=json.loads((P/'player-names.json').read_text());profiles=json.loads((P/'source-profiles.json').read_text());nativebody=player_model.baseline_rows();body={}
for pid in names:
 values=player_model.baseline(pid);assert len(values)==11,(pid,'missingbody');body[pid]={'name':names[pid][0],'height':profiles[pid]['parameters'][47],'weight':profiles[pid]['parameters'][48],'model':values,'native_appearance_fullID_present':pid in nativebody}
c=Path(P/'Country-decoded.bin').read_bytes();countries=[]
for off in range(0,len(c),1488):
 row=c[off:off+1488];code=(int.from_bytes(row[:4],'little')>>10)&511;flag=int.from_bytes(row[:4],'little')&1023;name=row[288:358].split(b'\0')[0].decode();countries.append({'id':code,'name':name,'flag_resource_id':flag})
assert next(r for r in countries if r['name']=='Portugal')['id']==228;assert next(r for r in countries if r['name']=='Vietnam')['id']==38
registry=json.loads(Path('/workspace/ronaldo-work/73-ui3/registry.json').read_text());teams={}
for league in registry['competitions'].values():
 for row in league['teams']:teams[str(row['team_id'])]={'id':row['team_id'],'name':row['name'],'competition':league['competition_id']}
teams['109']['name']='Real Madrid';teams['100']['name']='Manchester United';models=['88039313485858','89138288266704','106726716084650','88044145348029','89138556701095','89138556575063','106786577226938'];bgs=['88039313485858','88045755960770','89138019805599','89138288266704','89133456301399','89133724764840','88037702764935']
d={'schema':1,'models':[dict(id=pid,name=names[pid][0])for pid in models],'backgrounds':[dict(id=pid,name=names[pid][0])for pid in bgs],'countries':sorted(countries,key=lambda r:r['name']),'clubs':sorted(teams.values(),key=lambda r:r['name']),'sources':body};(T/'profile_options.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));print('OPTIONS',len(teams),len(countries),{p:b['native_appearance_fullID_present']for p,b in body.items()})
