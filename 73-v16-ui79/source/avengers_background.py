from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math,random
P=Path('/tmp/73-ui79/art');W,H=736,1024;im=Image.new('RGB',(W,H));p=im.load()
for y in range(H):
 for x in range(W):
  glow=max(0,1-math.hypot((x-W*.5)/(W*.8),(y-H*.35)/(H*.65)));p[x,y]=(int(5+12*glow),int(12+30*glow),int(24+45*glow))
d=ImageDraw.Draw(im);random.seed(79)
for _ in range(90):
 x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,2]);d.ellipse((x-r,y-r,x+r,y+r),fill=(67,91,111))
# Hand-built, restrained city/circuit composition. Source faces are composited later without regeneration.
for i in range(21):
 x=i*37;h=random.randrange(50,210);d.rectangle((x,H-h-42,x+30,H-42),fill=(8,17,29));
 for y in range(H-h-35,H-50,18):d.rectangle((x+8,y,x+12,y+4),fill=(30,56,69))
layer=Image.new('RGBA',im.size);q=ImageDraw.Draw(layer);q.ellipse((132,126,604,598),outline=(144,180,193,72),width=13);q.polygon([(277,545),(376,166),(475,545),(426,545),(402,447),(330,447),(307,545)],fill=(144,180,193,68));q.polygon([(343,397),(389,397),(367,296)],fill=(7,18,31,255));q.polygon([(311,417),(520,389),(503,425),(306,452)],fill=(144,180,193,68));im=Image.alpha_composite(im.convert('RGBA'),layer);d=ImageDraw.Draw(im)
# Thin double frame leaves the face unobscured; bottom label stays below the head region.
d.rounded_rectangle((13,13,W-14,H-14),radius=24,outline=(170,139,84,255),width=4);d.rounded_rectangle((27,27,W-28,H-28),radius=17,outline=(67,92,114,255),width=2)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',34);label='AVENGERS';box=d.textbbox((0,0),label,font=font);d.text(((W-(box[2]-box[0]))/2,H-66),label,font=font,fill=(207,190,145))
im.save(P/'avengers-background.png');print('BACKGROUND_READY')
