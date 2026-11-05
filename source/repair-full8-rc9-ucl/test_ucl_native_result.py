"""Real v19.1 score-field contract, aggregate edge cases and atomic persistence."""
from pathlib import Path
import sys,json,sqlite3,copy
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import *
from ucl_lp_result import decode,game_id

def packet(home,away,extra=(0,0),pk=None,gid=9007199254740993):
    rows=[dict(score_1st=h,score_2nd=0,score_ex1st=e,score_ex2nd=0)for h,e in zip((home,away),extra)]
    if pk is not None:
        for row,value in zip(rows,pk):row['score_pk']=value
    return dict(score=rows,match_result=dict(game_id=gid,pk_flag='YES'if pk is not None else'NO',gameend_reason='NORMAL_END',abnormalend_reason='NOERR'))

def fails(fn):
    try:fn()
    except UclError:return
    raise AssertionError('invalid native result accepted')

def run():
    doc=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text());teams=doc['teams'];draw=doc['draws'][0]['rounds'];s=new(teams,draw,teams[0]['team_id'],0);m=own_match(s)
    assert decode(s,m,packet(1,0))['home']==1
    fails(lambda:decode(s,m,packet(1,0,extra=(1,0))))
    fails(lambda:decode(s,m,packet(0,0,pk=(5,4))))
    req=packet(0,0);req['score'][0]['score_1st']=True;fails(lambda:decode(s,m,req))
    req=packet(0,0);req['game_id']='9007199254740995';fails(lambda:game_id(req))
    for key,value in [('gameend_reason','NORMAL_GIVEUP'),('abnormalend_reason','NORMAL_GIVEUP'),('abnormalend_reason','NETWORK_ERROR')]:
        req=packet(1,0);req['match_result'][key]=value;fails(lambda:decode(s,m,req))
    req=packet(1,0);req['intentional_give_up']='YES';fails(lambda:decode(s,m,req))
    a,b=teams[0]['team_id'],teams[1]['team_id'];add_ties(s,'PLAYOFFS',[(a,b)],True);one,two=s['matches'][-2:];one['result']=score(s,one,2,1)
    # Second-leg1-0 is NOT a draw in isolation, but ties the aggregate2-2.
    assert decode(s,two,packet(1,0,pk=(2,0)))['pk_home']==2
    assert decode(s,two,packet(1,0,pk=(1,0)))['pk_home']==1
    fails(lambda:decode(s,two,packet(1,0)))
    assert decode(s,two,packet(1,0,extra=(1,0)))['home']==2
    fails(lambda:decode(s,two,packet(0,0,extra=(1,0))))
    fails(lambda:decode(s,two,packet(2,0,pk=(5,4))))
    for valid in [(1,0),(2,0),(3,0),(4,1),(5,3),(5,4),(6,5),(20,19)]:assert valid_shootout(*valid)and valid_shootout(*valid[::-1])
    for invalid in [(0,0),(1,1),(4,0),(5,1),(5,2),(6,4),(6,6)]:assert not valid_shootout(*invalid)
    conn=sqlite3.connect(':memory:');st=Store(conn);st.create(teams,draw,a,0);st.reserve('9007199254740993',{'fixture':'original'});st.start('9007199254740993');before=st.get();bad=packet(1,0,extra=(1,0));fails(lambda:st.finish_native(bad));assert st.get()==before;assert conn.execute('SELECT receipt FROM ucl_lp_sessions').fetchone()[0]is None
    receipt=st.finish_native(packet(1,0));after=copy.deepcopy(st.get());assert st.finish_native(dict(match_result=dict(game_id='9007199254740993')))==receipt;assert st.get()==after;conn.close()
    print(json.dumps(dict(passed=True,native_period_fields_verified=True,non_draw_leg_aggregate_penalties=True,legal_low_shootout_scores=True,illegal_early_terminal_scores_rejected=True,extra_time_requires_tied_aggregate=True,abnormal_result_rejected=True,invalid_result_rolls_back=True,duplicate_native_receipt=True,command_hooks_installed=False,phone_verified=False),indent=2))
if __name__=='__main__':run()
