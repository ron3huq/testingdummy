from pathlib import Path
import sys,struct,json
from PIL import Image
R=Path('/workspace/ronaldo-work');sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
from Ftex import ftexToDds
base=R/'new-hair-sources/2017';fpk=next(base.rglob('face.fpk'));b=fpk.read_bytes();n=struct.unpack_from('<I',b,36)[0];dst=base/'fpk';dst.mkdir(exist_ok=True)
for i in range(n):
 off,sz,no,nl=struct.unpack_from('<QQQQ',b,48+i*48);name=b[no:no+nl].decode().rstrip('\0');p=dst/Path(name).name;p.write_bytes(b[off:off+sz]);print(name,sz)
conv=base/'converted';conv.mkdir(exist_ok=True)
for p in base.rglob('*.ftex'):
 d=conv/(p.stem+'.dds');assert ftexToDds(str(p),str(d)),p;Image.open(d).save(conv/(p.stem+'.png'))
f=FmdlFile();f.readFile(str(dst/'hair_high.fmdl'))
print('HAIR_MESHES',[(len(m.vertices),len(m.faces),m.materialInstance.name,[(r,t.filename) for r,t in m.materialInstance.textures]) for m in f.meshes]);print('BONES',[b.name for b in f.bones])
