"""Repair the known public RC5 nested checksum regression, preserving all gates.
Input is the exact SHA-verified RC5 FULL, never an installed user directory.
"""
from pathlib import Path
import json,hashlib,sys

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fix(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';baseline=json.loads((root/'payload-inventory.json').read_text());assert baseline['resource_revision']==19012
 p=t/'private_bundles.json';assert sha(p)=='6b1e4e13e6bbb01142dd9d1be3b7a6e7bc992f5c6b1e434e45e1d4ce2953a474','Unexpected RC5 private manifest'
 meta=json.loads((t/'noodle_bundle.json').read_text());assert meta['appearance_files']['private_bundles.json']=='6efedc72a2b632bc404cc33258d898f5dba2e5f1be645ac2b4af7d035de866ec'
 for name,pin in meta['appearance_files'].items():
  if name!='private_bundles.json':assert sha(t/name)==pin,name
 d=json.loads(p.read_text());assert d['resource_revision']==19012;d['resource_revision']=19013;p.write_text(json.dumps(d,indent=2))
 # Dependency first, then its enclosing pin. Do not bypass the validator.
 meta['appearance_files']['private_bundles.json']=sha(p);(t/'noodle_bundle.json').write_text(json.dumps(meta,indent=2))
 for n,key in [('ui6-runtime-manifest.json','version'),('release-manifest.json','release_id')]:
  p=g/n;d=json.loads(p.read_text());d[key]='V19.1-FULL8-RC5-HF1-login-integrity';p.write_text(json.dumps(d,indent=2))
 p=root/'README-VI.md';s=p.read_text().replace('# FULL-8 RC5 ·','# FULL-8 RC5 HF1 ·',1).replace('Resource revision19012.','Resource revision19013.');s=s.replace('\n\nResource revision', '\n\nHF1 sửa lỗi C_NAJM_0009: checksum private_bundles.json trong noodle_bundle.json bị cũ sau khi dựng lại tài nguyên RV8F. Cập nhật pin lồng nhau theo đúng thứ tự, giữ nguyên chặn LOGIN khi runtime chưa hợp lệ. Không sửa save, CPK đăng nhập, hook Single Player, mesh/texture, Transfer hay accessories. Kiểm tra gọi trực tiếp validator trước LOGIN và kiểm tra cố ý làm sai checksum vẫn bị từ chối. Chưa xác nhận trên điện thoại.\n\nResource revision',1);p.write_text(s)
 helper=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';ns={};exec(compile(helper.read_text(),str(helper),'exec'),ns);ns['update'](g);assert ns['check'](g)==219
 # Must exercise the exact pre-login validator, not merely Save/build success.
 sys.path.insert(0,str(Path(__file__).resolve().parent));from check_startup_integrity import verify
 result=verify(root);from verify_login_gate import run;result.update(run(root));(root/'validation/full8-rc5-hf1-startup-integrity.json').write_text(json.dumps(result,indent=2))
 files=[]
 allowed={row['path']for row in baseline['files']}|{p.relative_to(root).as_posix()for p in(root/'source/repair-full8-rc5-hf1').glob('*')if p.is_file()}|{'validation/full8-rc5-hf1-startup-integrity.json'}
 for name in sorted(allowed):
  p=root/name;assert p.is_file(),name
  assert '__pycache__'not in p.parts and p.suffix.lower()not in{'.db','.sqlite','.sqlite3','.log','.rar','.zip','.apk','.mp4'},p
  files.append(dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
 (root/'payload-inventory.json').write_text(json.dumps(dict(version='V19.1-FULL8-RC5-HF1',resource_revision=19013,phone_verified=False,files=files),indent=2));print(json.dumps(result,indent=2));print('Final HF1 inventory',len(files)+1)
if __name__=='__main__':fix(sys.argv[1])
