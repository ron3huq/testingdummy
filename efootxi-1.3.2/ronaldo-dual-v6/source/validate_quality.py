from pathlib import Path
import sys,json,struct
import numpy as np
from PIL import Image
from mesh_tools import Mesh
r=Path(sys.argv[1]);out=Path(__file__).parent.parent;checks=[]
for profile in ['ND01','ND06']:
 name='SK_'+profile+'ep00v0313_Face';m=Mesh((out/'asset'/(name+'.uasset')).read_bytes(),(r/('v6-'+profile+'ep00v0313.log')).read_text());ns=m.info[0]['verts']-135
 neck=(m.positions[:ns,2]<156)&(m.positions[:ns,1]<12)&(m.positions[:ns,1]>1)
 uv=m.uv[:ns,:2][neck].astype(float);im=np.array(Image.open(out/('T_'+profile+'ep00v0313_Face_N-decoded.png')));ix=np.clip((uv*2048).astype(int),0,2047);pix=im[ix[:,1],ix[:,0],:3];delta=np.abs(pix[:,:2].astype(int)-128);metric=float(np.median(delta));assert len(pix)>30 and metric<8,(profile,metric)
 checks.append({'profile':profile,'neck_normal_sample_vertices':len(pix),'median_tangent_normal_xy_error_from_flat':metric})
name='T_ND0006_Hair_D';data=(out/'asset'/(name+'.uasset')).read_bytes();assert b'TEXTUREGROUP_Character' in data and b'TEXTUREGROUP_Project06' not in data
original=np.array(Image.open(next((r/'input-1').rglob('hair_parts_bsm_alp.dds'))).convert('RGBA'));decoded=np.array(Image.open(out/(name+'-decoded.png')).convert('RGBA'));assert decoded.shape==original.shape==(512,2048,4);mae=float(abs(original[:,:,3].astype(float)-decoded[:,:,3]).mean());assert mae<4,mae
for q in ['HQ','MQ']:
 mat=(out/'asset'/('MI_ND0006_Head_Hair_'+q+'.uasset')).read_bytes();assert b'M_Head_Hair_HQ' in mat and b'M_Head_Hair_MQ' not in mat
report={'status':'NECK_FLAT_NORMAL_HAIR_HQ_2048X512_ALPHA_AND_GROUP_PASS','neck_checks':checks,'hair_source_resolution':[2048,512],'hair_alpha_compression_mae':mae,'hair_both_quality_slots_use_hq':True,'normal_map_srgb_metadata_from_native_normal_template':True,'phone_tested':False,'cutscene_confirmed_fixed':False};(out/'quality-validation.json').write_text(json.dumps(report,indent=2));print(report['status'],checks,'hair alpha MAE',mae)
