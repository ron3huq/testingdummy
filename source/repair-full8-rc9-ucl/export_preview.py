from pathlib import Path
import sys,struct,json,numpy as np
from scipy.spatial.transform import Rotation
sys.path[:0]=[str(Path(__file__).parent),str(Path(__file__).parent.parent/'repair-full8-rc7'),str(Path(__file__).parent.parent/'repair-full8-rc4')]
from iostore import Toc
from mesh_tools import Mesh
from validate_face import read_lod
from bundle_tools import decode_first_texture
r=Path('/workspace/apk73');out=Path('/workspace/apk73-build/preview');out.mkdir(exist_ok=True);live=r/'assets/gateway-release/livedata';t=Toc(str(live/'pc9361_mobile_and.utoc'));old=Toc(str(live/'pc9356_mobile_and.utoc'));b=t.read(t.files['character/RealFace/SK_R8A2_Face.uasset']);raw=old.read(old.files['character/RealFace/SK_RG28_Face.uasset']);mesh=Mesh(raw,json.loads((r/'source/repair-full8-rc7/mesh-ranges.json').read_text())['SK_RG27_Face'],lod_index=1);lod=read_lod(b,mesh.lods[0]);at=lod['stream']+2;fmt,nbytes,ni=struct.unpack_from('<BII',b,at);assert fmt==2;at+=9;f=np.frombuffer(b,dtype='<u2',offset=at,count=ni).reshape(-1,3).copy();at+=ni*2;stride,n,st,n2=struct.unpack_from('<4I',b,at);assert stride==st==12 and n==n2;at+=16;p=np.frombuffer(b,dtype='<f4',offset=at,count=n*3).reshape(-1,3).copy();at+=n*12;tan=np.frombuffer(b,dtype='u1',offset=at+26,count=n*8).reshape(-1,8).copy();at+=26+n*8;uv=np.frombuffer(b,dtype='<f2',offset=at+8,count=n*4).reshape(-1,4).copy();at+=8+n*8;w=np.frombuffer(b,dtype='u1',offset=at+30,count=n*8).reshape(-1,8).copy();weights=np.zeros((n,166));offset=0
for sec in lod['sections']:
 for i in range(sec['verts']):
  for k,v in zip(w[offset+i,:4],w[offset+i,4:]):weights[offset+i,sec['bones'][k]]+=v/255
 offset+=sec['verts']
ref=mesh.r['REF_BEGIN'];nb=struct.unpack_from('<I',b,ref)[0];parents=np.array([struct.unpack_from('<i',b,ref+4+i*12+8)[0]for i in range(nb)]);at=ref+4+nb*12;assert struct.unpack_from('<I',b,at)[0]==nb;tr=np.frombuffer(b,dtype='<f4',offset=at+4,count=nb*10).reshape(nb,10);local=np.tile(np.eye(4),(nb,1,1));local[:,:3,:3]=Rotation.from_quat(tr[:,:4]).as_matrix()*tr[:,None,7:10];local[:,:3,3]=tr[:,4:7];rest=[]
for i in range(nb):rest.append(local[i]if parents[i]<0 else rest[parents[i]]@local[i])
rest=np.array(rest);np.savez(out/'asset.npz',p=p,f=f,uv=uv,tan=tan,weights=weights,parents=parents,local=local,rest=rest,skin_tris=lod['sections'][0]['tris']);
for name,toc,key in [('skin-D',t,'T_R8A2_Face_D'),('skin-SRO',t,'T_R8A2_Face_SRO'),('skin-N',old,'T_RG28_Face_N'),('hair-D',old,'T_RG2801_Hair_D')]:
 prefix='character/RealFace/'+key;decode_first_texture(toc.read(toc.files[prefix+'.uasset']),toc.read(toc.files[prefix+'.ubulk'])).save(out/(name+'.png'))
print('Actual packaged asset exported; vertices',n,'tris',len(f),'jaw pivot',rest[8,:3,3].tolist())
