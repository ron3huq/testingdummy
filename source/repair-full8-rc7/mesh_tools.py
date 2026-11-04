"""Read/write only the audited inlined UE4.26 mobile mesh layout.
Reader offsets come from the patched UEViewer, not guessed byte signatures.
"""
import re,struct
import numpy as np

def ranges(data,log,lod_index=None):
 f=struct.unpack_from('<16I',data);em=f[11]
 delta=f[13]+f[14]+struct.unpack_from('<Q',data,em+8)[0]-struct.unpack_from('<Q',data,em+72)[0]
 pairs=[(k,int(v)+delta) for k,v in re.findall(r'RANGE (\w+) (\d+)',log)]
 lods=[v for k,v in pairs if k=='LOD_BEGIN']
 if lod_index is not None:
  begin=lods[lod_index];end=lods[lod_index+1] if lod_index+1<len(lods) else len(data)+1
  pairs=[(k,v) for k,v in pairs if v<lods[0] or begin<=v<end or (k=='STREAM_END' and v==end)]
 return dict(pairs),[v for k,v in pairs if k=='SECTION_BEGIN'],lods

class Mesh:
 def __init__(self,data,log,lod_index=None):
  self.data=data;self.r,self.sections,self.lods=ranges(data,log,lod_index);r=self.r
  s=r['INDICES_BEGIN'];assert data[s]==2 and struct.unpack_from('<I',data,s+1)[0]==2
  ni=struct.unpack_from('<I',data,s+5)[0];self.indices=np.frombuffer(data,dtype='<u2',count=ni,offset=s+9).reshape(-1,3).copy()
  s=r['POSITIONS_BEGIN'];stride,n,stride2,n2=struct.unpack_from('<4I',data,s);assert stride==stride2==12 and n==n2
  self.positions=np.frombuffer(data,dtype='<f4',count=n*3,offset=s+16).reshape(-1,3).copy()
  s=r['TANGENT_UV_BEGIN'];self.tuhead=data[s:s+18];assert struct.unpack_from('<II',data,s+18)==(8,n)
  self.tangents=np.frombuffer(data,dtype='u1',count=n*8,offset=s+26).reshape(-1,8).copy();s+=26+n*8;assert struct.unpack_from('<II',data,s)==(4,n*2)
  self.uv=np.frombuffer(data,dtype='<f2',count=n*4,offset=s+8).reshape(-1,4).copy()
  s=r['SKIN_WEIGHTS_BEGIN'];self.swhead=data[s:s+22];assert struct.unpack_from('<II',data,s+22)==(1,n*8)
  self.weights=np.frombuffer(data,dtype='u1',count=n*8,offset=s+30).reshape(-1,8).copy();self.swtail=data[s+30+n*8:r['SKIN_WEIGHTS_END']]
  s=r['SKIN_WEIGHTS_END'];assert struct.unpack_from('<4I',data,s+2)==(4,n,4,n)
  self.colors=np.frombuffer(data,dtype='u1',count=n*4,offset=s+18).reshape(-1,4).copy();self.colhead=data[s:s+2];self.coltail=data[s+18+n*4:r['STREAM_END']]
  self.info=[]
  for i,s in enumerate(self.sections):
   z=self.sections[i+1] if i+1<len(self.sections) else r['SECTIONS_END'];nb=struct.unpack_from('<I',data,s+29)[0];end=s+33+nb*2
   baseidx,nt=struct.unpack_from('<II',data,s+4);basevert=struct.unpack_from('<I',data,s+21)[0];nv=struct.unpack_from('<I',data,end)[0]
   self.info.append(dict(baseidx=baseidx,tris=nt,basevert=basevert,verts=nv,bones=list(struct.unpack_from('<%dH'%nb,data,s+33)),head=data[s:s+29],tail=data[end:z]))
  assert len(self.info)==2 and sum(q['verts'] for q in self.info)==n
  for q in self.info:
   w=self.weights[q['basevert']:q['basevert']+q['verts']];assert np.all(w[:,4:].sum(1)==255);assert w[:,:4].max()<len(q['bones'])
 def global_weights(self,section):
  q=self.info[section];w=self.weights[q['basevert']:q['basevert']+q['verts']];return [[(q['bones'][int(k)],int(v)) for k,v in zip(row[:4],row[4:]) if v] for row in w]
