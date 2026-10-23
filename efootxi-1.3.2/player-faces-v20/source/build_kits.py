"""Exact-team native kit atlases, native glyph-color-only edits and UI thumbnails.
No font shape, native glyph dimensions, name text, number or geometry edits.
Thumbnail projection is a separate technical PES-atlas to native UI conversion.
"""
from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageFilter
from bundle_tools import Bundle,replace_texture
from iostore import Toc
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');base=Toc(str(O/'heads-container/pc9298_mobile_and.utoc'));bundle=Bundle(base)
def native(n):return Toc(str(next((R/'resources').rglob(n+'_mobile_and.utoc'))))
uni=native('pc0101');fonts=native('pc0103');ui=native('pc1000');dest=O/'kit-previews';dest.mkdir(exist_ok=True);rows=[]
kits=[(351,'Sparta Rotterdam','Real Madrid 2017',O/'references/sparta-inputs/u0109p1_home.png',O/'references/sparta-inputs/u0109p1_third.png',(18,20,25),(240,240,240)),(352,'Telstar','Manchester United 2007',R/'v20-input/mu2007/MU2007_home_p1.png',R/'v20-input/mu2007/MU2007_away_p2.png',(245,245,245),(245,245,245)),(242,'AZ','Real Madrid 2011',R/'v20-input/rm2011/RM2011_home_p1.png',R/'v20-input/rm2011/RM2011_away_p2.png',(20,20,20),(196,163,92)),(245,'sc Heerenveen','Barcelona 2017',R/'v20-input/barca2017/Barca2017_home_p1.png',R/'v20-input/barca2017/Barca2017_second_p2.png',(233,192,49),(17,29,26))]
def project_kit(im,full):
 # Front torso UV panel is the canonical PES2021 lower central atlas island.
 # Use separate polygons for torso, sleeves, shorts and socks; source whole
 # atlas must never be stretched directly into a UI card rectangle.
 W,H=256,1024 if full else 256;buf=np.zeros((H,W,4),dtype='u1');texture=np.array(im.convert('RGBA'));th,tw=texture.shape[:2]
 def quad(xy,uv,shade=True):
  for ids in [(0,1,2),(0,2,3)]:
   a=np.array(xy)[list(ids)];u=np.array(uv)[list(ids)];lo=np.maximum(np.floor(a.min(0)).astype(int),[0,0]);hi=np.minimum(np.ceil(a.max(0)).astype(int),[W-1,H-1]);xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));den=(a[1,1]-a[2,1])*(a[0,0]-a[2,0])+(a[2,0]-a[1,0])*(a[0,1]-a[2,1]);aa=((a[1,1]-a[2,1])*(xx-a[2,0])+(a[2,0]-a[1,0])*(yy-a[2,1]))/den;bb=((a[2,1]-a[0,1])*(xx-a[2,0])+(a[0,0]-a[2,0])*(yy-a[2,1]))/den;cc=1-aa-bb;mask=(aa>=0)&(bb>=0)&(cc>=0);uvv=aa[...,None]*u[0]+bb[...,None]*u[1]+cc[...,None]*u[2];uvv=np.clip(uvv,0,.99999);pix=texture[(uvv[:,:,1]*th).astype(int),(uvv[:,:,0]*tw).astype(int)].copy();light=.78+.22*np.cos((xx-W/2)/(W/2)*1.2);pix[:,:,:3]=(pix[:,:,:3]*light[:,:,None]).astype('u1');pix[:,:,3]=255;buf[lo[1]:hi[1]+1,lo[0]:hi[0]+1][mask]=pix[mask]
 scale=.95 if full else 1.;top=52 if full else 20;bottom=top+(252 if full else 226);x0,x1=64,192
 quad([(x0,top),(x1,top),(183,bottom),(73,bottom)],[(.34,.47),(.66,.47),(.66,.935),(.34,.935)])
 # short sleeves on the atlas upper lateral panels, not pants islands
 quad([(64,top),(34,top+22),(22,top+84),(65,top+95)],[(.18,.38),(.02,.38),(.02,.49),(.18,.49)])
 quad([(192,top),(222,top+22),(234,top+84),(191,top+95)],[(.82,.38),(.98,.38),(.98,.49),(.82,.49)])
 # Collar opening: preserve transparency, small fabric lip follows source kit.
 yy,xx=np.mgrid[:H,:W];hole=((xx-128)/26)**2+((yy-top)/16)**2<1;buf[hole,3]=0
 if full:
  y=bottom+7
  quad([(72,y),(128,y),(124,y+130),(64,y+130)],[(.02,.58),(.25,.58),(.25,.92),(.02,.92)])
  quad([(128,y),(184,y),(192,y+130),(132,y+130)],[(.75,.58),(.98,.58),(.98,.92),(.75,.92)])
  color=np.array(texture[int(.40*th),int(.08*tw),:3]);
  for left in [75,145]:
   for row in range(y+155,y+315):
    width=15-int((row-y-155)/18);buf[row,left-width:left+width,:3]=color;buf[row,left-width:left+width,3]=255
 return Image.fromarray(buf).resize((128,512) if full else (128,128),Image.Resampling.LANCZOS)
