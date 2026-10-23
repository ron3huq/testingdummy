"""Safe archive/model/texture recovery from supplied source data. No attached
instructions/scripts are executed. Reuses the existing audited PES dependency.
"""
from pathlib import Path
import argparse,sys,struct,zlib,json,hashlib,zipfile
import libarchive
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,default=Path('/workspace/ronaldo-work'));a=p.parse_args();O=Path(__file__).resolve().parent.parent;R=a.work;sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from Ftex import ftexToDds
inventory={x['filename']:x for x in json.loads((O/'input-inventory.json').read_text())['user_latest_archives']}
def top_ftex(src,dst):
 b=src.read_bytes();magic,version,fmt,w,h,d=struct.unpack_from('<4sfHHHH',b);assert magic==b'FTEX'and fmt==11 and d==1;offset,size,comp,index,ext,chunks=struct.unpack_from('<IIIBBH',b,64);assert index==ext==0;pieces=[]
 for i in range(chunks):
  cs,us,off=struct.unpack_from('<HHI',b,offset+i*8);piece=b[offset+(off&0x7fffffff):offset+(off&0x7fffffff)+cs];data=piece if off>>31 else zlib.decompress(piece);assert len(data)==us;pieces.append(data)
 payload=b''.join(pieces);assert len(payload)==size==((w+3)//4)*((h+3)//4)*16;hdr=struct.pack('<I6I11I',124,0x81007,h,w,len(payload),0,0,*([0]*11))+struct.pack('<II4s5I',32,4,b'DX10',0,0,0,0,0)+struct.pack('<5I',0x1000,0,0,0,0);dds=dst.with_suffix('.top.dds');dds.write_bytes(b'DDS '+hdr+struct.pack('<5I',98,3,0,1,0)+payload);Image.open(dds).save(dst);dds.unlink()
for name,label in [('real madrid2011.rar','rm2011'),('Ronaldo Noodle Hair 2017.rar','2017'),('barcelona2017.rar','barca2017'),('manchesterunited2007.rar','mu2007'),('Ozil.rar','ozil'),('Ronaldo 2027.rar','2027')]:
 arc=O/'original-inputs'/name;assert hashlib.sha256(arc.read_bytes()).hexdigest()==inventory[name]['sha256'];root=R/'v20-input'/label;root.mkdir(parents=True,exist_ok=True)
 with libarchive.file_reader(str(arc))as entries:
  for e in entries:
   dest=(root/e.pathname.replace('\\','/')).resolve();assert dest.is_relative_to(root.resolve())
   if e.isdir:continue
   assert e.isfile;dest.parent.mkdir(parents=True,exist_ok=True)
   with dest.open('wb')as f:
    for b in e.get_blocks():f.write(b)
 for src in root.rglob('*.fpk'):
  b=src.read_bytes();assert b[:6]==b'foxfpk';dest=src.parent/'face_fpk';dest.mkdir(exist_ok=True)
  for i in range(struct.unpack_from('<I',b,36)[0]):
   off,size,no,ns=struct.unpack_from('<4Q',b,48+48*i);n=b[no:no+ns].decode();assert Path(n).name==n and off+size<=len(b);(dest/n).write_bytes(b[off:off+size])
 for src in root.rglob('*.ftex'):
  if label in ['rm2011','barca2017','mu2007']:top_ftex(src,src.with_suffix('.png'))
  else:
   dest=root/'converted';dest.mkdir(exist_ok=True);dds=dest/(src.stem+'.dds');assert ftexToDds(str(src),str(dds));Image.open(dds).save(dest/(src.stem+'.png'))
 print(label,'source recovered')
# Recover the valid top level of supplied Sparta sources as well; source small
# mips were malformed, so they are not fed to the Android encoder.
for src in (O/'references/sparta-inputs').glob('*.ftex'):top_ftex(src,src.with_suffix('.png'))
# Recover pc9261 from cached public resources before requesting phone files.
for archive in [R/'resources-03.zip']:
 with zipfile.ZipFile(archive)as z:
  for info in z.infolist():
   if 'Download/pc9261_mobile_and.'in info.filename:
    dest=R/'resources'/info.filename;dest.parent.mkdir(parents=True,exist_ok=True);data=z.read(info)
    if dest.exists():assert dest.read_bytes()==data
    else:dest.write_bytes(data)
# Restore the previous cooked baseline from the verified published v19 install.
previous=O.parent/'player-faces-v19';arc=previous/'Faces-v19-13-cards-Sparta-kits.zip';assert hashlib.sha256(arc.read_bytes()).hexdigest()=='40ffebb97edd616138150c7967675b9f03dab12698b7642d9c5fd42197c4375d'
with zipfile.ZipFile(arc)as z:
 for ext in ['pak','utoc','ucas']:
  dest=previous/'container'/('pc9298_mobile_and.'+ext);data=z.read('livedata/'+dest.name);dest.parent.mkdir(exist_ok=True)
  if dest.exists():assert dest.read_bytes()==data
  else:dest.write_bytes(data)
print('V20 sources and pinned v19 baseline ready')
