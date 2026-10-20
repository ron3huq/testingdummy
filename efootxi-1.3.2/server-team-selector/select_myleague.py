#!/usr/bin/env python3
"""Select a My League club on a NEW COPY of an efootxi 1.3.2 save, using its own server logic."""
import argparse,hashlib,importlib,json,os,sqlite3,sys,tempfile,uuid
from pathlib import Path
EXPECTED_MODULE = '06ef47e1700e408044543ebc227729bff8904b63a68891c825a70e2a9d047f0b'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def game_tables(conn):
 out={}
 for (name,) in conn.execute("select name from sqlite_master where type='table' and name not in ('meta','events','sqlite_sequence') order by name"):
  escaped='"'+name.replace('"','""')+'"';h=hashlib.sha256();count=0
  for row in conn.execute('select * from '+escaped):
   h.update(json.dumps(list(row),ensure_ascii=False,default=lambda x:{'blob':x.hex()},separators=(',',':')).encode());h.update(b'\n');count+=1
  out[name]=(count,h.hexdigest())
 return out

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--gateway',required=True,type=Path,help='extracted gateway-release directory containing work/ and outputs/')
 p.add_argument('--list',action='store_true',help='list teams for the competition; no save is opened')
 p.add_argument('--competition',type=int,default=122)
 p.add_argument('--input-save',type=Path)
 p.add_argument('--output-save',type=Path)
 p.add_argument('--team',type=int)
 p.add_argument('--restart-season',action='store_true',help='explicitly permit restarting an existing My League season in the OUTPUT COPY')
 a=p.parse_args();gateway=a.gateway.resolve();module=gateway/'work/tools/my_league.py'
 if not module.is_file() or digest(module)!=EXPECTED_MODULE:raise ValueError('Unsupported my_league.py version: use the matching efootxi 1.3.2 gateway code.')
 registry=json.loads((gateway/'outputs/reference/ziru-data/ml_competition_registry.json').read_text(encoding='utf-8'));competition=registry['competitions'].get(str(a.competition))
 if not competition:raise ValueError('Unknown competition.')
 if a.list:
  print(json.dumps({'competition':a.competition,'teams':competition['teams']},ensure_ascii=False,indent=2));return
 if not a.input_save or not a.output_save or not a.team:p.error('use --list, or provide --input-save, --output-save and --team')
 source=a.input_save.resolve();output=a.output_save.resolve()
 if source==output or output.exists():raise ValueError('Output must be a different NEW path. Existing files are never overwritten.')
 if not source.is_file():raise ValueError('Input save missing.')
 if any(Path(str(source)+s).exists() and Path(str(source)+s).stat().st_size for s in ['-wal','-journal']):raise ValueError('Input has pending WAL/journal. Export a consistent SQLite backup after stopping the game first.')
 if a.team not in competition['team_ids'] or registry['team_to_competition'].get(str(a.team))!=a.competition:raise ValueError('Team is not a member of the selected competition in this gateway registry.')
 source_sha=digest(source);sys.dont_write_bytecode=True;sys.path.insert(0,str(gateway/'work/tools'))
 league=importlib.import_module('my_league');output.parent.mkdir(parents=True,exist_ok=True)
 input_conn=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True)
 try:
  if input_conn.execute('pragma quick_check').fetchone()[0]!='ok':raise ValueError('Input integrity check failed.')
  with tempfile.TemporaryDirectory(prefix='.myleague-copy-',dir=output.parent) as tmp:
   temp=Path(tmp)/'save.sqlite3';conn=sqlite3.connect(temp);conn.row_factory=sqlite3.Row
   try:
    input_conn.backup(conn);before=game_tables(conn);old=league.state(conn)
    if old and not a.restart_season:raise ValueError('Existing season found. --restart-season is required to replace it in the output copy.')
    if old and (old.get('active') or {}).get('started'):raise ValueError('A started My League match is pending. Finish it in game before changing teams.')
    if old and old['team_id']==a.team and not old['completed']:raise ValueError('This team already has an ongoing season; use the current save instead of restarting it.')
    request={'msgid':'CMD_SET_SEASON_ENTER','rqid':'offline-selector-'+uuid.uuid4().hex,'select_team_id':a.team,'select_compe_unit_id':a.competition}
    reply=league.select(conn,{},request,session_token='offline-selector')
    if reply.get('result')!='NOERR':raise ValueError('Server rejected selection: '+str(reply.get('result')))
    state=league.state(conn);root=league.root_view(conn,{'season_root_info':{}})['season_root_info'];schedule=league.fixtures(state)
    if state['team_id']!=a.team or state['competition_id']!=a.competition or root['team_id']!=a.team or root['league_compe_unit_id']!=a.competition:raise ValueError('Selection state mismatch.')
    if set(root['league_team_id_list'])!=set(competition['team_ids']):raise ValueError('League membership mismatch.')
    if game_tables(conn)!=before:raise ValueError('Unexpected modification outside season metadata/events. Output discarded.')
    conn.commit()
    if conn.execute('pragma quick_check').fetchone()[0]!='ok':raise ValueError('Output integrity check failed.')
    result={'status':'SERVER_LOGIC_VALIDATED_DEVICE_UNTESTED','team_id':a.team,'competition_id':a.competition,'season':state['season'],'rounds':len(schedule),'league_team_count':len(root['league_team_id_list']),'player_and_inventory_tables_unchanged':True,'input_sha256':source_sha}
   finally:conn.close()
   if digest(source)!=source_sha:raise ValueError('Input changed during operation. Output discarded.')
   # Exclusive creation prevents accidentally overwriting an existing output.
   with temp.open('rb') as src,output.open('xb') as dst:
    while block:=src.read(1<<20):dst.write(block)
   result['output_sha256']=digest(output);print(json.dumps(result,ensure_ascii=False,indent=2))
 finally:input_conn.close()

if __name__=='__main__':
 try:main()
 except Exception as exc:print('ERROR: '+str(exc),file=sys.stderr);sys.exit(1)
