# Atlas packing only; photographic changes were made with image_gen.
# Used by build_heads.py with completed source Bundle in memory.
from PIL import ImageDraw
art=O/'art';sheet=Image.open(art/'ronaldo-mini-sheet.png').convert('RGBA');w,h=sheet.size
cards=['88044950524330','89135066911146','106726716084650','106781745353130']
# Head bounds measured in the reviewed 627-square cells, excluding arms/torso.
head_bounds=[(200,20,500,445),(135,25,500,440),(170,8,465,448),(170,12,465,450)]
framing=[]
for i,(card,box)in enumerate(zip(cards,head_bounds)):
 cell=sheet.crop((i%2*w//2,i//2*h//2,(i%2+1)*w//2,(i//2+1)*h//2));l,t,r,b=[v*(w//2)/627 for v in box];scale=85/(b-t);cx=(l+r)/2;dx=64-cx*scale;dy=8-t*scale
 # Single uniform scale: never independently squeeze width/height.
 image=cell.transform((128,128),Image.Transform.AFFINE,(1/scale,0,-dx/scale,0,1/scale,-dy/scale),Image.Resampling.BICUBIC)
 image.save(art/(card+'_.png'));path=next(p for p in old.files if Path(p).name==card+'_.uasset');raw,bulk,dims,decoded=replace_texture(old.read(old.files[path]),image);assert not bulk and dims[0]==[128,128]
 key,_=bundle.files[path];bundle.files[path]=(key,raw);decoded.save(art/(card+'_-decoded.png'));framing.append({'card':card,'measured_head_bounds_source':box,'head_center_x_after':cx*scale+dx,'head_top_after':t*scale+dy,'head_width_after':(r-l)*scale,'head_height_after':(b-t)*scale,'uniform_scale':scale,'independent_mini_not_squeezed_large_card':True})
canvas=Image.new('RGB',(640,180),'#243545');draw=ImageDraw.Draw(canvas)
for i,card in enumerate(cards):
 image=Image.open(art/(card+'_.png'));canvas.paste(image,(i*160+16,30),image);draw.text((i*160+3,8),card,fill='white')
canvas.save(O/'Mini-preview.png');(O/'mini-framing.json').write_text(json.dumps(framing,indent=2))
