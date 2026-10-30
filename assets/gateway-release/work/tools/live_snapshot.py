"""On-demand passive native counters. Never waits for the engine or reads save rows."""
from pathlib import Path
import json,ctypes as C,time,functools

def snapshot():
 import noodle_hair as face,select_team_runtime as team,photo_editor,appearance_gear
 out={'version':'73-ui7.18','captured_unix':time.time(),'read_only_native_counters':True,'custom_photo_ids':list(photo_editor._profiles)[:16]}
 h=team._native_handle
 if h is not None and team._ready.is_set():
  def words(name,keys):
   f=getattr(h,name);f.argtypes=[C.c_uint];f.restype=C.c_uint64;return {k:int(f(i))for i,k in enumerate(keys)}
  out['tactics']=words('editor_tactics_status',['calls','cloned_plan_applies','ambiguous_key','fallback_identity_rejected','last_team'])
  out['wrist_loader']=words('editor_wrist_load_status',['calls','requested_cards','added','removed','rejected','last_card','left_in_loader','right_in_loader'])
  out['expanded_accessories']=words('editor_gear_detail_status',['calls','rejected','appended','last_count','left_enabled','right_enabled','canonicalized','last_card'])
  out['shirt']=words('appearance_shirt_status',['calls','exact_matches','alias_matches','applies','last_card','before','after'])
  out['teams']=words('editor_status',['ready','player_applies','team_applies','failures','last_error'])
 f=face._handle
 if f is not None and face._ready.is_set():
  f.noodle_photo_metadata_status.argtypes=[C.c_uint];f.noodle_photo_metadata_status.restype=C.c_uint64
  f.noodle_photo_last_card.argtypes=[];f.noodle_photo_last_card.restype=C.c_uint64
  out['photo']={'builder_calls':int(f.noodle_photo_metadata_status(0)),'custom_card_calls':int(f.noodle_photo_metadata_status(1)),'last_applied_card':int(f.noodle_photo_last_card())}
  for key,method in [('input_key','noodle_photo_input_path'),('output_key','noodle_photo_last_path')]:
   func=getattr(f,method);func.argtypes=[C.c_uint];func.restype=C.c_uint;out['photo'][key]=''.join(chr(func(i))for i in range(192)).split('\0',1)[0]
 return out

def install(module):
 if getattr(module.manage,'_ui718_snapshot',False):return
 old=module.manage
 @functools.wraps(old)
 def manage(action,payload=''):
  if action!='ui718_runtime_snapshot':return old(action,payload)
  out=snapshot();p=Path(__file__).with_name('ui718-live-runtime-status.json');tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(out,indent=2));tmp.replace(p);return json.dumps(out)
 manage._ui718_snapshot=True;module.manage=manage
