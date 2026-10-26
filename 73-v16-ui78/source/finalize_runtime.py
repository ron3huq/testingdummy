from pathlib import Path
import re,hashlib
T=Path('/workspace/ronaldo-work/73-ui78/payload/work/tools');f=T/'select_team_runtime.py';s=f.read_text();s=re.sub("HOOK_SHA='[0-9a-f]+'","HOOK_SHA='"+hashlib.sha256((T/'libselect_team.so').read_bytes()).hexdigest()+"'",s)
s=s.replace("hook.editor_status.argtypes=", "hook.skin_status.argtypes=[C.c_uint];hook.skin_status.restype=C.c_uint64\n                hook.editor_status.argtypes=")
s=s.replace("diagnostic('HOOK_ACTIVE',player_model_status=", "diagnostic('HOOK_ACTIVE',skin_palette_status={k:hook.skin_status(i)for i,k in enumerate(['ready','profiles','applies','last_card_id','last_palette'])},player_model_status=");f.write_text(s)
