from pathlib import Path
import base64,gzip,json,hashlib
r=Path('/workspace/analysis/my-league/hotfix-v16');app=Path(__file__).parent
names=['gateway_runtime.py','select_team_runtime.py','libselect_team.so','myleague_realism.py','myleague_worlds.py','myleague_balance.py','myleague_custom.json','myleague_editor_runtime.py']
payload={n:base64.b64encode((r/n).read_bytes()).decode()for n in names}
html=(app/'template.html').read_text().replace('__CATALOG__',base64.b64encode(gzip.compress((app/'catalog.json').read_bytes(),mtime=0)).decode()).replace('__PAYLOAD__',json.dumps(payload,separators=(',',':'))).replace('__JAVASCRIPT__',(app/'app.js').read_text())
p=app/'MyLeagueEditor.html';p.write_text(html)
(app/'embedded-payload-sha256.json').write_text(json.dumps({n:hashlib.sha256((r/n).read_bytes()).hexdigest()for n in names},indent=2)+'\n');print('Offline HTML bytes',p.stat().st_size)
