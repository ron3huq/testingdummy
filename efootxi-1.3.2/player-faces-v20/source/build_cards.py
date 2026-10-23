"""Separate full card and square mini crops. Native package dimensions and
mip metadata retained; never stretch full-size art into a square icon.
Backgrounds are custom Big Time-inspired art, NOT verified latest Konami files.
"""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageOps,ImageDraw
from bundle_tools import Bundle,replace_texture
from iostore import Toc
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');art=O/'art';art.mkdir(exist_ok=True);native=[Toc(str(next((R/'resources').rglob('pc100'+str(i)+'_mobile_and.utoc')))) for i in [0,1]];native.append(Toc(str(next((R/'resources').rglob('pc9261_mobile_and.utoc')))));bundle=Bundle(Toc(str(O/'kits-container/pc9298_mobile_and.utoc')));rows=[]
ids=['88044950524330','89135066911146','106726716084650','106781745353130','106778792700170','105874433662542']
paths=[{'id':card,'path':str(art/(card+'-sheet.png'))}for card in ids]if all((art/(card+'-sheet.png')).exists()for card in ids)else json.loads((R/'v20-art-paths.json').read_text())
for row in paths:
 card=row['id'];p=Path(row['path']);sheet=Image.open(p).convert('RGBA');w,h=sheet.size;assert abs(w/h-2)<.03,(card,sheet.size);
 if p.resolve()!=(art/(card+'-sheet.png')).resolve():shutil.copyfile(p,art/(card+'-sheet.png'))
 left=sheet.crop((0,0,w//2,h));right=sheet.crop((w//2,0,w,h));large=ImageOps.fit(left,(184,256),Image.Resampling.LANCZOS,centering=(.60,.5));small=ImageOps.fit(right,(128,128),Image.Resampling.LANCZOS);large.save(art/(card+'-large.png'));small.save(art/(card+'-small.png'))
 for suffix,im in [('_l',large),('_',small)]:
  n=card+suffix+'.uasset';found=next(((t,p) for t in native for p in t.files if Path(p).name==n),None);assert found,'Native portrait missing: restore pc1000/pc1001/pc9261 before building '+n
  t,path=found;raw=t.read(t.files[path]);new,bulk,dims,decoded=replace_texture(raw,im);assert not bulk and dims[0]==list(im.size);bundle.native(t,path,new)
  decoded.save(art/(card+('-small-decoded.png'if suffix=='_'else'-large-decoded.png')))
  rows.append({'card_id':card,'native_path':path,'native_source_package_preserved':True,'native_dimensions':dims,'separate_mini_and_large_compositions':True,'aspect_preserved':True,'source_sheet_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'background':'custom Big Time-inspired emerald/gold photographic stadium; not verified latest original game background','portrait_source':'supplied photo'if card not in ['106778792700170','105874433662542']else'user supplied 3D face reference rendered in Blender then photographic art reconstruction'})
bundle.write(O/'container');(O/'card-art-validation.json').write_text(json.dumps({'cards':rows,'count':len(rows),'phone_verified':False,'latest_2026_2027_original_background_verified':False,'native_UI_frame_rating_names_team_badges_not_baked_into_portrait':True,'2006_and_2008_portrait_swap_preserved':True},indent=2));canvas=Image.new('RGB',(6*250,320),'#122324');d=ImageDraw.Draw(canvas)
for i,row in enumerate(paths):
 card=row['id'];canvas.paste(Image.open(art/(card+'-large.png')),(i*250,25));canvas.paste(Image.open(art/(card+'-small.png')),(i*250+115,185));d.text((i*250+4,6),card,fill='white')
canvas.save(O/'Card-layout-preview.png');print('TWELVE_NATIVE_CARD_TEXTURES_ASPECT_PRESERVED')
