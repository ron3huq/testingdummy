from pathlib import Path
import subprocess,sys,shutil,json
from PIL import Image
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');kind=sys.argv[1];N=P/('android-five-'+kind);info=json.loads((R/'targets.json').read_text())[kind];prefix=info['prefix'];mi=info['material_prefix'];etc=P/'Etc2Comp/build/EtcTool/EtcTool'
def run(*a):subprocess.run(list(map(str,a)),check=True)
if kind=='ronaldo':
 Image.open(R/'source/ronaldo2009/png/hair_parts_bsm_alp.png').convert('RGBA').resize((2048,2048)).save(N/'noodle-color-atlas-2048.png');Image.open(R/'ronaldo/native_face_diffuse.png').convert('RGB').save(N/'face1024.png')
else:
 Image.open(R/kind/'atlas.png').convert('RGBA').save(N/'noodle-color-atlas-2048.png');Image.open(R/kind/'atlas.png').convert('RGB').resize((1024,1024)).save(N/'face1024.png')
run(etc,N/'noodle-color-atlas-2048.png','-format','RGBA8','-effort','15','-mipmaps','12','-jobs','4','-output',N/'noodle-color-atlas-2048.ktx')
run(etc,N/'face1024.png','-format','RGB8','-effort','15','-mipmaps','11','-jobs','4','-output',N/'pc-face-1024.ktx')
for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:run(sys.executable,N/'build_pc_head.py',v)
run(sys.executable,N/'build_face_textures.py');run(sys.executable,N/'build_materials.py')
# Nonhuman heads use only the private opaque atlas material. Ronaldo keeps native face shaders.
if kind!='ronaldo':
 sys.path.insert(0,str(N));from zen_clone import rename;base='/Game/Assets/character/RealFace/'
 for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
  f=N/'asset'/('SK_'+variant.replace('4522',prefix,1)+'_Face.uasset');rep={};imports={}
  for q in ['HQ','MQ']:
   for part in ['FaceLegacy','FaceUpcon']:
    old=base+'MI_'+variant+'_Head_'+part+'_'+q;new=base+'MI_'+mi+'_Head_Hair_'+q;rep[old]=new;rep[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1];imports[old]=new
  f.write_bytes(rename(f.read_bytes(),rep,imports=imports))
print('COOKED',kind,flush=True)
