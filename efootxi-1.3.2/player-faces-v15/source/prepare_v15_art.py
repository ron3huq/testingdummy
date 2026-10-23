"""Split generated two-layout sheets, then encode using aspect-preserving crops.
This performs asset formatting only; backgrounds and portrait edits were imagegen.
"""
from pathlib import Path
import json,shutil
from PIL import Image,ImageOps
out=Path(__file__).resolve().parent.parent
rows=[] if len(list((out/'art').glob('*-sheet.png')))==11 else json.loads(Path('/workspace/ronaldo-work/v15-art-paths.json').read_text())
for row in rows:shutil.copyfile(row['path'],out/'art'/(row['id']+'-sheet.png'))
report=[]
for p in sorted((out/'art').glob('*-sheet.png')):
 im=Image.open(p).convert('RGB');w,h=im.size;assert abs(w/h-2)<.03
 left=im.crop((0,0,w//2,h));right=im.crop((w//2,0,w,h))
 # crop 2-3pxcenter divider only; same square perspective retained
 left=left.crop((0,0,min(left.width,h),h));right=right.crop((max(0,right.width-h),0,right.width,h))
 card=p.stem.split('-')[0]
 ImageOps.fit(left,(184,256),Image.Resampling.LANCZOS,centering=(.5,.5)).save(out/'art'/(card+'-large.png'))
 ImageOps.fit(right,(128,128),Image.Resampling.LANCZOS).save(out/'art'/(card+'-small.png'))
 report.append({'card_id':card,'sheet':p.name,'large_size':[184,256],'small_size':[128,128],'uniform_scale_and_crop':True,'stretch':False,'single_person_each_layout':True})
(out/'art/layouts.json').write_text(json.dumps(report,indent=2))
print('Prepared',len(report),'independent card-layout pairs')
