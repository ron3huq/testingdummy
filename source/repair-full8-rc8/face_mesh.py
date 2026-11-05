"""Preserve authored close-up topology, hair, facial weights and bind pose.
Supply a genuine full LOD0 and an independent native-weighted low LOD.
Never remap authored facial weights to head merely to satisfy RequiredBones.
"""
from pathlib import Path
import struct,re,sys,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from mesh_tools import Mesh,ranges

def labels(m):
 n=m.info[0]['verts'];tri=m.indices[:m.info[0]['tris']];edges=np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[0,2]]]);return connected_components(coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(n,n)),directed=False)[1]

def lip_displacement(p):
 x,y,z=p.T;d=z-163.60
 # A smooth, monotone local compression seals the rest opening. Identical
 # positions on split material/UV islands receive identical corrections.
 wx=np.exp(-(abs(x)/3.5)**8);wy=np.clip((y-14.5)/1.0,0,1);wy=wy*wy*(3-2*wy)
 return -.95*d*np.exp(-np.minimum((d/1.0)**4,100))*wx*wy

def lip_mesh(m):
 pos=m.positions.copy();tan=m.tangents.copy();n=m.info[0]['verts'];lab=labels(m);idx=np.flatnonzero(lab<28);old=pos[idx].astype(float);dz=lip_displacement(old);selected=idx[abs(dz)>1e-6];pos[idx,2]+=dz
 points=m.positions[selected].astype(float);eps=1e-3;grad=np.zeros((len(selected),3))
 for axis in range(3):
  a=points.copy();b=points.copy();a[:,axis]+=eps;b[:,axis]-=eps;grad[:,axis]=(lip_displacement(a)-lip_displacement(b))/(2*eps)
 J=np.broadcast_to(np.eye(3),(len(selected),3,3)).copy();J[:,2,:]+=grad;assert np.linalg.det(J).min()>.04
 tx=tan[selected,:3].copy().view('i1')/127;nz=tan[selected,4:7].copy().view('i1')/127
 tx=np.einsum('nij,nj->ni',J,tx);nz=np.einsum('nji,nj->ni',np.linalg.inv(J),nz);nz/=np.maximum(np.linalg.norm(nz,axis=1)[:,None],1e-9);tx-=np.sum(tx*nz,axis=1)[:,None]*nz;tx/=np.maximum(np.linalg.norm(tx,axis=1)[:,None],1e-9)
 tan[selected,:3]=np.rint(np.clip(tx,-1,1)*127).astype('i1').view('u1');tan[selected,4:7]=np.rint(np.clip(nz,-1,1)*127).astype('i1').view('u1')
 assert np.array_equal(pos[n:],m.positions[n:]);assert np.array_equal(pos[:n][lab>=28],m.positions[:n][lab>=28]);assert np.max(abs(dz))<.55
 return pos,tan,lab,{'local_lip_vertices':len(selected),'maximum_lip_delta_cm':float(np.max(abs(dz))),'positive_jacobian_min':float(np.linalg.det(J).min())}

def nearest(p,t):
 a,b,c=t[:,0],t[:,1],t[:,2];ab=b-a;ac=c-a;ap=p-a;d00=(ab*ab).sum(1);d01=(ab*ac).sum(1);d11=(ac*ac).sum(1);d20=(ap*ab).sum(1);d21=(ap*ac).sum(1);den=d00*d11-d01*d01
 v=np.divide(d11*d20-d01*d21,den,out=np.zeros(len(den)),where=abs(den)>1e-12);w=np.divide(d00*d21-d01*d20,den,out=np.zeros(len(den)),where=abs(den)>1e-12);bc=np.c_[1-v-w,v,w];q=np.einsum('ij,ijk->ik',bc,t);d=((q-p)**2).sum(1);d[(bc<0).any(1)|(abs(den)<1e-12)]=np.inf;opts=[(q,bc,d)]
 for i,j in [(0,1),(1,2),(2,0)]:
  a=t[:,i];vec=t[:,j]-a;s=np.clip(((p-a)*vec).sum(1)/np.maximum((vec*vec).sum(1),1e-12),0,1);q=a+s[:,None]*vec;bc=np.zeros((len(s),3));bc[:,i]=1-s;bc[:,j]=s;opts.append((q,bc,((q-p)**2).sum(1)))
 best=min((float(z[2][k]),j,k)for j,z in enumerate(opts)for k in range(len(t)));_,j,k=best;return opts[j][0][k],opts[j][1][k],k

