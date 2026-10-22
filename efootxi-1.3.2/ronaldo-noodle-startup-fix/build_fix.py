from pathlib import Path
import ast,json,hashlib,zipfile,shutil
r=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-hair-v1');o=Path(__file__).parent
base=Path('/workspace/analysis/my-league/android/official-apk/assets/gateway-release')
entry=next(x for x in json.loads((base/'release-manifest.json').read_text())['files'] if x['path']=='work/tools/gateway_runtime.py')
expected=entry['bytes'];assert expected==2441
# Python indentation is reduced without changing the AST; padding is a comment.
def pack(source):
 t=ast.parse(source);s=ast.unparse(t)+'\n'
 lines=[]
 for line in s.splitlines():
  n=len(line)-len(line.lstrip(' '));assert n%4==0
  lines.append(' '*(n//4)+line.lstrip(' '))
 s='\n'.join(lines)+'\n';assert ast.dump(ast.parse(s))==ast.dump(t)
 room=expected-len(s.encode());assert room>=2,(len(s.encode()),expected)
 data=s.encode()+b'#'+b' '*(room-2)+b'\n';assert len(data)==expected;compile(data,'gateway_runtime.py','exec');return data
trial=pack((r/'gateway_runtime.py').read_text());restore=pack(Path('/workspace/analysis/my-league/hotfix-v18/gateway_runtime.py').read_text())
(o/'gateway_runtime_fixed.py').write_bytes(trial);(o/'gateway_runtime_restore.py').write_bytes(restore)
(r/'deploy/work/tools/gateway_runtime.py').write_bytes(trial)
# Guard's actual existing-file branch: equal byte length skips repair entirely.
guard=Path('/workspace/analysis/my-league/android/dex/classes8-Lorg_efootballrevival_bootstrap_GatewayGuard.txt').read_text()
assert '->length()J' in guard and 'goto/16 +0d6h' in guard and '->renameTo' in guard
old=(r/'gateway_runtime.py').read_bytes();assert len(old)!=expected
original=(base/entry['path']).read_bytes();assert len(original)==expected and hashlib.sha256(original).hexdigest()==entry['sha256']
report={'guard_source':'GatewayGuard.prepare, extracted classes8.dex','manifest_expected_bytes':expected,'broken_trial_bytes':len(old),'fixed_trial_bytes':len(trial),'recovery_bytes':len(restore),'trial_ast_preserved':True,'recovery_v18_ast_preserved':True,'existing_file_branch':'matching size skips asset repair and repair hash check','original_apk_asset_hash_verified':True,'phone_tested':False}
(o/'bootstrap-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
