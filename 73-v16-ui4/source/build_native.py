"""Compile the reviewed C sources without regenerating their policy tables.
Requires Python with ziglang0.13.0. Supply an output directory as argv1.
"""
from pathlib import Path
import subprocess,sys
source=Path(__file__).resolve().parent
out=Path(sys.argv[1]if len(sys.argv)>1 else './ui4-native-build').resolve();out.mkdir(parents=True,exist_ok=True)
for name in ['select_team','noodle_hair']:
 obj=out/(name+'.o');lib=out/('lib'+name+'.so')
 subprocess.run([sys.executable,'-m','ziglang','cc','-target','aarch64-linux-musl','-mno-outline-atomics','-c','-fPIC','-O2','-fvisibility=hidden','-fno-stack-protector','-fno-builtin',str(source/(name+'.c')),'-o',str(obj)],check=True)
 subprocess.run([sys.executable,'-m','ziglang','build-lib',str(obj),'-target','aarch64-linux-musl','-dynamic','-Bsymbolic','-fno-compiler-rt','-femit-bin='+str(lib)],check=True)
 print(lib)
