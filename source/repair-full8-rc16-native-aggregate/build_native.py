"""Build a separate experimental ARM64 input adapter; no release mutation."""
import hashlib,json,subprocess,sys,os
from pathlib import Path
source=Path(__file__).parent;out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
obj=out/'ucl_rules.o';lib=out/'libucl_rules.so'
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR=str(out/'zig-global'),ZIG_LOCAL_CACHE_DIR=str(out/'zig-local'))
subprocess.run([sys.executable,'-m','ziglang','cc','-target','aarch64-freestanding','-c','-ffreestanding','-fno-stack-protector','-ffixed-x18','-fPIC','-fvisibility=hidden','-mno-outline-atomics','-O2','-g0',str(source/'ucl_rules.c'),'-o',str(obj)],check=True,env=env)
subprocess.run([sys.executable,'-m','ziglang','ld.lld','-shared','-z','max-page-size=16384',str(obj),'-o',str(lib)],check=True,env=env)
print(json.dumps(dict(experimental=True,installed=False,library=str(lib),sha256=hashlib.sha256(lib.read_bytes()).hexdigest()),indent=2))
