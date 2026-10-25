from pathlib import Path
import sys,json,inspect,struct,hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle,decode_first_texture,replace_texture
from zen_clone import rename,pid
P=Path('/workspace/ronaldo-work/73-ui4');R=Path('/workspace/ronaldo-work');font=Toc(str(next((R/'resources').rglob('pc0103_mobile_and.utoc'))));coach=Toc(str(next((R/'resources').rglob('pc1000_mobile_and.utoc'))));base=Toc('/workspace/ronaldo-work/73-v25-port/package/payload/livedata/pc9298_mobile_and.utoc')
bundle=object.__new__(Bundle);bundle.base=base;bundle.files={};bundle.entries={};headers={}
def clone(t,path,dest,raw):
 h=headers.setdefault(t.path,parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10))));i=t.files[path];oldpath='/Game/Assets/'+(t.mount+path).split('/Content/Assets/')[1].removesuffix('.uasset');newpath='/Game/Assets/'+dest.removesuffix('.uasset');oldname=Path(path).stem;newname=Path(dest).stem
 raw=rename(raw,{oldpath:newpath,oldname:newname},oldpath,newpath);oldpid=int.from_bytes(t.ids[i][:8],'little');idb=struct.pack('<Q',pid(newpath))+t.ids[i][8:];bundle.put(dest,idb,raw,store_entry(h['store'],h['pids'].index(oldpid)))
rows=[]
colors={242:[(0,0,0),(0,0,0)],351:[(2,121,165),(245,245,245)],352:[(245,245,245),(245,245,245)],245:[(244,218,59),(15,35,62)]}
for tid,slots in colors.items():
 for slot,color in enumerate(slots,1):
  for kind in['Name_D','Name_Ex_D','Back_D','Chest_D','Leg_D']:
   source=f'character/Uniform/LowTextures/T_u0100p{slot}_Font{kind}.uasset';dest=f'character/Uniform/LowTextures/T_u{tid:04d}p{slot}_Font{kind}.uasset';raw=font.read(font.files[source]);image=decode_first_texture(raw);pixels=np.array(image);pixels[:,:,:3]=color;new,bulk,dims,out=replace_texture(raw,Image.fromarray(pixels),preserve_alpha=True);assert not bulk;assert out.getchannel('A').tobytes()==image.getchannel('A').tobytes();clone(font,source,dest,new);rows.append(dict(kind='glyph',team=tid,slot=slot,name=kind,color=color,dimensions=dims,template='nativeMU100',encoded_alpha_unchanged=True))
for cid,label in[(17606144688129,'zidane'),(17604802510874,'ferguson')]:
 path=next(k for k in coach.files if '/Symbol/Coach/coach_'in k);raw=coach.read(coach.files[path]);img=Image.open(P/label/'coach-portrait.png').convert('RGBA');new,bulk,dims,_=replace_texture(raw,img);assert not bulk;dest='ui/Data/Symbol/Coach/Variation/coach_'+str(cid)+'_.uasset';clone(coach,path,dest,new);rows.append(dict(kind='coach_portrait',id=str(cid),source=label+'.rar',dimensions=dims,source_image_sha256=hashlib.sha256((P/label/'coach-portrait.png').read_bytes()).hexdigest()))
source=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9300_mobile_and'");ns={};exec('class Writer:\n'+source,Bundle.write.__globals__,ns);ns['Writer'].write(bundle,P/'payload/livedata');(P/'extras-build.json').write_text(json.dumps(rows,indent=2));print('EXTRAS_BUILT',len(rows))
