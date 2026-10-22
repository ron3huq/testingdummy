from pathlib import Path
import sys,struct,json,hashlib,math
import texture2ddecoder
from PIL import Image
from zen_clone import rename,pid
r=Path(__file__).resolve().parent;ref=r/'material-reference';out=r/'asset';base='/Game/Assets/character/RealFace/'
ktx=(r/'noodle-mask-256.ktx').read_bytes();assert ktx[:12]==b'\xabKTX 11\xbb\r\n\x1a\n';header=struct.unpack_from('<13I',ktx,12);assert header[0]==0x04030201 and header[4]==0x9278
at=64+header[12];mips=[]
for i in range(header[11]):
 n=struct.unpack_from('<I',ktx,at)[0];at+=4;mips.append(ktx[at:at+n]);at=(at+n+3)&~3
assert [len(m) for m in mips]==[65536,16384,4096,1024,256,64,16,16,16]
texold='T_133157_Hair_High_D';texnew='T_ND0001_Hair_D';texpath=base+texnew
tex=bytearray((ref/(texold+'.uasset')).read_bytes());f=struct.unpack_from('<16I',tex);delta=f[13]+f[14]-struct.unpack_from('<Q',tex,f[11])[0];assert delta==-180
starts=[1072,1108,1144,5276,6336,6628,6728,6780,6832];newbulk=bytearray()
for i,(start,payload) in enumerate(zip(starts,mips)):
 raw=start+delta;flags,count,size,off=struct.unpack_from('<IIIq',tex,raw);assert count==len(payload)==size
 if i<2:
  assert off==len(newbulk);newbulk.extend(payload)
 else:
  assert off==start+20;tex[raw+20:raw+20+len(payload)]=payload
tex=rename(tex,{base+texold:texpath,texold:texnew},base+texold,texpath);(out/(texnew+'.uasset')).write_bytes(tex);(out/(texnew+'.ubulk')).write_bytes(newbulk)
# Both shader quality variants deliberately use the existing single-layer MQ shader.
# This preserves the supplied alpha silhouette; FOX's second color layer is not emulated.
oldmat='MI_133157_Head_Hair_MQ';matbytes=(ref/(oldmat+'.uasset')).read_bytes();oldtexpath=base+'T_133157_Hair_D'
materials={};remaps={}
for quality in ['HQ','MQ']:
 name='MI_ND0001_Head_Hair_'+quality;path=base+name
 repl={base+oldmat:path,oldmat:name,oldtexpath:texpath,'T_133157_Hair_D':texnew}
 body=rename(matbytes,repl,base+oldmat,path,{oldtexpath:texpath});(out/(name+'.uasset')).write_bytes(body);materials[name]={'template':oldmat,'texture_import_remap':{oldtexpath:texpath},'shader':'M_Head_Hair_MQ'}
 remaps[base+'MI_4522_Head_Hair_'+quality]=path
for variant in ['4522','4522lg00v0000','4522ep01v0291','4522ep00v0313']:
 meshfile=out/('SK_'+variant.replace('4522','ND01',1)+'_Face.uasset');mesh=meshfile.read_bytes();repl={};vremaps={}
 for quality in ['HQ','MQ']:
  old=base+'MI_'+variant+'_Head_Hair_'+quality;new=base+'MI_ND0001_Head_Hair_'+quality
  vremaps[old]=new;repl[old]=new;repl[old.rsplit('/',1)[-1]]=new.rsplit('/',1)[-1]
 mesh=rename(mesh,repl,imports=vremaps);meshfile.write_bytes(mesh)
# Decode the exact ETC2 bytes destined for Android, not a PNG stand-in.
rgba=texture2ddecoder.decode_etc2a8(mips[0],256,256);decoded=Image.frombytes('RGBA',(256,256),rgba,'raw','BGRA');decoded.save(r/'noodle-mask-ETC2-decoded.png');original=Image.open(r/'noodle-mask-256.png').convert('RGBA')
a=list(original.getchannel('A').getdata());z=list(decoded.getchannel('A').getdata());mae=sum(abs(x-y) for x,y in zip(a,z))/len(a);assert mae<4
report={'texture':texnew,'material_templates':materials,'head_import_remap':remaps,'format':'PF_ETC2_RGBA','mips':[len(x) for x in mips],'alpha_mae':mae,'shader_limitation':'Single-layer masked Android hair shader; no FOX UV1 color blend/blonde tips port','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}}
(r/'material-build.json').write_text(json.dumps(report,indent=2));print('Android ETC2 texture and two private material instances built. Alpha MAE',mae)
