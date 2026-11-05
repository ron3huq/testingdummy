"""Run after the public reconstruction chain RC4..RC7, never after RC8."""
from pathlib import Path
import subprocess,sys,os,shutil
root=Path.cwd();src=root/'source/repair-full8-rc10-face-detail';stage=root/'.ci-face-detail';stage.mkdir(exist_ok=True);t=root/'assets/gateway-release/work/tools'
def run(args,**kw):subprocess.run([str(x)for x in args],check=True,**kw)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(stage/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(stage/'zig-local'))
shutil.copyfile(t/'libnoodle_hair.so',stage/'rc7-noodle.so')
run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c',src/'profile.S','-o',stage/'profile.o'],env=env);run([sys.executable,'-m','ziglang','ld.lld','-T',src/'profile.ld',stage/'profile.o','-o',stage/'profile.elf'],env=env)
run([sys.executable,src/'patch_profile.py',stage/'rc7-noodle.so',stage/'profile.elf',stage/'libnoodle_hair.so']);shutil.copyfile(stage/'libnoodle_hair.so',stage/'face-noodle.so')
run([sys.executable,src/'build_face.py',root,root/'source/repair-full8-rc7/mesh-ranges.json',root/'source/repair-full8-rc9-ucl/low-ranges.json',root/'validation/full8-rc10-face.json'])
for script,output in [('validate_face.py','full8-rc10-face-readback.json'),('test_face_profile.py','full8-rc10-face-profile.json')]:
 with (root/'validation'/output).open('w')as f:run([sys.executable,src/script,*([root]if script=='validate_face.py'else[])],stdout=f,env=dict(os.environ,FACE_TEST_BUILD=str(stage)))
run([sys.executable,root/'source/repair-full8-rc9-ucl/test_ucl.py'])
run([sys.executable,src/'verify_host_motion.py',root])
run([sys.executable,src/'finalize_face_candidate.py',root]);run([sys.executable,src/'check_candidate.py',root])
