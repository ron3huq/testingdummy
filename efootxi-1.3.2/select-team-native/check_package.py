"""Host package guards; does not claim Android loading or rendering success."""
import ast, hashlib, importlib.util, json
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('runtime',root/'select_team_runtime.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert hashlib.sha256((root/'libselect_team.so').read_bytes()).hexdigest()==m.HOOK_SHA
for source in [0x737e05c,0x7012345678]:
 for delta in [-(1<<27),-4,0,4,(1<<27)-4]:
  word=m.branch(source,source+delta);n=word&0x3ffffff
  if n&(1<<25):n-=1<<26
  assert source+4*n==source+delta
 for delta in [1,-(1<<27)-4,1<<27]:
  try:m.branch(source,source+delta)
  except ValueError:pass
  else:raise AssertionError('invalid branch accepted')
original=(root/'gateway_runtime.original.py').read_bytes()
patched=(root/'gateway_runtime.py').read_bytes()
assert len(original)==len(patched)
def strip_docs(tree):
 for node in ast.walk(tree):
  if hasattr(node,'body') and isinstance(node.body,list) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):node.body.pop(0)
 return tree
original_ast=strip_docs(ast.parse(original));patched_ast=ast.parse(patched)
assert isinstance(patched_ast.body[-1],ast.Try)
patched_ast.body.pop()
assert ast.dump(original_ast)==ast.dump(patched_ast)
for p in root.glob('*.py'):compile(p.read_bytes(),str(p),'exec')
report={'status':'HOST_GUARDS_PASS','device_tested':False,'checks':['hook binary SHA matches loader','branch encoding positive/negative and boundaries','invalid branch rejected','gateway runtime functions unchanged apart from docstrings','gateway byte length preserved for support-file size guard','Python sources compile']}
(root/'package-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
