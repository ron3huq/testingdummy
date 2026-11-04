"""Keep compact last-active hook counters across launcher restarts; no save rows."""
from pathlib import Path
import json,os,time
HERE=Path(__file__).resolve().parent
KEYS={
 'face':('identity_profiles','shirt_name_changes','shirt_name_failures','shirt_name_last_card','native_ui_name_changes','native_ui_name_last_card','native_shirt_setter_intercepts','record_name_fields_updated','record_name_field_rejections','shirt_render_text_replaced','font_name_resource_paths','shirt_resource_key_calls'),
 'accessories':('wrist_loader','accessory_vector_status','accessory_packed_status','editor_status','appearance_error','editor_error','cached_gameplan')}
def record(kind,state,data):
 if state!='HOOK_ACTIVE'or kind not in KEYS:return
 try:
  out={'version':'V19.1-FULL8-RC6','historical':True,'pid':os.getpid(),'captured_unix':time.time(),'state':state,'counters':{k:data[k]for k in KEYS[kind]if k in data}}
  p=HERE/('full4-last-active-'+kind+'.json');tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(out,separators=(',',':')));tmp.replace(p)
 except Exception:pass

def previous():
 out={}
 for kind in KEYS:
  try:
   p=HERE/('full4-last-active-'+kind+'.json')
   if p.stat().st_size<=16384:out[kind]=json.loads(p.read_text())
  except (OSError,ValueError):pass
 return out
