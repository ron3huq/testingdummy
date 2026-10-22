from pathlib import Path
import sys,json
from PIL import Image
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'pes-fmdl-blender/pes-fmdl'))
from FmdlFile import FmdlFile
from Ftex import ftexToDds
out=ROOT/'converted';out.mkdir(exist_ok=True)
report={'models':{},'textures':{}}
for p in sorted((ROOT/'source-extracted').glob('*.fmdl')):
 f=FmdlFile();f.readFile(str(p))
 data={'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'local':vars(b.localPosition),'global':vars(b.globalPosition)} for b in f.bones], 'materials':[{'name':m.name,'shader':m.shader,'technique':m.technique,'textures':[(r,vars(t)) for r,t in m.textures]} for m in f.materialInstances], 'meshes':[]}
 for m in f.meshes:
  data['meshes'].append({'vertices':len(m.vertices),'triangles':len(m.faces),'material':m.materialInstance.name,'alpha_flags':m.alphaFlags,'uv_sets':m.vertexFields.uvCount,'weighted_vertices':sum(bool(v.boneMapping) for v in m.vertices),'weight_sum_range':[min(sum(v.boneMapping.values()) for v in m.vertices),max(sum(v.boneMapping.values()) for v in m.vertices)] if m.vertexFields.hasBoneMapping else None})
 report['models'][p.name]=data
for p in sorted((ROOT/'source-extracted').glob('*.ftex')):
 dds=out/(p.stem+'.dds')
 try:
  ok=ftexToDds(str(p),str(dds)); im=Image.open(dds);im.load();im.save(out/(p.stem+'.png'))
  report['textures'][p.name]={'converted':bool(ok),'size':im.size,'mode':im.mode}
 except Exception as e: report['textures'][p.name]={'error':str(e)}
(ROOT/'model-analysis.json').write_text(json.dumps(report,indent=2))
for k,v in report['models'].items():print(k,'bones',len(v['bones']),'meshes',v['meshes'],'materials',v['materials'])
print(report['textures'])
