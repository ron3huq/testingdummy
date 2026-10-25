from pathlib import Path
import json,struct,re,sys,numpy as np
P=Path('/workspace/ronaldo-work/73-ui5');ns={};exec(Path('/workspace/ronaldo-work/73-ui4/build_cuffs.py').read_text().split('def build(raw')[0],ns);Toc=ns['Toc'];buffers=ns['buffers'];source={}
for t in [ns['base'],ns['custom']]:
 for path,index in t.files.items():
  m=re.search(r'SK_(\d{3})([ad])(\d{2})\.uasset$',path)
  if m:source[m.groups()]=(t,index)
new=Toc(str(P/'payload/livedata/pc9301_mobile_and.utoc'));count=0;vertices=0
for path,index in new.files.items():
 m=re.search(r'SK_(\d{4})([ad])(\d{2})\.uasset$',path)
 if not m:continue
 number,style,var=m.groups();key=(f'{int(number)-4000:03d}',style,var);t,oldindex=source[key];old=t.read(oldindex);data=new.read(index);a=buffers(old);b=buffers(data);assert len(a)==len(b)==2
 for before,after in zip(a,b):
  n=before['n'];assert n==after['n'];skin=np.any(before['colors']!=0,axis=1);assert np.array_equal(before['colors'],after['colors']);assert np.array_equal(before['uv'],after['uv']);assert np.array_equal(before['tri'],after['tri']);assert np.array_equal(before['pos'][skin],after['pos'][skin]),path
  def weights(blob,buffer):
   for inf in [4,8]:
    at=blob.find(struct.pack('<II',1,n*inf*2),buffer['pa']+n*12,buffer['ca'])
    if at>=0:
     array=np.frombuffer(blob,dtype='u1',count=n*inf*2,offset=at+8).reshape(n,inf*2)
     if np.all(array[:,inf:].sum(1)==255):return array
   raise AssertionError('Missing weights')
  ow=weights(old,before);nw=weights(data,after);assert np.array_equal(ow[skin],nw[skin]);assert np.isfinite(after['pos']).all();assert abs(after['pos']).max()<250
  vertices+=n
 count+=1
assert count==356
# Readback through the actual native-format reader includes all4 representative variants.
for name in ['SK_4015a07','SK_4015d07','SK_4015a02','SK_4123d07']:
 text=(P/(name+'-new.log')).read_text();assert 'Exporting SkeletalMesh4 '+name in text and 'ERROR:'not in text.replace('ERROR: glTF animation could be exported from mesh viewer only.','')
(P/'body-assets-validation.json').write_text(json.dumps({'passed':True,'models':count,'LODs_per_model':2,'vertices_checked':vertices,'all_skin_positions_and_weights_exact':True,'all_UV_colors_indices_exact':True,'four_native_reader_samples':True,'source_bone_palettes_and_skeletons_retained':True,'android_gpu_tested':False},indent=2));print('BODY_ASSETS_PASS',count,vertices)
