from pathlib import Path
import shutil,subprocess,os,re,json,hashlib,sys
P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');R=P/'android-orc-v1';S=P/'android-hulk-only';T=P/'android-ronaldo-v2-final';card='53878485695166';version='orc-supplied-sculpt-v1'
for name in ['noodle_hair.c','noodle_hair.py','build_native.sh','validate_native.py']:
 s=(S/name).read_text()
 if name=='noodle_hair.c':s=s.replace('#define VENOM 106754901843130UL\n','')
 if name=='noodle_hair.py':s=s.replace("{'hulk':'53878485695166'}", "{'orc':'"+card+"'}").replace('hulk-only-v3',version).replace("version['version']+=31", "version['version']+=35")
 (R/name).write_text(s)
for name in ['validate_install.py','validate_runtime.py']:
 s=(T/name).read_text().replace('ronaldo-v2-hair2017-eyes-dark-v1',version).replace("+34", "+35");(R/name).write_text(s)
env=os.environ.copy();env.update(ZIG_GLOBAL_CACHE_DIR='/workspace/.cache/zig-global',ZIG_LOCAL_CACHE_DIR='/workspace/.cache/zig-local');env['PATH']='/workspace/.venvs/testingdummy/bin:'+env['PATH'];subprocess.run(['sh',str(R/'build_native.sh')],env=env,check=True)
print('ORC_NATIVE_COMPILED')
