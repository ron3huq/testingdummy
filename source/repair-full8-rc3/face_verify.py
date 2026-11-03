from pathlib import Path
import sys,inspect,struct,json
import numpy as np
sys.path[:0]=['/workspace/work/full8/recovered-tools']
import mesh_tools
from iostore import Toc
scope={};exec(inspect.getsource(mesh_tools.Mesh).replace('len(self.info)==2','len(self.info)in(2,3)'),mesh_tools.__dict__,scope);Mesh=scope['Mesh']
R=Path('/workspace/work/full8-rc3/face');report=[]
for i,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
 t=Toc(str(R/'built'/f'pc{9336+i}_mobile_and.utoc'));name='SK_RV8C'+suffix+'_Face';b=t.read(t.files['character/RealFace/'+name+'.uasset']);log=(R/'readbacklogs'/(name+'.log')).read_text();assert log.count('cooked_out=0 inlined=1')==2;assert '*** ERROR'not in log
 high=Mesh(b,log,0);low=Mesh(b,log,1);assert len(high.info)==3 and len(low.info)==2
 assert [struct.unpack_from('<H',q['head'],2)[0]for q in high.info]==[0,2,1]
 assert [struct.unpack_from('<H',q['head'],2)[0]for q in low.info]==[2,1]
 assert mesh_tools.platform_lod_properties(b)['MinLod']==[0]
 native=Path('/workspace/ronaldo-work/ronaldo-android-fit/extracted/SK_4522'+suffix+'_Face.uasset').read_bytes();nlog=Path('/workspace/ronaldo-work',('native-'+suffix+'.log')if suffix else'native-.log').read_text();nm=Mesh(native,nlog,1)
 at=high.r['REF_BEGIN'];nat=nm.r['REF_BEGIN'];off=4+166*12+4
 assert b[at+off:at+off+166*40]==native[nat+off:nat+off+166*40]
 assert b[at:at+4+166*12]==native[nat:nat+4+166*12]
 assert np.array_equal(low.positions[:743],nm.positions[:743]);assert np.array_equal(low.uv[:743],nm.uv[:743])
 assert 'Loading MaterialInstanceConstant MI_4522'+suffix+'_Head_'in log
 assert 'Loading MaterialInstanceConstant MI_RV8C'+suffix+'_Head_'in log
 assert 'Loading Texture2D T_4522'+suffix+'_Face_D'in log
 props=(R/'readback/Game/Assets/character/RealFace'/(name+'.props.txt')).read_text();assert 'LODMaterialMap[2] = { 2, 1 }'in props
 assert set(high.info[0]['bones'])<={4,5,6,7,8,10,11,12,13,14,15};assert {8,14,15}<=set(high.info[1]['bones']);assert high.info[2]['bones']==[7]
 for m in [high,low]:
  assert np.all(np.isfinite(m.positions));assert m.indices.max()<len(m.positions)
  for si,q in enumerate(m.info):
   assert all(sum(w for k,w in pairs)==255 for pairs in m.global_weights(si))
   indices=m.indices[q['baseidx']//3:q['baseidx']//3+q['tris']];assert indices.min()>=q['basevert']and indices.max()<q['basevert']+q['verts']
 # Every LOD keeps the same expanded source V8 hair; face contains no limb influences.
 hair=np.load(R/'hair-native.npz');q=high.info[2];assert np.array_equal(high.positions[q['basevert']:],hair['positions']);assert np.allclose(high.uv[q['basevert']:],hair['uv'],atol=.001)
 report.append(dict(asset=name,independent_reader_exported_both_LODs=True,three_high_sections_skin_native_eyes_oral_hair=True,native4522_eye_oral_material_loaded=True,custom_skin_material_loaded=True,low_LOD_native_material_redirect_verified=True,native_body_bind_and_hierarchy_byte_exact=True,low_native_skin_and_UV_byte_exact=True,MinLod=0,all_weights_sum255=True,eyes_and_jaw_independent_bones=True,no_limb_influences=True,V8_hair_geometry_preserved=True,phone_verified=False))
(R/'geometry-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
