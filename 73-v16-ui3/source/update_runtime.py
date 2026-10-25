from pathlib import Path
import json,re,hashlib
P=Path('/workspace/ronaldo-work/73-ui3');T=P/'payload/work/tools';cfg=json.loads((T/'myleague_custom.json').read_text());f=T/'myleague_balance.py';s=f.read_text().replace('def target_ovr(pid):','def target_ovr(pid,cid=518):').replace("config()['ovr_policy']['518']['target_by_id']","config()['ovr_policy'][str(cid)]['target_by_id']")
a=s.index(' if int(cid)==122');s=s[:a]+''' if int(cid)==473:
  from myleague_worlds import config,STAT_INDEX
  profile=config()['classic_profiles'].get(pid,{})
  if profile.get('competition')==473:
   p[0]=profile['formation_role'];p[p[0]+1]=2
   for flag in profile.get('skill_flags_add',[]):p[flag]=1
   if p[72]:p[116]=1
   if p[108]:p[135]=1
   p[72]=p[108]=0
   floors={STAT_INDEX[k]:v for k,v in profile.get('minimum_stats',{}).items()}
''' +s[a:]
s=s.replace('target=target_ovr(pid) if int(cid)==518 else None','target=target_ovr(pid,cid) if int(cid)in(518,473)else None');f.write_text(s)
f=T/'myleague_73.py';s=f.read_text().replace("row['roles'][0] for pid,row", "row.get('formation_role',row['roles'][0]) for pid,row");f.write_text(s)
f=T/'myleague_realism.py';s=f.read_text().replace('SIMULATED_COMPETITIONS = {122,518,566,128}','SIMULATED_COMPETITIONS = {122,518,566,128,473}').replace('if cid==518:\n        from myleague_worlds','if cid in (518,473):\n        from myleague_worlds')
# Reuse the existing Premier/Uefa top0-v-top1 model for Y08. Modern-team-specific
# exceptions stay confined to122. Exact-Y08 team identities have their own tiers.
s=s.replace('if cid==122 and {ht,at}=={0,1} and {home,away}!={108,109}:','if (cid==473 and {ht,at}=={0,1})or(cid==122 and {ht,at}=={0,1} and {home,away}!={108,109}):').replace('elif cid==122 and ht==at==0:','elif cid in(122,473)and ht==at==0:').replace('elif cid==122 and ht==at==1:','elif cid in(122,473)and ht==at==1:')
# Add a defensive score distribution rather than a guaranteed scripted clean sheet.
s=s.replace('        legal.append((hg,ag,w))','''        if cid==473 and 1956 in (home,away):
            conceded=ag if home==1956 else hg
            w*={0:3.2,1:1.,2:.18,3:.03}.get(conceded,.005)
        legal.append((hg,ag,w))''')
# Check actual append line before accepting the edit.
if 'conceded=ag if home==1956'not in s:
 a=s.index('    # Remove exact reverse-leg');s=s[:a]+'''    if cid==473 and 1956 in(home,away):
        def defence_weight(row):
            x,y,w=row;hg,ag=(x,y)if winner in(None,home)else(y,x)
            conceded=ag if home==1956 else hg
            return x,y,w*{0:3.2,1:1.,2:.18,3:.03}.get(conceded,.005)
        rows=[defence_weight(row)for row in rows]
''' +s[a:]
f.write_text(s)
f=T/'rolled_runtime.py';s=f.read_text().replace("+17","+18");f.write_text(s)
f=T/'editor_names.py';s=f.read_text().replace("NAMES={","NAMES={'88046292734664':'Ronaldo Nazário','88046312750111':'Thierry Henry','89136418985301':'Zinedine Zidane',");f.write_text(s)
f=T/'select_team_runtime.py';s=f.read_text();h=hashlib.sha256((T/'libselect_team.so').read_bytes()).hexdigest();s=re.sub("HOOK_SHA = '[0-9a-f]+'","HOOK_SHA = '"+h+"'",s)
# Diagnostic array lengths now derive from shipped data instead of UI2's counts.
marker='                previous = None';s=s.replace(marker,"                rules=list(settings['leagues']);rule_ids=['122','566','128','125','549','473'];native_ids=list(settings['native_rosters']);rule_count=len(rule_ids);native_count=len(native_ids)\n"+marker)
s=s.replace('range(13)','range(3+2*rule_count)').replace('range(22)','range(native_count+4)')
s=s.replace('active_competition=stats[35],selected_stadium=stats[36],ovr_balance_failures=stats[37]','active_competition=hook.environment_status(0),selected_stadium=hook.environment_status(1),ovr_balance_failures=hook.environment_status(2)')
a=s.index('league_results={cid:stats[3+i]');b=s.index(',native_last_player_full_id=',a)
s=s[:a]+"league_results={cid:hook.status(3+i)for i,cid in enumerate(rule_ids)},patched_leagues={cid:hook.status(3+rule_count+i)for i,cid in enumerate(rule_ids)},native_team_results={tid:hook.native_status(i)for i,tid in enumerate(native_ids)},native_player_applies=hook.native_status(native_count),native_last_player_error=hook.native_status(native_count+1),native_last_team_error=hook.native_status(native_count+2),native_last_player_reason=hook.native_status(native_count+3)"+s[b:]
f.write_text(s)
# Refresh appearance library/runtime hashes, leaving all face identities/files untouched.
f=T/'noodle_bundle.json';m=json.loads(f.read_text())
for n in m['appearance_files']:
 if(T/n).exists():m['appearance_files'][n]=hashlib.sha256((T/n).read_bytes()).hexdigest()
m['editor_ui']='73-ui3-tapered-cuffs-y08';f.write_text(json.dumps(m,indent=2))
f=T/'rolled_bundle.json';m=json.loads(f.read_text());m['files']={x.name:{'size':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()}for x in(P/'payload/livedata').iterdir()};f.write_text(json.dumps(m,indent=2))
# Every changed designer file included in its original installation manifest.
r=P/'apk-assets/assets/card-designer';f=r/'MANIFEST.json';m=json.loads(f.read_text())
for n in m:
 x=r/n
 if x.is_file():m[n]={'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()}
f.write_text(json.dumps(m,indent=2))
print('RUNTIMES_UPDATED',h)
