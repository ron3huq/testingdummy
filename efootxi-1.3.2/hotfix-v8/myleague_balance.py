"""Neutral My League OVR projection; immutable sources, no owned-database writes."""
import copy
FIELDS=tuple(i for i in range(14,41) if i!=33)
DEFENCE_SKILLS=(106,111,113,115)
STYLE_SKILLS={0:(88,90,100,105),1:(106,111,113,115,125),2:(84,93,106,111,113,119,125),3:(84,93,106,111,113,119,125),4:(82,93,106,110,118,122,125),5:(78,82,110,118,122,127),6:(70,84,116,119,124,135),7:(70,84,116,119,124,135),8:(70,78,82,110,116,118,122,127),9:(70,103,116,119,124,135),10:(70,103,116,119,124,135),11:(70,81,116,128,136),12:(81,103,114,128,136)}
def target_ovr(pid):
 from myleague_worlds import config
 return config()['ovr_policy']['518']['target_by_id'].get(str(pid),90)
def balance(parameters,cid,pinned=(),target=None,floors=None):
 import native_overall
 p=list(parameters);floors=floors or {}
 if len(p)!=147 or not 0<=p[0]<=12:raise ValueError('canonical147 with known position required')
 low,high=(target,target) if target is not None else (80,86) if int(cid)==566 else (87,95)
 fields=[i for i in FIELDS if i not in pinned and (i not in (16,29,30,31,32) if p[0]!=0 else i in (16,29,30,31,32,34,35,36,38,39,40))]
 for i,v in floors.items():p[i]=max(p[i],v)
 for step in range(128):
  score=native_overall.rating(p,p[0])
  if low<=score<=high:return p
  direction=1 if score<low else -1;old=list(p)
  for i in fields:p[i]=max(floors.get(i,40),min(99,p[i]+direction))
  after=native_overall.rating(p,p[0])
  if (score<low and after>high) or (score>high and after<low):
   p=old
   for i in fields:
    p[i]=max(floors.get(i,40),min(99,p[i]+direction))
    score=native_overall.rating(p,p[0])
    if low<=score<=high:return p
  if p==old:break
 raise ValueError('cannot satisfy requested neutral OVR without changing pinned identity/stats')
def project(player,cid,messi=False):
 out=copy.deepcopy(player);p=list(out.get('parameters')or[])
 if len(p)!=147:return out
 pid=str((out.get('gameplayer_id')or{}).get('id',0))
 learned=set(out.get('additional_skill_id')or[])|set(out.get('additional_skill')or[])
 floors={}
 if int(cid)==518:
  from myleague_worlds import config,STAT_INDEX
  profile=config()['classic_profiles'].get(pid,{})
  if profile:p[0]=profile['roles'][0]
  for i in range(2,14):p[i]=2
  if p[0]!=0:p[1]=0
  for flag in profile.get('skill_flags_add',[]):p[flag]=1
  floors={STAT_INDEX[k]:v for k,v in profile.get('minimum_stats',{}).items()}
  if p[72] or 3 in learned:p[116]=1
  if p[108] or 5 in learned:p[135]=1
  p[72]=p[108]=0
  for flag in STYLE_SKILLS[p[0]]:p[flag]=1
  for key in ['additional_skill_id','additional_skill']:
   if key in out:out[key]=[74 if sid in (3,5) else sid for sid in out[key]]
  if 'is_skill_added' in out:out['is_skill_added']='YES' if any(x!=74 for x in out.get('additional_skill_id',out.get('additional_skill',[]))) else 'NO'
 if int(cid)==122 and p[0] in (1,2,3):
  for flag in DEFENCE_SKILLS:p[flag]=1
 pinned=()
 if messi:p[17]=p[28]=94;p[120]=p[116]=1;pinned=(17,28)
 out['parameters']=balance(p,cid,pinned,target=target_ovr(pid) if int(cid)==518 else None,floors=floors)
 return out
