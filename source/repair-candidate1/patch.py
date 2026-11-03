from pathlib import Path
import json

ROOT=Path('/workspace/work/full8/candidate')
TOOLS=ROOT/'assets/gateway-release/work/tools'

# Repair the route actually used by LauncherWeb, preserving all existing tools.
p=Path('/workspace/work/full8/smali/org/efootballrevival/runtimeprobe/PrivateTools.smali')
s=p.read_text()
needle='    :cond_16\n    const-string v2, "diagnostics"'
replacement='''    :cond_16
    const-string v2, "single-player"

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :full8_existing_tools

    invoke-static {p0}, Lorg/efootballrevival/runtimeprobe/SinglePlayerSettings;->open(Landroid/app/Activity;)V
    return-void

    :full8_existing_tools
    const-string v2, "diagnostics"'''
assert s.count(needle)==1
p.write_text(s.replace(needle,replacement))
p=ROOT/'assets/launcher/index.html';s=p.read_text()
needle='<button class="quick" id="private-transfer"'
assert s.count(needle)==1
s=s.replace(needle,'<button class="quick" id="private-single-player" type="button"><svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="3"/><path d="M7 21v-5a5 5 0 0 1 10 0v5"/></svg><b>Single Player · AI</b><small>Choose player by full ID</small></button>\n'+needle)
p.write_text(s)
p=ROOT/'assets/launcher/launcher.js';s=p.read_text()
needle='    $("private-transfer").addEventListener'
assert s.count(needle)==1
s=s.replace(needle,'    $("private-single-player").addEventListener("click",()=>call("editor",{op:"privateTool",payload:{tool:"single-player"}}).catch(e=>setProgress(e.message)));\n'+needle)
p.write_text(s)

# DB is the durable owner of Transfer profiles. Rebuild runtime configuration
# after APK resource extraction, just as the existing player editor does.
p=TOOLS/'transfer_editor.py';s=p.read_text()
needle='def kit_choices(tid):'
assert s.count(needle)==1
s=s.replace(needle,'''def restore_config():
 if not profiles:return
 cfg=json.loads(editor.PATH.read_text())
 replacements={(row['team_id'],row['competition']):copy.deepcopy(row)for row in profiles.values()}
 cfg['teams']=[row for row in cfg['teams']if(row['team_id'],row['competition'])not in replacements]+list(replacements.values())
 editor.validate(cfg)
 encoded=json.dumps(cfg,indent=2)
 if encoded!=editor.PATH.read_text():
  tmp=editor.PATH.with_suffix('.transfer-restore.tmp');tmp.write_text(encoded);tmp.replace(editor.PATH)
 editor._config=None

'''+needle)
needle=' load(module._logic.conn)\n import transfer_player_editor'
assert s.count(needle)==1
s=s.replace(needle,' load(module._logic.conn)\n restore_config()\n import transfer_player_editor')
p.write_text(s)

# Interpret record types separately. In cached teams word zero is an index,
# while word one remains the exact player ID. Never derive identity from index.
p=TOOLS/'myleague_team_snapshot.py';s=p.read_text()
needle=" ids=[];shirts=[]"
assert s.count(needle)==1
s=s.replace(needle," ids=[];shirts=[];native_keys=[];cache_indices=set()")
needle="  if kind!=0 or not 0<pid<2**63:raise ValueError('non-base/native player key; cannot safely edit this roster')"
assert s.count(needle)==1
s=s.replace(needle,"""  if not 0<pid<2**63:raise ValueError('invalid exact native player ID')
  if origin==1:
   if kind!=0:raise ValueError('unsupported stock player key kind')
  else:
   if kind>=2**32 or kind==0xffffffff or kind in cache_indices:raise ValueError('invalid or duplicate cached player index')
   cache_indices.add(kind)
  native_keys.append({'word0':kind,'player_id':str(pid)})""")
needle='native_roster_order=ids,native_match_order=order'
assert s.count(needle)==1
s=s.replace(needle,'native_roster_order=ids,native_keys=native_keys,native_key_mode=origin,native_match_order=order')
p.write_text(s)

# Keep bandage and player overlays on the same fully expanded configuration.
# This preserves exact competition overrides and includes DB-restored choices.
p=TOOLS/'bandage_runtime.py';s=p.read_text()
needle="    rows=editor.config()['players']"
assert s.count(needle)==1
s=s.replace(needle,"    rows=editor.requested_long_sleeves(editor.config())['players']")
p.write_text(s)

print('Candidate patched; native libraries and face containers remain unchanged.')
