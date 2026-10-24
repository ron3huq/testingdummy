from pathlib import Path
import sys,struct,json,hashlib
import numpy as np
from PIL import Image
from iostore import Toc
from bundle_tools import Bundle,replace_texture,decode_first_texture
from mesh_tools import Mesh,write_native_lods,platform_lod_properties
from shading_tools import repair_frame
from zen_clone import rename,pid
O=Path(__file__).resolve().parent.parent;R=Path('/workspace/ronaldo-work');P=R/'v25';BASE='/Game/Assets/character/RealFace/';old=Toc(str(O.parent/'player-faces-v24/container/pc9298_mobile_and.utoc'));bundle=Bundle(old);a=np.load(P/'export.npz');rows=[]
def read(n,e='uasset'):return old.read(old.files['character/RealFace/'+n+'.'+e])
def put(n,b,t,imports=None,e='uasset'):
 pk=int.from_bytes(old.ids[old.files['character/RealFace/'+t+'.uasset']][:8],'little');fixed,im=bundle.entries[pk];entry=(fixed,[(imports or {}).get(k,k)for k in im])if e=='uasset'else None
 bundle.put('character/RealFace/'+n+'.'+e,struct.pack('<Q',pid(BASE+n))+b'\0\0\0'+(b'\2'if e=='uasset'else b'\3'),b,entry)
