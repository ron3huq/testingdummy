from pathlib import Path
import struct,json,hashlib,sys
import texture2ddecoder
from PIL import Image
from zen_clone import rename
r=Path(__file__).parent;base='/Game/Assets/character/RealFace/';k=(r/'pc-face-1024.ktx').read_bytes();h=struct.unpack_from('<13I',k,12);assert h[4]==0x9274 and h[6:8]==(1024,1024) and h[11]==11
at=64+h[12];mips=[]
for i in range(11):n=struct.unpack_from('<I',k,at)[0];at+=4;mips.append(k[at:at+n]);at=(at+n+3)&~3
assert [len(m) for m in mips]==[max(4,1024>>i)**2//2 for i in range(11)]
old=(r/'reference/T_133157_Face_D.uasset').read_bytes();f=struct.unpack_from('<16I',old);em=f[11];delta=f[13]+f[14]-struct.unpack_from('<Q',old,em)[0];start=old.find(struct.pack('<III',256,256,1),800);assert start>800
pre_end=1060+delta-4;assert start+36==pre_end;pre=bytearray(old[:pre_end]);struct.pack_into('<II',pre,start,1024,1024);struct.pack_into('<I',pre,pre_end-4,11)
body=bytearray();bulk=bytearray()
for i,data in enumerate(mips):
 body+=struct.pack('<I',1);virtual=len(pre)+len(body)-delta
 if 1024>>i>64:body+=struct.pack('<IIIq',66817,len(data),len(data),len(bulk));bulk+=data
 else:body+=struct.pack('<IIIq',72,len(data),len(data),virtual+20)+data
 dim=max(4,1024>>i);body+=struct.pack('<III',dim,dim,1)
raw=pre+body+old[-12:];struct.pack_into('<Q',raw,start-8,len(pre)+len(body)+4-delta);struct.pack_into('<Q',raw,em+8,struct.unpack_from('<Q',old,em+8)[0]+len(raw)-len(old))
for v in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 name='T_'+v.replace('4522','ND01',1)+'_Face_D';tex=rename(raw,{base+'T_133157_Face_D':base+name,'T_133157_Face_D':name},base+'T_133157_Face_D',base+name);(r/'asset'/(name+'.uasset')).write_bytes(tex);(r/'asset'/(name+'.ubulk')).write_bytes(bulk)
 # Head native face material references remain original: the existing engine texture callback
 # assigns T_ND01...Face_D using the unchanged original material parameter names.
 mesh=r/'asset'/('SK_'+v.replace('4522','ND01',1)+'_Face.uasset');rep={};imports={}
 for q in ['HQ','MQ']:
  a=base+'MI_'+v+'_Head_Hair_'+q;b=base+'MI_ND0001_Head_Hair_'+q;rep[a]=b;rep[a.rsplit('/',1)[-1]]=b.rsplit('/',1)[-1];imports[a]=b
 mesh.write_bytes(rename(mesh.read_bytes(),rep,imports=imports))
data=texture2ddecoder.decode_etc2(mips[0],1024,1024);im=Image.frombytes('RGBA',(1024,1024),data,'raw','BGRA');im.save(r/'pc-face-ETC2-decoded.png')
(r/'face-texture-validation.json').write_text(json.dumps({'size':[1024,1024],'format':'PF_ETC2_RGB','variants':4,'mip_sizes':[len(x) for x in mips],'external_bulk_bytes':len(bulk),'native_texture_loader_callback_preserved':True,'engine_material_assignment_not_phone_verified':True},indent=2));print('four private PC-color Face_D textures built')
