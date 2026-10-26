from pathlib import Path
import sys,struct,json,hashlib,math
import numpy as np
import texture2ddecoder
from PIL import Image
from zen_clone import rename,pid
r=Path(__file__).parent;ref=r/'material-reference';out=r/'asset';base='/Game/Assets/character/RealFace/'
ktx=(r/'noodle-color-atlas-2048.ktx').read_bytes();assert ktx[:12]==b'\xabKTX 11\xbb\r\n\x1a\n';h=struct.unpack_from('<13I',ktx,12);assert h[0]==0x04030201 and h[4]==0x9278 and h[6:8]==(2048,2048) and h[11]==12
at=64+h[12];mips=[]
for i in range(h[11]):
 n=struct.unpack_from('<I',ktx,at)[0];at+=4;mips.append(ktx[at:at+n]);at=(at+n+3)&~3
assert [len(x) for x in mips]==[max(4,2048>>i)**2 for i in range(12)]
texold='T_133157_Hair_High_D';texnew='T_ND0001_Hair_D';texpath=base+texnew
old=(ref/(texold+'.uasset')).read_bytes();f=struct.unpack_from('<16I',old);em=f[11];delta=f[13]+f[14]-struct.unpack_from('<Q',old,em)[0];assert delta==-180
# Rebuild the platform-data mip array: large mips stay in an IoStore bulk chunk.
start=851;assert struct.unpack_from('<III',old,start)==(256,256,1)
assert struct.unpack_from('<II',old,880)==(0,9)
pre=bytearray(old[:888]);struct.pack_into('<II',pre,start,2048,2048);struct.pack_into('<I',pre,884,len(mips));raw=bytearray();bulk=bytearray()
for i,data in enumerate(mips):
 raw+=struct.pack('<I',1);cooked_bulk_at=len(pre)+len(raw)-delta
 if max(1,2048>>i)>64:
  raw+=struct.pack('<IIIq',66817,len(data),len(data),len(bulk));bulk+=data
 else:
  raw+=struct.pack('<IIIq',72,len(data),len(data),cooked_bulk_at+20)+data
 dim=max(4,2048>>i);raw+=struct.pack('<III',dim,dim,1)
# Template footer: non-virtual marker followed by final None pixel-format FName.
assert old[-12:-8]==b'\0'*4
tex=pre+raw+old[-12:];struct.pack_into('<Q',tex,843,len(pre)+len(raw)+4-delta)
struct.pack_into('<Q',tex,em+8,struct.unpack_from('<Q',old,em+8)[0]+len(tex)-len(old))
tex=rename(tex,{base+texold:texpath,texold:texnew},base+texold,texpath);(out/(texnew+'.uasset')).write_bytes(tex);(out/(texnew+'.ubulk')).write_bytes(bulk)
oldmat='MI_133157_Head_Hair_MQ';matbytes=(ref/(oldmat+'.uasset')).read_bytes();oldtexpath=base+'T_133157_Hair_D'
for quality in ['HQ','MQ']:
 name='MI_ND0001_Head_Hair_'+quality;path=base+name
 repl={base+oldmat:path,oldmat:name,oldtexpath:texpath,'T_133157_Hair_D':texnew}
 (out/(name+'.uasset')).write_bytes(rename(matbytes,repl,base+oldmat,path,{oldtexpath:texpath}))
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 meshfile=out/('SK_'+variant.replace('4522','ND01',1)+'_Face.uasset');repl={};imports={}
 for q in ['HQ','MQ']:
  old=base+'MI_'+variant+'_Head_Hair_'+q;new=base+'MI_ND0001_Head_Hair_'+q;imports[old]=new;repl[old]=new;repl[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1]
 meshfile.write_bytes(rename(meshfile.read_bytes(),repl,imports=imports))
rgba=texture2ddecoder.decode_etc2a8(mips[0],2048,2048);decoded=Image.frombytes('RGBA',(2048,2048),rgba,'raw','BGRA');decoded.save(r/'atlas-ETC2-decoded.png');a=np.array(Image.open(r/'noodle-color-atlas-2048.png').convert('RGBA'),dtype=float);z=np.array(decoded,dtype=float);alpha_mae=float(np.abs(a[:,:,3]-z[:,:,3]).mean());mask=a[:,:,3]>128;rgb_mae=float(np.abs(a[:,:,:3]-z[:,:,:3])[mask].mean());assert alpha_mae<4 and rgb_mae<12
report={'texture':texnew,'format':'PF_ETC2_RGBA','size':[2048,2048],'mips':[len(x) for x in mips],'bulk_bytes':len(bulk),'alpha_mae':alpha_mae,'visible_rgb_mae':rgb_mae,'source_color_and_alpha_baked':True,'shader':'existing M_Head_Hair_MQ; no new shader permutation','phone_tested':False}
(r/'material-build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
