"""World Nation128: position-specific additions, never clears innate/additional skills."""
import json
GK=[100,126,129,88,90,105,95,97]
CB=[115,123,125,111,112,106,113,94,97,128]
FB=[119,117,122,84,85,87,106,125,111,97]
MID=[117,118,122,131,82,110,83,87,85,130,124,97,128]
WIDE=[116,124,130,135,119,120,117,122,131,134,127,82,110,97]
FORWARD=[114,121,134,127,124,128,116,130,120,76,81,79,82,110,97]
def flags(role):return GK if role==0 else CB if role==1 else FB if role in(2,3)else MID+[115,125,111,106]if role==4 else MID if role in(5,8)else WIDE if role in(6,7,9,10)else FORWARD
def project(player,cid):
 if int(cid or 0)!=128 or len(player.get('parameters',[]))!=147:return player
 out=dict(player);p=list(player['parameters'])
 for flag in flags(p[0]):p[flag]=1
 out['parameters']=p;return out
