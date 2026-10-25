from pathlib import Path
import re,json,hashlib,copy
P=Path('/workspace/ronaldo-work/73-ui3');T=P/'payload/work/tools';S=Path('/workspace/testingdummy/73-v16-ui3/source');cfg=json.loads((T/'myleague_custom.json').read_text());y08=cfg['leagues']['473']['teams'];s=Path('/workspace/testingdummy/73-v16-ui2/source/select_team.c').read_text()
def array(name,content):
 global s
 s,n=re.subn(r'(static const [^;\n]*?\b'+name+r'\[\](?:\[\d+\])?=)\{.*?\};',lambda m:m[1]+'{'+content+'};',s,count=1);assert n,name
# Add the Swiss menu membership rule while preserving all five previous rules.
s=s.replace('#define RULE_COUNT 5','static const u32 old_5_0[]={'+','.join(map(str,cfg['leagues']['473']['original_teams']))+'};\nstatic const u32 target_5[]={'+','.join(map(str,y08))+'};\n#define RULE_COUNT 6')
s=s.replace('{old_4_0,12,0,0,target_4,8}};','{old_4_0,12,0,0,target_4,8},{old_5_0,12,0,0,target_5,10}};')
# Replace only generated data arrays, preserve existing native implementations.
a=s.index('static const uptr roster_0[]');b=s.index('/* Public player lookup',a)
rosters=list(cfg['native_rosters'].items());r=''.join('static const uptr roster_%d[]={%s};\n'%(i,','.join(map(str,ids)))for i,(tid,ids)in enumerate(rosters))
r+='typedef struct {u32 team;const uptr *ids;u32 n;} NativeRoster;\nstatic const NativeRoster native_rosters[]={'+','.join('{%s,roster_%d,%d}'%(tid,i,len(ids))for i,(tid,ids)in enumerate(rosters))+'};\n#define ROSTER_COUNT %d\n\n'%len(rosters);s=s[:a]+r+s[b:]
s=s.replace('u32 roles,flags[24];u32 n;} ClassicProfile','u32 roles,flags[24];u32 n,competition,role;} ClassicProfile')
array('classic_profiles',','.join('{%s,%d,{%s},%d,%d,%d}'%(pid,sum(1<<x for x in p['roles']),','.join(map(str,p['skill_flags_add'])),len(p['skill_flags_add']),p.get('competition',518),p.get('formation_role',0xffffffff))for pid,p in cfg['classic_profiles'].items()))
s=s.replace('#define CLASSIC_COUNT 176','#define CLASSIC_COUNT '+str(len(cfg['classic_profiles'])))
s=s.replace('   /* Keep original primary position and every proficiency field0..13. */','   if(r->competition==473&&r->role<13){values[0]=r->role;values[r->role+1]=2;}\n   /* Old Y17 profiles retain all original position/proficiency fields. */')
s=s.replace('active_competition==518?values[i]:classic_original[ix][i]','active_competition==classic_profiles[ix].competition?values[i]:classic_original[ix][i]')
# OVR targets and explicit defensive floor for AC Milan's back four in Y08 only.
pos=s.index('static int classic_star');s=s[:pos]+'static u32 y08_target(uptr pid){static const struct {uptr pid;u32 ovr;} rows[]={'+','.join('{%s,%d}'%(pid,ovr)for pid,ovr in cfg['ovr_policy']['473']['target_by_id'].items())+'};for(unsigned i=0;i<sizeof(rows)/sizeof(rows[0]);i++)if(rows[i].pid==pid)return rows[i].ovr;return 93;}\n'+s[pos:]
a=s.index('static u32 rating_floor(');b=s.index('\nstatic int rating_field',a);old=s[a:b];milan=[p['player_id']for p in cfg['classic_teams']['1956']['slots']if p['role']in ['CB','RB','LB']];s=s[:a]+old.replace('return cid==518','if(cid==473&&(ix==15||ix==24||ix==26)&&('+'||'.join('pid==%dul'%i for i in milan)+'))return 97;return cid==518')+s[b:]
s=s.replace('u32 lo=cid==518?classic_target(pid):','u32 lo=cid==473?y08_target(pid):cid==518?classic_target(pid):').replace('hi=cid==518?lo:','hi=(cid==518||cid==473)?lo:')
# Fixed-size classic loops become array-length based. Includes Y08 teams.
a=s.index('static int is_classic_team(');b=s.index('\nstatic void apply_roster',a);s=s[:a]+'static int is_classic_team(u32 tid){static const u32 ids[]={'+','.join(cfg['classic_teams'])+'};for(unsigned i=0;i<sizeof(ids)/sizeof(ids[0]);i++)if(ids[i]==tid)return 1;return 0;}'+s[b:]
array('names',','.join('{%s,%s,%s}'%(tid,json.dumps(x['name'],ensure_ascii=True),json.dumps(x['short']))for tid,x in cfg['team_names'].items()))
array('shirts',','.join('{%s,%s,%s}'%(tid,pid,num)for tid,rows in cfg['shirt_overrides'].items()for pid,num in rows.items()))
array('plans',','.join('{%s,{%s},{%s},%s}'%(tid,','.join('{%s}'%','.join(map(str,v))for v in x['formation']),','.join(map(str,x['set_piece_taker'])),x['responsibilities']['captain'])for tid,x in cfg['classic_teams'].items()))
s=s.replace('i<12;i++)if(plans[i].team','i<sizeof(plans)/sizeof(plans[0]);i++)if(plans[i].team')
array('visuals',','.join('{%s,%d}'%(tid,donor)for tid,donor in cfg['visual_aliases'].items()))
# Add exact-ID mappings to tailcall shims; source aliases checked before replacing W0.
extra=''.join('mov w10,#%s\\ncmp w0,w10\\nmov w9,#%s\\ncsel w0,w9,w0,eq\\n'%(tid,cfg['visual_aliases'][str(tid)])for tid in y08)
for function,original in [('emblem_hook','original_emblem'),('kit_hook','original_kit')]:
 a=s.index('void '+function+'(');b=s.index('\n',a);line=s[a:b];line=line.replace('adrp x16,'+original,extra+'adrp x16,'+original);s=s[:a]+line+s[b:]
