from pathlib import Path
import ast,types,json,sys,zipfile,marshal,tempfile,shutil
P=Path('/workspace/ronaldo-work/73-ui75');root=Path('/workspace/ronaldo-work/73-v25-full/test-gateway');sys.path.insert(0,str(P/'payload/work/tools'))
a=zipfile.ZipFile('/workspace/ronaldo-work/73-inspect/v16-meta/assets/chaquopy/app.imy');pr=types.ModuleType('_protected_runtime');pr.__file__=str(root/'work/tools/_protected_runtime.py');sys.modules[pr.__name__]=pr;exec(marshal.loads(a.read('_protected_runtime.pyc')[16:]),pr.__dict__);pr.install_root(root)
import team_kits
cfg=json.loads((P/'payload/work/tools/myleague_custom.json').read_text());tree=ast.parse((P/'payload/work/tools/myleague_73.py').read_text());install=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='install');start=next(n for n in install.body if isinstance(n,ast.FunctionDef)and n.name=='start');start.decorator_list=[]
ns={'cfg':cfg,'json':json,'y08_uniform_ids':None,'worlds':types.SimpleNamespace(edit_projection=lambda p:p,_prepare_environment=lambda s:None),'editor':types.SimpleNamespace(project=lambda p,c:p)}
helper=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='y08_uniform_ids');slots=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='Y08_KIT_SLOTS'for t in n.targets));exec(compile(ast.Module(body=[slots,helper,start],type_ignores=[]),'production-y08-route','exec'),ns)
r=Path(tempfile.mkdtemp());ns['HERE']=r
state={};fixture={}
ns['context']=lambda conn:(state,state['competition_id'])
ns['league']=types.SimpleNamespace(state=lambda conn:state,current=lambda s:(None,fixture,None),fail=lambda *a:{'result':'ERROR'})
ns['report']=lambda *a,**k:None
calls=[]
def old(conn,resp,req,entries):calls.append(entries);return {'result':'NOERR','uniform_list_home':{'base_team_id':0,'uniform_list':[]},'uniform_list_away':{'base_team_id':999,'uniform_list':[]}}
ns['old_start']=old;total=0
for own in cfg['leagues']['473']['teams']:
 for opponent in cfg['leagues']['473']['teams']:
  if own==opponent:continue
  for side in ['HOME','AWAY']:
   state.update(team_id=own,competition_id=473,active={'side':side});fixture.update(home_team_id=own,away_team_id=opponent);reply=ns['start'](None,{}, {},[{'id':'owned'}]);assert calls[-1]==[{'id':'owned'}]
   for key,team in [('home'if side=='HOME'else'away',own),('away'if side=='HOME'else'home',opponent)]:
    route=reply['uniform_list_'+key];assert route['base_team_id']==team and len(route['uniform_list'])>=2
    assert all(v>>14==team for v in route['uniform_list'])
    donor=cfg['kit_aliases'][str(team)];assert [v&16383 for v in route['uniform_list']]==[v&16383 for v in ns['y08_uniform_ids'](donor)]
   total+=1
state.update(competition_id=518);reply=ns['start'](None,{}, {},[]);assert reply['uniform_list_home']['base_team_id']==0 and reply['uniform_list_away']['base_team_id']==999
shutil.rmtree(r);report={'passed':True,'production_start_wrapper_AST':True,'original_start_boundary_simulated':True,'Y08_opponent_pairs_and_user_sides':total,'all10_logical_team_IDs_consistent_with_rosters_and_uniform_keys':True,'donor_slot_selection_retained':True,'owned_players_unchanged':True,'Y17_branch_unchanged':True,'device_tested':False};(P/'kits-wire-validation.json').write_text(json.dumps(report,indent=2));print('Y08_WIRE_PASS',total)
