from pathlib import Path
import sys,json,struct,inspect,hashlib,math
import numpy as np
from PIL import Image,ImageOps
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle,replace_texture,decode_first_texture
from zen_clone import rename,pid
P=Path('/workspace/ronaldo-work/73-ui5');R=P.parent
native=Toc(str(next((R/'resources').rglob('pc1000_mobile_and.utoc'))))
# Preserve every existing kit glyph exactly. Correct coach pictures alone.
old=Toc(str(R/'73-ui4/payload/livedata/pc9300_mobile_and.utoc'));portraits=Bundle(old)
for cid,label in [('17606144688129','zidane'),('17604802510874','ferguson')]:
 path='ui/Data/Symbol/Coach/Variation/coach_'+cid+'_.uasset';raw=native.read(native.files[path]);dims=decode_first_texture(raw).size
 if label=='zidane':edited=raw;method='restore native Zidane variation photo; original proportions'
 else:
  image=Image.open(R/'73-ui4'/label/'coach-portrait.png').convert('RGBA');side=min(dims)-6
  image=ImageOps.fit(image,(side,side),Image.Resampling.LANCZOS,centering=(.5,.30));canvas=Image.new('RGBA',dims);canvas.alpha_composite(image,(3,dims[1]-side));edited,bulk,_,_=replace_texture(raw,canvas);assert not bulk;method='aspect-preserving crop, native128-square template, transparent margins'
 portraits.native(native,path,edited);print('PORTRAIT',label,dims,method)
source=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9300_mobile_and'");ns={};exec('class Writer:\n'+source,Bundle.write.__globals__,ns);ns['Writer'].write(portraits,P/'payload/livedata')
# Extend the manager overlay with private league logos, leaving standard symbols intact.
t=Toc(str(P/'manager-payload/pc9302_mobile_and.utoc'));bundle=Bundle(t);h=parse_header(native.read(next(j for j,x in enumerate(native.ids)if x[11]==10)))
atlas=Image.open('/workspace/generated_images/exec-47af9458-8394-46e3-9a50-72a516d78ea0.png').convert('RGBA');codes=['Y08','Y17','UCL','AP','WORLD','AFC'];ids=[473,518,122,549,128,566];rows=[];(P/'logos').mkdir(exist_ok=True)
for index,(code,cid)in enumerate(zip(codes,ids)):
 x=index%3*512;y=index//3*512;image=atlas.crop((x,y,x+512,y+512));box=image.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox();assert box;image=image.crop(box);image.save(P/'logos'/(code+'.png'))
 for suffix in ['','_s','_l']:
  path='ui/Data/Symbol/Other/emblemOther-nationalEurope'+suffix+'.uasset';raw=native.read(native.files[path]);at=raw.rfind(b'PF_B8G8R8A8\0')+len(b'PF_B8G8R8A8\0');first,count=struct.unpack_from('<II',raw,at);assert first==0 and count==1;at+=8;cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;assert cooked==1 and n==size and not(flags&0x100);w,hh,depth=struct.unpack_from('<III',raw,at+n);assert w*hh*4==n
  # Keep the native icon's transparent outer padding and square sampling box.
  canvas=Image.new('RGBA',(w,hh));fit=ImageOps.contain(image,(max(1,round(w*.90)),max(1,round(hh*.90))),Image.Resampling.LANCZOS);canvas.alpha_composite(fit,((w-fit.width)//2,(hh-fit.height)//2));array=np.array(canvas);payload=array[:,:,[2,1,0,3]].tobytes();edited=raw[:at]+payload+raw[at+n:];dims=[[w,hh]]
  oldname=Path(path).stem;name='emblemOther-UI5_'+code+suffix;op='/Game/Assets/'+path[:-7];np_='/Game/Assets/ui/Data/Symbol/Other/'+name;edited=rename(edited,{oldname:name,op:np_},op,np_);idx=native.files[path];pk=int.from_bytes(native.ids[idx][:8],'little');idb=struct.pack('<Q',pid(np_))+native.ids[idx][8:];bundle.put('ui/Data/Symbol/Other/'+name+'.uasset',idb,edited,store_entry(h['store'],h['pids'].index(pk)));rows.append(dict(competition=cid,code=code,suffix=suffix,dimensions=dims,drawn_content_size=fit.size))
source=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9302_mobile_and'");ns={};exec('class Writer:\n'+source,Bundle.write.__globals__,ns);ns['Writer'].write(bundle,P/'payload/livedata');(P/'logo-build.json').write_text(json.dumps(rows,indent=2));print('LEAGUE_LOGOS',len(rows))
