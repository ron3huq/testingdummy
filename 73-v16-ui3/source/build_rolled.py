from pathlib import Path
import sys,re,struct,json,hashlib,types,inspect
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from zen_clone import rename,pid
from bundle_tools import Bundle
P=Path('/workspace/ronaldo-work/73-ui3');S=Path('/workspace/testingdummy/73-v16-ui3/source')
base=Toc('/workspace/ronaldo-work/resources/assetpacks/pad_ff_01/311010101/311010101/assets/pc0101_mobile_and.utoc')
custom=Toc('/workspace/ronaldo-work/73-ui2/body/pc9261_mobile_and.utoc')
pat=re.compile(re.escape(struct.pack('<I',12))+b'(.{4})'+re.escape(struct.pack('<I',12))+b'\\1',re.S)

def buffers(data):
 result=[]
 for m in pat.finditer(data):
  n=struct.unpack('<I',m[1])[0];at=m.end()
  if not 100<=n<=20000 or at+n*12>len(data):continue
  pos=np.frombuffer(data,dtype='<f4',count=n*3,offset=at).reshape(-1,3).copy()
  if not np.isfinite(pos).all()or abs(pos).max()>1000 or pos[:,2].max()<100:continue
  ch=data.find(struct.pack('<4I',4,n,4,n),at+n*12)
  if ch<0:continue
  colors=np.frombuffer(data,dtype='u1',count=n*4,offset=ch+16).reshape(-1,4)
  result.append((pos,np.all(colors==0,axis=1)))
 return result

