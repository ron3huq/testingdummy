from pathlib import Path
import sys,libarchive
out=Path(__file__).resolve().parent.parent;arc=Path(sys.argv[1]) if len(sys.argv)>1 else out/'original-inputs/Card.rar';dest=out/'card-inputs';dest.mkdir(exist_ok=True)
with libarchive.file_reader(str(arc)) as entries:
 for e in entries:
  if e.isdir:continue
  assert e.isfile and Path(e.pathname).suffix.lower()=='.png'
  p=dest/Path(e.pathname).name
  with p.open('wb') as f:
   for block in e.get_blocks():f.write(block)
print('Card PNG data extracted; no archive instructions executed')
