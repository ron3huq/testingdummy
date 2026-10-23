from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageChops
from iostore import Toc
root=Path(__file__).resolve().parent.parent
old=Toc(str(root.parent/'player-faces-v18/container/pc9298_mobile_and.utoc'));new=Toc(str(root/'container/pc9298_mobile_and.utoc'))
for p,i in old.files.items():assert p in new.files and old.read(i)==new.read(new.files[p])
expected={'character/Uniform/LowTextures/T_u0351'+slot+'_Uni_D.uasset' for slot in ['p1','p2']};assert set(new.files)-set(old.files)==expected
reader=Path('/workspace/ronaldo-work/v19-reader');exports=Path('/workspace/ronaldo-work/v19-research/verified-kit');logs=root/'reader-logs';logs.mkdir(exist_ok=True)
for slot in ['p1','p2']:
 name='T_u0351'+slot+'_Uni_D'
 cmd=['/workspace/ronaldo-work/UEViewer/umodel','-export','-png','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(reader),'-out='+str(exports),name]
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(logs/(name+'.log')).write_text(p.stdout);assert p.returncode==0 and 'Exporting Texture2D '+name in p.stdout
 independent=Image.open(next(exports.rglob(name+'.png'))).convert('RGBA');ours=Image.open(root/'kit-previews'/('Sparta351-'+slot+'-ETC2.png')).convert('RGBA');assert independent.size==ours.size==(1024,1024);assert ImageChops.difference(independent,ours).getbbox() is None
report={'status':'V19_ALL299_PRIOR_ASSET_CHUNKS_IDENTICAL_TWO_SPARTA_TEXTURES_INDEPENDENT_READBACK_PASS','unchanged_v18_chunks':len(old.files),'new_uniform_chunks':len(expected),'Sparta_team_id':351,'all_prior_heads_hair_LODs_weights_materials_and_card_art_byte_identical':True,'independent_ETC2_readback_pixel_match':True,'native_uniform_mip_layout':'one1024x1024 level per native template; no invalid source small FTEX mip reused','container_sha256':hashlib.sha256((root/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest(),'kit_engine_shader_UV_application_verified':False,'renderer_black_face_fix_verified':False,'phone_tested':False};(root/'asset-validation.json').write_text(json.dumps(report,indent=2));print(report['status'])
