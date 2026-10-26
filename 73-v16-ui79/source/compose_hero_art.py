"""Assemble self-made hero cards from exact supplied 3D heads, preserving aspect ratio."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import numpy as np,json
P=Path('/tmp/73-ui79');A=P/'art';rows=[]
settings=[('106754901843130','HULK',(52,210,686,815),(77,218,658,688)),('105647605587130','SPIDER-MAN',(158,211,582,745),(176,223,563,692))]
for pid,name,bustbox,headbox in settings:
 source=Image.open(A/(pid+'-render.png')).convert('RGBA');cut=source.crop(bustbox);a=np.array(cut);h=cut.height;fade=np.clip((h-np.arange(h))/(h*.28),0,1);a[:,:,3]=(a[:,:,3].astype('float32')*fade[:,None]).astype('uint8');cut=Image.fromarray(a)
 bg=Image.open(A/'avengers-background.png').convert('RGBA');fit=ImageOps.contain(cut,(654,700),Image.Resampling.LANCZOS);pos=((736-fit.width)//2,135);bg.alpha_composite(fit,pos)
 # Restrained custom title on the full card, outside the head and eye area.
 draw=ImageDraw.Draw(bg);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',54 if name=='HULK'else 44);bounds=draw.textbbox((0,0),name,font=font);draw.text(((736-(bounds[2]-bounds[0]))//2,846),name,font=font,fill=(226,214,178));draw.line((151,919,585,919),fill=(107,132,153),width=2)
 bg.save(A/(pid+'-card-master.png'));bg.resize((184,256),Image.Resampling.LANCZOS).save(A/(pid+'-large.png'))
 head=source.crop(headbox);mini=Image.new('RGBA',(128,128));fitmini=ImageOps.contain(head,(120,120),Image.Resampling.LANCZOS);mini.alpha_composite(fitmini,((128-fitmini.width)//2,2));mini.save(A/(pid+'-small.png'))
 rows.append({'card_id':pid,'name':name,'large':[184,256],'miniface':[128,128],'large_source_crop':bustbox,'mini_source_crop':headbox,'source':'User-supplied 3D face mesh rendered in Blender, self-created card artwork authorized by user','face_geometry_regenerated':False,'uniform_scale':True,'face_texture_source_unchanged':True,'background':'Hand-built Avengers graphic; no downloaded photograph'})
proof=Image.new('RGB',(2*368,670),'#0e1a29');d=ImageDraw.Draw(proof)
for i,(pid,name,_,__)in enumerate(settings):
 im=Image.open(A/(pid+'-large.png')).resize((368,512),Image.Resampling.NEAREST);proof.paste(im,(i*368,0));mini=Image.open(A/(pid+'-small.png'));proof.paste(mini,(i*368+120,525),mini);d.text((i*368+116,651),pid,fill='white')
proof.save(A/'hero-cards-preview.png');(P/'hero-card-layouts.json').write_text(json.dumps(rows,indent=2));print('HERO_CARD_ART_READY',len(rows))
