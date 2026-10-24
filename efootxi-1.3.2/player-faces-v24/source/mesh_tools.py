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
 def write(self,positions,tangents,uv,weights,colors,triangles,skin_vertices,skin_triangles,bonemap,active_bones):
  b=self.data;r=self.r;n=len(positions);hair_vertices=n-skin_vertices
  assert n<65536 and np.all(weights[:,4:].sum(1)==255) and len(bonemap)<=75
  indices=struct.pack('<BII',2,2,triangles.size)+triangles.astype('<u2').tobytes()
  points=struct.pack('<4I',12,n,12,n)+positions.astype('<f4').tobytes()
  h=bytearray(self.tuhead);struct.pack_into('<I',h,6,n)
  tu=bytes(h)+struct.pack('<II',8,n)+tangents.astype('u1').tobytes()+struct.pack('<II',4,n*2)+uv.astype('<f2').tobytes()
  h=bytearray(self.swhead);struct.pack_into('<II',h,10,n*4,n)
  sw=bytes(h)+struct.pack('<II',1,n*8)+weights.astype('u1').tobytes()+self.swtail
  col=self.colhead+struct.pack('<4I',4,n,4,n)+colors.astype('u1').tobytes()+self.coltail
  stream=b[r['STREAM_BEGIN']:r['INDICES_BEGIN']]+indices+points+tu+sw+col
  sections=[]
  for q,nv,nt,bi,bv,bm in [(self.info[0],skin_vertices,skin_triangles,0,0,bonemap),(self.info[1],hair_vertices,len(triangles)-skin_triangles,skin_triangles*3,skin_vertices,[7])]:
   head=bytearray(q['head']);tail=bytearray(q['tail']);struct.pack_into('<II',head,4,bi,nt);struct.pack_into('<I',head,21,bv);struct.pack_into('<II',tail,0,nv,4)
   sections.append(bytes(head)+struct.pack('<I',len(bm))+struct.pack('<%dH'%len(bm),*bm)+tail)
  prefix=bytearray(b[:r['STREAM_BEGIN']]);struct.pack_into('<I',prefix,r['BUFFERS_SIZE'],len(stream))
  lo=positions.min(0);hi=positions.max(0);center=(hi+lo)/2;extent=(hi-lo)/2;struct.pack_into('<7f',prefix,r['BOUNDS_BEGIN'],*center,*extent,float(np.linalg.norm(extent)))
  packed=struct.pack('<I',len(active_bones))+struct.pack('<%dH'%len(active_bones),*active_bones)
  edits=[(self.sections[0],r['SECTIONS_END'],b''.join(sections)),(r['ACTIVE_BEGIN'],r['ACTIVE_END'],packed)]
  for lod in self.lods:
   count=struct.unpack_from('<I',b,lod+10)[0];edits.append((lod+10,lod+14+count*2,packed))
  for a,z,value in sorted(edits,reverse=True):prefix[a:z]=value
  new=bytearray(prefix+stream+b[r['STREAM_END']:]);em=struct.unpack_from('<I',b,44)[0];struct.pack_into('<Q',new,em+80,struct.unpack_from('<Q',b,em+80)[0]+len(new)-len(b))
  return bytes(new)

def quantize(rows,bones):
 local={b:i for i,b in enumerate(bones)};out=[]
 for row in rows:
  row=sorted(row.items(),key=lambda x:-x[1])[:4];total=sum(v for k,v in row);assert total>0
  ids=[local[k] for k,v in row];ws=[round(v/total*255) for k,v in row];ws[0]+=255-sum(ws);assert min(ws)>=0
  out.append(ids+[0]*(4-len(ids))+ws+[0]*(4-len(ws)))
 return np.array(out,dtype='u1')


