from pathlib import Path
import sys,json,numpy as np
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import decode_first_texture
P=Path('/tmp/73-ui79');t=Toc('/workspace/ronaldo-work/apk/assets/pc0010_mobile_and.utoc');t1=Toc('/workspace/ronaldo-work/resources/assetpacks/pad_ff_00/311010101/311010101/assets/pc0102_mobile_and.utoc');out=[]
for i in range(1,7):
 source=t1 if i==1 else t;p=next(k for k in source.files if k.endswith(f'T_Sk{i}_Skin_D.uasset'));bulk=source.read(source.files[p[:-7]+'.ubulk'])if p[:-7]+'.ubulk'in source.files else b'';im=decode_first_texture(source.read(source.files[p]),bulk);im.save(P/'art'/f'native-skin-{i}.png');a=np.array(im);rgb=a[:,:,:3];lum=rgb.astype('u4')@np.array([54,183,19])//256;mask=(a[:,:,3]>0)&(lum>30)&(rgb[:,:,0]>=rgb[:,:,1])&(rgb[:,:,1]>=rgb[:,:,2]);sample=np.median(rgb[mask],axis=0).round().astype(int);out.append({'id':i,'hex':''.join(f'{x:02x}'for x in sample),'source':p,'preview':'Median of skin-coloured opaque pixels from the native skin albedo; in-game lighting varies'})
(P/'build/payload/work/tools/native_skin_previews.json').write_text(json.dumps(out,indent=2));print(out)
