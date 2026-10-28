exec(open('/workspace/ronaldo-work/73-ui75/inspect_wire.py').read().split('import my_league')[0])
from pathlib import Path
import sys,struct
P=Path('/workspace/73-ui712');T=P/'build/apk/assets/gateway-release/work/tools';sys.path.insert(0,str(T));sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
import photo_codec as p
from iostore import Toc
import cityhash
for text in [b'',b'abc',b'x'*80]:assert p.cityhash.CityHash64(text)==cityhash.CityHash64(text)
photos={'88044950524330':[bytes([30,90,200,255])*(128*128),bytes([200,70,30,255])*(184*256)]}
p.create(P/'photo-codec-test/livedata',photos);t=Toc(str(P/'photo-codec-test/livedata/pc9311_mobile_and.utoc'))
for path,i in t.files.items():
 raw=t.read(i);at=raw.rfind(b'PF_B8G8R8A8\0')+12+8;_,_,n,_,off=struct.unpack_from('<IIIIq',raw,at);w,h,_=struct.unpack_from('<III',raw,at+24+n);assert n==w*h*4;assert raw[at+24:at+28]in[bytes([30,90,200,255]),bytes([200,70,30,255])]
print('PHOTO_CODEC_CITYHASH_ROUNDTRIP_OK')