def restore_rgb_untouched(raw,bulk,newraw,newbulk,oldimage,newimage):
 # Preserve every old EAC alpha block and all unchanged/accessory RGB blocks.
 b=bytearray(newraw);ub=bytearray(newbulk);alpha=raw.rfind(b'PF_ETC2_RGBA\0')>raw.rfind(b'PF_ETC2_RGB\0');fmt=b'PF_ETC2_RGBA\0'if alpha else b'PF_ETC2_RGB\0';p=raw.rfind(fmt);assert p>0;bs=16 if alpha else 8;at=p+len(fmt);first,count=struct.unpack_from('<II',raw,at);at+=8;stats=[]
 for level in range(count):
  cooked,flags,n,size,off=struct.unpack_from('<IIIIq',raw,at);at+=24;ext=bool(flags&0x100);dw,dh,d=struct.unpack_from('<III',raw,at if ext else at+n);w=max(4,dw);h=max(4,dh);oldpayload=bulk[off:off+n]if ext else raw[at:at+n];payload=bytearray(ub[off:off+n]if ext else b[at:at+n]);before=np.array(oldimage.resize((w,h),Image.Resampling.LANCZOS));after=np.array(newimage.resize((w,h),Image.Resampling.LANCZOS));mask=np.any(before[:,:,:3]!=after[:,:,:3],2);kept=edited=0
  for by in range(h//4):
   for bx in range(w//4):
    k=(by*(w//4)+bx)*bs;allowed=bx*4+4<=dw//2 and by*4+4<=dh//2
    if not allowed or not mask[by*4:by*4+4,bx*4:bx*4+4].any():payload[k:k+bs]=oldpayload[k:k+bs];kept+=1
    else:
     if alpha:payload[k:k+8]=oldpayload[k:k+8]
     edited+=1
  if alpha:assert all(payload[k:k+8]==oldpayload[k:k+8]for k in range(0,n,16))
  if ext:ub[off:off+n]=payload
  else:b[at:at+n]=payload
  stats.append({'mip':level,'unchanged_rgb_blocks_retained':kept,'edited_skin_rgb_blocks':edited,'all_original_alpha_blocks_exact':True});at+=(0 if ext else n)+12
 return bytes(b),bytes(ub),stats
for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
 t='SK_ND06'+suffix+'_Face';raw=read(t);log=(O.parent/'player-faces-v20/references/ND06'/('v10-ND06'+suffix+'.log')).read_text();m=Mesh(raw,log,0);native=Mesh(raw,log,1);ns=m.info[0]['verts'];pc=ns-135;assert pc==2369 and np.array_equal(m.indices[:len(a['skin_tri'])],a['skin_tri']);assert np.max(abs(m.uv[:pc,:2]*2-a['skin_uv']))<.0005
 skinpos=m.positions[:ns].copy();skinpos[:pc]+=a['skin_delta'];skin_tn=m.tangents[:ns].copy();J=a['skin_jac'];assert np.linalg.det(J).min()>.5
 for i,jac in enumerate(J):
  if np.max(abs(jac-np.eye(3)))<1e-6:continue
  values=skin_tn[i].view('i1').astype(float)/127;n=np.linalg.inv(jac).T@values[4:7];n/=np.linalg.norm(n);tg=jac@values[:3];tg-=n*np.dot(tg,n);tg/=np.linalg.norm(tg);skin_tn[i,:3]=np.rint(tg*127).astype('i1').view('u1');skin_tn[i,4:7]=np.rint(n*127).astype('i1').view('u1')
 hp=a['hairpos'].astype('<f4');hu=a['hairuv'];ht=a['hairtri'].astype('<u2');hn=a['hairnormal'];tn=np.zeros((len(hp),8),dtype='i1');tn[:,0]=127;tn[:,3]=127;tn[:,4:7]=np.rint(hn*127).astype('i1');tn[:,7]=127;tn=repair_frame(hp,tn.view('u1'),hu,ht,derive=True)
 pp=np.concatenate([skinpos,hp]);tans=np.concatenate([skin_tn,tn]);uvs=np.concatenate([m.uv[:ns],np.c_[hu,np.full((len(hu),2),3.0517578125e-5)].astype('<f2')]);cols=np.concatenate([m.colors[:ns],np.full((len(hp),4),255,dtype='u1')]);tri=np.concatenate([m.indices[:m.info[0]['tris']],ht+ns]);weights=[dict(row)for row in m.global_weights(0)]
 built=write_native_lods(native,native,pp,tans,uvs,weights,cols,tri,ns,m.info[0]['tris'],list(range(16)),lod1_rows=[dict(r)for r in native.global_weights(0)])
 name='SK_NV17'+suffix+'_Face';kind='FaceUpcon'if suffix=='lg00v0000'else'FaceLegacy';imports={BASE+'MI_ND0006_Head_Hair_'+q:BASE+'MI_NVH1_Head_Hair_'+q for q in ['HQ','MQ']};imports.update({BASE+'MI_ND06'+suffix+'_Head_'+kind+'_'+q:BASE+'MI_NV17'+suffix+'_Head_'+kind+'_'+q for q in ['HQ','MQ']});rep={BASE+t:BASE+name,t:name}
 for k,v in imports.items():rep[k]=v;rep[k.split('/')[-1]]=v.split('/')[-1]
 built=rename(built,rep,BASE+t,BASE+name,imports=imports);built,_=platform_lod_properties(built,True);put(name,built,t,{pid(k):pid(v)for k,v in imports.items()})
 alphastats=[]
 for ch in ['D','N','SRO']:
  tx='T_ND06'+suffix+'_Face_'+ch;nt='T_NV17'+suffix+'_Face_'+ch;rr=read(tx);bulk=read(tx,'ubulk')
  if ch=='D':
   before=decode_first_texture(rr,bulk);img=np.array(before);assert img.shape[:2]==(2048,2048);base=np.array(Image.open(P/'base_skin.png').convert('RGB')).astype('i2');origin=img[:1024,:1024,:3].astype('i2');merged=origin.copy()
   for part,file in [('cap','2017_Scalp_SeamMatched_BAKED.png'),('face','2017_Face_Temples_Clean_BAKED.png')]:
    mask=np.array(Image.open(P/(part+'-coverage.png')))>0;src=np.array(Image.open(R/'hair-repair-v3/2017'/file).convert('RGB')).astype('i2');delta=src-base;delta[np.max(abs(delta),axis=2)<=1]=0;merged[mask]=origin[mask]+delta[mask]
   img[:1024,:1024,:3]=np.clip(merged,0,255).astype('u1');target=Image.fromarray(img);nr,nb,_,_=replace_texture(rr,target,bulk,preserve_alpha=b'PF_ETC2_RGBA\0'in rr);rr,bulk,alphastats=restore_rgb_untouched(rr,bulk,nr,nb,before,target)
   after=decode_first_texture(rr,bulk);assert np.array_equal(np.array(before)[:,:,3],np.array(after)[:,:,3]);after.save(P/('native-face-'+(suffix or 'plain')+'.png'))
  # N and SRO including bulk stay exactly the working ND06 payload.
  rr=rename(rr,{BASE+tx:BASE+nt,tx:nt},BASE+tx,BASE+nt);put(nt,rr,tx);put(nt,bulk,tx,e='ubulk')
 for q in ['HQ','MQ']:
  mt='MI_ND06'+suffix+'_Head_'+kind+'_'+q;nm='MI_NV17'+suffix+'_Head_'+kind+'_'+q;im={BASE+'T_ND06'+suffix+'_Face_'+c:BASE+'T_NV17'+suffix+'_Face_'+c for c in ['D','N','SRO']};rep={BASE+mt:BASE+nm,mt:nm}
  for k,v in im.items():rep[k]=v;rep[k.split('/')[-1]]=v.split('/')[-1]
  put(nm,rename(read(mt),rep,BASE+mt,BASE+nm,imports=im),mt,{pid(k):pid(v)for k,v in im.items()})
 rows.append({'profile':'NV17'+suffix,'skin_vertices':ns,'hair_vertices':len(hp),'skin_weights_uv_triangles_native_accessories_unchanged':True,'source_sculpt_delta_applied':True,'max_sculpt_cm':float(np.linalg.norm(a['skin_delta'],axis=1).max()),'native166_153_skeleton_unchanged':True,'original_face_alpha_normal_SRO_preserved':True,'mip_rgb_and_alpha_retention':alphastats})
t='T_ND0006_Hair_D';n='T_NVH1_Hair_D';raw,bulk,_,decoded=replace_texture(read(t),Image.open(P/'hair-mobile-atlas.png'),read(t,'ubulk'));decoded.save(P/'hair-native-readback.png');raw=rename(raw,{BASE+t:BASE+n,t:n},BASE+t,BASE+n);put(n,raw,t);put(n,bulk,t,e='ubulk')
for q in ['HQ','MQ']:
 t='MI_ND0006_Head_Hair_'+q;n='MI_NVH1_Head_Hair_'+q;im={BASE+'T_ND0006_Hair_D':BASE+'T_NVH1_Hair_D'};rep={BASE+t:BASE+n,t:n,BASE+'T_ND0006_Hair_D':BASE+'T_NVH1_Hair_D','T_ND0006_Hair_D':'T_NVH1_Hair_D'};put(n,rename(read(t),rep,BASE+t,BASE+n,imports=im),t,{pid(k):pid(v)for k,v in im.items()})
bundle.write(O/'container');(O/'head-build.json').write_text(json.dumps({'status':'V25_TARGET_2017_BUILT_NOT_DEVICE_VERIFIED','changed_card_id':'88044950524330','base':'phone-proven ND06 native materials/skeleton/skin topology','heads':rows,'all_old_v24_chunks_retained_byte_exact':True,'device_verified':False},indent=2));print('V25_FOUR_NATIVE_VARIANTS_BUILT')
