from pathlib import Path
import json,sqlite3,struct,re,sys,gzip,base64
root=Path('/workspace/analysis/my-league');r=root/'hotfix-v18';out=Path(__file__).parent
sys.path[:0]=[str(root/'android/user-gateway/work/tools')];import player_skills
c=json.loads((r/'myleague_custom.json').read_text());can=json.loads((root/'android/user-gateway/outputs/reference/canonical_rosters.json').read_text());src=(root/'android/tables/Player.bin').read_bytes()
con=sqlite3.connect('file:'+str(root/'android/user-gateway/outputs/efootball/local-club.sqlite3')+'?mode=ro',uri=True)
params={str(pid):json.loads(raw).get('parameters')for pid,raw in con.execute('select card_id,payload from managed_cards')};con.close()
players=[];lookup={}
for off in range(0,len(src),400):
 pid=str(struct.unpack_from('<Q',src,off+8)[0]);name=src[off+332:off+400].split(b'\0')[0].decode('utf8',errors='replace');p=params.get(pid);p=p if isinstance(p,list)and len(p)==147 else None;role=p[0]if p else can['positions'].get(pid)
 row=[pid,name,role,p];players.append(row);lookup[pid]=row
teamnames=json.loads((root/'android/user-gateway/outputs/reference/ziru-data/team_names.json').read_text())
leagues={k:{'name':v['name'],'teams':v['teams']}for k,v in c['leagues'].items()if k in ['122','566','128','549']}
leagues['518']={'name':'Y17 Champion League','teams':[int(x)for x in c['classic_teams']]}
teams={}
for cid,league in leagues.items():
 for tid in league['teams']:
  key=str(tid);name=c['team_names'].get(key,{}).get('name')or teamnames.get(key,{}).get('name')or key
  teams[f'{cid}:{key}']={'team_id':tid,'competition':int(cid),'name':name,'roster':[],'captain':None,'kickers':[None]*6,'plans':[],'verified_formation':False,'source':'OFFLINE_REFERENCE'}
fields=[[14,'Nhận thức tấn công'],[15,'Nhận thức phòng ngự'],[16,'GK Awareness'],[17,'Rê bóng'],[18,'Kiểm soát bóng'],[19,'Giữ bóng chặt'],[20,'Dứt điểm'],[21,'Chuyền thấp'],[22,'Chuyền bổng'],[23,'Đánh đầu'],[24,'Tackling'],[25,'Quyết liệt'],[26,'Gắn kết phòng ngự'],[27,'Sút phạt'],[28,'Độ xoáy'],[29,'GK Catching'],[30,'GK Parrying'],[31,'GK Reflexes'],[32,'GK Reach'],[34,'Tốc độ'],[35,'Sức mạnh cơ thể'],[36,'Thăng bằng'],[37,'Lực sút'],[38,'Tăng tốc'],[39,'Bật nhảy'],[40,'Thể lực']]
from skills_verified import SKILLS,MOTIONS,UNRESOLVED
skills=SKILLS
data={'players':players,'packPlayerIds':list(params),'teams':teams,'leagues':leagues,'fields':fields,'skills':skills,'roles':['GK','CB','LB','RB','DMF','CMF','LMF','RMF','AMF','LWF','RWF','SS','CF'],'default':json.loads((r/'myleague_editor.json').read_text()),'baseVersion':'native-hotfix-v18','motions':MOTIONS,'unresolvedSkills':UNRESOLVED}
(out/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('players',len(players),'teams',len(teams),'catalog', (out/'catalog.json').stat().st_size)
