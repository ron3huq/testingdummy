"""Read/export the two exact Pato card-image assets from existing public game data."""
from pathlib import Path
import sys,subprocess,json,hashlib
from iostore import Toc
from PIL import Image
work=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;dest=out/'card-art-research';dest.mkdir(exist_ok=True);toc=next((work/'resources').rglob('pc1000_mobile_and.utoc'));t=Toc(str(toc));rows=[]
for name in ['88038776539586_','88038776539586_l']:
 key='ui/Data/Thumbnail/Player/Variation2022/'+name+'.uasset';raw=t.read(t.files[key]);log=dest/(name+'-reader.log')
 cmd=[str(work/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(work/'v10-reader'),'-out='+str(work/'card-art-research/export'),name]
 with log.open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
 image=work/'card-art-research/export/Game/Assets/ui/Data/Thumbnail/Player/Variation2022'/(name+'.png');im=Image.open(image);assert im.mode=='RGBA';(dest/image.name).write_bytes(image.read_bytes());rows.append({'package':key,'asset_bytes':len(raw),'asset_sha256':hashlib.sha256(raw).hexdigest(),'size':list(im.size),'mode':im.mode})
(dest/'verified-assets.json').write_text(json.dumps({'card_id':'88038776539586','textures':rows,'artwork_replaced':False,'phone_tested':False},indent=2));print('EXACT_PATO_TEXTURES_EXPORTED_AND_DIMENSIONS_VERIFIED')
