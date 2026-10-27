from pathlib import Path
import shutil,json
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');S=P/'android-spiderman-original-neck-v6';heads=[('hulk','ND01','ND0001','53878485695166'),('orc','ND02','ND0002','70379213169392'),('ronaldo','ND03','ND0003','89135066911146'),('joker','ND04','ND0004','106783087647748'),('naruto','ND05','ND0005','106783356083208')]
(R/'targets.json').write_text(json.dumps({k:{'prefix':a,'material_prefix':b,'card_id':c}for k,a,b,c in heads},indent=2))
for kind,prefix,mi,card in heads:
 N=P/('android-five-'+kind);N.mkdir(exist_ok=True)
 for name in ['build_pc_head.py','build_face_textures.py','build_materials.py','zen_clone.py']:
  path=(P/'android-ronaldo-v2-final'/name)if kind=='ronaldo'and name!='build_materials.py'else S/name
  s=path.read_text().replace('ND0001',mi).replace('ND01',prefix).replace('88044950524330',card)
  if kind=='ronaldo':
   s=s.replace('/workspace/analysis/ronaldo-v2-final-native/game_geometry.json',str(R/'ronaldo/game_geometry.json'))
   s=s.replace("'native_743_vertex_face_used':False", "'native_743_vertex_face_used':True").replace("'source_pc_skin_positions_unchanged':True", "'source_pc_skin_positions_unchanged':False,'source_2006_surface_projection':True").replace("'source_pc_uv0_unchanged':True", "'source_pc_uv0_unchanged':False,'original_native_uv0_bytes_preserved':True").replace("'facial_controls':'named jaw/eyelids retained; unsupported fine controls reduced explicitly'", "'facial_controls':'original native face weights, vertex order and shader flags retained'")
  else:s=s.replace('/workspace/analysis/spiderman-original-neck-v6/native_geometry.json',str(R/kind/'native_geometry.json')).replace('Ronaldo 2006 mesh0 and lower throat, source weights explicitly retargeted','Ronaldo 2006 actual source neck, upper overlap fitted to supplied head').replace('sk_head 1.0; no jaw/lip animation applied to rigid mask','fixed head expression; native neck blend')
  (N/name).write_text(s)
 for folder in ['reference','material-reference']:
  if not (N/folder).exists():shutil.copytree(S/folder,N/folder)
 (N/'asset').mkdir(exist_ok=True)
print('FIVE_COOK_ROOTS_READY')
