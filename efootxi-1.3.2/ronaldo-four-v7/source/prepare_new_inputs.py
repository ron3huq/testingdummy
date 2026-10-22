"""Extract only regular archive files; attached prose is never executed."""
from pathlib import Path
import argparse,sys,struct,json,hashlib
import libarchive
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('rar2013',type=Path);p.add_argument('rar2027',type=Path);a=p.parse_args();sys.path.insert(0,str(a.work/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
from Ftex import ftexToDds
report={}
for year,archive in [('2013',a.rar2013),('2027',a.rar2027)]:
 root=a.work/('input-'+year);root.mkdir(exist_ok=True);files=[]
 with libarchive.file_reader(str(archive)) as arc:
  for e in arc:
   dest=(root/e.pathname).resolve();assert dest.is_relative_to(root.resolve())
   if e.isdir:dest.mkdir(parents=True,exist_ok=True)
   elif e.isfile:
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('wb') as f:
     for block in e.get_blocks():f.write(block)
    files.append(e.pathname)
   else:raise ValueError('Nonregular archive member')
 for fpk in root.rglob('face.fpk'):
  data=fpk.read_bytes();assert data[:6]==b'foxfpk';n=struct.unpack_from('<I',data,36)[0]
  dest=fpk.parent/'face_fpk';dest.mkdir(exist_ok=True)
  for i in range(n):
   off,size,nameoff,namesize=struct.unpack_from('<4Q',data,48+i*48);name=data[nameoff:nameoff+namesize].decode();assert Path(name).name==name and off+size<=len(data)
   (dest/name).write_bytes(data[off:off+size])
 converted=root/'converted';converted.mkdir(exist_ok=True);textures={};models={}
 for src in root.rglob('*.ftex'):
  if '/cris1h/' in str(src):continue
  dds=converted/(src.stem+'.dds');assert ftexToDds(str(src),str(dds));im=Image.open(dds);im.save(converted/(src.stem+'.png'));textures[src.stem]={'size':im.size,'mode':im.mode}
 for src in root.rglob('*.fmdl'):
  model=FmdlFile();model.readFile(str(src));models[src.name]=[{'index':i,'vertices':len(m.vertices),'triangles':len(m.faces),'material':m.materialInstance.name,'textures':[(role,t.filename) for role,t in m.materialInstance.textures]} for i,m in enumerate(model.meshes)]
 report[year]={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'archive_bytes':archive.stat().st_size,'archive_files':files,'models':models,'textures':textures}
(Path(__file__).resolve().parent.parent/'new-input-analysis.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
