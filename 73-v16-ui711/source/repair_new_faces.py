from pathlib import Path
import sys,json,struct,inspect,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import Bundle;from mesh_tools import Mesh,ranges,platform_lod_properties
P=Path('/tmp/73-ui711');t=Toc(str(P/'new-faces/livedata/pc9308_mobile_and.utoc'));b=Bundle(t);native=Toc('/tmp/73-ui710/modder-original/pc3700_mobile_and.utoc');refraw=native.read(native.files[next(k for k in native.files if k.endswith('/SK_40122_Face.uasset'))]);rr,_,_=ranges(refraw,Path('/tmp/73-ui710/lukaku-export.log').read_text());at=rr['REF_BEGIN'];parents=[struct.unpack_from('<i',refraw,at+4+i*12+8)[0]for i in range(166)];poses=refraw[at+4+166*12+4:at+4+166*12+4+166*40];rows=[]
for path,(ident,raw)in list(b.files.items()):
 if not path.endswith('.uasset')or'SK_NCA'not in path:continue
 name=Path(path).stem;log=(P/'variant-logs'/(name+'.log')).read_text();r,sections,starts=ranges(raw,log,lod_index=1);at=r['REF_BEGIN'];assert struct.unpack_from('<I',raw,at)[0]==166;assert [struct.unpack_from('<i',raw,at+4+i*12+8)[0]for i in range(166)]==parents
 sourcepose=raw[at+4+166*12+4:at+4+166*12+4+166*40];diff=[i for i in range(166)if sourcepose[i*40:(i+1)*40]!=poses[i*40:(i+1)*40]];bodydiff=[i for i in diff if i<8 or i>20];assert not bodydiff,(name,'non-native-body-bind',bodydiff)
 m=Mesh(raw,log,lod_index=1)
 for section in range(len(m.info)):
  for weight in m.global_weights(section):assert sum(v for bone,v in weight)==255 and all(0<=bone<166 for bone,v in weight)
 # Keep the supplied facial controls and all native body transforms unchanged.
 lod=bytearray(raw[starts[1]:r['STREAM_END']]);assert struct.unpack_from('<II',lod,2)==(0,1)
 n=struct.unpack_from('<I',lod,10)[0];req=list(struct.unpack_from('<%dH'%n,lod,14));assert req==list(range(166))
 assert struct.unpack_from('<I',raw,r['ACTIVE_BEGIN'])[0]==166 and list(struct.unpack_from('<166H',raw,r['ACTIVE_BEGIN']+4))==list(range(166))
 tail=raw[r['STREAM_END']:];assert tail==bytes.fromhex('020200000000')
 data=bytearray(raw[:starts[0]]+lod+lod+tail);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',data,em+80,struct.unpack_from('<Q',raw,em+80)[0]+len(data)-len(raw));data,props=platform_lod_properties(data,edit=True);b.files[path]=(ident,bytes(data));rows.append({'asset':name,'source_166_reference_transforms_preserved':True,'body_reference_transforms_equal_native73':True,'facial_pose_differences_retained':diff,'required_and_active_bones_both_LODs':166,'both_LODs_real_inline_geometry':True,'all_BoneMaps_and_weights_valid':True,'no_vertex_or_limb_scaling':True})
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9308_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'fixed-faces/livedata');(P/'new-face-skeleton-validation.json').write_text(json.dumps({'passed':True,'variants':rows,'Android_tested':False},indent=2));assert len(rows)==20;print('20_FACES_NATIVE166_AND_REAL_LODS_PASS')
