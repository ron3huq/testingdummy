"""Extract only regular archive files; attached prose is never executed."""
from pathlib import Path
import argparse,sys,struct,json,hashlib,shutil
import libarchive
from PIL import Image
import texture2ddecoder
p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('xuan_son',type=Path);p.add_argument('junior',type=Path);p.add_argument('dinh_bac',type=Path);a=p.parse_args();sys.path.insert(0,str(a.work/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
from Ftex import ftexToDds
report={}
for year,archive in [('xuan-son',a.xuan_son),('junior',a.junior),('dinh-bac',a.dinh_bac)]:
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
  dds=converted/(src.stem+'.dds');ok=ftexToDds(str(src),str(dds))
  if not ok:
   supplied=src.with_suffix('.dds')
   if not supplied.exists():textures[src.stem]={'conversion_error':'unsupported FTEX, no supplied DDS'};continue
   shutil.copyfile(supplied,dds)
  im=Image.open(dds);repair=None
  try:im.load()
  except OSError:
   data=dds.read_bytes();width,height=im.size;fourcc=data[84:88];assert fourcc in [b'DXT1',b'DXT5'] and (width%4 or height%4);block=8 if fourcc==b'DXT1' else 16
   need=((width+3)//4)*((height+3)//4)*block;payload=data[128:];missing=need-len(payload);assert 0<missing<=((width+3)//4)*block+block
   # Only incomplete final BC block row; do not read outside supplied payload.
   full=len(payload)//block*block;payload=payload[:full];last=payload[-block:];payload+=last*((need-len(payload))//block)
   im=Image.frombytes('RGBA',(width,height),(texture2ddecoder.decode_bc1 if block==8 else texture2ddecoder.decode_bc3)(payload,width,height),'raw','BGRA');repair={'missing_edge_payload_bytes':missing,'method':'replicate last complete BC block into incomplete bottom row'}
  im.save(converted/(src.stem+'.png'));textures[src.stem]={'size':im.size,'mode':im.mode,'repair':repair}
 for src in root.rglob('*.fmdl'):
  model=FmdlFile();model.readFile(str(src));models[src.name]=[{'index':i,'vertices':len(m.vertices),'triangles':len(m.faces),'material':m.materialInstance.name,'textures':[(role,t.filename) for role,t in m.materialInstance.textures]} for i,m in enumerate(model.meshes)]
 report[year]={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'archive_bytes':archive.stat().st_size,'archive_files':files,'models':models,'textures':textures}
(Path(__file__).resolve().parent.parent/'new-input-analysis.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
