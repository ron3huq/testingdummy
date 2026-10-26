from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
p=0x30010000
for ix in [47,48]:
 for v in [0,40,130,140,180,220,250,255,256,300,350,511]:
  call(0x82a907c,p,ix,v);print(ix,v,get(p,ix))
