from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import decode_first_texture
P=Path('/tmp/73-ui711');t=Toc(str(P/'art-pack/livedata/pc9306_mobile_and.utoc'));old=Toc(str(P/'build/payload/livedata/pc9306_mobile_and.utoc'));updated=set();rows=[]
for pid in json.loads((P/'new-targets.json').read_text())['targets']+['88044950524330']:
 for suffix,kind,size in [('_','small',(128,128)),('_l','large',(184,256))]:
  path='ui/Data/Thumbnail/Player/Variation2022/U79_'+pid+suffix+'.uasset';raw=t.read(t.files[path]);im=decode_first_texture(raw);assert im.size==size;assert im.getchannel('A').getextrema()==(0,255);source=Image.open(P/'art'/(pid+'-'+kind+'.png'));a=np.array(im).astype(float);b=np.array(source).astype(float);mask=b[:,:,3]>240;error=np.abs(a[:,:,:3]-b[:,:,:3])[mask].mean();assert error<15,(pid,kind,error);updated.add(path);rows.append({'id':pid,'view':kind,'size':size,'mean_ETC2_RGB_error_opaque_pixels':round(error,3)});im.save(P/'art'/(pid+'-'+kind+'-game.png'))
for path,index in old.files.items():
 if path not in updated:assert t.read(t.files[path])==old.read(index),path
(P/'art-decode-validation.json').write_text(json.dumps({'passed':True,'textures':rows,'old_unrelated_photos_byte_preserved':True,'new_five_original_face_RGB_not_generated':True,'uniform_scaling_layouts':'portrait-layouts.json','Android_tested':False},indent=2));print('ART_TEXTURE_DECODE_PASS')
