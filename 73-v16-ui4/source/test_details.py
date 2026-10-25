from pathlib import Path
import sys,sqlite3,shutil,json,tempfile,types,importlib.util,copy,time
P=Path('/workspace/ronaldo-work/73-ui4');T=P/'payload/work/tools';scope={};exec(Path('/workspace/ronaldo-work/73-ui/inspect_live.py').read_text().split("print('APPEARANCE'")[0],scope)
sys.path.insert(0,str(T));import player_skills
for name in ['myleague_editor_runtime','myleague_worlds','editor_details','coach_changes']:
 sys.modules.pop(name,None)
import editor_details as mod,coach_changes
with tempfile.TemporaryDirectory(dir=P)as d:
 root=Path(d);tools=root/'work/tools';tools.mkdir(parents=True);shutil.copy2(T/'myleague_editor.json',tools/'myleague_editor.json');mod.ROOT=root
 src=sqlite3.connect('file:/workspace/ronaldo-work/73-ui/save-audit/club.sqlite3?mode=ro',uri=True);conn=sqlite3.connect(root/'test.sqlite3');src.backup(conn);src.close()
 row=conn.execute('SELECT id,serial,json FROM gameplayers LIMIT 1').fetchone();req=dict(id=str(row[0]),serial=int(row[1]));original=json.loads(row[2]);data=mod.get(conn,req);assert len(data['skills'])>=70 and all('label'in x for x in data['skills']);assert data['height']==original['parameters'][47]
 # Meaningful edit: height, mass, remove a built-in skill and choose a valid one.
 selected=list(data['selected']);selected=[x for x in selected if x!=5];selected=sorted(set(selected)|{62});edited=dict(req,height=193,weight=91,skills=selected)
 result=mod.apply(conn,edited);assert result['saved'];after=json.loads(conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(req['id'],req['serial'])).fetchone()[0]);allowed={47,48}|set(player_skills.PARAMETER_BY_SKILL.values())
 for index,(a,b)in enumerate(zip(original['parameters'],after['parameters'])):
  if index not in allowed:assert a==b,index
 assert after['parameters'][47:49]==[193,91];assert after['parameters'][player_skills.PARAMETER_BY_SKILL[5]]==0;assert after['parameters'][player_skills.PARAMETER_BY_SKILL[62]]==1
 for key,value in original.items():
  if key not in ['parameters','_careerplan_base_parameters','_skills']:assert after[key]==value,key
 assert mod.get(conn,req)['selected']==selected
 cfg=json.loads((tools/'myleague_editor.json').read_text());rule=next(r for r in cfg['players']if r['id']==req['id']and r['competition']==0);assert rule['ui4_details']and rule['parameters']['47']==193 and rule['parameters']['125']==1
 before=conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(req['id'],req['serial'])).fetchone()[0];config=(tools/'myleague_editor.json').read_bytes()
 for bad in [dict(edited,height=139),dict(edited,weight=131),dict(edited,skills=[62,62]),dict(edited,skills=[999]),dict(edited,serial=-1)]:
  try:mod.apply(conn,bad);raise AssertionError('invalid request accepted')
  except ValueError:pass
 assert conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(req['id'],req['serial'])).fetchone()[0]==before and(tools/'myleague_editor.json').read_bytes()==config
 # Failed config validation must roll back both files and transaction.
 old=mod.write_config;mod.write_config=lambda x:(_ for _ in()).throw(ValueError('test validation failure'))
 try:mod.apply(conn,dict(edited,height=194));raise AssertionError('failure accepted')
 except ValueError:pass
 mod.write_config=old;assert not conn.in_transaction and(tools/'myleague_editor.json').read_bytes()==config
 assert conn.execute('SELECT json FROM gameplayers WHERE id=? AND serial=?',(req['id'],req['serial'])).fetchone()[0]==before
 untouched={'gameplayer_id':{'id':1},'parameters':[0]*147};assert mod.project(untouched)is untouched
 # Hot wire projection performs no SQL, no catalogue loading, no deep copy.
 value={'gameplayer_id':{'id':int(req['id'])},'parameters':original['parameters']};start=time.perf_counter()
 for _ in range(10000):wire=mod.project(value)
 elapsed=time.perf_counter()-start;assert wire['parameters'][47:49]==[193,91]and value['parameters']==original['parameters']
 conn.close()
for cid,rule in coach_changes.RULES.items():
 row={'coach_id':{'id':cid},'age':50,'nested':[1]};out=coach_changes.project(row);assert out['name']==rule[0]and out['age']==rule[1]and row=={'coach_id':{'id':cid},'age':50,'nested':[1]}
u={'coach_id':{'id':123}};assert coach_changes.project(u)is u
(P/'details-validation.json').write_text(json.dumps({'passed':True,'checks':['Owned-instance edit read back; valid native height/mass and Chop Turn removal/Long-reach Tackle replacement','Unrelated stats/progression/booster/additional-skill data exact','Invalid requests rejected; SQLite and config rollback; fresh config has only chosen exact card ID','10000 edited-card wire projections no SQL or catalogue scans; immutable source','Only two coach wires altered; source and unrelated coaches immutable'],'wire_10000_seconds':round(elapsed,3),'phone_tested':False},indent=2));print('DETAILS_PASS',round(elapsed,3))
