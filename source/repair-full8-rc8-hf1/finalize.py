from pathlib import Path
import json,hashlib,sys,ast
VERSION='V19.1-FULL8-RC8-HF1-hook-arena-4k'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finalize(root):
 root=Path(root);g=root/'assets/gateway-release';t=g/'work/tools';s=root/'source/repair-full8-rc8-hf1';v=root/'validation';prior=json.loads((root/'payload-inventory.json').read_text());assert prior['resource_revision']==19017
 p=t/'private_bundles.json';d=json.loads(p.read_text());d['resource_revision']=19019;p.write_text(json.dumps(d,indent=2))
 p=t/'full4_trace.py';p.write_text(p.read_text().replace('FULL8-RC8','FULL8-RC8-HF1'))
 p=t/'noodle_bundle.json';d=json.loads(p.read_text());d.update(version=VERSION,asset_revision=19019);d['appearance_files']={n:sha(t/n)for n in d['appearance_files']};d['appearance_overlay_sha256']=sha(t/'myleague_editor_runtime.py');p.write_text(json.dumps(d,indent=2))
 for name,key in [('release-manifest.json','release_id'),('ui6-runtime-manifest.json','version')]:
  p=g/name;d=json.loads(p.read_text());d[key]=VERSION;p.write_text(json.dumps(d,indent=2))
 (root/'README-RC8-HF1-VI.md').write_text('FULL8 RC8 HF1, revision19019. Cumulative payload assets/ + classes5.dex. Phone diagnostics showed LOGIN blocked by No shared hook page in branch range:0hints, bound_targets0; not a missing-resource or external-network diagnosis. Compact63 arena slots from88 to64bytes and trampoline offset32 to24, fitting all slots in one4KiB page instead of8KiB. Cached lookup uses the shared offset. Preserve native libraries, all faces, stats, Single Player behavior, accessories and LOGIN/integrity guard. Host reproduction validates4KiB fragmentation and ARM64 dispatch/conditional trampoline paths. This does not prove actual on-phone login. No personal diagnostics/save/database or research archives included. Keep existing app data.\n')
 ns={};q=root/'source/repair-full8-rc2-hf1/build_runtime_manifests.py';exec(compile(q.read_text(),str(q),'exec'),ns);ns['update'](g);ns['check'](g)
 sys.path.insert(0,str(root/'source/repair-full8-rc5-hf1'));from check_startup_integrity import verify;report=verify(root);from verify_login_gate import run;report.update(run(root));report['revision']=19019;(v/'full8-rc8-hf1-startup.json').write_text(json.dumps(report,indent=2))
 for q in t.glob('*.py'):ast.parse(q.read_text())
 names={x['path']for x in prior['files']}|{q.relative_to(root).as_posix()for q in s.rglob('*')if q.is_file()}|{q.relative_to(root).as_posix()for q in v.glob('full8-rc8-hf1-*.json')}|{'README-RC8-HF1-VI.md'}
 rows=[]
 for name in sorted(names):
  q=root/name;assert q.is_file()and '__pycache__'not in q.parts and not q.name.endswith('.private.json')and q.suffix.lower()not in{'.zip','.rar','.apk','.log','.db','.sqlite','.sqlite3','.mp4'},name;rows.append({'path':name,'bytes':q.stat().st_size,'sha256':sha(q)})
 (root/'payload-inventory.json').write_text(json.dumps({'version':VERSION,'resource_revision':19019,'phone_verified':False,'files':rows},indent=2));print(json.dumps({'files':len(rows)+1,'startup':report}))
if __name__=='__main__':finalize(sys.argv[1])
