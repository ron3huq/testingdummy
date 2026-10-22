"""Exercise Python installation/diagnostics with native boundary mocked."""
from pathlib import Path
import importlib.util,tempfile,json,ctypes,sys
r=Path(__file__).parent;sys.path.insert(0,str(r))
spec=importlib.util.spec_from_file_location('runtime',r/'select_team_runtime.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
engine=(r.parent/'android/official-apk/lib/arm64-v8a/libUE4.so').read_bytes()
class Stop(BaseException):pass
class Fn:
 def __init__(self,f=lambda *a:0):self.f=f
 def __call__(self,*args):return self.f(*args)
class Handle:
 def __init__(self):self.trial=False;self.ready=0
 def __getattr__(self,name):
  funcs={'editor_commit':lambda:(setattr(self,'ready',1),1)[1],'editor_status':lambda i:[self.ready,0,0,0,0][i],'set_appearance_trial':lambda v:setattr(self,'trial',False), 'appearance_card_status':lambda i:[0,2,88044950524330,1,3,5,0,int(self.trial)][i], 'appearance_diagnostic':lambda i:[123,20,2,17,1,89138556572074,89138556572074,0,1][i], 'appearance_shirt_status':lambda i:[30,2,3,5,4522,0,1][i], 'appearance_seen':lambda stage,i:([89138556572074,114758]if stage==0 else [4522,16781738])[i]if i<2 else 0,'appearance_status':lambda:4}
  f=Fn(funcs.get(name,lambda *a:0))
  setattr(self,name,f);return f
m.platform.machine=lambda:'aarch64';m.maps=lambda:[(0,0x10000000,'r-xp',0,'/fake/libUE4.so')]
def stop(*a):raise Stop
m.time.sleep=stop
reports=[]
for fail_entity,trial_enabled in [(False,False),(True,False),(False,True)]:
 hook=Handle();entries=[]
 def install(base,path,entry=m.GETTER,prologue=m.PROLOGUE,hook_name='menu_hook',**kw):
  assert engine[entry-0x4000:entry-0x4000+16]==prologue,(hex(entry),hook_name)
  entries.append(entry)
  if fail_entity and entry==0x68db150:raise RuntimeError('modeled entity installation failure')
  return hook
 m.install=install
 with tempfile.TemporaryDirectory()as d:
  m.HERE=Path(d)
  settings=json.loads((r/'myleague_custom.json').read_text());settings['requested_appearance']['sleeve_copy']['rolled_trial']['enabled']=trial_enabled
  (m.HERE/'myleague_custom.json').write_text(json.dumps(settings))
  try:m.worker()
  except Stop:pass
  out=json.loads((m.HERE/'select-team-status.json').read_text())
  assert out['state']=='HOOK_ACTIVE' and out['version']=='native-hotfix-v18'
  assert out['appearance_build_matches']==2 and out['appearance_sleeve_applies']==4
  assert out['appearance_last_build_id']==89138556572074
  assert hook.appearance_diagnostic.restype is ctypes.c_uint64
  assert all(e in entries for e in [0x68d0868,0x68ceb44,0x68db150,0x3a0b28c])
  assert bool(out['appearance_error'])==fail_entity
  assert out['appearance_hooks']['build']=='INSTALLED' and out['appearance_hooks']['shirt']=='INSTALLED'
  assert out['editor_error']is None and out['editor_status']['ready']==1
  assert out['appearance_trial_error']is None and out['appearance_trial_enabled']is False and hook.trial is False
  assert out['appearance_policy_matches']=={'Y17':3,'UEFA':5,'rolled_trial':0}
  assert out['appearance_build_matches_by_id']=={'89138556572074':0,'88044950524330':2}
  assert out['appearance_last_applied_id']==88044950524330 and out['appearance_build_after']==1
  assert out['appearance_shirt_applies']==5 and out['appearance_shirt_alias_matches']==3
  assert out['appearance_build_ids']==[114758,89138556572074] and out['appearance_shirt_ids']==[4522,16781738]
  assert (out['appearance_hooks']['entity']=='INSTALLED')== (not fail_entity)
  reports.append({'entity_install_failure_modeled':fail_entity,'trial_enabled':trial_enabled,'state':out['state'],'full64_id_preserved':True,'all_existing_appearance_prologues_match_original_engine':True})
report={'status':'APPEARANCE_RUNTIME_PASS','device_tested':False,'boundary':'native installation mocked; engine prologues checked against actual ELF','cases':reports}
(r/'appearance-runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