def low_surface(m,native,pos,tan,lab):
 ns=m.info[0]['verts'];nn=native.info[0]['verts'];assert nn==743
 tri=m.indices[:m.info[0]['tris']];tri=tri[lab[tri[:,0]]<35];tree=cKDTree(pos[tri].mean(1));q=native.positions[:nn].copy();uv=native.uv[:nn].copy();t=native.tangents[:nn].copy();dist=[]
 for i,p in enumerate(q):
  _,ix=tree.query(p,k=min(48,len(tri)));face=tri[np.atleast_1d(ix)];v,bc,j=nearest(p,pos[face].astype(float));vs=face[j];dist.append(float(np.linalg.norm(v-p)));q[i]=v;uv[i]=bc@m.uv[vs];tx=bc@(tan[vs,:3].copy().view('i1')/127);nz=bc@(tan[vs,4:7].copy().view('i1')/127);nz/=max(np.linalg.norm(nz),1e-9);tx-=np.dot(tx,nz)*nz;tx/=max(np.linalg.norm(tx),1e-9);t[i,:3]=np.rint(np.clip(tx,-1,1)*127).astype('i1').view('u1');t[i,4:7]=np.rint(np.clip(nz,-1,1)*127).astype('i1').view('u1')
 lowpos=np.concatenate([q,pos[ns:]]);lowtan=np.concatenate([t,tan[ns:]]);lowuv=np.concatenate([uv,m.uv[ns:]]);lowcol=np.concatenate([native.colors[:nn],m.colors[ns:]])
 lowtri=np.concatenate([native.indices[:native.info[0]['tris']],m.indices[m.info[0]['tris']:].astype(int)-ns+nn]);assert all(k==7 for row in m.global_weights(1)for k,v in row if v)
 weights=np.concatenate([native.weights[:nn],np.tile(np.array([0,0,0,0,255,0,0,0],dtype='u1'),(len(pos)-ns,1))])
 return (lowpos,lowtan,lowuv,weights,lowcol,lowtri,nn,native.info[0]['tris'],native.info[0]['bones']),max(dist)

def fit_neck(m,nm,pos,tan,lab):
 from collections import defaultdict
 def quantize(rows,bones):
  out=[];lookup={v:k for k,v in enumerate(bones)}
  for row in rows:
   row=sorted(((k,v)for k,v in row.items()if v>1e-9),key=lambda p:-p[1])[:4];total=sum(v for k,v in row);assert total>0
   ids=[lookup[k]for k,v in row];ws=[round(v/total*255)for k,v in row];ws[0]+=255-sum(ws);out.append(ids+[0]*(4-len(ids))+ws+[0]*(4-len(ws)))
  return np.array(out,dtype='u1')
 weights=m.weights.copy();tri=nm.indices[:nm.info[0]['tris']];tree=cKDTree(nm.positions[tri].mean(1));nw=nm.global_weights(0);sw=m.global_weights(0);bm=m.info[0]['bones'];deltas=[];changed=[]
 for i in np.flatnonzero((lab==34)&(pos[:len(lab),2]<156)):
  p=pos[i].copy();_,near=tree.query(p,k=min(48,len(tri)));q,bc,j=nearest(p,nm.positions[tri[np.atleast_1d(near)]].astype(float));vs=tri[np.atleast_1d(near)[j]]
  blend=float(np.clip((156-p[2])/5,0,1));blend=blend*blend*(3-2*blend);pos[i]=p*(1-blend)+q*blend;deltas.append(float(np.linalg.norm(pos[i]-p)));changed.append(int(i))
  row=defaultdict(float)
  for bone,v in sw[i]:row[bone]+=v*(1-blend)
  for k,factor in zip(vs,bc):
   for bone,v in nw[k]:row[bone]+=v*factor*blend
  assert set(row)<=set(bm);weights[i]=quantize([row],bm)[0]
  oldtx=m.tangents[i,:3].copy().view('i1')/127;oldnz=m.tangents[i,4:7].copy().view('i1')/127
  tx=oldtx*(1-blend)+(bc@(nm.tangents[vs,:3].copy().view('i1')/127))*blend;nz=oldnz*(1-blend)+(bc@(nm.tangents[vs,4:7].copy().view('i1')/127))*blend;nz/=max(np.linalg.norm(nz),1e-9);tx-=np.dot(tx,nz)*nz;tx/=max(np.linalg.norm(tx),1e-9)
  tan[i,:3]=np.rint(np.clip(tx,-1,1)*127).astype('i1').view('u1');tan[i,4:7]=np.rint(np.clip(nz,-1,1)*127).astype('i1').view('u1')
 assert np.array_equal(weights[:len(lab)][lab!=34],m.weights[:len(lab)][lab!=34]);assert np.array_equal(pos[:len(lab)][lab==34][m.positions[:len(lab)][lab==34,2]>=156],m.positions[:len(lab)][lab==34][m.positions[:len(lab)][lab==34,2]>=156])
 return weights,{'native_neck_vertices_fitted':len(changed),'maximum_neck_fit_cm':max(deltas),'facial_weights_unchanged':True,'neck_fit_below_z156_only':True}

