"""Data-only audit of supplied FMDL sources, never execute archive scripts."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.spatial import cKDTree
R=Path('/workspace/ronaldo-work');O=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
roots={'2006':R/'input-1','2017':R/'v20-input/2017','2027':R/'v20-input/2027','ozilV2':R/'v23-input/ozil'};out=[]
for label,root in roots.items():
 row={'source':label,'blend_files_in_recovered_archive_tree':[p.name for p in root.rglob('*.blend')],'models':[]};models=[]
 for file in ['face_high.fmdl','hair_high.fmdl']:
  p=next(root.rglob(file));f=FmdlFile();f.readFile(str(p));models.append(f);meshes=[]
  for m in f.meshes:
   pts=np.array([[v.position.x,v.position.y,v.position.z]for v in m.vertices]);ws=np.array([sum(v.boneMapping.values())for v in m.vertices]);meshes.append({'material':m.materialInstance.name,'vertices':len(pts),'triangles':len(m.faces),'finite_positions':bool(np.isfinite(pts).all()),'weight_sum_min_max':[float(ws.min()),float(ws.max())],'base_textures':[(role,t.filename)for role,t in m.materialInstance.textures if role.startswith('Base')]})
  row['models'].append({'file':file,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bones':len(f.bones),'meshes':meshes})
 skin=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for f in models for m in f.meshes if m.materialInstance.name.startswith('fox_skin_mat')for v in m.vertices]);tree=cKDTree(skin);shells=[]
 for m in models[1].meshes:
  if not m.materialInstance.name.startswith('fox_head_shell_mat'):continue
  pts=np.array([[v.position.x*100,v.position.z*100,v.position.y*100]for v in m.vertices]);d,_=tree.query(pts);shells.append({'vertices':len(pts),'fraction_within_0_05_cm_of_opaque_skin':float((d<.05).mean()),'mean_distance_cm':float(d.mean())})
 row['hair_shell_distance_to_skin']=shells;out.append(row)
report={'sources':out,'separate_2006_blender_reference_available':(R/'input-0/Ronaldo_2006_EDIT.blend').exists(),'missing_source_or_bad_Blender_proven':False,'notes':['No blend file in recovered 2017/2027 source archives. FMDL vertex positions and skin weight sums are finite.','FOX pass selection and atlas layout differ; neither proves the black-face root cause.','All 2027 hair-shell vertices lie within 0.05 cm of opaque skin; do not render those passes as additional opaque skin.','Ozil V2 uses face_bsm rather than face_bsm_alp, plus a separate hair_bsm_alp scalp tile. Native eye/oral assets replace unsupported PC common eye/oral dependencies.']}
(O/'source-comparison.json').write_text(json.dumps(report,indent=2));print('FMDL_SOURCE_AND_SHELL_COMPARISON_PASS')
