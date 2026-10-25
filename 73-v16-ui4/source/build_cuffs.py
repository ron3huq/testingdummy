"""Continuous native LONG-sleeve mesh, stock palette/weights untouched.
Only distal skin/UV and a small cuff fold change. Never copy short-section bone indices.
"""
from pathlib import Path
import sys,re,struct,json,hashlib,inspect
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from zen_clone import rename,pid
from bundle_tools import Bundle
P=Path('/workspace/ronaldo-work/73-ui4');S=Path('/workspace/testingdummy/73-v16-ui4/source')
base=Toc('/workspace/ronaldo-work/resources/assetpacks/pad_ff_01/311010101/311010101/assets/pc0101_mobile_and.utoc');custom=Toc('/workspace/ronaldo-work/73-ui2/body/pc9261_mobile_and.utoc')
pat=re.compile(re.escape(struct.pack('<I',12))+b'(.{4})'+re.escape(struct.pack('<I',12))+b'\\1',re.S)
oldproof=json.loads(Path('/workspace/ronaldo-work/73-ui3/rolled-build.json').read_text());oldmap={r['source']:r for r in oldproof['models']}
def buffers(data):
 result=[]
 for m in pat.finditer(data):
  n=struct.unpack('<I',m[1])[0];at=m.end()
  if not 100<=n<=20000 or at+n*12>len(data):continue
  pos=np.frombuffer(data,dtype='<f4',count=n*3,offset=at).reshape(-1,3).copy()
  if not np.isfinite(pos).all()or abs(pos).max()>1000 or pos[:,2].max()<100:continue
  ch=data.find(struct.pack('<4I',4,n,4,n),at+n*12)
  if ch<0:continue
  colors=np.frombuffer(data,dtype='u1',count=n*4,offset=ch+16).reshape(-1,4).copy();th=data.find(struct.pack('<II',8,n),at+n*12,ch)
  if th<0:continue
  ua=th+8+n*8;stride,nu=struct.unpack_from('<II',data,ua);assert stride==4 and nu%n==0;channels=nu//n*2
  uv=np.frombuffer(data,dtype='<f2',count=n*channels,offset=ua+8).reshape(n,channels).astype(float)
  # Locate exactly the inlined index buffer ending at this position header.
  ih=data.rfind(struct.pack('<I',2),0,at-16)
  while ih>=0:
   ni=struct.unpack_from('<I',data,ih+4)[0]
   if ni%3==0 and n<=ni<=n*20 and ih+8+ni*2==at-16:break
   ih=data.rfind(struct.pack('<I',2),0,ih)
  assert ih>=0
  tri=np.frombuffer(data,dtype='<u2',count=ni,offset=ih+8).reshape(-1,3)
  result.append(dict(n=n,pa=at,ca=ch+16,ua=ua+8,uv=uv,pos=pos,colors=colors,tri=tri))
 return result

