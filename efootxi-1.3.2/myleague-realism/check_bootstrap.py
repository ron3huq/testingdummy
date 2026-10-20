import ast,hashlib,json
from pathlib import Path
r=Path(__file__).parent
old=(r/'gateway_runtime.previous.py').read_bytes();new=(r/'gateway_runtime.py').read_bytes()
assert len(old)==len(new)==2441
before=ast.parse(old);after=ast.parse(new)
assert len(after.body)==len(before.body)+1
assert ast.dump(ast.Module(body=after.body[:-1],type_ignores=[]))==ast.dump(before)
for name in ['gateway_runtime.py','myleague_realism.py']:compile((r/name).read_bytes(),name,'exec')
report={'status':'BOOTSTRAP_VALIDATED','previous_gateway_sha256':hashlib.sha256(old).hexdigest(),'new_gateway_sha256':hashlib.sha256(new).hexdigest(),'gateway_bytes':2441,'native_select_team_loader_unchanged':True,'gateway_url_functions_unchanged':True,'additional_statement':'guarded realism module install','new_python_sources_compile':True}
(r/'bootstrap-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
