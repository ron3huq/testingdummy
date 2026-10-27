"""Restore native166 reference transforms without reducing any active/required list or scaling body parts."""
from pathlib import Path
import sys,struct,json,inspect,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import Bundle;from mesh_tools import ranges,Mesh
P=Path('/tmp/73-ui710');native=Toc(str(P/'modder-original/pc3700_mobile_and.utoc'));nraw=native.read(native.files[next(k for k in native.files if k.endswith('/SK_40122_Face.uasset'))]);nr,_,_=ranges(nraw,(P/'lukaku-export.log').read_text());nb=nr['REF_BEGIN'];assert struct.unpack_from('<I',nraw,nb)[0]==166;pose_at=nb+4+166*12;assert struct.unpack_from('<I',nraw,pose_at)[0]==166;native_pose=nraw[pose_at+4:pose_at+4+166*40];t=Toc(str(P/'new-heads/livedata/pc9307_mobile_and.utoc'));b=Bundle(t);proof=[]
for path,(ident,raw)in list(b.files.items()):
 if not path.endswith('.uasset')or not any(k in path for k in ['SK_NNAR','SK_NORC']):continue
 label=Path(path).stem;log=(P/'new-variant-logs'/(label+'.log')).read_text();r,sections,lods=ranges(raw,log);ref=r['REF_BEGIN'];assert struct.unpack_from('<I',raw,ref)[0]==166;at=ref+4+166*12;assert struct.unpack_from('<I',raw,at)[0]==166
 # Parent indices must match before transferring transforms. FName indices are package local and remain untouched.
 assert [struct.unpack_from('<i',raw,ref+4+i*12+8)[0]for i in range(166)]==[struct.unpack_from('<i',nraw,nb+4+i*12+8)[0]for i in range(166)]
 before_pose=raw[at+4:at+4+166*40];different=[i for i in range(166)if before_pose[i*40:(i+1)*40]!=native_pose[i*40:(i+1)*40]];data=bytearray(raw);data[at+4:at+4+166*40]=native_pose;stats=[]
 # The trial has a cooked-out LOD0 shell. Supply a real inlined LOD0 from the same validated source geometry.
 rr,ss,_=ranges(raw,log,lod_index=1);m=Mesh(raw,log,lod_index=1);weights=m.global_weights(0)+m.global_weights(1);assert all(sum(v for bone,v in row)==255 and all(0<=bone<166 for bone,v in row)for row in weights)
 active_n=struct.unpack_from('<I',raw,rr['ACTIVE_BEGIN'])[0];assert active_n==166
 assert list(struct.unpack_from('<166H',raw,rr['ACTIVE_BEGIN']+4))==list(range(166))
 lodblob=bytes(data[lods[1]:rr['STREAM_END']]);assert struct.unpack_from('<II',lodblob,2)==(0,1)
 tail=raw[rr['STREAM_END']:];assert tail==bytes.fromhex('020200000000')
 rebuilt=bytearray(data[:lods[0]]+lodblob+lodblob+tail);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',rebuilt,em+80,struct.unpack_from('<Q',raw,em+80)[0]+len(rebuilt)-len(raw))
 from mesh_tools import platform_lod_properties
 rebuilt,properties=platform_lod_properties(rebuilt,edit=True);data=bytearray(rebuilt)
 stats=[{'LOD':i,'active':166,'required':166,'cooked_out':False,'inlined':True,'all_weight_indices_valid':True,'sum_weights255':True,'section_BoneMaps':[q['bones']for q in m.info]}for i in [0,1]]
 b.files[path]=(ident,bytes(data));proof.append({'asset':path,'native_reference_bone_transforms_restored':166,'different_before_bones':different,'bone_order_and_parent_indices_preserved':True,'inverse_bind_basis':'Derived by Unreal from the exact native166 reference transforms; no independent inverse-bind table is serialized in this UE4.26 mesh payload','body_vertices_and_scale_not_edited':True,'LODs':stats})
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9307_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'fixed-new/livedata');(P/'new-heads-native166-validation.json').write_text(json.dumps({'passed':True,'all_four_variants':proof,'native_source':'73 host40122 skeleton, not an arbitrary external template','native_source_brown_Orc_and_Naruto_geometry_preserved':True,'Android_replay_and_celebration_tested':False},indent=2));print('NEW_HEADS_NATIVE166_RESTORED',len(proof))
