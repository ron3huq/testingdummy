"""Neutral My League OVR projection; immutable sources, no owned-database writes."""
import copy
FIELDS=tuple(i for i in range(14,41) if i!=33)
DEFENCE_SKILLS=(106,111,113,115)
STYLE_SKILLS={0:(88,90,100,105),1:(106,111,113,115,125),2:(84,93,106,111,113,119,125),3:(84,93,106,111,113,119,125),4:(82,93,106,110,118,122,125),5:(78,82,110,118,122,127),6:(70,84,116,119,124,135),7:(70,84,116,119,124,135),8:(70,78,82,110,116,118,122,127),9:(70,103,116,119,124,135),10:(70,103,116,119,124,135),11:(70,81,116,128,136),12:(81,103,114,128,136)}
def balance(parameters,cid,pinned=()):
 import native_overall
 p=list(parameters)
 if len(p)!=147 or not 0<=p[0]<=12:raise ValueError('canonical147 with known position required')
 low,high=(80,86) if int(cid)==566 else (87,95)
 fields=[i for i in FIELDS if i not in pinned]
 for step in range(128):
  score=native_overall.rating(p,p[0])
  if low<=score<=high:return p
  direction=1 if score<low else -1;changed=False
  # Preserve GK vs outfield identities: tune only relevant attributes.
  for i in fields:
   if p[0]!=0 and i in (16,29,30,31,32):continue
   if p[0]==0 and i not in (16,29,30,31,32,34,35,36,38,39,40):continue
   value=max(40,min(99,p[i]+direction))
   if value!=p[i]:p[i]=value;changed=True
  if not changed:break
 raise ValueError('cannot satisfy requested neutral OVR range without changing pinned identity/stats')
def project(player,cid,messi=False):
 out=copy.deepcopy(player);p=list(out.get('parameters')or[])
 if len(p)!=147:return out
 learned=set(out.get('additional_skill_id')or[])|set(out.get('additional_skill')or[])
 if int(cid)==518:
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
 out['parameters']=balance(p,cid,pinned)
 return out
