from pathlib import Path
import sys,struct,json,zlib,base64
P=Path('/workspace/73-ui712');S=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');T=P/'build/apk/assets/gateway-release/work/tools';sys.path.insert(0,str(S))
from iostore import Toc,parse_header,store_entry
from zen_clone import rename
base=Toc(str(T.parent.parent/'livedata/pc9306_mobile_and.utoc'))
head=parse_header(base.read(next(i for i,x in enumerate(base.ids)if x[11]==10)))
rows=[]
for suffix in ['_','_l']:
 path=next(p for p in base.files if p.endswith('/U79_88044950524330'+suffix+'.uasset'));i=base.files[path];raw=base.read(i);f=struct.unpack_from('<16I',raw);fmt=b'PF_ETC2_RGBA\0';at=raw.rfind(fmt);p=at+len(fmt)+8;c,flags,n,size,off=struct.unpack_from('<IIIIq',raw,p);w,h,d=struct.unpack_from('<III',raw,p+24+n);assert c==1 and not(flags&0x100)and n==size
 newfmt=b'PF_B8G8R8A8\0';pixels=bytes(w*h*4);data=bytearray(raw[:at-4]+struct.pack('<I',len(newfmt))+newfmt+raw[at+len(fmt):p]+struct.pack('<IIIIq',c,flags,len(pixels),len(pixels),off-1)+pixels+raw[p+24+n:]);struct.pack_into('<Q',data,f[11]+8,struct.unpack_from('<Q',raw,f[11]+8)[0]+len(data)-len(raw));struct.pack_into('<Q',data,at-24,struct.unpack_from('<Q',raw,at-24)[0]+len(data)-len(raw));old='U79_88044950524330'+suffix;new='U712_00000000000000'+suffix;own='/Game/Assets/'+path[:-7];dest=own.replace(old,new);data=rename(data,{old:new,own:dest,'PF_ETC2_RGBA':'PF_B8G8R8A8'},own,dest)
 pixel=data.rfind(newfmt)+len(newfmt)+8+24
 assert data[pixel:pixel+len(pixels)]==pixels
 fixed,imports=store_entry(head['store'],head['pids'].index(int.from_bytes(base.ids[i][:8],'little')))
 rows.append(dict(path=dest,old=new,w=w,h=h,pixel=pixel,data=base64.b64encode(data).decode(),fixed=base64.b64encode(fixed).decode(),imports=imports))
meta={'rows':rows,'header':base64.b64encode(base.raw[:base.hs]).decode(),'pak':base64.b64encode(Path(base.path[:-5]+'.pak').read_bytes()).decode()};(T/'photo_templates.zlib').write_bytes(zlib.compress(json.dumps(meta).encode(),9))
# Portable writer: original verified container algorithm; runtime stdlib and original protected CityHash only.
rename_src=(S/'zen_clone.py').read_text().split('MASK=')[1];rename_src='ENTRY=16\nMASK='+rename_src
io=(S/'iostore.py').read_text();func=io[io.index('def build_store'):io.index('\ndef main()')]
writer=(S/'bundle_tools.py').read_text();writer=writer[writer.index('class Bundle:'):writer.index('\ndef replace_texture')];writer=writer.replace("name='pc9298_mobile_and'","name='pc9311_mobile_and'").replace('zlib.compress(raw,9)','zlib.compress(raw,3)');writer=writer[:writer.index('  t=Toc(')]+"  return out\n"
code='''"""Runtime photograph IoStore writer. No network, external encoder or trial code."""\nfrom pathlib import Path\nimport struct,hashlib,zlib,shutil,base64,json,types\nclass cityhash:\n @staticmethod\n def CityHash64(value):\n  from diy_iostore import city64\n  return city64(value)\ndef wstr(s):\n b=s.encode('latin1')+b'\\0';return struct.pack('<i',len(b))+b\n'''+rename_src+'\n'+func+'\n'+writer+'''
def templates():return json.loads(zlib.decompress(Path(__file__).with_name('photo_templates.zlib').read_bytes()))
def create(out,photos):
 Path(out).mkdir(parents=True,exist_ok=True)\n doc=templates();header=base64.b64decode(doc['header']);pak=Path(out).parent/'empty-photo.pak';pak.write_bytes(base64.b64decode(doc['pak']))
 obj=Bundle.__new__(Bundle);obj.base=types.SimpleNamespace(raw=header,hs=len(header),path=str(pak)[:-4]+'.utoc');obj.files={};obj.entries={}
 for card,images in sorted(photos.items()):
  for row,image in zip(doc['rows'],images):
   raw=bytearray(base64.b64decode(row['data']));n=row['w']*row['h']*4
   if len(image)!=n:raise ValueError('Portrait dimensions mismatch')
   raw[row['pixel']:row['pixel']+n]=image;old=row['old'];new='U712_'+card+('_l'if old.endswith('_l')else'_');own=row['path'];dest=own.replace(old,new);data=rename(raw,{old:new,own:dest},own,dest);key=pid(dest);path=dest.split('/Game/Assets/',1)[1]+'.uasset';obj.put(path,struct.pack('<Q',key)+b'\\0\\0\\0\\2',data,(base64.b64decode(row['fixed']),row['imports']))
 obj.write(out);pak.unlink()
'''
# Remove Bundle methods using external Toc; constructor/native unused but names harmless.
(T/'photo_codec.py').write_text(code);print('PHOTO_TEMPLATE',[(x['w'],x['h'])for x in rows],(T/'photo_templates.zlib').stat().st_size)