def roll(data,reference):
 references=buffers(reference)
 if len(references)!=2:raise ValueError('long-sleeve reference LODs unavailable')
 out=bytearray(data);reports=[]
 for m in pat.finditer(data):
  n=struct.unpack('<I',m[1])[0];at=m.end()
  if not 100<=n<=20000 or at+n*12>len(data):continue
  pos=np.frombuffer(data,dtype='<f4',count=n*3,offset=at).reshape(-1,3).copy()
  if not np.isfinite(pos).all()or abs(pos).max()>1000 or pos[:,2].max()<100:continue
  colhead=data.find(struct.pack('<4I',4,n,4,n),at+n*12)
  if colhead<0:continue
  ca=colhead+16;colors=np.frombuffer(data,dtype='u1',count=n*4,offset=ca).reshape(-1,4)
  if ca+n*4>len(data):continue
  wa=-1
  for inf in [8,4]:
   head=data.find(struct.pack('<II',1,n*inf*2),at+n*12,colhead)
   if head<0:continue
   candidate=np.frombuffer(data,dtype='u1',count=n*inf*2,offset=head+8).reshape(n,inf*2)
   if np.all(candidate[:,inf:].sum(1)==255):wa=head+8;weights=candidate.copy();break
  if wa<0:raise ValueError('no validated weight array')
  old=pos.copy();newweights=weights.copy();cloth=np.all(colors==0,axis=1);changed=np.zeros(n,dtype=bool);sides=[]
  for sign in [-1,1]:
   x=old[:,0]*sign;arm=(x>20)&(old[:,2]>100);c=arm&cloth;skin=arm&~cloth
   if c.sum()<8 or skin.sum()<8:raise ValueError('arm masks unavailable')
   cuff=x[c].max();wrist=x[skin].max()
   if not 5<wrist-cuff<40:raise ValueError('unrecognized cuff/wrist geometry')
   fore=old[skin&(x>cuff-1)];center=fore.mean(0);_,_,vh=np.linalg.svd(fore-center,full_matrices=False);axis=vh[0]
   if axis[0]*sign<0:axis=-axis
   if abs(axis[0])<.4:raise ValueError('invalid forearm axis')
   along=(old-center)@axis;cuff_t=along[c].max();wrist_t=along[skin].max();root=cuff_t-12
   select=c&(along>root);q=np.clip((along[select]-root)/(cuff_t-root),0,1);q=q*q*(3-2*q)
   delta=(wrist_t-cuff_t)*.60
   moved=old[select]+q[:,None]*delta*axis
   # Fit the entire upper sleeve and extended cuff to the real stock long-sleeve
   # envelope. UI2 erroneously retained a short sleeve's broad circumference.
   refpos,refcloth=references[len(reports)]
   refarm=refpos[refcloth&(refpos[:,0]*sign>19)&(refpos[:,2]>100)]
   if len(refarm)<12:raise ValueError('long-sleeve reference arm unavailable')
   # True forearm-normal cross-sections, rather than X-axis slices. A sloping
   # arm's X slice underestimates its underside and lets skin pierce the cloth.
   basis_y=np.array([0.,1.,0.]);basis_y-=axis*np.dot(basis_y,axis);basis_y/=np.linalg.norm(basis_y);basis_z=np.cross(axis,basis_y)
   basis=np.stack([axis,basis_y,basis_z],axis=1)
   ref_local=(refarm-center)@basis;skin_local=(old[skin]-center)@basis
   allselect=c&(x>21);allids=np.flatnonzero(allselect)
   current=old[allselect].copy();lookup={int(v):i for i,v in enumerate(allids)}
   for vi,point in zip(np.flatnonzero(select),moved):current[lookup[int(vi)]]=point
   ratios=[]
   for ri,point in enumerate(current):
    local=(point-center)@basis;t=local[0];dist=abs(ref_local[:,0]-t)
    band=max(.75,float(np.partition(dist,min(11,len(dist)-1))[min(11,len(dist)-1)]))
    near=ref_local[dist<=band,1:];lower=near.min(0);upper=near.max(0);mid=(lower+upper)*.5;half=np.maximum((upper-lower)*.5,.5)
    skin_near=skin_local[abs(skin_local[:,0]-t)<1.,1:]
    if len(skin_near):
     # Tight stock envelope, expanded only as needed for the exact retained arm.
     # Include angular skin extent; no arbitrary 12% puff or global maximum radius.
     sl=skin_near.min(0);su=skin_near.max(0)
     mid=(np.minimum(lower,sl)+np.maximum(upper,su))*.5
     half=np.maximum(half,np.maximum(abs(skin_near-mid).max(0),.5)+.12)
     expansion=max(1.,float(np.linalg.norm((skin_near-mid)/half,axis=1).max()))
     half*=expansion;half+=.12
    radial=local[1:]-mid;length=np.linalg.norm(radial/half)
    if length<1e-5:continue
    target=mid+radial/length
    blend=np.clip((abs(point[0])-21)/5,0,1);blend=blend*blend*(3-2*blend)
    tq=float(np.clip((t-root)/(cuff_t-root+delta),0,1));fold=.12*np.exp(-((tq-.97)/.055)**2)
    target+=radial/max(np.linalg.norm(radial),1e-6)*fold
    local[1:]=local[1:]*(1-blend)+target*blend
    current[ri]=center+local@basis.T
    if blend>.99:ratios.append(float(np.linalg.norm((local[1:]-mid)/half)))
   pos[allselect]=current;changed|=allselect
   # Stock long sleeves omit skin under their cloth. The short-body donor keeps
   # it; tuck only fully covered arm vertices inside the sleeve to prevent
   # two animated surfaces intersecting. Visible forearm/wrist remains exact.
   covered=skin&(along<cuff_t+delta-.7)
   local=(old[covered]-center)@basis
   fade=np.clip((cuff_t+delta-.7-local[:,0])/1.2,0,1)
   local[:,1:]*=(1-.18*fade[:,None])
   pos[covered]=center+local@basis.T;changed|=covered
   # Weight interpolation below applies only to the newly lengthened forearm.
   # The short-sleeve source retains the whole bare forearm. Copy only existing
   # same-section arm weights onto the extended cuff, so it follows the elbow.
   skin_indices=np.flatnonzero(skin);nearest=cKDTree(old[skin]).query(moved)[1]
   targets=weights[skin_indices[nearest]]
   for vertex,target,blend in zip(np.flatnonzero(select),targets,q):
    combined={}
    for row,factor in [(weights[vertex],1-blend),(target,blend)]:
     for bone,weight in zip(row[:inf],row[inf:]):
      if weight:combined[int(bone)]=combined.get(int(bone),0)+float(weight)*factor
    items=sorted(combined.items(),key=lambda kv:kv[1],reverse=True)[:inf];vals=np.array([w for _,w in items]);vals=vals/vals.sum()*255;quant=np.floor(vals).astype(int)
    for atq in np.argsort(-(vals-quant))[:255-quant.sum()]:quant[atq]+=1
    newweights[vertex]=0
    for ix,((bone,_),weight)in enumerate(zip(items,quant)):newweights[vertex,ix]=bone;newweights[vertex,inf+ix]=weight
   changed|=select
   sides.append({'side':sign,'cloth_vertices':int(select.sum()),'source_cuff_cm':float(cuff),'source_wrist_cm':float(wrist),'cuff_extension_cm':float(delta),'long_sleeve_radius_ratio_max':max(ratios,default=1.),'covered_skin_tucked':int(covered.sum()),'covered_t_limit':float(cuff_t+delta-.7),'axis':axis.tolist(),'center':center.tolist()})
  assert np.array_equal(old[~changed],pos[~changed]);assert np.array_equal(weights[~changed],newweights[~changed]);assert np.all(newweights[:,inf:].sum(1)==255)
  # Preserve the index buffer and recalculate normals/tangents only on cuff vertices.
  ih=-1;search=data.rfind(struct.pack('<I',2),0,at-16)
  while search>=0:
   if search+8<=len(data):
    ni=struct.unpack_from('<I',data,search+4)[0]
    if ni%3==0 and n<=ni<=n*20 and search+8+ni*2==at-16:ih=search;break
   search=data.rfind(struct.pack('<I',2),0,search)
  if ih<0:raise ValueError('index buffer not validated')
  tri=np.frombuffer(data,dtype='<u2',count=ni,offset=ih+8).reshape(-1,3);assert tri.max()<n
  th=data.find(struct.pack('<II',8,n),at+n*12,wa)
  if th<0:raise ValueError('tangent buffer unavailable')
  tang=np.frombuffer(data,dtype='i1',count=n*8,offset=th+8).reshape(-1,8).copy();oldnormal=tang[:,4:7].astype(float)/127
  def normals(points):
   face=np.cross(points[tri[:,1]]-points[tri[:,0]],points[tri[:,2]]-points[tri[:,0]]);normal=np.zeros_like(points,dtype=float)
   for corner in range(3):np.add.at(normal,tri[:,corner],face)
   normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12);return normal
  direction=1 if np.sum(normals(old)*oldnormal)>=0 else -1;normal=normals(pos)*direction;tx=tang[:,:3].astype(float)/127
  tx-=np.sum(tx*normal,axis=1)[:,None]*normal;tx/=np.maximum(np.linalg.norm(tx,axis=1,keepdims=True),1e-12)
  tang[changed,:3]=np.rint(np.clip(tx[changed],-1,1)*127).astype('i1');tang[changed,4:7]=np.rint(np.clip(normal[changed],-1,1)*127).astype('i1')
  out[th+8:th+8+n*8]=tang.tobytes()
  out[at:at+n*12]=pos.astype('<f4').tobytes();out[wa:wa+n*inf*2]=newweights.tobytes()
  reports.append({'vertices':n,'edited':int(changed.sum()),'position_offset':at,'weights_offset':wa,'influences':inf,'sides':sides})
 if len(reports)!=2:raise ValueError('expected two validated native LODs, got '+str(len(reports)))
 return bytes(out),reports

