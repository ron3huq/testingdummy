"""Construct packaged runtime manifests without importing payload modules.
Run after staging/cleanup. Validation must run again on the final archive.
Legacy release entries from the base APK are retained; transient cache is not.
"""
import argparse,hashlib,json
from pathlib import Path

def forbidden(path):
 return '__pycache__'in path.parts or path.name.endswith(('.tmp','.installing','-status.json'))

def rows(root):
 result=[]
 for f in sorted(root.rglob('*')):
  if not f.is_file()or forbidden(f.relative_to(root))or f.name in {'release-manifest.json','ui6-runtime-manifest.json'}:continue
  if f.suffix.lower()in{'.db','.sqlite','.sqlite3','.log','.zip','.rar','.apk'}:raise ValueError('Unexpected private/research file: '+str(f))
  b=f.read_bytes();result.append(dict(path=f.relative_to(root).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 return result

def update(root):
 real=rows(root);runtime=root/'ui6-runtime-manifest.json';doc=json.loads(runtime.read_text());doc['files']=real;runtime.write_text(json.dumps(doc,indent=2))
 p=root/'release-manifest.json';doc=json.loads(p.read_text());old={r['path']:r for r in doc['files']if not forbidden(Path(r['path']))};old.update({r['path']:r for r in real});doc['files']=list(old.values());p.write_text(json.dumps(doc,indent=2))

def check(root):
 expected=rows(root);doc=json.loads((root/'ui6-runtime-manifest.json').read_text());actual={r['path']:r for r in doc['files']};assert len(actual)==len(doc['files']),'Duplicate path'
 assert actual=={r['path']:r for r in expected},'Runtime manifest does not match staged assets'
 for filename in ['release-manifest.json','ui6-runtime-manifest.json']:
  doc=json.loads((root/filename).read_text());assert all(not forbidden(Path(r['path']))for r in doc['files']),'Transient cache declared'
 return len(actual)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--write',action='store_true');args=p.parse_args()
 if args.write:update(args.root)
 print('Verified runtime assets:',check(args.root))
