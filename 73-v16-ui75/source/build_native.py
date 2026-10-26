from pathlib import Path
import os,subprocess,sys
p=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(out/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(out/'zig-local'))
subprocess.run([sys.executable,'-m','ziglang','cc','-target','aarch64-linux-musl','-mno-outline-atomics','-c','-fPIC','-O2','-fvisibility=hidden','-fno-stack-protector','-fno-builtin',str(p/'select_team.c'),'-o',str(out/'select_team.o')],env=env,check=True)
subprocess.run([sys.executable,'-m','ziglang','build-lib',str(out/'select_team.o'),'-target','aarch64-linux-musl','-dynamic','-Bsymbolic','-fno-compiler-rt','-femit-bin='+str(out/'libselect_team.so')],env=env,check=True)
