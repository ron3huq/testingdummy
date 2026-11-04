"""Build final game payload from verified public baseline and transparent source.
No private DB/save input and no opaque ELF/DEX upload. Workflow is read-only.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,os
root=Path.cwd();stage=root/'.ci-full8-rc4';doc=json.loads((stage/'READY.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
for row in doc['files']:
 p=root/row['path'];assert p.is_relative_to(root);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb')as f:
  for part in row['parts']:f.write((root/part).read_bytes())
 assert p.stat().st_size==row['size']and sha(p)==row['sha256'],row['path']
recipe=json.loads((root/'source/repair-full8-rc4/build_recipe.json').read_text())
for item in recipe['public_patches']:
 p=root/item['path'];assert sha(p)==item['input_public_sha256'],'Public baseline mismatch: '+item['path'];b=bytearray(p.read_bytes())
 for patch in item['patches']:
  off=patch['offset'];before=bytes.fromhex(patch['before']);after=bytes.fromhex(patch['after']);assert len(before)==len(after)and b[off:off+len(before)]==before;b[off:off+len(before)]=after
 p.write_bytes(b);assert sha(p)==item['output_sha256']
print('Verified small native patches applied to exact public RC3 inputs')
item=recipe['native_compile'];env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'))
obj=stage/'single_live.o';run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',root/item['source'],'-o',obj],env=env)
run([sys.executable,'-m','ziglang','ld.lld','-shared','-z','max-page-size=16384',obj,'-o',root/item['output']],env=env);assert sha(root/item['output'])==item['sha256'],'Compiled control module differs from validated source build'
print('Native Single Player ELF compiled from source and SHA256 matched')
item=recipe['dex'];target=root/'classes5.dex';assert sha(target)==item['input_public_sha256'];jar=stage/'apktool.jar'
run(['curl','--fail','--location','--retry','3','--max-time','180',item['apktool_url'],'-o',jar]);assert sha(jar)==item['apktool_sha256'],'Untrusted tool JAR'
smali=stage/'dex-smali';run(['java','-cp',jar,root/item['tool'],'d',target,smali])
for name in item['overlays']:shutil.copy2(root/'source/repair-full8-rc4'/(name+'.smali'),smali/'org/efootballrevival/runtimeprobe'/(name+'.smali'))
run(['java','-cp',jar,root/item['tool'],'a',smali,target]);assert sha(target)==item['output_sha256'],'DEX source rebuild mismatch'
print('DEX rebuilt from public baseline and two transparent smali UI classes; SHA256 matched')
item=recipe['face'];run([sys.executable,root/item['script'],root,root/item['spec'],root/item['weights']])
print('Ronaldo final facial controls built from validated V8 assets and explicit vertex weights')
inventory=json.loads((root/'payload-inventory.json').read_text());assert inventory['resource_revision']==doc['resource_revision']==19011
for row in inventory['files']:
 p=root/row['path'];assert p.is_file()and p.stat().st_size==row['bytes'];assert sha(p)==row['sha256'],row['path']
g=root/'assets/gateway-release';runtime=json.loads((g/'ui6-runtime-manifest.json').read_text());assert len(runtime['files'])==doc['runtime_assets']==204
for row in runtime['files']:
 assert '__pycache__'not in row['path'];assert sha(g/row['path'])==row['sha256']
shutil.rmtree(stage)
print('FULL8 RC4 revision19011 complete inventory and 204 runtime hashes verified. Phone verification remains false.')
