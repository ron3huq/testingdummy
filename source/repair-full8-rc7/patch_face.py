"""Conservative authored-face correction: eyelids and rigid lower oral parts only.
No topology, head scale, body rig, reference pose, LOD, UV or texture edits.
"""
from pathlib import Path
import sys,struct,json,hashlib
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parent.parent/'repair-full8-rc4')]
from iostore import Toc
from ci_bundle import Bundle
from mesh_tools import Mesh
from zen_clone import rename,pid
BASE='/Game/Assets/character/RealFace/'
R=Path('/workspace/work/full8-rc7')
def eye_displacement(p):
 x,y,z=p[:,0],p[:,1],p[:,2];dx=np.minimum(abs(x-3.24),abs(x+3.20));front=np.exp(-((y-15.0)/2.0)**2);width=np.exp(-(dx/1.45)**2)
 d=(-.12*np.exp(-((z-171.15)/.70)**2)+.045*np.exp(-((z-169.55)/.65)**2))*front*width
 return np.where((z>168)&(z<173)&(abs(x)<5.6)&(y>12),d,0)

def modify(raw,log):
 m=Mesh(raw,log,lod_index=1);n=m.info[0]['verts'];tri=m.indices[:m.info[0]['tris']];edges=np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[0,2]]]);_,labels=connected_components(coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(n,n)),directed=False)
 assert np.sum(labels==30)==103 and np.sum(labels==29)==47
 old=m.positions.copy();pos=old.copy();skin=np.flatnonzero((labels==0)|(labels==1));dz=eye_displacement(pos[skin]);pos[skin,2]+=dz
 # Native material splits contain rigid lower teeth and tongue. Head/jaw blend
 # stretches these parts during a shout. Keep upper teeth and facial skin weights.
 weights=m.weights.copy();oral=np.flatnonzero((labels==30)|(labels==29));bm=m.info[0]['bones'];assert 8 in bm;weights[oral]=np.array([bm.index(8),0,0,0,255,0,0,0],dtype='u1')
 # Preserve tangent handedness while transforming normals by the local Jacobian.
 tangent=m.tangents.copy();selected=skin[abs(dz)>1e-7];points=old[selected].astype(float);eps=1e-3;grad=np.zeros((len(selected),3))
 for axis in range(3):
  plus=points.copy();minus=points.copy();plus[:,axis]+=eps;minus[:,axis]-=eps;grad[:,axis]=(eye_displacement(plus)-eye_displacement(minus))/(2*eps)
 J=np.broadcast_to(np.eye(3),(len(selected),3,3)).copy();J[:,2,:]+=grad
 tx=tangent[selected,:3].view('i1').astype(float)/127;nz=tangent[selected,4:7].view('i1').astype(float)/127;tx=np.einsum('nij,nj->ni',J,tx);nz=np.einsum('nji,nj->ni',np.linalg.inv(J),nz);nz/=np.maximum(np.linalg.norm(nz,axis=1)[:,None],1e-9);tx-=np.sum(tx*nz,axis=1)[:,None]*nz;tx/=np.maximum(np.linalg.norm(tx,axis=1)[:,None],1e-9)
 tangent[selected,:3]=np.rint(np.clip(tx,-1,1)*127).astype('i1').view('u1');tangent[selected,4:7]=np.rint(np.clip(nz,-1,1)*127).astype('i1').view('u1')
 b=bytearray(raw);r=m.r;start=r['POSITIONS_BEGIN']+16;b[start:start+pos.nbytes]=pos.astype('<f4').tobytes();start=r['SKIN_WEIGHTS_BEGIN']+30;b[start:start+weights.nbytes]=weights.tobytes();start=r['TANGENT_UV_BEGIN']+26;b[start:start+tangent.nbytes]=tangent.tobytes()
 assert len(b)==len(raw);check=Mesh(bytes(b),log,lod_index=1);assert np.array_equal(check.positions[n:],old[n:]);assert np.array_equal(check.weights[n:],m.weights[n:]);assert np.array_equal(check.uv,m.uv);assert np.array_equal(check.indices,m.indices);assert bytes(b[:r['POSITIONS_BEGIN']])==raw[:r['POSITIONS_BEGIN']]
 assert np.array_equal(check.positions[:n][labels==34],old[:n][labels==34]);assert np.max(np.linalg.norm(pos-old,axis=1))<.13
 assert np.array_equal(check.positions[oral],old[oral]);assert np.all(check.weights[:,4:].sum(1)==255)
 return bytes(b),{'changed_lid_vertices':int(len(selected)),'max_lid_adjustment_cm':float(np.max(abs(dz))),'rigid_lower_oral_vertices':len(oral),'unchanged_topology_UV_ref_pose_LODs_body_hair':True,'no_texture_edit':True,'phone_verified':False}

def build(root,logfile):
 live=Path(root)/'assets/gateway-release/livedata';logmap=json.loads(Path(logfile).read_text());allfiles={};entries={};base_t=None;report=[]
 for n in range(9352,9356):
  t=Toc(str(live/('pc%d_mobile_and.utoc'%n)));orig=Bundle(t);base_t=t
  for path,index in t.files.items():allfiles[path]=(t.ids[index],t.read(index));entries.update(orig.entries)
 change=lambda s:s.replace('RG2701','RG2801').replace('RG27','RG28')
 mappings={BASE+Path(p).stem:BASE+change(Path(p).stem)for p in allfiles if p.endswith('.uasset')};remap={pid(a):pid(b)for a,b in mappings.items()};out=Bundle(base_t);out.files={};out.entries={}
 for path,(idb,raw)in allfiles.items():
  name=Path(path).stem;newname=change(name);ext=Path(path).suffix;entry=None
  if name.startswith('SK_'):
   raw,check=modify(raw,logmap[name]);report.append({'asset':newname,**check})
  if ext=='.uasset':
   fixed,deps=entries[int.from_bytes(idb[:8],'little')];entry=(fixed,[remap.get(v,v)for v in deps]);repl={BASE+name:BASE+newname,name:newname}
   for a,b in mappings.items():repl[a]=b;repl[Path(a).name]=Path(b).name
   raw=rename(raw,repl,BASE+name,BASE+newname,imports=mappings)
  out.put('character/RealFace/'+newname+ext,struct.pack('<Q',pid(BASE+newname))+b'\0\0\0'+(b'\2'if ext=='.uasset'else b'\3'),raw,entry)
 for i,suffix in enumerate(['','ep00v0313','ep01v0291','lg00v0000']):
  part=Bundle(base_t);part.files={p:v for p,v in out.files.items()if(suffix in p if suffix else not any(s in p for s in ['ep00v0313','ep01v0291','lg00v0000']))};part.entries=out.entries;part.output_name='pc%d_mobile_and'%(9356+i);part.write(live)
 return report
if __name__=='__main__':
 result=build(*sys.argv[1:3]);Path(sys.argv[3]).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
