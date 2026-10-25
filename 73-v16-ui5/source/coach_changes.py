"""Exact two manager projections; immutable owned rows and all other managers."""
import copy,functools
RULES={17606144688129:('Zinedine Zidane',45,208,21),17604802510874:('Sir Alex Ferguson',66,232,53)}
def project(row):
 identity=row.get('coach_id');cid=identity.get('id')if isinstance(identity,dict)else identity
 try:rule=RULES.get(int(cid))
 except(TypeError,ValueError):return row
 if not rule:return row
 out=copy.deepcopy(row);name,age,nation,flag=rule;out.update(age=age,is_coach_texture_use='YES',name=name,name_en=name,_nation_id=nation,initial_base_national_team_id=flag)
 return out

def install():
 import club_store
 if getattr(club_store.coaches,'_ui4_coaches',False):return False
 original=club_store.coaches
 @functools.wraps(original)
 def coaches(*args,**kwargs):return[project(row)for row in original(*args,**kwargs)]
 coaches._ui4_coaches=True;club_store.coaches=coaches
 return True
