"""RC7: source build after exact SHA-verified RC6; no opaque new asset uploads."""
from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil
root=Path.cwd();stage=root/'.ci-full8-rc7';src=root/'source/repair-full8-rc7';t=root/'assets/gateway-release/work/tools';spec=json.loads((stage/'expected.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
assert sha(root/'classes5.dex')=='4b6989711dc7b27fab5b399491542f5d9de0d50bae05e863407891609889221e'
assert sha(root/'payload-inventory.json')=='f22cdfcb67882ce1df71f9cac35de4593076b945bb5a8020745e96a47e94a819'
for p in(src/'overlays').rglob('*'):
 if p.is_file():q=root/p.relative_to(src/'overlays');q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'))
for name,output,extra in [('single_live','libsingle_player_live.so',[]),('transfer_final','libtransfer_final.so',['-Bsymbolic'])]:
 obj=stage/(name+'.o');run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',src/(name+'.c'),'-o',obj],env=env);run([sys.executable,'-m','ziglang','ld.lld','-shared',*extra,'-z','max-page-size=16384',obj,'-o',t/output],env=env);assert sha(t/output)==spec['native_sha256'][output]
jar=root/'.ci-full8-rc5/apktool.jar';tool=root/'source/repair-full8-rc4/DexTool.java';smali=stage/'smali';run(['java','-cp',jar,tool,'d',root/'classes5.dex',smali]);dst=smali/'org/efootballrevival/runtimeprobe'
for p in dst.glob('SinglePlayerInMatch*.smali'):p.unlink()
for p in src.glob('*.smali'):shutil.copyfile(p,dst/p.name)
run(['java','-cp',jar,tool,'a',smali,root/'classes5.dex']);assert sha(root/'classes5.dex')==spec['dex_sha256']
run([sys.executable,src/'patch_face.py',root,src/'mesh-ranges.json',root/'validation/full8-rc7-face-local-corrections.json'])
shutil.copyfile(src/'RESEARCH-UCL-V23.1.md',root/'RESEARCH-UCL-V23.1.md')
run([sys.executable,src/'finalize.py',root]);run([sys.executable,src/'check_payload.py',root]);assert sha(root/'payload-inventory.json')==spec['inventory_sha256'],'RC7 FULL differs from validated local inventory'
print('RC7 FULL source reconstruction matches local inventory; phone verification remains false.')
