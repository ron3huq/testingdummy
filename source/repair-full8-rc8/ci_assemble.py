"""Rebuild RC8 from verified public RC7 and transparent source, never personal data."""
from pathlib import Path
import hashlib,json,subprocess,sys,os,shutil
root=Path.cwd();stage=root/'.ci-full8-rc8';src=root/'source/repair-full8-rc8';t=root/'assets/gateway-release/work/tools';spec=json.loads((stage/'expected.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
assert sha(root/'payload-inventory.json')=='4acc1d023a92a7e75874aa7684e97e21e49193f3cd166911fc04eacd78e95ff8'
assert sha(root/'classes5.dex')=='687f574b70c37888c274bd8d9b1cf193dc3eff33d4556eb8db34d8b124a53c51'
for p in(src/'overlays').rglob('*'):
 if p.is_file():q=root/p.relative_to(src/'overlays');q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'))
obj=stage/'single_live.o';run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',src/'single_live.c','-o',obj],env=env);run([sys.executable,'-m','ziglang','ld.lld','-shared','-z','max-page-size=16384',obj,'-o',t/'libsingle_player_live.so'],env=env)
obj=stage/'profile.o';stub=stage/'profile.elf';run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c',src/'profile.S','-o',obj],env=env);run([sys.executable,'-m','ziglang','ld.lld','-T',src/'profile.ld',obj,'-o',stub],env=env)
run([sys.executable,src/'patch_profile.py',t/'libnoodle_hair.so',stub,t/'libnoodle_hair.so'])
for name,wanted in spec['native_sha256'].items():assert sha(t/name)==wanted,name
jar=root/'.ci-full8-rc5/apktool.jar';tool=root/'source/repair-full8-rc4/DexTool.java';smali=stage/'smali';run(['java','-cp',jar,tool,'d',root/'classes5.dex',smali]);
for p in src.glob('*.smali'):shutil.copyfile(p,smali/'org/efootballrevival/runtimeprobe'/p.name)
run(['java','-cp',jar,tool,'a',smali,root/'classes5.dex']);assert sha(root/'classes5.dex')==spec['dex_sha256']
run([sys.executable,src/'build_face.py',root,root/'source/repair-full8-rc7/mesh-ranges.json',src/'low-ranges.json',root/'validation/full8-rc8-face-local-corrections.json'])
run([sys.executable,src/'finalize.py',root]);run([sys.executable,src/'check_payload.py',root]);assert sha(root/'payload-inventory.json')==spec['inventory_sha256'],'RC8 reconstruction differs from local inventory'
print('RC8 cumulative FULL source reconstruction exactly matches validated local inventory. Phone verification remains false.')
