from pathlib import Path
import sys,struct,inspect,json
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from bundle_tools import Bundle;from mesh_tools import Mesh,ranges,platform_lod_properties
P=Path('/workspace/73-ui712');t=Toc(str(P/'android-faces/livedata/pc9313_mobile_and.utoc'));b=Bundle(t);rows=[]
for path,(ident,raw)in list(b.files.items()):
 if not path.endswith('.uasset')or'/SK_'not in path:continue
 name=Path(path).stem;log=(P/'mesh-logs'/(name+'.log')).read_text();r,sec,lods=ranges(raw,log,lod_index=1);at=r['REF_BEGIN'];assert struct.unpack_from('<I',raw,at)[0]==166
 m=Mesh(raw,log,lod_index=1)
 for q in range(len(m.info)):
  for row in m.global_weights(q):assert sum(v for k,v in row)==255 and all(k<166 for k,v in row)
 lod=bytearray(raw[lods[1]:r['STREAM_END']]);assert struct.unpack_from('<II',lod,2)==(0,1);required=list(struct.unpack_from('<%dH'%struct.unpack_from('<I',lod,10)[0],lod,14));assert required==list(range(166))
 # A supplied real LOD1 is cloned as real LOD0; no head-only active list.
 active=r['ACTIVE_BEGIN']-lods[1];count=struct.unpack_from('<I',lod,active)[0];lod[active:active+4+count*2]=struct.pack('<I166H',166,*range(166))
 tail=raw[r['STREAM_END']:];assert tail==bytes.fromhex('020200000000');new=bytearray(raw[:lods[0]]+lod+lod+tail);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',new,em+80,struct.unpack_from('<Q',raw,em+80)[0]+len(new)-len(raw));new,_=platform_lod_properties(new,True);b.files[path]=(ident,new);rows.append(name)
src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9313_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'fixed-android/livedata');(P/'android-rig-validation.json').write_text(json.dumps({'passed':True,'native_bones':166,'real_LOD0_and_LOD1':True,'both_Active_Required_full166':True,'variants':rows,'Android_tested':False},indent=2));print('8_ANDROID_RIG_REPAIRED')
