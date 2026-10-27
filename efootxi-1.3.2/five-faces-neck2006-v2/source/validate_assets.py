from pathlib import Path
import json,numpy as np
from scipy.spatial import cKDTree
R=Path(__file__).parent;P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');N=P/'android-five-combined';D=N/'export-final/Game/Assets/character/RealFace';O=P/'android-hair-v1/original-export/Game/Assets/character/RealFace';targets=json.loads((R/'targets.json').read_text())
def load(p):return json.loads(p.read_text()),p.parent

def arr(g,folder,index):
 a=g['accessors'][index];v=g['bufferViews'][a['bufferView']];raw=(folder/g['buffers'][v['buffer']]['uri']).read_bytes();num={'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16,'SCALAR':1}[a['type']];out=np.frombuffer(raw,dtype={5126:'<f4',5123:'<u2',5121:'u1'}[a['componentType']],offset=v.get('byteOffset',0)+a.get('byteOffset',0),count=a['count']*num).reshape(-1,num);return out.astype(float)/255 if a.get('normalized')and a['componentType']==5121 else out
report={'phone_tested':False,'reader':'independent UEViewer','heads':{}}
for kind,info in targets.items():
 geo=json.loads((R/kind/('game_geometry.json'if kind=='ronaldo'else'native_geometry.json')).read_text());rows=[]
 for suffix in ['','lg00v0000','ep01v0291','ep00v0313']:
  g,f=load(D/('SK_'+info['prefix']+suffix+'_Face.gltf'));orig,of=load(O/('SK_4522'+suffix+'_Face.gltf'));names=[g['nodes'][j]['name']for j in g['skins'][0]['joints']];onames=[orig['nodes'][j]['name']for j in orig['skins'][0]['joints']];assert names==onames and len(names)==166;assert arr(g,f,g['skins'][0]['inverseBindMatrices']).tobytes()==arr(orig,of,orig['skins'][0]['inverseBindMatrices']).tobytes();stats={}
  for part,pi in [('face',0),('hair',1)]if kind=='ronaldo'else[('head',1)]:
   vertices=geo[part]if kind=='ronaldo'else geo['vertices'];triangles=geo[part+'_triangles']if kind=='ronaldo'else geo['triangles'];pr=g['meshes'][0]['primitives'][pi];a=pr['attributes'];pos=arr(g,f,a['POSITION']);expected=np.array([[r['p'][0],r['p'][2],-r['p'][1]]for r in vertices]);assert pos.shape==expected.shape
   err=float(np.abs(pos-expected).max())if part!='hair'else float(cKDTree(expected).query(pos)[0].max());assert err<1e-6,(kind,part,err);ww=arr(g,f,a['WEIGHTS_0']);jj=arr(g,f,a['JOINTS_0']);assert np.max(np.abs(ww.sum(axis=1)-1))<1e-6;assert np.max(jj)<166;ind=arr(g,f,pr['indices']).reshape(-1,3);assert len(ind)==len(triangles)and ind.max()<len(pos)
   if part!='hair':
    assert np.array_equal(np.sort(ind,axis=1),np.sort(np.array(triangles),axis=1));uv=arr(g,f,a['TEXCOORD_0']);expected_uv=np.array([[r['uv'][0],1-r['uv'][1]]for r in vertices]);uve=float(np.abs(uv-expected_uv).max());assert uve<.00051,(kind,uve)
    for i,row in enumerate(vertices):
     expected_w={k:v for k,v in row['weights'].items()if v>1e-8};actual={names[int(j)]:float(w)for j,w in zip(jj[i],ww[i])if w>0};assert set(actual)<=set(expected_w);assert all(abs(actual.get(k,0)-v)<.008 for k,v in expected_w.items())
   if kind=='ronaldo'and part=='face':
    base,bf=load(O/'SK_4522_Face.gltf');attrs=base['meshes'][0]['primitives'][0]['attributes'];assert np.array_equal(arr(g,f,a['TEXCOORD_1']),arr(base,bf,attrs['TEXCOORD_1']));assert np.array_equal(arr(g,f,a['COLOR_0']),arr(base,bf,attrs['COLOR_0']));locked=json.loads((R/kind/'native-wrap-validation.json').read_text())['native_orbital_vertices_kept_exact']+json.loads((R/kind/'native-ear-validation.json').read_text())['native_ear_vertices_kept_exact'];assert np.max(np.abs(pos[locked]-arr(base,bf,attrs['POSITION'])[locked]))<1e-6
   stats[part]={'vertices':len(pos),'triangles':len(ind),'position_error_m':err,'weights_normalized':True}
  rows.append({'variant':suffix or'base','native_166_bind_matrices_identical':True,**stats})
 report['heads'][kind]=rows
(N/'asset-validation.json').write_text(json.dumps(report,indent=2));print('TWENTY_MESHES_166_BINDS_UV_WEIGHTS_AND_RONALDO_NATIVE_EYES_PASS')
