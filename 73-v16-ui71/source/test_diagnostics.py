from pathlib import Path
import tempfile,types,sys,json,marshal,zipfile,io,hashlib
P=Path('/workspace/ronaldo-work/73-ui71');root=Path(tempfile.mkdtemp(prefix='ui71-diagnostic-test-'));tools=root/'work/tools';tools.mkdir(parents=True)
m=types.ModuleType('mod_startup');m.__file__=str(tools/'mod_startup.py');exec(compile((P/'payload/work/tools/mod_startup.py').read_text(),m.__file__,'exec'),m.__dict__);sys.modules['mod_startup']=m
(tools/'select-team-status.json').write_text('{"state":"INSTALL_FAILED","error":"test prologue mismatch"}')
pr=types.ModuleType('_protected_runtime')
def inject(name,g):
 g['initialize']=lambda root,installed_version=None:{'ready':True,'version':installed_version}
 g['handle']=lambda path,body:body
pr.exec_into=inject;sys.modules['_protected_runtime']=pr
bridge=types.SimpleNamespace(install=lambda *a:None);sys.modules['_v25_bridge_73']=bridge
w=types.ModuleType('ui71_boot_test');sys.modules[w.__name__]=w;exec(compile((P/'embedded_gateway_wrapper.py').read_text(),'embedded_gateway.py','exec'),w.__dict__)
assert w.initialize(str(root),9)=={'ready':True,'version':9}
def fail(*a):raise ValueError('deliberate bootstrap failure')
bridge.install=fail
try:w.initialize(str(root),9);raise AssertionError('bootstrap falsely returned ready')
except RuntimeError as e:assert 'Runtime Diagnostics'in str(e)
report=json.loads((tools/'mod-last-error.json').read_text());assert report['stage']=='python-bootstrap'and 'deliberate bootstrap failure'in report['traceback']and report['select-team-status.json']['state']=='INSTALL_FAILED'
assert w.handle('/CMD_LOGIN',b'wire')==b'wire'
original_log=m.record_request
m.record_request=fail
assert w.handle('/CMD_LOGIN',b'wire-still-valid')==b'wire-still-valid'
m.record_request=original_log
w._v25_original_handle=fail
try:w.handle('/CMD_LOGIN?not-stored=123',b'private-body');raise AssertionError('request error swallowed')
except ValueError:pass
report=json.loads((tools/'mod-last-error.json').read_text());assert report['stage']=='gateway-request:/CMD_LOGIN'and 'private-body'not in json.dumps(report)and 'not-stored'not in json.dumps(report)
# No worker reinitialization/report update clears the persisted failure.
assert (tools/'mod-last-error.json').exists()
out={'passed':True,'checks':['successful original bootstrap result retained','bridge failure now reaches launcher instead of falsely returning ready','request success bytes unchanged; request exception re-raised','last failure persists with traceback and native diagnostic snapshots','request query and body excluded from report'],'device_tested':False};(P/'diagnostics-validation.json').write_text(json.dumps(out,indent=2));print('DIAGNOSTICS_PASS')
