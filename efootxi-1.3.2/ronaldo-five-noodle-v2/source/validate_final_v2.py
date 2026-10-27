from pathlib import Path
import json,numpy as np,hashlib,struct
from scipy.spatial import cKDTree
from PIL import Image
import texture2ddecoder
R=Path(__file__).parent;V=R/'v2';P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/'android-r5-v2-combined';D=N/'export-final/Game/Assets/character/RealFace';O=P/'android-hair-v1/original-export/Game/Assets/character/RealFace';targets=json.loads((V/'targets.json').read_text())
def load(p):return json.loads(p.read_text()),p.parent
def arr(g,folder,index):
 a=g['accessors'][index];v=g['bufferViews'][a['bufferView']];raw=(folder/g['buffers'][v['buffer']]['uri']).read_bytes();num={'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16,'SCALAR':1}[a['type']];out=np.frombuffer(raw,dtype={5126:'<f4',5123:'<u2',5121:'u1'}[a['componentType']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),count=a['count']*num).reshape(-1,num);return out.astype(float)/255 if a.get('normalized')and a['componentType']==5121 else out
report={'phone_tested':False,'cards':{},'texture_maps':{},'first_only_scope':None}
for card,row in targets.items():
 geo=json.loads((V/card/'game_geometry.json').read_text());checks=[]
 for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
  g,f=load(D/('SK_'+row['prefix']+suffix+'_Face.gltf'));orig,of=load(O/('SK_4522'+suffix+'_Face.gltf'));names=[g['nodes'][j]['name']for j in g['skins'][0]['joints']];onames=[orig['nodes'][j]['name']for j in orig['skins'][0]['joints']];assert names==onames and len(names)==166;assert arr(g,f,g['skins'][0]['inverseBindMatrices']).tobytes()==arr(orig,of,orig['skins'][0]['inverseBindMatrices']).tobytes();stats={}
  assert g['materials'][g['meshes'][0]['primitives'][0]['material']]['name']=='MI_'+row['material_prefix']+'_Head_FaceLegacy_MQ'
  assert g['materials'][g['meshes'][0]['primitives'][1]['material']]['name']=='MI_'+row['material_prefix']+'_Head_Hair_MQ'
  for part,pi in [('face',0),('hair',1)]:
   full=geo[part];tt=geo[part+'_triangles'];used=sorted(set(i for t in tt for i in t));vertices=[full[i]for i in used];pr=g['meshes'][0]['primitives'][pi];a=pr['attributes'];pos=arr(g,f,a['POSITION']);expected=np.array([[r['p'][0],r['p'][2],-r['p'][1]]for r in vertices]);assert len(pos)==len(vertices),(card,part,len(pos),len(vertices));err=max(float(cKDTree(expected).query(pos)[0].max()),float(cKDTree(pos).query(expected)[0].max()));assert err<1e-6,(card,part,err);ww=arr(g,f,a['WEIGHTS_0']);jj=arr(g,f,a['JOINTS_0']);assert np.max(abs(ww.sum(axis=1)-1))<1e-6 and jj.max()<166;ind=arr(g,f,pr['indices']).reshape(-1,3);assert len(ind)==len(tt)and ind.max()<len(pos);uv=arr(g,f,a['TEXCOORD_0']);euv=np.array([[r['uv'][0],1-r['uv'][1]]for r in vertices]);features=np.column_stack([pos,uv*.01]);ef=np.column_stack([expected,euv*.01]);uverror=float(cKDTree(ef).query(features)[0].max());assert uverror<.000006,(card,part,uverror);stats[part]={'referenced_vertices':len(pos),'triangles':len(ind),'max_position_error_m':err,'uv_feature_error':uverror,'weights_sum_one':True}
  checks.append({'variant':suffix or'base','original_166_bind_matrices_bit_identical':True,**stats})
 report['cards'][card]=checks
 photo=np.array(Image.open(R/'android-source'/card/'face_bsm_alp.png').convert('RGB'));atlas=np.array(Image.open(V/card/'face-atlas-2048.png'));assert np.array_equal(photo,atlas[:1024,:1024])
 for which in ['D','N','SRO']:
  data=(V/card/('final-'+which+'.ktx')).read_bytes();h=struct.unpack_from('<13I',data,12);assert h[4]==0x9274 and h[6:8]==(2048,2048)and h[11]==12;at=64+h[12];mips=[]
  for i in range(12):
   count=struct.unpack_from('<I',data,at)[0];at+=4;mip=data[at:at+count];at=(at+count+3)&~3;dim=max(4,2048>>i);assert len(mip)==dim*dim//2;decoded=texture2ddecoder.decode_etc2(mip,dim,dim);assert len(decoded)==dim*dim*4;mips.append(count)
  report['texture_maps'][card+'/'+which]={'twelve_mips_decoded':True,'base_2048':True,'mip_sizes':mips}
# Combined and single-card packages must agree on the first face's actual asset bytes.
F=P/'android-r5-v2-first';first=list(targets)[0];prefix=targets[first]['prefix'];mp=targets[first]['material_prefix'];same=0
for f in(F/'asset').iterdir():
 if f.name.startswith('SK_'+prefix)or f.name.startswith('T_'+prefix)or f.name.startswith('MI_'+mp):assert f.read_bytes()==(N/'asset'/f.name).read_bytes(),f.name;same+=1
meta=json.loads((F/'deploy/work/tools/noodle_bundle.json').read_text());assert meta['target_card_ids']=={first:first};report['first_only_scope']={'id':first,'matching_asset_files':same}
for folder in [N,F]:
 assert len((folder/'deploy/work/tools/gateway_runtime.py').read_bytes())==2441;m=json.loads((folder/'deploy/work/tools/noodle_bundle.json').read_text());assert hashlib.sha256((folder/'deploy/work/tools/libnoodle_hair.so').read_bytes()).hexdigest()==m['native_sha256']
 for name,check in m['files'].items():b=(folder/'deploy/livedata'/name).read_bytes();assert len(b)==check['size']and hashlib.sha256(b).hexdigest()==check['sha256']
(V/'final-validation.json').write_text(json.dumps(report,indent=2));print('FINAL_TWENTY_MESHES_SOURCE_SHAPE_UV_BINDS_FIFTEEN_TEXTURES_AND_BOTH_PACKAGES_PASS',flush=True)
