"""Apply reviewed RC5 changes after the exact public RC4 source build.
No private DB/save input. No repository writes and no opaque native/DEX upload.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,os,shutil
root=Path.cwd();stage=root/'.ci-full8-rc5';doc=json.loads((stage/'READY.json').read_text());recipe=doc['recipe'];G=root/'assets/gateway-release'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
assert sha(root/'classes5.dex')==recipe['dex_input_sha256'],'RC4 input DEX mismatch'
assert sha(G/'release-manifest.json')=='3a770345db0ce20aea50a6b777ff89293369fab64efc9c0df6bf539c351ac1ad','Public RC4 manifest provenance mismatch'
public_release=json.loads((G/'release-manifest.json').read_text())
p=G/'work/tools/libnoodle_hair.so';assert sha(p)==recipe['noodle_input_sha256'];b=p.read_bytes();assert b.count(b'RV8E\0')==1;p.write_bytes(b.replace(b'RV8E\0',b'RV8F\0'));assert sha(p)==recipe['noodle_output_sha256']
for row in doc['files']:
 p=root/row['path'];assert p.is_relative_to(root);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb')as f:
  for part in row['parts']:f.write((root/part).read_bytes())
 assert p.stat().st_size==row['size']and sha(p)==row['sha256'],row['path']
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'));obj=stage/'single_live.o'
run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',root/recipe['native_source'],'-o',obj],env=env)
run([sys.executable,'-m','ziglang','ld.lld','-shared','-z','max-page-size=16384',obj,'-o',G/'work/tools/libsingle_player_live.so'],env=env);assert sha(G/'work/tools/libsingle_player_live.so')==recipe['native_sha256']
jar=stage/'apktool.jar';run(['curl','--fail','--location','--retry','3','--max-time','180','https://github.com/iBotPeaches/Apktool/releases/download/v2.11.1/apktool_2.11.1.jar','-o',jar]);assert sha(jar)=='56d59c524fc764263ba8d345754d8daf55b1887818b15cd3b594f555d249e2db'
smali=stage/'smali';src=root/'source/repair-full8-rc5';run(['java','-cp',jar,src/'DexTool.java','d',root/'classes5.dex',smali])
for name in recipe['overlays']:shutil.copy2(src/(name+'.smali'),smali/'org/efootballrevival/runtimeprobe'/(name+'.smali'))
run(['java','-cp',jar,src/'DexTool.java','a',smali,root/'classes5.dex']);assert sha(root/'classes5.dex')==recipe['dex_output_sha256']
runtime_doc=json.loads((G/'ui6-runtime-manifest.json').read_text());public_release['release_id']=runtime_doc['version'];rows={r['path']:r for r in public_release['files']};rows.update({r['path']:r for r in runtime_doc['files']});public_release['files']=list(rows.values());(G/'release-manifest.json').write_text(json.dumps(public_release,indent=2))
run([sys.executable,root/'source/repair-full8-rc5/face_from_geometry.py',root,root/'source/repair-full8-rc5/face_geometry.json'])
inventory=json.loads((root/'payload-inventory.json').read_text());assert inventory['resource_revision']==doc['resource_revision']==19012
for row in inventory['files']:
 p=root/row['path'];assert p.is_file()and p.stat().st_size==row['bytes']and sha(p)==row['sha256'],row['path']
runtime=json.loads((G/'ui6-runtime-manifest.json').read_text());assert len(runtime['files'])==doc['runtime_assets']==219
for row in runtime['files']:
 assert '__pycache__'not in row['path'];assert sha(G/row['path'])==row['sha256']
print('RC5 FULL inventory and all219 runtime assets verified; source-built native/DEX hashes matched. Phone verification remains false.')
