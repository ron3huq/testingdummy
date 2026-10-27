import bpy,numpy as np,sys
from pathlib import Path
R=Path('/workspace/analysis/five-faces-2026');sys.path.insert(0,str(R));from common import render_views
p=R/'orc/ORC_NECK2006_GAME.blend';bpy.ops.wm.open_mainfile(filepath=str(p));im=next(i for i in bpy.data.images if i.name.startswith('ORC final game atlas'));a=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(a);a=a.reshape(-1,4);from PIL import Image,ImageDraw
import json
geo=json.loads((R/'orc/native_geometry.json').read_text());mask=Image.new('L',(2048,2048));draw=ImageDraw.Draw(mask)
for tri in geo['triangles']:
 v=[geo['vertices'][i]for i in tri];x,y,z=np.mean([r['p']for r in v],axis=0)
 eye=abs(x)>.013 and abs(x)<.055 and 1.697<z<1.743 and y<-.10
 tusk=abs(x)>.032 and 1.617<z<1.703 and y<-.124
 if not (eye or tusk):draw.polygon([(r['uv'][0]*2047,r['uv'][1]*2047)for r in v],fill=255)
m=np.asarray(mask).ravel()>0;a[m,:3]=(.48,.29,.18);
im.pixels.foreach_set(a.ravel());im.filepath_raw=str(R/'orc/atlas.png');im.file_format='PNG';im.save();im.pack();bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True);render_views(R/'orc',.45);print('ORC_COLOUR_CLEAN_COMPLETE',int(m.sum()),flush=True)
