"""Same hooks + data, swap only the four failing private head profiles to ND06.
This is a temporary phone diagnostic, never a finished four-face correction.
"""
from pathlib import Path
import subprocess,shutil,json,os
r=Path(__file__).resolve().parent;dest=r/'comparison';dest.mkdir(exist_ok=True)
for name in ['noodle_hair.c','validate_native.py','validate_install.py','noodle_hair.py']:shutil.copyfile(r/name,dest/name)
validation=(dest/'validate_native.py').read_text()
validation=validation.replace("   assert all('NF01' not in e[1] for e in es if e[0] in ('mesh','path'))","   assert all('ORIGINAL_PROFILE_2017' not in e[1] for e in es if e[0] in ('mesh','path'))")
for key in ['NF01','NF27','NFJR','NDHD']:validation=validation.replace(key,'ND06')
validation=validation.replace('ORIGINAL_PROFILE_2017','NF01')
(dest/'validate_native.py').write_text(validation)
env=dict(os.environ,ZIG_GLOBAL_CACHE_DIR='/workspace/ronaldo-work/zig-global',ZIG_LOCAL_CACHE_DIR='/workspace/ronaldo-work/zig-local')
subprocess.run(['python','-m','ziglang','cc','-target','aarch64-linux-musl','-mno-outline-atomics','-DFOUR_FACE_COMPARISON=1','-c','-fPIC','-O2','-fvisibility=hidden','-fno-stack-protector','-fno-builtin','-o','noodle_hair.o','noodle_hair.c'],cwd=dest,env=env,check=True)
subprocess.run(['python','-m','ziglang','build-lib','noodle_hair.o','-target','aarch64-linux-musl','-dynamic','-Bsymbolic','-fno-compiler-rt','-femit-bin=libnoodle_hair.so'],cwd=dest,env=env,check=True)
subprocess.run(['python','validate_native.py'],cwd=dest,check=True)
report=json.loads((dest/'native-validation.json').read_text());report['diagnostic_only']=True;report['four_failing_cards_use']='known working ND06 head, materials and textures already present in v16 container';report['renderer_verified']=False
(r.parent/'comparison-native-validation.json').write_text(json.dumps(report,indent=2))
