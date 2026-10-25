from pathlib import Path
import sys,json
from PIL import Image
sys.path.insert(0,'/workspace/ronaldo-work/pes-fmdl-blender/pes-fmdl');from Ftex import ftexToDds
p=Path('/workspace/ronaldo-work/73-ui4/ferguson');out=p/'blender-textures'
def convert(root,stem):
 f=next((p/root).rglob(stem+'.ftex'));dest=out/(root+'-'+stem+'.dds');assert ftexToDds(str(f),str(dest));png=dest.with_suffix('.png');Image.open(dest).save(png);return png
base=Image.open(convert('fer','face_bsm')).convert('RGBA');mask=Image.open(convert('65342','face_bsm_alp')).convert('RGBA');base=base.resize(mask.size);Image.alpha_composite(base,mask).save(out/'composited-skin.png')
hair=convert('65342','hair_parts_bsm_alp');shell=out/'65342-face_bsm_alp.png'
d=json.loads((p/'blender-model.json').read_text())
for r in d['meshes']:
 if r['material']=='fox_skin_mat':r['texture']=str(out/'composited-skin.png')
 elif r['material']=='fox_hair_mat':r['texture']=str(hair)
 elif r['material']=='fox_head_shell_mat':r['texture']=str(shell)
(p/'blender-model.json').write_text(json.dumps(d))
print('Source material namespaces resolved, skin mask composited over base')
