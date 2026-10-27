from pathlib import Path
import sys,json,struct,subprocess,shutil
from PIL import Image
import texture2ddecoder
R=Path(__file__).parent;V=R/'v2';P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');which=sys.argv[1];targets=json.loads((V/'targets.json').read_text());etc=P/'Etc2Comp/build/EtcTool/EtcTool';size=2048;nmips=12
for card,row in targets.items():
 C=P/('android-r5-v2-'+card);sys.path.insert(0,str(C));from zen_clone import rename
 image=V/card/('face-'+which+'-atlas-2048.png');ktx=V/card/('final-'+which+'.ktx');subprocess.run(list(map(str,[etc,image,'-format','RGB8','-effort','15','-mipmaps',12,'-jobs','4','-output',ktx])),check=True)
 data=ktx.read_bytes();h=struct.unpack_from('<13I',data,12);assert h[4]==0x9274 and h[6:8]==(2048,2048)and h[11]==12;at=64+h[12];mips=[]
 for i in range(12):n=struct.unpack_from('<I',data,at)[0];at+=4;mips.append(data[at:at+n]);at=(at+n+3)&~3
 name='T_133157_Face_'+which;ref=(C/'reference'/('T_133157_Face_D.uasset'))if which=='D'else V/'texture-reference'/(name+'.uasset');b=ref.read_bytes();f=struct.unpack_from('<16I',b);em=f[11];delta=f[13]+f[14]-struct.unpack_from('<Q',b,em)[0];start=b.find(struct.pack('<III',256 if which=='D'else 128,256 if which=='D'else 128,1),800);assert start>800;pre=bytearray(b[:start+36]);struct.pack_into('<II',pre,start,2048,2048);struct.pack_into('<I',pre,len(pre)-4,12);body=bytearray();bulk=bytearray()
 for i,mip in enumerate(mips):
  body+=struct.pack('<I',1);virtual=len(pre)+len(body)-delta
  if 2048>>i>64:body+=struct.pack('<IIIq',66817,len(mip),len(mip),len(bulk));bulk+=mip
  else:body+=struct.pack('<IIIq',72,len(mip),len(mip),virtual+20)+mip
  dim=max(4,2048>>i);body+=struct.pack('<III',dim,dim,1)
 raw=pre+body+b[-12:];struct.pack_into('<Q',raw,start-8,len(pre)+len(body)+4-delta);struct.pack_into('<Q',raw,em+8,struct.unpack_from('<Q',b,em+8)[0]+len(raw)-len(b));base='/Game/Assets/character/RealFace/'
 for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
  newname='T_'+row['prefix']+suffix+'_Face_'+which;asset=rename(raw,{base+name:base+newname,name:newname},base+name,base+newname);(C/'asset'/(newname+'.uasset')).write_bytes(asset);(C/'asset'/(newname+'.ubulk')).write_bytes(bulk)
 decoded=Image.frombytes('RGBA',(2048,2048),texture2ddecoder.decode_etc2(mips[0],2048,2048),'raw','BGRA');decoded.save(V/card/('face-'+which+'-ETC2-decoded.png'))
 if which=='D':decoded.save(C/'pc-face-ETC2-decoded.png');shutil.copyfile(ktx,C/'pc-face-2048.ktx')
 (V/card/('final-texture-'+which+'-validation.json')).write_text(json.dumps({'mips':12,'base_size':2048,'gutter':64,'source_photo_pixels_unchanged_before_compression':which=='D','native_sampler_srgb':which=='D','variants':4,'phone_tested':False},indent=2));print('FINAL_TEXTURE_READY',which,card,flush=True)
