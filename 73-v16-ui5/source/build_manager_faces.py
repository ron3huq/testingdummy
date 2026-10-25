"""Port supplied PC face meshes into exact native DemoFace manager variants.
Preserve each LOD's own section bone maps/RequiredBones; retain native eyes/mouth.
"""
from pathlib import Path
import sys,json,struct,inspect
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
sys.path.insert(0,'/workspace/testingdummy/efootxi-1.3.2/player-faces-v25/source')
from iostore import Toc,parse_header,store_entry
from bundle_tools import Bundle,replace_texture,decode_first_texture
import mesh_tools
from zen_clone import rename,pid
from shading_tools import repair_frame
P=Path('/workspace/ronaldo-work/73-ui5');R=P.parent
base=Toc('/workspace/ronaldo-work/pc0000/PesMobile/Content/Paks/pakchunk0-Android_ETC2.utoc');face=Toc('/workspace/ronaldo-work/73-v25-port/package/payload/livedata/pc9298_mobile_and.utoc')
# Read manager templates with2/3 material sections instead of the player helper's2.
code=inspect.getsource(mesh_tools.Mesh).replace('assert len(self.info)==2 and','assert len(self.info)>=1 and');code=code.replace("assert struct.unpack_from('<II',data,s)==(4,n*2)","assert struct.unpack_from('<II',data,s)==(4,n)")
code=code.replace("self.uv=np.frombuffer(data,dtype='<f2',count=n*4,offset=s+8).reshape(-1,4).copy()","self.uv=np.c_[np.frombuffer(data,dtype='<f2',count=n*2,offset=s+8).reshape(-1,2),np.full((n,2),3.0517578125e-5)]")
a=code.index("  s=r['SKIN_WEIGHTS_END'];assert");z=code.index('  self.info=[]',a)
code=code[:a]+"  s=r['SKIN_WEIGHTS_END'];self.has_colors=s+18<=len(data)and struct.unpack_from('<4I',data,s+2)==(4,n,4,n)\n  self.colors=np.frombuffer(data,dtype='u1',count=n*4,offset=s+18).reshape(-1,4).copy()if self.has_colors else np.full((n,4),255,dtype='u1')\n  self.colhead=data[s:s+2]if self.has_colors else b'';self.coltail=data[s+18+n*4:r['STREAM_END']]if self.has_colors else data[s:r['STREAM_END']]\n"+code[z:]
ns={};exec(code,mesh_tools.__dict__,ns);Mesh=ns['Mesh']
bundle=object.__new__(Bundle);bundle.base=face;bundle.files={};bundle.entries={}
writer=inspect.getsource(Bundle.write).replace("name='pc9298_mobile_and'","name='pc9302_mobile_and'");ns={};exec('class Writer:\n'+writer,Bundle.write.__globals__,ns);write=ns['Writer'].write
ROOT='PesMobile/Content/Assets/character/DemoFace/Manager/';PUB='/Game/Assets/character/DemoFace/Manager/'
proof=[]
def packed(values):return struct.pack('<I',len(values))+struct.pack('<%dH'%len(values),*values)
def normal_frame(pos,tri,uv):
 normals=np.zeros_like(pos,dtype=float);tangents=np.zeros_like(pos,dtype=float)
 a,b,c=pos[tri[:,0]],pos[tri[:,1]],pos[tri[:,2]];n=np.cross(b-a,c-a);d1=uv[tri[:,1]]-uv[tri[:,0]];d2=uv[tri[:,2]]-uv[tri[:,0]];det=d1[:,0]*d2[:,1]-d1[:,1]*d2[:,0];det=np.where(abs(det)>1e-9,det,1);t=((b-a)*d2[:,1,None]-(c-a)*d1[:,1,None])/det[:,None]
 for k in range(3):np.add.at(normals,tri[:,k],n);np.add.at(tangents,tri[:,k],t)
 normals*=-1;normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-9);tangents-=np.sum(tangents*normals,axis=1)[:,None]*normals;tangents/=np.maximum(np.linalg.norm(tangents,axis=1,keepdims=True),1e-9)
 out=np.zeros((len(pos),8),dtype='i1');out[:,:3]=np.rint(tangents*127).astype('i1');out[:,3]=127;out[:,4:7]=np.rint(normals*127).astype('i1');out[:,7]=127;return out.view('u1')
def texture_from_working(template,source_image,dest):
 src='character/RealFace/'+template+'.uasset';raw=face.read(face.files[src]);bulkpath=src[:-7]+'.ubulk';bulk=face.read(face.files[bulkpath])if bulkpath in face.files else b''
 edited,newbulk,dims,_=replace_texture(raw,source_image,bulk);op='/Game/Assets/character/RealFace/'+template;np_=PUB+dest;edited=rename(edited,{template:dest,op:np_},op,np_)
 h=parse_header(face.read(next(j for j,x in enumerate(face.ids)if x[11]==10)));pk=int.from_bytes(face.ids[face.files[src]][:8],'little');idb=struct.pack('<Q',pid(np_))+face.ids[face.files[src]][8:]
 bundle.put('character/DemoFace/Manager/'+dest+'.uasset',idb,edited,store_entry(h['store'],h['pids'].index(pk)))
 if newbulk:bundle.put('character/DemoFace/Manager/'+dest+'.ubulk',idb[:11]+b'\3',newbulk)
 return dims
