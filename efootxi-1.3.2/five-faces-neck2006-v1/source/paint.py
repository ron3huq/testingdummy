import numpy as np,math

def paint(kind,pos,ids,base):
 p=pos; x=p[:,0];y=p[:,1];z=p[:,2];out=base.copy()
 if kind=='joker':
  x=x+.0047;z=z+.0079
  head=ids==1;front=y<-.105
  out[head]=(.61,.67,.60)
  back=np.clip((y+.13)/.12,0,1);line=(1.776+.015*np.exp(-((abs(x)-.030)/.027)**2)-.025*(abs(x)/.10)**2)*(1-back)+1.671*back
  hair=head&(z>line);ears=(abs(x)>.076)&(z>1.689)&(z<1.739)&(y<-.017);hair&=~ears
  # Muted film green, with fine colour variation on the existing sculpted hair.
  variation=.9+.1*np.sin(x*1100+np.sin(z*400))*np.sin(z*1200+y*100)
  out[hair]=np.column_stack([.025*variation[hair],.105*variation[hair],.038*variation[hair]])
  for sign in [-1,1]:
   cx=sign*.034;dx=x-cx;dz=z-1.7214
   liner=head&front&((dx/.014)**2+(dz/.0035)**2<1);out[liner]=(.009,.012,.011)
   sclera=head&front&((dx/.011)**2+(dz/.0022)**2<1);out[sclera]=(.67,.71,.65)
   iris=sclera&((dx/.0025)**2+(dz/.0025)**2<1);out[iris]=(.045,.09,.075)
   pupil=iris&((dx/.0011)**2+(dz/.0011)**2<1);out[pupil]=(.001,.002,.001)
   glint=iris&((dx+.0010)**2+(dz-.0010)**2<.00065**2);out[glint]=(.9,.9,.9)
   browline=1.739+.006*np.maximum(0,1-(dx/.024)**2)+sign*.04*dx
   brow=head&front&(abs(dx)<.023)&(abs(z-browline)<.0014);out[brow]=(.008,.011,.008)
  smile=1.660+.014*(x/.060)**2;lip=head&(y<-.06)&(abs(x)<.061)&(abs(z-smile)<(.0075-.003*np.minimum(1,abs(x)/.061)));out[lip]=(.34,.007,.014)
  gap=head&(y<-.065)&(abs(x)<.057)&(abs(z-smile)<.00085);out[gap]=(.012,.002,.004)
 elif kind=='naruto':
  y=y-.02
  face=ids==1;hair=ids==2;band=ids==3;mouth=ids==4;eyes=ids==5;front=y<-.16
  out[face]=(.90,.64,.40);out[hair]=(.95,.63,.035);out[band]=(.009,.018,.052);out[mouth]=(.013,.004,.003);out[eyes]=(.78,.80,.73)
  # Forehead plate: new artwork, since the original BODY.PNG was absent.
  X=x/.055;Z=(z-1.750)/.016;plate=band&(y<-.183)&((abs(X)/1.)**8+(abs(Z)/1.)**8<1)
  out[plate]=(.37,.43,.46)
  edge=plate&((abs(X)>.94)|(abs(Z)>.90));out[edge]=(.08,.11,.13)
  for sign in [-1,1]:
   rivet=plate&((x-sign*.045)**2+(z-1.75)**2<.002**2);out[rivet]=(.10,.13,.14)
  # Recognizable leaf spiral with its left stroke, drawn on the existing plate.
  glyph=np.zeros(len(x),dtype=bool)
  for i in range(90):
   t=i/89;a=t*3.5*math.pi;r=.015+.37*t;xx=-.1+r*math.cos(a);zz=r*math.sin(a);glyph|=(X-xx)**2+(Z-zz)**2<.055**2
  for a,b in [((-.39,.25),(-.69,.53)),((-.69,.53),(-.69,-.42)),((-.69,-.42),(-.28,-.39))]:
   vx=b[0]-a[0];vz=b[1]-a[1];t=np.clip(((X-a[0])*vx+(Z-a[1])*vz)/(vx*vx+vz*vz),0,1);glyph|=(X-(a[0]+t*vx))**2+(Z-(a[1]+t*vz))**2<.055**2
  out[plate&glyph]=(.017,.023,.026)
  for sign in [-1,1]:
   side=sign*x
   for i in range(3):
    line=1.691-i*.010+.045*(side-.045)
    whisk=face&front&(side>.026)&(side<.064)&(abs(z-line)<.0007);out[whisk]=(.075,.035,.014)
   # New irises are painted onto the two original eye meshes, not extra spheres.
   dx=x-sign*.031;dz=z-1.714;iris=eyes&(y<-.145)&((dx/.009)**2+(dz/.010)**2<1);out[iris]=(.012,.21,.58)
   rim=iris&((dx/.009)**2+(dz/.010)**2>.75);out[rim]=(.005,.018,.045)
   pupil=iris&((dx/.004)**2+(dz/.005)**2<1);out[pupil]=(.001,.002,.004)
   glint=iris&((dx+.0025)**2+(dz-.0035)**2<.0017**2);out[glint]=(.95,.95,.95)
   liner=face&front&(abs(x-sign*.031)<.021)&(abs(z-(1.723+sign*.13*(x-sign*.031)))<.0011);out[liner]=(.025,.012,.006)
  teeth=mouth&(y<-.164)&(z>1.650)&(z<1.663)&(abs(x)<.029);out[teeth]=(.78,.76,.66)
 return out
