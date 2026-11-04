"""Exact game73 parameter records; public game data, never a personal save.
The native baseline was decoded by original 0x82aa124/0x82a84d4. Saved
owned records and competition overlays take precedence, with source disclosed.
"""
from pathlib import Path
import functools,json
@functools.lru_cache(maxsize=1)
def baselines():return json.loads(Path(__file__).with_name('native_player_parameters.json').read_text())
def read(c,pid,cid):
 import player_editor,myleague_editor_runtime as editor
 pid=str(pid);params=None;source=None;observed_params=None
 try:
  observed=json.loads(Path(__file__).with_name('transfer-native-observed.private.json').read_text())
  item=observed.get('records',{}).get(str(cid)+':'+pid,{})
  if observed.get('schema')==1 and isinstance(item.get('parameters'),list)and len(item['parameters'])==147:observed_params=list(item['parameters'])
 except(OSError,ValueError):pass
 for table in ('gameplayers','player_pool'):
  records=c.execute('SELECT json FROM '+table+' WHERE id=? ORDER BY serial LIMIT 2',(int(pid),)).fetchall()
  if len(records)==1:
   data=json.loads(records[0][0]);raw=data.get('parameters')
   if isinstance(raw,list)and len(raw)in(144,147):params=player_editor.native_parameters(raw);source=table;break
 if params is None and observed_params is not None:params=observed_params;source='native_MyLeague_record_observed'
 if params is None:
  classic=json.loads(Path(__file__).with_name('transfer_classic_native_baselines.json').read_text())
  raw=classic.get(str(cid)+':'+pid)
  source='game73_classic_native_path'if raw is not None else'game73_native_base'
  if raw is None:raw=baselines().get(pid)
  if raw is None:raise ValueError('No verified native record for this exact player ID: '+pid)
  params=list(raw)
 params=list(params)
 for row in sorted((r for r in editor.requested_long_sleeves(editor.config())['players']if r['id']==pid and r['competition']in(0,cid)),key=lambda r:r['competition']!=0):
  for k,v in row.get('parameters',{}).items():params[int(k)]=v
  if 'boosters'in row:params[144:147]=row['boosters']
  for k,v in row.get('position_parameters',{}).items():params[int(k)]=v
 assert len(params)==147
 return params,source

def celebrations():
 import appearance_choices
 result={}
 for key,rows in appearance_choices.choices().items():
  result[key]=[]
  for row in rows:
   out=dict(row);names=list(dict.fromkeys(str(c.get('name','')).strip()for c in row.get('cards',[])if c.get('name')));out['label']=' / '.join(names)if names else'No named owner in game73 table';result[key].append(out)
 return result
