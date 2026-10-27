from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np,math,random,json
P=Path('/tmp/73-ui710');A=P/'art';A.mkdir(exist_ok=True);rows=[]
def background(kind):
 W,H=736,1024;im=Image.new('RGB',(W,H));a=np.zeros((H,W,3),dtype='uint8');yy,xx=np.mgrid[:H,:W];glow=np.clip(1-np.hypot((xx-368)/620,(yy-310)/820),0,1)
 base={'naruto':(7,16,37),'orc':(17,14,12),'spider':(5,11,28)}[kind];accent={'naruto':(84,51,13),'orc':(53,33,18),'spider':(26,23,54)}[kind]
 for c in range(3):a[:,:,c]=base[c]+glow*accent[c]
 im=Image.fromarray(a).convert('RGBA');d=ImageDraw.Draw(im);color={'naruto':(237,155,52,255),'orc':(166,122,68,255),'spider':(175,55,61,255)}[kind]
 d.rounded_rectangle((13,13,W-14,H-14),22,outline=color,width=5);d.rounded_rectangle((28,28,W-29,H-29),16,outline=(86,99,119,255),width=2)
 if kind=='spider':
  cx,cy=368,430
  for angle in range(0,360,30):
   t=math.radians(angle);d.line((cx,cy,cx+1200*math.cos(t),cy+1200*math.sin(t)),fill=(61,53,76,255),width=2)
  for r in [130,245,360,475,590]:d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(70,45,62,255),width=2)
 elif kind=='naruto':
  for r in [180,230,280]:d.arc((368-r,350-r,368+r,350+r),20,320,fill=(129,99,58,255),width=5)
 else:
  random.seed(710)
  for j in range(45):
   x=random.randrange(50,686);y=random.randrange(80,930);d.line((x,y,x+random.randrange(-55,55),y+random.randrange(10,100)),fill=(70,51,35,255),width=2)
 random.seed(10)
 for i in range(25):
  x=i*31;h=random.randrange(50,160);d.rectangle((x,958-h,x+24,958),fill=(8,14,24,255))
 return im
settings=[('105804908868664','NARUTO','naruto',(130,190,620,895),(175,212,580,716)),('105873896755947','ORC','orc',(120,175,632,940),(165,205,590,702)),('105647605587130','SPIDER-MAN','spider',(158,211,582,745),(176,223,563,692)),('106754901843130','HULK','orc',(52,210,686,815),(77,218,658,688))]
for pid,name,kind,bustbox,headbox in settings:
 f=A/(pid+'-render.png')
 if not f.exists():f=Path('/tmp/73-ui79/art')/(pid+'-render.png')
 source=Image.open(f).convert('RGBA');cut=source.crop(bustbox);a=np.array(cut);fade=np.clip((cut.height-np.arange(cut.height))/(cut.height*.25),0,1);a[:,:,3]=(a[:,:,3].astype('float32')*fade[:,None]).astype('uint8');cut=Image.fromarray(a)
 foreground=Image.new('RGBA',(736,1024));fit=ImageOps.contain(cut,(630,710),Image.Resampling.LANCZOS);foreground.alpha_composite(fit,((736-fit.width)//2,110));foreground.resize((184,256),Image.Resampling.LANCZOS).save(A/(pid+'-foreground.png'))
 if pid!='106754901843130':
  full=background(kind);full.alpha_composite(foreground);d=ImageDraw.Draw(full);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf',52 if len(name)<9 else 44);box=d.textbbox((0,0),name,font=font);d.text(((736-(box[2]-box[0]))//2,846),name,font=font,fill=(231,218,186));d.line((144,925,592,925),fill=(117,119,119),width=2);full.save(A/(pid+'-card-master.png'));full.resize((184,256),Image.Resampling.LANCZOS).save(A/(pid+'-large.png'))
 mini=Image.new('RGBA',(128,128));head=ImageOps.contain(source.crop(headbox),(120,120),Image.Resampling.LANCZOS);mini.alpha_composite(head,((128-head.width)//2,2));mini.save(A/(pid+'-small.png'));rows.append({'id':pid,'name':name,'source':'supplied native face mesh, offline CPU render','generated_AI_photo':False,'large_size':[184,256],'mini_size':[128,128],'uniform_scale':True,'native_background_uses_transparent_foreground':True})
preview=Image.new('RGB',(3*368,670),'#101c2c');d=ImageDraw.Draw(preview)
for i,(pid,name,*_)in enumerate(settings[:3]):
 im=Image.open(A/(pid+'-large.png')).resize((368,512));preview.paste(im,(i*368,0));mini=Image.open(A/(pid+'-small.png'));preview.paste(mini,(i*368+120,530),mini);d.text((i*368+100,653),pid,fill='white')
preview.save(A/'cards-preview.jpg');(P/'card-art-layouts.json').write_text(json.dumps(rows,indent=2));print('THREE_REDESIGNED_CARDS_AND_FOUR_TRANSPARENT_BG_VARIANTS_READY')
