exec(open('/tmp/73-ui79/prepare_portraits.py').read().split('def prepare(')[0])
def clean(image):
 arr=np.array(image);labels,n=ndimage.label(arr[:,:,3]>24)
 if n:
  sizes=np.bincount(labels.ravel());sizes[0]=0;main=int(sizes.argmax());keep=ndimage.binary_dilation(labels==main,iterations=2);arr[:,:,3]=np.where(keep,arr[:,:,3],0)
 return Image.fromarray(arr)
P=Path('/tmp/73-ui711');A=P/'art';A.mkdir(exist_ok=True);rows=[]
# Source-space hair-to-chin rectangles, checked against the supplied photographs.
boxes={'105563585358239':(610,180,945,665),'105758469512061':(835,225,1210,700),'105837926394281':(900,110,1250,670),'106654775417922':(755,110,1060,545),'88040387132864':(680,670,925,1010),'88044950524330':(275,39,384,190)}
for card,box in boxes.items():
 f=P/'input/Image'/(card+'.png')if card!='88044950524330'else Path('/tmp/73-ui79/input/images/88044950524330.png');im=Image.open(f).convert('RGBA');cut=cutout(im,white=True)
 if card=='105837926394281':
  arr=np.array(im);rgb=arr[:,:,:3];nearwhite=(rgb.min(2)>240)&(rgb.max(2)-rgb.min(2)<12);labels,n=ndimage.label(nearwhite);edge=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));arr[:,:,3]=np.where(np.isin(labels,edge[edge>0]),0,255);cut=Image.fromarray(arr)
 cut.save(A/(card+'-cutout.png'));x0,y0,x1,y1=box;head=x1-x0;h=y1-y0;cx=(x0+x1)/2
 # Match native portraits: hair/chin fills ~80% of the square; large view favours head and torso, not feet.
 side=max(head/.65,h/.80);top=y0-side*.07;small=cut.transform((128,128),Image.Transform.AFFINE,(side/128,0,cx-side/2,0,side/128,top),Image.Resampling.BICUBIC);small=clean(small);small.save(A/(card+'-small.png'))
 scale=70/h;w=184/scale;hh=256/scale;top=y0-14/scale;large=cut.transform((184,256),Image.Transform.AFFINE,(1/scale,0,cx-w/2,0,1/scale,top),Image.Resampling.BICUBIC);large=clean(large);large.save(A/(card+'-large.png'));rows.append({'id':card,'source_dimensions':list(im.size),'source_face_box':box,'mini_head_height_px':h*128/side,'large_head_height_px':70,'mini_dimensions':[128,128],'large_dimensions':[184,256],'same_scale_for_both_axes':True,'generated_face':False})
(P/'portrait-layouts.json').write_text(json.dumps(rows,indent=2));tiles=[]
for r in rows:
 card=r['id'];tile=Image.new('RGB',(220,430),'#182c44');big=Image.open(A/(card+'-large.png'));sm=Image.open(A/(card+'-small.png'));tile.paste(big,(18,5),big);tile.paste(sm,(46,270),sm);from PIL import ImageDraw;ImageDraw.Draw(tile).text((7,408),card,fill='white');tiles.append(tile)
can=Image.new('RGB',(220*len(tiles),430));[can.paste(im,(i*220,0))for i,im in enumerate(tiles)];can.save(A/'portrait-preview.jpg');print('PHOTOS_PREPARED')
