from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
import csv
b=Path('/workspace/ronaldo-work/73-ui6/Player-decoded.bin').read_bytes();p=0x30010000;source=0x30011000;out={}
for off in range(0,len(b),400):
 row=b[off:off+400];pid=struct.unpack_from('<Q',row,8)[0];u.mem_write(source,row);call(0x82aa124,p,source,0)
 for ix in [59,60]:
  value=get(p,ix);k=(ix,value)
  if k not in out or (int(out[k]['card_id'])<2**40 and pid>=2**40):out[k]={'parameter':ix,'celebration_id':value,'card_id':str(pid)}
 if off==0:print('FIRST',out,flush=True)
pth=Path('/workspace/ronaldo-work/73-ui76')
with (pth/'celebration-card-map.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['parameter','celebration_id','card_id']);w.writeheader();w.writerows(out[k]for k in sorted(out))
(pth/'celebration-scan.json').write_text(json.dumps({'passed':True,'raw_records_imported_by_original73_82aa124':len(b)//400,'original_native_getter':True,'distinct_mappings':len(out),'scope':'Source table values59/60, distinct from animation clip IDs. One source card per value. Not on-pitch motion verification.'},indent=2));print('SCAN_COMPLETE',len(out),flush=True)
