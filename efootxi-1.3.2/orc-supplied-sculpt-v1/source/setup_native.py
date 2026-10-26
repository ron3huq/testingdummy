from pathlib import Path
import shutil
P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');S=P/'android-spiderman-original-neck-v6';R=P/'android-orc-v1';R.mkdir(exist_ok=True)
for name in ['build_pc_head.py','build_face_textures.py','build_materials.py','zen_clone.py']:
 text=(S/name).read_text().replace('/workspace/analysis/spiderman-original-neck-v6/native_geometry.json','/workspace/analysis/orc-source/native_geometry.json')
 if name=='build_pc_head.py':
  text=text.replace("'target_card_id':'88044950524330'", "'target_card_id':None")
  text=text.replace("'neck_source':'Ronaldo 2006 mesh0 and lower throat, source weights explicitly retargeted'", "'neck_source':'supplied Orc sculpt, continuous head-neck-chest skinning'")
  text=text.replace("'mask_weight':'sk_head 1.0; no jaw/lip animation applied to rigid mask'", "'mask_weight':'fixed original sculpt expression; sk_head plus neck/chest blend'")
 (R/name).write_text(text)
for name in ['reference','material-reference']:
 if not (R/name).exists():shutil.copytree(S/name,R/name)
(R/'asset').mkdir(exist_ok=True)
(R/'build_full_container.py').write_bytes((P/'android-hulk-only/build_full_container.py').read_bytes())
