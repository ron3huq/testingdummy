from pathlib import Path
import sys,json
R=Path('/workspace/ronaldo-work');P=R/'73-ui4';sys.path.insert(0,str(R/'pes-fmdl-blender/pes-fmdl'));from FmdlFile import FmdlFile
from Ftex import ftexToDds
from PIL import Image
for label in['zidane','ferguson']:
 root=P/label;rows=[];bones={}
 for fn in['face_high.fmdl','hair_high.fmdl','suit.fmdl']:
  f=FmdlFile();source=next((P/'ferguson').rglob('suit.fmdl'))if fn=='suit.fmdl'else root/'fpk'/fn;f.readFile(str(source))
  for bone in f.bones:
   gp=bone.globalPosition;bones[bone.name]={'parent':bone.parent.name if bone.parent else None,'head':[gp.x,-gp.z,gp.y]}
  for mi,m in enumerate(f.meshes):
   pts=[];uv=[];weights=[];ix={id(v):i for i,v in enumerate(m.vertices)}
   for v in m.vertices:pts.append([v.position.x,-v.position.z,v.position.y]);uv.append([v.uv[0].u,1-v.uv[0].v]);weights.append({b.name:float(w)for b,w in v.boneMapping.items()})
   texture=None
   for role,t in m.materialInstance.textures:
    if role=='Base_Tex_SRGB':
     stem=Path(t.filename).stem;candidates=list((P/'ferguson'if fn=='suit.fmdl'else root).rglob(stem+'.ftex'))
     if not candidates:continue
     preferred=[q for q in candidates if any(part in str(getattr(t,'directory',''))for part in q.parts[-5:-2])];src=(preferred or candidates)[0];out=root/'blender-textures';out.mkdir(exist_ok=True);dst=out/(str(len(rows))+'-'+stem+'.dds');assert ftexToDds(str(src),str(dst));png=dst.with_suffix('.png');Image.open(dst).save(png);texture=str(png)
   rows.append(dict(name=fn+'-'+str(mi),material=m.materialInstance.name,positions=pts,uv=uv,weights=weights,triangles=[[ix[id(v)]for v in face.vertices]for face in m.faces],texture=texture))
 (root/'blender-model.json').write_text(json.dumps(dict(meshes=rows,bones=bones)))
 print(label,len(rows),len(bones))
