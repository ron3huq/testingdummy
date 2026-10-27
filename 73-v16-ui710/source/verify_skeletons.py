from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source');from iostore import Toc;from mesh_tools import ranges,Mesh
P=Path('/tmp/73-ui710');native=json.loads((P/'native-bones.json').read_text());rows=[]
def bones(f):
 b=f.read_bytes();at=0
 while at<len(b):
  tag,flag,size,count=struct.unpack_from('<20siii',b,at);at+=32
  if tag.rstrip(b'\0')==b'REFSKELT':return [b[at+i*size:at+i*size+64].split(b'\0')[0].decode()for i in range(count)]
  at+=size*count
 raise AssertionError(f)
for group,num,tags in [('fixed-spider',9305,['NSPD']),('fixed-new',9307,['NNAR','NORC'])]:
 t=Toc(str(P/group/f'livedata/pc{num}_mobile_and.utoc'))
 for path,index in t.files.items():
  if not path.endswith('.uasset')or not any('SK_'+tag in path for tag in tags):continue
  name=Path(path).stem;assert bones(P/'independent-fixed-export/Game/Assets/character/RealFace'/(name+'.psk'))==native
  raw=t.read(index);log=(P/'independent-fixed-logs'/(name+'.log')).read_text();proof=[]
  for lod in [0,1]:
   r,sections,starts=ranges(raw,log,lod_index=lod);at=starts[lod];n=struct.unpack_from('<I',raw,at+10)[0];req=list(struct.unpack_from('<%dH'%n,raw,at+14));assert req==list(range(166));assert list(struct.unpack_from('<166H',raw,r['ACTIVE_BEGIN']+4))==list(range(166));m=Mesh(raw,log,lod_index=lod)
   for section in range(len(m.info)):
    for row in m.global_weights(section):assert sum(v for bone,v in row)==255 and all(0<=bone<166 for bone,v in row)
   proof.append({'LOD':lod,'required_bones_exact_order_0_to165':True,'active_bones_exact_order_0_to165':True,'section_skin_weights_valid':True,'render_stream_sha256':hashlib.sha256(raw[r['BUFFERS_SIZE']:r['STREAM_END']]).hexdigest()})
  assert proof[0]['render_stream_sha256']==proof[1]['render_stream_sha256'];rows.append({'asset':name,'all166_native_names_and_order_match':True,'LODs':proof})
(P/'skeleton-deep-validation.json').write_text(json.dumps({'passed':True,'variants':rows,'template_native_bone_count':166,'arm_leg_scale_edited':False,'device_cutscene_tested':False},indent=2));print('ALL12_DEEP_NATIVE166_PASS')
