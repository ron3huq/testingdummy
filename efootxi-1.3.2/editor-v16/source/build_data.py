from pathlib import Path
import json,sqlite3,struct,re,sys,gzip,base64
root=Path('/workspace/analysis/my-league');r=root/'hotfix-v16';out=Path(__file__).parent
sys.path[:0]=[str(root/'android/user-gateway/work/tools')];import player_skills
c=json.loads((r/'myleague_custom.json').read_text());can=json.loads((root/'android/user-gateway/outputs/reference/canonical_rosters.json').read_text());src=(root/'android/tables/Player.bin').read_bytes()
con=sqlite3.connect('file:'+str(root/'android/user-gateway/outputs/efootball/local-club.sqlite3')+'?mode=ro',uri=True)
params={str(pid):json.loads(raw).get('parameters')for pid,raw in con.execute('select card_id,payload from managed_cards')};con.close()
players=[];lookup={}
for off in range(0,len(src),400):
 pid=str(struct.unpack_from('<Q',src,off+8)[0]);name=src[off+332:off+400].split(b'\0')[0].decode('utf8',errors='replace');p=params.get(pid);p=p if isinstance(p,list)and len(p)==147 else None;role=p[0]if p else can['positions'].get(pid)
 row=[pid,name,role,p];players.append(row);lookup[pid]=row
code=(r/'select_team.c').read_text();plans=json.loads(re.search(r'static const Plan plans\[\]=(.*?);',code,re.S).group(1).replace('{','[').replace('}',']'));plans={str(p[0]):p for p in plans}
shirts=json.loads(re.search(r'static const Shirt shirts\[\]=(.*?);',code,re.S).group(1).replace('{','[').replace('}',']'));numbers={(str(tid),str(pid)):n for tid,pid,n in shirts}
teamnames=json.loads((root/'android/user-gateway/outputs/reference/ziru-data/team_names.json').read_text());leagues={k:{'name':v['name'],'teams':v['teams']}for k,v in c['leagues'].items()if k in ['122','566','128','549']};leagues['518']={'name':'Y17 Champion League','teams':[int(x)for x in c['classic_teams']]}
teams={};defaultxy=[[0,3,52],[1,11,34],[1,11,70],[3,13,88],[2,13,16],[4,22,52],[5,27,34],[8,35,70],[10,42,86],[9,42,18],[12,46,52]]
for cid,league in leagues.items():
 for tid in league['teams']:
  key=str(tid);ids=list(map(str,c['native_rosters'].get(key,can['rosters'].get(key,[]))))
  if len(ids)<11:continue
  plan=plans.get(key);verified=bool(plan)
  if not plan:
   pool=list(ids);ordered=[]
   for role,x,y in defaultxy:
    pos=next((p for p in pool if lookup.get(p,[None,None,None])[2]==role),None)
    if pos is None:pos=next((p for p in pool if lookup.get(p,[None,None,None])[2]!=0),pool[0])
    ordered.append(pos);pool.remove(pos)
   ids=ordered+pool
  used=set();slots=[]
  preferred={pid:numbers[key,pid]for pid in ids if(key,pid)in numbers}
  for i,pid in enumerate(ids):
   number=preferred.get(pid)
   if not number or number in used:number=next(n for n in range(1,100)if n not in used and n not in preferred.values())
   used.add(number);role,x,y=(plan[1][i]if plan and i<11 else defaultxy[i]if i<11 else [lookup.get(pid,[None,None,12])[2]or 12,26,52]);slots.append(dict(id=pid,shirt=number,role=role,x=x,y=y))
  name=c['team_names'].get(key,{}).get('name')or teamnames.get(key,{}).get('name')or key
  teams[f'{cid}:{key}']={'team_id':tid,'competition':int(cid),'name':name,'verified_formation':verified,'roster':slots,'captain':ids[plan[3]if plan else 0],'kickers':[ids[i]for i in(plan[2]if plan else[10]*6)]}
fields=[[14,'Nhận thức tấn công'],[15,'Nhận thức phòng ngự'],[16,'GK Awareness'],[17,'Rê bóng'],[18,'Kiểm soát bóng'],[19,'Giữ bóng chặt'],[20,'Dứt điểm'],[21,'Chuyền thấp'],[22,'Chuyền bổng'],[23,'Đánh đầu'],[24,'Tackling'],[25,'Quyết liệt'],[26,'Gắn kết phòng ngự'],[27,'Sút phạt'],[28,'Độ xoáy'],[29,'GK Catching'],[30,'GK Parrying'],[31,'GK Reflexes'],[32,'GK Reach'],[34,'Tốc độ'],[35,'Sức mạnh cơ thể'],[36,'Thăng bằng'],[37,'Lực sút'],[38,'Tăng tốc'],[39,'Bật nhảy'],[40,'Thể lực']]
friendly={'SCISSORS_SKILLS':'Scissor Feint','ROULETTE_SKILLS':'Marseille Turn','EDGE_TURN':'Chop Turn','TAP_FAKE':'Tap Trick','SPRING_CUT':'Snap Striker','ACCEL_BURST':'Acceleration Burst','BREAKTHROUGH_DRIBBLE':'Magnetic Feet','DROP_SHOT':'Dipping Shot','LOW_IMPACT_SHOT':'Low Screamer','BLITZ_CROSSING':'Edge Crossing','PHYSICAL_TACKLE':'Long-Reach Tackle','SHADOW_GUARDIAN':'Shadow Hunt','CHASING':'Track Back','INTERCEPT':'Interception','SLIDING':'Sliding Tackle','AMAZON':'Attack Trigger'}
skills=[[flag,friendly.get(player_skills.SKILL_NAMES[sid],player_skills.SKILL_NAMES[sid].replace('_',' ').title())]for sid,flag in player_skills.PARAMETER_BY_SKILL.items()]
data={'players':players,'teams':teams,'leagues':leagues,'fields':fields,'skills':skills,'roles':['GK','CB','LB','RB','DMF','CMF','LMF','RMF','AMF','LWF','RWF','SS','CF'],'default':json.loads((r/'myleague_editor.json').read_text()),'baseVersion':'native-hotfix-v16'}
(out/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('players',len(players),'teams',len(teams),'catalog', (out/'catalog.json').stat().st_size)
