from pathlib import Path
import sys,mmap,numpy as np
sys.path.insert(0,'/workspace/ronaldo-work/73-ui75');from native_dis import read,dis
f=open('/workspace/ronaldo-work/73-inspect/v16-meta/lib/arm64-v8a/libUE4.so','rb');b=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ);a=np.frombuffer(b,dtype='<u4');hits=np.flatnonzero((a&0xfc000000)==0x94000000);vals=a[hits]&0x3ffffff;rel=vals.astype(np.int64);rel[rel>=0x2000000]-=0x4000000;targets=(hits.astype(np.int64)*4+0x4000+rel*4)
for target in [0x68d2b4c,0x68d2d64,0x68d288c]:
 addrs=(hits[targets==target]*4+0x4000).tolist();print(hex(target),[hex(x)for x in addrs])
 for addr in addrs[:6]:print(dis(addr-24,48))
