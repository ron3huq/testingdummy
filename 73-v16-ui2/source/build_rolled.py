from pathlib import Path
import sys,re,struct,json,hashlib,types,inspect
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from zen_clone import rename,pid
from bundle_tools import Bundle
P=Path('/workspace/ronaldo-work/73-ui2');S=Path('/workspace/testingdummy/73-v16-ui2/source')
base=Toc('/workspace/ronaldo-work/resources/assetpacks/pad_ff_01/311010101/311010101/assets/pc0101_mobile_and.utoc')
custom=Toc(str(P/'body/pc9261_mobile_and.utoc'))
pat=re.compile(re.escape(struct.pack('<I',12))+b'(.{4})'+re.escape(struct.pack('<I',12))+b'\\1',re.S)

def roll(data):
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
   delta=(wrist_t-cuff_t)*.5
   moved=old[select]+q[:,None]*delta*axis
   skin_points=old[skin];skin_t=(skin_points-center)@axis;skin_radial=skin_points-center-skin_t[:,None]*axis
   radial=moved-center-((moved-center)@axis)[:,None]*axis;radius=np.linalg.norm(radial,axis=1)
   # Keep the cuff outside the retained skin surface, rather than pushing skin away.
   for ri,tcoord in enumerate((moved-center)@axis):
    near=abs(skin_t-tcoord)<1.5
    if q[ri]>.1 and near.any() and radius[ri]>1e-5:
     clearance=np.linalg.norm(skin_radial[near],axis=1).max()+.4
     radial[ri]*=max(1.,clearance/radius[ri])
   fold=.12*np.exp(-((q-.93)/.12)**2)
   moved=center+((moved-center)@axis)[:,None]*axis+radial*(1+fold[:,None])
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
   pos[select]=moved;changed|=select
   sides.append({'side':sign,'cloth_vertices':int(select.sum()),'source_cuff_cm':float(cuff),'source_wrist_cm':float(wrist),'cuff_extension_cm':float(delta)})
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
  raw=t.read(i);edited,proof=roll(raw)
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
