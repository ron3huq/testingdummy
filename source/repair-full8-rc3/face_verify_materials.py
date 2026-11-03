from pathlib import Path
import sys,numpy as np,json
sys.path.insert(0,'/workspace/work/full8/recovered-tools');from iostore import Toc;from bundle_tools import decode_first_texture
import mesh_tools,inspect
ns={};exec(inspect.getsource(mesh_tools.Mesh).replace('len(self.info)==2','len(self.info)in(2,3)'),mesh_tools.__dict__,ns);Mesh=ns['Mesh']
R=Path('/workspace/work/full8-rc3/face');reports=[]
for i,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
 t=Toc(str(R/'built'/f'pc{9336+i}_mobile_and.utoc'));n='character/RealFace/T_RV8C'+suffix+'_Face_D';a=np.asarray(decode_first_texture(t.read(t.files[n+'.uasset']),t.read(t.files[n+'.ubulk'])).convert('RGBA'))
 assert np.min(a[:1024,:1024,3])>=254
 # Validate actual compressed texture readback, not the source PNG alone.
 assert np.mean(a[:1024,:1024,:3])>60
 mname='SK_RV8C'+suffix+'_Face';raw=t.read(t.files['character/RealFace/'+mname+'.uasset']);high=Mesh(raw,(R/'readbacklogs'/(mname+'.log')).read_text(),0)
 native=Mesh(Path('/workspace/ronaldo-work/ronaldo-android-fit/extracted/SK_4522'+suffix+'_Face.uasset').read_bytes(),Path('/workspace/ronaldo-work',('native-'+suffix+'.log')if suffix else'native-.log').read_text(),1)
 # Native accessory ordering is3..22 and628..742: ear0..2 and connected
 # skin23..627 are not part of the native ocular/oral islands.
 ids=list(range(3,23))+list(range(628,743));q=high.info[1]
 assert q['verts']==135 and np.array_equal(high.positions[q['basevert']:q['basevert']+135],native.positions[ids])
 assert np.array_equal(high.uv[q['basevert']:q['basevert']+135],native.uv[ids])
 reports.append(dict(native4522_eye_oral_positions_and_UV_byte_exact=True,variant=suffix or'base',actual_compressed_diffuse_alpha_min=int(a[:1024,:1024,3].min()),native_opaque_skin_alpha=True,mean_skin_RGB=float(a[:1024,:1024,:3].mean()),phone_render_not_executed=True))
(R/'material-validation.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
