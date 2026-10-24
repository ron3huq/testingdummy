"""Exact-card skill substitution. No SQL and no physical/editor settings."""
import functools,copy
CARDS={'89136418985303','89136418985302'}
CHOP_PARAMETER=108
LONG_REACH_PARAMETER=125

def project(player):
 cid=str((player.get('gameplayer_id')or{}).get('id',player.get('id','')))
 if cid not in CARDS:return player
 out=dict(player)
 if len(player.get('parameters',[]))==147:
  out['parameters']=list(player['parameters']);out['parameters'][CHOP_PARAMETER]=0;out['parameters'][LONG_REACH_PARAMETER]=1
 if 'innate_skills'in player:
  out['innate_skills']=sorted((set(player['innate_skills'])-{5})|{62})
 return out

def install():
 import club_store,player_editor
 if getattr(club_store.wire_player,'_ui2_skills',False):return False
 original_wire=club_store.wire_player
 @functools.wraps(original_wire)
 def wire(player,*args,**kwargs):return project(original_wire(player,*args,**kwargs))
 wire._ui2_skills=True;club_store.wire_player=wire
 original_players=player_editor.players
 @functools.wraps(original_players)
 def players(*args,**kwargs):return [project(p)for p in original_players(*args,**kwargs)]
 player_editor.players=players
 return True

def install_native_config(root):
 """One startup migration; no save SQL and no per-player work in read routes."""
 from pathlib import Path
 import json
 import myleague_editor_runtime as editor
 tools=Path(root)/'work/tools';path=tools/'myleague_editor.json';data=json.loads(path.read_text());before=json.dumps(data,sort_keys=True)
 for row in data.get('players',[]):
  params=row.get('parameters',{});had_body=any(k in params for k in ['43','47','48','60'])
  for key in ['43','47','48','60']:params.pop(key,None)
  row.pop('accessories',None)
  if had_body:row['sleeve']='none'
 defaults=json.loads((tools/'ui2_skill_rules.json').read_text())
 for cid,flags in defaults.items():
  rows=[row for row in data['players']if row['id']==cid]
  if not any(row['competition']==0 for row in rows):
   row={'id':cid,'competition':0,'sleeve':'long','parameters':{}};data['players'].append(row);rows.append(row)
  for row in rows:row['parameters'].update(flags);row['sleeve']='long'
 editor.validate(data)
 if json.dumps(data,sort_keys=True)!=before:
  temp=path.with_suffix('.ui2.tmp');temp.write_text(json.dumps(data,indent=2));temp.replace(path)
 editor._config=None
