"""Prepare public references + user 2006 ZIP for the audited build scripts.
Downloads about 4 GB on an empty cache. Reuses verified downloads/extractions.
Never operates on the installed game or requires files from a phone.
"""
from pathlib import Path
import argparse,hashlib,json,urllib.request,zipfile,subprocess,shutil,zlib
P=Path(__file__).resolve().parent;OUT=P.parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=Path('/workspace/ronaldo-work'));ap.add_argument('--input-2006',required=True,type=Path);args=ap.parse_args();R=args.work.resolve();R.mkdir(parents=True,exist_ok=True)
I=json.loads((OUT/'input-inventory.json').read_text())
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def fetch(name,url,path,local=None):
 expected=I['files'][name]['sha256']
 if path.exists():assert digest(path)==expected,'Existing cache hash mismatch: '+str(path);return
 if local is not None and local.exists():shutil.copyfile(local,path)
 else:
  temp=path.with_suffix(path.suffix+'.partial')
  with urllib.request.urlopen(url,timeout=120) as src,temp.open('wb') as dst:shutil.copyfileobj(src,dst)
  assert digest(temp)==expected,'Download hash mismatch';temp.rename(path)
 assert digest(path)==expected

def extract(path,dest,predicate=lambda n:True):
 with zipfile.ZipFile(path) as z:
  for info in z.infolist():
   if not predicate(info.filename):continue
   target=(dest/info.filename).resolve();assert target.is_relative_to(dest.resolve()),'Unsafe archive path'
   if info.is_dir():target.mkdir(parents=True,exist_ok=True);continue
   if target.exists():
    assert target.stat().st_size==info.file_size and zlib.crc32(target.read_bytes())==info.CRC,'Existing extracted file changed: '+str(target)
   else:
    target.parent.mkdir(parents=True,exist_ok=True)
    with z.open(info) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)

def run(*cmd,**kwargs):return subprocess.run(cmd,check=True,**kwargs)
def clone(url,path,commit):
 if not path.exists():run('git','clone',url,str(path))
 actual=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
 if actual!=commit:
  assert not subprocess.check_output(['git','-C',str(path),'status','--porcelain']),'Modified dependency checkout'
  run('git','-C',str(path),'fetch','origin',commit);run('git','-C',str(path),'checkout','--detach',commit)
 assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()==commit

fetch('apk','https://github.com/maxlzyver/efootxi/releases/download/v1.3.2/efootxi-1.3.2.apk',R/'efootxi-1.3.2.apk')
for n in ['02','03']:fetch('resources-'+n,'https://github.com/maxlzyver/efootxi/releases/download/resources-311010101-v1/resources-'+n+'.zip',R/('resources-'+n+'.zip'))
fetch('resource-manifest','https://github.com/maxlzyver/efootxi/releases/download/resources-311010101-v1/manifest.json',R/'resource-manifest.json')
base='https://raw.githubusercontent.com/ron3huq/testingdummy/chat-downloads/efootxi-1.3.2/'
fetch('v4a',base+'ronaldo-pc-mesh-v4a/Ronaldo-PC-mesh-v4a-88044950524330.zip',R/'v4a.zip')
local=OUT.parent/'ronaldo-noodle-source/Ronaldo-noodle-88044950524330-SOURCE-NOT-INSTALLABLE.zip'
fetch('noodle-source',base+'ronaldo-noodle-source/Ronaldo-noodle-88044950524330-SOURCE-NOT-INSTALLABLE.zip',R/'noodle-source.zip',local=local)
assert digest(args.input_2006)==I['files']['upload:CRISTIANO RONALDO 2006.zip']['sha256'],'Wrong 2006 input ZIP'
extract(R/'v4a.zip',R/'v4a');extract(R/'noodle-source.zip',R/'ronaldo-noodle-source');extract(args.input_2006,R/'input-1')
extract(R/'efootxi-1.3.2.apk',R/'apk',lambda n:n=='lib/arm64-v8a/libUE4.so' or n.startswith(('assets/pc0000','assets/pc0010','assets/gateway-release/livedata/pc9257')) or n=='assets/gateway-release/work/templates/CMD_LOGIN_LIVEDATA.json')
extract(R/'apk/assets/pc0000_mobile_and.pak',R/'pc0000')
extract(R/'resources-03.zip',R/'resources',lambda n:n.endswith('.utoc') or any(s in n for s in ['pc3700_mobile_and.','pc3611_mobile_and.','pc0102_mobile_and.']))
extract(R/'resources-02.zip',R/'resources',lambda n:n.endswith('.utoc') or 'pc3611_mobile_and_optional.' in n)
clone('https://github.com/the4chancup/pes-fmdl-blender.git',R/'pes-fmdl-blender',I['source_commits']['pes-fmdl-blender'])
clone('https://github.com/gildor2/UEViewer.git',R/'UEViewer',I['source_commits']['UEViewer'])
patch=P/'ueviewer-v5.patch';probe=subprocess.run(['git','-C',str(R/'UEViewer'),'apply','--check',str(patch)],capture_output=True)
if probe.returncode==0:run('git','-C',str(R/'UEViewer'),'apply',str(patch))
else:run('git','-C',str(R/'UEViewer'),'apply','--reverse','--check',str(patch))
run('bash','build.sh',cwd=R/'UEViewer')
reader=R/'reader-input';reader.mkdir(exist_ok=True)
paths=list((R/'resources').rglob('pc3700_mobile_and.*'))+list((R/'resources').rglob('pc3611_mobile_and.*'))+list((R/'resources').rglob('pc3611_mobile_and_optional.*'))+list((R/'resources').rglob('pc0102_mobile_and.*'))+list((R/'apk/assets/gateway-release/livedata').glob('pc9257*'))+list((R/'apk/assets').glob('pc0010*'))+list((R/'pc0000/PesMobile/Content/Paks').glob('global.*'))+list((R/'pc0000/PesMobile/Content/Paks').glob('pakchunk0*'))
for p in paths:
 dst=reader/p.name
 if not dst.exists():dst.symlink_to(p.resolve())
 else:assert dst.resolve()==p.resolve()
vreader=R/'v4a-reader';vreader.mkdir(exist_ok=True)
for p in list((R/'v4a/livedata').iterdir())+list((R/'pc0000/PesMobile/Content/Paks').glob('global.*')):
 dst=vreader/p.name
 if not dst.exists():dst.symlink_to(p.resolve())
import sys
sys.path.insert(0,str(P));from iostore import Toc
t=Toc(str(R/'v4a/livedata/pc9298_mobile_and.utoc'));ex=R/'v4a-extracted';ex.mkdir(exist_ok=True)
for f,i in t.files.items():(ex/Path(f).name).write_bytes(t.read(i))
for version,profile,inp in [('native','4522',reader),('v4a','ND01',vreader)]:
 for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
  with (R/(version+'-'+suffix+'.log')).open('w') as log:
   run(str(R/'UEViewer/umodel'),'-export','-game=ue4.26','-android','-notex','-noanim','-gltf','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(inp),'-out='+str(R/(version+'-export')),'SK_'+profile+suffix+'_Face',stdout=log,stderr=subprocess.STDOUT)
print('Verified source inputs and native/v4a reference exports prepared:',R)
