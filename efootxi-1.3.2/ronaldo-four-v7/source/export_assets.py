"""Independent UEViewer parser/export of every LOD, material and texture."""
from pathlib import Path
import sys,json,subprocess
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;reader=R/'v7-reader';reader.mkdir(exist_ok=True)
for p in (R/'reader-input').iterdir():
 if p.name.startswith('pc9298'):continue
 dest=reader/p.name
 if not dest.exists():dest.symlink_to(p.resolve())
for p in (out/'container').iterdir():
 dest=reader/p.name
 if dest.is_symlink():dest.unlink()
 if not dest.exists():dest.symlink_to(p.resolve())
for row in json.loads((out/'build-report.json').read_text())['meshes']:
 name='SK_'+row['profile']+row['variant'][4:]+'_Face'
 cmd=[str(R/'UEViewer/umodel'),'-export','-lods','-game=ue4.26','-android','-notex','-noanim','-gltf','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(R/'v7-export'),name]
 with (R/('v7-'+row['profile']+row['variant'][4:]+'.log')).open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
for profile in ['ND01','ND06','ND13','ND27']:
 cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-gltf','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(R/'v7-full-export'),'SK_'+profile+'ep00v0313_Face']
 with (R/('v7-'+profile+'-materials.log')).open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
print('UEViewer all 16 heads / 32 LODs and 4 full material/texture exports complete')
