"""Host event policy checks; optional comparison with actual v25 function code."""
import copy,json,marshal,sys,types,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_event_rules import configure
from ucl_lp_mode import UclError

def run(path=None):
    source={'match_env':{'ball':'original','exTime':'NO','pk':'NO'},'ch_mission_info_list':[{'unchanged':17}]};original=copy.deepcopy(source)
    for stage in ['LEAGUE_PHASE','PLAYOFFS','R16','QF','SF','FINAL']:
        for level in ['VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND']:
            value=configure(source,dict(stage=stage,cpu_level=level,knockout_legs=1));flag='NO'if stage=='LEAGUE_PHASE'else'YES'
            assert value['match_env']==dict(ball='original',exTime=flag,pk=flag,cpu_level=level)
            assert source==original and value['ch_mission_info_list']==original['ch_mission_info_list']
    for template,state in [({},dict(stage='R16',knockout_legs=1)),(source,dict(stage='R16',knockout_legs=2)),(source,dict(stage='UNKNOWN',knockout_legs=1))]:
        try:configure(template,state)
        except UclError:pass
        else:raise AssertionError('invalid event policy accepted')
    report=dict(passed=True,stage_level_combinations=42,league_phase_extra_time_disabled=True,knockout_extra_time_penalties_enabled=True,source_template_unchanged=True,start_reply_root_not_used=True,native_event_entry_integrated=False,phone_verified=False)
    if path:
        raw=Path(path).read_bytes();code=marshal.loads(raw[16:]);function=next(c for c in code.co_consts if isinstance(c,types.CodeType)and c.co_name=='_knockout_event')
        assert function.co_filename=='cup_entry.py'
        # Execute this selected function only; no protected-module initialization.
        namespace=dict(copy=copy,TITLE='reference',KNOCKOUT_DESCRIPTION='reference',_banner_fields=lambda spec:{},CPU_LEVELS=['NORMAL'])
        native=types.FunctionType(function,namespace)
        spec=types.SimpleNamespace(key='ucl',knockout_event_id=1120007,knockout_compe_unit_id=16001)
        reference=native(source,dict(two_legs=False,phase='R16'),spec)
        ours=configure(source,dict(stage='R16',cpu_level='NORMAL',knockout_legs=1))
        assert reference['match_env']==ours['match_env']and source==original
        report.update(actual_v25_knockout_function_compared=True,v25_input_sha256=hashlib.sha256(raw).hexdigest())
    print(json.dumps(report,indent=2))
if __name__=='__main__':run(sys.argv[1]if len(sys.argv)>1 else None)
