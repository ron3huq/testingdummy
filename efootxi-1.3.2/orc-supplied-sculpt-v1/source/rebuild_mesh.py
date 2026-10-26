from pathlib import Path
import subprocess,sys
R=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-orc-v1')
for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:subprocess.run([sys.executable,str(R/'build_pc_head.py'),v],check=True)
subprocess.run([sys.executable,str(R/'build_materials.py')],check=True)
sys.path.insert(0,str(R));from zen_clone import rename
base='/Game/Assets/character/RealFace/'
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 f=R/'asset'/('SK_'+variant.replace('4522','ND01',1)+'_Face.uasset');rep={};imports={}
 for q in ['HQ','MQ']:
  for part in ['FaceLegacy','FaceUpcon']:
   old=base+'MI_'+variant+'_Head_'+part+'_'+q;new=base+'MI_ND0001_Head_Hair_'+q;rep[old]=new;rep[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1];imports[old]=new
 f.write_bytes(rename(f.read_bytes(),rep,imports=imports))
subprocess.run([sys.executable,str(R/'build_full_container.py')],check=True)
