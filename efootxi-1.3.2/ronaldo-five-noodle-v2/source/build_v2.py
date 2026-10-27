from pathlib import Path
import sys,json,math,shutil,hashlib
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
R=Path(__file__).parent;V=R/'v2';V.mkdir(exist_ok=True);P=Path('/workspace/analysis/my-league/ronaldo-pc-conversion');sys.path.insert(0,str(P/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
fits=json.loads((R/'eye-fits-v2.json').read_text());targets=json.loads((R/'targets.json').read_text());(V/'targets.json').write_text(json.dumps(targets,indent=2))
common_eye=Image.open(R/'android-source/105577812455608/eye_sclera_bsm.png').convert('RGB');report={}
def rows(mesh):
 vv=[];ix={id(v):i for i,v in enumerate(mesh.vertices)}
 for v in mesh.vertices:
  p=v.position;n=v.normal;t=v.tangent;vv.append({'p':[p.x,-p.z,p.y],'n':[n.x,-n.z,n.y],'tangent':[t.x,-t.z,t.y,t.w],'uv':[v.uv[0].u,1-v.uv[0].v],'uv2':[3.0517578125e-5]*2,'weights':{b.name:w for b,w in v.boneMapping.items()if w>0}})
 return vv,[[ix[id(v)]for v in reversed(t.vertices)]for t in mesh.faces]
for card,target in targets.items():
 original=R/'original-models'/card;out=V/card;out.mkdir(exist_ok=True);f=FmdlFile();f.readFile(str(original/'face_high.fmdl'));h=FmdlFile();h.readFile(str(original/'hair_high.fmdl'));donor=FmdlFile();donor.readFile(str(R/'android-source'/card/'hair_high.fmdl'));face=[];tri=[];parts=[]
 for name,model in [('original_face',f),('original_scalp_shell',h)]:
  for mi,m in enumerate(model.meshes):
   if m.materialInstance.name not in ['fox_skin_mat','fox_head_shell_mat']:continue
   vv,tt=rows(m);start=len(face);face+=vv;tri.extend([[start+i for i in t]for t in tt]);parts.append({'source':name,'mesh':mi,'material':m.materialInstance.name,'start':start,'count':len(vv),'source_positions_sha256':hashlib.sha256(np.array([r['p']for r in vv],dtype='<f4').tobytes()).hexdigest()})
 skin_count=len(face);source_uv=[v['uv'].copy()for v in face];original_positions=np.array([v['p']for v in face],dtype='<f4');valid=[r for r in face if r['weights']];tree=cKDTree([r['p']for r in valid]);missing=0
 for row in face:
  if not row['weights']:row['weights']=valid[tree.query(row['p'])[1]]['weights'].copy();missing+=1
 # Keep UV splits and all original coordinates; bind coincident seam copies alike.
 groups={}
 for i,row in enumerate(face):groups.setdefault(tuple(round(x,7)for x in row['p']),[]).append(i)
 seam_copies=0
 for indices in groups.values():
  first=indices[0]
  for i in indices[1:]:
   if face[i]['weights']!=face[first]['weights']:face[i]['weights']=face[first]['weights'].copy();seam_copies+=1
 for row in face:row['uv']=[row['uv'][0]*.5,.5+row['uv'][1]*.5]
 eyes=[]
 for side,fit in zip(['l','r'],fits[card]):
  cx,cz=fit['center'];cy=fit['front_y']+.010;rx,ry,rz=.014,.010,.011;start=len(face);nt=len(tri);segments=40;rings=20
  for j in range(rings+1):
   phi=math.pi*j/rings
   for i in range(segments+1):
    theta=math.tau*i/segments;dx=rx*math.sin(phi)*math.cos(theta);dy=ry*math.sin(phi)*math.sin(theta);dz=rz*math.cos(phi);normal=np.array([dx/rx**2,dy/ry**2,dz/rz**2]);normal/=max(1e-12,np.linalg.norm(normal));u=np.clip(.5+dx/.022,.015,.985);v=np.clip(.5+dz/.022,.015,.985)
    face.append({'p':[cx+dx,cy+dy,cz+dz],'n':normal.tolist(),'tangent':[1,0,0,1],'uv':[.5+.5*float(u),.5+.5*float(v)],'uv2':[3.0517578125e-5]*2,'weights':{'skf_eye_'+side:1.}})
  for j in range(rings):
   for i in range(segments):
    a=start+j*(segments+1)+i;b=a+segments+1
    if j>0:tri.append([a,b,a+1])
    if j<rings-1:tri.append([a+1,b,b+1])
  eyes.append({'side':side,'start':start,'count':len(face)-start,'triangles':len(tri)-nt,'center':[cx,cy,cz],'radii':[rx,ry,rz],'bone':'skf_eye_'+side})
 hairm=next(m for m in donor.meshes if m.materialInstance.name=='Material.002');hv,ht=rows(hairm);auv=np.load(R/'atlas_uv.npy')
 for i,row in enumerate(hv):row['uv']=[float(auv[i,0]),float(1-auv[i,1])]
 assert np.array_equal(original_positions,np.array([r['p']for r in face[:skin_count]],dtype='<f4'))
 g={'face':face,'face_triangles':tri,'hair':hv,'hair_triangles':ht,'original_skin_count':skin_count,'original_parts':parts,'source_uv':source_uv,'eyes':eyes};(out/'game_geometry.json').write_text(json.dumps(g))
 atlas=Image.new('RGB',(2048,2048));im=Image.open(R/'android-source'/card/'face_bsm_alp.png').convert('RGB');assert im.size==(1024,1024);atlas.paste(im,(0,0));atlas.paste(im,(0,1024));atlas.paste(common_eye.resize((1024,1024)),(1024,0));atlas.paste(common_eye.resize((1024,1024)),(1024,1024));atlas.save(out/'face-atlas-2048.png')
 N=P/('android-r5-v2-'+card);N.mkdir(exist_ok=True);S=P/('android-ronaldo-hair-'+card)
 for filename in ['build_pc_head.py','build_face_textures.py','build_materials.py','zen_clone.py']:
  s=(S/filename).read_text().replace(str(R/'android-source'/card/'game_geometry.json'),str(out/'game_geometry.json'))
  if filename=='build_face_textures.py':s=s.replace('1024','2048').replace('==11','==12').replace('range(11)','range(12)').replace('pre_end-4,11','pre_end-4,12')
  (N/filename).write_text(s)
 for folder in ['reference','material-reference']:shutil.copytree(S/folder,N/folder,dirs_exist_ok=True)
 (N/'asset').mkdir(exist_ok=True);report[card]={'parts':parts,'original_skin_positions_bit_identical':True,'skin_count':skin_count,'source_missing_weights':missing,'seam_weight_copies_synchronized':seam_copies,'eyes_in_game_mesh':eyes,'donor_strand_vertices':len(hv),'donor_scalp_used':False,'face_texture_original_pixels_preserved':True}
(V/'source-validation.json').write_text(json.dumps(report,indent=2));print('V2_GEOMETRY_AND_TEXTURES_PREPARED',flush=True)
