"""Document math, CPU isolation, frozen season policy and legal knockout scores."""
import collections,copy,json,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'runtime'))
import ucl_lp_probability as p
import ucl_lp_mode as core

def run():
    assert sum(row[2]for row in p.CLOSE)==120
    assert sum(row[2]for row in p.BIG)==113
    assert sum(row[2]for row in p.DRAWS)==100
    assert p.probabilities(1,1)==(.4,.27,.33)
    assert p.probabilities(1,1,neutral=True)==(.365,.27,.365)
    for a in range(1,6):
        for b in range(1,6):
            regular=p.probabilities(a,b);neutral=p.probabilities(a,b,neutral=True)
            assert abs(sum(regular)-1)<1e-12
            assert all(abs(x-y)<1e-12 for x,y in zip(neutral,p.probabilities(b,a,neutral=True)[::-1]))
            assert abs(p.probabilities(a,b,derby=True)[1]-regular[1]-.05)<1e-12
    value=p.probabilities(3,1,away_streak=3)
    assert all(abs(a-b)<1e-12 for a,b in zip(value,(.19133333333333333,.21866666666666668,.59)))
    # Same draw stream: prolific scoring changes score distribution, never W/D/L.
    for seed in range(3000):
        a=p.regulation(random.Random(seed),1,5)
        b=p.regulation(random.Random(seed),1,5,prolific=(True,True))
        assert (a['home']>a['away'],a['home']==a['away'])==(b['home']>b['away'],b['home']==b['away'])
    data=json.loads((Path(__file__).parent/'runtime/ucl_lp_draws.json').read_text())
    state=core.new(data['teams'],data['draws'][0]['rounds'],4219,123)
    assert collections.Counter(state['cpu_policy']['groups'].values())=={1:4,2:2,3:5,4:13,5:12}
    assert state['cpu_policy']['count_extra_time_goals'] is True
    assert state['cpu_policy']['count_shootout_goals'] is False
    match=core.own_match(state)
    actual=dict(home=99,away=0)
    core.apply(state,match['id'],actual)
    assert match['result']['home']==99 and 'simulation'not in match['result']
    cpu=next(m for m in state['matches']if m['result']and m is not match)
    assert cpu['result']['simulation']['model']==p.MODEL
    # Penalized series must be accepted by the independent terminal-score validator.
    test=core.new(data['teams'],data['draws'][0]['rounds'],4219,1)
    test['matches'].append(dict(id='test-final',stage='FINAL',round=1,leg=1,home=4219,away=114,result=None))
    final=test['matches'][-1]
    for seed in range(10000):
        h,a=p.shootout(random.Random(seed))
        core.score(test,final,0,0,h,a)
    # Streak resets on a draw or reversed result; future fixtures do not count.
    s={'matches':[dict(id=str(i),home=1,away=2,result=dict(home=h,away=a))for i,(h,a)in enumerate([(1,0),(2,0),(3,0),(0,0),(0,1),(0,2)])]}
    assert p.streak(s,1,'3')==3 and p.streak(s,1,'4')==0 and p.streak(s,1,'end')==-2
    print(json.dumps(dict(passed=True,score_weight_totals=[120,113],penalty_series_checked=10000,human_result_preserved=True,extra_time_goals_count=True,shootout_goals_count=False)))
if __name__=='__main__':run()
