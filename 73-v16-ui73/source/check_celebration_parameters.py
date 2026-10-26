from pathlib import Path
exec(Path('/workspace/ronaldo-work/73-ui6/test_native.py').read_text().split('import sys,sqlite3')[0])
p=0x30010000;out=[]
for ix,values in[(59,[0,16,22,90,94,212,219,349,511,542,571,595]),(60,[0,90,127,542,571,595])]:
 for v in values:
  returned=call(0x82a907c,p,ix,v);actual=get(p,ix);out.append({'parameter':ix,'requested':v,'native_setter_return':returned,'readback':actual})
  if v<=(511 if ix==59 else 127):assert actual==v
Path('/workspace/ronaldo-work/73-ui73/celebration-parameters-validation.json').write_text(json.dumps({'passed':True,'original73_native_accessors':True,'synthetic_record':True,'rows':out,'device_tested':False},indent=2));print(out)
