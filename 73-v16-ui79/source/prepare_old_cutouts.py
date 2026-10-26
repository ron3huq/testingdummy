exec(open('/tmp/73-ui79/prepare_portraits.py').read().split('rows=[]')[0])
from PIL import ImageDraw
rows=[];canvas=Image.new('RGB',(6*184,2*280),'#153142');d=ImageDraw.Draw(canvas)
for row in json.loads((P/'old-art.json').read_text()):
 pid=row['id']
 if pid in ['89135066911146','88044950524330']:continue
 im=Image.open(P/'art'/(pid+'-old.png')).convert('RGBA');out=cutout(im);a=np.array(out);# Keep the original portrait interior; alpha is the only edited channel.
 # Every supplied older card has its main face near upper centre. An inset ellipse protects the face from segmentation holes.
 yy,xx=np.mgrid[:im.height,:im.width];inside=((xx-im.width*.5)/(im.width*.19))**2+((yy-im.height*.29)/(im.height*.19))**2<1;a[:,:,3][inside]=255
 if pid=='106726716084650':
  # Preserve both source portraits; fade the large shirt naturally into the new background.
  shape=Image.new('L',im.size,0);painter=ImageDraw.Draw(shape);painter.polygon([(88,172),(100,174),(106,184),(103,194),(109,205),(106,214),(101,226),(94,234),(96,241),(105,255),(79,255),(76,248),(78,240),(73,231),(71,222),(66,223),(60,233),(56,244),(48,241),(51,233),(55,224),(56,216),(65,207),(69,195),(78,188)],fill=255);small=np.array(shape)>0;fade=np.clip((215-np.arange(im.height))/25,0,1)[:,None];alpha=a[:,:,3].astype('float32');alpha=np.where(small,alpha,alpha*fade);a[:,:,3]=alpha.astype('uint8')
 out=Image.fromarray(a);out.save(P/'art'/(pid+'-background-cutout.png'));n=len(rows);canvas.paste(out,((n%6)*184,(n//6)*280),out);d.text(((n%6)*184,(n//6)*280+258),pid,fill='white');rows.append(pid)
canvas.save(P/'art/old-background-cutouts.jpg');(P/'old-cutouts.json').write_text(json.dumps(rows));print('OLD_BACKGROUND_CUTOUTS',len(rows))
