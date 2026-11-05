from pathlib import Path
import struct,json
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
R=Path(__file__).parent
new=load(R/'libnoodle_hair.so',0x39000000);old=load(Path('/workspace/work/full8-rc7/payload/assets/gateway-release/work/tools/libnoodle_hair.so'),0x3a000000)
def txt(p):return bytes(u.mem_read(p,16)).split(b'\0')[0].decode()if p else None
ids=[89138556572074,106654775417922,105756321970183,88042803047215,106782819217056,88035555413452,123]
for skin in range(1,7):
 assert call(0x39101028,skin)==1
 assert txt(call(0x3901a5e8,ids[0]))=='R8A'+str(skin)
 for pid in ids[1:]:assert txt(call(0x3901a5e8,pid))==txt(call(0x3a01a5e8,pid))
for bad in [0,7,255]:assert call(0x39101028,bad)==0
print('PASS six startup head palette selectors; full ID scope; other profiles unchanged; no phone test.')
