"""Display/search aliases for the 73 pre-game editor; no owned-player DB edits."""
import functools,copy
NAMES={'88045755960841':'Nguyen Xuan Son','88038776539586':'Nguyen Dinh Bac','105643042189511':'Nguyen Hoang Duc','106728863696709':'Do Hoang Hen','105848932271764':'Cao Pendant Quang Vinh','105874433662542':'Nguyen Tai Loc','88033139360669':'IShowSpeed','105765448873424':'Ronaldo Jr','106778792700170':'Mesut Ozil'}
def install():
 import player_editor
 original=player_editor.name_index
 if getattr(original,'_v25_aliases',False):return False
 @functools.wraps(original)
 def index():
  result=dict(original())
  for cid,name in NAMES.items():result[cid]=[name,name]
  return result
 index._v25_aliases=True;player_editor.name_index=index
 old_players=player_editor.players
 @functools.wraps(old_players)
 def players(conn,*args,**kwargs):
  rows=old_players(conn,*args,**kwargs);out=[]
  for row in rows:
   if str(row.get('id')) in NAMES:
    row=dict(row);row['name']=row['name_en']=NAMES[str(row['id'])]
   out.append(row)
  return out
 player_editor.players=players
 return True
