from pathlib import Path
import sys,struct,json,zlib,base64,hashlib
import numpy as np,texture2ddecoder
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle
from zen_clone import rename,pid
P=Path('/tmp/73-ui79');toc=Toc(str(next(Path('/workspace/ronaldo-work/resources').rglob('pc0102_mobile_and.utoc'))));header=parse_header(toc.read(next(i for i,x in enumerate(toc.ids)if x[11]==10)));out={'schema':1,'header':base64.b64encode(toc.raw[:toc.hs]).decode(),'pak':base64.b64encode(Path('/workspace/ronaldo-work/73-ui7/carry/livedata/pc9298_mobile_and.pak').read_bytes()).decode(),'slots':{},'source':{}};proof=[];sample=Bundle(toc);sample.files={};sample.entries={};prefix='MaterialLibrary/Character/Body/CommonTextures/';B='/Game/Assets/'+prefix
for part,stem in [('Skin','T_Sk1_Skin_D'),('Body','T_Base_Body_D'),('Lowbody','T_Base_Lowbody_D')]:
 key='Assets/'+prefix+stem+'.uasset';raw=toc.read(toc.files[key]);bulk=toc.read(toc.files[key[:-7]+'.ubulk']);f=struct.unpack_from('<16I',raw);em=f[11];serialoff,serialsize=struct.unpack_from('<QQ',raw,em);actual=f[13]+f[14];alpha=raw.rfind(b'PF_ETC2_RGBA\0')>raw.rfind(b'PF_ETC2_RGB\0');fmt=b'PF_ETC2_RGBA\0'if alpha else b'PF_ETC2_RGB\0';a=raw.rfind(fmt);at=a+len(fmt);first,count=struct.unpack_from('<II',raw,at);at+=8;assert first==0;levels=[]
 for i in range(count):
  cooked,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;external=bool(flags&256);w,h,d=struct.unpack_from('<III',raw,at if external else at+n);src=bulk[offset:offset+n]if external else raw[at:at+n];assert len(src)==n
  dec=(texture2ddecoder.decode_etc2a8 if alpha else texture2ddecoder.decode_etc2)(src,max(4,w),max(4,h));image=np.frombuffer(dec,dtype='u1').reshape(max(4,h),max(4,w),4)
  if i==0:basew,baseh=w,h
  dw,dh=max(1,basew>>i),max(1,baseh>>i);image=image[:dh,:dw].copy();levels.append((dw,dh,image.tobytes()));at+=(0 if external else n)+12
 # Rebuild serialized platform payload, retaining original UTexture properties and using native uncompressed BGRA.
 newfmt=b'PF_B8G8R8A8\0';pre=bytearray(raw[:a-4])+struct.pack('<I',len(newfmt))+newfmt+struct.pack('<II',0,count);spans=[];sources=[]
 for dw,dh,data in levels:
  pos=len(pre)+24;size=dw*dh*4;pre+=struct.pack('<IIIIq',1,0x48,size,size,serialoff+pos-actual);spans.append([pos,size,dw,dh]);pre+=bytes(size)+struct.pack('<III',dw,dh,1);sources.append(data)
 pre+=raw[at:];delta=len(pre)-len(raw);struct.pack_into('<Q',pre,em+8,serialsize+delta)
 # Cooked skip pointer is a virtual archive offset, independent of IoStore name-map layout.
 skips=[]
 for j in range(actual,a-4-7):
  if struct.unpack_from('<Q',raw,j)[0]==serialoff+serialsize-8:struct.pack_into('<Q',pre,j,serialoff+serialsize+delta-8);skips.append(j)
 assert len(skips)==1,(stem,skips)
 # Change the name-map's pixel-format token too; this shifts the serialized bytes but not virtual offsets.
 renamed=rename(bytes(pre),{fmt[:-1].decode():'PF_B8G8R8A8'});shift=len(renamed)-len(pre);spans=[[p+shift,n,w,h]for p,n,w,h in spans]
 source=b''.join(sources);img=np.frombuffer(sources[0],dtype='u1').reshape(baseh,basew,4);b,g,r=img[:,:,0],img[:,:,1],img[:,:,2];lum=(r.astype('u4')*54+g.astype('u4')*183+b.astype('u4')*19)>>8;mask=(r>=g)&(g>=b)&(lum>30)&(img[:,:,3]>0);reference=max(1,int(np.median(lum[mask] if mask.any()else lum)))
 out['source'][part]={'pixels':base64.b64encode(zlib.compress(source,9)).decode(),'reference':reference,'sizes':[len(x)for x in sources]}
 pk=int.from_bytes(toc.ids[toc.files[key]][:8],'little');fixed,deps=store_entry(header['store'],header['pids'].index(pk))
 for slot in range(1,65):
  name=f'T_C79{slot:04d}_{part}_D';nr=rename(renamed,{stem:name,B+stem:B+name},B+stem,B+name);s2=len(nr)-len(renamed);slots=[[p+s2,n,w,h]for p,n,w,h in spans];idb=struct.pack('<Q',pid(B+name))+b'\0\0\0\2';out['slots'].setdefault(str(slot),{})[part]={'path':prefix+name+'.uasset','id':idb.hex(),'fixed':base64.b64encode(fixed).decode(),'imports':deps,'data':base64.b64encode(zlib.compress(nr,9)).decode(),'spans':slots}
  if slot==1:
   v=bytearray(nr);off=0
   for pos,n,w,h in slots:
    pixels=np.frombuffer(source[off:off+n],dtype='u1').reshape(-1,4).copy();Y=(pixels[:,2].astype('u4')*54+pixels[:,1].astype('u4')*183+pixels[:,0].astype('u4')*19)>>8
    for chan,target in [(0,55),(1,91),(2,78)]:pixels[:,chan]=np.minimum(255,(Y*target+reference//2)//reference)
    v[pos:pos+n]=pixels.tobytes();off+=n
   sample.put(prefix+name+'.uasset',idb,v,(fixed,deps))
 proof.append({'part':part,'base_size':[basew,baseh],'mips':len(levels),'source_alpha_preserved':True,'reference_luminance':reference,'pixel_format':'PF_B8G8R8A8','all_inline_mips':True,'native_virtual_offsets_rebuilt':True})
encoded=json.dumps(out,separators=(',',':')).encode();dest=P/'build/payload/work/tools/skin_templates.zlib';dest.write_bytes(zlib.compress(encoded,9));sample.write(P/'skin-sample/livedata');(P/'skin-template-validation.json').write_text(json.dumps({'built':True,'slots':64,'templates':proof,'template_bytes':dest.stat().st_size,'phone_tested':False},indent=2));print('BUILT_SKIN_TEMPLATES',dest.stat().st_size,proof)
