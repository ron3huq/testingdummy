import bpy,json,sys
from pathlib import Path
R=Path('/workspace/analysis/five-faces-2026');sys.path.insert(0,str(R));from common import smooth
def native_weights(p):
 z=p[2];h=smooth((z-1.405)/.095);c=smooth((z-1.445)/.10);chest=(1-h)*(1-c);return {"sk_head":h,"sk_cervicalspine_02":1-h-chest,"sk_spine_03":chest}
for k in ['orc','naruto']:
 p=R/k/'native_geometry.json';g=json.loads(p.read_text())
 for v in g['vertices']:v['weights']={name:w for name,w in native_weights(v['p']).items()if w>1e-8}
 p.write_text(json.dumps(g))
 b=R/k/(k.upper()+'_NECK2006_GAME.blend');bpy.ops.wm.open_mainfile(filepath=str(b));o=next(o for o in bpy.data.objects if o.type=='MESH')
 for group in list(o.vertex_groups):o.vertex_groups.remove(group)
 for name in ['sk_head','sk_cervicalspine_02','sk_spine_03']:o.vertex_groups.new(name=name)
 for v in o.data.vertices:
  for name,w in native_weights(v.co).items():
   if w>1e-8:o.vertex_groups[name].add([v.index],w,'REPLACE')
 bpy.ops.wm.save_as_mainfile(filepath=str(b),compress=True)
print('WEIGHTS_FIXED')
