from pathlib import Path
import ast,sys,json,struct,numpy as np,hashlib
from PIL import Image
import etcpak,texture2ddecoder
out=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(out/'source'))
from iostore import Toc
from mesh_tools import Mesh
from zen_clone import rename
R=Path('/workspace/ronaldo-work');OUT=out;ASSET=out/'asset';BASE='/Game/Assets/character/RealFace/';ref=Toc(str(R/'apk/assets/gateway-release/livedata/pc9257_mobile_and.utoc'));previous_textures={};recipes=[];texture_reports=[]
for n in ast.parse((out/'source/build_assets.py').read_text()).body:
 if isinstance(n,ast.FunctionDef) and n.name in ['extract','add','texture']:exec(compile(ast.Module(body=[n],type_ignores=[]),'build_assets.py','exec'))
r=json.loads((out/'build-report.json').read_text());results=[];target=np.array([82.,52.,37.])
for code in ['NDXS','NDPQ','NDSP']:
 ver='v10' if code=='NDSP' else 'v9';name='T_'+code+'ep00v0313_Face_D';im=Image.open(out/(name+'-decoded.png')) if code=='NDSP' else Image.open(out/'references/v9'/(name+'.png'));a=np.array(im.convert('RGBA'));raw=(ASSET/('SK_'+code+'ep00v0313_Face.uasset')).read_bytes();m=Mesh(raw,((out/'references/v9' if ver=='v9' else R)/(ver+'-'+code+'ep00v0313.log')).read_text(),0)
 row=next(x for x in r['meshes'] if x['profile']==code);n=row['skin_vertices'];p=m.positions[:n];mask=(abs(p[:,0])<5)&(p[:,1]>13)&(p[:,2]>168)&(p[:,2]<171);uv=m.uv[:n,:2].astype(float);px=np.clip((uv[mask]*2048).astype(int),0,2047);assert len(px)>30
 before=np.median(a[px[:,1],px[:,0],:3],axis=0);scale=target/np.maximum(before,1);a[:1024,:,:3]=np.clip(np.rint(a[:1024,:,:3]*scale),0,255).astype('u1');texture('face',ref,'character/RealFace/T_133157_Face_D.uasset',name,Image.fromarray(a));results.append({'profile':code,'before_median':before.tolist(),'target_median_srgb':target.tolist(),'channel_scale':scale.tolist(),'sample_vertices':len(px)})
for report in texture_reports:r['textures']=[report if x['name']==report['name'] else x for x in r['textures']]
(out/'build-report.json').write_text(json.dumps(r,indent=2));(out/'skin-tone-report.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