def pack(a):return struct.pack('<I',len(a))+struct.pack('<%dH'%len(a),*a)
def lod_blob(m,geometry,required,active):
 pos,tan,uv,weights,col,tri,ns,nt,bm=geometry;n=len(pos);assert set(bm)<=set(required);assert np.all(weights[:,4:].sum(1)==255)
 sections=[]
 for q,nv,ntri,bi,bv,bmap in [(m.info[0],ns,nt,0,0,bm),(m.info[1],n-ns,len(tri)-nt,nt*3,ns,m.info[1]['bones']if len(required)==166 else[7])]:
  h=bytearray(q['head']);tail=bytearray(q['tail']);struct.pack_into('<II',h,4,bi,ntri);struct.pack_into('<I',h,21,bv);struct.pack_into('<II',tail,0,nv,4);sections.append(bytes(h)+pack(bmap)+tail)
 th=bytearray(m.tuhead);struct.pack_into('<I',th,6,n);sh=bytearray(m.swhead);struct.pack_into('<II',sh,10,n*4,n)
 stream=m.data[m.r['STREAM_BEGIN']:m.r['INDICES_BEGIN']]+struct.pack('<BII',2,2,tri.size)+tri.astype('<u2').tobytes()+struct.pack('<4I',12,n,12,n)+pos.astype('<f4').tobytes()
 stream+=bytes(th)+struct.pack('<II',8,n)+tan.astype('u1').tobytes()+struct.pack('<II',4,n*2)+uv.astype('<f2').tobytes()+bytes(sh)+struct.pack('<II',1,n*8)+weights.astype('u1').tobytes()+m.swtail+m.colhead+struct.pack('<4I',4,n,4,n)+col.astype('u1').tobytes()+m.coltail
 header=bytearray(m.data[m.lods[1]:m.lods[1]+10]);struct.pack_into('<II',header,2,0,1)
 return bytes(header)+pack(required)+struct.pack('<I',2)+b''.join(sections)+pack(active)+struct.pack('<I',len(stream))+stream

def build_mesh(raw,log,native_raw,native_log):
 m=Mesh(raw,log,lod_index=1);nm=Mesh(native_raw,native_log,lod_index=1);pos,tan,lab,report=lip_mesh(m)
 weights,neck_report=fit_neck(m,nm,pos,tan,lab);report.update(neck_report)
 high=(pos,tan,m.uv,weights,m.colors,m.indices,m.info[0]['verts'],m.info[0]['tris'],m.info[0]['bones']);low,maxdist=low_surface(m,nm,pos,tan,lab)
 req0=list(range(166));at=nm.lods[1];n=struct.unpack_from('<I',native_raw,at+10)[0];req1=list(struct.unpack_from('<%dH'%n,native_raw,at+14));assert len(req1)==153 and not set(range(8,21))&set(req1)
 prefix=bytearray(raw[:m.lods[0]]);lo=pos.min(0);hi=pos.max(0);cen=(hi+lo)/2;ext=(hi-lo)/2;struct.pack_into('<7f',prefix,m.r['BOUNDS_BEGIN'],*cen,*ext,float(np.linalg.norm(ext)))
 # Change MinLod only. Preserve authored ScreenSize thresholds instead of
 # forcing an unrelated parent component's LOD or modifying a body mesh.
 from audit_rig import names
 ns=names(raw);key=struct.pack('<II',ns.index('MinLod'),0);found=[];start=0
 while True:
  p=prefix.find(key,start)
  if p<0:break
  start=p+1
  if p+57<len(prefix) and struct.unpack_from('<II',prefix,p+16)==(8,0) and ns[struct.unpack_from('<I',prefix,p+8)[0]]=='StructProperty':found.append(p)
 assert len(found)==1;struct.pack_into('<I',prefix,found[0]+53,0)
 suffix=raw[m.r['STREAM_END']:];assert suffix==bytes.fromhex('020200000000');out=bytearray(prefix+lod_blob(m,high,req0,list(range(166)))+lod_blob(m,low,req1,list(range(8)))+suffix);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',out,em+80,struct.unpack_from('<Q',raw,em+80)[0]+len(out)-len(raw))
 report.update(high_vertices=len(pos),low_vertices=len(low[0]),low_native_skin_vertices=743,low_projection_max_cm=maxdist,required_bones=[166,153],MinLod=0,authored_facial_weights_unchanged=True,authored_high_hair_unchanged=True,all_reference_bones_unchanged=True,phone_verified=False)
 return bytes(out),lab,report
