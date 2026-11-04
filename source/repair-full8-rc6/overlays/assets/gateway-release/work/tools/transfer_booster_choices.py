"""Native booster IDs/effects, English labels; only +4..+8 choices, stable order."""
STAT={0:'Offensive Awareness',1:'Defensive Awareness',2:'GK Awareness',3:'Dribbling',4:'Ball Control',5:'Tight Possession',6:'Finishing',7:'Low Pass',8:'Lofted Pass',9:'Heading',10:'Tackling',11:'Aggression',12:'Defensive Engagement',13:'Set Piece Taking',14:'Curl',15:'GK Catching',16:'GK Parrying',17:'GK Reflexes',18:'GK Reach',19:'Speed',20:'Physical Contact',21:'Balance',22:'Kicking Power',23:'Acceleration',24:'Jumping',25:'Stamina'}
CATEGORY={1:'Shooting',2:'Set Pieces',3:'Aerial Superiority',4:'Passing',5:'Dribbling',6:'Technique',7:'Defending',8:'Duelling',9:'Agility',10:'Physicality',11:'Goalkeeping',12:'Total Upgrade',13:'Striker Instinct',14:'Shutdown',15:'Endurance',16:'Goalkeeping Special',17:'Crossing',18:'Creativity',19:'Commanding',20:'Build Up',21:'Accuracy',22:'Attacking Engine',23:'Ball Shielding',24:'Two Way',25:'Counter Attack',26:'Aerial Defence',27:'Breakthrough',28:'Strength',29:'Off Ball Movement',30:'Ball Winning'}
def catalogue():
 import editor_boosters as native
 result=[]
 for row in native.catalogue():
  if row['amount']<4:continue
  row=dict(row);effects=native.EFFECTS.get(row['id'],());description=', '.join(STAT.get(stat,'Attribute '+str(stat))+' +'+str(value)for stat,value in effects)
  row['label']=CATEGORY.get(row['category'],'Special Booster')+' +'+str(row['amount'])+' · ID '+str(row['id']);row['description']=description
  result.append(row)
 return sorted(result,key=lambda r:(r['amount'],r['category']or 1000,r['kind'],r['id']))
