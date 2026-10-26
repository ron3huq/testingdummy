from pathlib import Path
import json,numpy as np
from scipy.spatial import cKDTree
r=Path('/workspace/analysis/my-league/ronaldo-pc-conversion/android-ronaldo-v2-final');R=Path(__file__).parent;d=r/'export-final/Game/Assets/character/RealFace';base=r.parent/'android-hair-v1/original-export/Game/Assets/character/RealFace';geo=json.loads((R/'game_geometry.json').read_text());locked=json.loads((R/'native-wrap-validation.json').read_text())['native_orbital_vertices_kept_exact']
def load(p):return json.loads(p.read_text()),p.parent
def ar(g,folder,i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];raw=(folder/g['buffers'][v['buffer']]['uri']).read_bytes();n={'VEC2':2,'VEC3':3,'VEC4':4,'SCALAR':1,'MAT4':16}[a['type']];out=np.frombuffer(raw,dtype={5126:'<f4',5123:'<u2',5121:'u1'}[a['componentType']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),count=a['count']*n).reshape(-1,n);return out.astype(float)/255 if a.get('normalized')and a['componentType']==5121 else out
report={'phone_tested':False,'native_topology_retained':True,'variants':[]};ref,rf=load(base/'SK_4522_Face.gltf');ra=ref['meshes'][0]['primitives'][0]['attributes'];refpos=ar(ref,rf,ra['POSITION']);refuv1=ar(ref,rf,ra['TEXCOORD_1']);refcolor=ar(ref,rf,ra['COLOR_0']);refnames=[ref['nodes'][i]['name']for i in ref['skins'][0]['joints']];refji=ar(ref,rf,ra['JOINTS_0']);refw=ar(ref,rf,ra['WEIGHTS_0'])
for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
 g,f=load(d/('SK_ND01'+suffix+'_Face.gltf'));orig,of=load(base/('SK_4522'+suffix+'_Face.gltf'));assert ar(g,f,g['skins'][0]['inverseBindMatrices']).tobytes()==ar(orig,of,orig['skins'][0]['inverseBindMatrices']).tobytes();names=[g['nodes'][i]['name']for i in g['skins'][0]['joints']];assert len(names)==166
 stats={}
 for pi,key in [(0,'face'),(1,'hair')]:
  p=g['meshes'][0]['primitives'][pi];a=p['attributes'];pos=ar(g,f,a['POSITION']);expected=np.array([[v['p'][0],v['p'][2],-v['p'][1]]for v in geo[key]]);assert pos.shape==expected.shape;err=float(np.abs(pos-expected).max())if pi==0 else float(cKDTree(expected).query(pos)[0].max());assert err<1e-6;ww=ar(g,f,a['WEIGHTS_0']);ji=ar(g,f,a['JOINTS_0']);assert np.abs(ww.sum(axis=1)-1).max()<1e-6
  if pi==0:
   assert np.array_equal(ar(g,f,a['TEXCOORD_1']),refuv1);assert np.array_equal(ar(g,f,a['COLOR_0']),refcolor);assert np.max(np.abs(pos[locked]-refpos[locked]))<1e-6
   for i in range(len(pos)):
    actual={names[int(j)]:float(w)for j,w in zip(ji[i],ww[i])if w>0};expectedw={refnames[int(j)]:float(w)for j,w in zip(refji[i],refw[i])if w>0};assert actual==expectedw,(i,actual,expectedw)
  stats[key]={'vertices':len(pos),'position_max_error_m':err}
 report['variants'].append({'variant':suffix or'base','native_166_bind_matrices_byte_identical':True,'native_face_weights_exact':True,'native_uv1_and_vertex_colours_exact':True,'native_orbital_vertices_exact':len(locked),**stats})
(R/'final-asset-validation.json').write_text(json.dumps(report,indent=2));print('FOUR_VARIANTS_EYE_POSITIONS_WEIGHTS_UV1_COLOURS_AND_166_BINDS_PASS')
