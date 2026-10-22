from pathlib import Path
import libarchive,sys,struct,json
sys.path.insert(0,str(Path(sys.argv[1])/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
out={}
import argparse
p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent.parent/'original-inputs');args=p.parse_args()
for label,arc in [('hoang-duc','Nguyen Hoang Duc.rar'),('hoang-hen','Do Hoang Hen.rar'),('pendant','Cao Pendant.rar'),('tai-loc','Nguyen Tai Loc.rar')]:
 root=args.work/('input-'+label);root.mkdir(exist_ok=True)
 with libarchive.file_reader(str(args.inputs/arc)) as entries:
  for e in entries:
   p=(root/e.pathname).resolve();assert p.is_relative_to(root)
   if e.isdir:p.mkdir(parents=True,exist_ok=True)
   elif e.isfile:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('wb') as f:
     for b in e.get_blocks():f.write(b)
   else:raise ValueError(e.pathname)
 for fpk in root.rglob('*.fpk'):
  data=fpk.read_bytes();assert data[:6]==b'foxfpk';dest=fpk.parent/(fpk.stem+'_fpk');dest.mkdir(exist_ok=True)
  for i in range(struct.unpack_from('<I',data,36)[0]):
   off,size,no,ns=struct.unpack_from('<4Q',data,48+48*i);name=data[no:no+ns].decode();assert Path(name).name==name and off+size<=len(data);(dest/name).write_bytes(data[off:off+size])
 models={}
 for p in root.rglob('*.fmdl'):
  f=FmdlFile();f.readFile(str(p));models[str(p.relative_to(root))]=[dict(verts=len(m.vertices),tris=len(m.faces),mat=m.materialInstance.name,textures=[(r,t.filename) for r,t in m.materialInstance.textures]) for m in f.meshes]
 out[label]=dict(files=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()],models=models)
(Path(__file__).resolve().parent.parent/'new-four-analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v['models'] for k,v in out.items()},indent=2))
