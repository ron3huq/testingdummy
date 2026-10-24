import bpy,sys
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath).parent;s=bpy.context.scene;s.render.resolution_x=650;s.render.resolution_y=760;s.render.resolution_percentage=100;s.cycles.samples=24
for label,loc in [('front',(0,-.70,1.77)),('right',(-.65,-.04,1.74)),('left',(.65,-.04,1.74)),('back',(0,.65,1.73)),('three-quarter',(-.27,-.65,1.80))]:
 cam=s.camera;cam.location=loc;cam.rotation_euler=(Vector((0,-.065,1.72))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.37;s.render.filepath=str(p/(label+'.png'));bpy.ops.render.render(write_still=True)
