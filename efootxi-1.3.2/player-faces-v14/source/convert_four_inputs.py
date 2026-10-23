from pathlib import Path
import sys,shutil,json,texture2ddecoder
from PIL import Image
sys.path.insert(0,str(Path(sys.argv[1])/'pes-fmdl-blender/pes-fmdl'))
from Ftex import ftexToDds
out={}
for label in ['hoang-duc','hoang-hen','pendant','tai-loc']:
 root=Path(sys.argv[1])/('input-'+label);conv=root/'converted';conv.mkdir(exist_ok=True);rows={}
 for f in root.rglob('*.ftex'):
  dest=conv/(f.stem+'.dds')
  if not ftexToDds(str(f),str(dest)):
   supplied=f.with_suffix('.dds')
   if not supplied.exists():continue
   shutil.copyfile(supplied,dest)
  im=Image.open(dest)
  try:im.load()
  except OSError:
   data=dest.read_bytes();w,h=im.size;block=8 if data[84:88]==b'DXT1' else 16;assert data[84:88] in [b'DXT1',b'DXT5'];payload=data[128:];need=((w+3)//4)*((h+3)//4)*block;assert 0<need-len(payload)<=((w+3)//4+1)*block;payload=payload[:len(payload)//block*block];payload+=payload[-block:]*((need-len(payload))//block);im=Image.frombytes('RGBA',(w,h),(texture2ddecoder.decode_bc1 if block==8 else texture2ddecoder.decode_bc3)(payload,w,h),'raw','BGRA')
  im.save(conv/(f.stem+'.png'));rows[f.stem]=list(im.size)
 for f in root.rglob('*.dds'):
  if f.parent==conv:continue
  if not (conv/(f.stem+'.png')).exists():
   im=Image.open(f);im.load();im.save(conv/(f.stem+'.png'));shutil.copyfile(f,conv/f.name);rows[f.stem]=list(im.size)
 out[label]=rows
print(json.dumps(out,indent=2))
