"""Build the modern Dortmund roster through the existing RC7 editor ABI.
This authoring step adds only a scoped team row, never a classic replacement.
"""
import copy,json
from pathlib import Path
from ucl_lp_mode import UclError
ROLES={'GK':0,'CB':1,'LB':2,'RB':3,'DMF':4,'CMF':5,'LMF':6,'RMF':7,'AMF':8,'LWF':9,'RWF':10,'SS':11,'CF':12}
COORDS=[(26,8),(18,28),(34,28),(5,35),(47,35),(20,48),(32,48),(26,68),(43,76),(9,76),(26,90)]

def dortmund_row(candidate=None):
    if candidate is None:candidate=json.loads(Path(__file__).with_name('ucl_lp_dortmund_roster.json').read_text())
    players=candidate['players']
    if candidate['team_id']!=126 or not 11<=len(players)<=40:raise UclError('invalid Dortmund roster')
    ids=[str(p['player_id'])for p in players];shirts=[p['shirt']for p in players]
    if len(set(ids))!=len(ids)or len(set(shirts))!=len(shirts):raise UclError('duplicate player or shirt')
    if any(type(p['player_id'])is not int or p['player_id']<=0 or type(p['shirt'])is not int or not 1<=p['shirt']<=99 for p in players):raise UclError('invalid Dortmund player or shirt')
    if [p['starting']for p in players]!=[i<11 for i in range(len(players))]:raise UclError('invalid starting order')
    roster=[]
    for i,p in enumerate(players):
        role=ROLES[p['requested_role']];x,y=COORDS[i]if i<11 else(0,0)
        if i<11 and(role==0)!=(i==0):raise UclError('starting lineup requires one GK')
        roster.append(dict(id=str(p['player_id']),shirt=p['shirt'],role=role,x=x,y=y))
    plan=dict(flags=0,slots=[{k:p[k]for k in('role','x','y')}for p in roster[:11]])
    # Existing verified ABI scope122 is the modern UEFA competition, not global0.
    # This also updates Dortmund when used in ordinary UEFA My League.
    return dict(team_id=126,competition=122,name='Borussia Dortmund',roster=roster,plans=[copy.deepcopy(plan)for _ in range(4)],captain='46825',kickers=['102240','60928','60928','60928','60928','142237'])

def inject(config):
    result=copy.deepcopy(config);row=dortmund_row()
    if any(r.get('team_id')==126 and r.get('competition')in(0,122)for r in result.get('teams',[])):raise UclError('Dortmund overlay already exists; refusing to overwrite')
    result.setdefault('teams',[]).append(row)
    return result