# Reuse the tested IoStore serializer under a separate container name.
source=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9299_mobile_and'")
ns={};exec('class Writer:\n'+source,Bundle.write.__globals__,ns);write=ns['Writer'].write
bundle=object.__new__(Bundle);bundle.base=custom;bundle.files={};bundle.entries={}
selected={}
for t in [base,custom]:
 h=parse_header(t.read(next(i for i,x in enumerate(t.ids)if x[11]==10)))
 for path,i in t.files.items():
  match=re.search(r'SK_(\d{3})([ad])(\d{2})\.uasset$',path)
  if match:selected[match.groups()]=(t,path,i,h)
report=[];failed=[];supported=set()
for (num,style,variant),(t,path,i,h)in sorted(selected.items()):
 try:
  raw=t.read(i);refpath='Body/SK_'+num+'b'+variant+'.uasset';refidx=base.files.get(refpath,base.files['Body/SK_015b07.uasset']);edited,proof=roll(raw,base.read(refidx))
 except ValueError as e:failed.append({'model':num+style+variant,'error':str(e)});continue
 newnum=int(num)+2000;deststyle={'a':'b','d':'e'}[style];oldname='SK_'+num+style+variant;newname=f'SK_{newnum:03d}{deststyle}{variant}'
 oldpath='/Game/Assets/character/Body/'+oldname;newpath='/Game/Assets/character/Body/'+newname
 replacements={oldname:newname,oldpath:newpath};edited=rename(edited,replacements,oldpath,newpath)
 oldpid=int.from_bytes(t.ids[i][:8],'little');newpid=pid(newpath);idb=struct.pack('<Q',newpid)+t.ids[i][8:]
 bundle.put('character/Body/'+newname+'.uasset',idb,edited,store_entry(h['store'],h['pids'].index(oldpid)))
 report.append({'source':oldname,'destination':newname,'source_sha256':hashlib.sha256(raw).hexdigest(),'lods':proof});supported.add((int(num),int(variant),int(style=='d')))
out=P/'payload/livedata';write(bundle,out)
(P/'rolled-build.json').write_text(json.dumps({'models':report,'failed':failed,'count':len(report),'source_skin_vertices_unchanged':True,'phone_tested':False},indent=2))
(S/'rolled-models.h').write_text('/* Exact source model/variant/mode pairs with separately cloned meshes. */\nstatic const unsigned rolled_models[][3]={'+','.join('{%d,%d,%d}'%x for x in sorted(supported))+'};\n')
print('ROLLED_MODELS',len(report),'FAILED',len(failed),failed[:3],flush=True)
