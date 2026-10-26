from pathlib import Path
import sys,json
import numpy as np
from PIL import Image,ImageOps
from scipy import ndimage
sys.path.insert(0,'/tmp/73-ui79/devdeps');import onnxruntime as ort
P=Path('/tmp/73-ui79');session_options=ort.SessionOptions();session_options.intra_op_num_threads=2;session_options.inter_op_num_threads=1;session=ort.InferenceSession(str(P/'u2netp.onnx'),session_options,providers=['CPUExecutionProvider']);input_name=session.get_inputs()[0].name

def cutout(image,white=False):
 im=image.convert('RGBA');rgb=np.array(im)[:,:,:3];size=(320,320);a=np.array(im.convert('RGB').resize(size,Image.Resampling.LANCZOS)).astype('float32');a/=max(1,float(a.max()));a=(a-np.array([.485,.456,.406],dtype='float32'))/np.array([.229,.224,.225],dtype='float32');out=session.run(None,{input_name:a.transpose(2,0,1)[None]})[0][0,0];out=(out-out.min())/max(1e-7,out.max()-out.min());mask=np.array(Image.fromarray(np.uint8(np.clip(out*255,0,255))).resize(im.size,Image.Resampling.LANCZOS));old=np.array(im)[:,:,3];mask=np.minimum(old,mask)
 if white:
  nearwhite=(rgb.min(2)>240)&(rgb.max(2)-rgb.min(2)<12);labels,num=ndimage.label(nearwhite);edge=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));background=np.isin(labels,edge[edge>0]);mask[background]=0
 return Image.fromarray(np.dstack([rgb,mask]).astype('uint8'),'RGBA')

def prepare(pid,box):
 im=Image.open(P/'input/images'/(pid+'.png')).convert('RGBA');cut=cutout(im,white=True);a=np.array(cut);# Preserve all source face colours and its opaque interior; only alpha changes.
 x0,y0,x1,y1=box;ys=slice(max(0,y0),min(im.height,y1));xs=slice(max(0,x0),min(im.width,x1));region=a[ys,xs,3];region_rgb=a[ys,xs,:3];region[(region>180)|(region_rgb.min(2)<230)]=255;cut=Image.fromarray(a);cut.save(P/'art'/(pid+'-cutout.png'));bounds=cut.getchannel('A').point(lambda v:255 if v>24 else 0).getbbox();assert bounds
 # Complete source pose contained in the large184x256 canvas; one uniform scale, never squash.
 full=cut.crop(bounds);large=Image.new('RGBA',(184,256));fit=ImageOps.contain(full,(176,244),Image.Resampling.LANCZOS);large.alpha_composite(fit,((184-fit.width)//2,256-fit.height));large.save(P/'art'/(pid+'-large.png'))
 # Head/shoulders crop is independent of the full-body pose's width.
 headw=x1-x0;headh=y1-y0;side=max(headw/0.60,headh/0.67);cx=(x0+x1)/2;top=y0-(side-headh)*.25;crop=cut.crop((round(cx-side/2),round(top),round(cx+side/2),round(top+side)));small=ImageOps.contain(crop,(128,128),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(128,128));canvas.alpha_composite(small,((128-small.width)//2,(128-small.height)//2));canvas.save(P/'art'/(pid+'-small.png'));return {'id':pid,'source_size':list(im.size),'face_box':box,'full_pose_bounds':bounds,'large_fit':list(fit.size),'large_size':[184,256],'small_size':[128,128],'uniform_scale_only':True,'face_pixels_not_regenerated':True}
rows=[]
# Explicit source-pixel boxes checked against the supplied full photographs.
for pid,box in [('89135066911146',(645,635,873,883)),('89138556572074',(260,68,366,202)),('88044950524330',(275,7,388,192))]:rows.append(prepare(pid,box))
(P/'portrait-layouts.json').write_text(json.dumps(rows,indent=2));print('RONALDO_LAYOUTS',rows)
