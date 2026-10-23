from pathlib import Path
import libarchive,struct,sys,json
arc=next(Path('/workspace/attachments').rglob('CRISTIANO RONALDO 2008.rar'));root=Path('/workspace/ronaldo-work/input-2008');root.mkdir(exist_ok=True)
with libarchive.file_reader(str(arc)) as entries:
 for e in entries:
  p=(root/e.pathname).resolve();assert p.is_relative_to(root)
  if e.isdir:p.mkdir(parents=True,exist_ok=True)
  elif e.isfile:
   p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('wb') as f:
    for b in e.get_blocks():f.write(b)
  else:raise ValueError(e.pathname)
for f in root.rglob('*.fpk'):
 b=f.read_bytes();assert b[:6]==b'foxfpk';d=f.parent/(f.stem+'_fpk');d.mkdir(exist_ok=True)
 for i in range(struct.unpack_from('<I',b,36)[0]):
  off,size,no,ns=struct.unpack_from('<4Q',b,48+48*i);name=b[no:no+ns].decode();assert Path(name).name==name and off+size<=len(b);(d/name).write_bytes(b[off:off+size])
sys.path.insert(0,'/workspace/ronaldo-work/pes-fmdl-blender/pes-fmdl');from FmdlFile import FmdlFile;from Ftex import ftexToDds
from PIL import Image
conv=root/'converted';conv.mkdir(exist_ok=True)
for f in root.rglob('*.ftex'):
 d=conv/(f.stem+'.dds');assert ftexToDds(str(f),str(d));im=Image.open(d);im.load();im.save(conv/(f.stem+'.png'))
models={}
for p in root.rglob('*.fmdl'):
 f=FmdlFile();f.readFile(str(p));models[str(p.relative_to(root))]=[{'verts':len(m.vertices),'tris':len(m.faces),'material':m.materialInstance.name,'textures':[(r,t.filename) for r,t in m.materialInstance.textures]} for m in f.meshes]
(root/'inspection.json').write_text(json.dumps(models,indent=2));print(json.dumps(models,indent=2))