s=s.replace('case 518:return "Y17 Champion League";','case 473:return "Y08 Champion League";case 518:return "Y17 Champion League";')
s=s.replace('cmp w0,#518\\nb.eq 1f\\nadrp x16,original_competition_name','cmp w0,#518\\nb.eq 1f\\ncmp w0,#473\\nb.eq 1f\\nadrp x16,original_competition_name')
s=s.replace('cid==518||cid==122','cid==473||cid==518||cid==122')
s=s.replace('is_classic_team(tid)&&cid==518','is_classic_team(tid)&&(cid==518||cid==473)')
s=s.replace('if(active_competition==518){u32 donor=visual_alias(tid);','if(active_competition==518||active_competition==473){u32 donor=visual_alias(tid);')
# Some callers hand the kit resolver an encoded uniform ID. Map its team part
# only when it is a Y08 team, retaining the original two slots.
s=s.replace('u32 resource=requested_kit_resource(tid);if(resource)return resource;', 'u32 resource=requested_kit_resource(tid);if(resource)return resource;if(active_competition==473&&(tid>>14)&&((tid&16383)<2)){u32 donor=visual_alias(tid>>14);if(donor!=(tid>>14))return donor;}')
# Keep native home assignments in step with the gateway's weather/stadium policy.
a=s.index(' static const struct {u32 team,stadium;} assignments[]');b=s.index('\n',a)
s=s[:a]+' static const struct {u32 team,stadium;} assignments[]={'+','.join('{%s,%d}'%(tid,v)for tid,v in cfg['match_environment']['home_stadiums'].items())+'};'+s[b:]
# Existing exported readback is intentionally bounded to its established76 teams.
# Existing snapshot export count hard-coded12? Expanded below only where a roster policy.
(S/'select_team.c').write_text(s)
# Runtime integrity pin includes old+new config data.
keys=('native_rosters','base_overrides','card_overrides','base_adjustments','team_names','league_logos','shirt_overrides','global_player_rules','classic_teams','classic_profiles','visual_aliases','ovr_policy','match_environment','messi_ids','defender_skill_policy','league_names');native={k:cfg[k]for k in keys};native['leagues']=cfg['leagues'];digest=hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest()
f=T/'myleague_worlds.py';text=f.read_text();text=re.sub("EXPECTED_NATIVE_CONFIG_SHA='[a-f0-9]+'","EXPECTED_NATIVE_CONFIG_SHA='"+digest+"'",text);f.write_text(text)
print('NATIVE_DATA_UPDATED',len(rosters),len(cfg['classic_profiles']),digest)
