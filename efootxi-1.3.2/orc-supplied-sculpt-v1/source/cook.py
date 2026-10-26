from pathlib import Path
import subprocess,sys,shutil
from PIL import Image
P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');R=P/'android-orc-v1';S=Path(__file__).parent;etc=P/'Etc2Comp/build/EtcTool/EtcTool'
def run(*a):subprocess.run(list(map(str,a)),check=True)
shutil.copyfile(S/'atlas.png',R/'noodle-color-atlas-2048.png');Image.open(S/'atlas.png').convert('RGB').resize((1024,1024)).save(R/'face1024.png')
run(etc,R/'noodle-color-atlas-2048.png','-format','RGBA8','-effort','15','-mipmaps','12','-jobs','4','-output',R/'noodle-color-atlas-2048.ktx')
run(etc,R/'face1024.png','-format','RGB8','-effort','15','-mipmaps','11','-jobs','4','-output',R/'pc-face-1024.ktx')
for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:run(sys.executable,R/'build_pc_head.py',v)
run(sys.executable,R/'build_face_textures.py');run(sys.executable,R/'build_materials.py')
sys.path.insert(0,str(R));from zen_clone import rename
base='/Game/Assets/character/RealFace/'
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 f=R/'asset'/('SK_'+variant.replace('4522','ND01',1)+'_Face.uasset');rep={};imports={}
 for q in ['HQ','MQ']:
  for part in ['FaceLegacy','FaceUpcon']:
   old=base+'MI_'+variant+'_Head_'+part+'_'+q;new=base+'MI_ND0001_Head_Hair_'+q;rep[old]=new;rep[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1];imports[old]=new
 f.write_bytes(rename(f.read_bytes(),rep,imports=imports))
run(sys.executable,R/'build_full_container.py')
for ext in ['utoc','ucas']:shutil.copyfile(P/'android-hulk-venom-combined/container'/('global.'+ext),R/'container'/('global.'+ext))
print('COOKED_ORC')
