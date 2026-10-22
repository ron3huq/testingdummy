import hashlib
from pathlib import Path
import sys,json,re
import numpy as np
from PIL import Image,ImageFilter
from mesh_tools import Mesh
from iostore import Toc
R=Path(sys.argv[1]);out=Path(__file__).resolve().parent.parent;t=Toc(str(out/'container/pc9298_mobile_and.utoc'));checks=[]
for profile,year in [('ND01','2017'),('ND06','2006'),('ND13','2013'),('ND27','2027')]:
 row=next(x for x in json.loads((out/'build-report.json').read_text())['meshes'] if x['profile']==profile and x['variant']=='4522ep00v0313');raw=t.read(t.files['RealFace/SK_'+profile+'ep00v0313_Face.uasset']);m=Mesh(raw,(R/('v7-'+profile+'ep00v0313.log')).read_text(),0)
 normal=np.array(Image.open(out/('T_'+profile+'ep00v0313_Face_N-decoded.png')).convert('RGB'));uv=m.uv[:row['neck_vertices'],:2].astype(float);pixel=np.clip((uv*2048).astype(int),0,2047);values=normal[pixel[:,1],pixel[:,0]];error=np.linalg.norm(values[:,:2].astype(float)-128,axis=1);assert np.median(error)<9,(profile,np.median(error))
 sro=np.array(Image.open(out/('T_'+profile+'ep00v0313_Face_SRO-decoded.png')).convert('RGB'));sro_samples=sro[pixel[:,1],pixel[:,0]].astype(float);deviation=np.median(np.abs(sro_samples-np.median(sro_samples,axis=0)),axis=0);assert deviation.max()<9,(profile,deviation)
 checks.append({'profile':profile,'neck_normal_sample_vertices':len(values),'neutral_xy_error_median':float(np.median(error)),'neck_sro_median_absolute_deviation':deviation.tolist()})
 if profile=='ND01':continue
 code='ND00'+profile[2:];name='T_'+code+'_Hair_D';src=Image.open(next((R/'input-1').rglob('hair_parts_bsm_alp.dds'))) if year=='2006' else Image.open(R/('input-'+year)/'converted/hair_parts_bsm_alp.dds');src=src.convert('RGBA');a=np.array(src);decoded=np.array(Image.open(out/(name+'-decoded.png')).convert('RGBA'));assert src.size==(2048,512) and decoded.shape==a.shape
 alpha_mae=float(np.abs(a[:,:,3].astype(float)-decoded[:,:,3]).mean());assert alpha_mae<4,(year,alpha_mae)
 asset=(out/'asset'/(name+'.uasset')).read_bytes();assert b'TEXTUREGROUP_Character' in asset
 for q in ['HQ','MQ']:
  material=(out/'asset'/('MI_'+code+'_Head_Hair_'+q+'.uasset')).read_bytes();assert b'M_Head_Hair_High' in material or b'133157_Hair_High' in material
 checks[-1].update(hair_size=src.size,hair_alpha_mae=alpha_mae,source_resolution_retained=True,unsharp_rgb_only=year in ['2006','2013'])
 # Independent UEViewer output must contain actual face, normal and hair PNGs.
 folder=R/'v7-full-export/Game/Assets/character/RealFace'
 for n in ['T_'+profile+'ep00v0313_Face_D','T_'+profile+'ep00v0313_Face_N',name]:assert (folder/(n+'.png')).exists(),n
result={'status':'FOUR_NECK_NORMAL_REGIONS_AND_NATIVE_RESOLUTION_ALPHA_HAIR_PASS','checks':checks,'renderer_tested':False,'phone_tested':False}
result['container_sha256']=hashlib.sha256((out/'container/pc9298_mobile_and.ucas').read_bytes()).hexdigest()
(out/'quality-validation.json').write_text(json.dumps(result,indent=2));print(result['status'])
