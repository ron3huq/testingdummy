from pathlib import Path
import libarchive,sys,json,struct
from PIL import Image
work=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/ronaldo-work');archive=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parent.parent/'original-inputs/ISHOWSPEED.rar'
sys.path.insert(0,str(work/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
from Ftex import ftexToDds
root=work/'input-speed';root.mkdir(exist_ok=True)
with libarchive.file_reader(str(archive)) as arc:
 for e in arc:
  p=(root/e.pathname).resolve();assert p.is_relative_to(root)
  if e.isdir:p.mkdir(parents=True,exist_ok=True)
  elif e.isfile:
   p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('wb') as f:
    for b in e.get_blocks():f.write(b)
  else:raise ValueError(e.pathname)
conv=root/'converted';conv.mkdir(exist_ok=True)
for f in root.rglob('*.ftex'):
 d=conv/(f.stem+'.dds');assert ftexToDds(str(f),str(d));im=Image.open(d);im.load();im.save(conv/(f.stem+'.png'))
report={}
for p in root.rglob('*.fmdl'):
 f=FmdlFile();f.readFile(str(p));report[p.name]=[{'verts':len(m.vertices),'tris':len(m.faces),'material':m.materialInstance.name,'textures':[(r,t.filename) for r,t in m.materialInstance.textures]} for m in f.meshes]
(Path(__file__).resolve().parent.parent/'speed-source-analysis.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