def build(raw,short,old):
 out=bytearray(raw);reports=[];ref=buffers(short)
 for li,r in enumerate(buffers(raw)):
  a=ref[min(li,len(ref)-1)];pos=r['pos'].copy();uv=r['uv'].copy();color=r['colors'].copy();changed=np.zeros(r['n'],bool);sides=[]
  for side in old['lods'][li]['sides']:
   sign=side['side'];axis=np.array(side['axis']);center=np.array(side['center']);limit=side['covered_t_limit']+.7+1.5
   t=(pos-center)@axis;arm=(pos[:,0]*sign>20)&(pos[:,2]>100);skin=np.any(a['colors']!=0,axis=1)&(a['pos'][:,0]*sign>19)&(a['pos'][:,2]>100)
   triangles=a['tri'][np.all(skin[a['tri']],axis=1)];assert len(triangles)>20
   tp=a['pos'][triangles];tree=cKDTree(tp.mean(1));choose=arm&(t>limit);points=pos[choose];_,candidates=tree.query(points,k=min(24,len(tp)));nn=tp[candidates];e0=nn[:,:,1]-nn[:,:,0];e1=nn[:,:,2]-nn[:,:,0];v=points[:,None,:]-nn[:,:,0];d00=np.sum(e0*e0,2);d01=np.sum(e0*e1,2);d11=np.sum(e1*e1,2);d20=np.sum(v*e0,2);d21=np.sum(v*e1,2);den=d00*d11-d01*d01;den=np.where(abs(den)>1e-10,den,1e-10)
   b=(d11*d20-d01*d21)/den;c=(d00*d21-d01*d20)/den;w=np.maximum(np.stack([1-b-c,b,c],2),0);w/=w.sum(2,keepdims=True);projected=np.sum(nn*w[:,:,:,None],2);dist=np.linalg.norm(projected-points[:,None,:],axis=2);best=np.argmin(dist,axis=1);weights=w[np.arange(len(points)),best];chosen=triangles[candidates[np.arange(len(points)),best]]
   pos[choose]=np.sum(a['pos'][chosen]*weights[:,:,None],axis=1)
   uv[choose]=np.sum(a['uv'][chosen]*weights[:,:,None],axis=1);color[choose]=a['colors'][chosen[:,0]];changed|=choose
   # A very small edge fold, without any new topology, bone indices or sections.
   edge=arm&(abs(t-limit)<.55)&~choose
   radial=pos[edge]-center-((pos[edge]-center)@axis)[:,None]*axis;length=np.maximum(np.linalg.norm(radial,axis=1,keepdims=True),1e-5)
   pos[edge]+=radial/length*.10;changed|=edge
   sides.append({'side':sign,'bare_forearm_vertices':int(choose.sum()),'cuff_fold_vertices':int(edge.sum()),'extension_from_UI3_cm':1.5,'max_skin_projection_cm':float(dist[np.arange(len(points)),best].max())})
  assert np.all(np.isfinite(pos))and np.all(np.isfinite(uv));assert np.array_equal(pos[~changed],r['pos'][~changed])
  out[r['pa']:r['pa']+r['n']*12]=pos.astype('<f4').tobytes();out[r['ua']:r['ua']+uv.size*2]=uv.astype('<f2').tobytes();out[r['ca']:r['ca']+color.size]=color.tobytes()
  reports.append({'lod':li,'vertices':r['n'],'changed':int(changed.sum()),'native_bone_indices_weights_section_palettes_untouched':True,'sides':sides})
 assert len(reports)==2
 return bytes(out),reports
source=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9299_mobile_and'");ns={};exec('class Writer:\n'+source,Bundle.write.__globals__,ns);write=ns['Writer'].write
bundle=object.__new__(Bundle);bundle.base=custom;bundle.files={};bundle.entries={};selected={}
for t in[base,custom]:
 for path,i in t.files.items():
  m=re.search(r'SK_(\d{3})([ad])(\d{2})\.uasset$',path)
  if m:selected[m.groups()]=(t,path,i)
report=[];failed=[];supported=set();headers={}
for(num,style,var),(t,path,i)in sorted(selected.items()):
 oldname='SK_'+num+style+var
 if oldname not in oldmap:failed.append(oldname);continue
 refpath='Body/SK_'+num+'b'+var+'.uasset'
 if refpath not in base.files:refpath='Body/SK_'+num+'b07.uasset'
 if refpath not in base.files:refpath='Body/SK_015b07.uasset'
 ri=base.files[refpath];raw=base.read(ri)
 try:edited,proof=build(raw,t.read(i),oldmap[oldname])
 except (ValueError,AssertionError)as e:failed.append(oldname+':'+str(e));continue
 refname=Path(refpath).stem;newnum=int(num)+2000;deststyle={'a':'b','d':'e'}[style];newname=f'SK_{newnum:03d}{deststyle}{var}';op='/Game/Assets/character/Body/'+refname;np_='/Game/Assets/character/Body/'+newname;edited=rename(edited,{refname:newname,op:np_},op,np_)
 if 'base'not in headers:headers['base']=parse_header(base.read(next(j for j,x in enumerate(base.ids)if x[11]==10)))
 h=headers['base'];oldpid=int.from_bytes(base.ids[ri][:8],'little');idb=struct.pack('<Q',pid(np_))+base.ids[ri][8:];bundle.put('character/Body/'+newname+'.uasset',idb,edited,store_entry(h['store'],h['pids'].index(oldpid)))
 report.append({'source':refname,'short_skin_donor':oldname,'destination':newname,'lods':proof});supported.add((int(num),int(var),int(style=='d')))
write(bundle,P/'payload/livedata');(P/'cuff-build.json').write_text(json.dumps({'models':report,'failed':failed,'count':len(report),'phone_tested':False},indent=2));(S/'rolled-models.h').write_text('/* Native long meshes; exact supported source IDs. */\nstatic const unsigned rolled_models[][3]={'+','.join('{%d,%d,%d}'%x for x in sorted(supported))+'};\n');print('CUFFS',len(report),'failed',len(failed))
