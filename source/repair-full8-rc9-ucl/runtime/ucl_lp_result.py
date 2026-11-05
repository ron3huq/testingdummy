"""Decode APK73 native score fields verified by static inspection of v19.1.
No invented extra time, shootouts, scorers, or abandoned-match outcomes.
This parser does not install command/UI hooks or enable aggregate engine rules.
"""
from ucl_lp_mode import UclError,session_key,aggregate_before,needs_decision,score,number
PERIODS=('score_1st','score_2nd','score_ex1st','score_ex2nd')

def game_id(request):
    if not isinstance(request,dict):raise UclError('result packet must be an object')
    detail=request.get('match_result')
    if not isinstance(detail,dict):raise UclError('missing native match_result')
    nested=detail.get('game_id');outer=request.get('game_id')
    if nested is None:nested=outer
    key=session_key(nested)
    if outer is not None and session_key(outer)!=key:raise UclError('conflicting native session IDs')
    return key

def decode(state,fixture,request):
    game_id(request)
    detail=request['match_result'];rows=request.get('score')
    if not isinstance(rows,list)or len(rows)!=2:raise UclError('two native score rows required')
    periods=[]
    for row in rows:
        if not isinstance(row,dict)or not any(k in row for k in PERIODS):raise UclError('missing native period scores')
        periods.append([number(row.get(k,0))for k in PERIODS])
    regulation=[sum(row[:2])for row in periods];extra=[sum(row[2:])for row in periods];total=[number(a+b)for a,b in zip(regulation,extra)]
    before=aggregate_before(state,fixture)if fixture['leg']==2 else(0,0)
    can_decide=needs_decision(state,fixture);tied_after90=regulation[0]+before[0]==regulation[1]+before[1]
    if any(extra)and not(can_decide and tied_after90):raise UclError('extra-time goals not permitted for this fixture/aggregate')
    flag=detail.get('pk_flag','NO')
    if flag not in('YES','NO'):raise UclError('invalid native penalty flag')
    penalties=[row.get('score_pk',0)for row in rows]
    for value in penalties:number(value)
    if flag=='NO'and any(penalties):raise UclError('penalty scores without native penalty flag')
    # Do not treat a forfeit/disconnect as a played score without a verified policy.
    if detail.get('gameend_reason')not in(None,'','NORMAL_END')or detail.get('abnormalend_reason')not in(None,'','NOERR')or request.get('intentional_give_up')=='YES':raise UclError('abandoned/abnormal-match policy not verified')
    return score(state,fixture,*total,*penalties)if flag=='YES'else score(state,fixture,*total)