def write_native_lods(template,native,positions,tangents,uv,rows,colors,triangles,skin_vertices,skin_triangles,active):
 """Keep each native LOD RequiredBones list EXACT. Supply real HQ LOD0.
 LOD1 uses the original native head/neck controls. A compact pose must never
 acquire extra facial entries ahead of the shared shoulder/limb indices.
 """
 b=template.data;r=template.r;n=len(positions);ns=skin_vertices
 def packed(a):return struct.pack('<I',len(a))+struct.pack('<%dH'%len(a),*a)
 def lod_blob(lod):
  at=native.lods[lod];count=struct.unpack_from('<I',native.data,at+10)[0];required=list(struct.unpack_from('<%dH'%count,native.data,at+14))
  usedrows=rows if lod==0 else [{(k if k in required else 7):sum(v for bone,v in row.items() if (bone if bone in required else 7)==(k if k in required else 7)) for k in row} for row in rows]
  bm=sorted({k for row in usedrows for k,v in row.items() if v>0});assert set(bm)<=set(required)
  weights=np.concatenate([quantize(usedrows,bm),np.tile(np.array([0,0,0,0,255,0,0,0],dtype='u1'),(n-ns,1))])
  act=active if lod==0 else list(range(8));assert set(act)<=set(required)
  sections=[]
  for q,nv,nt,bi,bv,bmap in [(template.info[0],ns,skin_triangles,0,0,bm),(template.info[1],n-ns,len(triangles)-skin_triangles,skin_triangles*3,ns,[7])]:
   head=bytearray(q['head']);tail=bytearray(q['tail']);struct.pack_into('<II',head,4,bi,nt);struct.pack_into('<I',head,21,bv);struct.pack_into('<II',tail,0,nv,4);sections.append(bytes(head)+packed(bmap)+tail)
  ih=struct.pack('<BII',2,2,triangles.size)+triangles.astype('<u2').tobytes();points=struct.pack('<4I',12,n,12,n)+positions.astype('<f4').tobytes()
  th=bytearray(template.tuhead);struct.pack_into('<I',th,6,n);tu=bytes(th)+struct.pack('<II',8,n)+tangents.astype('u1').tobytes()+struct.pack('<II',4,n*2)+uv.astype('<f2').tobytes()
  sh=bytearray(template.swhead);struct.pack_into('<II',sh,10,n*4,n);sw=bytes(sh)+struct.pack('<II',1,n*8)+weights.tobytes()+template.swtail
  col=template.colhead+struct.pack('<4I',4,n,4,n)+colors.astype('u1').tobytes()+template.coltail
  stream=b[r['STREAM_BEGIN']:r['INDICES_BEGIN']]+ih+points+tu+sw+col
  header=bytearray(b[template.lods[1]:template.lods[1]+10]);struct.pack_into('<II',header,2,0,1)
  return bytes(header)+packed(required)+struct.pack('<I',2)+b''.join(sections)+packed(act)+struct.pack('<I',len(stream))+stream
 prefix=bytearray(b[:template.lods[0]]);lo=positions.min(0);hi=positions.max(0);center=(hi+lo)/2;extent=(hi-lo)/2;struct.pack_into('<7f',prefix,r['BOUNDS_BEGIN'],*center,*extent,float(np.linalg.norm(extent)))
 # Trailing resource metadata: NumInlinedLODs=2, NumNonOptionalLODs=2 (native).
 suffix=b[r['STREAM_END']:];assert suffix==bytes.fromhex('020200000000')
 new=bytearray(prefix+lod_blob(0)+lod_blob(1)+suffix);em=struct.unpack_from('<I',b,44)[0];struct.pack_into('<Q',new,em+80,struct.unpack_from('<Q',b,em+80)[0]+len(new)-len(b));return bytes(new)

def platform_lod_properties(data,edit=False):
 """Read cooked FPerPlatformInt/Float property tags, with structural validation.
 Original mesh MinLod=1 would permanently clamp out the new animated LOD0.
 """
 b=bytearray(data);f=struct.unpack_from('<16I',b);at=f[6];names=[]
 for i in range((f[9]-8)//8):
  h=int.from_bytes(b[at:at+2],'big');at+=2;wide=h>>15;n=h&32767;names.append(bytes(b[at:at+n*(2 if wide else 1)]).decode('utf-16-le' if wide else 'utf8'));at+=n*(2 if wide else 1)
 found={}
 for name,typename in [('MinLod','PerPlatformInt'),('ScreenSize','PerPlatformFloat')]:
  key=struct.pack('<II',names.index(name),0);start=f[13]+f[14];values=[]
  while True:
   p=b.find(key,start)
   if p<0:break
   start=p+1
   typeindex=struct.unpack_from('<I',b,p+8)[0]
   if typeindex>=len(names) or names[typeindex]!='StructProperty':continue
   if struct.unpack_from('<II',b,p+16)!=(8,0):continue
   actual=names[struct.unpack_from('<I',b,p+24)[0]]
   if actual not in [typename,'F'+typename]:continue
   assert b[p+48]==0 and struct.unpack_from('<I',b,p+49)[0]==1
   fmt='I' if name=='MinLod' else 'f';old=struct.unpack_from('<'+fmt,b,p+53)[0]
   if edit:struct.pack_into('<'+fmt,b,p+53,0 if name=='MinLod' else [.3,.05][len(values)])
   values.append(struct.unpack_from('<'+fmt,b,p+53)[0])
  found[name]=values
 assert len(found['MinLod'])==1 and len(found['ScreenSize'])==2,found
 return (bytes(b),found) if edit else found
