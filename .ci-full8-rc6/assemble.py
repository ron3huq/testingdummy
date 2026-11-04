"""Build RC6 after exact public RC5-HF1; only reviewed source and face assets.
The optional CI face inputs are not part of the shipped FULL inventory.
"""
from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil
root=Path.cwd();stage=root/'.ci-full8-rc6';source=root/'source/repair-full8-rc6';t=root/'assets/gateway-release/work/tools'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
spec=json.loads((stage/'expected.json').read_text())
assert sha(root/'classes5.dex')=='d7108676b9ce6b205f05afd3fcac772518f5da727fb0cda9a3505d77b2d4f258'
assert json.loads((root/'payload-inventory.json').read_text())['resource_revision']==19013
for p in(source/'overlays').rglob('*'):
 if p.is_file():dest=root/p.relative_to(source/'overlays');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'))
for name,out,flags in [('single_live','libsingle_player_live.so',[]),('transfer_final','libtransfer_final.so',['-Bsymbolic'])]:
 obj=stage/(name+'.o');run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',source/(name+'.c'),'-o',obj],env=env)
 run([sys.executable,'-m','ziglang','ld.lld','-shared',*flags,'-z','max-page-size=16384',obj,'-o',t/out],env=env);assert sha(t/out)==spec['native_sha256'][out],out
obj=stage/'editor_callbacks.o';stub=stage/'editor_callbacks.elf';run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c',source/'editor_callbacks.S','-o',obj],env=env)
run([sys.executable,'-m','ziglang','ld.lld','-Ttext=0x10c1000','--defsym=callbacks=0x10d0000','--defsym=original_apply_tail=0x2d020','--defsym=original_apply_ret=0x2d17c','--defsym=original_rating_tail=0x37190',obj,'-o',stub],env=env)
run([sys.executable,source/'patch_editor_callbacks.py',t/'libselect_team.so',stub,t/'libselect_team.so']);assert sha(t/'libselect_team.so')==spec['native_sha256']['libselect_team.so']
jar=root/'.ci-full8-rc5/apktool.jar';tool=root/'source/repair-full8-rc4/DexTool.java';smali=stage/'smali';run(['java','-cp',jar,tool,'d',root/'classes5.dex',smali]);dst=smali/'org/efootballrevival/runtimeprobe'
for p in dst.glob('SinglePlayerInMatch*.smali'):p.unlink()
for p in source.glob('*.smali'):shutil.copyfile(p,dst/p.name)
run(['java','-cp',jar,tool,'a',smali,root/'classes5.dex']);assert sha(root/'classes5.dex')==spec['dex_sha256']
inputs=root/'.ci-full8-rc6-input';face=stage/'face-input';face.mkdir(exist_ok=True)
for row in json.loads((inputs/'face-input.json').read_text())['files']:
 dest=face/row['name']
 with dest.open('wb')as f:
  for part in row['parts']:f.write((root/part).read_bytes())
 assert dest.stat().st_size==row['bytes']and sha(dest)==row['sha256'],row['name']
run([sys.executable,source/'clone_face.py',root,face,stage/'face-clone-validation.json'])
run([sys.executable,source/'verify_face_clone.py',root,face,root/'validation/full8-rc6-face-preservation.json'])
run([sys.executable,source/'finalize.py',root]);run([sys.executable,source/'check_payload.py',root])
assert sha(root/'payload-inventory.json')==spec['inventory_sha256'],'RC6 cumulative FULL differs from validated local files'
print('RC6 complete payload matches validated local inventory. Real-phone verification remains false.')
