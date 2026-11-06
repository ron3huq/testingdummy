"""Headless Chromium + actual launcher scripts; Android host is a test fixture."""
from pathlib import Path
import sys,threading,subprocess,json,sqlite3,types
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import unquote,urlsplit
root=Path(sys.argv[1]).resolve();stage=Path(sys.argv[2]).resolve();source=Path(__file__).parent;sys.path.insert(0,str(root/'source/repair-full8-rc9-ucl/runtime'))
from ucl_lp_controller import Controller
conn=sqlite3.connect(':memory:',check_same_thread=False);conn.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)');conn.execute('INSERT INTO meta VALUES(?,?)',('my_league_state_v1','normal-sentinel'));conn.commit();lock=threading.Lock();bridge=types.SimpleNamespace(aggregate_setup=lambda *a:None);controller=Controller(conn,lambda:bridge)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  with lock:
   try:
    if self.path=='/__test__/ready':bridge.aggregate_setup=(lambda *a:None)if request['ready']else None;reply={}
    elif self.path=='/api/ucl':reply=controller.manage(request)
    else:raise ValueError('unknown endpoint')
   except Exception as e:reply=dict(error=str(e))
  data=json.dumps(reply,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(data)
 def do_GET(self):
  relative=unquote(urlsplit(self.path).path).lstrip('/');parts=Path(relative).parts
  if'..'in parts:self.send_error(400);return
  p=stage/relative
  if not p.is_file():p=root/relative
  if not p.is_file():self.send_error(404);return
  mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.svg':'image/svg+xml'}.get(p.suffix,'application/octet-stream');self.send_response(200);self.send_header('Content-Type',mime);self.end_headers();self.wfile.write(p.read_bytes())
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 result=subprocess.run(['node',str(source/'test_ui.cjs'),'http://127.0.0.1:'+str(server.server_port),str(stage)],capture_output=True,text=True,timeout=90);print(result.stdout,end='');print(result.stderr,end='',file=sys.stderr);assert result.returncode==0;assert conn.execute('SELECT value FROM meta WHERE key=?',('my_league_state_v1',)).fetchone()[0]=='normal-sentinel'
finally:server.shutdown();conn.close()