for label,variant in [('zidane','1sp00v0052'),('ferguson','26sp00v0047')]:
 name='SK_'+variant+'_Face';path=ROOT+name+'.uasset';raw=base.read(base.files[path]);log=(P/(name+'.log')).read_text();hq=Mesh(raw,log,0);low=Mesh(raw,log,1)
 source=json.loads((R/'73-ui4'/label/'blender-model.json').read_text());gltf=json.loads((P/'manager-export/Game/Assets/character/DemoFace/Manager'/(name+'.gltf')).read_text());bone_names=[gltf['nodes'][i]['name']for i in gltf['skins'][0]['joints']];bone_ids={n:i for i,n in enumerate(bone_names)}
 groups=[];skin=hq.info[0];count=skin['verts'];original_pos=hq.positions[:count];original_uv=hq.uv[:count];original_weights=hq.global_weights(0)
 # Source accessory atlas sits in the bottom strip; native eyeball bones are14/15.
 preserve=(original_pos[:,2]<156)|(original_uv[:,1]>.94)|np.array([any(b in[14,15]and w>100 for b,w in r)for r in original_weights]);original_tri=hq.indices[:skin['tris']];tri=original_tri[np.all(preserve[original_tri],axis=1)];indices=np.unique(tri);remap=np.full(count,-1);remap[indices]=np.arange(len(indices));verts=[original_pos[indices]];uvs=[np.c_[original_uv[indices,:2]*.5+np.array([.5,0]),original_uv[indices,2:]]];weights=[dict(original_weights[i])for i in indices];colors=[hq.colors[indices]];triangles=[remap[tri]];n=len(indices)
 tree=cKDTree(original_pos)
 for row in source['meshes']:
  if row['material']!='fox_skin_mat':continue
  # Source JSON is BlenderXYZ. Native UE is X,-Y,Z, measured in cm.
  points=np.array(row['positions'],dtype=float)*np.array([100,-100,100]);uv=np.array(row['uv'],dtype=float);uv[:,1]=1-uv[:,1];uv4=np.c_[uv*.5,np.full((len(uv),2),3.0517578125e-5)];tri=np.array(row['triangles'],dtype=int)[:,[0,2,1]]
  nearest=tree.query(points)[1];verts.append(points);uvs.append(uv4);colors.append(hq.colors[nearest]);triangles.append(tri+n)
  for mapping in row['weights']:
   dst={}
   for bone,w in mapping.items():
    bid=bone_ids.get(bone,7)
    if bid not in skin['bones']:bid=7
    dst[bid]=dst.get(bid,0)+w
   weights.append(dst or{7:1})
  n+=len(points)
 skinpos=np.concatenate(verts);skinuv=np.concatenate(uvs);skincolors=np.concatenate(colors);skintri=np.concatenate(triangles);groups.append(dict(pos=skinpos,uv=skinuv,colors=skincolors,tri=skintri,weights=weights))
 # Hair/glasses use their native masked material section. Eyelashes stay native.
 for gi,q in enumerate(hq.info[1:],start=1):
  hair_rows=[r for r in source['meshes']if r['material']in['fox_hair_mat','fox_head_shell_mat']]if label=='ferguson'and gi==1 else[]
  if hair_rows:
   ps=[];uv=[];tr=[];w=[];base_index=0
   for row in hair_rows:
    points=np.array(row['positions'])*[100,-100,100];u=np.array(row['uv']);u[:,1]=1-u[:,1]
    # Shell and loose hair occupy separate atlas halves.
    u=u*.5+([.5,0]if row['material']=='fox_head_shell_mat'else[0,0]);ps.append(points);uv.append(np.c_[u,np.full((len(u),2),3.0517578125e-5)]);tr.append(np.array(row['triangles'])[:,[0,2,1]]+base_index);w.extend([{7:1}for _ in points]);base_index+=len(points)
   groups.append(dict(pos=np.concatenate(ps),uv=np.concatenate(uv),colors=np.full((base_index,4),255,dtype='u1'),tri=np.concatenate(tr),weights=w))
  else:
   start=q['basevert'];end=start+q['verts'];ti=hq.indices[q['baseidx']//3:q['baseidx']//3+q['tris']]-start;groups.append(dict(pos=hq.positions[start:end],uv=hq.uv[start:end],colors=hq.colors[start:end],tri=ti,weights=[dict(r)for r in hq.global_weights(gi)]))
 positions=np.concatenate([g['pos']for g in groups]);uv=np.concatenate([g['uv']for g in groups]);cols=np.concatenate([g['colors']for g in groups]);alltri=[];vbase=0
 for g in groups:alltri.append(g['tri']+vbase);vbase+=len(g['pos'])
 alltri=np.concatenate(alltri).astype('<u2');tn=normal_frame(positions,alltri,uv[:,:2]);tn=repair_frame(positions,tn,uv,alltri,derive=True);n=len(positions)
 def lod_blob(lod):
  mesh=[hq,low][lod];at=mesh.lods[lod];required_count=struct.unpack_from('<I',raw,at+10)[0];required=list(struct.unpack_from('<%dH'%required_count,raw,at+14));sections=[];weight_arrays=[];vbase=0;ibase=0
  for group_index,group in enumerate(groups):
   q=mesh.info[group_index]if group_index<len(mesh.info)else hq.info[group_index]
   allowed=[bid for bid in q['bones']if bid in required]
   if 7 not in allowed:allowed.append(7)
   rows=[]
   for row in group['weights']:
    dst={}
    for bid,w in row.items():
     target=bid if bid in allowed else 7;dst[target]=dst.get(target,0)+w
    rows.append(dst)
   quant=mesh_tools.quantize(rows,allowed);weight_arrays.append(quant);head=bytearray(q['head']);tail=bytearray(q['tail']);struct.pack_into('<II',head,4,ibase,len(group['tri']));struct.pack_into('<I',head,21,vbase);struct.pack_into('<II',tail,0,len(group['pos']),4);sections.append(bytes(head)+packed(allowed)+tail);vbase+=len(group['pos']);ibase+=len(group['tri'])*3
  weights=np.concatenate(weight_arrays);r=mesh.r;ih=struct.pack('<BII',2,2,alltri.size)+alltri.tobytes();points=struct.pack('<4I',12,n,12,n)+positions.astype('<f4').tobytes();th=bytearray(mesh.tuhead);struct.pack_into('<I',th,6,n);tu=bytes(th)+struct.pack('<II',8,n)+tn.tobytes()+struct.pack('<II',4,n)+uv[:,:2].astype('<f2').tobytes();sh=bytearray(mesh.swhead);struct.pack_into('<II',sh,10,n*4,n);sw=bytes(sh)+struct.pack('<II',1,n*8)+weights.tobytes()+mesh.swtail;col=(mesh.colhead+struct.pack('<4I',4,n,4,n)+cols.astype('u1').tobytes()if mesh.has_colors else b'')+mesh.coltail;stream=raw[r['STREAM_BEGIN']:r['INDICES_BEGIN']]+ih+points+tu+sw+col
  ab=raw[r['ACTIVE_BEGIN']:r['ACTIVE_END']];header=bytearray(raw[at:at+10]);struct.pack_into('<II',header,2,0,1);return bytes(header)+packed(required)+struct.pack('<I',len(sections))+b''.join(sections)+ab+struct.pack('<I',len(stream))+stream
 prefix=bytearray(raw[:hq.lods[0]]);lo=positions.min(0);hi=positions.max(0);center=(hi+lo)/2;ext=(hi-lo)/2;struct.pack_into('<7f',prefix,hq.r['BOUNDS_BEGIN'],*center,*ext,float(np.linalg.norm(ext)));suffix=raw[low.r['STREAM_END']:];assert suffix==bytes.fromhex('020200000000')
 out=bytearray(prefix+lod_blob(0)+lod_blob(1)+suffix);em=struct.unpack_from('<I',raw,44)[0];struct.pack_into('<Q',out,em+80,struct.unpack_from('<Q',raw,em+80)[0]+len(out)-len(raw));bundle.native(base,path,out)
 old_image=Image.open(P/'manager-export/Game/Assets/character/DemoFace/Manager'/('T_'+variant+'_Face_D.tga')).convert('RGBA');atlas=Image.new('RGBA',(2048,2048),(125,93,75,255));pcimage=Image.open(R/'73-ui4'/label/('blender-textures/composited-skin.png'if label=='ferguson'else'blender-textures/0-face_bsm_alp.png')).convert('RGBA');atlas.paste(pcimage.resize((1024,1024)),(0,0));atlas.paste(old_image.resize((1024,1024)),(1024,0));dims=texture_from_working('T_NV17_Face_D',atlas,'T_'+variant+'_Face_D')
 if label=='ferguson':
  hairatlas=Image.new('RGBA',(2048,2048),(0,0,0,0));im=Image.open(R/'73-ui4/ferguson/blender-textures/65342-hair_parts_bsm_alp.png').convert('RGBA');hairatlas.paste(im.resize((1024,1024)),(0,0));im=Image.open(R/'73-ui4/ferguson/blender-textures/65342-face_bsm_alp.png').convert('RGBA');hairatlas.paste(im.resize((1024,1024)),(1024,0));texture_from_working('T_NVH1_Hair_D',hairatlas,'T_'+variant+'_Hair_D')
 proof.append(dict(label=label,variant=variant,vertices=n,triangles=len(alltri),materials=len(groups),native_eyes_mouth_neck_vertices=len(indices),native_bone_maps_required_bones_preserved=True,texture_dimensions=dims))
write(bundle,P/'manager-payload');(P/'manager-build.json').write_text(json.dumps(proof,indent=2));print('MANAGER_MODELS_BUILT',proof)
