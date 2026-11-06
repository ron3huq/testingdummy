"""Native event metadata rules, matching v25's single-match knockout path.
This edits an existing event definition, not the CMD_START_GAME response root.
Entry projection and match routing must use the same selected UCL season.
"""
import copy
from ucl_lp_mode import UclError,TWO_LEGS
LEVELS={'VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND'}

def configure(source,state):
    if not isinstance(source,dict)or not isinstance(source.get('match_env'),dict):raise UclError('native event template with match_env is required')
    if state.get('knockout_legs',2)!=1:raise UclError('this provider only supports single-match knockout seasons')
    stage=state.get('stage');level=state.get('cpu_level','NORMAL')
    if stage not in TWO_LEGS|{'FINAL','LEAGUE_PHASE'}or level not in LEVELS:raise UclError('invalid UCL event stage/difficulty')
    out=copy.deepcopy(source);deciding=stage!='LEAGUE_PHASE'
    out['match_env'].update(exTime='YES'if deciding else'NO',pk='YES'if deciding else'NO',cpu_level=level)
    return out
