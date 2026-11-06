import sys,sqlite3,types,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_install import install
from ucl_lp_mode import UclError

def run():
    calls=[]
    class Logic:
        responses={};templates={}
        def __init__(self):
            self.conn=sqlite3.connect(':memory:');self.conn.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');self.conn.commit()
        def handle(self,cmd,req):calls.append(cmd);return dict(original=True)
        def _home_entries(self,refs,log_substitutes=False):return refs
    module=types.SimpleNamespace(_logic=Logic(),manage=lambda a,p:json.dumps(dict(original=True)))
    native=types.SimpleNamespace(aggregate_setup=None,info=lambda resp,req:dict(result='NOERR',ranking=list(range(36))),league=types.SimpleNamespace(is_season=lambda r:r.get('match_category')=='MYLEAGUE'))
    prior=sys.modules.get('my_league');sys.modules['my_league']=types.SimpleNamespace(fail=lambda cmd,req:dict(result='FAIL',msgid=cmd))
    try:
        assert install(module,bridge_factory=lambda logic:native)
        assert not install(module,bridge_factory=lambda logic:native)
        assert module._logic.handle('CMD_GET_SEASON_INFO',{})==dict(original=True)
        data=json.loads(module.manage('ui73_ucl','{}'));assert data['season']is None
        module.manage('ui73_ucl',json.dumps(dict(op='create',team_id=data['teams'][0]['team_id'])))
        try:module.manage('ui73_ucl',json.dumps(dict(op='activate')))
        except UclError:pass
        else:raise AssertionError('incomplete native aggregate activated')
        native.aggregate_setup=lambda *args:None;module.manage('ui73_ucl',json.dumps(dict(op='activate')))
        assert len(module._logic.handle('CMD_GET_SEASON_INFO',{})['ranking'])==36
        assert module._logic.handle('CMD_GET_VSCOM_OPPONENT',dict(match_category='EXHIBITION'))==dict(original=True)
        assert json.loads(module.manage('other','{}'))==dict(original=True)
        # Instance scoping: another gateway instance must retain its own behavior.
        other=Logic();assert other.handle('CMD_GET_SEASON_INFO',{})==dict(original=True)
        module.manage('ui73_ucl',json.dumps(dict(op='leave')));assert module._logic.handle('CMD_GET_SEASON_INFO',{})==dict(original=True)
        print(json.dumps(dict(passed=True,entry_routing=True,normal_mode_passthrough=True,other_gateway_instance_unchanged=True,activation_requires_aggregate_provider=True,installed_in_shipped_payload=False),indent=2))
    finally:
        if prior is None:sys.modules.pop('my_league',None)
        else:sys.modules['my_league']=prior
if __name__=='__main__':run()
