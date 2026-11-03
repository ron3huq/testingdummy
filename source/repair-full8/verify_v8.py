from pathlib import Path
import sys,json,struct,hashlib,collections
import numpy as np
sys.path[:0]=['/workspace/work/full8/recovered-tools','/workspace/ronaldo-work']
from iostore import Toc
from mesh_tools import Mesh,platform_lod_properties
from gltf_read import Gltf
R=Path('/workspace/work/full8/face-v8')
g=Gltf(Path('/workspace/ronaldo-work/native-export/Game/Assets/character/RealFace/SK_4522_Face.gltf'));inv=g.get(g.d['skins'][0]['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1);bind=np.linalg.inv(inv)
reports=[]
def psk_bones(path):
 data=path.read_bytes();at=0
 while at<len(data):
  tag,flags,size,n=struct.unpack_from('<20siii',data,at);at+=32
  if tag.rstrip(b'\0')==b'REFSKELT':return [data[at+i*size:at+i*size+64].split(b'\0')[0].decode()for i in range(n)]
  at+=size*n
 raise AssertionError('Missing reference skeleton')
for suffix in ['','ep00v0313','ep01v0291','lg00v0000']:
 number={'':9328,'ep00v0313':9329,'ep01v0291':9330,'lg00v0000':9331}[suffix];t=Toc(str(R/'built'/('pc'+str(number)+'_mobile_and.utoc')))
 name='SK_RV08'+suffix+'_Face';b=t.read(t.files['character/RealFace/'+name+'.uasset']);log=(R/'logs'/(name+'.log')).read_text();assert log.count('cooked_out=0 inlined=1')==2 and 'cooked_out=1'not in log
 high=Mesh(b,log,0);low=Mesh(b,log,1);props=platform_lod_properties(b);assert props['MinLod']==[0]
 assert psk_bones(R/'readback/Game/Assets/character/RealFace'/(name+'.psk'))==[g.d['nodes'][j]['name']for j in g.d['skins'][0]['joints']]
 native=Path('/workspace/ronaldo-work/ronaldo-android-fit/extracted/SK_4522'+suffix+'_Face.uasset').read_bytes()
 nlog=Path('/workspace/ronaldo-work',('native-'+suffix+'.log')if suffix else'native-.log').read_text();nm=Mesh(native,nlog,1)
 at=high.r['REF_BEGIN'];nat=nm.r['REF_BEGIN'];off=4+166*12+4
 assert b[at+off:at+off+166*40]==native[nat+off:nat+off+166*40]
 assert [struct.unpack_from('<i',b,at+4+i*12+8)[0]for i in range(166)]==[struct.unpack_from('<i',native,nat+4+i*12+8)[0]for i in range(166)]
 def required(m,lod):
  p=m.lods[lod];n=struct.unpack_from('<I',b,p+10)[0];return list(struct.unpack_from('<%dH'%n,b,p+14))
 assert required(high,0)==list(range(166));assert required(low,1)==list(range(8))+list(range(21,166))
 assert set(high.info[0]['bones'])<={4,5,6,7,8,10,11,12,13,14,15}
 assert {8,10,11,12,13,14,15}<=set(high.info[0]['bones']);assert set(low.info[0]['bones'])<={4,5,6,7}
 assert np.array_equal(low.positions[:743],nm.positions[:743]);assert np.array_equal(low.indices[:nm.info[0]['tris']],nm.indices[:nm.info[0]['tris']])
 for m in [high,low]:
  assert np.all(np.isfinite(m.positions));assert int(m.indices.max())<len(m.positions)
  for sec in [0,1]:
   for pairs in m.global_weights(sec):assert sum(w for k,w in pairs)==255
 # Skin exactly as loaded by independent readback, including quantization.
 ns=high.info[0]['verts'];p=high.positions[:ns];weights=np.zeros((ns,166))
 for i,pairs in enumerate(high.global_weights(0)):
  for k,w in pairs:weights[i,k]+=w/255
 pp=np.c_[p[:,[0,2,1]]/100,np.ones(ns)]
 def pose(changes):
  moved=pp[:,:3].copy()
  for bone,(axis,degrees)in changes.items():
   angle=np.deg2rad(degrees);c=np.cos(angle);s=np.sin(angle);mat=np.eye(4);ix=[i for i in range(3)if i!=axis];mat[np.ix_(ix,ix)]=[[c,-s],[s,c]];delta=(bind[bone]@mat@inv[bone]@pp.T).T[:,:3]-pp[:,:3];moved+=weights[:,bone,None]*delta
  return moved[:,[0,2,1]]*100
 jaw=pose({8:(1,-15)});blink=pose({10:(0,8),11:(0,-4),12:(0,8),13:(0,-4)})
 jawmove=np.linalg.norm(jaw-p,axis=1);blinkmove=np.linalg.norm(blink-p,axis=1)
 assert np.count_nonzero(jawmove>1e-4)>100;assert np.count_nonzero(blinkmove>1e-4)>10
 # No face/eye control can move the native neck seam or any limb influence.
 neck=p[:,2]<154;assert np.max(jawmove[neck])<1e-4 and np.max(blinkmove[neck])<1e-4
 # Exact duplicated low-neck vertices remain joined through head/neck poses.
 buckets=collections.defaultdict(list)
 for i,pt in enumerate(p):
  if pt[2]<154:buckets[tuple(np.round(pt,4))].append(i)
 for ids in buckets.values():
  if len(ids)>1:assert np.max(np.ptp(weights[ids],axis=0))<1/255+1e-8
 reports.append(dict(asset=name,independent_reader_both_LODs_real=True,MinLod=0,required_counts=[166,153],native_body_bind_pose_exact=True,low_native_skin_exact=True,quantized_weights_sum255=True,facial_weights_include_jaw_eyes_eyelids=True,jaw_vertices_moved=int(np.count_nonzero(jawmove>1e-4)),eyelid_vertices_moved=int(np.count_nonzero(blinkmove>1e-4)),maximum_jaw_displacement_cm=float(jawmove.max()),maximum_eyelid_displacement_cm=float(blinkmove.max()),neck_stationary_under_facial_controls=True,limb_bones_not_used=True,phone_verified=False))
(R/'geometry-validation.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
