from pathlib import Path
import json,numpy as np
from PIL import Image
R=Path(__file__).parent;V=R/'v2';targets=json.loads((V/'targets.json').read_text());common_eye=Image.open(R/'android-source/105577812455608/eye_sclera_bsm.png').convert('RGB')
def atlas(skin,eye):
 skin=skin.convert('RGB');a=np.array(skin);background=tuple(np.round(a[300:900,200:820].mean(axis=(0,1))).astype('uint8'));out=Image.new('RGB',(2048,2048),background)
 for y in [0,1024]:
  out.paste(skin,(0,y));out.paste(skin.crop((0,0,64,1024)),(1024,y));out.paste(skin.crop((960,0,1024,1024)),(1984,y))
 eye=eye.convert('RGB').resize((768,768));gutter=np.pad(np.array(eye),((64,64),(64,64),(0,0)),mode='wrap');out.paste(Image.fromarray(gutter),(1088,0));return out
report={}
for card in targets:
 folder=V/card;g=json.loads((folder/'game_geometry.json').read_text());before=[r['p'].copy()for r in g['face']];face_uv_before=[r['uv'].copy()for r in g['face'][:g['original_skin_count']]]
 for eye in g['eyes']:
  cx,cy,cz=eye['center']
  for row in g['face'][eye['start']:eye['start']+eye['count']]:
   u=float(np.clip(.5+(row['p'][0]-cx)/.022,.015,.985));v=float(np.clip(.5+(row['p'][2]-cz)/.022,.015,.985));row['uv']=[(1152+u*768)/2048,1-(64+(1-v)*768)/2048]
 assert before==[r['p']for r in g['face']];assert face_uv_before==[r['uv']for r in g['face'][:g['original_skin_count']]];(folder/'game_geometry.json').write_text(json.dumps(g))
 skin=Image.open(R/'android-source'/card/'face_bsm_alp.png').convert('RGB');d=atlas(skin,common_eye);d.save(folder/'face-atlas-2048.png');d.save(folder/'face-D-atlas-2048.png');assert np.array_equal(np.array(d)[:1024,:1024],np.array(skin))
 for which,color in [('N',(128,128,255)),('SRO',(128,40,0))]:
  p=folder/('face-'+which+'-atlas-2048.png');src=Image.open(p).crop((0,0,1024,1024));atlas(src,Image.new('RGB',(768,768),color)).save(p)
 report[card]={'face_pixels_original_1024_square_bit_identical':True,'face_positions_and_uv_unchanged_by_gutter_fix':True,'horizontal_repeat_gutter_pixels':64,'eye_texture_tile':[1152,64,768,768],'all_three_map_layouts_match':True}
(V/'gutter-validation.json').write_text(json.dumps(report,indent=2));print('GUTTERS_READY')
