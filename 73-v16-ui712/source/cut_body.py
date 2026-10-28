"""Clip stock long sleeves; restore the exposed native short-template arm. No body scaling."""
from pathlib import Path
import sys,struct,re,subprocess,json,hashlib,inspect,concurrent.futures
import numpy as np
S='/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source';sys.path.insert(0,S)
from iostore import Toc,parse_header,store_entry
from zen_clone import rename,pid
from bundle_tools import Bundle
P=Path('/workspace/73-ui712');T=P/'build/apk/assets/gateway-release/work/tools';root=P/'mesh-reader';logs=P/'body-logs';logs.mkdir(exist_ok=True);out=Path('/tmp/ui712-cut-export')
base=Toc('/workspace/ronaldo-work/resources/assetpacks/pad_ff_01/311010101/311010101/assets/pc0101_mobile_and.utoc');hdr=parse_header(base.read(next(i for i,c in enumerate(base.ids)if c[11]==10)))
def reader(name):
 f=logs/(name+'.log')
 if f.exists():return f.read_text()
 r=subprocess.run(['/workspace/ronaldo-work/UEViewer/umodel','-testexport','-game=ue4.26','-android','-noanim','-aes=0x4552d45005dfe94964893f4925ec747d3d591401e060ed8b3d58be5721c81295','-path='+str(root),'-out='+str(out),name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);text=r.stdout.decode();f.write_text(text);assert r.returncode==0 and'RANGE STREAM_END'in text,(name,text[-500:]);return text
class Body:
 def __init__(self,data,log,index):
  self.raw=data;f=struct.unpack_from('<16I',data);assert(f[12]-f[11])//72==1;delta=f[13]+f[14]-struct.unpack_from('<Q',data,f[11])[0];pairs=[(k,int(v)+delta)for k,v in re.findall(r'RANGE (\w+) (\d+)',log)];lods=[v for k,v in pairs if k=='LOD_BEGIN'];assert len(lods)==2;a=lods[index];z=lods[index+1]if index==0 else len(data);pairs=[(k,v)for k,v in pairs if v<lods[0]or a<=v<z or(k=='STREAM_END'and v==z)];r=dict(pairs);self.r=r;self.begin=a;self.end=r['STREAM_END'];assert len([1 for k,v in pairs if k=='SECTION_BEGIN'])==1
  s=r['POSITIONS_BEGIN'];stride,n,stride2,n2=struct.unpack_from('<4I',data,s);assert stride==stride2==12 and n==n2;self.positions=np.frombuffer(data,dtype='<f4',count=n*3,offset=s+16).reshape(n,3).copy();s=r['INDICES_BEGIN'];assert data[s]==2 and struct.unpack_from('<I',data,s+1)[0]==2;ni=struct.unpack_from('<I',data,s+5)[0];self.tri=np.frombuffer(data,dtype='<u2',count=ni,offset=s+9).reshape(-1,3).copy();assert self.tri.max()<n
  s=r['TANGENT_UV_BEGIN'];self.tuhead=data[s:s+18];self.uvn=struct.unpack_from('<I',data,s+2)[0];assert self.uvn in[1,2,4];assert struct.unpack_from('<II',data,s+18)==(8,n);self.tangents=np.frombuffer(data,dtype='u1',count=n*8,offset=s+26).reshape(n,8).copy();s+=26+n*8;assert struct.unpack_from('<II',data,s)==(4,n*self.uvn);self.uv=np.frombuffer(data,dtype='<f2',count=n*self.uvn*2,offset=s+8).reshape(n,self.uvn*2).copy()
  s=r['SKIN_WEIGHTS_BEGIN'];self.swhead=data[s:s+22];self.inf=struct.unpack_from('<I',data,s+6)[0];assert self.inf in[4,8];assert struct.unpack_from('<II',data,s+22)==(1,n*self.inf*2);w=np.frombuffer(data,dtype='u1',count=n*self.inf*2,offset=s+30).reshape(n,self.inf*2).copy();assert np.all(w[:,self.inf:].sum(1)==255);self.swtail=data[s+30+n*self.inf*2:r['SKIN_WEIGHTS_END']];s=r['SKIN_WEIGHTS_END'];assert struct.unpack_from('<4I',data,s+2)==(4,n,4,n);self.colhead=data[s:s+2];self.colors=np.frombuffer(data,dtype='u1',count=n*4,offset=s+18).reshape(n,4).copy();self.coltail=data[s+18+n*4:r['STREAM_END']]
  s=r['SECTION_BEGIN'];nb=struct.unpack_from('<I',data,s+29)[0];bm=list(struct.unpack_from('<%dH'%nb,data,s+33));self.section_head=data[s:s+29];self.section_tail=data[s+33+nb*2:r['SECTIONS_END']];assert w[:,:self.inf].max()<nb;self.rows=[{bm[int(k)]:int(v)for k,v in zip(row[:self.inf],row[self.inf:])if v}for row in w]
  ref=r['REF_BEGIN'];assert struct.unpack_from('<I',data,ref)[0]==166;self.ref=data[ref:r['REF_END']]
 def vertex(self,i):return(self.positions[i].astype(float),self.tangents[i].view(np.int8).astype(float),self.uv[i].astype(float),self.colors[i].astype(float),self.rows[i])
 def write(self,verts,tri):
  n=len(verts);assert n<65536 and len(tri)>0;pos=np.array([v[0]for v in verts],dtype='<f4');tan=np.array([v[1]for v in verts],dtype=float);
  for a in [0,4]:
   lengths=np.linalg.norm(tan[:,a:a+3],axis=1);tan[:,a:a+3]*=(127/np.maximum(lengths,1))[:,None]
  tan=np.rint(np.clip(tan,-128,127)).astype('i1').view('u1');uv=np.array([v[2]for v in verts],dtype='<f2');col=np.array([v[3]for v in verts],dtype='u1');bm=sorted({k for v in verts for k in v[4]});assert len(bm)<=75;local={b:i for i,b in enumerate(bm)};weights=[]
  for v in verts:
   rows=sorted(v[4].items(),key=lambda x:-x[1])[:self.inf];total=sum(v for k,v in rows);assert total>0;ids=[local[k]for k,v in rows];ws=[round(v/total*255)for k,v in rows];ws[0]+=255-sum(ws);weights.append(ids+[0]*(self.inf-len(ids))+ws+[0]*(self.inf-len(ws)))
  weights=np.array(weights,dtype='u1');assert np.all(weights[:,self.inf:].sum(1)==255)
  ih=struct.pack('<BII',2,2,len(tri)*3)+np.array(tri,dtype='<u2').tobytes();points=struct.pack('<4I',12,n,12,n)+pos.tobytes();th=bytearray(self.tuhead);struct.pack_into('<I',th,6,n);tu=bytes(th)+struct.pack('<II',8,n)+tan.tobytes()+struct.pack('<II',4,n*self.uvn)+uv.tobytes();sh=bytearray(self.swhead);struct.pack_into('<II',sh,10,n*self.inf,n);sw=bytes(sh)+struct.pack('<II',1,n*self.inf*2)+weights.tobytes()+self.swtail;colors=self.colhead+struct.pack('<4I',4,n,4,n)+col.tobytes()+self.coltail;r=self.r;raw=self.raw;stream=raw[r['STREAM_BEGIN']:r['INDICES_BEGIN']]+ih+points+tu+sw+colors
  head=bytearray(self.section_head);tail=bytearray(self.section_tail);struct.pack_into('<II',head,4,0,len(tri));struct.pack_into('<I',head,21,0);struct.pack_into('<II',tail,0,n,self.inf);packed=struct.pack('<I166H',166,*range(166));header=raw[self.begin:self.begin+10]+packed+struct.pack('<I',1);section=bytes(head)+struct.pack('<I',len(bm))+struct.pack('<%dH'%len(bm),*bm)+tail
  return header+section+packed+struct.pack('<I',len(stream))+stream,{'vertices':n,'triangles':len(tri),'bones':len(bm),'full_active_required':166}
def interp(a,b,t):
 rows={k:a[4].get(k,0)*(1-t)+b[4].get(k,0)*t for k in set(a[4])|set(b[4])};return(a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t,a[3]*(1-t)+b[3]*t,rows)
def clip(poly,axis,limit,keep_low):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=float(a[0]@axis-limit);db=float(b[0]@axis-limit);ina=da<=0 if keep_low else da>=0;inb=db<=0 if keep_low else db>=0
  if ina:out.append(a)
  if ina!=inb:out.append(interp(a,b,da/(da-db)))
 return out

def build(long,short):
 assert long.ref[:2000]==short.ref[:2000]and long.ref[8640:]==short.ref[8640:]and np.allclose(np.frombuffer(long.ref,dtype='<f4',offset=2000,count=1660),np.frombuffer(short.ref,dtype='<f4',offset=2000,count=1660),atol=1e-6,rtol=0)and long.uvn==short.uvn
 vertices=[];tri=[];planes={};proof=[];lookup={}
 for sign in [-1,1]:
  p=short.positions;c=np.all(short.colors==0,axis=1);arm=(p[:,0]*sign>20)&(p[:,2]>100);skin=p[arm&~c];cloth=p[arm&c];assert len(skin)>20 and len(cloth)>10;fore=skin[skin[:,0]*sign>35];center=fore.mean(0);_,_,vh=np.linalg.svd(fore-center,full_matrices=False);axis=vh[0]
  if axis[0]*sign<0:axis=-axis
  cuff=float((cloth@axis).max());wrist=float((skin@axis).max());assert wrist>cuff+5;cut=cuff+.6*(wrist-cuff);planes[sign]=(axis,cut);proof.append({'side':sign,'cuff':cuff,'wrist':wrist,'cut':cut,'covered_forearm_ratio':.6})
 def emit(poly):
  if len(poly)<3:return
  indices=[]
  for vertex in poly:
   key=(np.round(np.concatenate(vertex[:4]),6).astype('<f4').tobytes(),tuple(sorted((k,round(v,6))for k,v in vertex[4].items())))
   index=lookup.get(key)
   if index is None:index=len(vertices);vertices.append(vertex);lookup[key]=index
   indices.append(index)
  for j in range(1,len(poly)-1):
   face=(indices[0],indices[j],indices[j+1])
   if len(set(face))==3:tri.append(face)
 for face in long.tri:
  poly=[long.vertex(i)for i in face];pos=np.array([v[0]for v in poly]);sign=1 if pos[:,0].mean()>0 else-1
  if np.all(pos[:,0]*sign>20)and np.all(pos[:,2]>100):axis,cut=planes[sign];poly=clip(poly,axis,cut,True)
  emit(poly)
 skin_triangles=0
 for face in short.tri:
  pos=short.positions[face];sign=1 if pos[:,0].mean()>0 else-1
  if not(np.all(pos[:,0]*sign>20)and np.all(pos[:,2]>100)and np.all(np.any(short.colors[face]!=0,axis=1))):continue
  axis,cut=planes[sign];poly=clip([short.vertex(i)for i in face],axis,cut-.6,False)
  if len(poly)>=3:skin_triangles+=len(poly)-2;emit(poly)
 assert skin_triangles>20;blob,meta=long.write(vertices,tri);meta.update(planes=proof,exposed_native_skin_triangles=skin_triangles,native_arm_positions_unscaled=True);return blob,meta

def main(limit=None):
 names=[]
 for path in base.files:
  m=re.fullmatch(r'Body/SK_(\d{3})([be])(\d{2})\.uasset',path)
  if m:
   num,style,var=m.groups();short='Body/SK_'+num+('a'if style=='b'else'd')+var+'.uasset'
   if short not in base.files:
    choices=[p for p in base.files if re.fullmatch(r'Body/SK_'+num+('a'if style=='b'else'd')+r'\d{2}\.uasset',p)]
    if not choices:choices=[p for p in base.files if re.fullmatch(r'Body/SK_'+num+r'[ad]\d{2}\.uasset',p)]
    if choices:short=min(choices,key=lambda p:abs(int(Path(p).stem[-2:])-int(var)))
   if short in base.files:names.append((path,short,m.groups()))
 if limit:names=[r for r in names if r[0]=='Body/SK_015b07.uasset']
 allnames=sorted({Path(p).stem for row in names for p in row[:2]});print('READ_NATIVE_BODIES',len(allnames),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:list(ex.map(reader,allnames))
 b=Bundle.__new__(Bundle);b.base=base;b.files={};b.entries={};proof=[];failed=[];supported=[]
 for path,short,parts in names:
  try:
   raw=base.read(base.files[path]);sr=base.read(base.files[short]);logs1=reader(Path(path).stem);logs2=reader(Path(short).stem);lods=[];checks=[]
   for l in [0,1]:
    model=Body(raw,logs1,l);sk=Body(sr,logs2,l);blob,meta=build(model,sk);lods.append(blob);checks.append(meta)
   first=Body(raw,logs1,0);last=Body(raw,logs1,1);edited=bytearray(raw[:first.begin]+b''.join(lods)+raw[last.end:]);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',edited,em+8,struct.unpack_from('<Q',raw,em+8)[0]+len(edited)-len(raw));num,style,var=parts;old=Path(path).stem;new='SK_'+str(int(num)+6000)+style+var;own='/Game/Assets/character/Body/'+old;dest=own.replace(old,new);edited=rename(edited,{old:new,own:dest},own,dest);ident=struct.pack('<Q',pid(dest))+b'\0\0\0\2';oldpid=int.from_bytes(base.ids[base.files[path]][:8],'little');b.put('character/Body/'+new+'.uasset',ident,edited,store_entry(hdr['store'],hdr['pids'].index(oldpid)));supported.append([int(num),int(var),int(style=='e')]);proof.append({'source':old,'skin_donor':Path(short).stem,'new':new,'LODs':checks,'reference_pose_sha256':hashlib.sha256(first.ref).hexdigest()})
  except Exception as e:failed.append({'path':path,'error':str(e)})
 print('CUT_BUILT',len(proof),'FAILED',len(failed),failed[:3],flush=True);assert proof
 src=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9312_mobile_and'");ns={};exec('class Writer:\n'+src,Bundle.write.__globals__,ns);ns['Writer'].write(b,P/'cut-bodies/livedata');(P/'cut-body-validation.json').write_text(json.dumps({'count':len(proof),'failed':failed,'models':proof,'Android_tested':False},indent=2));(P/'build/native/cut-models.h').write_text('static const u32 cut_models[][3]={'+','.join('{%d,%d,%d}'%tuple(r)for r in supported)+'};\n')
if __name__=='__main__':main('one'if'--one'in sys.argv else None)
