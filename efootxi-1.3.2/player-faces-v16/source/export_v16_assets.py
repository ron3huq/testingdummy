from pathlib import Path
import subprocess,json
r=Path('/workspace/ronaldo-work');out=Path('/workspace/testingdummy/efootxi-1.3.2/player-faces-v16');reader=r/'v16-reader';reader.mkdir(exist_ok=True)
for old in (r/'v15-reader').iterdir():
 if not old.name.startswith('pc9298'):
  dest=reader/old.name
  if not dest.exists():dest.symlink_to(old.resolve())
for ext in ['pak','ucas','utoc']:
 p=reader/('pc9298_mobile_and.'+ext)
 if not p.exists():p.symlink_to(out/'container'/p.name)
report=json.loads((out/'card-art-validation.json').read_text());names=[Path(row['path']).stem for row in report['cards']];logs=out/'reader-logs';logs.mkdir(exist_ok=True)
for name in names:
 with (logs/(name+'.log')).open('w') as f:
  subprocess.run([str(r/'UEViewer/umodel'),'-export','-png','-gltf','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(r/'v16-verified'),name],stdout=f,stderr=subprocess.STDOUT,check=True)
print('Independent UEViewer exports',len(names))
