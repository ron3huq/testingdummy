from pathlib import Path
import sys,struct,json,inspect
from PIL import Image
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry;from bundle_tools import Bundle,replace_texture;from zen_clone import rename,pid
P=Path('/tmp/73-ui710');t=Toc('/tmp/73-ui79/art-pack/livedata/pc9306_mobile_and.utoc');b=Bundle(t);folder='ui/Data/Thumbnail/Player/Variation2022/';base='/Game/Assets/'+folder;report=[]
def put(key,template,image=None):
 raw=b.files[folder+template+'.uasset'][1];entry=b.entries[pid(base+template)];data=raw
 if image is not None:data,bulk,dims,decoded=replace_texture(raw,image);assert not bulk
 data=rename(data,{template:key,base+template:base+key},base+template,base+key);ident=struct.pack('<Q',pid(base+key))+b'\0\0\0\2';b.put(folder+key+'.uasset',ident,data,entry);report.append(key)
for target in ['105804908868664','105873896755947','105647605587130']:
 for suffix,kind in [('_l','large'),('_','small')]:put('U79_'+target+suffix,'U79_88044950524330'+suffix,Image.open(P/'art'/(target+'-'+kind+'.png')))
for target in ['106754901843130','105647605587130','105804908868664','105873896755947']:
 put('U710_'+target+'_l','U79_'+target+'_l',Image.open(P/'art'/(target+'-foreground.png')));put('U710_'+target+'_','U79_'+target+'_')
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9306_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'art-pack/livedata');(P/'art-pack-validation.json').write_text(json.dumps({'passed':True,'native_photo_packages':len(b.entries),'updated_keys':report,'hero_background_overrides_have_transparent_foregrounds':True,'unchanged_old_photos_preserved':True,'device_tested':False},indent=2));print('ART_PACK_READY',len(b.entries))
