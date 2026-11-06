"""Single-match knockout rules requested by the user; retain old season format."""
import json,sys,copy,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
from ucl_lp_mode import *
from ucl_lp_result import decode

def rejected(fn):
    try:fn()
    except UclError:return
    raise AssertionError('invalid score accepted')

def run():
    data=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text());teams=data['teams'];routes=[]
    for cutoff in (0,8):
        for draw in data['draws']:
            state=new(teams,draw['rounds'],4219,123,knockout_legs=1)
            for day in range(8):
                for match in current_matches(state):match['result']=simulate(state,match)
                if day==7:state['own']=table(state)[cutoff]['team_id']
                transition(state)
            advance_cpu(state);own=state['own'];penalties=0
            while not state['champion']:
                match=own_match(state);assert match and needs_decision(state,match)and match['leg']==1
                # A drawn knockout requires a real, deciding shootout receipt.
                rejected(lambda:score(state,match,0,0))
                h,a=(5,4)if match['home']==own else(4,5)
                apply(state,match['id'],dict(home=0,away=0,pk_home=h,pk_away=a));penalties+=1
            assert state['champion']==own and len(state['matches'])==167
            assert all(m['leg']==1 for m in state['matches'])
            assert sum(own in(m['home'],m['away'])for m in state['matches'])==(12 if cutoff==0 else 13)
            assert penalties==(4 if cutoff==0 else 5)
            from ucl_lp_view import projection
            view=projection(state)
            assert all(row['result']=='WIN'for key,row in view['played'].items()if int(key)>8)
        routes.append(12 if cutoff==0 else 13)
    state=new(teams,data['draws'][0]['rounds'],4219,1,knockout_legs=1)
    add_ties(state,'QF',[(4219,114)],True);match=own_match(state)
    # ET winner, or tied after ET + real PK. PK kicks remain separate from goals.
    request=dict(match_result=dict(game_id=123,pk_flag='NO'),score=[dict(score_1st=0,score_2nd=1,score_ex1st=1),dict(score_1st=1,score_2nd=0)])
    assert decode(state,match,request)['home']==2
    request['score'][1]['score_ex2nd']=1;rejected(lambda:decode(state,match,request))
    request['match_result']['pk_flag']='YES';request['score'][0]['score_pk']=5;request['score'][1]['score_pk']=4
    value=decode(state,match,request);assert(value['home'],value['away'],value['pk_home'])==(2,2,5)
    request['score'][0]['score_2nd']=2;rejected(lambda:decode(state,match,request))
    c=sqlite3.connect(':memory:');store=Store(c);assert store.create(teams,data['draws'][0]['rounds'],4219,1,knockout_legs=1)['knockout_legs']==1
    legacy=new(teams,data['draws'][0]['rounds'],4219,1);legacy.pop('knockout_legs');add_ties(legacy,'QF',[(4219,114)],True)
    assert len([m for m in legacy['matches']if m['stage']=='QF'])==2
    print(json.dumps(dict(passed=True,draws_checked=8,whole_season_champion_routes=routes,total_matches=167,no_return_legs=True,extra_time_native_scores=True,shootout_native_scores=True,old_saved_season_format_preserved=True,phone_verified=False),indent=2))
if __name__=='__main__':run()
