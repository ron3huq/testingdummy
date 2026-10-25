from pathlib import Path
import json,sys,struct,hashlib
import numpy as np
P=Path('/workspace/ronaldo-work/73-ui5')
source=(P/'build_manager_faces.py').read_text();exec(source[:source.index("for label,variant in")]);new=Toc(str(P/'payload/livedata/pc9302_mobile_and.utoc'));checks=[]
for row in json.loads((P/'manager-build.json').read_text()):
 name='SK_'+row['variant']+'_Face';path=ROOT+name+'.uasset';raw=new.read(new.files['character/DemoFace/Manager/'+name+'.uasset']);old=base.read(base.files[path]);log=(P/(name+'-new.log')).read_text();assert 'Exporting SkeletalMesh4 '+name in log
 for lod in [0,1]:
  m=Mesh(raw,log,lod);prior=Mesh(old,(P/(name+'.log')).read_text(),lod)
  assert len(m.positions)==row['vertices'] and len(m.indices)==row['triangles'];assert np.isfinite(m.positions).all();assert np.all(m.weights[:,4:].sum(1)==255)
  assert np.linalg.norm(m.positions.max(0)-m.positions.min(0))<65
  for group,section in enumerate(m.info):
   assert set(section['bones'])<=set(prior.info[min(group,len(prior.info)-1)]['bones'])|{7}
  # Real ported head must differ from the old actor in vertices and raw package.
  assert len(m.positions)!=len(prior.positions) and raw!=old
 checks.append({'manager':row['label'],'LODs':2,'vertices':row['vertices'],'triangles':row['triangles'],'native_reader':True,'finite_head_size':True})
# User-approved Y17 kit glyph textures are all unchanged bytes from UI4.
a=Toc(str(P.parent/'73-ui4/payload/livedata/pc9300_mobile_and.utoc'));b=Toc(str(P/'payload/livedata/pc9300_mobile_and.utoc'));glyphs=0
for path,i in a.files.items():
 if path.endswith('.uasset')and'/Coach/'not in path:
  assert b.read(b.files[path])==a.read(i),path;glyphs+=1
assert glyphs==40,glyphs
logos=[]
for path,i in new.files.items():
 if 'emblemOther-UI5_'not in path:continue
 raw=new.read(i);at=raw.rfind(b'PF_B8G8R8A8\0')+len(b'PF_B8G8R8A8\0');first,count=struct.unpack_from('<II',raw,at);at+=8;_,flags,n,size,offset=struct.unpack_from('<IIIIq',raw,at);at+=24;w,h,depth=struct.unpack_from('<III',raw,at+n);assert w==h and w in[64,128,256]and w*h*4==n
 img=np.frombuffer(raw[at:at+n],dtype='u1').reshape(h,w,4);yy,xx=np.where(img[:,:,3]>8);assert len(xx)>0;assert min(xx)>0 and max(xx)<w-1 and min(yy)>0 and max(yy)<h-1;logos.append({'path':path,'size':w})
assert len(logos)==18
assert not any('emblemOther-national' in p for p in new.files)
(P/'art-assets-validation.json').write_text(json.dumps({'passed':True,'managers':checks,'unchanged_kit_glyph_assets':glyphs,'private_logos':logos,'android_gpu_tested':False},indent=2));print('ART_ASSETS_PASS',glyphs,len(logos))
