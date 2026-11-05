"""Native ETC2 atlas engineering; preserve untouched compressed blocks/alpha.
Only skin uses native palette ratios; oral cavity and tongue are dark with no specular; teeth are retained.
"""
import struct,numpy as np,etcpak,texture2ddecoder
from PIL import Image,ImageDraw,ImageFilter
from bundle_tools import decode_first_texture
PALETTES=np.array([[174,137,117],[162,120,93],[162,116,85],[138,102,77],[101,74,60],[85,62,52]],float)

def masks(mesh,lab,size):
 out=[];tri=mesh.indices[:mesh.info[0]['tris']];uv=mesh.uv[:,:2].astype(float)
 for which in ['skin','neck','oral']:
  mask=Image.new('L',size);draw=ImageDraw.Draw(mask)
  for face in tri:
   component=int(lab[face[0]]);yes=(component<28 or component==34)if which=='skin' else component==34 if which=='neck' else component in (29,31)
   if yes:draw.polygon([(float(uv[k,0]*size[0]),float(uv[k,1]*size[1]))for k in face],fill=255)
  out.append(mask.filter(ImageFilter.MaxFilter(11)))
 return out

def patch_blocks(raw,bulk,image,mask):
 b=bytearray(raw);bb=bytearray(bulk);p=max(b.rfind(b'PF_ETC2_RGB\0'),b.rfind(b'PF_ETC2_RGBA\0'));assert p>0;alpha=b[p:p+13]==b'PF_ETC2_RGBA\0';fmt=b'PF_ETC2_RGBA\0'if alpha else b'PF_ETC2_RGB\0';at=p+len(fmt);first,count=struct.unpack_from('<II',b,at);assert first==0;at+=8;changed=0;outside=0;checks=[]
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',b,at);at+=24;assert cooked==1 and n==size;external=bool(flags&0x100);dw,dh,d=struct.unpack_from('<III',b,at if external else at+n);assert d==1;w,h=max(dw,4),max(dh,4)
  im=image.resize((w,h),Image.Resampling.LANCZOS).convert('RGBA');ma=np.array(mask.resize((w,h),Image.Resampling.BOX))>0;ma=ma.reshape(h//4,4,w//4,4).any((1,3)).reshape(-1);encoded=(etcpak.compress_etc2_rgba if alpha else etcpak.compress_etc2_rgb)(im.tobytes(),w,h);assert len(encoded)==n
  old=bytes(bb[off:off+n])if external else bytes(b[at:at+n]);new=bytearray(old);step=16 if alpha else 8
  for k,yes in enumerate(ma):
   if yes:new[k*step+(8 if alpha else 0):(k+1)*step]=encoded[k*step+(8 if alpha else 0):(k+1)*step];changed+=1
   else:outside+=1
  if alpha:
   for k in range(0,n,16):assert new[k:k+8]==old[k:k+8]
  if external:bb[off:off+n]=new
  else:b[at:at+n]=new;at+=n
  checks.append([dw,dh]);at+=12
 assert len(b)==len(raw)and len(bb)==len(bulk)
 return bytes(b),bytes(bb),{'changed_blocks':changed,'untouched_blocks_exact':outside,'all_alpha_blocks_exact':True,'mips':checks}

def build_texture(raw,bulk,channel,palette,skin,neck,oral):
 im=decode_first_texture(raw,bulk);a=np.array(im).astype(float);s=np.array(skin)>0;n=np.array(neck)>0;o=np.array(oral)>0
 if channel=='D':
  # The source lower-left neck atlas is pink (167,118,101); its adjoining
  # upper-neck pixels are (160,117,92). Retain the seam, then remove that
  # authored offset progressively over the first 8% of the neck chart.
  gain=PALETTES[palette-1]/PALETTES[1];a[s,:3]*=gain
  yy=np.arange(a.shape[0])[:,None]/a.shape[0];ramp=np.clip((yy-.505)/.04,0,1);correction=np.array([160/167,117/118,92/101]);g=1+ramp[:,:,None]*(correction-1);a[n,:3]*=np.broadcast_to(g,a[:,:,:3].shape)[n]
  a[o,:3]=0
  mask=Image.fromarray(np.uint8((s if palette!=2 else n)|o)*255)
 else:
  assert channel=='SRO';a[o,0]=0;a[o,1]=255;a[o,2]=0;mask=oral
 new=Image.fromarray(np.rint(np.clip(a,0,255)).astype('u1'),'RGBA');return patch_blocks(raw,bulk,new,mask)
