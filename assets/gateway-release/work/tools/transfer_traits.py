"""Transfer skills/boosters use the same native fields and catalogue as Player Editor."""
from pathlib import Path
import json
import myleague_editor_runtime as editor
def manage(c,action,req):
 import transfer_editor as transfer,transfer_player_editor as players,editor_boosters,editor_names,player_editor
 tid,cid=transfer.identity(req);pid=str(req.get('player_id',''));editor.identity(pid)
 team=transfer.source(tid,cid)
 if team is None or not any(p['id']==pid for p in team['roster']):raise ValueError('Select a current team member')
 if action.endswith('_apply'):
  return players.manage(c,'ui712_transfer_player_apply',dict(req,values={k:req[k]for k in ('skills','boosters')if k in req}))
 source=c.execute('SELECT json FROM gameplayers WHERE id=? ORDER BY serial LIMIT 1',(int(pid),)).fetchone()
 if source is None:source=c.execute('SELECT json FROM player_pool WHERE id=? ORDER BY serial LIMIT 1',(int(pid),)).fetchone()
 if source is None:raise ValueError('Native card data is unavailable; no skill list was guessed')
 data=json.loads(source[0]);params=player_editor.native_parameters(data.get('parameters'))
 # Apply persisted overlays in the same global -> competition precedence.
 for row in sorted((r for r in editor.requested_long_sleeves(editor.config())['players']if r['id']==pid and r['competition']in(0,cid)),key=lambda r:r['competition']!=0):
  for k,v in row.get('parameters',{}).items():params[int(k)]=v
  if 'boosters'in row:params[144:147]=row['boosters']
 labels=json.loads(Path(__file__).with_name('innate_skill_labels.json').read_text())
 return dict(player_id=pid,name=editor_names.NAMES.get(pid,pid),skills=[i for i,flag in enumerate(editor.FLAGS)if params[flag]],skill_choices=[{'id':i,'label':labels.get(str(i),'Native skill '+str(i))}for i in range(len(editor.FLAGS))],boosters=params[144:147],booster_choices=editor_boosters.catalogue(),booster_limits=list(getattr(editor_boosters,'EDITOR_LIMITS',(255,1023,1023))))
