"""Native event metadata policy. This is not a CMD_START_GAME root extension.
Two-leg returns require a separately verified aggregate-aware native provider.
"""
import copy
from ucl_lp_mode import UclError,TWO_LEGS
LEVELS={'VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND'}

def configure(source,state,native_aggregate_ready=False):
    if not isinstance(source,dict)or not isinstance(source.get('match_env'),dict):raise UclError('native event template with match_env is required')
    legs=state.get('knockout_legs',2)
    if type(legs)is not int or legs not in(1,2)or type(native_aggregate_ready)is not bool:raise UclError('invalid knockout/native setup policy')
    stage=state.get('stage');level=state.get('cpu_level','NORMAL')
    if stage not in TWO_LEGS|{'FINAL','LEAGUE_PHASE'}or level not in LEVELS:raise UclError('invalid UCL event stage/difficulty')
    deciding=stage!='LEAGUE_PHASE'
    if stage in TWO_LEGS and legs==2:
        leg=state.get('round')
        if type(leg)is not int or leg not in(1,2):raise UclError('two-leg event requires the exact current leg')
        deciding=leg==2
        if deciding and not native_aggregate_ready:raise UclError('return-leg extra time requires verified native aggregate setup')
    out=copy.deepcopy(source)
    out['match_env'].update(exTime='YES'if deciding else'NO',pk='YES'if deciding else'NO',cpu_level=level)
    return out