for tid,team,label,p1,p2,c1,c2 in kits:
 for ix,src,color in [(0,p1,c1),(1,p2,c2)]:
  slot='p'+str(ix+1);im=Image.open(src).convert('RGBA');path=f'Uniform/LowTextures/T_u{tid:04d}{slot}_Uni_D.uasset';raw=uni.read(uni.files[path]);updated,bulk,dims,decoded=replace_texture(raw,im);assert not bulk;bundle.native(uni,path,updated);decoded.save(dest/(str(tid)+'-'+slot+'-atlas.png'))
  changedfonts=[]
  for kind in ['Name','Back','Chest','Leg']:
   path=f'character/Uniform/LowTextures/T_u{tid:04d}{slot}_Font{kind}_D.uasset';raw=fonts.read(fonts.files[path]);fmt=max(raw.rfind(b'PF_ETC2_RGBA\0'),raw.rfind(b'PF_ETC2_RGB\0'));# Decode native glyphs through reader exports before color substitution.
   png=next((R/'v20-fonts').rglob(Path(path).stem+'.png'),R/'v20-fonts'/(Path(path).stem+'.png'))
   if not png.exists():
    import subprocess
    cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(R/'v19-reader'),'-out='+str(R/'v20-fonts'),Path(path).stem];p=__import__('subprocess').run(cmd,capture_output=True);assert p.returncode==0;png=next((R/'v20-fonts').rglob(Path(path).stem+'.png'))
   glyph=Image.open(png).convert('RGBA');alpha=glyph.getchannel('A');a=np.array(glyph);a[:,:,:3]=color;glyph=Image.fromarray(a);assert glyph.getchannel('A').tobytes()==alpha.tobytes();new,bulk,fdims,_=replace_texture(raw,glyph,preserve_alpha=True);assert not bulk;bundle.native(fonts,path,new);changedfonts.append({'kind':kind,'native_dimensions':fdims,'alpha_geometry_preserved':True,'RGB_only':list(color)})
  previews=[]
  for full in [False,True]:
   name='uni'+str((tid<<14)+ix)+('_full_r' if full else '_r');path='ui/Data/Thumbnail/Uniform/'+name+'.uasset';assert path in ui.files;image=project_kit(im,full);image.save(dest/(name+'.png'));raw=ui.read(ui.files[path]);new,bulk,dd,_=replace_texture(raw,image);assert not bulk;bundle.native(ui,path,new);previews.append({'path':path,'dimensions':dd,'source_atlas_front_projection':True})
  rows.append({'team_id':tid,'team':team,'replacement':label,'slot':slot,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'native_kit_dimensions':dims,'glyph_color_only':changedfonts,'previews':previews,'phone_verified':False})
bundle.write(O/'kits-container');(O/'kit-build.json').write_text(json.dumps({'kits':rows,'team_ids':[351,352,242,245],'glyph_shape_size_and_original_font_preserved':True,'shirt_numbers_and_text_render_resources_not_renamed':True,'phone_verified':False},indent=2));print('BUILT_EIGHT_KITS_16_PREVIEWS_32_GLYPH_COLOR_ASSETS')
