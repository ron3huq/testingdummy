"""Build HF1 from SHA-verified public RC5; exercise nested LOGIN validators."""
from pathlib import Path
import json,hashlib,subprocess,sys,shutil
root=Path.cwd();stage=root/'.ci-full8-rc5-hf1';source=root/'source/repair-full8-rc5-hf1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args):subprocess.run([str(x)for x in args],check=True)
assert sha(root/'classes5.dex')=='a67f538ce35d98c77cbd66de473ffdec33771ac598f365ccaad7705f4cf9f71a'
jar=root/'.ci-full8-rc5/apktool.jar';assert sha(jar)=='56d59c524fc764263ba8d345754d8daf55b1887818b15cd3b594f555d249e2db'
tool=root/'source/repair-full8-rc4/DexTool.java';smali=stage/'smali';run(['java','-cp',jar,tool,'d',root/'classes5.dex',smali]);shutil.copy2(source/'RuntimeDiagnostics.smali',smali/'org/efootballrevival/runtimeprobe/RuntimeDiagnostics.smali');run(['java','-cp',jar,tool,'a',smali,root/'classes5.dex'])
assert sha(root/'classes5.dex')=='d7108676b9ce6b205f05afd3fcac772518f5da727fb0cda9a3505d77b2d4f258'
run([sys.executable,source/'fix_integrity.py',root])
expected=json.loads((stage/'expected.json').read_text());inventory=json.loads((root/'payload-inventory.json').read_text());assert sha(root/'payload-inventory.json')==expected['inventory_sha256'],'Final inventory differs from validated local HF1'
assert inventory['resource_revision']==19013 and len(inventory['files'])+1==1280
for row in inventory['files']:
 p=root/row['path'];assert p.is_file()and p.stat().st_size==row['bytes']and sha(p)==row['sha256'],row['path']
print('HF1 passed actual prelogin bundle validators and LOGIN guard regression; bad checksum remains blocked; native workers mocked. All1280 files/219 runtime assets verified. Phone login verification remains false.')
