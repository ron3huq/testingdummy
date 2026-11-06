"""Explicit UCL selection and command routing; normal My League stays separate.
Not installed into the shipped RC7 gateway. Activation requires aggregate setup.
"""
import json,copy
from pathlib import Path
from ucl_lp_mode import Store,UclError,session_key,own_match,table
from ucl_lp_stats import leaderboard
from ucl_lp_result import game_id
PASS=object()
MODE_KEY='ucl_lp_enabled_season'

class Controller:
    def __init__(self,conn,bridge_factory,draws=None,home_entries=None):
        self.conn=conn;self.store=Store(conn);self.bridge_factory=bridge_factory;self.home_entries=home_entries
        self.draws=draws or json.loads(Path(__file__).with_name('ucl_lp_draws.json').read_text())
    def enabled(self):
        row=self.conn.execute('SELECT value FROM meta WHERE key=?',(MODE_KEY,)).fetchone();season=self.store.get()
        return bool(row and season and row[0]==season['season_uuid'])
    def status(self):
        season=self.store.get();bridge=self.bridge_factory()
        return dict(ready=bridge.aggregate_setup is not None,enabled=self.enabled(),draw_count=len(self.draws['draws']),teams=self.draws['teams'],levels=['VERYEASY','EASY','NORMAL','HARD','VERYHARD','HARDEST','LEGEND'],season=None if season is None else dict(id=season['season_uuid'],own=season['own'],stage=season['stage'],knockout_legs=season.get('knockout_legs',2),round=season['round'],champion=season['champion'],pending=season.get('active')is not None,ranking=table(season),matches=copy.deepcopy(season['matches']),goals=leaderboard(season),assists=leaderboard(season,'assists')))
    def manage(self,request):
        op=request.get('op','status')
        if op=='status':return self.status()
        if op=='create':
            previous=self.store.get()
            if previous and request.get('replace_season_uuid')!=previous['season_uuid']:raise UclError('confirm the current season before creating another one')
            index=request.get('draw',0)
            if type(index)is not int or not 0<=index<len(self.draws['draws']):raise UclError('invalid draw index')
            self.store.create(self.draws['teams'],self.draws['draws'][index]['rounds'],request.get('team_id'),request.get('seed',0),request.get('level','NORMAL'))
        elif op=='activate':
            bridge=self.bridge_factory()
            if bridge.aggregate_setup is None:raise UclError('UCL aggregate match setup is not ready')
            with self.store.transaction():
                season=self.store.get()
                if not season:raise UclError('create a UCL season first')
                self.conn.execute('INSERT OR REPLACE INTO meta(key,value)VALUES(?,?)',(MODE_KEY,season['season_uuid']))
        elif op=='leave':
            with self.store.transaction():
                season=self.store.get()
                if season and season.get('active'):raise UclError('finish the pending UCL match before leaving')
                self.conn.execute('DELETE FROM meta WHERE key=?',(MODE_KEY,))
        else:raise UclError('unsupported UCL operation')
        return self.status()
    def route(self,command,request,response):
        if command=='CMD_GET_VSCOM_GAME_RESULT':
            # Route an existing UCL receipt even after an app restart; do not claim
            # another mode's result just because the UCL menu was selected.
            try:game=game_id(request)
            except UclError:return PASS
            row=self.conn.execute('SELECT game FROM ucl_lp_sessions WHERE game=?',(game,)).fetchone()
            if row:return self.bridge_factory().finish(request,response)
            return PASS
        if not self.enabled():return PASS
        bridge=self.bridge_factory()
        if command=='CMD_SET_SEASON_ENTER':return bridge.enter(request)
        if command=='CMD_SET_MYCLUB_SPECIAL_DREAM_SQUAD_INFO':return bridge.special(request)
        if command=='CMD_GET_SEASON_INFO':return bridge.info(response,request)
        if command=='CMD_GET_SEASON_SCHEDULE':return bridge.schedule(response,request)
        if command=='CMD_GET_VSCOM_OPPONENT':
            if not bridge.league.is_season(request):return PASS
            return bridge.prepare(request)
        if command=='CMD_START_GAME':
            try:game=session_key(request.get('game_id'))
            except UclError:return PASS
            season=self.store.get();active=season.get('active')if season else None
            if not active or game!=session_key(active['game_id']):return PASS
            # Entry construction belongs to the installed gateway's owned-player
            # path. Never invent or replace its native player objects here.
            if self.home_entries is None:raise UclError('unsupported gateway owned-entry binding')
            refs=bridge.home_references(request);entries=self.home_entries(refs,log_substitutes=False)
            return bridge.start(response,request,entries)
        return PASS
