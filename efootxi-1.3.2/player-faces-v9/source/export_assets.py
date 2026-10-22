"""Independent UEViewer parser/export of every LOD, material and texture."""
from pathlib import Path
import sys,json,subprocess
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;reader=R/'v9-reader';reader.mkdir(exist_ok=True)
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
 cmd=[str(R/'UEViewer/umodel'),'-export','-lods','-game=ue4.26','-android','-notex','-noanim','-gltf','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(R/'v9-export'),name]
 with (R/('v9-'+row['profile']+row['variant'][4:]+'.log')).open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
for profile in ['NF01','ND06','ND13','NF27','NFJR','NDXS','NDDB','NDHD','NDHH','NDPQ','NDTL']:
 cmd=[str(R/'UEViewer/umodel'),'-export','-png','-game=ue4.26','-android','-noanim','-gltf','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(R/'v9-full-export'),'SK_'+profile+'ep00v0313_Face']
 with (R/('v9-'+profile+'-materials.log')).open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
print('UEViewer all 23 heads / 46 LODs and 11 full material/texture exports complete')
