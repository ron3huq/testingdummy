"""Extract generated atlas cells; encode native square minis and portrait cards.
Creative editing is done by image_gen; this step only cuts sprite-sheet cells,
preserves aspect ratio and converts to the game's exact Texture2D dimensions.
"""
from pathlib import Path
import json,shutil
import numpy as np
from PIL import Image,ImageOps,ImageDraw
from iostore import Toc
from bundle_tools import Bundle,replace_texture

O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');art=O/'art';art.mkdir(exist_ok=True)
sources={'minis':Path('/workspace/generated_images/exec-99ebd58c-f50b-45df-9bc4-552977588d3f.png'),'large':Path('/workspace/generated_images/exec-ea587f25-e65f-40cb-b7aa-c9f49a787f6e.png')}
for label,path in sources.items():
    target=art/(label+'-sheet.png')
    if not target.exists():shutil.copyfile(path,target)
native=[Toc(str(next((R/'resources').rglob('pc100'+str(i)+'_mobile_and.utoc'))))for i in [0,1]]
t=Toc(str(O/'letters-container/pc9298_mobile_and.utoc'));bundle=Bundle(t);rows=[]
minis=['88038776539586','106778792700170','106781745353130','106726716084650','89135066911146','88044950524330']
large=['88044950524330','89135066911146','106726716084650','106781745353130']
for label,cards,cols,nrows,suffix,size in [('minis',minis,3,2,'_',(128,128)),('large',large,2,2,'_l',(184,256))]:
    sheet=Image.open(art/(label+'-sheet.png')).convert('RGBA');w,h=sheet.size
    if label=='minis':assert w//cols==h//nrows
    for i,card in enumerate(cards):
        x,y=i%cols,i//cols;cell=sheet.crop((x*w//cols,y*h//nrows,(x+1)*w//cols,(y+1)*h//nrows))
        # Keep original aspect ratio. Large artwork is cropped from the top,
        # retaining the full hairstyle; NEVER squeeze portrait art into a mini.
        image=ImageOps.fit(cell,size,Image.Resampling.LANCZOS,centering=(.5,0))
        image.save(art/(card+suffix+'.png'));name=card+suffix+'.uasset'
        nt,path=next((nt,path)for nt in native for path in nt.files if Path(path).name==name)
        updated,bulk,dims,decoded=replace_texture(nt.read(nt.files[path]),image);assert not bulk and dims[0]==list(size)
        bundle.native(nt,path,updated);decoded.save(art/(card+suffix+'-decoded.png'))
        data=np.array(image);row={'card':card,'kind':label,'dimensions':dims,'aspect_preserved':True,'native_UI_frame_rating_and_names_not_baked':True,'independent_mini_and_large_assets':True}
        if label=='minis':
            a=data[:,:,3];head=a[:80]>128;yy,xx=np.where(head)
            row.update(transparent_pixel_fraction=float(np.mean(a==0)),head_top=int(yy.min()),head_center_x=float(xx.mean()),head_width=int(xx.max()-xx.min()+1))
            assert 3<=row['head_top']<=16 and 54<=row['head_center_x']<=74
        rows.append(row)
bundle.write(O/'container');(O/'card-layout-validation.json').write_text(json.dumps({'portraits':rows,'large_art_style':'custom photographic collector-card compositions using user references; no claim of official Big Time background','phone_verified':False},indent=2))
preview=Image.new('RGB',(900,340),'#243545');draw=ImageDraw.Draw(preview)
for i,card in enumerate(minis):
    im=Image.open(art/(card+'_.png')).convert('RGBA');preview.paste(im,(i*150+10,30),im);draw.text((i*150+4,9),card,fill='white')
    if card in large:
        im=Image.open(art/(card+'_l.png')).convert('RGBA');im.thumbnail((115,160));preview.paste(im,(i*150+10,170))
preview.save(O/'Card-layout-preview.png');print('SIX_MINIS_FOUR_LARGE_NATIVE_CARD_TEXTURES_BUILT')
